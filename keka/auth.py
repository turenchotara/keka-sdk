import logging
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

from .config import KekaConfig
from .exceptions import KekaAuthError
from .transport import AsyncTransport, Transport

logger = logging.getLogger(__name__)

# Re-authenticate slightly before actual expiry to avoid edge-of-expiry races.
_EXPIRY_SKEW_SECONDS = 30.0


@dataclass
class KekaAuth:
    """
    Keka API credentials.

    Args:
        client_id: OAuth client identifier.
        client_secret: OAuth client secret.
        api_key: Keka API key (sent as the ``X-API-Key`` header).
        scope: OAuth scope (Keka uses ``kekaapi``).
        grant_type: OAuth grant type. Defaults to ``kekaapi``.
    """

    client_id: str
    client_secret: str
    api_key: str
    scope: str = "kekaapi"
    grant_type: str = "kekaapi"

    def token_request_data(self) -> Dict[str, str]:
        """Form body for the token request."""
        return {
            "grant_type": self.grant_type,
            "scope": self.scope,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "api_key": self.api_key,
        }

    def token_request_headers(self) -> Dict[str, str]:
        """Headers for the token request."""
        return {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }


class _TokenState:
    """Shared, transport-agnostic token storage and parsing."""

    def __init__(self, credentials: KekaAuth, config: KekaConfig):
        self._credentials = credentials
        self._config = config
        self._access_token: Optional[str] = None
        self._token_type: str = "Bearer"
        self._expires_at: Optional[float] = None

    @property
    def access_token(self) -> Optional[str]:
        return self._access_token

    @property
    def is_token_valid(self) -> bool:
        if not self._access_token:
            return False
        if self._expires_at is None:
            return True
        return time.time() < (self._expires_at - _EXPIRY_SKEW_SECONDS)

    def auth_header(self) -> Dict[str, str]:
        """Authorization header for API requests; empty if not authenticated."""
        if self._access_token:
            return {"Authorization": f"{self._token_type} {self._access_token}"}
        return {}

    def clear(self) -> None:
        self._access_token = None
        self._expires_at = None

    def _store_token(self, payload: Dict[str, Any]) -> None:
        access_token = payload.get("access_token")
        if not access_token:
            raise KekaAuthError("No access_token in authentication response")
        self._access_token = access_token
        self._token_type = payload.get("token_type", "Bearer")
        expires_in = payload.get("expires_in")
        self._expires_at = time.time() + float(expires_in) if expires_in else None
        logger.info("Keka access token acquired")


class AuthManager(_TokenState):
    """Synchronous token lifecycle manager."""

    def __init__(self, credentials: KekaAuth, config: KekaConfig, transport: Transport):
        super().__init__(credentials, config)
        self._transport = transport

    def authenticate(self) -> str:
        """Acquire a fresh access token and return it."""
        response = self._transport.post(
            self._config.token_url,
            data=self._credentials.token_request_data(),
            headers=self._credentials.token_request_headers(),
        )
        if not response.is_success:
            detail = ""
            try:
                body = response.json()
                detail = f" - {body.get('error_description') or body.get('error') or body}"
            except Exception:
                pass
            raise KekaAuthError(
                f"Authentication failed: {response.status_code}{detail}"
            )
        self._store_token(response.json())
        if not self._access_token:
            raise KekaAuthError("Authentication succeeded but access token is empty")
        return self._access_token

    def ensure_token(self) -> str:
        """Return a valid token, authenticating/refreshing as needed."""
        if self.is_token_valid and self._access_token:
            return self._access_token
        return self.authenticate()

    def refresh(self) -> str:
        """Force re-acquisition of the access token."""
        self.clear()
        return self.authenticate()


class AsyncAuthManager(_TokenState):
    """Asynchronous token lifecycle manager."""

    def __init__(self, credentials: KekaAuth, config: KekaConfig, transport: AsyncTransport):
        super().__init__(credentials, config)
        self._transport = transport

    async def authenticate(self) -> str:
        """Acquire a fresh access token and return it."""
        response = await self._transport.post(
            self._config.token_url,
            data=self._credentials.token_request_data(),
            headers=self._credentials.token_request_headers(),
        )
        if not response.is_success:
            detail = ""
            try:
                body = response.json()
                detail = f" - {body.get('error_description') or body.get('error') or body}"
            except Exception:
                pass
            raise KekaAuthError(
                f"Authentication failed: {response.status_code}{detail}"
            )
        self._store_token(response.json())
        if not self._access_token:
            raise KekaAuthError("Authentication succeeded but access token is empty")
        return self._access_token

    async def ensure_token(self) -> str:
        """Return a valid token, authenticating/refreshing as needed."""
        if self.is_token_valid and self._access_token:
            return self._access_token
        return await self.authenticate()

    async def refresh(self) -> str:
        """Force re-acquisition of the access token."""
        self.clear()
        return await self.authenticate()


AnyAuthManager = Union[AuthManager, AsyncAuthManager]
