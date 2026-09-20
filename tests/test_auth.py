import httpx
import pytest
import respx

from keka.auth import AsyncAuthManager, AuthManager, KekaAuth
from keka.config import KekaConfig
from keka.exceptions import KekaAuthError
from keka.transport import AsyncTransport, Transport

BASE = "https://acme.keka.com"
TOKEN_URL = "https://login.keka.com/connect/token"


def _config():
    return KekaConfig(instance_url=BASE, retry_delay=0.0, jitter=0.0)


def _auth():
    return KekaAuth(client_id="cid", client_secret="secret", api_key="key")


def test_keka_auth_default_grant_type():
    auth = _auth()
    data = auth.token_request_data()
    assert auth.grant_type == "kekaapi"
    assert data["grant_type"] == "kekaapi"
    # api_key is carried in the form body for this auth model.
    assert data["api_key"] == "key"
    headers = auth.token_request_headers()
    assert headers["Content-Type"] == "application/x-www-form-urlencoded"


@respx.mock
def test_authenticate_stores_token():
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    transport = Transport(_config())
    try:
        manager = AuthManager(_auth(), _config(), transport)
        token = manager.authenticate()
        assert token == "tok"
        assert manager.is_token_valid
        assert manager.auth_header() == {"Authorization": "Bearer tok"}
        assert route.called
    finally:
        transport.close()


@respx.mock
def test_ensure_token_caches():
    route = respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    transport = Transport(_config())
    try:
        manager = AuthManager(_auth(), _config(), transport)
        manager.ensure_token()
        manager.ensure_token()
        assert route.call_count == 1
    finally:
        transport.close()


@respx.mock
def test_authenticate_failure_raises_keka_auth_error():
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(401, json={"error_description": "bad creds"})
    )
    transport = Transport(_config())
    try:
        manager = AuthManager(_auth(), _config(), transport)
        with pytest.raises(KekaAuthError):
            manager.authenticate()
    finally:
        transport.close()


@respx.mock
def test_missing_access_token_raises():
    respx.post(TOKEN_URL).mock(return_value=httpx.Response(200, json={"token_type": "Bearer"}))
    transport = Transport(_config())
    try:
        manager = AuthManager(_auth(), _config(), transport)
        with pytest.raises(KekaAuthError):
            manager.authenticate()
    finally:
        transport.close()


@respx.mock
async def test_async_authenticate_stores_token():
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )
    transport = AsyncTransport(_config())
    try:
        manager = AsyncAuthManager(_auth(), _config(), transport)
        token = await manager.authenticate()
        assert token == "tok"
        assert manager.is_token_valid
    finally:
        await transport.close()
