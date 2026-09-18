import httpx
import pytest
import respx

from keka_sdk import (
    AsyncKekaClient,
    KekaAuth,
    KekaClient,
    KekaConfig,
    KekaNotFoundError,
)

BASE = "https://acme.keka.com"
TOKEN_URL = "https://login.keka.com/connect/token"


def _config():
    return KekaConfig(instance_url=BASE, retry_delay=0.0, jitter=0.0)


def _auth():
    return KekaAuth(client_id="cid", client_secret="secret", api_key="key")


def _mock_token():
    respx.post(TOKEN_URL).mock(
        return_value=httpx.Response(200, json={"access_token": "tok", "expires_in": 3600})
    )


def test_client_rejects_non_keka_auth():
    with pytest.raises(TypeError):
        KekaClient("not-auth", BASE)  # type: ignore[arg-type]


def test_client_exposes_resources_and_instance_url():
    with KekaClient(_auth(), BASE) as client:
        assert client.instance_url == BASE
        assert client.hr is not None
        assert client.helpdesk is not None
        # One shared transport injected everywhere.
        assert client.hr._transport is client.transport
        assert client.helpdesk._transport is client.transport
        assert client.auth._transport is client.transport


@respx.mock
def test_search_employee_sends_token_and_returns_payload():
    _mock_token()
    search = respx.post(f"{BASE}/hris/employees/search").mock(
        return_value=httpx.Response(200, json={"succeeded": True, "data": {"id": "e1"}})
    )
    with KekaClient(_auth(), _config()) as client:
        result = client.hr.search_employee(work_email="a@acme.com")
        assert result["succeeded"] is True
        assert result["data"]["id"] == "e1"
        sent = search.calls.last.request
        assert sent.headers["Authorization"] == "Bearer tok"


def test_search_employee_requires_an_argument():
    with KekaClient(_auth(), BASE) as client:
        with pytest.raises(ValueError):
            client.hr.search_employee()


@respx.mock
def test_get_employee_not_found_maps_to_typed_error():
    _mock_token()
    respx.get(f"{BASE}/hris/employees/missing").mock(return_value=httpx.Response(404))
    with KekaClient(_auth(), _config()) as client:
        with pytest.raises(KekaNotFoundError):
            client.hr.get_employee("missing")


def test_create_employee_requires_mandatory_arguments():
    with KekaClient(_auth(), BASE) as client:
        with pytest.raises(TypeError):
            client.hr.create_employee(first_name="A")  # type: ignore[call-arg]


@respx.mock
async def test_async_client_search_employee():
    _mock_token()
    respx.post(f"{BASE}/hris/employees/search").mock(
        return_value=httpx.Response(200, json={"succeeded": True, "data": {"id": "e1"}})
    )
    async with AsyncKekaClient(_auth(), _config()) as client:
        result = await client.hr.search_employee(work_phone="+1555")
        assert result["data"]["id"] == "e1"
