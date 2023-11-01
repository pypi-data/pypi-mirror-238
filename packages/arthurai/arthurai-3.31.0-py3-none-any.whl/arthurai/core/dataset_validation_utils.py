import datetime
from dateutil.parser import parse, ParserError
import logging
import re
from typing import Any

import numpy as np
import pandas as pd
from pandas import Series
from pandas.core.dtypes.common import is_float_dtype

from arthurai import ArthurAttribute, util as arthur_util
from arthurai.common.constants import ValueType
from arthurai.common.exceptions import UnexpectedTypeError, UnexpectedValueError, UserTypeError, UserValueError
from arthurai.core.util import NumpyEncoder, is_bool_like, is_date_like, is_float_like, is_int_like, is_list_like, \
    is_str_like, is_valid_datetime_obj, can_cast

logger = logging.getLogger(__name__)


def validate_series_data_type(series: Series, attr: ArthurAttribute) -> None:
    """ Validates if the series data type matches the attribute's Arthur value type

    Raises a UserTypeError if there is a data type mismatch where the series data type is not valid for the
    passed attribute's value type. Logs a warning if the series data type cannot be inferred because of None objects
    or empty lists or dicts.

    :param series: the Series to infer the data type from
    :param attr: the ArthurAttribute that the Series corresponds to
    :raises: UnexpectedValueError: A parameter is None.
    :raises: UserTypeError: Found data type mismatch between series and attr.
    """

    if series is None or attr is None:
        raise UnexpectedValueError("Parameter was None.")

    # standardize series
    series = series.replace([np.inf, -np.inf], np.nan)
    nans_present = series.isnull().values.any()
    series = series.dropna()
    if len(series) != 0:
        if is_float_dtype(series) and nans_present and attr.value_type == ValueType.Integer:
            if len(series) > 0 and np.array_equal(series, series.astype(int)):  # int col with nans received as floats
                series = series.astype(pd.Int64Dtype())

        # validate data type mismatch
        sample_datum = series.iloc[0]
        ensure_obj_matches_attr_value_type(sample_datum, attr.value_type, attr.name)
    else:
        logger.warning(f"The data type of column {attr.name} cannot be validated because the column only has "
                       f"None objects.")


def obj_value_type_mismatch_err(attr_name: str, expected: str, obj_type: str) -> UserTypeError:
    """ Returns UserTypeError with data type mismatch message
    :param: attr_name: Name of attribute whose value type has been mismatched with a column's data type
    :param: expected: String representing expected data type for the attribute
    :param: obj_type: String representing the object type that didn't match expected
    :raises: UnexpectedTypeError: Parameter was unexpectedly a None object.
    :returns: UserTypeError with mismatch message.
    """
    if attr_name is None or expected is None or obj_type is None:
        raise UnexpectedTypeError("Cannot pass None parameters.")
    return UserTypeError(f"Expected {expected} data type for attribute {attr_name} but got object of type {obj_type}. "
                         f"Please correct the data type mismatch by changing either the value_type field of the "
                         f"attribute or the data type of the column.")


def ensure_obj_matches_attr_value_type(obj: Any, value_type: ValueType, source: str) -> None:
    """ Validates the object data type matches the Arthur value type

    Raises a UserTypeError if the object data type does not match any valid data type corresponding to
    the Arthur Value Type of the passed attribute.

    :param obj: Object whose data type should be compared
    :param value_type: ValueType to validate against obj
    :param source: String representation of source of data for clear error messages
    :raises: UserTypeError when obj's data type does not match attr's value_type Value Type.
    """
    if source is None or obj is None or value_type is None:
        raise UnexpectedTypeError("Cannot pass None parameters.")

    if value_type == ValueType.Float:
        if not is_float_like(obj):
            raise obj_value_type_mismatch_err(source, "float", str(type(obj)))
    elif value_type == ValueType.Integer:
        if not is_int_like(obj):
            raise obj_value_type_mismatch_err(source, "int", str(type(obj)))
    elif value_type == ValueType.String or value_type == ValueType.Image or \
            value_type == ValueType.Unstructured_Text:
        if not is_str_like(obj):
            raise obj_value_type_mismatch_err(source, "str", str(type(obj)))
        elif value_type == ValueType.String and is_valid_datetime_obj(obj):  # validate str obj isn't a valid timestamp
            raise UserTypeError(f"Column {source} parses to valid timestamps but its attribute value_type is "
                                f"{ValueType.String}, not {ValueType.Timestamp}. Please change the attribute "
                                f"value_type and ensure the column consists of timezone aware Datetime objects.")
        elif can_cast(float, obj) or can_cast(int, obj):
            logger.warning(f"Column {source} has a attribute value_type of {ValueType.String} and its data are "
                           f"string objects, but at least one of its data parses to a valid int or float. Consider "
                           f"casting the column's data to integer or float types and changing the attribute "
                           f"value_type if all the data are numbers.")
    elif value_type == ValueType.Boolean:
        if not is_bool_like(obj):
            raise obj_value_type_mismatch_err(source, "bool", str(type(obj)))
    elif value_type == ValueType.Timestamp:
        if not is_date_like(obj):
            raise obj_value_type_mismatch_err(source, "datetime or pd.Timestamp", str(type(obj)))
        else:
            datetime_obj = NumpyEncoder.convert_value(obj)
            arthur_util.format_timestamp(datetime_obj, col_name=source)
    elif value_type == ValueType.Tokens:  # expected type is list[str]
        list_obj = get_first_elem_if_valid_list(obj, source, "list[str]")  # validates list
        if list_obj is not None and not is_str_like(list_obj):  # validates list element
            raise obj_value_type_mismatch_err(source, "list[str]", f"list[{str(type(list_obj))}]")
    elif value_type == ValueType.TokenLikelihoods:
        validate_token_likelihoods_type(obj, source)
    elif value_type == ValueType.BoundingBox:  # expected type is list[list[Union[float, int]]]
        list_obj = get_first_elem_if_valid_list(obj, source, "list[list[Union[int, float]]]")
        if list_obj is not None:
            if not is_list_like(list_obj):
                raise obj_value_type_mismatch_err(source, "list[list[Union[int, float]]]",
                                                  f"list[{str(type(list_obj))}]")
            elif len(list_obj) != 6 and not len(list_obj) == 0:  # warning logged in _get_first_elem_if_valid_list if length is 0
                raise UserValueError(f"Bounding box column {source} should have six values in the nested "
                                     f"list but an entry in your column had {len(list_obj)} values. For a full "
                                     f"description of Arthur's bounding box format see: "
                                     f"https://docs.arthur.ai/docs/cv-onboarding#formatting-bounding-boxes.")
            else:  # validate inner list
                nested_obj = get_first_elem_if_valid_list(list_obj, source,
                                                          "list[list[Union[int, float]]]", "list")
                if nested_obj is not None and not (is_float_like(nested_obj) or is_int_like(nested_obj)):
                    raise obj_value_type_mismatch_err(source, "list[list[Union[int, float]]]",
                                                      f"list[list[{str(type(nested_obj))}]]")

def get_first_elem_if_valid_list(obj: Any, source: str, expected: str, outer_type: str = "") -> Any:
    """ Validates obj is list-like and non-empty and returns the first element.

    Raises a UserTypeError if obj is not list-like (is not a numpy array or python list). Logs a warning if the
    length of the list is 0 or the list has a None object.

    :param: obj: Object whose data type is being checked.
    :param: attr_name: String source of the object for clear error messages.
    :param: expected: String of expected type of the object for clear error messages.
    :param: outer_type: String representing the data type of the object obj was nested in for clear error messages. Defaults to empty string.
    :raises: UserTypeError if obj is not list-like.
    :returns: first element if obj is a list, None otherwise
    """
    if obj is None or source is None or expected is None or outer_type is None:
        raise UnexpectedValueError("Parameters cannot be None.")

    if not is_list_like(obj):  # validate list type
        if outer_type != "":
            raise obj_value_type_mismatch_err(source, expected, outer_type + "[" + str(type(obj)) + "]")
        else:
            raise obj_value_type_mismatch_err(source, expected, str(type(obj)))
    list_obj = NumpyEncoder.convert_value(obj)
    if outer_type != "":
        outer_type = " nested"
    if len(list_obj) == 0:
        logger.warning(f"The length of the first{outer_type} list in {source} was 0. If you are using lists to "
                       f"represent missing values instead of None objects, please change your empty lists to None "
                       f"objects. The type of the list cannot be inferred from a zero-length list, so the data type "
                       f"of {source} cannot be validated.")
        return None
    elif obj[0] is None:
        logger.warning(f"The first element in the first{outer_type} list in {source} was None. The type of the list cannot be "
                       f"inferred from a None object, so the data type of {source} cannot be validated.")
        return None
    else:
        return list_obj[0]


def validate_token_likelihoods_type(obj: Any, source: str) -> None:
    """ Validates obj data type matches TokenLikelihoods Value Type

    Raises a UserTypeError if the object's data type does not match any valid data type corresponding to the
    TokenLikelihoods Value Type. Logs a warning if any of the nested types—list, dict, or dict keys—are length 0
    or None objects. The valid data type for TokenLikelihoods is list[dict[str, Union[int, float]]].
    :param obj: Object to validate.
    :param source: String representation of the source of obj for clear error messages.
    :raises: UserTypeError when obj's data type does not match a TokenLikelihoods Value Type data type.
    """
    if obj is None or source is None:
        raise UnexpectedTypeError("Parameters cannot be None.")
    list_obj = get_first_elem_if_valid_list(obj, source, "list[dict[str, Union[int, float]]]")
    if list_obj is not None:  # validate list element type is dict
        if not isinstance(list_obj, dict):
            raise obj_value_type_mismatch_err(source, "list[dict[str, Union[int, float]]]",
                                              f"list[{str(type(list_obj))}]")
        if len(list_obj) == 0:
            logger.warning(f"The first dict in the first list in {source} was empty. The data type "
                           f"cannot be validated for this column because no type can be inferred for the dictionary "
                           f"keys or values.")
        else:  # validate key and value types of dict
            key, val = next(iter(list_obj.items()))
            if key is None or val is None:
                logger.warning(f"A key or value in the first dict in the first list in {source} was None. The data "
                               f"type cannot be validated for this column because a type can't be inferred from a "
                               f"None object.")
            elif not is_str_like(key):
                raise obj_value_type_mismatch_err(source, "list[dict[str, Union[int, float]]]",
                                                  f"list[dict[{str(type(key))}, {str(type(val))}]]")
            elif not (is_float_like(val) or is_int_like(val)):
                raise obj_value_type_mismatch_err(source, "list[dict[str, Union[int, float]]]",
                                                  f"list[dict[str, {str(type(val))}]]")



def validate_attr_names(col_names: pd.Index) -> None:
    """ Validates attribute names are correctly formatted

    Validates attribute names are made of alphanumeric characters and underscores and don't start with a number.

    :param: col_names: pd.Index of attribute names to be checked
    :raises: UserValueError: At least one attribute name is not correctly formatted
    """
    attr_name_regex = re.compile(r'^[A-Za-z_][A-Za-z0-9_]+$')
    misformatted_cols = []
    for col in col_names:
        if not attr_name_regex.match(col):
            misformatted_cols.append(col)
    if len(misformatted_cols) != 0:
        raise UserValueError(f"The following column names are misformatted: {str(misformatted_cols)[1:-1]}. Please "
                             f"ensure each name consists of only alphanumeric characters and underscores and "
                             f"doesn't start with a number.")


def valid_rec_obj(obj: Any) -> bool:
    """Validates recommendation object formatting

    Validates obj is a dict with an "item_id" key that has a string value
    :returns: True if obj meets criteria, False otherwise
    """
    return isinstance(obj, dict) and is_str_like(dict(obj).get("item_id"))
