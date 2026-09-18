import logging
from typing import Any, AsyncGenerator, Dict, Generator, Optional
import httpx

logger = logging.getLogger(__name__)


def _format_paginated_response(data: Dict[str, Any], next_page_gen: Any) -> Dict[str, Any]:
    """Helper to structure the paginated response exactly as requested."""
    return {
        "succeeded": data.get("succeeded", True),
        "message": data.get("message", ""),
        "errors": data.get("errors", []),
        "data": data.get("data", []),
        "next_page": next_page_gen
    }


class PaginatedCursor:
    """
    A cursor/generator class to handle paginated API responses.

    The generator preserves all original query parameters (filters, sorting,
    page size, etc.) and constructs each subsequent page request internally.
    It does NOT rely on the ``nextPage`` URL returned by the API.

    Each yielded page includes its own ``next_page`` generator for the
    remaining pages, or ``None`` if it is the last page.
    """

    def __init__(
        self,
        client: Any,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        initial_response: Optional[httpx.Response] = None,
        initial_data: Optional[Dict[str, Any]] = None
    ):
        self.client = client
        self.endpoint = endpoint
        self.params = params or {}
        self.headers = headers or {}
        self._initial_response = initial_response
        self._initial_data = initial_data
        self._current_page = 0
        self._total_pages: int = 1

    @classmethod
    def execute(
        cls,
        client: Any,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create a paginated cursor by making the initial API call.
        Returns the initial dictionary payload formatted with the generator attached.
        """
        response = client.get(endpoint=endpoint, params=params, headers=headers)

        if response is None or response.status_code != 200:
            status = response.status_code if response else "None"
            logger.warning(f"Initial pagination request failed: {status}")
            return _format_paginated_response({}, None)

        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Failed to parse initial response: {e}")
            return _format_paginated_response({}, None)

        if not isinstance(data, dict):
            return _format_paginated_response({}, None)

        page_number = data.get("pageNumber", 1)
        total_pages = data.get("totalPages", 1)
        if page_number >= total_pages:
            return _format_paginated_response(data, None)

        cursor = cls(
            client=client,
            endpoint=endpoint,
            params=params,
            headers=headers,
            initial_response=response,
            initial_data=data
        )
        cursor._current_page = page_number
        cursor._total_pages = total_pages

        return _format_paginated_response(data, cursor._generator())

    def _generator(self) -> Generator[Dict[str, Any], None, None]:
        """
        Internal generator that yields subsequent pages on demand.

        Each yielded page is a formatted response dict. If more pages remain
        after the yielded page, its ``next_page`` field contains a new
        generator for the remaining pages; otherwise ``next_page`` is ``None``.

        After the last page has been yielded, the generator returns (which
        causes ``StopIteration`` to be raised on the next ``next()`` call).
        """
        while self._current_page < self._total_pages:
            try:
                self._current_page += 1

                # Build params from the original request, overriding only pageNumber
                next_params = dict(self.params)
                next_params['pageNumber'] = self._current_page

                response = self.client.get(
                    endpoint=self.endpoint,
                    params=next_params,
                    headers=self.headers
                )

                if response is None or response.status_code != 200:
                    logger.warning(f"Failed to fetch page {self._current_page}")
                    return  # raises StopIteration

                data = response.json()
                if not isinstance(data, dict):
                    return  # raises StopIteration

                # Allow totalPages to update from server (dynamic datasets)
                self._total_pages = data.get("totalPages", self._total_pages)

                # Attach a generator for remaining pages, or None on last page
                if self._current_page < self._total_pages:
                    next_gen = self._generator()
                else:
                    next_gen = None

                yield _format_paginated_response(data, next_gen)

            except Exception as e:
                logger.error(f"Error fetching page {self._current_page}: {e}")
                return  # raises StopIteration


class AsyncPaginatedCursor:
    """
    An async cursor/generator class to handle paginated API responses.

    Mirrors ``PaginatedCursor`` but uses ``async/await`` for I/O.
    """

    def __init__(
        self,
        client: Any,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        initial_response: Optional[httpx.Response] = None,
        initial_data: Optional[Dict[str, Any]] = None
    ):
        self.client = client
        self.endpoint = endpoint
        self.params = params or {}
        self.headers = headers or {}
        self._initial_response = initial_response
        self._initial_data = initial_data
        self._current_page = 0
        self._total_pages: int = 1

    @classmethod
    async def execute(
        cls,
        client: Any,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create an async paginated cursor by making the initial API call.
        Returns the initial dictionary payload formatted with the generator attached.
        """
        response = await client.get(endpoint=endpoint, params=params, headers=headers)

        if response is None or response.status_code != 200:
            status = response.status_code if response else "None"
            logger.warning(f"Initial pagination request failed: {status}")
            return _format_paginated_response({}, None)

        try:
            data = response.json()
        except Exception as e:
            logger.error(f"Failed to parse initial response: {e}")
            return _format_paginated_response({}, None)

        if not isinstance(data, dict):
            return _format_paginated_response({}, None)

        page_number = data.get("pageNumber", 1)
        total_pages = data.get("totalPages", 1)
        if page_number >= total_pages:
            return _format_paginated_response(data, None)

        cursor = cls(
            client=client,
            endpoint=endpoint,
            params=params,
            headers=headers,
            initial_response=response,
            initial_data=data
        )
        cursor._current_page = page_number
        cursor._total_pages = total_pages

        return _format_paginated_response(data, cursor._async_generator())

    def _async_generator(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Internal async generator that yields subsequent pages on demand.

        Each yielded page is a formatted response dict. If more pages remain
        after the yielded page, its ``next_page`` field contains a new async
        generator for the remaining pages; otherwise ``next_page`` is ``None``.
        """
        async def _gen() -> AsyncGenerator[Dict[str, Any], None]:
            while self._current_page < self._total_pages:
                try:
                    self._current_page += 1

                    next_params = dict(self.params)
                    next_params['pageNumber'] = self._current_page

                    response = await self.client.get(
                        endpoint=self.endpoint,
                        params=next_params,
                        headers=self.headers
                    )

                    if response is None or response.status_code != 200:
                        logger.warning(f"Failed to fetch async page {self._current_page}")
                        return

                    data = response.json()
                    if not isinstance(data, dict):
                        return

                    self._total_pages = data.get("totalPages", self._total_pages)

                    if self._current_page < self._total_pages:
                        next_gen = self._async_generator()
                    else:
                        next_gen = None

                    yield _format_paginated_response(data, next_gen)

                except Exception as e:
                    logger.error(f"Error fetching page {self._current_page}: {e}")
                    return

        return _gen()
