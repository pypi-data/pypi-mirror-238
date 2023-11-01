import logging
from typing import List

from arthurai.common.constants import EnrichmentStatus, ENRICHMENT_READY_OR_FAILED_STATES, \
    ENRICHMENTS_SPINNER_MESSAGE, ENRICHMENTS_UPDATE_MESSAGE
from arthurai.common.exceptions import ExpectedParameterNotFoundError, UserValueError
from arthurai.core.status_waiter import StatusWaiter

logger = logging.getLogger(__name__)


class StatusForEnrichment:
    def __init__(self, enrichment_name: str, status: EnrichmentStatus):
        self.enrichment_name = enrichment_name
        self.status = status


class EnrichmentStatusWaiter(StatusWaiter):
    def __init__(self, model):
        self.err_mess = "Failed when trying to fetch the statuses of the enrichments. " \
                        "Please retry to wait for the statuses of the enrichments."
        super().__init__(model, self.err_mess)

    def _check_valid_status(self, status_list: List) -> bool:
        """Returns True if all enrichment statuses have reached valid final states in `status_list`, False otherwise"""
        for enrichment in self._status:
            if enrichment.status not in status_list:
                return False
        return True

    def _update_status(self):
        """Updates `_status` with the latest enrichment statuses"""
        self._status = []
        enrichments = self.model.get_enrichments()
        for key, val in enrichments.items():
            if 'status' not in val:
                raise ExpectedParameterNotFoundError(f"An error occurred: 'status' was not found in enrichment "
                                                     f"{key}—got {val} instead")
            else:
                self._status.append(StatusForEnrichment(key, val['status']))


def await_enrichments_ready(model):
    """wait for enrichments to be Ready, Training, Disabled, or Failed

    Wait until all enrichments for the model reach
    :py:attr:`~arthurai.common.constants.EnrichmentStatus.EnrichmentStatusReady`,
    :py:attr:`~arthurai.common.constants.EnrichmentStatus.EnrichmentStatusTraining`,
    :py:attr:`~arthurai.common.constants.EnrichmentStatus.EnrichmentStatusFailed`, or
    :py:attr:`~arthurai.common.constants.EnrichmentStatus.EnrichmentStatusDisabled` states. Prints to the log that it is
    waiting for the enrichments to be ready to receive inferences until all enrichments reach valid enrichment statuses.

    :raises UserValueError: If an exception occurs when checking the status of the model's enrichments or all
        enrichments have reached valid statuses and at least one enrichment is in the
        :py:attr:`~arthurai.common.constants.EnrichmentStatus.EnrichmentStatusFailed` state.
    """
    enrichment_statuses = EnrichmentStatusWaiter(model).wait_for_valid_status(
        ENRICHMENT_READY_OR_FAILED_STATES, ENRICHMENTS_SPINNER_MESSAGE, ENRICHMENTS_UPDATE_MESSAGE)
    failed_workflows = []
    for enrichment in enrichment_statuses:
        if enrichment.status == EnrichmentStatus.EnrichmentStatusFailed:
            failed_workflows.append(enrichment.enrichment_name)
    if len(failed_workflows) != 0:
        raise UserValueError(f"The following enrichments failed to provision: {', '.join(failed_workflows)}. Please "
                             f"fix the failed enrichments before sending inferences, or the enrichments will not "
                             f"process correctly. If you wish to proceed without the enrichments, set the "
                             f"wait_for_enrichments parameter to False when calling the 'send_bulk_inferences' or "
                             f"'send_inferences' functions.")
    else:
        logger.info("All enrichments are ready to accept inferences. Continuing with inference upload.")
