import numpy as np
import pandas as pd
import pytest

from arthurai import ArthurAttribute, ArthurModel
from arthurai.common.constants import ValueType, Stage, OutputType, InputType

from tests.fixtures.mocks import client

GROUND_TRUTH = "gt"
TEMPO = "tempo"
PRED = "recommendations"

RANKED_LIST_DATAFRAME = pd.DataFrame({
    TEMPO: [88, 66],
    PRED: [
        [{"item_id": "1", "label": "test", "score": 0.88},
         {"item_id": "2", "label": "test", "score": 0.88}],
        [{"item_id": "1", "label": "test", "score": 0.66},
         {"item_id": "2", "label": "test", "score": 0.66}],
    ],
    GROUND_TRUTH: [["test1", "test2"], ["test3", "test4"]]
})

RANKED_LIST_JSON = [
    {
        "reference_data": {
            TEMPO: 88,
            PRED: [
                {"item_id": "1", "label": "test", "score": 0.88},
                {"item_id": "2", "label": "test", "score": 0.88}
            ],
            GROUND_TRUTH: ["test1", "test2"],
        }
    },
    {
        "reference_data": {
            TEMPO: 66,
            PRED: [
                {"item_id": "1", "label": "test", "score": 0.66},
                {"item_id": "2", "label": "test", "score": 0.66}
            ],
            GROUND_TRUTH: ["test3", "test4"]
        }
    }
]

TEMPO_ATTR = ArthurAttribute(name=TEMPO,
                             value_type=ValueType.Integer,
                             stage=Stage.ModelPipelineInput,
                             position=0)

GT_ATTR = ArthurAttribute(
            name=GROUND_TRUTH,
            stage=Stage.GroundTruth,
            value_type=ValueType.StringArray,
            attribute_link=PRED,
            position=0)

PRED_ATTR = ArthurAttribute(
            name=PRED,
            stage=Stage.PredictedValue,
            value_type=ValueType.RankedList,
            attribute_link=GROUND_TRUTH,
            position=0)

RANKED_LIST_MODEL_ATTRIBUTES = [TEMPO_ATTR, GT_ATTR, PRED_ATTR]

MODEL_DATA = {"partner_model_id": "test",
              "input_type": InputType.Tabular,
              "output_type": OutputType.RankedList}

MODEL_ID = "c4ea58b6-4ec7-43b2-94d3-786eccb2a492"


@pytest.fixture
def ranked_list_model(client):
    model = ArthurModel(
        **MODEL_DATA,
        client=client.client,
        attributes=RANKED_LIST_MODEL_ATTRIBUTES
    )
    model.id = MODEL_ID
    return model
