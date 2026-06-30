from typing import Any, Dict, Optional

from ..auth import AsyncAuthManager, AuthManager
from ..config import KekaConfig
from ..transport import AsyncTransport, Transport, raise_for_keka_status
from ..utils.pagination import AsyncPaginatedCursor, PaginatedCursor


class BaseResource:
    """Base class for synchronous resources."""

    #: Endpoint path (relative to ``instance_url``) for the resource.
    endpoint: str = ""

    def __init__(self, transport: Transport, config: KekaConfig, auth: AuthManager):
        self._transport = transport
        self._config = config
        self._auth = auth

    def _authorize(self) -> None:
        """Ensure a valid token and apply it to the shared transport."""
        token = self._auth.ensure_token()
        self._transport.set_header("Authorization", f"Bearer {token}")

    def _build_path(self, *parts: str) -> str:
        segments = [self.endpoint.strip("/")] + [str(p).strip("/") for p in parts if p != ""]
        return "/".join(s for s in segments if s)

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._authorize()
        response = self._transport.get(path, params=params)
        raise_for_keka_status(response)
        payload: Dict[str, Any] = response.json()
        return payload

    def _post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self._authorize()
        response = self._transport.post(path, json=json, data=data)
        raise_for_keka_status(response)
        payload: Dict[str, Any] = response.json()
        return payload

    def _put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        self._authorize()
        response = self._transport.put(path, json=json, data=data)
        raise_for_keka_status(response)
        payload: Dict[str, Any] = response.json()
        return payload

    def _paginate(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        self._authorize()
        return PaginatedCursor.execute(self._transport, path, params=params)


class AsyncBaseResource:
    """Base class for asynchronous resources."""

    endpoint: str = ""

    def __init__(self, transport: AsyncTransport, config: KekaConfig, auth: AsyncAuthManager):
        self._transport = transport
        self._config = config
        self._auth = auth

    async def _authorize(self) -> None:
        """Ensure a valid token and apply it to the shared transport."""
        token = await self._auth.ensure_token()
        self._transport.set_header("Authorization", f"Bearer {token}")

    def _build_path(self, *parts: str) -> str:
        segments = [self.endpoint.strip("/")] + [str(p).strip("/") for p in parts if p != ""]
        return "/".join(s for s in segments if s)

    async def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._authorize()
        response = await self._transport.get(path, params=params)
        raise_for_keka_status(response)
        payload: Dict[str, Any] = response.json()
        return payload

    async def _post(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        await self._authorize()
        response = await self._transport.post(path, json=json, data=data)
        raise_for_keka_status(response)
        payload: Dict[str, Any] = response.json()
        return payload

    async def _put(
        self,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        await self._authorize()
        response = await self._transport.put(path, json=json, data=data)
        raise_for_keka_status(response)
        payload: Dict[str, Any] = response.json()
        return payload

    async def _paginate(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        await self._authorize()
        return await AsyncPaginatedCursor.execute(self._transport, path, params=params)
