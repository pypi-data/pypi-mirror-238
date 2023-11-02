from __future__ import annotations

import threading
import time
from datetime import datetime

from .enums import PoolWorkerState, JobCompletionStatus
from .job import Job
from .jobqueue import JobQueue
from .utils import async_raise


class PoolWorker(threading.Thread):
    """
    Internal worker object of the threadpool
    """
    terminate: bool = False
    queue: JobQueue = None
    name: str = ""
    verbose: bool = False
    state: PoolWorkerState = PoolWorkerState.IDLE
    job: Job | None = None
    idle_stamp: datetime
    on_started = None
    on_complete = None
    on_failed = None

    def __init__(self, queue: JobQueue, name: str, on_started=None, on_complete=None, on_failed=None, verbose: bool = False):
        threading.Thread.__init__(self)
        self.terminate = False
        self.queue = queue
        self.name = name
        self.verbose = verbose
        self.state = PoolWorkerState.IDLE
        self.job = None
        self.idle_stamp = datetime.min
        self.log(f"Worker {self.name} starting")
        self.on_started = on_started
        self.on_complete = on_complete
        self.on_failed = on_failed
        self.start()

    def log(self, value: str):
        if self.verbose:
            print(value)

    def stop(self):
        self.state = PoolWorkerState.STOPPING

    def kill(self):
        self.terminate = True

    def force_kill(self):
        async_raise(self._get_my_tid(), Exception)

    def is_dead(self):
        return self.state == PoolWorkerState.TERMINATED

    def is_active(self):
        return self.state == PoolWorkerState.RUNNING or self.state == PoolWorkerState.STARTING

    def is_alive(self):
        return self.state == PoolWorkerState.RUNNING \
            or self.state == PoolWorkerState.STARTING \
            or self.state == PoolWorkerState.IDLE

    def get_next_job(self):
        try:
            job: Job = self.queue.get_job()

            if job is None:
                return False

            self.log(f"{self.name} picked up job {job.name}")
            self.job = job
            self.state = PoolWorkerState.STARTING
            return True
        except Exception as ex:
            print(ex)
            return False

    def run(self) -> None:
        while True:
            try:
                if self.terminate:
                    self.state = PoolWorkerState.TERMINATED
                    return

                if self.state == PoolWorkerState.STARTING:
                    self.log(f"{self.name} starting")
                    self.state = PoolWorkerState.RUNNING

                if self.state == PoolWorkerState.STOPPING:
                    self.log(f"{self.name} stopping")
                    self.state = PoolWorkerState.IDLE

                if self.state == PoolWorkerState.IDLE:
                    if not self.get_next_job():
                        if self.idle_stamp == datetime.min:
                            self.idle_stamp = datetime.now()
                        time.sleep(0.1)

                if self.state == PoolWorkerState.RUNNING:
                    self.idle_stamp = datetime.min
                    if self.job is not None:
                        self.log(f"{self.name} running job {self.job.name}")
                        self.job.on_started = self.on_started
                        self.job.on_complete = self.on_complete
                        self.job.on_failed = self.on_failed
                        self.job.work()
                        self.job.on_started = None
                        self.job.on_complete = None
                        self.job.on_failed = None
                        if self.job.result == JobCompletionStatus.SUCCESS:
                            self.queue.commit_job(self.job)
                        elif self.job.result == JobCompletionStatus.FAIL_RETRY:
                            self.queue.rollback_job(self.job)
                        elif self.job.result == JobCompletionStatus.FAIL_NO_RETRY:
                            self.queue.fail_job(self.job)
                        self.log(f"{self.name} done job {self.job.name}")
                        self.state = PoolWorkerState.IDLE
                    else:
                        self.state = PoolWorkerState.IDLE

            except Exception as ex:
                print(ex)
                self.state = PoolWorkerState.TERMINATED
                return

    def _get_my_tid(self):
        """determines this (self's) thread id """

        if not self.is_alive():
            raise threading.ThreadError("the thread is not active")

        for tid, tobj in threading._active.items():
            if tobj is self:
                return tid

        raise AssertionError("could not determine the thread's id")
