# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Common callbacks for all vetricals."""

import os
import json
import shutil

from transformers.trainer_callback import TrainerCallback, TrainerControl, TrainerState
from transformers.trainer import TrainingArguments, get_last_checkpoint

from azureml.acft.common_components.model_selector.constants import ModelSelectorDefaults, ModelSelectorConstants


class SaveExtraFilesToCheckpoints(TrainerCallback):
    """save extrafiles to checkpoint folder for image/multimodal verticals."""

    def __init__(self, model_name: str,
                 input_model_path: str,
                 pytorch_output_folder: str) -> None:
        """
        :param model_name: name of the model
        :type model_name: str
        :param input_model_path: path of the input model
        :type input_model_path: str
        :param input_model_path: path of pytorch output
        :type input_model_path: str

        :return: None
        :rtype: None
        """
        super().__init__()
        self.model_name = model_name
        self.input_model_metadata_path = os.path.join(input_model_path, ModelSelectorDefaults.MODEL_METADATA_PATH)
        self.input_model_defaults_path = os.path.join(input_model_path, ModelSelectorDefaults.MODEL_DEFAULTS_PATH)
        self.pytorch_output_folder = pytorch_output_folder

    def save_files(self, output_dir: str) -> None:
        """Save required files in the folder specified.

        :param output_dir: path of the directory for dumping files
        :type output_dir: str

        :return: None
        :rtype: None
        """
        op_metadata_path = os.path.join(output_dir, ModelSelectorDefaults.MODEL_METADATA_PATH)
        if os.path.isfile(self.input_model_metadata_path):
            shutil.copy(self.input_model_metadata_path, op_metadata_path)
        else:
            metadata = {ModelSelectorConstants.MODEL_NAME: self.model_name}
            with open(op_metadata_path, 'w') as f:
                json.dump(metadata, f)

        op_modeldefaults_path = os.path.join(output_dir, ModelSelectorDefaults.MODEL_DEFAULTS_PATH)
        if os.path.isfile(self.input_model_defaults_path):
            shutil.copy(self.input_model_defaults_path, op_modeldefaults_path)

    def on_save(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs) -> None:
        """Callback called after saving each checkpoint.
        :param args: training arguments
        :type args: TrainingArguments (transformers.TrainingArguments)
        :param state: trainer state
        :type state: TrainerState (transformers.TrainerState)
        :param control: trainer control
        :type control: TrainerControl (transformers.TrainerControl)
        :param kwargs: keyword arguments
        :type kwargs: dict

        :return: None
        :rtype: None
        """
        last_checkpoint_folder = get_last_checkpoint(args.output_dir)
        if args.should_save:  # save only on rank-0
            self.save_files(last_checkpoint_folder)

    def on_train_end(self, args: TrainingArguments, state: TrainerState, control: TrainerControl, **kwargs) -> None:
        """Callback called at the end of training.
        :param args: training arguments
        :type args: TrainingArguments (transformers.TrainingArguments)
        :param state: trainer state
        :type state: TrainerState (transformers.TrainerState)
        :param control: trainer control
        :type control: TrainerControl (transformers.TrainerControl)
        :param kwargs: keyword arguments
        :type kwargs: dict

        :return: None
        :rtype: None
        """

        if args.should_save:  # save only on rank-0
            self.save_files(self.pytorch_output_folder)
