import logging
from http import HTTPStatus
from typing import List

from arthurai.client.http.requests import HTTPClient
from arthurai.common.exceptions import ExpectedParameterNotFoundError
from arthurai.core.status_waiter import StatusWaiter

logger = logging.getLogger(__name__)


class ModelStatusWaiter(StatusWaiter):
    def __init__(self, model, client: HTTPClient):
        self.err_mess = "Failed when trying to fetch the status of the model. " \
                        "Please retry to wait for the status of the model."
        super().__init__(model, self.err_mess, client)

    def _update_status(self):
        """Updates `_status` with the latest status of the current model"""
        model_resp = self._client.get(f'/models/{self.model.id}', return_raw_response=True,
                                      validation_response_code=HTTPStatus.OK)
        model_resp_json = model_resp.json()
        if 'id' not in model_resp_json:
            raise ExpectedParameterNotFoundError(
                f"An error occurred: {model_resp}, {model_resp.status_code}, {model_resp.content}")
        self._status = model_resp_json['status']

    def _check_valid_status(self, status_list: List) -> bool:
        """Returns True if model status has reached valid final state in `status_list`, False otherwise"""
        return self._status in status_list
