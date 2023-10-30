import logging
import traceback
import types
from typing import Type


class LimitedTracebackFormatter(logging.Formatter):
    def __init__(self, *args, stack_trace_limit=5, **kwargs):
        super().__init__(*args, **kwargs)
        self._stack_trace_limit = stack_trace_limit

    def formatException(
        self, exc_info: tuple[Type[BaseException], BaseException, types.TracebackType] | tuple[None, None, None]
    ) -> str:
        _, _, tb = exc_info
        return "".join(traceback.format_tb(tb)[-self._stack_trace_limit :])


def get_logger(level: str) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.setLevel(level)
    fmt = LimitedTracebackFormatter("%(asctime)s - %(levelname)s - %(message)s")
    handler = logging.StreamHandler()
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger
