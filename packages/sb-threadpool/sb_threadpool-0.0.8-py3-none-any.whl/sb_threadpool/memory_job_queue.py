from __future__ import annotations

import threading

from llist import sllist

from .job import Job
from .jobqueue import JobQueue


class QueueItem:
    def __init__(self, item):
        self.item = item
        self.in_progress = False


class MemoryJobQueue(JobQueue):
    """
    Use to queue jobs for the pool
    Internally stores the jobs in memory
    Override to store in db instead
    """
    queue: sllist
    lock: threading.Lock

    def __init__(self):
        super().__init__()
        self.queue = sllist()
        self.lock = threading.Lock()

    def get_job(self) -> Job | None:
        """
        Called by the threadpool to get the next job in the queue
        :return: Job
        """
        try:
            self.lock.acquire()
            if self.queue.size > 0:
                for i in range(self.queue.size - 1):
                    item: QueueItem = self.queue.nodeat(i).value
                    if not item.in_progress:
                        item.in_progress = True
                        return item.item

            return None
        finally:
            self.lock.release()

    def commit_job(self, job: Job):
        """
        called when the job was completed and should be removed from the queue
        :param job:
        :return:
        """
        try:
            self.lock.acquire()
            for i in range(self.queue.size - 1):
                node = self.queue.nodeat(i)
                item: QueueItem = node.value
                if item.item == job:
                    self.queue.remove(node)
                    return

            raise Exception("Not found")
        except Exception as ex:
            print(ex)
            raise
        finally:
            self.lock.release()

    def rollback_job(self, job: Job):
        """
        called when the job was not successful and should be reattempted
        :param job:
        :return:
        """
        try:
            self.lock.acquire()
            for i in range(self.queue.size - 1):
                item: QueueItem = self.queue.nodeat(i).value
                if item.item == job:
                    item.in_progress = False
                    return

            raise Exception("Not found")
        except Exception as ex:
            print(ex)
            raise

        finally:
            self.lock.release()

    def queue_job(self, job: Job):
        """
        Called by you to add a job to the queue
        :param job:
        :return: None
        """
        try:
            self.lock.acquire()
            self.queue.append(QueueItem(job))
        finally:
            self.lock.release()

    def count(self) -> int:
        """
        Number of outstanding items in the queue
        :return: int
        """
        try:
            self.lock.acquire()
            return self.queue.size
        finally:
            self.lock.release()

    def clear(self):
        """
        Clears the queue
        Returns: None
        """
        try:
            self.lock.acquire()
            self.queue.clear()
        finally:
            self.lock.release()
