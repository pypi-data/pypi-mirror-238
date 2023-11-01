import filecmp
import io
import json
import logging
import os

from datetime import datetime, timezone, MINYEAR, MAXYEAR
from http import HTTPStatus
from pathlib import Path, PurePath
from queue import Queue
import shutil

import numpy as np
import pandas as pd
import pytest
import responses
from mock import MagicMock, mock_open, patch

import arthurai.core.util as core_util
from arthurai.common.constants import ImageContentType, ImageResponseType, InputType, ModelStatus, ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE, \
    OutputType, Stage, ValueType
from arthurai.common.exceptions import ArthurUnexpectedError, MethodNotApplicableError, UserTypeError, UserValueError
from arthurai.core.attributes import ArthurAttribute, AttributeBin, AttributeCategory
from arthurai.core.dataset_validation_utils import ensure_obj_matches_attr_value_type, validate_attr_names, validate_series_data_type
from arthurai.core.inferences import nest_reference_data
from arthurai.core.models import ArthurModel, ArthurModelGroup
from http import HTTPStatus
from mock import patch, mock_open, MagicMock

from tests.fixtures.mocks import client
from tests.fixtures.models import multiclass as mclass, nlp, regression as reg, ranked_list as rlist
from tests.fixtures.models.multiclass import MODEL_DATA_WITH_ATTRIBUTES_IMPLICIT_NEG, SAMPLE_DATAFRAME_NO_NEG_PRED, \
    initial_biclass_model
from tests.fixtures.models.ranked_list import ranked_list_model
from tests.fixtures.models.regression import initial_batch_model as reg_initial_batch_model, \
    unsaved_batch_model as reg_unsaved_batch_model, streaming_model
from tests.fixtures.models.nlp import initial_nlp_classification_model, initial_nlp_regression_model, \
    initial_nlp_sequence_model
from tests.fixtures.models.regression import initial_batch_model as reg_initial_batch_model, streaming_model, \
    unsaved_batch_model as reg_unsaved_batch_model
from tests.helpers import assert_attributes_equal, generate_rec_ranked_list, generate_unique_str_list, mock_get, \
    mock_patch, mock_post
from tests.test_request_models import load_json, load_json_string
from tests.test_request_models.fixtures import model_response_json_strings

MODEL_RESPONSE_JSON = [
    load_json(
        os.path.join(os.path.dirname(__file__), 'test_request_models', 'resources', 'model_with_categories.json')),
    load_json(
        os.path.join(os.path.dirname(__file__), 'test_request_models', 'resources', 'model_with_attributes.json'))
]

MODEL_GROUP_ID = "01234567-89ab-cdef-0123-456789abcdef"
MODEL_GROUP_NAME = "Test Model Group"
MODEL_GROUP_DESCRIPTION = "Test Model Group Description"
MODEL_GROUP_ARCHIVED = False
MODEL_GROUP_CREATED_AT = "2022-01-20T23:22:18.185267Z"
MODEL_GROUP_UPDATED_AT = "2022-01-20T23:22:32.914068Z"
MODEL_GROUP_JSON = {
    "id": MODEL_GROUP_ID,
    "name": MODEL_GROUP_NAME,
    "description": MODEL_GROUP_DESCRIPTION,
    "archived": MODEL_GROUP_ARCHIVED,
    "created_at": MODEL_GROUP_CREATED_AT,
    "updated_at": MODEL_GROUP_UPDATED_AT,
    "versions": MODEL_RESPONSE_JSON
}


@pytest.mark.parametrize('model_filename,expected_string', [
    ('model_with_attributes.json', "Tabular Regression Model\n"
                                   "\tFICO Score:3456\n"
                                   "\tStage: Production\n"
                                   "\tAttributes: ['PIPELINE_INPUT[2]:attr_3']"),
    ('model_multiclass_with_bias.json', "Tabular Multiclass Model\n"
                                        "\ttest model 1:1113\n"
                                        "\tStage: Production\n"
                                        "\tAttributes: ['NON_INPUT_DATA[0]:bias', 'PREDICTED_VALUE[0]:attr_1', 'PREDICTED_VALUE[1]:attr_2', 'PREDICTED_VALUE[2]:attr_3']")
])
def test__str__(model_filename, expected_string):
    model_json = load_json_string(
        os.path.join(os.path.dirname(__file__), 'test_request_models', 'resources', model_filename))
    model = ArthurModel.from_json(model_json)
    assert str(model) == expected_string


@responses.activate
def test_send_parquet_file():
    input_dict = {
        "attr1": np.Inf,
        "attr2": "string1",
        "attr3": 3.44,
        "attr4": True,
        "attr5": np.nan,
        "attr6": -np.inf,
        "attr7": "string2",
        "attr8": None,
        "attr9": "",
        "attr10": np.inf,
    }
    expected_dict = {
        "attr1": None,
        "attr2": "string1",
        "attr3": 3.44,
        "attr4": True,
        "attr5": None,
        "attr6": None,
        "attr7": "string2",
        "attr8": None,
        "attr9": "",
        "attr10": None,
    }
    output_dict = ArthurModel._replace_nans_and_infinities_in_dict(input_dict)
    assert expected_dict == output_dict


def test_replace_nans_none_type():
    output_dict = ArthurModel._replace_nans_and_infinities_in_dict(None)
    assert output_dict is None


def test_standardize_pd_obj_for_nans():
    input_df = pd.DataFrame(
        [
            [1, 2, 3., 4, 5, 6, np.inf, np.nan, 1, 1],
            [7, 8, 9., 1, 2, 3, np.nan, -np.inf, 2, 2],
            [4, 5.5, 9., -np.inf, np.nan, np.Inf, np.nan, np.nan, np.nan, np.nan],
        ],
        columns=["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"]
    )
    expected_df = pd.DataFrame(
        [
            [1, 2, 3., 4, 5, 6, np.nan, np.nan, 1, 1],
            [7, 8, 9., 1, 2, 3, np.nan, np.nan, 2, 2],
            [4, 5.5, 9., np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
        ],
        columns=["x0", "x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9"]
    )
    expected_df.x3 = expected_df.x3.astype(pd.Int64Dtype())
    expected_df.x4 = expected_df.x4.astype(pd.Int64Dtype())
    expected_df.x5 = expected_df.x5.astype(pd.Int64Dtype())

    attributes = {
        "x3": ValueType.Integer,
        "x4": ValueType.Integer,
        "x5": ValueType.Integer,
        "x8": ValueType.Float,
    }

    assert expected_df.equals(
        core_util.standardize_pd_obj(input_df, dropna=False, replacedatetime=False, attributes=attributes)
    )
    with pytest.raises(ValueError):
        assert expected_df.equals(
            core_util.standardize_pd_obj(input_df, dropna=True, replacedatetime=False, attributes=attributes)
        )


def test_standardize_pd_obj_for_series():
    input_series = [
        pd.Series([1, 2, 3]),
        pd.Series([1., 2., 3.]),
        pd.Series([1, 2, np.Inf], name="x1"),
        pd.Series([1, 2, np.Inf], name="x1"),
        pd.Series([1, 2, np.Inf], name="x1"),
        pd.Series([np.nan, -np.inf, np.inf]),
    ]
    input_attributes = [
        {},
        None,
        {"x1": ValueType.Integer},
        {"x1": ValueType.Float},
        {"x2": ValueType.Integer},
        {}
    ]
    expected_undropped_series = [
        pd.Series([1, 2, 3]),
        pd.Series([1., 2., 3.]),
        pd.Series([1, 2, np.nan]).astype(pd.Int64Dtype()),
        pd.Series([1, 2, np.nan]),
        pd.Series([1, 2, np.nan]),
        pd.Series([np.nan, np.nan, np.nan]),
    ]
    expected_dropped_series = [
        pd.Series([1, 2, 3]),
        pd.Series([1., 2., 3.]),
        pd.Series([1, 2]).astype(pd.Int64Dtype()),
        pd.Series([1, 2.]),
        pd.Series([1, 2.]),
        pd.Series([]),
    ]

    for inp, inp_attributes, exp_undropped, exp_dropped in zip(input_series, input_attributes,
                                                               expected_undropped_series, expected_dropped_series):
        print(inp_attributes)
        assert exp_undropped.equals(
            core_util.standardize_pd_obj(inp, dropna=False, replacedatetime=False, attributes=inp_attributes)
        )
        assert exp_dropped.equals(
            core_util.standardize_pd_obj(inp, dropna=True, replacedatetime=False, attributes=inp_attributes)
        )


def test_standardize_pd_obj_bad_input():
    for inp in ["string", "", 123, [1, 2, 3], {"key": "value"}]:
        with pytest.raises(TypeError):
            core_util.standardize_pd_obj(inp, dropna=True, replacedatetime=False)


def test_standardize_pd_obj_for_datetimes():
    unaware_timestamp = datetime(2021, 2, 8, 12, 10, 5)
    aware_timestamp = datetime(2021, 2, 8, 12, 10, 5, tzinfo=timezone.utc)
    timestamp_to_expected_output = (
        (unaware_timestamp, ValueError),
        (aware_timestamp, "2021-02-08T12:10:05+00:00"),
    )

    for timestamp, expected_output in timestamp_to_expected_output:
        if isinstance(expected_output, str):
            actual_output = core_util.standardize_pd_obj(pd.Series([timestamp]), dropna=False, replacedatetime=True)
            assert expected_output == actual_output.values[0]
        else:
            with pytest.raises(expected_output):
                core_util.standardize_pd_obj(pd.Series([timestamp]), dropna=False, replacedatetime=True)


def test_add_attribute_with_categories():
    model = ArthurModel.from_json(model_response_json_strings[2])
    model.add_attribute(
        name="test_categorical_1",
        value_type=ValueType.Integer,
        stage=Stage.ModelPipelineInput,
        categorical=True,
        categories=[1, 2, 3, 4],
    )
    attr = model.get_attribute(name="test_categorical_1")
    assert len(attr.categories) == 4
    assert isinstance(attr.categories[0], AttributeCategory)

    model.add_attribute(
        name="test_categorical_2",
        value_type=ValueType.Integer,
        stage=Stage.ModelPipelineInput,
        categorical=True,
        categories=[AttributeCategory(value="hello")],
    )
    attr = model.get_attribute(name="test_categorical_2")
    assert len(attr.categories) == 1
    assert isinstance(attr.categories[0], AttributeCategory)
    assert attr.categories[0].value == "hello"


def test_add_attribute_with_bins():
    model = ArthurModel.from_json(model_response_json_strings[2])
    model.add_attribute(
        name="test_bins_1",
        value_type=ValueType.Integer,
        stage=Stage.ModelPipelineInput,
        categorical=True,
        bins=[None, 10, 15, 20, None],
    )
    attr = model.get_attribute(name="test_bins_1")
    assert len(attr.bins) == 4
    assert isinstance(attr.bins[0], AttributeBin)
    assert attr.bins[0].continuous_start is None
    assert attr.bins[0].continuous_end == 10

    model.add_attribute(
        name="test_bins_2",
        value_type=ValueType.Integer,
        stage=Stage.ModelPipelineInput,
        categorical=True,
        bins=[
            AttributeBin(continuous_start=None, continuous_end=10),
            AttributeBin(continuous_start=10, continuous_end=15),
            AttributeBin(continuous_start=15, continuous_end=20),
        ],
    )
    attr = model.get_attribute(name="test_bins_2")
    assert len(attr.bins) == 3
    assert isinstance(attr.bins[0], AttributeBin)
    assert attr.bins[0].continuous_start is None
    assert attr.bins[0].continuous_end == 10


def test_add_nlp_attribute():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.NLP,
        output_type=OutputType.Multiclass,
    )
    ref_data = pd.DataFrame(
        {"input_text": ["hello", "hi", "what's up", "yo", "cool"], }
    )
    model.infer_schema(ref_data, stage=Stage.ModelPipelineInput)

    assert (
            model.get_attribute("input_text").value_type == ValueType.Unstructured_Text
    )
    assert model.get_attribute("input_text").categories is None


def test_float_categorical():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.Multiclass,
    )
    ref_data = pd.DataFrame(
        {"feature1": [float(1.0), float(1.0), float(-1.0), float(-1.0), float(1.0)], }
    )
    model.infer_schema(ref_data, stage=Stage.ModelPipelineInput)

    attribute = model.get_attribute("feature1")

    assert attribute.value_type == ValueType.Float
    assert attribute.categorical
    category_values = sorted([a.value for a in attribute.categories])
    assert category_values == ["-1.0", "1.0"]


def test_all_null_column():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.NLP,
        output_type=OutputType.Multiclass,
    )
    df = pd.DataFrame({'col1': [1], 'col2': [float("nan")]})
    model.infer_schema(df, stage=Stage.ModelPipelineInput)

    expected_attributes = [
        ArthurAttribute(name='col1', value_type=ValueType.Integer, stage=Stage.ModelPipelineInput, position=0,
                        categorical=True, categories=[AttributeCategory(value='1', label=None)], is_unique=False),
        ArthurAttribute(name='col2', value_type=ValueType.Float, stage=Stage.ModelPipelineInput, position=1,
                        categorical=False, is_unique=False)]

    assert model.attributes == expected_attributes


def test_nonzero_index_column():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.NLP,
        output_type=OutputType.Multiclass,
    )
    df = pd.DataFrame({'col1': [1], 'col2': [float("nan")]})
    df.index = [5]
    model.infer_schema(df, stage=Stage.ModelPipelineInput)

    expected_attributes = [
        ArthurAttribute(name='col1', value_type=ValueType.Integer, stage=Stage.ModelPipelineInput, position=0,
                        categorical=True, categories=[AttributeCategory(value='1', label=None)], is_unique=False),
        ArthurAttribute(name='col2', value_type=ValueType.Float, stage=Stage.ModelPipelineInput, position=1,
                        categorical=False, is_unique=False)]

    assert model.attributes == expected_attributes


def test_infer_numerical_string():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.Multiclass,
    )
    df = pd.DataFrame({'col1': ["0", "1", "0", "1", "1", "0"], 'col2': ["0.0", "1.0", "0.0", "1.0", "1.0", "0.0"]})
    model.infer_schema(df, stage=Stage.ModelPipelineInput)

    expected_attributes = [
        ArthurAttribute(name='col1', value_type=ValueType.String, stage=Stage.ModelPipelineInput, position=0,
                        categorical=True, categories=[AttributeCategory(value='0', label=None),
                                                      AttributeCategory(value='1', label=None)], is_unique=False),
        ArthurAttribute(name='col2', value_type=ValueType.String, stage=Stage.ModelPipelineInput, position=1,
                        categorical=True, categories=[AttributeCategory(value='0.0', label=None),
                                                      AttributeCategory(value='1.0', label=None)], is_unique=False)
    ]

    assert_attributes_equal(expected_attributes, model.attributes)


@pytest.mark.parametrize('stage,expected', [
    (Stage.ModelPipelineInput, [
        ArthurAttribute(name='time_series_input', value_type=ValueType.TimeSeries, stage=Stage.ModelPipelineInput,
                        position=0, is_unique=True),
        ArthurAttribute(name='col1', value_type=ValueType.Integer, stage=Stage.ModelPipelineInput, position=1,
                        categorical=True, is_unique=False, categories=[AttributeCategory("0"), AttributeCategory("1")]),
        ArthurAttribute(name='time_series_2', value_type=ValueType.TimeSeries, stage=Stage.ModelPipelineInput,
                        position=2, categorical=False, is_unique=True),
        ArthurAttribute(name='time_series_3', value_type=ValueType.TimeSeries, stage=Stage.ModelPipelineInput,
                        position=3, categorical=False, is_unique=True),
        ArthurAttribute(name='time_series_4', value_type=ValueType.TimeSeries, stage=Stage.ModelPipelineInput,
                        position=4, categorical=False, is_unique=True)]),  # happy path with time series
    (Stage.NonInputData, [  # happy path not parsing lists as time series for non-model pipeline input attributes
        ArthurAttribute(name='col1', value_type=ValueType.Integer, stage=Stage.NonInputData, position=1,
                        categorical=True, is_unique=False, categories=[AttributeCategory("0"), AttributeCategory("1")]),
        ArthurAttribute(name='time_series_4', value_type=ValueType.String, stage=Stage.NonInputData, position=4,
                        categorical=True, categories=[], is_unique=False)]),
])
def test_infer_time_series(stage, expected):
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.TimeSeries,
        output_type=OutputType.Multiclass,
    )
    time_series_value_1 = {"timestamp": "2023-10-05T00:00:00Z", "value": 1}
    time_series_value_2 = {"timestamp": "2023-10-04T00:00:00Z", "value": 2}

    df = pd.DataFrame({
        'time_series_input': [[time_series_value_1, time_series_value_2],
                              [time_series_value_1]],
        'col1': [0, 1],
        'time_series_2': [[], []],
        'time_series_3': [None, []],
        'time_series_4': [None, None]})
    model.infer_schema(df, stage=stage)

    assert_attributes_equal(expected, model.attributes)


def test_infer_string_categorical_dtype():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.Multiclass
    )

    df = pd.DataFrame({"col1": list("abca"), "col2": list("bccd")}, dtype="category")
    model.infer_schema(df, stage=Stage.ModelPipelineInput)

    expected_attributes = [
        ArthurAttribute(name='col1', value_type=ValueType.String, stage=Stage.ModelPipelineInput, position=0,
                        categorical=True, categories=[AttributeCategory(value='a', label=None),
                                                      AttributeCategory(value='b', label=None),
                                                      AttributeCategory(value='c', label=None)], is_unique=False),
        ArthurAttribute(name='col2', value_type=ValueType.String, stage=Stage.ModelPipelineInput, position=1,
                        categorical=True, categories=[AttributeCategory(value='d', label=None),
                                                      AttributeCategory(value='b', label=None),
                                                      AttributeCategory(value='c', label=None)], is_unique=False)
    ]
    assert_attributes_equal(expected_attributes, model.attributes)


def test_infer_int_categorical_dtype():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.Multiclass
    )

    df = pd.DataFrame({"col1": [1, 0, 0, 1], "col2": [1, 2, 1, 0]}, dtype="category")
    model.infer_schema(df, stage=Stage.ModelPipelineInput)

    expected_attributes = [
        ArthurAttribute(name='col1', value_type=ValueType.Integer, stage=Stage.ModelPipelineInput, position=0,
                        categorical=True, categories=[AttributeCategory(value='0', label=None),
                                                      AttributeCategory(value='1', label=None)], is_unique=False),
        ArthurAttribute(name='col2', value_type=ValueType.Integer, stage=Stage.ModelPipelineInput, position=1,
                        categorical=True, categories=[AttributeCategory(value='0', label=None),
                                                      AttributeCategory(value='1', label=None),
                                                      AttributeCategory(value='2', label=None)], is_unique=False)
    ]
    assert_attributes_equal(expected_attributes, model.attributes)


def test_non_tz_datetime_column():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.NLP,
        output_type=OutputType.Multiclass,
    )
    df = pd.DataFrame({'event_time': [datetime.now()]})
    df.index = [5]
    with pytest.raises(UserValueError) as e:
        model.infer_schema(df, stage=Stage.ModelPipelineInput)

    assert 'event_time' in str(e.value)


def test_set_categorical_value_labels():
    model = ArthurModel.from_json(model_response_json_strings[2])
    model.add_attribute(
        name="test_categorical_1",
        value_type=ValueType.Integer,
        stage=Stage.ModelPipelineInput,
        categorical=True,
        categories=[1, 2],
    )
    expected_categories = {1: "Male", 2: "Female"}
    model.set_attribute_labels("test_categorical_1", labels=expected_categories)
    cats = model.get_attribute("test_categorical_1").categories
    for category in cats:
        assert int(category.value) in expected_categories
        assert expected_categories[int(category.value)] == category.label


@responses.activate
def test_get_image(client):
    model = ArthurModel(client=client.client,
                        partner_model_id="test",
                        input_type=InputType.Image,
                        output_type=OutputType.Multiclass)
    model.id = '1234567890abcdef'
    image_id = '0a1b2c3d4e5f9687'
    path = '.'
    type = ImageResponseType.RawImage
    file_ext = '.png'
    response_content = 'content'.encode()
    expected_image_file = f"{path}/{type}_{image_id}{file_ext}"

    mock_get(f"/api/v3/models/{model.id}/inferences/images/{image_id}?type={type}", response_content,
             headers={'Content-Type': ImageContentType.Png})
    open_mock = mock_open()
    with patch("arthurai.core.models.open", open_mock, create=True):
        resulting_file = model.get_image(image_id, path, type=type)

    assert resulting_file == expected_image_file
    open_mock.assert_called_with(expected_image_file, 'wb')
    open_mock.return_value.write.assert_called_once_with(response_content)


def test_add_object_detection_output_attributes():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Image,
        output_type=OutputType.Multiclass,
    )

    # cannot call without proper types
    with pytest.raises(MethodNotApplicableError):
        model.add_object_detection_output_attributes('pred', 'gt', ['class_1', 'class_2'])
    model.input_type = InputType.NLP
    model.output_type = OutputType.ObjectDetection
    with pytest.raises(MethodNotApplicableError):
        model.add_object_detection_output_attributes('pred', 'gt', ['class_1', 'class_2'])

    # cannot call without classes
    model.output_type = OutputType.ObjectDetection
    model.input_type = InputType.Image
    with pytest.raises(UserValueError):
        model.add_object_detection_output_attributes('pred', 'gt', [])

    # names cannot match
    with pytest.raises(UserValueError):
        model.add_object_detection_output_attributes('pred', 'pred', ['class_1', 'class_2'])

    # happy path
    model.add_object_detection_output_attributes('pred', 'gt', ['class_1', 'class_2'])
    assert model.get_attribute('pred').value_type == ValueType.BoundingBox
    assert model.get_attribute('gt').value_type == ValueType.BoundingBox
    assert model.image_class_labels == ['class_1', 'class_2']


def test_build_tabular_model(reg_initial_batch_model):
    pred_gt_map = {reg.PRED: reg.GROUND_TRUTH}
    reg_initial_batch_model.build(data=reg.SAMPLE_DATAFRAME, pred_to_ground_truth_map=pred_gt_map,
                                  non_input_columns=[reg.FLOAT_NONINPUT])

    assert_attributes_equal(reg.MODEL_ATTRIBUTES, reg_initial_batch_model.attributes)
    pd.testing.assert_frame_equal(reg_initial_batch_model.reference_dataframe, reg.SAMPLE_DATAFRAME)


def test_build_tabular_class_model(initial_biclass_model):
    pred_gt_map = {mclass.DOG_PRED: mclass.DOG_GROUND_TRUTH, mclass.CAT_PRED: mclass.CAT_GROUND_TRUTH}
    initial_biclass_model.build(data=mclass.SAMPLE_DATAFRAME, pred_to_ground_truth_map=pred_gt_map,
                                non_input_columns=[mclass.FLOAT_NONINPUT], positive_predicted_attr=mclass.DOG_PRED)

    assert_attributes_equal(mclass.MODEL_ATTRIBUTES, initial_biclass_model.attributes)
    pd.testing.assert_frame_equal(initial_biclass_model.reference_dataframe, mclass.SAMPLE_DATAFRAME)


def test_build_tabular_class_model_implicit_negative_pred(initial_biclass_model):
    pred_gt_map = {mclass.DOG_PRED: mclass.DOG_GROUND_TRUTH, None: mclass.CAT_GROUND_TRUTH}
    initial_biclass_model.build(data=SAMPLE_DATAFRAME_NO_NEG_PRED,
                                pred_to_ground_truth_map=pred_gt_map, non_input_columns=[mclass.FLOAT_NONINPUT])
    assert_attributes_equal(mclass.MODEL_ATTRIBUTES_NO_NEG_PRED, initial_biclass_model.attributes)
    pd.testing.assert_frame_equal(initial_biclass_model.reference_dataframe, SAMPLE_DATAFRAME_NO_NEG_PRED)


def test_build_tabular_model_no_refset(reg_unsaved_batch_model):
    pred_gt_map = {reg.PRED: reg.GROUND_TRUTH}
    reg_unsaved_batch_model.build(data=reg.SAMPLE_DATAFRAME, pred_to_ground_truth_map=pred_gt_map,
                                  non_input_columns=[reg.FLOAT_NONINPUT], set_reference_data=False)

    assert_attributes_equal(reg.MODEL_ATTRIBUTES, reg_unsaved_batch_model.attributes)
    assert reg_unsaved_batch_model.reference_dataframe is None


def test_build_tabular_model_single_column_gt(initial_biclass_model):
    pred_class_map = {mclass.DOG_PRED: "0", mclass.CAT_PRED: "1"}
    initial_biclass_model.build(data=mclass.SINGLE_COLUMN_DATAFRAME, pred_to_ground_truth_map=pred_class_map,
                                ground_truth_column=mclass.GROUND_TRUTH, non_input_columns=[mclass.FLOAT_NONINPUT],
                                positive_predicted_attr=mclass.DOG_PRED)
    assert_attributes_equal(mclass.SINGLE_COL_MODEL_ATTRIBUTES, initial_biclass_model.attributes)
    pd.testing.assert_frame_equal(initial_biclass_model.reference_dataframe, mclass.SINGLE_COLUMN_DATAFRAME)


def test_build_nlp(initial_nlp_regression_model):
    initial_nlp_regression_model.build(nlp.NLP_DATAFRAME, pred_to_ground_truth_map={"pred": "gt"})

    assert initial_nlp_regression_model.get_attribute("input_text").value_type == ValueType.Unstructured_Text
    assert initial_nlp_regression_model.get_attribute("input_text").categories is None
    pd.testing.assert_frame_equal(initial_nlp_regression_model.reference_dataframe, nlp.NLP_DATAFRAME)


def test_build_nlp_sing_col(initial_nlp_classification_model):
    pred_class_map = {mclass.DOG_PRED: nlp.DOG_CLASS_STRING, mclass.CAT_PRED: nlp.CAT_CLASS_STRING}
    initial_nlp_classification_model.build(data=nlp.NLP_CLASSIFICATION_DATAFRAME,
                                           pred_to_ground_truth_map=pred_class_map,
                                           positive_predicted_attr=mclass.DOG_PRED,
                                           ground_truth_column=mclass.GROUND_TRUTH)
    assert_attributes_equal(nlp.CLASSIFICATION_MODEL_ATTRIBUTES, initial_nlp_classification_model.attributes)
    pd.testing.assert_frame_equal(initial_nlp_classification_model.reference_dataframe,
                                  nlp.NLP_CLASSIFICATION_DATAFRAME)


def test_build_nlp_sequence_model(initial_nlp_sequence_model):
    initial_nlp_sequence_model.build_token_sequence_model(input_column='input_text',
                                                          output_text_column='output_text')
    assert_attributes_equal(nlp.SEQUENCE_MODEL_ATTRIBUTES, initial_nlp_sequence_model.attributes)


def test_build_nlp_sequence_model_with_probs(initial_nlp_sequence_model):
    initial_nlp_sequence_model.build_token_sequence_model(input_column='input_text',
                                                          output_text_column='output_text',
                                                          output_token_column='output_tokens',
                                                          output_likelihood_column='output_probs')
    assert_attributes_equal(nlp.SEQUENCE_MODEL_WITH_PROBS_ATTRIBUTES, initial_nlp_sequence_model.attributes)


def test_build_nlp_sequence_model_with_gt(initial_nlp_sequence_model):
    initial_nlp_sequence_model.build_token_sequence_model(input_column='input_text',
                                                          output_text_column='output_text',
                                                          ground_truth_text_column='gt_text',
                                                          ground_truth_tokens_column='gt_tokens')
    assert_attributes_equal(nlp.SEQUENCE_MODEL_WITH_GT_ATTRIBUTES, initial_nlp_sequence_model.attributes)


def test_build_image():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Image,
        output_type=OutputType.Regression,
    )
    data = pd.DataFrame({'image': ["path1", "path2"], 'preds': [15.2, 31.6], 'gt': [12, 40]})
    model.build(data, pred_to_ground_truth_map={'preds': 'gt'})

    assert model.get_attribute("image").value_type == ValueType.Image
    assert model.get_attribute("image").categories is None
    pd.testing.assert_frame_equal(model.reference_dataframe, data)


def test_build_ranked_list():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.RankedList,
    )
    data = pd.DataFrame({'input': [1, 2],
                         'pred': [[recommended_item, recommended_item], [recommended_item]],
                         'gt': [["liked1", "liked2"], ["arr2"]]})

    model.build(data, pred_to_ground_truth_map={'pred': 'gt'})  # test happy path
    pred_attr = model.get_attribute("pred")
    assert pred_attr.value_type == ValueType.RankedList and pred_attr.categorical is False
    gt_attr = model.get_attribute("gt")
    assert gt_attr.value_type == ValueType.StringArray and gt_attr.categorical is False

    with pytest.raises(UserValueError):  # test wrong number of pred & ground truth attrs
        data['pred2'] = [[recommended_item, recommended_item], [recommended_item]]
        data['pred'] = [[recommended_item, recommended_item], [recommended_item]]
        data['gt2'] = data['gt']
        model.build(data, pred_to_ground_truth_map={'pred': 'gt', 'pred2': 'gt2'})


def test_build_time_series_model():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.TimeSeries,
        output_type=OutputType.RankedList,
    )
    time_series_value_1 = {"timestamp": "2023-10-05T00:00:00Z", "value": 1}
    time_series_value_2 = {"timestamp": "2023-10-04T00:00:00Z", "value": 2}

    data = pd.DataFrame({'time_series_input': [[time_series_value_1, time_series_value_2],
                                               [time_series_value_1]],
                         'pred': [[recommended_item, recommended_item], [recommended_item]],
                         'gt': [["liked1", "liked2"], ["arr2"]]})
    model.build(data, pred_to_ground_truth_map={'pred': 'gt'})  # test happy path

    expected_attributes = [
        ArthurAttribute(name='time_series_input', value_type=ValueType.TimeSeries, stage=Stage.ModelPipelineInput,
                        position=0, categorical=False, is_unique=True),
        ArthurAttribute(name='gt', value_type=ValueType.StringArray, stage=Stage.GroundTruth, position=0,
                        categorical=False, is_unique=False, attribute_link='pred'),
        ArthurAttribute(name='pred', value_type=ValueType.RankedList, stage=Stage.PredictedValue, position=0,
                        categorical=False, is_unique=False, attribute_link='gt')
    ]

    assert_attributes_equal(expected_attributes, model.attributes)


def test_build_object_detection():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Image,
        output_type=OutputType.ObjectDetection,
    )
    # not actually valid object data but that's okay
    data = pd.DataFrame({'image': ["path1", "path2"], 'preds': [0.8, 0.3], 'gt': [1, 0]})
    with pytest.raises(MethodNotApplicableError):
        model.build(data, pred_to_ground_truth_map={'preds': 'gt'})


def test_build_binary_classifier():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.Multiclass,
        classifier_threshold=0.42
    )

    data = pd.DataFrame({'pred0': [0.1, 0.9, 0.2, 0.8, 0.3, 0.7],
                         'pred1': [0.9, 0.1, 0.8, 0.2, 0.7, 0.3],
                         'gt0': [1, 1, 1, 0, 0, 0],
                         'gt1': [0, 0, 0, 1, 1, 1]})

    model.build(data, pred_to_ground_truth_map={'pred0': 'gt0', 'pred1': 'gt1'}, positive_predicted_attr='pred1')

    assert model.classifier_threshold == 0.42


@pytest.mark.parametrize("pred_to_gt_map,positive_predicted_attr,non_input_cols,gt_col", [
    # unknown predicted column
    ({'pred0': 'gt0', 'pred1': 'gt1', 'pred2': 'gt1'}, None, None, None),
    # unknown gt column in map
    ({'pred0': 'gt0', 'pred1': 'gt2'}, None, None, None),
    # unknown gt column in single-column
    ({'pred1': 1}, None, None, 'gt'),
    # zero predicted columns
    ({}, None, None, None),
    # unknown non input column
    ({'pred0': 'gt0', 'pred1': 'gt1'}, None, ['dummy'], None),
    # unknown positive predicted column
    ({'pred0': 'gt0', 'pred1': 'gt1'}, 'dummy', None, None),
])
def test_build_missing_attributes(pred_to_gt_map, positive_predicted_attr, non_input_cols, gt_col):
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.Multiclass,
        classifier_threshold=0.42
    )

    data = pd.DataFrame({'pred0': [0.1, 0.9, 0.2, 0.8, 0.3, 0.7],
                         'pred1': [0.9, 0.1, 0.8, 0.2, 0.7, 0.3],
                         'gt0': [1, 1, 1, 0, 0, 0],
                         'gt1': [0, 0, 0, 1, 1, 1]})

    with pytest.raises(UserValueError):
        model.build(data,
                    pred_to_ground_truth_map=pred_to_gt_map,
                    positive_predicted_attr=positive_predicted_attr,
                    non_input_columns=non_input_cols,
                    ground_truth_column=gt_col)


@responses.activate
def test_save_model_with_refset(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data

    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Pending
    }, status=201)

    with patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
               return_value=ModelStatus.Ready) as model_status_waiter_mock:
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    model_status_waiter_mock.assert_called_once_with([ModelStatus.Ready, ModelStatus.CreationFailed],
                                                     ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1
    assert reg_unsaved_batch_model.status == ModelStatus.Ready


@responses.activate
def test_save_model_no_refset(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Pending
    }, status=201)

    with patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
               return_value=ModelStatus.Ready) as model_status_waiter_mock:
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    model_status_waiter_mock.assert_called_once_with([ModelStatus.Ready, ModelStatus.CreationFailed],
                                                     ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1
    assert reg_unsaved_batch_model.status == ModelStatus.Ready


@responses.activate
def test_save_model_provisioning_failed(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Pending
    }, status=201)

    with pytest.raises(ArthurUnexpectedError), \
            patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
                  return_value=ModelStatus.CreationFailed) as model_status_waiter_mock:
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_not_called()
    model_status_waiter_mock.assert_called_once_with([ModelStatus.Ready, ModelStatus.CreationFailed],
                                                     ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1
    assert reg_unsaved_batch_model.status == ModelStatus.CreationFailed


@responses.activate
def test_save_model_provisioning_failed_retry(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Pending
    }, status=201)

    mock_post(f"/api/v3/models/{reg.TABULAR_MODEL_ID}/retry", response_body={}, status=200)

    with pytest.raises(ArthurUnexpectedError), \
            patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
                  return_value=ModelStatus.CreationFailed):
        reg_unsaved_batch_model.save()

    with patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
               return_value=ModelStatus.Ready) as model_status_waiter_mock:
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    model_status_waiter_mock.assert_called_once_with([ModelStatus.Ready, ModelStatus.CreationFailed],
                                                     ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 2
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1
    assert reg_unsaved_batch_model.status == ModelStatus.Ready


@responses.activate
def test_save_model_twice_error(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Pending
    }, status=201)

    mock_post(f"/api/v3/models/{reg.TABULAR_MODEL_ID}/retry", response_body={}, status=200)

    with patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
               return_value=ModelStatus.Ready) as model_status_waiter_mock:
        reg_unsaved_batch_model.save()

    with pytest.raises(MethodNotApplicableError):
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    model_status_waiter_mock.assert_called_once_with([ModelStatus.Ready, ModelStatus.CreationFailed],
                                                     ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1
    assert reg_unsaved_batch_model.status == ModelStatus.Ready


@responses.activate
def test_save_model_twice_creating(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Pending
    }, status=201)

    mock_post(f"/api/v3/models/{reg.TABULAR_MODEL_ID}/retry", response_body={}, status=200)

    with patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
               return_value=ModelStatus.Creating) as model_status_waiter_mock:
        reg_unsaved_batch_model.save()

    with pytest.raises(MethodNotApplicableError):
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    model_status_waiter_mock.assert_called_once_with([ModelStatus.Ready, ModelStatus.CreationFailed],
                                                     ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1
    assert reg_unsaved_batch_model.status == ModelStatus.Creating


@responses.activate
def test_save_model_twice_pending(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Pending
    }, status=201)

    mock_post(f"/api/v3/models/{reg.TABULAR_MODEL_ID}/retry", response_body={}, status=200)

    with patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
               return_value=ModelStatus.Pending) as model_status_waiter_mock:
        reg_unsaved_batch_model.save()

    with pytest.raises(MethodNotApplicableError):
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    model_status_waiter_mock.assert_called_once_with([ModelStatus.Ready, ModelStatus.CreationFailed],
                                                     ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1
    assert reg_unsaved_batch_model.status == ModelStatus.Pending


@responses.activate
def test_save_model_provisioning_exception(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': [],
        'status': ModelStatus.Pending
    }, status=201)

    with pytest.raises(ArthurUnexpectedError), \
            patch('arthurai.core.model_status_waiter.ModelStatusWaiter.wait_for_valid_status',
                  side_effect=ArthurUnexpectedError) as model_status_waiter_mock:
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_not_called()
    model_status_waiter_mock.assert_called_once_with([ModelStatus.Ready, ModelStatus.CreationFailed],
                                                     ONBOARDING_SPINNER_MESSAGE, ONBOARDING_UPDATE_MESSAGE)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1


@responses.activate
def test_save_model_no_status_backwards_compatibility_check(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': []
    }, status=201)

    reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1


@responses.activate
def test_save_model_twice_no_status_backwards_compatibility_check(reg_unsaved_batch_model):
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'model_group_id': reg.TABULAR_MODEL_GROUP_ID,
        'version_sequence_num': 1,
        'attributes': []
    }, status=201)

    reg_unsaved_batch_model.save()

    with pytest.raises(MethodNotApplicableError):
        reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id == reg.TABULAR_MODEL_GROUP_ID
    assert reg_unsaved_batch_model.version_sequence_num == 1


@responses.activate
def test_save_model_binary_implicit_negative(initial_biclass_model):
    pred_gt_map = {mclass.DOG_PRED: mclass.DOG_GROUND_TRUTH, None: mclass.CAT_GROUND_TRUTH}
    model = initial_biclass_model
    model.build(data=SAMPLE_DATAFRAME_NO_NEG_PRED, pred_to_ground_truth_map=pred_gt_map,
                non_input_columns=[mclass.FLOAT_NONINPUT], set_reference_data=False)
    mock_post("/api/v3/models", response_body=MODEL_DATA_WITH_ATTRIBUTES_IMPLICIT_NEG, status=201)
    model.save()

    assert model.id == mclass.MODEL_ID
    assert_attributes_equal(mclass.MODEL_ATTRIBUTES_IMPLICIT_NEG, model.attributes)


@responses.activate
def test_save_model_without_model_group_id(reg_unsaved_batch_model):
    # Ensure models can still be saved even when the POST `models/` endpoint does not response with model_group_id
    # For testing backwards compatibility of model versioning SDK changes with pre-model-versioning API versions
    reg_unsaved_batch_model.reference_dataframe = reg.SAMPLE_DATAFRAME
    mock_set_ref_data = MagicMock()
    reg_unsaved_batch_model.set_reference_data = mock_set_ref_data
    mock_post("/api/v3/models", response_body={
        'id': reg.TABULAR_MODEL_ID,
        'attributes': []
    }, status=201)

    reg_unsaved_batch_model.save()

    mock_set_ref_data.assert_called_once_with(data=reg.SAMPLE_DATAFRAME)
    assert len(responses.calls) == 1
    assert os.getenv("ARTHUR_LAST_MODEL_ID") == reg.TABULAR_MODEL_ID
    assert reg_unsaved_batch_model.model_group_id is None
    assert reg_unsaved_batch_model.version_sequence_num is None


def test_add_attribute_positions(reg_unsaved_batch_model):
    reg_unsaved_batch_model.infer_schema(reg.SAMPLE_DATAFRAME[reg.INT_INPUT], stage=Stage.ModelPipelineInput)
    reg_unsaved_batch_model.infer_schema(reg.SAMPLE_DATAFRAME[reg.FLOAT_NONINPUT], stage=Stage.NonInputData)
    reg_unsaved_batch_model.add_regression_output_attributes({reg.PRED: reg.GROUND_TRUTH}, value_type=ValueType.Integer)
    # there is one actual attribute in each stage so should be two in each with duplicates
    expected_attr_positions = {0, 1}
    for stage in (Stage.ModelPipelineInput, Stage.NonInputData, Stage.PredictedValue, Stage.GroundTruth):
        actual_attr_positions = [attr.position for attr in reg_unsaved_batch_model.attributes if attr.stage == stage]
        assert len(actual_attr_positions) == len(expected_attr_positions)
        assert set(actual_attr_positions) == expected_attr_positions


@responses.activate
def test_find_hotspots(streaming_model):
    model = streaming_model

    response_body = {'data': [{'rules': {},
                               'gt_to_info': {'-1': {'class_f1': 0.8870523415977962,
                                                     'class_precision': 0.8298969072164949,
                                                     'class_recall': 0.9526627218934911,
                                                     'count': 169,
                                                     'pred_to_count': {'-1': 161, '1': 8}},
                                              '1': {'class_f1': 0.9356357927786499,
                                                    'class_precision': 0.9738562091503268,
                                                    'class_recall': 0.9003021148036254,
                                                    'count': 331,
                                                    'pred_to_count': {'-1': 33, '1': 298}}},
                               'precision': 0.9251979650966916,
                               'recall': 0.918,
                               'f1': 0.9192145862795214,
                               'accuracy': 0.918,
                               'impurity': 0.15055200000000002,
                               'n_samples': 500,
                               'feature': 'x2',
                               'cutoff': -3.560836390126483}]}

    mock_get(f"/api/v3/models/{model.id}/enrichments/hotspots/find?metric=f1&threshold=0.999&date=2021-08-04",
             response_body=response_body, status=200)
    model.find_hotspots(metric="f1", threshold=0.999, date="2021-08-04")
    assert len(responses.calls) == 1


@responses.activate
def test_query(streaming_model):
    query_body = {"property": "my_base_prop"}
    response_body = {'query_result': "base query response"}
    mock_post(f"/api/v3/models/{streaming_model.id}/inferences/query",
              response_body=response_body, status=200)

    streaming_model.query(query_body)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.body == json.dumps(query_body)


@responses.activate
def test_query_psi_buckets(streaming_model):
    query_body = {"property": "my_psi_prop"}
    response_body = {'query_result': "psi bucket response"}
    mock_post(f"/api/v3/models/{streaming_model.id}/inferences/query/data_drift_psi_bucket_calculation_table",
              response_body=response_body, status=200)

    streaming_model.query(query_body, query_type="drift_psi_bucket_table")

    # assert request body was query
    assert len(responses.calls) == 1
    assert responses.calls[0].request.body == json.dumps(query_body)


@responses.activate
def test_query_bad_type(streaming_model):
    query_body = {"property": "my_prop"}
    with pytest.raises(UserValueError):
        streaming_model.query(query_body, query_type="foobar")


def test_model_group_from_dict():
    model_group = ArthurModelGroup.from_dict(MODEL_GROUP_JSON)

    assert model_group.id == MODEL_GROUP_ID
    assert model_group.name == MODEL_GROUP_NAME
    assert model_group.description == MODEL_GROUP_DESCRIPTION
    assert model_group.archived is MODEL_GROUP_ARCHIVED  # boolean value
    assert model_group.created_at == MODEL_GROUP_CREATED_AT
    assert model_group.updated_at == MODEL_GROUP_UPDATED_AT


def test_model_group_add_version():
    model = ArthurModel.from_dict(MODEL_RESPONSE_JSON[0])
    model_group = ArthurModelGroup.from_dict(MODEL_GROUP_JSON)
    label = "test_label"
    model_group.add_version(model, label)

    assert model.model_group_id == MODEL_GROUP_ID
    assert model.version_label == label


@responses.activate
def test_model_group_update_name(client):
    model_group = ArthurModelGroup.from_dict(MODEL_GROUP_JSON)
    model_group._update_client(client.client)
    model_group_new_name = "New Name"

    patch_response = MODEL_GROUP_JSON
    patch_response['name'] = model_group_new_name

    mock_patch(f"/api/v3/model_groups/{MODEL_GROUP_JSON['id']}",
               status=HTTPStatus.OK,
               response_body=patch_response)
    model_group.name = model_group_new_name

    assert model_group.name == model_group_new_name


@responses.activate
def test_model_group_update_description(client):
    model_group = ArthurModelGroup.from_dict(MODEL_GROUP_JSON)
    model_group._update_client(client.client)
    model_group_new_description = "New Description"

    patch_response = MODEL_GROUP_JSON
    patch_response['description'] = model_group_new_description

    mock_patch(f"/api/v3/model_groups/{MODEL_GROUP_JSON['id']}",
               status=HTTPStatus.OK,
               response_body=patch_response)
    model_group.description = model_group_new_description

    assert model_group.description == model_group_new_description


def test_get_attribute_wrong_stage():
    model_one = ArthurModel.from_json(model_response_json_strings[1])
    print(model_one.get_attributes(stage=Stage.ModelPipelineInput))
    # cannot call valid attribute name but invalid stage
    with pytest.raises(UserValueError):
        # correct stage is Stage.ModelPipelineInput
        model_one.get_attribute(name='attr_1', stage=Stage.GroundTruth)


def test_get_attribute_names_stage_none():
    model_one = ArthurModel.from_json(model_response_json_strings[1])
    attr_one = model_one.get_attribute_names(stage=None)
    assert len(attr_one) == 2

    model_two = ArthurModel.from_json(model_response_json_strings[2])
    attr_two = model_two.get_attribute_names(stage=None)
    assert len(attr_two) == 1


def test_build_categories_ordering(initial_nlp_classification_model):
    pred_class_map = {mclass.DOG_PRED: nlp.DOG_CLASS_STRING, mclass.CAT_PRED: nlp.CAT_CLASS_STRING}
    initial_nlp_classification_model.build(data=nlp.NLP_CLASSIFICATION_DATAFRAME,
                                           pred_to_ground_truth_map=pred_class_map,
                                           positive_predicted_attr=mclass.DOG_PRED,
                                           ground_truth_column=mclass.GROUND_TRUTH)
    gt_attr = initial_nlp_classification_model.get_attribute(nlp.GROUND_TRUTH)
    assert gt_attr.categories == [AttributeCategory(value=nlp.CAT_CLASS_STRING),
                                  AttributeCategory(value=nlp.DOG_CLASS_STRING)]


int_attr = ArthurAttribute(name="int_attr", value_type=ValueType.Integer, stage=Stage.ModelPipelineInput)
float_attr = ArthurAttribute(name="float_attr", value_type=ValueType.Float, stage=Stage.ModelPipelineInput)
bool_attr = ArthurAttribute(name="bool_attr", value_type=ValueType.Boolean, stage=Stage.ModelPipelineInput)
timestamp_attr = ArthurAttribute(name="timestamp_attr", value_type=ValueType.Timestamp, stage=Stage.ModelPipelineInput)
bounding_box_attr = ArthurAttribute(name="bounding_box_attr", value_type=ValueType.BoundingBox, stage=Stage.ModelPipelineInput)
tokens_attr = ArthurAttribute(name="tokens_attr", value_type=ValueType.Tokens, stage=Stage.ModelPipelineInput)
token_likelihoods_attr = ArthurAttribute(name="token_likelihoods_attr", value_type=ValueType.TokenLikelihoods, stage=Stage.ModelPipelineInput)
str_attr = ArthurAttribute(name="str_attr", value_type=ValueType.String, stage=Stage.ModelPipelineInput)
image_attr = ArthurAttribute(name="img_attr", value_type=ValueType.Image, stage=Stage.ModelPipelineInput)
unstructured_text_attr = ArthurAttribute(name="unstructured_attr", value_type=ValueType.Unstructured_Text, stage=Stage.ModelPipelineInput)


@pytest.mark.parametrize('obj,attr,expected', [
    ("str", str_attr, True), (0.8, float_attr, True), (1, int_attr, True),  # happy test cases
    ("img_path", image_attr, True), (True, bool_attr, True),
    (datetime.now(timezone.utc), timestamp_attr, True), (np.bool_(True), bool_attr, True),
    ("text", unstructured_text_attr, True), ([[0.1, .3, .13, .1, .4, .6]], bounding_box_attr, True),
    ([[1, 2, 3, 4, 5, 6]], bounding_box_attr, True), ([{"str": 0.8}], token_likelihoods_attr, True),
    ([{"str": 10}], token_likelihoods_attr, True), (["str", "str2"], tokens_attr, True),
    (np.int64(13), int_attr, True), (np.str_("hello"), str_attr, True), (np.single(0.8), float_attr, True),
    (np.str_("hello"), image_attr, True), (np.str_("hello"), unstructured_text_attr, True),
    (pd.Timestamp(year=2000, month=10, day=29).tz_localize(tz=timezone.utc), timestamp_attr, True),
    ([np.array([0.4, 0.2, 1, 2, 3, 4])], bounding_box_attr, True), ([np.array([4, 2, 1, 2, 3, 4])], bounding_box_attr, True),
    (np.array([[0.4, 0.2, 1, 2, 3, 4]]), bounding_box_attr, True), (np.array([[4, 2, 1, 2, 3, 4]]), bounding_box_attr, True),
    (np.array(["array", "of", "strings"]), tokens_attr, True),
    (np.array([{"dict": 0.4}, {"dict2": 0}]), token_likelihoods_attr, True),
    (np.array([{"dict": 4}, {"dict2": 0}]), token_likelihoods_attr, True),
    (datetime.now(timezone.utc), str_attr, False), (datetime.now(), str_attr, False),  # mismatch cases
    (np.datetime64("1970-01-01T00:00:00"), timestamp_attr, False),  # np.datetime64 can't be tz-aware so will always fail
    (np.datetime64(datetime.now(timezone.utc)), str_attr, False), (True, int_attr, False),
    (np.datetime64(datetime.now(timezone.utc)), timestamp_attr, False),
    (pd.Timestamp(year=2000, month=10, day=29), timestamp_attr, False),
    (datetime.now(), timestamp_attr, False), (np.datetime64(datetime.now()), timestamp_attr, False),
    (pd.Timestamp(year=2000, month=10, day=29), str_attr, False), (np.datetime64(datetime.now()), str_attr, False),
    ([{"str": False}], token_likelihoods_attr, False), ([{0.1: 3}], token_likelihoods_attr, False),
    ([True, False], tokens_attr, False), (Queue(), bounding_box_attr, False), (0.8, int_attr, False),
    ("str", tokens_attr, False), (["str"], image_attr, False), (["str"], unstructured_text_attr, False),
    (1, float_attr, False), ("str", bool_attr, False), (False, str_attr, False), (1, bool_attr, False),
    (datetime.now(), unstructured_text_attr, False), (12, image_attr, False), ([1, 3, 4], tokens_attr, False),
    (["str", "list", "three", "four", "five", "six"], bounding_box_attr, False), (True, int_attr, False),
    ("10/29/100", timestamp_attr, False), ([{"str": False}], token_likelihoods_attr, False),
    ([{"one": 12}, {"two": .3}], tokens_attr, False), ([{"str": "str"}], token_likelihoods_attr, False),
    ([[True, False, True, False, True, False]], bounding_box_attr, False), ([[.2, 4]], bounding_box_attr, False),
    ([[.2, .3, .4, .5, .6, .7, .8]], bounding_box_attr, False), ([1.3, 1.4], float_attr, False),
    ([["str"]], token_likelihoods_attr, False), ([], tokens_attr, "cannot be validated"),  # warning test cases
    ([None, None], tokens_attr, "cannot be validated"), ([{}], token_likelihoods_attr, "cannot be validated"),
    ([{None: 0.8}], token_likelihoods_attr, "cannot be validated"),
    ([{"str": None}], token_likelihoods_attr, "cannot be validated"),
    ([[None, None, None, None, None, None]], bounding_box_attr, "cannot be validated"),
    ([[]], bounding_box_attr, "cannot be validated"),
    ([], bounding_box_attr, "cannot be validated"), ([None, None], bounding_box_attr, "cannot be validated"),
    ([[None, None]], bounding_box_attr, False), ([{None: None}], token_likelihoods_attr, "cannot be validated"),
    ([], token_likelihoods_attr, "cannot be validated"),
    ("1", str_attr, "casting the column's data to integer or float types"),  # test incomplete timestamps as strings
    ("1/" + str(MINYEAR), str_attr, True), ("1/" + str(MAXYEAR), str_attr, True),
    ("1.0", str_attr, "casting the column's data to integer or float types")
])
def test__ensure_obj_matches_attr_value_type(caplog, obj, attr, expected):
    if isinstance(expected, bool) and not expected:
        with pytest.raises((UserTypeError, UserValueError)):
            ensure_obj_matches_attr_value_type(obj, attr.value_type, attr.name)
    elif isinstance(expected, str):
        with caplog.at_level(logging.WARNING):
            ensure_obj_matches_attr_value_type(obj, attr.value_type, attr.name)
        assert expected in caplog.text
    else:
        ensure_obj_matches_attr_value_type(obj, attr.value_type, attr.name)


weird_series_index = pd.Series([["weird", "series", "index"]])
weird_series_index.reindex(index=[7, 8, 2])


@pytest.mark.parametrize('series,attr,expected',
                         [([1, 0.1], float_attr, True), ([1, 2], int_attr, True),
                          ([0.4, 1], float_attr, True), ([False, True], bool_attr, True),
                          ([1, 0], bool_attr, False), ([False, True], int_attr, False),
                          ([12, 13], float_attr, False), ([1, 0.1], int_attr, False),
                          ([np.int64(13), np.single(0.8)], float_attr, True),
                          ([np.int64(13), np.single(0.8)], int_attr, False),
                          ([np.int64(13), np.int64(12)], int_attr, True),
                          ([[], []], float_attr, False), ([[None, None]], str_attr, False),
                          ([[], []], tokens_attr, "warning"), ([[None, None]], bounding_box_attr, "warning"),
                          ([[{}]], token_likelihoods_attr, "warning"),
                          ([[True, False], [False, True]], token_likelihoods_attr, False),
                          ([{"one": "two"}], str_attr, False),
                          ([[{"one": "two"}]], token_likelihoods_attr, False),
                          ([[{12: 13}, {17: 3}]], token_likelihoods_attr, False),
                          ([{}], tokens_attr, False), (Queue(), float_attr, False),
                          ([[0.1, 0.5, 60, .3, .5, .7]], bounding_box_attr, False),
                          ([[1, 5, 60, 3, 5, 7]], bounding_box_attr, False),
                          ([[[0.1, 0.5, 60, .3, .5, .7]]], bounding_box_attr, True),
                          ([[[1, 5, 60, 3, 5, 7]]], bounding_box_attr, True),
                          ([None, None, None], float_attr, "warning"),
                          (weird_series_index, tokens_attr, True), ([datetime.now(timezone.utc)], timestamp_attr, True),
                          ([str(datetime.now(timezone.utc))], timestamp_attr, False),
                          ([str(datetime.now(timezone.utc))], str_attr, False), ([datetime.now()], timestamp_attr, False),
                          ([str(datetime.now())], str_attr, False),
                          ([None, 0.4, None], float_attr, True),
                          ([None, 12, None], int_attr, True),
                          ([1.0, 2.0, np.nan, 3.0], int_attr, True),
                          ([1.5, 2.5, np.nan, 3.5], int_attr, False),
                          ([1.0, 2.0, np.nan, 3.0], float_attr, True),
                          ([1.0, 2.0, None, 3.0], float_attr, True)])
def test__validate_series_data_type(caplog, series, attr, expected):
    series = pd.Series(series)
    if expected is True:
        validate_series_data_type(series, attr)
    elif expected is False:
        with pytest.raises((UserTypeError, UserValueError)):
            validate_series_data_type(series, attr)
    else:
        with caplog.at_level(logging.WARNING):
            validate_series_data_type(series, attr)
        assert 'cannot be validated' in caplog.text


dup_cols_df = mclass.SAMPLE_DATAFRAME.copy()
dup_cols_df.insert(0, mclass.DOG_PRED, [0.12, 0.8, 0.2, 0.45, 0.94, 0.12], allow_duplicates=True)
extra_cols_df = mclass.SAMPLE_DATAFRAME.copy()
extra_cols_df['EXTRA'] = [0, 1, 1, 1, 1, 0]
string_df = mclass.SAMPLE_DATAFRAME.copy()
string_df["STRING_COL"] = ["one", "two", "three", "four", "five", "six"]
exempt_df = mclass.SAMPLE_DATAFRAME.copy()
exempt_df["col"] = [1.9, "exempt", 8.5, "exempt", 1, 2]
complex_df = mclass.SAMPLE_DATAFRAME.copy()
complex_df["col"] = [complex(1.0, 2.0), complex(3.0, 1.0), complex(1.0, 2.0), complex(3.0, 1.0), complex(1.0, 2.0), complex(3.0, 1.0)]
datetime_valid_df = mclass.SAMPLE_DATAFRAME.copy()
datetime_valid_df['DATETIME_VALID'] = [datetime.now(timezone.utc), datetime.now(timezone.utc),
                                       datetime.now(timezone.utc), datetime.now(timezone.utc),
                                       datetime.now(timezone.utc), datetime.now(timezone.utc)]
datetime_invalid_df = mclass.SAMPLE_DATAFRAME.copy()
datetime_invalid_df["DATETIME_INVALID"] = [datetime.now(), datetime.now(), datetime.now(), datetime.now(),
                                           datetime.now(), datetime.now()]
non_dt_timestamps_df = mclass.SAMPLE_DATAFRAME.copy()
non_dt_timestamps_df["TIMESTAMPS_INVALID"] = ["02/06/2020 00:12:58", "02/06/2020 00:12:58", "02/06/2020 00:12:58",
                                              "02/06/2020 00:12:58", "02/06/2020 00:12:58", "02/06/2020 00:12:58"]
numpy_floats_df = mclass.SAMPLE_DATAFRAME.copy()
numpy_floats_df["FLOATS"] = [np.single(0.1), np.single(0.1), np.single(0.1), np.single(0.1), np.single(0.1),
                             np.single(0.1)]
empty_col_df = mclass.SAMPLE_DATAFRAME.copy()
empty_col_df["EMPTY"] = [None, None, None, None, None, None]
weird_indices_df = mclass.SAMPLE_DATAFRAME.copy()
weird_indices_df['NEW_INDEX'] = [12, 51, 9, 230, 5, 4]
weird_indices_df = weird_indices_df.set_index('NEW_INDEX')
np_float_list = [np.single(0.1), np.single(0.8), np.single(0.3), np.single(0.2), np.single(0.1),
                 np.single(0.4)]
bounding_box_entry = [1, 0.3, 0.7, 0.8, 0.3, 0.4]

bounding_df = mclass.SAMPLE_DATAFRAME.copy()
bounding_df['image'] = ["path1", "path2", "path3", "path4", "path5", "path6"]
bounding_box = [np_float_list, np_float_list, np_float_list, np_float_list, np_float_list,
                np_float_list]
bounding_df['pred_bounding_box_column'] = [bounding_box, bounding_box, bounding_box, bounding_box, bounding_box,
                                           bounding_box]
bounding_box_2 = [None, bounding_box_entry, bounding_box_entry, bounding_box_entry,
                  bounding_box_entry, bounding_box_entry]
bounding_df['gt_bounding_box_column'] = [bounding_box_2, bounding_box_2, bounding_box_2, bounding_box_2, bounding_box_2,
                                         bounding_box_2]
nlp_df_1 = mclass.SAMPLE_DATAFRAME.copy()
nlp_df_1['input_text'] = ["TEXT1", "TEXT2", "TEXT1", "TEXT1", "TEXT2", "TEXT1"]
nlp_df_2 = nlp_df_1.copy()
nlp_df_2['gt_tokens'] = [["LIST"], ["LIST"], ["LIST"], ["LIST"], ["LIST"], ["LIST"]]
nlp_df_3 = nlp_df_1.copy()
list_dicts = [{"STR1": 0.1, "STR2": 0.3}]
nlp_df_3['output_probs'] = [list_dicts, list_dicts, list_dicts, list_dicts, list_dicts, list_dicts]
terrible_df = mclass.SAMPLE_DATAFRAME.copy()
terrible_df['queues'] = [Queue(), Queue(), Queue(), Queue(), Queue(), Queue()]


@pytest.mark.parametrize('df,error_expected,attr_changes,data_changes',
                         [
                             (mclass.SAMPLE_DATAFRAME, False, None, None),  # tests basic happy path
                             (dup_cols_df, True, None, None),  # tests dup cols
                             (mclass.SAMPLE_DATAFRAME.copy().drop(labels=mclass.DOG_PRED, axis=1), True, None, None),  # tests missing col
                             (extra_cols_df, True, None, None),  # tests extra col
                             (pd.DataFrame(), True, None, None),  # tests empty DataFrame,
                             (empty_col_df, False, [("EMPTY", ValueType.String)], None),
                             (mclass.SAMPLE_DATAFRAME, True, [(mclass.DOG_PRED, ValueType.Integer)], None),  # tests col of floats w/ int attr
                             (mclass.SAMPLE_DATAFRAME, True, [(mclass.CAT_GROUND_TRUTH, ValueType.Float)], None),  # tests col of ints w/ float attr
                             (mclass.SAMPLE_DATAFRAME, True, [(mclass.CAT_PRED, ValueType.String)], None),  # tests col of floats w/ str attr
                             (string_df, True, [("STRING_COL", ValueType.Boolean)], None),  # tests col of str w/ bool attr
                             (mclass.SAMPLE_DATAFRAME, False, None, {mclass.DOG_PRED: np.float64, mclass.CAT_PRED: float}),  # tests np floats pass
                             (exempt_df, True, [("col", ValueType.Float)], None),  # tests parquet serialization failure
                             (complex_df, True, [("col", ValueType.Float)], None),  # tests parquet serialization failure
                             (datetime_valid_df, False, [("DATETIME_VALID", ValueType.Timestamp)], None),  # test datetime aware tz objects don't error
                             (datetime_valid_df, True, [("DATETIME_VALID", ValueType.String)], None),  # tests Datetime obj with string attr errors
                             (datetime_valid_df, True, [("DATETIME_VALID", ValueType.String)], {"DATETIME_VALID": str}),
                             # tests valid tz aware datetime obj passed as strings errors
                             (datetime_invalid_df, True, [("DATETIME_INVALID", ValueType.Timestamp)], None),  # tests Datetime obj not timezone aware errors
                             (datetime_invalid_df, True, [("DATETIME_INVALID", ValueType.String)], None),
                             # tests col of Datetime objects not tz aware and expected as str attr errors
                             (datetime_invalid_df, True, [("DATETIME_INVALID", ValueType.Timestamp)], {"DATETIME_INVALID": str}),
                             # tests col of not tz aware datetime obj passed as strings expected as timestamp attr  errors
                             (datetime_invalid_df, True, [("DATETIME_INVALID", ValueType.String)], {"DATETIME_INVALID": str}),
                             # tests col of not tz aware datetime obj passed as strings expected as str attr errors
                             (non_dt_timestamps_df, True, [("TIMESTAMPS_INVALID", ValueType.String)], None),
                             # tests col of non-datetime timestamp strings errors
                             (numpy_floats_df, False, [("FLOATS", ValueType.Float)], None),  # tests valid numpy types pass
                             (weird_indices_df, False, None, None),
                             (bounding_df, False, [("image", ValueType.Image), ("pred_bounding_box_column", ValueType.BoundingBox),
                                                   ('gt_bounding_box_column', ValueType.BoundingBox)], None),  # tests models with boundingbox cols
                             (bounding_df, True, [("image", ValueType.BoundingBox), ("pred_bounding_box_column", ValueType.BoundingBox),
                                                  ('gt_bounding_box_column', ValueType.BoundingBox)], None),
                             (bounding_df, True,
                              [("image", ValueType.Image), ("pred_bounding_box_column", ValueType.String), ('gt_bounding_box_column', ValueType.BoundingBox)],
                              None),
                             (nlp_df_1, False, [("input_text", ValueType.Unstructured_Text)], None),  # test nlp object types
                             (nlp_df_1, True, [("input_text", ValueType.Float)], None),
                             (nlp_df_2, False, [("input_text", ValueType.Unstructured_Text), ("gt_tokens", ValueType.Tokens)], None),
                             (nlp_df_2, True, [("input_text", ValueType.Unstructured_Text), ("gt_tokens", ValueType.TokenLikelihoods)], None),
                             (nlp_df_3, False, [("input_text", ValueType.Unstructured_Text), ('output_probs', ValueType.TokenLikelihoods)], None),
                             (nlp_df_3, True, [("input_text", ValueType.Unstructured_Text), ('output_probs', ValueType.Integer)], None),
                             (nlp_df_3, True, [("input_text", ValueType.Unstructured_Text), ('output_probs', ValueType.String)], None),
                             (nlp_df_3, True, [("input_text", ValueType.Unstructured_Text), ('output_probs', ValueType.Image)], None),
                             (nlp_df_3, True, [("input_text", ValueType.Unstructured_Text), ('output_probs', ValueType.TokenLikelihoods)],
                              {'output_probs': str}),
                             (terrible_df, True, [("queues", ValueType.Tokens)], None)  # test terrible object type
                         ],  # once col was empty
                         )
def test_validate_reference_data(initial_biclass_model, df, error_expected, attr_changes, data_changes):
    pred_gt_map = {mclass.DOG_PRED: mclass.DOG_GROUND_TRUTH, mclass.CAT_PRED: mclass.CAT_GROUND_TRUTH}
    initial_biclass_model.build(data=mclass.SAMPLE_DATAFRAME, pred_to_ground_truth_map=pred_gt_map,
                                non_input_columns=[mclass.FLOAT_NONINPUT], positive_predicted_attr=mclass.DOG_PRED)

    if attr_changes is not None:
        for change in attr_changes:
            try:
                attr = initial_biclass_model.get_attribute(change[0])
                attr.set(value_type=change[1])
            except UserValueError:  # attr not in model
                initial_biclass_model.add_attribute(name=change[0], stage=Stage.ModelPipelineInput, value_type=change[1])
    if data_changes is not None:
        df = df.astype(data_changes)
    if not error_expected:
        initial_biclass_model.validate_reference_data(df)
    else:
        with pytest.raises(UserTypeError):
            initial_biclass_model.validate_reference_data(df)


@pytest.mark.parametrize('new_name,err', [
    ({mclass.INT_INPUT: "9input"}, True), ({mclass.INT_INPUT: "_INT_1NpUt"}, False),
    ({mclass.INT_INPUT: "int_input?"}, True), ({mclass.INT_INPUT: " intinput"}, True),
    ({mclass.INT_INPUT: "int input"}, True), ({mclass.INT_INPUT: "INT_1NpUt"}, False),
    ({mclass.INT_INPUT: "int-input"}, True)])
def test_validate_attr_names(new_name, err):
    data = mclass.SAMPLE_DATAFRAME.rename(columns=new_name)
    if err:
        with pytest.raises(UserValueError):
            validate_attr_names(data.columns)
    else:
        validate_attr_names(data.columns)


def test_add_ranked_list_attributes():
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.RankedList,
    )
    expected_attrs = [
        ArthurAttribute(
            name='gt',
            stage=Stage.GroundTruth,
            value_type=ValueType.StringArray,
            attribute_link='pred',
            position=0),
        ArthurAttribute(
            name='pred',
            stage=Stage.PredictedValue,
            value_type=ValueType.RankedList,
            attribute_link='gt',
            position=0)
    ]
    model.add_ranked_list_output_attributes('pred', 'gt')
    assert_attributes_equal(expected_attrs, model.attributes)
    with pytest.raises(UserValueError):
        model.add_ranked_list_output_attributes('pred', 'pred')
    with pytest.raises(MethodNotApplicableError):
        model.output_type = OutputType.Regression
        model.add_ranked_list_output_attributes('pred', 'gt')


int_pred_attr = ArthurAttribute(name="int_pred_attr", value_type=ValueType.Integer, stage=Stage.PredictedValue)
ranked_list_pred_attr = ArthurAttribute(name="ranked_list_pred_attr", value_type=ValueType.RankedList,
                                        stage=Stage.PredictedValue)
cat_pred_attr = ArthurAttribute(name="cat_pred_attr", value_type=ValueType.RankedList, stage=Stage.PredictedValue,
                                categorical=True)
str_arr_gt_attr = ArthurAttribute(name="str_arr_gt_attr", value_type=ValueType.StringArray, stage=Stage.GroundTruth)
int_gt_attr = ArthurAttribute(name="int_gt_attr", value_type=ValueType.Integer, stage=Stage.GroundTruth)
cat_gt_attr = ArthurAttribute(name="cat_gt_attr", value_type=ValueType.StringArray, stage=Stage.GroundTruth,
                              categorical=True)
recommended_item = {"item_id": "recommendation_1", "score": 0.324, "label": "apple"}
recs_1000 = generate_rec_ranked_list(1000)
rec_str_1000 = generate_unique_str_list(1000)
rec_per_inf_limit_broken_df = pd.DataFrame({
    'ranked_list_pred_attr': [[recommended_item] * 101, [recommended_item]],
    'str_arr_gt_attr': [["liked1", "liked2"], ["arr2"]]})
rec_per_inf_limit_gt = pd.DataFrame({
    'ranked_list_pred_attr': [[recommended_item] * 99, [recommended_item]],
    'str_arr_gt_attr': [["arr2"], ["liked_item"] * 101]})
rec_limit_broken_pred_df = pd.DataFrame({
    'ranked_list_pred_attr': [recs_1000[0:100], recs_1000[100:200], recs_1000[200:300], recs_1000[300:400],
                              recs_1000[400:500], np.array(recs_1000[500:600]), recs_1000[600:700], recs_1000[700:800],
                              recs_1000[800:900], recs_1000[900:], [recommended_item]],
    'str_arr_gt_attr': [[None] for _ in range(11)]})
rec_limit_broken_gt_df = pd.DataFrame({
    'ranked_list_pred_attr': [[None] for _ in range(11)],
    'str_arr_gt_attr': [rec_str_1000[0:100], rec_str_1000[100:200], np.array(rec_str_1000[200:300]), rec_str_1000[300:400],
                        rec_str_1000[400:500], rec_str_1000[500:600], rec_str_1000[600:700], rec_str_1000[700:800],
                        rec_str_1000[800:900], rec_str_1000[900:], ["recommendation_1"]]})
rec_limit_broken_pred_and_gt_df = pd.DataFrame({
    'ranked_list_pred_attr': [recs_1000[0:100], recs_1000[100:200], recs_1000[200:300], recs_1000[300:400],
                              recs_1000[400:499], [recommended_item]],
    'str_arr_gt_attr': [rec_str_1000[0:100], rec_str_1000[100:200], np.array(rec_str_1000[200:300]), rec_str_1000[300:400],
                        rec_str_1000[400:500], ["another_unique_recommended_item"]]})
valid_df_size_with_dups = pd.DataFrame({
    'ranked_list_pred_attr': [recs_1000[0:100], np.array(recs_1000[0:100]), recs_1000[100:200], recs_1000[200:300],
                              recs_1000[300:400], recs_1000[400:500], recs_1000[0:100], recs_1000[0:100],
                              np.array([0.8]), [0.8], None, [np.nan], np.inf, -np.inf, [np.inf, -np.inf]],
    'str_arr_gt_attr': [rec_str_1000[0:100], rec_str_1000[100:200], rec_str_1000[200:300], rec_str_1000[300:400],
                        rec_str_1000[400:500], rec_str_1000[0:100], np.array(rec_str_1000[0:100]), rec_str_1000[0:100],
                        np.array([0.8]), [0.8], None, [np.nan], np.inf, -np.inf, [np.inf, -np.inf]]})
rec_df_nones = pd.DataFrame({
    'ranked_list_pred_attr': [recs_1000[0:100], None, [None, np.nan, np.inf, -np.inf], np.nan, np.inf, -np.inf, [],
                              [{}], [[]], Queue(), [{"item_id": 0.8}], np.array([]), np.array([None, np.nan, np.inf, -np.inf])],
    'str_arr_gt_attr': [rec_str_1000[0:100], None, [None, np.nan, np.inf, -np.inf], np.nan, np.inf, -np.inf, [], [{}],
                        [[]], Queue(), [{"item_id": 0.8}], np.array([]), np.array([None, np.nan, np.inf, -np.inf])]
})


@pytest.mark.parametrize('attr,err,data', [
    ([int_pred_attr, ranked_list_pred_attr], True, None), ([ranked_list_pred_attr], True, None),
    ([int_pred_attr, str_arr_gt_attr], True, None), ([int_gt_attr, ranked_list_pred_attr], True, None),
    ([cat_pred_attr, str_arr_gt_attr], True, None), ([cat_gt_attr, ranked_list_pred_attr], True, None),
    ([ranked_list_pred_attr, str_arr_gt_attr], True, rec_per_inf_limit_broken_df),
    ([ranked_list_pred_attr, str_arr_gt_attr], True, rec_per_inf_limit_gt),
    ([ranked_list_pred_attr, str_arr_gt_attr], True, rec_limit_broken_pred_df),
    ([ranked_list_pred_attr, str_arr_gt_attr], True, rec_limit_broken_gt_df),
    ([ranked_list_pred_attr, str_arr_gt_attr], True, rec_limit_broken_pred_and_gt_df),
    ([ranked_list_pred_attr, str_arr_gt_attr], False, None),
    ([ranked_list_pred_attr, str_arr_gt_attr], False, valid_df_size_with_dups),
    ([ranked_list_pred_attr, str_arr_gt_attr], False, rec_df_nones)])
def test__validate_ranked_list_model(attr, err, data):
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=InputType.Tabular,
        output_type=OutputType.RankedList,
    )
    if data is not None:
        model.set_reference_data(data=data)
    for elem in attr:
        model._add_attribute_to_model(elem)
    if err:
        with pytest.raises(UserValueError):
            model._validate_ranked_list_model(data=data)
    else:
        model._validate_ranked_list_model(data=data)
    if data is not None:
        pd.testing.assert_frame_equal(model.reference_dataframe, data)


ranked_list_df_not_standardized = pd.DataFrame({
    rlist.TEMPO: [np.int_(88), np.nan],
    rlist.PRED: [
        [{"item_id": "1", "label": "test", "score": None}, None], None],
    rlist.GROUND_TRUTH: [["test1", "test2"], np.inf]
})

ranked_list_json_not_standardized = [
    {
        "reference_data":  {
            rlist.TEMPO: 88.0,
            rlist.PRED: [{"item_id": "1", "label": "test", "score": None}, None],
            rlist.GROUND_TRUTH: ["test1", "test2"]
        },
    },
    {
        "reference_data": {
            rlist.TEMPO: None,
            rlist.PRED: None,
            rlist.GROUND_TRUTH: None
        },
    }
]


@pytest.mark.parametrize('data,expected', [
    (rlist.RANKED_LIST_DATAFRAME, rlist.RANKED_LIST_JSON),
    (ranked_list_df_not_standardized, ranked_list_json_not_standardized)])
def test__ref_df_to_json(ranked_list_model, data, expected):
    assert ranked_list_model._ref_df_to_json(data) == json.dumps(expected, indent=4)


def test_nest_reference_data(ranked_list_model):
    assert nest_reference_data(ranked_list_json_not_standardized, ranked_list_model.attributes) == ranked_list_json_not_standardized


dir_path = '.' if os.getcwd().endswith('tests') else './tests'

parquet_files = [f"{dir_path}/data/inference_batch_data/parquet/inferences.parquet",
                 io.open(f"{dir_path}/data/inference_batch_data/parquet/inferences.parquet", "rb"),
                 io.open(f"{dir_path}/data/inference_batch_data/parquet/inferences.parquet", "r"),
                 Path(f"{dir_path}/data/inference_batch_data/parquet/inferences.parquet"),
                 PurePath(f"{dir_path}/data/inference_batch_data/parquet/inferences.parquet")]

json_files = [f"{dir_path}/data/ranked_list_reference_data_transformed.json",
              io.open(f"{dir_path}/data/ranked_list_reference_data_transformed.json", "rb"),
              io.open(f"{dir_path}/data/ranked_list_reference_data_transformed.json", "r"),
              Path(f"{dir_path}/data/ranked_list_reference_data_transformed.json"),
              PurePath(f"{dir_path}/data/ranked_list_reference_data_transformed.json")]


def test__count_json_num_rows(ranked_list_model):
    assert ranked_list_model._count_json_num_rows(file_paths=parquet_files) == 0  # test parquet files are ignored
    assert ranked_list_model._count_json_num_rows(file_paths=json_files) == 10


def test__count_parquet_num_rows(ranked_list_model):
    assert ranked_list_model._count_parquet_num_rows(file_paths=json_files) == 0  # test json files are ignored
    assert ranked_list_model._count_parquet_num_rows(file_paths=parquet_files) == 16


@pytest.mark.parametrize('is_dir_path_param,param_val', [
    (True, f"{dir_path}/data/reference_data"),
    (False, [f"{dir_path}/data/reference_data/ranked_list_reference_data.json",
             f"{dir_path}/data/reference_data/ranked_list_nested_reference_data.json",
             f"{dir_path}/data/reference_data/parquet_test.parquet"])])
def test__transform_json_reference_data(ranked_list_model, is_dir_path_param, param_val):
    if is_dir_path_param:
        transformed_files, temp_dir = ranked_list_model._transform_json_reference_data(directory_path=param_val)
    else:
        transformed_files, temp_dir = ranked_list_model._transform_json_reference_data(files=param_val)

    expected_json_files_paths = [f"{dir_path}/data/ranked_list_reference_data_transformed.json",
                                 f"{dir_path}/data/reference_data/ranked_list_nested_reference_data.json",
                                 f"{dir_path}/data/reference_data/parquet_test.parquet"]

    # naming of temp json files is not guaranteed so the test passes if the expected file matches any transformed file
    for transformed_file in transformed_files:
        found_matching_file = False
        for expected_file in expected_json_files_paths:
            if filecmp.cmp(expected_file, transformed_file, shallow=False):
                found_matching_file = True
        if not found_matching_file:
            assert False
    shutil.rmtree(temp_dir)


@pytest.mark.parametrize('input_type,add_attr,err,err_message', [
    # test validate input type
    (InputType.Tabular, None, MethodNotApplicableError, r"model is not a time series input type model"),
    # test validate time series attr exists
    (InputType.TimeSeries, None, UserValueError, r"Time Series input type models must have at least one time series type PIPELINE_INPUT"),
    (InputType.TimeSeries, ArthurAttribute(name="time_series", value_type=ValueType.TimeSeries,
                                           stage=Stage.NonInputData, position=0, categorical=False),
     UserValueError, r"Time Series input type models must have at least one time series type PIPELINE_INPUT"),
    # test validate time series attr isn't categorical
    (InputType.TimeSeries, ArthurAttribute(name="time_series", value_type=ValueType.TimeSeries,
                                           stage=Stage.ModelPipelineInput, position=0, categorical=True),
     UserValueError, r"Time Series value type attributes cannot be categorical."),
    # test happy path
    (InputType.TimeSeries, ArthurAttribute(name="time_series", value_type=ValueType.TimeSeries,
                                           stage=Stage.ModelPipelineInput, position=0, categorical=False), None, "")
])
def test__validate_time_series_model_schema(input_type, add_attr, err, err_message):
    model = ArthurModel(
        partner_model_id="test",
        client=None,
        input_type=input_type,
        output_type=OutputType.RankedList,
    )

    if add_attr is not None:
        model._add_attribute_to_model(add_attr)

    if err is not None:
        with pytest.raises(err, match=err_message):
            model._validate_time_series_model_schema()
    else:
        model._validate_time_series_model_schema()
