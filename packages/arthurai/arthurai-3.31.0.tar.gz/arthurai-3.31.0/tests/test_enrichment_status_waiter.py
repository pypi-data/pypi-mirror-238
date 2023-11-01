from typing import NamedTuple, Dict, List, Optional, Union, Type

import logging
import pytest
import responses

from arthurai import ArthurModel
from arthurai.common.constants import ENRICHMENTS_SPINNER_MESSAGE, ENRICHMENTS_UPDATE_MESSAGE, \
    EnrichmentStatus, InputType, OutputType
from arthurai.common.exceptions import ArthurUnexpectedError, UserValueError
from arthurai.core.enrichment_status_waiter import EnrichmentStatusWaiter, await_enrichments_ready
from tests.helpers import mock_get
from tests.fixtures.mocks import client

READY_FOR_INFERENCES_STATUS_LIST = [EnrichmentStatus.EnrichmentStatusDisabled, EnrichmentStatus.EnrichmentStatusFailed,
                                    EnrichmentStatus.EnrichmentStatusTraining, EnrichmentStatus.EnrichmentStatusReady]

RESPONSE_NOT_READY = {
    "anomaly_detection": {
        "status": EnrichmentStatus.EnrichmentStatusDisabled
    },
    "explainability": {
        "status": EnrichmentStatus.EnrichmentStatusReady,
        "enabled": True
    },
    "hotspots": {
        "status": EnrichmentStatus.EnrichmentStatusPending,
    },
    "bias_mitigation": {
        "status": EnrichmentStatus.EnrichmentStatusTraining,
    }
}
RESPONSE_READY = {
    "anomaly_detection": {
        "status": EnrichmentStatus.EnrichmentStatusDisabled
    },
    "explainability": {
        "status": EnrichmentStatus.EnrichmentStatusReady,
        "enabled": True
    },
    "hotspots": {
        "status": EnrichmentStatus.EnrichmentStatusTraining,
    },
    "bias_mitigation": {
        "status": EnrichmentStatus.EnrichmentStatusFailed,
    }
}
RESPONSE_READY_WITHOUT_FAILED = {
    "anomaly_detection": {
        "status": EnrichmentStatus.EnrichmentStatusDisabled
    },
    "explainability": {
        "status": EnrichmentStatus.EnrichmentStatusReady,
        "enabled": True
    },
    "hotspots": {
        "status": EnrichmentStatus.EnrichmentStatusTraining,
    },
    "bias_mitigation": {
        "status": EnrichmentStatus.EnrichmentStatusReady,
    }
}

NO_STATUS_RESPONSE = {
    "explainability": {
        "enabled": True
    },
}


class ConstructEnrichmentStatusWaiterTestCase(NamedTuple):
    response_body: List[Dict[str, Dict]]
    status: List[int]
    expect_err: Optional[Union[str, Type[Exception]]]


WAIT_FOR_VALID_STATUS_CASES = [
    ConstructEnrichmentStatusWaiterTestCase(status=[200, 200], response_body=[RESPONSE_NOT_READY, RESPONSE_READY],
                                            expect_err=None),
    ConstructEnrichmentStatusWaiterTestCase(status=[500], response_body=[{}], expect_err="500 Internal Server Error"),
    ConstructEnrichmentStatusWaiterTestCase(status=[200], response_body=[NO_STATUS_RESPONSE],
                                            expect_err="ExpectedParameterNotFoundError")
]


def get_test_model(client) -> ArthurModel:
    return ArthurModel(
        id="test_model_id",
        partner_model_id="test",
        client=client.client,
        input_type=InputType.Tabular,
        output_type=OutputType.Multiclass,
    )


@pytest.mark.parametrize("case", WAIT_FOR_VALID_STATUS_CASES)
@responses.activate
def test_enrichment_status_wait_for_valid_status(client, case: ConstructEnrichmentStatusWaiterTestCase, caplog):
    model = get_test_model(client)
    for i in range(len(case.status)):
        mock_get(f"/api/v3/models/{model.id}/enrichments", response_body=case.response_body[i], status=case.status[i])

    enrichment_status_waiter = EnrichmentStatusWaiter(model)
    expected_statuses, statuses = [], []

    if case.expect_err is not None:
        with pytest.raises(ArthurUnexpectedError):
            with caplog.at_level(logging.ERROR):
                enrichments = enrichment_status_waiter.wait_for_valid_status(READY_FOR_INFERENCES_STATUS_LIST,
                                                                             ENRICHMENTS_SPINNER_MESSAGE,
                                                                             ENRICHMENTS_UPDATE_MESSAGE)
                statuses = [enrichment.status for enrichment in enrichments]
                assert len(statuses) == 0
        assert case.expect_err in caplog.text
    else:
        enrichments = enrichment_status_waiter.wait_for_valid_status(READY_FOR_INFERENCES_STATUS_LIST,
                                                                     ENRICHMENTS_SPINNER_MESSAGE,
                                                                     ENRICHMENTS_UPDATE_MESSAGE)
        statuses = [enrichment.status for enrichment in enrichments]
        for key, value in case.response_body[len(case.response_body) - 1].items():
            expected_statuses.append(value['status'])
        assert expected_statuses == statuses
    assert len(responses.calls) == len(case.status)


AWAIT_ENRICHMENTS_READY_CASES = [
    ConstructEnrichmentStatusWaiterTestCase(status=[200, 200],
                                            response_body=[RESPONSE_NOT_READY, RESPONSE_READY_WITHOUT_FAILED],
                                            expect_err=None),
    ConstructEnrichmentStatusWaiterTestCase(status=[200, 200], response_body=[RESPONSE_NOT_READY, RESPONSE_READY],
                                            expect_err=UserValueError),
    ConstructEnrichmentStatusWaiterTestCase(status=[500], response_body=[{}], expect_err=ArthurUnexpectedError),
    ConstructEnrichmentStatusWaiterTestCase(status=[200], response_body=[NO_STATUS_RESPONSE],
                                            expect_err=ArthurUnexpectedError)
]


@pytest.mark.parametrize("case", AWAIT_ENRICHMENTS_READY_CASES)
@responses.activate
def test_await_enrichments_ready(client, case: ConstructEnrichmentStatusWaiterTestCase):
    model = get_test_model(client)
    for i in range(len(case.status)):
        mock_get(f"/api/v3/models/{model.id}/enrichments", response_body=case.response_body[i], status=case.status[i])

    if case.expect_err is not None:
        with pytest.raises(case.expect_err):
            await_enrichments_ready(model)
    else:
        await_enrichments_ready(model)
    assert len(responses.calls) == len(case.status)
