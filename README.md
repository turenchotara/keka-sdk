# Keka SDK

A composition-based Python SDK for the [Keka HR API](https://developers.keka.com/reference).
It provides a single client facade with one shared HTTP transport (connection pool),
one auth manager, typed resources, automatic retries with jitter, and a typed error
hierarchy. Both synchronous and asynchronous clients are available.

## Features

- **Single client facade** — `KekaClient` / `AsyncKekaClient` expose `.hr` and `.helpdesk`.
- **One transport, one pool** — a single `httpx` client is created by the client and injected
  into the auth manager and every resource (no per-resource connection pools).
- **Single auth system** — `AuthManager` owns token acquisition/refresh/expiry; the OAuth token
  endpoint is derived from your `instance_url` (no hardcoded hosts), using `client_credentials`.
- **Typed errors** — `KekaError` base with `KekaAuthError`, `KekaAPIError`, `KekaRateLimitError`,
  and `KekaNotFoundError`.
- **Resilient retries** — exponential backoff with jitter and a max cap; honors `Retry-After` on 429.
- **Pagination** — lazy cursor that preserves your query parameters across pages.
- **Typed responses** — `TypedDict` models and a shipped `py.typed` marker.

## Installation

```bash
pip install keka-sdk
```

From source:

```bash
git clone https://github.com/turenchotara/keka-sdk.git
cd keka-sdk
pip install -e .[dev]
```

## Quick Start

### Synchronous

```python
from keka_sdk import KekaClient, KekaAuth

auth = KekaAuth(
    client_id="your-client-id",
    client_secret="your-client-secret",
    api_key="your-api-key",
)

with KekaClient(auth, "https://your-company.keka.com") as client:
    # Token is acquired lazily on the first authenticated call.
    result = client.hr.search_employee(work_email="john.doe@your-company.com")
    if result.get("succeeded"):
        print(result["data"])

    # Paginated listing — iterate pages via the next_page generator.
    page = client.hr.list_employees(status="active", pageSize=50)
    print(page["data"])
    gen = page["next_page"]
    while gen is not None:
        page = next(gen)
        print(page["data"])
        gen = page["next_page"]
```

### Asynchronous

```python
import asyncio
from keka_sdk import AsyncKekaClient, KekaAuth

async def main():
    auth = KekaAuth(
        client_id="your-client-id",
        client_secret="your-client-secret",
        api_key="your-api-key",
    )
    async with AsyncKekaClient(auth, "https://your-company.keka.com") as client:
        result = await client.hr.search_employee(work_phone="+15551234567")
        print(result)

asyncio.run(main())
```

### Advanced configuration

Pass a `KekaConfig` instead of a bare URL to tune timeouts and retries:

```python
from keka_sdk import KekaClient, KekaConfig, KekaAuth

config = KekaConfig(
    instance_url="https://your-company.keka.com",
    timeout=30.0,
    max_retries=3,
    retry_delay=1.0,
    backoff_factor=2.0,
    max_backoff=30.0,
    jitter=0.5,
)
client = KekaClient(KekaAuth(client_id="...", client_secret="...", api_key="..."), config)
```

## Authentication

`KekaAuth` holds your credentials. The client builds an `AuthManager` that exchanges them for a
bearer token at the tenant's OAuth token endpoint (derived from `instance_url`, e.g.
`https://login.keka.com/connect/token`), using the `client_credentials` grant and the API key in
the `X-API-Key` header. Tokens are acquired lazily and refreshed automatically when expired.

## Error Handling

```python
from keka_sdk import KekaError, KekaAuthError, KekaRateLimitError, KekaNotFoundError

try:
    client.hr.get_employee("emp_123")
except KekaNotFoundError:
    print("Employee not found")
except KekaRateLimitError as e:
    print(f"Rate limited; retry after {e.retry_after}s")
except KekaAuthError as e:
    print(f"Auth failed: {e}")
except KekaError as e:
    print(f"Keka request failed: {e}")
```

## Public API

| Symbol | Description |
| --- | --- |
| `KekaClient` / `AsyncKekaClient` | Client facades (context managers) exposing `.hr` and `.helpdesk` |
| `KekaAuth` | API credentials |
| `KekaConfig` | Instance URL, timeouts, retry policy |
| `KekaError` (+ subclasses) | Typed error hierarchy |

> Note: methods whose Keka API payload contract is not yet verified (e.g. employee/ticket
> creation) raise `NotImplementedError`. This SDK is `0.x`; the public surface may change.

## Development

```bash
pip install -e .[dev]
pre-commit install
pytest
mypy keka_sdk
flake8 keka_sdk
```

## Dependencies

- `httpx>=0.24.0`

## License

MIT — see [LICENSE](LICENSE).
