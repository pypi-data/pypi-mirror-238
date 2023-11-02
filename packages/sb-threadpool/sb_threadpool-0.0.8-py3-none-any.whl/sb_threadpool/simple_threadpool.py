from threading import Thread

from .enums import JobCompletionStatus
from .job import Job
from .jobqueue import JobQueue


class SimpleWorker(Thread):
    job: Job

    def __init__(self, job: Job):
        super().__init__()
        self.job = job
        self.start()

    def run(self):
        self.job.work()

    def result(self) -> JobCompletionStatus:
        return self.job.result


class SimpleThreadpool:
    queue: JobQueue
    name: str = ""
    num_threads: int = 0
    verbose: bool = False
    threads: list[SimpleWorker]

    def __init__(
        self, queue: JobQueue, name: str, num_threads: int = 1, verbose: bool = False
    ):
        super().__init__()
        self.queue = queue
        self.name = name
        self.num_threads = num_threads
        self.verbose = verbose
        self.threads: list[SimpleWorker] = []

    def loop(self) -> None:
        for thread in self.threads:
            if not thread.is_alive():
                result = thread.result()
                if result == JobCompletionStatus.SUCCESS:
                    self.queue.commit_job(thread.job)
                elif result == JobCompletionStatus.FAIL_RETRY:
                    self.queue.rollback_job(thread.job)
                else:
                    self.queue.commit_job(thread.job)
                self.threads.remove(thread)

        while len(self.threads) < self.num_threads:
            job: Job = self.queue.get_job()
            if job is not None:
                self.threads.append(SimpleWorker(job))

    def shutdown(self):
        for thread in self.threads:
            thread.join(1000)

    def thread_count(self):
        return len(self.threads)
