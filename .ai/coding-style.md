# Coding Style

Conventions actually observed in this codebase.

## Naming Conventions

| Element | Convention | Example |
|---|---|---|
| Package / module | lowercase, underscores | `keka_sdk`, `transport.py` |
| Class | PascalCase | `KekaClient`, `HRResource`, `AsyncAuthManager` |
| Function / method | snake_case | `search_employee`, `ensure_token`, `_build_url` |
| Private method | leading underscore | `_authorize`, `_get`, `_build_path` |
| Module-level private | leading underscore | `_SEARCH_PATH`, `_EXPIRY_SKEW_SECONDS` |
| Constants | UPPER_SNAKE_CASE | `DEFAULT_RETRY_STATUS_CODES`, `TOKEN_PATH` |
| Type alias | PascalCase | `GenderType`, `TicketStatusEnum`, `AnyAuthManager` |
| Parameter | snake_case | `instance_url`, `page_size`, `work_email` |
| API field mapping | camelCase in dicts | `{"employeeId": ...}`, `{"pageNumber": ...}` |

### Async Naming Pattern

Async counterparts are prefixed with `Async`:
- `KekaClient` → `AsyncKekaClient`
- `AuthManager` → `AsyncAuthManager`
- `Transport` → `AsyncTransport`
- `HRResource` → `AsyncHRResource`

## Folder Organisation

```
keka/
├── Core modules (auth, client, config, exceptions, transport) at package root
├── resources/     → one file per domain (hr.py, helpdesk.py, etc.)
├── types/         → single __init__.py with all TypedDicts
└── utils/         → helpers (pagination.py)
```

- No nested sub-packages beyond one level.
- Each resource file contains both sync and async classes.
- Tests in `tests/` mirror module names: `test_auth.py`, `test_client.py`, etc.

## File Organisation

Each resource file follows this order:
1. Imports (stdlib → third-party → local).
2. Module-level constants (endpoint paths like `_SEARCH_PATH`).
3. Module-level builder functions (`_build_*_body`, `_build_*_params`).
4. Sync resource class (subclasses `BaseResource`).
5. Async resource class (subclasses `AsyncBaseResource`).

## Error Handling

- **Typed exception hierarchy**: All errors subclass `KekaError`. Never return `None` for failures.
- **Transport layer** maps HTTP status codes to typed exceptions via `raise_for_keka_status()`.
- **Auth errors** raise `KekaAuthError` with descriptive messages including status code and error description from the response body.
- **No bare `except`**: Catch specific `httpx` exceptions (`ConnectError`, `TimeoutException`, `HTTPError`).
- **No double-wrapping**: Exceptions use `raise ... from exception` for clean chaining.
- **Validation errors**: `ValueError` for invalid input (e.g. no search criteria), `TypeError` for wrong argument types.

## Logging

- Uses standard library `logging` with module-level loggers: `logger = logging.getLogger(__name__)`.
- Log levels used:
  - `logger.info` — token acquisition success.
  - `logger.warning` — retry attempts, pagination request failures.
  - `logger.error` — response parsing failures, page fetch errors.
- No print statements anywhere in the SDK.

## Validation

- Input validation at the resource level using module-level builder functions.
- `_validate_auth()` in `client.py` checks `isinstance(auth, KekaAuth)`.
- `_coerce_config()` accepts `str | KekaConfig`, converting strings to `KekaConfig`.
- `KekaConfig.__post_init__` validates `instance_url` is non-empty and strips trailing slashes.
- Builder functions raise `ValueError` when mandatory fields are missing.

## Testing

- **Framework**: `pytest` with `pytest-asyncio` (auto mode).
- **HTTP Mocking**: `respx` for httpx request interception — no real network calls.
- **Test markers**: `slow`, `integration`, `unit` (defined in `pyproject.toml`).
- **Pattern**: Factory functions for config and auth (`_config()`, `_auth()`, `_mock_token()`).
- **Resource cleanup**: Tests use `try/finally` to close transports, or context managers.
- **Async tests**: Decorated with `@respx.mock` and `async def test_*`.
- **Assertions**: Direct `assert` statements, `pytest.raises` for exception testing.

## Dependency Rules

- **Single runtime dependency**: `httpx`. No other third-party imports in production code.
- **No cross-resource imports** (except `helpdesk.py` reusing `_build_search_body` from `hr.py`).
- **Resources never import `httpx` directly** — all HTTP goes through the transport layer.
- **Types are import-only** — the `types/` module has zero runtime dependencies.

## Type Annotations

- All public methods have full type annotations (enforced by `mypy --strict`-like config).
- `TypedDict` with `total=False` for optional API fields.
- `Literal` types for integer enums (e.g. `GenderType = Literal[0, 1, 2, 3]`).
- `Union[str, KekaConfig]` for flexible config parameter.
- `py.typed` marker shipped for PEP 561 compliance.

## Formatting

- **Black**: line length 88, target Python 3.8–3.12.
- **isort**: profile `black`, `multi_line_output = 3`.
- Pre-commit hooks enforce formatting on commit.

## Security Practices

- No credentials hardcoded anywhere in the SDK.
- Token endpoint URL is derived from `instance_url`, not hardcoded to a demo host.
- Tokens are stored in-memory only (no disk persistence).
- Expiry skew (`_EXPIRY_SKEW_SECONDS = 30`) prevents edge-of-expiry authentication races.

## Performance Guidelines

- Single connection pool shared across all resources (no per-resource pool).
- Lazy pagination — pages are fetched on-demand via generators, not buffered.
- Token caching via `ensure_token()` — avoids redundant auth requests.
- Retry with jitter prevents thundering herd on rate limits.
