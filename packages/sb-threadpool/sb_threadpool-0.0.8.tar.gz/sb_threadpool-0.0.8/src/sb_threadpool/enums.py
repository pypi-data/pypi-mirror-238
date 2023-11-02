from enum import Enum


class JobCompletionStatus(Enum):
    """
    Status of the job
    Execute method should return this to instruct the pool what to do next
    """
    SUCCESS = 0
    """ Job completed successfully """
    FAIL_NO_RETRY = 1
    """ Job failed - do not attempt retry """
    FAIL_RETRY = 2
    """ Job failed - attempt retry """
    PENDING = 3
    """ Job not yet started """


class PoolWorkerState(Enum):
    """ Internal state of the worker """
    STOPPING = 1
    """ The worker is instructed to stop processing as soon as the current job is done """
    STARTING = 2
    """ The worker is starting up again after being idle """
    IDLE = 0
    """ The worker is idle """
    RUNNING = 3
    """ The worker is running a job """
    TERMINATED = 4
    """ The worker is terminated """
