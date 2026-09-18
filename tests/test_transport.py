import httpx
import pytest
import respx

from keka_sdk.config import KekaConfig
from keka_sdk.exceptions import (
    KekaAPIError,
    KekaError,
    KekaNotFoundError,
    KekaRateLimitError,
)
from keka_sdk.transport import AsyncTransport, Transport, raise_for_keka_status

BASE = "https://acme.keka.com"


def _config(**kwargs):
    return KekaConfig(
        instance_url=BASE,
        retry_delay=0.0,
        backoff_factor=1.0,
        jitter=0.0,
        max_backoff=0.0,
        **kwargs,
    )


@respx.mock
def test_get_success_returns_response():
    respx.get(f"{BASE}/ping").mock(return_value=httpx.Response(200, json={"ok": True}))
    transport = Transport(_config())
    try:
        response = transport.get("ping")
        assert response.status_code == 200
        assert response.json() == {"ok": True}
    finally:
        transport.close()


@respx.mock
def test_retries_on_500_then_succeeds():
    route = respx.get(f"{BASE}/flaky").mock(
        side_effect=[httpx.Response(500), httpx.Response(200, json={"ok": True})]
    )
    transport = Transport(_config(max_retries=3))
    try:
        response = transport.get("flaky")
        assert response.status_code == 200
        assert route.call_count == 2
    finally:
        transport.close()


@respx.mock
def test_returns_last_response_after_exhausting_retries():
    respx.get(f"{BASE}/down").mock(return_value=httpx.Response(503))
    transport = Transport(_config(max_retries=2))
    try:
        response = transport.get("down")
        # Never None — the final 503 is returned for the caller to map.
        assert response.status_code == 503
    finally:
        transport.close()


@respx.mock
def test_connection_error_raises_keka_error():
    respx.get(f"{BASE}/boom").mock(side_effect=httpx.ConnectError("nope"))
    transport = Transport(_config(max_retries=1))
    try:
        with pytest.raises(KekaError):
            transport.get("boom")
    finally:
        transport.close()


def test_raise_for_keka_status_maps_errors():
    assert raise_for_keka_status(httpx.Response(200)).status_code == 200

    with pytest.raises(KekaNotFoundError):
        raise_for_keka_status(httpx.Response(404, json={"message": "nope"}))

    with pytest.raises(KekaAPIError):
        raise_for_keka_status(httpx.Response(500))

    with pytest.raises(KekaRateLimitError) as exc:
        raise_for_keka_status(httpx.Response(429, headers={"Retry-After": "12"}))
    assert exc.value.retry_after == 12.0


@respx.mock
async def test_async_get_success():
    respx.get(f"{BASE}/ping").mock(return_value=httpx.Response(200, json={"ok": True}))
    transport = AsyncTransport(_config())
    try:
        response = await transport.get("ping")
        assert response.json() == {"ok": True}
    finally:
        await transport.close()
