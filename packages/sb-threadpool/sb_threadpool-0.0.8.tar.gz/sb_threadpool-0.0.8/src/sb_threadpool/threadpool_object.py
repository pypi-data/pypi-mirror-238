import time
from typing import List

from .jobqueue import JobQueue
from .pool_worker import PoolWorker


class ThreadPool:  # (threading.Thread):
    """ Thread pool class
        Manages pool of workers (which manage threads)
        Each worker retrieves next job from queue, executes it, then returns.
    """

    queue: JobQueue
    name: str = ""
    num_threads: int = 0
    verbose: bool = False
    workers: List[PoolWorker]

    def __init__(self, queue: JobQueue, name: str = "", num_threads: int = 5, on_started=None, on_complete=None,
                 on_failed=None, verbose: bool = False):
        self.queue = queue
        self.name = name
        self.num_threads = num_threads
        self.verbose = verbose
        self.workers = [PoolWorker(queue, f"{name}_{i}", on_started, on_complete, on_failed, verbose) for i in
                        range(num_threads)]

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.shutdown()

    def log(self, value: str):
        if self.verbose:
            print(value)

    def _kill_worker(self, worker: PoolWorker):
        self.log(f"Killing worker {worker.name}")
        worker.kill()
        time.sleep(0.1)
        while not worker.is_dead():
            worker.join(1)

    def shutdown(self):
        """ Shutdown the pool """
        self.log(f"Shutdown started")
        while len(self.workers) > 0:
            pool_worker = self.workers[0]
            self._kill_worker(pool_worker)
            del self.workers[0]

    def shutdown_when_done(self):
        """shutdown the pool when finished"""
        while self.busy():
            time.sleep(1)

        self.shutdown()

    def shutdown_when_done_this_job(self):
        """
        shutdown the pool when finished with current jobs
        clears the queue and waits for completion
        """
        self.queue.clear()
        while self.busy():
            time.sleep(1)

        self.shutdown()

    def current_threads(self):
        """retrieves the total workers in the list"""
        return len([worker for worker in self.workers if worker.is_alive()])

    def waiting_jobs(self):
        """number of jobs waiting in the queue"""
        return self.queue.count()

    def active_threads(self):
        return len([worker for worker in self.workers if worker.is_active()])

    def busy(self):
        """is the pool still busy"""
        return self.active_threads() > 0 or self.queue.count() > 0
