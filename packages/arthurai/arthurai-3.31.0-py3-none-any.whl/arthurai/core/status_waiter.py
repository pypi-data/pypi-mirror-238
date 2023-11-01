import logging
import threading
import time
from abc import ABC, abstractmethod
from typing import List, Any

from yaspin import yaspin

from arthurai.client.http.requests import HTTPClient
from arthurai.common.exceptions import ArthurUnexpectedError

logger = logging.getLogger(__name__)


class StatusWaiter(ABC):
    def __init__(self, model, err_mess: str, client: HTTPClient = None):
        """Superclass for waiting on some attribute of a model to reach a final state

        See :class:`arthurai.core.ModelStatusWaiter` for an example subclass implementation.

        :param model: ArthurModel for which the status of some related attribute is being waited on
        :param err_mess: Error message to log when the `update_status_func` function raises an exception.
        :param client: Optional HTTPClient.
        """
        self.model = model
        self._client = client
        self._status = None
        self._status_exception: bool = False
        self._status_available = threading.Event()
        self.err_mess = err_mess

    def wait_for_valid_status(self, status_list: List, spinner_message: str, update_message: str,
                              update_interval_seconds=60) -> Any:
        """ Wait to reach a status on the status_list

        Starts the thread that is responsible for checking the status until the attribute being checked reaches a status
        passed in the list as an argument or an exception occurs, and runs a spinner providing updates while waiting for
        the valid final status state.

        :param status_list: List of final valid statuses.
        :param spinner_message: The message you want to display when spinner is running and waiting for results
        :param update_message: The message you want to display when update_interval_seconds time is exceeded
        :param update_interval_seconds: Frequency at which an update is provided on the console
        """

        self._status_available.clear()
        self._status_exception = False
        thread = threading.Thread(target=self._await_final_status_thread, args=[status_list])
        thread.start()

        with yaspin(text=spinner_message) as sp:
            while not self._status_available.wait(timeout=update_interval_seconds):
                sp.write(update_message)
            sp.stop()

        if self._status_exception is True:
            raise ArthurUnexpectedError(self.err_mess)

        return self._status

    def _await_final_status_thread(self, status_list: List, poll_interval_seconds=5):
        """ Thread that polls the current status

        Polls the current status until it reaches a status in the status_list or an exception occurs.
        This method is used as a thread and sets the flag _status_available at the end of execution.
        Do not use as a regular function.
        :param status_list: List of valid statuses
        :param poll_interval_seconds: polling interval to check status on the model
        """
        while True:
            try:
                self._update_status()
            except BaseException as ex:
                logger.exception(ex)
                self._status_exception = True
                self._status_available.set()  # setting the flag on the threading event when result is available
                break
            if self._check_valid_status(status_list):  # if the final state is reached, set the flag and break
                self._status_available.set()
                break
            time.sleep(poll_interval_seconds)

    @abstractmethod
    def _check_valid_status(self, status_list: List) -> bool:
        """Returns a boolean indicating if a final valid status has been reached.

        Must be overridden by subclass.

        :param status_list: List of final valid statuses.
        """
        raise NotImplementedError

    @abstractmethod
    def _update_status(self):
        """Updates the `StatusWaiter._status` field with the current status of the attribute being waited on.

        Must be overridden by subclass.
        """
        raise NotImplementedError
