from impaction_ai.constants import (
    API_MAX_RETIRES,
    FLUSH_BATCH_SIZE,
    FLUSH_INTERVAL_MS,
    FLUSH_TIMEOUT_SECONDS,
    MAX_BUFFER_SIZE,
)


class Config:
    def __init__(
        self,
        flush_interval_ms: int = FLUSH_INTERVAL_MS,
        flush_batch_size: int = FLUSH_BATCH_SIZE,
        flush_timeout_seconds: int = FLUSH_TIMEOUT_SECONDS,
        max_buffer_size: int = MAX_BUFFER_SIZE,
        api_max_retries: int = API_MAX_RETIRES,
    ):
        """impaction.ai client configuration to adjust the behavior of the SDK.

        Args:
            flush_interval_ms (int, optional): Interval for consuming the buffer. Defaults to 3000.
            flush_batch_size (int, optional): Batch size for consuming the buffer. Defaults to 50.
            flush_timeout_seconds (int, optional): The timeout seconds, used for flush() and close(), after which the SDK will stop flushing. For close(), the remaining data in the buffer will be lost after the timeout. Defaults to 5.
            max_buffer_size (int, optional): Maximum buffer size. Defaults to 200.
            api_max_retries (int, optional): The number of retries for sending API request. Defaults to 3.
        """  # noqa: E501
        self.flush_interval_ms = flush_interval_ms
        self.flush_batch_size = flush_batch_size
        self.flush_timeout_seconds = flush_timeout_seconds
        self.max_buffer_size = max_buffer_size
        self.api_max_retries = api_max_retries
