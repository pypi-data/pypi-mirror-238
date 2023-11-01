import json
from io import BufferedReader, BufferedRandom
from os import PathLike
from pathlib import Path
import pyarrow.parquet as pq
from pyarrow.lib import ArrowInvalid
from typing import Dict, List, Optional, Union, Any

import arthurai
import numpy as np
from arthurai.common.constants import Stage, OutputType, ValueType


def check_has_bias_attrs(model):
    """
    Returns True if and only if the model has any attributes being monitored for bias by Arthur
    """
    for attr in model.attributes:
        if attr.monitor_for_bias:
            return True 
    return False


def check_attr_is_bias(model, attr_name: str):
    """
    Returns True if and only if the model has an attribute with the given name `attr_name` being monitored for bias by
    Arthur
    """
    attr = model.get_attribute(attr_name)
    return attr.monitor_for_bias


def get_positive_predicted_class(model):
    """
    Checks if model is a binary classifier. Returns False if multiclass, otherwise returns the name of the positive
    predicted attribute
    """
    if model.output_type != OutputType.Multiclass:
        return("Not a classifier model.")
    predicted_value_attributes = model.get_attributes(stage=Stage.PredictedValue)
    if len(predicted_value_attributes) != 2:
        return ("Not a binary classifier.")
    for attr in predicted_value_attributes:
        if attr.is_positive_predicted_attribute:
            return attr.name


"""
Token Sequence Output Type Related Helpers
"""

EPSILON = 1e-3


def tensors_to_arthur_inference(log_tensor: np.array, id_to_vocab: Dict[int, str], num_probs: int
                                ) -> List[Dict[str, float]]:
    """
    Convert an array of log probabilities with shape (sequence length, vocab size) to an Arthur Token Likelihoods
    formatted object.

    :param log_tensor: array of log probabilities for a generated sequence
    :param id_to_vocab: mapping from token ids to vocab strings
    :param num_probs: the number of tokens at each index in the sequence to include (up to 5)
    """
    if num_probs > 5:
        raise ValueError("num_probs must be <= 5")

    # TODO: this function should probably be batch
    if log_tensor.ndim != 2:
        raise ValueError("expected token probabilities to be two-dimensional")

    arthur_likelihoods = []
    probabilities = np.exp(log_tensor)
    invalid_probs = np.abs(np.sum(probabilities, axis=1) - 1) >= EPSILON
    if np.sum(invalid_probs) != 0:
        raise ValueError("all token probabilities must sum to 1")

    # get num_probs argmax
    top_indices = np.argpartition(probabilities, -num_probs, axis=1)[:, -num_probs:]
    top_values = probabilities[np.vstack(np.arange(len(probabilities))), top_indices]
    for v, i in zip(top_values, top_indices):
        arthur_likelihoods.append({id_to_vocab[index]: value.item() for value, index in zip(v, i)})
    return arthur_likelihoods


def _text_attr(name: str, stage: Stage):
    return arthurai.ArthurAttribute(
        name=name,
        stage=stage,
        position=0,
        categorical=True,
        value_type=ValueType.Unstructured_Text,
        is_unique=False if stage == Stage.PredictedValue else True
    )


def _tokens_attr(name: str, stage: Stage, position: int = 0):
    return arthurai.ArthurAttribute(
        name=name,
        stage=stage,
        value_type=ValueType.Tokens,
        categorical=False,
        is_unique=False,
        position=position
    )


def _token_likelihoods_attr(name: str, position: int = 0):
    return arthurai.ArthurAttribute(
        name=name,
        stage=Stage.PredictedValue,
        value_type=ValueType.TokenLikelihoods,
        categorical=False,
        is_unique=False,
        position=position
    )


def _image_attr(name: str):
    return arthurai.ArthurAttribute(
        name=name,
        stage=Stage.ModelPipelineInput,
        value_type=ValueType.Image,
        categorical=False,
        position=0
    )


def _get_json_data(file_path: Union[str, Path, PathLike, BufferedReader, BufferedRandom]) -> Optional[Any]:
    """Gets data from json file

    Also validates file_path refers to a json file.

    :param file_path: path of json file
    :return: Python object with loaded json data, None if file_path does not refer to a json file
    """
    if isinstance(file_path, (str, Path, PathLike)):
        if not str(file_path).endswith('.json'):
            return None
        with open(file_path, "r") as json_file:
            json_data = json.loads(json_file.read())
    else:
        try:
            json_data = json.loads(file_path.read())
        except UnicodeDecodeError:
            return None
    return json_data


def _get_parquet_file(file_path: Union[str, Path, PathLike, BufferedReader, BufferedRandom]) -> Optional[pq.ParquetFile]:
    """Gets ParquetFile from parquet file

    Also validates file_path refers to a parquet file.

    :param file_path: path of parquet file
    :return: ParquetFile corresponding to file_path, None if file_path does not refer to a parquet file
    """
    try:
        return pq.ParquetFile(file_path)
    except (ArrowInvalid, TypeError):
        return None
