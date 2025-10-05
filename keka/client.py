import asyncio
import logging
import time
from typing import Any, Dict, Optional, Set
from urllib.parse import urljoin

import httpx

logger = logging.getLogger(__name__)


class ApiClient:
    """
    A basic API client with CRUD operations and automatic retry logic.

    Supports GET, POST, PATCH/PUT, and DELETE operations with exponential backoff
    for transient errors (timeouts, 5xx, and 429 responses).
    """

    def __init__(
            self,
            base_url: str,
            headers: Optional[Dict[str, str]] = None,
            timeout: float = 30.0,
            max_retries: int = 3,
            retry_delay: float = 1.0,
            backoff_factor: float = 2.0,
            retry_status_codes: Optional[Set[int]] = None
    ):
        """
        Initialize the API client.

        Args:
            base_url: The base URL for all API requests
            headers: Default headers to include in all requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries in seconds
            backoff_factor: Multiplier for exponential backoff
            retry_status_codes: Set of status codes to retry on
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.backoff_factor = backoff_factor
        self.retry_status_codes = retry_status_codes or {429, 500, 502, 503, 504}

        # Initialize HTTP client
        self.client = httpx.Client(
            timeout=timeout,
            headers=self.headers
        )

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return urljoin(self.base_url + '/', endpoint.lstrip('/'))

    def _should_retry(self, response: httpx.Response, exception: Optional[Exception] = None) -> bool:
        """Determine if a request should be retried."""
        if exception:
            # Retry on connection errors, timeouts, etc.
            return True

        if response.status_code in self.retry_status_codes:
            return True

        return False

    def _make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response | None:
        """
        Make an HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PATCH, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers for this request

        Returns:
            httpx.Response object

        Raises:
            httpx.HTTPError: If all retries are exhausted
        """
        url = self._build_url(endpoint).strip("/")
        request_headers = {**self.headers, **(headers or {})}

        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.request(
                    method=method,
                    url=url,
                    json=json,
                    data=data,
                    params=params,
                    headers=request_headers
                )

                # Check if we should retry
                if self._should_retry(response):
                    if attempt < self.max_retries:
                        delay = self.retry_delay * (self.backoff_factor ** attempt)
                        logger.warning(
                            f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}). "
                            f"Status: {response.status_code}. Retrying in {delay:.2f}s..."
                        )
                        time.sleep(delay)
                        continue
                    else:
                        logger.error(f"Request failed after {self.max_retries + 1} attempts")

                return response

            except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError) as e:
                if attempt < self.max_retries:
                    delay = self.retry_delay * (self.backoff_factor ** attempt)
                    logger.warning(
                        f"Request failed with exception (attempt {attempt + 1}/{self.max_retries + 1}): "
                        f"{type(e).__name__}. Retrying in {delay:.2f}s..."
                    )
                    time.sleep(delay)
                    continue
                else:
                    logger.error(f"Request failed after {self.max_retries + 1} attempts")
                    raise
        return None

    def get(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform a GET request."""
        return self._make_request('GET', endpoint, params=params, headers=headers)

    def post(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform a POST request."""
        return self._make_request('POST', endpoint, data=data, json=json, params=params, headers=headers)

    def put(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform a PUT request."""
        return self._make_request('PUT', endpoint, data=data, params=params, headers=headers)

    def patch(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform a PATCH request."""
        return self._make_request('PATCH', endpoint, data=data, params=params, headers=headers)

    def delete(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform a DELETE request."""
        return self._make_request('DELETE', endpoint, params=params, headers=headers)

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncApiClient:
    """
    An async API client with CRUD operations and automatic retry logic.

    Supports GET, POST, PATCH/PUT, and DELETE operations with exponential backoff
    for transient errors (timeouts, 5xx, and 429 responses).
    """

    def __init__(
            self,
            base_url: str,
            headers: Optional[Dict[str, str]] = None,
            timeout: float = 30.0,
            max_retries: int = 3,
            retry_delay: float = 1.0,
            backoff_factor: float = 2.0,
            retry_status_codes: Optional[Set[int]] = None
    ):
        """
        Initialize the async API client.

        Args:
            base_url: The base URL for all API requests
            headers: Default headers to include in all requests
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries in seconds
            backoff_factor: Multiplier for exponential backoff
            retry_status_codes: Set of status codes to retry on
        """
        self.base_url = base_url.rstrip('/')
        self.headers = headers or {}
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.backoff_factor = backoff_factor
        self.retry_status_codes = retry_status_codes or {429, 500, 502, 503, 504}

        # Initialize async HTTP client
        self.client = httpx.AsyncClient(
            timeout=timeout,
            headers=self.headers
        )

    def _build_url(self, endpoint: str) -> str:
        """Build full URL from endpoint."""
        return urljoin(self.base_url + '/', endpoint.lstrip('/'))

    def _should_retry(self, response: httpx.Response, exception: Optional[Exception] = None) -> bool:
        """Determine if a request should be retried."""
        if exception:
            # Retry on connection errors, timeouts, etc.
            return True

        if response.status_code in self.retry_status_codes:
            return True

        return False

    async def _make_request(
            self,
            method: str,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response | None:
        """
        Make an async HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PATCH, PUT, DELETE)
            endpoint: API endpoint
            data: Request body data
            params: Query parameters
            headers: Additional headers for this request

        Returns:
            httpx.Response object

        Raises:
            httpx.HTTPError: If all retries are exhausted
        """
        url = self._build_url(endpoint)
        request_headers = {**self.headers, **(headers or {})}

        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(
                    method=method,
                    url=url,
                    json=data,
                    params=params,
                    headers=request_headers
                )

                # Check if we should retry
                if self._should_retry(response):
                    if attempt < self.max_retries:
                        delay = self.retry_delay * (self.backoff_factor ** attempt)
                        logger.warning(
                            f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}). "
                            f"Status: {response.status_code}. Retrying in {delay:.2f}s..."
                        )
                        await asyncio.sleep(delay)
                        continue
                    else:
                        logger.error(f"Request failed after {self.max_retries + 1} attempts")

                return response

            except (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError) as e:
                if attempt < self.max_retries:
                    delay = self.retry_delay * (self.backoff_factor ** attempt)
                    logger.warning(
                        f"Request failed with exception (attempt {attempt + 1}/{self.max_retries + 1}): "
                        f"{type(e).__name__}. Retrying in {delay:.2f}s..."
                    )
                    await asyncio.sleep(delay)
                    continue
                else:
                    logger.error(f"Request failed after {self.max_retries + 1} attempts")
                    raise
        return None

    async def get(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform an async GET request."""
        return await self._make_request('GET', endpoint, params=params, headers=headers)

    async def post(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform an async POST request."""
        return await self._make_request('POST', endpoint, data=data, params=params, headers=headers)

    async def put(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform an async PUT request."""
        return await self._make_request('PUT', endpoint, data=data, params=params, headers=headers)

    async def patch(
            self,
            endpoint: str,
            data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform an async PATCH request."""
        return await self._make_request('PATCH', endpoint, data=data, params=params, headers=headers)

    async def delete(
            self,
            endpoint: str,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None
    ) -> httpx.Response:
        """Perform an async DELETE request."""
        return await self._make_request('DELETE', endpoint, params=params, headers=headers)

    async def close(self):
        """Close the async HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


# Legacy Client class for backward compatibility
class Client:
    def __init__(self, instant_url):
        self.instant_url = instant_url
