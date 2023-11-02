from .enums import JobCompletionStatus
from typing import Any


class Job:
    """
    An individual job to process in the pool
    Override it with an execute method to handle the processing
    """

    name = ""
    state = None
    result = JobCompletionStatus.PENDING
    is_complete = False
    on_started = None
    on_complete = None
    on_failed = None

    def __init__(
        self, name: str, state, on_started=None, on_complete=None, on_failed=None
    ):
        self.name = name
        self.state = state
        self.result = JobCompletionStatus.PENDING
        self.is_complete = False
        self.on_started = on_started
        self.on_complete = on_complete
        self.on_failed = on_failed

    def load(self, row: Any):
        self.name = row[0]

    def execute(self):
        """
        Override this method to do the work
        throw exception if failure - don't eat exception
        :return: JobCompletionStatus in self.result
        """
        pass

    def work(self):
        """
        Internal work method - don't override unless necessary
        Override the execute method instead
        :return: None
        """
        try:
            if self.on_started is not None:
                self.on_started(self)
            self.execute()
            self.is_complete = True
            if self.on_complete is not None:
                self.on_complete(self)
        except Exception as ex:
            self.is_complete = True
            if self.on_failed is not None:
                self.on_failed(self)
