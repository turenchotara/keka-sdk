import asyncio
import logging
import random
import time
from typing import Any, Dict, Optional
from urllib.parse import urljoin

import httpx

from .config import KekaConfig
from .exceptions import (
    KekaAPIError,
    KekaError,
    KekaNotFoundError,
    KekaRateLimitError,
)

logger = logging.getLogger(__name__)


def _parse_retry_after(response: httpx.Response) -> Optional[float]:
    """Parse the ``Retry-After`` header (seconds) when present and numeric."""
    value = response.headers.get("Retry-After")
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _safe_body(response: httpx.Response) -> Any:
    """Return parsed JSON body, falling back to text, for error reporting."""
    try:
        return response.json()
    except Exception:
        return response.text


def raise_for_keka_status(response: httpx.Response) -> httpx.Response:
    """
    Map a non-2xx response to the Keka error hierarchy.

    Returns the response unchanged on success so callers can chain the call.
    """
    if response.is_success:
        return response

    status = response.status_code
    body = _safe_body(response)
    message = f"Keka API request failed with status {status}"

    if status == 429:
        raise KekaRateLimitError(
            message, status_code=status, body=body, retry_after=_parse_retry_after(response)
        )
    if status == 404:
        raise KekaNotFoundError(message, status_code=status, body=body)
    raise KekaAPIError(message, status_code=status, body=body)


class _RetryCore:
    """Shared retry/error logic for the sync and async transports."""

    def __init__(self, config: KekaConfig):
        self._config = config

    def _build_url(self, endpoint: str) -> str:
        base = self._config.instance_url + "/"
        url = urljoin(base, endpoint.lstrip("/"))
        if not endpoint.endswith("/") and url.endswith("/"):
            url = url.rstrip("/")
        return url

    def _should_retry(
        self, response: Optional[httpx.Response], exception: Optional[Exception]
    ) -> bool:
        if exception is not None:
            return True
        if response is not None and response.status_code in self._config.retry_status_codes:
            return True
        return False

    def _compute_delay(self, attempt: int, retry_after: Optional[float]) -> float:
        """Exponential backoff with jitter, capped, honoring ``Retry-After``."""
        if retry_after is not None:
            return min(retry_after, self._config.max_backoff)
        base = self._config.retry_delay * (self._config.backoff_factor ** attempt)
        capped = min(base, self._config.max_backoff)
        return capped + random.uniform(0, self._config.jitter)


class Transport(_RetryCore):
    """Synchronous transport backed by a single ``httpx.Client``."""

    def __init__(self, config: KekaConfig, headers: Optional[Dict[str, str]] = None):
        super().__init__(config)
        self.headers: Dict[str, str] = headers or {}
        self._client = httpx.Client(timeout=config.timeout, headers=self.headers)

    def set_header(self, key: str, value: str) -> None:
        """Set a default header applied to every subsequent request."""
        self.headers[key] = value
        self._client.headers[key] = value

    def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        url = self._build_url(endpoint)
        last_response: Optional[httpx.Response] = None

        for attempt in range(self._config.max_retries + 1):
            response: Optional[httpx.Response] = None
            exception: Optional[Exception] = None
            try:
                response = self._client.request(
                    method=method, url=url, json=json, data=data, params=params, headers=headers
                )
                last_response = response
            except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError) as exc:
                exception = exc

            if self._should_retry(response, exception) and attempt < self._config.max_retries:
                retry_after = _parse_retry_after(response) if response is not None else None
                delay = self._compute_delay(attempt, retry_after)
                logger.warning(
                    "Request to %s failed (attempt %d/%d); retrying in %.2fs",
                    url, attempt + 1, self._config.max_retries + 1, delay,
                )
                time.sleep(delay)
                continue

            if exception is not None:
                raise KekaError(f"Request to {url} failed: {exception}") from exception
            if response is None:
                raise KekaError(f"Request to {url} failed: no response received")
            return response

        if last_response is not None:
            return last_response
        raise KekaError(f"Request to {url} failed after {self._config.max_retries + 1} attempts")

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return self.request("GET", endpoint, params=params, headers=headers)

    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
             json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return self.request("POST", endpoint, data=data, json=json, params=params, headers=headers)

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return self.request("PUT", endpoint, data=data, json=json, params=params, headers=headers)

    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
              json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None,
              headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return self.request("PATCH", endpoint, data=data, json=json, params=params, headers=headers)

    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return self.request("DELETE", endpoint, params=params, headers=headers)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "Transport":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()


class AsyncTransport(_RetryCore):
    """Asynchronous transport backed by a single ``httpx.AsyncClient``."""

    def __init__(self, config: KekaConfig, headers: Optional[Dict[str, str]] = None):
        super().__init__(config)
        self.headers: Dict[str, str] = headers or {}
        self._client = httpx.AsyncClient(timeout=config.timeout, headers=self.headers)

    def set_header(self, key: str, value: str) -> None:
        """Set a default header applied to every subsequent request."""
        self.headers[key] = value
        self._client.headers[key] = value

    async def request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> httpx.Response:
        url = self._build_url(endpoint)
        last_response: Optional[httpx.Response] = None

        for attempt in range(self._config.max_retries + 1):
            response: Optional[httpx.Response] = None
            exception: Optional[Exception] = None
            try:
                response = await self._client.request(
                    method=method, url=url, json=json, data=data, params=params, headers=headers
                )
                last_response = response
            except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError) as exc:
                exception = exc

            if self._should_retry(response, exception) and attempt < self._config.max_retries:
                retry_after = _parse_retry_after(response) if response is not None else None
                delay = self._compute_delay(attempt, retry_after)
                logger.warning(
                    "Request to %s failed (attempt %d/%d); retrying in %.2fs",
                    url, attempt + 1, self._config.max_retries + 1, delay,
                )
                await asyncio.sleep(delay)
                continue

            if exception is not None:
                raise KekaError(f"Request to {url} failed: {exception}") from exception
            if response is None:
                raise KekaError(f"Request to {url} failed: no response received")
            return response

        if last_response is not None:
            return last_response
        raise KekaError(f"Request to {url} failed after {self._config.max_retries + 1} attempts")

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return await self.request("GET", endpoint, params=params, headers=headers)

    async def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                   json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None,
                   headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return await self.request(
            "POST", endpoint, data=data, json=json, params=params, headers=headers
        )

    async def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                  json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None,
                  headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return await self.request(
            "PUT", endpoint, data=data, json=json, params=params, headers=headers
        )

    async def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
                    json: Optional[Dict[str, Any]] = None, params: Optional[Dict[str, Any]] = None,
                    headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return await self.request(
            "PATCH", endpoint, data=data, json=json, params=params, headers=headers
        )

    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
                     headers: Optional[Dict[str, str]] = None) -> httpx.Response:
        return await self.request("DELETE", endpoint, params=params, headers=headers)

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncTransport":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()
