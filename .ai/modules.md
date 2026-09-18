# Modules

## Client (`keka/client.py`)

**Purpose**: Top-level facade that wires the entire SDK together.

**Responsibilities**:
- Accept `KekaAuth` credentials and `KekaConfig` (or a plain URL string).
- Create and own the single `Transport` / `AsyncTransport` instance.
- Create the `AuthManager` and inject the shared transport into it.
- Instantiate all resource classes with the shared transport, config, and auth.
- Implement context-manager protocol (`__enter__` / `__exit__`) for transport lifecycle.
- Expose `authenticate()` for eager token acquisition.

**Public Interface**:
- `KekaClient(auth, config)` — sync client.
- `AsyncKekaClient(auth, config)` — async client.
- Properties: `.hr`, `.helpdesk`, `.leave`, `.attendance`, `.groups`, `.departments`, `.locations`, `.job_titles`, `.currencies`, `.notice_periods`, `.exit_reasons`, `.instance_url`.

**Dependencies**: `auth`, `config`, `transport`, all resource modules.

**Entry Point**: Consumer creates a `KekaClient` — everything else is constructed internally.

---

## Auth (`keka/auth.py`)

**Purpose**: OAuth2 token lifecycle management.

**Responsibilities**:
- `KekaAuth` — credentials dataclass holding `client_id`, `client_secret`, `api_key`, `scope`, `grant_type`.
- `_TokenState` — transport-agnostic token storage, expiry tracking, auth header generation.
- `AuthManager` / `AsyncAuthManager` — token acquisition via `POST` to the token endpoint, caching, refresh, expiry-skew (30s early).

**Public Interface**:
- `KekaAuth.token_request_data()` — form body dict.
- `KekaAuth.token_request_headers()` — request headers dict.
- `AuthManager.authenticate()` → `str` — force-acquire a token.
- `AuthManager.ensure_token()` → `str` — return cached or acquire.
- `AuthManager.refresh()` → `str` — clear + re-acquire.
- `AuthManager.is_token_valid` — bool property.
- `AuthManager.auth_header()` → `Dict[str, str]`.

**Dependencies**: `config` (for token URL), `transport` (for HTTP POST), `exceptions` (for `KekaAuthError`).

---

## Config (`keka/config.py`)

**Purpose**: Centralised configuration for the SDK.

**Responsibilities**:
- `KekaConfig` dataclass with fields: `instance_url`, `login_url`, `timeout`, `max_retries`, `retry_delay`, `backoff_factor`, `max_backoff`, `jitter`, `retry_status_codes`.
- `derive_login_url()` — compute OAuth token endpoint from `instance_url` by replacing the subdomain with `login.<base_domain>`.
- `token_url` property — resolved endpoint used by `AuthManager`.

**Public Interface**:
- `KekaConfig(instance_url="https://acme.keka.com", ...)`
- `config.token_url` → `str`

**Dependencies**: Standard library only (`urllib.parse`, `dataclasses`).

---

## Transport (`keka/transport.py`)

**Purpose**: HTTP transport layer with retry logic and error mapping.

**Responsibilities**:
- `_RetryCore` — shared retry/backoff/jitter logic, URL building (`_build_url`).
- `Transport` — sync HTTP client wrapping `httpx.Client`. Methods: `get`, `post`, `put`, `patch`, `delete`, `request`. Retry loop with `time.sleep`.
- `AsyncTransport` — async mirror wrapping `httpx.AsyncClient` with `asyncio.sleep`.
- `raise_for_keka_status()` — module-level function mapping non-2xx responses to typed exceptions.
- `_parse_retry_after()` — extract `Retry-After` header value.

**Public Interface**:
- `Transport(config, headers=None)` — sync.
- `AsyncTransport(config, headers=None)` — async.
- `.set_header(key, value)` — applies to all subsequent requests.
- `.close()` / `await .close()`.
- Context manager protocol.

**Dependencies**: `httpx`, `config`, `exceptions`.

---

## Exceptions (`keka/exceptions.py`)

**Purpose**: Typed error hierarchy for all SDK-raised errors.

**Responsibilities**:
- `KekaError` — base class.
- `KekaAuthError` — authentication failures.
- `KekaAPIError` — non-2xx API responses (`status_code`, `body`).
- `KekaRateLimitError` — HTTP 429 with `retry_after` attribute.
- `KekaNotFoundError` — HTTP 404.

**Public Interface**: All 5 exception classes are exported from `keka.__init__`.

**Dependencies**: None (standard library only).

---

## Resources — Base (`keka/resources/base.py`)

**Purpose**: Abstract base for all API resources.

**Responsibilities**:
- `BaseResource` / `AsyncBaseResource` — constructor accepts `(transport, config, auth)`.
- `_authorize()` — call `auth.ensure_token()` and set the `Authorization` header on the transport.
- `_get()`, `_post()`, `_put()` — authorized request helpers that return `Dict[str, Any]`.
- `_paginate()` — delegates to `PaginatedCursor.execute()`.
- `_build_path()` — join endpoint segments.

**Extension Point**: Subclass and set `endpoint` class attribute; use `_get/_post/_put/_paginate`.

---

## Resources — HR (`keka/resources/hr.py`)

**Purpose**: Employee management operations.

**Responsibilities**:
- `HRResource` / `AsyncHRResource` — endpoint `hris/employees`.
- CRUD: `list_employees`, `search_employee`, `get_employee`, `create_employee`.
- Updates: `update_job_details`, `update_personal_details`.
- Exit: `deactivate_employee`, `update_exit_request`.
- Module-level builder functions: `_build_search_body`, `_build_employee_list_params`, `_build_create_employee_body`, etc.

**Dependencies**: `base`, `types` (for enum literals and `EmployeeSearchResponse`).

---

## Resources — Helpdesk (`keka/resources/helpdesk.py`)

**Purpose**: Helpdesk ticket management.

**Responsibilities**:
- `HelpdeskResource` / `AsyncHelpdeskResource` — endpoint `helpdesk/tickets`.
- CRUD: `list_tickets`, `get_ticket`, `create_ticket`, `update_ticket`.
- Employee search: `search_employee_for_ticket` (reuses HR search path).
- Metadata: `list_categories`, `list_closing_reasons`.

**Dependencies**: `base`, `types`, `hr._build_search_body`.

---

## Resources — HRIS Lookups (`keka/resources/hris.py`)

**Purpose**: Organisational lookup data.

**Responsibilities**:
- 7 resource class pairs (sync + async): `GroupsResource`, `DepartmentsResource`, `LocationsResource`, `JobTitlesResource`, `CurrencyResource`, `NoticePeriodResource`, `ExitReasonsResource`.
- Each provides a single `list_*` method (paginated except `ExitReasonsResource` which uses `_get`).
- `GroupsResource` additionally provides `list_group_types`.

**Dependencies**: `base`.

---

## Resources — Leave (`keka/resources/leave.py`)

**Purpose**: Leave management operations.

**Responsibilities**:
- `LeaveResource` / `AsyncLeaveResource` — endpoint `time`.
- Operations: `list_balances`, `list_plans`, `list_requests`, `create_request`, `list_types`.

**Dependencies**: `base`, `types` (for `SessionType`).

---

## Resources — Attendance (`keka/resources/attendance.py`)

**Purpose**: Attendance and time tracking operations.

**Responsibilities**:
- `AttendanceResource` / `AsyncAttendanceResource` — endpoint `time`.
- Listing: `list_records`, `list_capture_schemes`, `list_shift_policies`, `list_tracking_policies`, `list_weekly_off_policies`, `list_holiday_calendars`, `list_holidays`.
- Creation: `create_time_entry`, `create_time_entry_for_employee`, `create_on_duty_request`, `create_wfh_request`.
- On-Duty/WFH: `list_on_duty_requests`, `list_wfh_requests`, `update_approval_status`.

**Dependencies**: `base`, `types` (for `ApprovalStatusEnum`, `SessionType`).

---

## Types (`keka/types/__init__.py`)

**Purpose**: Shared type definitions for all API entities.

**Responsibilities**:
- Literal type aliases for enums (`GenderType`, `MaritalStatusType`, `TicketStatusEnum`, `TicketPriorityEnum`, `SessionType`, `ApprovalStatusEnum`, etc.).
- `TypedDict` definitions for API entities: `EmployeeProfile`, `Department`, `Location`, `Group`, `Ticket`, `LeaveRequest`, `AttendanceRecord`, etc.
- Request body types: `EmployeeCreateRequest`, `TicketCreateRequest`, etc.
- Response envelope types: `BaseKekaResponse`, `EmployeeSearchResponse`, `PaginatedResponse`, etc.
- Nested structures: `Address`, `Education`, `Experience`, `Relation`, `CustomField`, etc.

**Extension Point**: Add new `TypedDict` definitions here when wrapping additional Keka API endpoints.

---

## Utils — Pagination (`keka/utils/pagination.py`)

**Purpose**: Cursor-based lazy pagination.

**Responsibilities**:
- `PaginatedCursor` — sync. Class method `execute()` makes the initial request, returns a dict with `{succeeded, message, errors, data, next_page}` where `next_page` is a `Generator` or `None`.
- `AsyncPaginatedCursor` — async mirror returning an `AsyncGenerator`.
- Preserves all original query parameters across pages, overriding only `pageNumber`.
- Allows `totalPages` to update dynamically from each response.

**Dependencies**: `httpx` (for response typing), standard library `logging`.

---

## Compatibility Shim (`keka_sdk/`)

**Purpose**: Backward-compatible import path.

**Responsibilities**:
- `keka_sdk/__init__.py` contains `from keka import *` — all public symbols are available under both `keka` and `keka_sdk`.
- Stub sub-packages (`resources/`, `types/`, `utils/`) exist as empty re-export points.

**Note**: The `keka_sdk` package is the one discovered by `setuptools` (via `include = ["keka*"]` in `pyproject.toml`). The canonical code lives in `keka/`.
