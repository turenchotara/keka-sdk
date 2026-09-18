# Architectural Decisions

Decisions inferred from the codebase with supporting evidence.

---

## ADR-1: Composition Over Inheritance for Resources

**Decision**: Resources receive transport, config, and auth via constructor injection rather than subclassing an HTTP client.

**Reason**: The previous implementation (`Employee(ApiClient)`, `TicketManagement(ApiClient)`) tightly coupled domain logic to HTTP transport. This made it impossible to share a connection pool or swap transport implementations.

**Tradeoffs**:
- (+) Single connection pool across all resources.
- (+) Resources are testable with mock transports.
- (+) Clear separation of concerns.
- (−) Every resource constructor has 3 parameters (`transport`, `config`, `auth`).

**Impact**: Fundamental to the SDK's architecture. All resources follow this pattern. Documented in `CHANGELOG.md` as the v0.1.0 consolidation.

**Evidence**: `BaseResource.__init__(self, transport, config, auth)` in `keka/resources/base.py`; `KekaClient.__init__` wiring in `keka/client.py`.

---

## ADR-2: Single Transport / Connection Pool

**Decision**: One `httpx.Client` (or `httpx.AsyncClient`) is created by `KekaClient` and injected into every resource and the auth manager.

**Reason**: Multiple HTTP clients cause connection pool proliferation and make it harder to enforce rate limiting, retries, and header management consistently.

**Tradeoffs**:
- (+) Efficient connection reuse.
- (+) Consistent retry and timeout behaviour.
- (+) Headers (like `Authorization`) set once apply everywhere.
- (−) Resources cannot have independent timeout configurations.

**Impact**: The transport is the shared backbone. All HTTP flows through it.

**Evidence**: `client.hr._transport is client.transport` assertion in `tests/test_client.py`.

---

## ADR-3: Token URL Derived from Instance URL

**Decision**: The OAuth token endpoint is derived by replacing the tenant subdomain with `login.<base_domain>` (e.g. `acme.keka.com` → `login.keka.com/connect/token`), rather than hardcoding `kekademo.com`.

**Reason**: The previous implementation hardcoded `kekademo.com` as the login host, making it unusable for production tenants or on-prem deployments.

**Tradeoffs**:
- (+) Works with any Keka tenant automatically.
- (+) Supports on-prem overrides via `login_url` parameter.
- (−) Assumes Keka's URL convention (`login.<domain>/connect/token`).

**Impact**: Eliminates a class of deployment bugs. The `login_url` escape hatch makes it future-proof.

**Evidence**: `derive_login_url()` in `keka/config.py`; test in `tests/test_config.py`.

---

## ADR-4: Typed Error Hierarchy

**Decision**: All SDK errors are subclasses of `KekaError`. HTTP errors are mapped to specific types (`KekaAuthError`, `KekaAPIError`, `KekaRateLimitError`, `KekaNotFoundError`).

**Reason**: The previous design returned `None` on failure or raised generic exceptions, making error handling unreliable.

**Tradeoffs**:
- (+) Consumers can catch specific error types (`except KekaNotFoundError`).
- (+) `KekaRateLimitError` carries `retry_after` for programmatic backoff.
- (+) `KekaAPIError` carries `status_code` and `body` for debugging.
- (−) Adds a layer of exception abstraction over httpx's native errors.

**Impact**: All transport errors flow through `raise_for_keka_status()`.

**Evidence**: `keka/exceptions.py`, `transport.py:raise_for_keka_status()`.

---

## ADR-5: Lazy Pagination via Generators

**Decision**: Paginated endpoints return a dict with `next_page` set to either a `Generator` or `None`, rather than eagerly fetching all pages.

**Reason**: Eager fetching buffers potentially large datasets in memory. Generator-based pagination is lazy and memory-efficient.

**Tradeoffs**:
- (+) Memory efficient — only one page in memory at a time.
- (+) Consumer controls iteration pace.
- (+) Preserves original query parameters across pages.
- (−) Slightly unusual API — consumers must check `next_page is not None` and call `next()`.
- (−) The generator holds a reference to the transport, which must remain open.

**Impact**: All `list_*` methods across every resource use this pattern.

**Evidence**: `PaginatedCursor` in `keka/utils/pagination.py`; `BaseResource._paginate()` in `keka/resources/base.py`.

---

## ADR-6: Sync + Async Dual API

**Decision**: The SDK provides both synchronous and asynchronous clients with identical APIs.

**Reason**: Python consumers span web frameworks (async — FastAPI, aiohttp) and scripts (sync). Supporting both avoids forcing consumers into one paradigm.

**Tradeoffs**:
- (+) Broadest consumer compatibility.
- (+) Shared non-I/O logic via base classes (`_RetryCore`, `_TokenState`).
- (−) Near-duplicate code in every resource (sync + async classes).
- (−) Maintenance burden — changes must be applied in two places.

**Impact**: Every resource file contains paired sync/async classes. `client.py` provides `KekaClient` and `AsyncKekaClient`.

**Evidence**: `HRResource` + `AsyncHRResource` in every resource file; `Transport` + `AsyncTransport` in `transport.py`.

---

## ADR-7: httpx as the HTTP Backend

**Decision**: Use `httpx` as the sole HTTP library instead of `requests`.

**Reason**: `httpx` natively supports both sync and async operations with the same API, eliminating the need for separate `requests` (sync) and `aiohttp` (async) dependencies.

**Tradeoffs**:
- (+) One library for sync + async.
- (+) Familiar `requests`-like API.
- (+) Connection pooling built-in.
- (−) Smaller ecosystem than `requests` (though mature enough for production).

**Impact**: The `requests` dependency was removed in v0.1.0.

**Evidence**: `pyproject.toml` lists `httpx>=0.24.0` as the sole runtime dependency; `CHANGELOG.md` notes removal of `requests`.

---

## ADR-8: pyproject.toml as Sole Packaging Config

**Decision**: Use `pyproject.toml` with setuptools backend and dynamic version. `setup.py` and `setup.cfg` are retained as legacy but slated for removal.

**Reason**: Modern Python packaging standards (PEP 621, PEP 517) encourage `pyproject.toml` as the single source of truth.

**Tradeoffs**:
- (+) Single file for all project metadata, dependencies, and tool config.
- (+) Dynamic version sourced from `keka/_version.py`.
- (−) Legacy `setup.py`/`setup.cfg` still exist (confusing for contributors).

**Impact**: `pyproject.toml` is the authoritative config. `setup.py` and `setup.cfg` should eventually be deleted.

**Evidence**: Version defined in `keka/_version.py`, referenced by `[tool.setuptools.dynamic]` in `pyproject.toml`.

---

## ADR-9: Backward-Compatible keka_sdk Shim

**Decision**: Maintain a `keka_sdk` package that re-exports everything from `keka` via `from keka import *`.

**Reason**: The original package was published as `keka_sdk`. Renaming to `keka` internally while keeping `keka_sdk` importable avoids breaking existing consumers.

**Tradeoffs**:
- (+) Zero breaking changes for existing users.
- (+) Both `from keka import KekaClient` and `from keka_sdk import KekaClient` work.
- (−) Two packages in the repo is confusing.
- (−) Tests import from `keka_sdk`, not `keka`.

**Impact**: The `keka_sdk/` directory must be maintained until a major version bump.

**Evidence**: `keka_sdk/__init__.py` contains `from keka import *`; `pyproject.toml` includes `keka*` in package discovery.

---

## ADR-10: Expiry Skew for Token Safety

**Decision**: Tokens are considered expired 30 seconds before their actual `expires_in` deadline.

**Reason**: Prevents edge-of-expiry races where a request is sent with a token that expires mid-flight.

**Tradeoffs**:
- (+) Robust against clock drift and network latency.
- (−) Slightly more token refreshes than strictly necessary.

**Impact**: Implemented in `_TokenState.is_token_valid` in `auth.py`.

**Evidence**: `_EXPIRY_SKEW_SECONDS = 30.0` in `keka/auth.py`.

---

## ADR-11: camelCase in Request Bodies, snake_case in SDK

**Decision**: SDK methods accept snake_case parameters and internally convert to camelCase for the Keka API.

**Reason**: The Keka REST API uses camelCase in JSON payloads, but Pythonic convention is snake_case. The builder functions handle the mapping.

**Tradeoffs**:
- (+) Natural Python API for consumers.
- (+) Mapping logic isolated in `_build_*` functions.
- (−) Every parameter must be mapped manually (no auto-conversion).

**Impact**: All resource method signatures use snake_case; all `_build_*` functions produce camelCase dicts.

**Evidence**: `_build_employee_list_params()` in `hr.py` maps `employee_ids` → `"employeeIds"`.
