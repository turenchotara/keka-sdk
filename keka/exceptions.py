from typing import Any, Optional


class KekaError(Exception):
    """Base class for every error raised by the Keka SDK."""


class KekaAuthError(KekaError):
    """Raised when authentication or token acquisition/refresh fails."""


class KekaAPIError(KekaError):
    """
    Raised when the Keka API returns an unsuccessful (non-2xx) response.

    Attributes:
        status_code: HTTP status code returned by the API.
        body: Parsed response body when available, otherwise the raw text.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        body: Any = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.body = body


class KekaRateLimitError(KekaAPIError):
    """
    Raised when the Keka API responds with HTTP 429 (Too Many Requests).

    Attributes:
        retry_after: Seconds to wait before retrying, parsed from the
            ``Retry-After`` header when present.
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        body: Any = None,
        retry_after: Optional[float] = None,
    ) -> None:
        super().__init__(message, status_code=status_code, body=body)
        self.retry_after = retry_after


class KekaNotFoundError(KekaAPIError):
    """Raised when the Keka API responds with HTTP 404 (Not Found)."""
