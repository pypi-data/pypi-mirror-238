from .common import *
from .consts import *

__version__ = Version(1, 0, 1)


def func(justin=JARVIS_FUNC, executor=None, handle_error=False, timeout=60, retry=None):
    def wrap(function):
        setattr(function, JARVIS_FUNC_FLAGS, justin)
        if executor is not None:
            setattr(function, JARVIS_FUNC_EXECUTOR_FLAGS, executor)
        if handle_error:
            setattr(function, JARVIS_FUNC_EXCEPTION_FLAGS, handle_error)
        if isinstance(timeout, (int, float)) and timeout > 0:
            setattr(function, JARVIS_FUNC_TIMEOUT_FLAGS, timeout)
        if isinstance(retry, int) and retry > 0:
            setattr(function, JARVIS_FUNC_RETRY_FLAGS, retry)
        return function

    return wrap

operator = func

def flow():
    def wrap(function):
        setattr(function, JARVIS_FLOW_FLAGS, True)
        return function
            
    return wrap
