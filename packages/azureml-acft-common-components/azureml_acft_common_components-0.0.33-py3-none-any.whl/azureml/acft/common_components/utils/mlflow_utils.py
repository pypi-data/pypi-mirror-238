# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""
This file defines the util functions related to mlflow
"""

from azureml.acft.common_components.utils.constants import MlflowMetaConstants


def fetch_mlflow_acft_metadata(
        is_finetuned_model: bool=True,
        base_model_name: str=None) -> dict:
    """ fetch metadata to be dumped in MlFlow MlModel File

    :param is_finetuned_model: whether the model is finetuned one or base model
    :type is_finetuned_model: bool
    :param is_acft_model: whether the model using acft packages
    :type is_acft_model: bool
    :param base_model_name: name of the model
    :type base_model_name: str

    :return: metadata
    :rtype: dict
    """

    metadata = {
        MlflowMetaConstants.IS_FINETUNED_MODEL : is_finetuned_model,
        MlflowMetaConstants.IS_ACFT_MODEL : True,
        MlflowMetaConstants.BASE_MODEL_NAME : base_model_name
    }

    return metadata
