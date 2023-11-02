from __future__ import annotations

from typing import TypeVar

T = TypeVar("T", bound="Job")


class JobQueue:
    """
    Use to queue jobs for the pool
    Internally stores the jobs in memory
    Override to store in db instead
    """

    def __init__(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def get_job(self) -> T:
        """
        Called by the threadpool to get the next job in the queue
        :return: Job
        """
        pass

    def commit_job(self, job: T):
        """
        called when the job was completed and should be removed from the queue
        :param job:
        :return:
        """
        pass

    def rollback_job(self, job: T):
        """
        called when the job was not successful and should be reattempted
        :param job:
        :return:
        """
        pass

    def fail_job(self, job: T):
        """
        called when the job was not successful and should NOT be reattempted
        :param job:
        :return:
        """
        pass

    def queue_job(self, job: T):
        """
        Called by you to add a job to the queue
        :param job:
        :return: None
        """
        pass

    def count(self) -> int:
        """
        Number of outstanding items in the queue
        :return: int
        """
        pass

    def clear(self):
        """
        Clears the queue
        Returns: None
        """
        pass

    def close(self):
        """
        Shutdown resources
        """
        pass
