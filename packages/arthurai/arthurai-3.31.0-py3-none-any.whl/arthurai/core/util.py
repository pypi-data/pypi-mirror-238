import json
import logging
import os
from datetime import datetime, MINYEAR, MAXYEAR
from pathlib import Path
from typing import Dict, Optional, Union, Any, List, Sequence, Iterable

import numpy as np
import pandas as pd
from dateutil.parser import parse, ParserError
from pandas import Series, DataFrame
from pandas.api.types import is_datetime64_any_dtype, is_float_dtype

import arthurai.util as arthur_util
from arthurai.common.constants import ValueType
from arthurai.common.exceptions import UnexpectedValueError, UnexpectedTypeError, UserTypeError

logger = logging.getLogger(__name__)


def retrieve_parquet_files(directory_path: str) -> List[Path]:
    """Checks whether a given directory and its subdirectories contain parquet files,
    if so this will return a list of the files

    :param directory_path: local path to check files types

    :return: List of paths for parquet files that are found
    """
    return _retrieve_files_with_specified_extension(directory_path, '.parquet')


def retrieve_json_files(directory_path: str) -> List[Path]:
    """Checks whether a given directory and its subdirectories contain json files,
    if so this will return a list of the files

    :param directory_path: local path to check files types

    :return: List of paths for json files that are found
    """
    return _retrieve_files_with_specified_extension(directory_path, '.json')


def _retrieve_files_with_specified_extension(directory_path: str, extension: str) -> List[Path]:
    """Checks whether a given directory and its subdirectories contain files with the specified extension,
    if so this will return a list of the files

    :param directory_path: local path to check files types
    :param extension: specific extension to check files for

    :return: List of paths for files that are found
    """
    desired_files = []
    for path, subdir, files in os.walk(directory_path):
        for file in files:
            if str(file).endswith(extension):
                desired_files.append(Path(os.path.join(path, file)))
    return desired_files


class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """

    @staticmethod
    def convert_value(obj):
        """Converts the given object from a numpy data type to a python data type, if the object is already a
        python data type it is returned

        :param obj: object to convert
        :return: python data type version of the object
        """
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return pd.Timestamp.to_pydatetime(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.datetime64):
            return obj.item()
        elif isinstance(obj, np.str_):
            return str(obj)
        elif isinstance(obj, float) and np.isnan(obj):
            return None
        return obj


def standardize_pd_obj(data: Union[pd.DataFrame, pd.Series], dropna: bool, replacedatetime: bool,
                       attributes: Optional[Dict[str, Union[str, ValueType]]] = None) -> Union[pd.DataFrame, pd.Series]:
    """Standardize pandas object for nans and datetimes.

    Standardization includes casting correct type for int columns that are float due to nans and 
    for converting datetime objects into isoformatted strings.

    :param data: the pandas data to standardize
    :param dropna: if True, drop nans from numeric columns
    :param replacedatetime: if True, replace timestamps with isoformatted strings
    :param attributes: if used for sending inferences, will handle column type conversions for columns with any nulls


    :return: the standardized pandas data
    :raises TypeError: timestamp is not of type `datetime.datetime`
    :raises ValueError: timestamp is not timezone aware and no location data is provided to remedy
    """

    def standardize_pd_series(series: pd.Series, datatype: Optional[str]) -> pd.Series:
        series = series.replace([np.inf, -np.inf], np.nan)
        nans_present = series.isnull().values.any()
        if dropna:
            series = series.dropna()

        if len(series) == 0:
            return series

        # Case 1: int column which has nans and there therefore seen as a float column
        if is_float_dtype(series) and nans_present and datatype == ValueType.Integer:
            valid_series = series.dropna()
            if len(valid_series) > 0 and np.array_equal(valid_series, valid_series.astype(int)):
                return series.astype(pd.Int64Dtype())
        # Case 2: datetime column or string column which are all datetime objects
        elif is_datetime64_any_dtype(series) or arthur_util.is_valid_datetime_string(series.values[0]):
            formatted_series = series.apply(arthur_util.format_timestamp)
            if replacedatetime:
                return formatted_series

        return series

    if isinstance(data, pd.Series):
        datatype = None
        if attributes and data.name in attributes:
            datatype = attributes[data.name]
        return standardize_pd_series(data, datatype)

    elif isinstance(data, pd.DataFrame):
        if dropna:
            raise UnexpectedValueError(f"Cannot use dropna={dropna} with data argument as pd.DataFrame.")
        df = data.copy()
        for column in df.columns:
            datatype = None
            if attributes and column in attributes:
                datatype = attributes[column]
            df[column] = standardize_pd_series(df[column], datatype)
        return df

    else:
        raise UnexpectedTypeError("Cannot standardize object that is not pd.DataFrame or pd.Series.")


def dataframe_like_to_list_of_dicts(data: Union[List[Dict[str, Any]], Dict[str, List[Any]], pd.DataFrame]):
    """
    Standardize data in a List of Dicts format (e.g. `[{'a': 1, 'b': 2}, {'a': 3, 'b': 4}]`). Input can be formatted as
    a List of Dicts, Dict of Lists (e.g. `{'a': [1, 3], 'b': [2, 4]}`), or a Pandas DataFrame. May return the same
    object as input if it already matches the correct format.
    :param data: the input data to format
    :return: the data restructured as a Dict of Lists
    :raises UserTypeError: if the data is in an unexpected format
    """
    if len(data) == 0:
        return []

    if isinstance(data, list) and isinstance(data[0], dict):
        return data
    elif isinstance(data, dict):
        data = pd.DataFrame(data)

    if isinstance(data, pd.DataFrame):
        return data.to_dict(orient='records')
    else:
        raise UserTypeError(f"Invalid input type {type(data)}, should be list of dicts, dict of lists, or DataFrame")


def update_column_in_list_of_dicts(data: List[Dict[str, Any]], target_column: str, column_values: Sequence[Any]) -> \
        None:
    """
    Adds column_values to target_column in a list of dicts **in place**. If values are present for target_column, they are
    overwritten.
    :param data: the List of Dict data to modify
    :param target_column: the name of the column to write values into
    :param column_values: the values to write
    :return: None (in place)
    :raises UserValueError: if the lengths don't match or aren't retrievable
    """
    try:
        if len(column_values) != len(data):
            raise ValueError(f"The dataset has {len(data)} elements but column {target_column} has "
                             f"{len(column_values)} elements. Cannot add values to data.")
    except TypeError:
        raise UserTypeError(f"Cannot compare lengths of data and values for column {target_column}, are you sure the "
                            "values have a definite length?")
    for i in range(len(data)):
        data[i][target_column] = column_values[i]


def intersection_is_non_empty(iter1: Iterable[Any], iter2: Iterable[Any]):
    """
    Returns True if the two iterables share at least one element
    :param iter1:
    :param iter2:
    :return:
    """
    for val in iter1:
        if val in iter2:
            return True
    return False


def is_float_like(obj: Any) -> bool:
    """
    Returns True if obj is a numpy or Python float, False if not
     """
    return isinstance(obj, np.floating) or isinstance(obj, float)


def is_int_like(obj: Any) -> bool:
    """ Returns True if obj is a numpy or Python int, False if not """
    return (isinstance(obj, np.integer) or isinstance(obj, int)) and not (isinstance(obj, np.bool_) or isinstance(obj, bool))


def is_str_like(obj: Any) -> bool:
    """ Returns True if obj is a numpy or Python String, False if not """
    return isinstance(obj, np.str_) or isinstance(obj, str)


def is_bool_like(obj: Any) -> bool:
    """ Returns True if obj is a numpy or Python bool, False if not """
    return isinstance(obj, np.bool_) or isinstance(obj, bool)


def is_date_like(obj: Any) -> bool:
    """ Returns True if obj is a numpy or Python datetime object or a pandas Timestamp, False if not """
    return isinstance(obj, np.datetime64) or isinstance(obj, datetime) or isinstance(obj, pd.Timestamp)


def is_list_like(obj: Any) -> bool:
    """ Returns True if obj is a numpy ndarray or Python list, False if not """
    return isinstance(obj, np.ndarray) or isinstance(obj, list)


def is_valid_datetime_obj(obj: str) -> bool:
    """ Returns True if obj can be parsed to a valid Datetime object, False if not

    obj must be a complete Datetime object (at least include day, month, and year). Note: this is necessary until
    dateutil.parser.parse(obj, default=None) works (open issue here: https://github.com/dateutil/dateutil/issues/1253).
    """
    try:
        parsed_dt = parse(obj, default=datetime(MINYEAR, 1, 1))
    except (ParserError, OverflowError):  # obj is not a timestamp
        return False

    # if parse returns the same Datetime object when an object is parsed with two different default dates, that means
    # all the day, month, and year fields got overwritten, so they are present in obj. If parse returns a different
    # Datetime object for different defaults then at least one of the defaults was used, so obj is not a complete
    # Datetime object
    return True if parsed_dt == parse(obj, default=datetime(MAXYEAR, 2, 2)) else False


def can_cast(cast_type: type, obj: Any) -> bool:
    """Returns True if obj can be cast to cast_type, False if not"""
    try:
        cast_type(obj)
    except (ValueError, OverflowError):
        return False
    return True


def series_to_df(data: Union[Series, DataFrame]) -> DataFrame:
    """Converts pandas Series to DataFrame

    Validates data is Series or DataFrame type and converts to DataFrame if it is a Series. Returns original object if
    data is already a DataFrame.

    :param data: data to be validated and converted to DataFrame
    :return: data as DataFrame
    :raises UserTypeError: data is not of Series or DataFrame type
    """
    if isinstance(data, Series):
        return data.to_frame()
    elif isinstance(data, DataFrame):
        return data
    else:
        raise UserTypeError("Unsupported data type: a pandas.DataFrame or pandas.Series is required")
