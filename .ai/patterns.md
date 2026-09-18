# Design Principles & Patterns

This document defines the Object-Oriented Design Principles and Low-Level Design (LLD) Patterns applied in the Keka SDK codebase. All future contributions and refactors **must** strictly adhere to these principles and patterns.

---

## 1. Core Design Principles

### Single Responsibility Principle (SRP)
Each module and class has one well-defined responsibility:
- **`transport.py`**: Handles HTTP I/O, status code checking, and connection retries.
- **`auth.py`**: Manages OAuth credential state, token acquisition, and auto-refresh.
- **`config.py`**: Holds runtime client configuration and derives target login URLs.
- **`exceptions.py`**: Defines the typed error hierarchy.
- **`pagination.py`**: Handles cursor creation and page-by-page lazy iteration.
- **`resources/*.py`**: Encapsulates specific domain API operations (HR, Helpdesk, Leave, Attendance, HRIS).

### Open/Closed Principle (OCP)
The SDK is **open for extension, but closed for modification**:
- New domain resources (e.g., `leave.py`, `attendance.py`) are added by subclassing `BaseResource` / `AsyncBaseResource` and attaching them to `KekaClient`.
- Adding new endpoints does not require modifying core transport, retry, or auth code.

### Liskov Substitution Principle (LSP)
Subclasses and mirrored components can be substituted without breaking caller expectations:
- `AsyncTransport` can be substituted for `Transport` in async execution flows.
- `AsyncBaseResource` mirrors `BaseResource` with identical parameter structures and return models.

### Interface Segregation Principle (ISP)
Consumers are not forced to depend on methods they do not use:
- Rather than a giant monolithic client class with hundreds of methods, `KekaClient` segregates API endpoints into focused domain sub-clients (`client.hr`, `client.helpdesk`, `client.leave`, `client.attendance`, `client.groups`, etc.).

### Dependency Inversion Principle (DIP)
High-level resource modules do not instantiate low-level HTTP clients:
- `BaseResource` depends on abstractions (`Transport` and `AuthManager` passed via constructor).
- `KekaClient` wires dependencies together at initialization.

### Composition Over Inheritance
Classes favor HAS-A relationships over IS-A relationships:
- Resources **have-a** transport injected into them; they do **not** inherit from `httpx.Client` or `ApiClient`.
- Transport primitives (`get`, `post`, `put`, `delete`) remain private helpers and are never exposed directly on resource interfaces.

### Don't Repeat Yourself (DRY)
Duplication is eliminated through shared base classes and module-level helper functions:
- Non-I/O retry logic lives in `_RetryCore`.
- Non-I/O token caching and validation lives in `_TokenState`.
- Uniform error mapping is handled globally by `raise_for_keka_status()`.

---

## 2. Low-Level Design Patterns

### Creational Patterns

#### 1. Dependency Injection (Constructor Injection)
Dependencies are passed into constructors rather than instantiated internally.

- **Where**: `client.py` → `AuthManager`, `Transport`, resource classes.
- **How**:
  ```python
  # KekaClient.__init__
  self.transport = Transport(self.config)
  self.auth = AuthManager(self._auth_credentials, self.config, self.transport)
  self.hr = HRResource(self.transport, self.config, self.auth)
  ```
- **Benefit**: Ensures a single HTTP connection pool and token cache shared across all resources.

#### 2. Builder Pattern (Request Payload Builders)
Complex API request dictionaries and query parameter maps are constructed step-by-step using dedicated builder functions.

- **Where**: Every resource module (`hr.py`, `helpdesk.py`, `leave.py`, `attendance.py`, `hris.py`).
- **How**:
  ```python
  def _build_search_body(work_email: Optional[str], work_phone: Optional[str]) -> Dict[str, str]:
      if not work_email and not work_phone:
          raise ValueError("At least one of work_email or work_phone must be provided")
      body: Dict[str, str] = {}
      if work_email:
          body["workEmail"] = work_email
      if work_phone:
          body["workPhone"] = work_phone
      return body
  ```
- **Benefit**: Keeps public resource methods clean, handles parameter validation, maps `snake_case` kwargs to API `camelCase` keys, and filters out `None` values.

---

### Structural Patterns

#### 3. Facade Pattern
`KekaClient` and `AsyncKekaClient` provide a unified, simple entry point hiding complex subsystem initialization.

- **Where**: `client.py`.
- **How**: Consumers instantiate `KekaClient(auth, config)` and access domain operations via clean properties (`client.hr.search_employee()`, `client.helpdesk.list_tickets()`), without managing connections or token refreshes manually.

#### 4. Adapter / Wrapper Pattern
SDK resource methods adapt generic HTTP responses into strongly-typed `TypedDict` objects and custom exception hierarchies.

- **Where**: `resources/base.py`, `transport.py`.
- **How**: `raise_for_keka_status()` adapts raw `httpx.Response` status codes into domain-specific exceptions (`KekaRateLimitError`, `KekaNotFoundError`, `KekaAPIError`).

---

### Behavioral Patterns

#### 5. Template Method Pattern
Defines the skeletal algorithm for HTTP execution and retries in a base class, delegating specific I/O steps to subclasses.

- **Where**: `transport.py` → `_RetryCore` (base) extended by `Transport` (sync) and `AsyncTransport` (async).
- **How**:
  ```python
  class _RetryCore:
      def _should_retry(self, response, exception) -> bool: ...
      def _compute_delay(self, attempt, retry_after) -> float: ...

  class Transport(_RetryCore):
      def request(self, method, endpoint, ...):
          for attempt in range(self._config.max_retries + 1):
              # Execute request, check _should_retry(), time.sleep(_compute_delay())
  ```

#### 6. Iterator / Cursor Pattern
Provides a way to access elements of a paginated collection sequentially without exposing the underlying HTTP pagination structure.

- **Where**: `utils/pagination.py` (`PaginatedCursor`, `AsyncPaginatedCursor`).
- **How**: `PaginatedCursor.execute()` returns a formatted dictionary containing a lazy `Generator` (`next_page`) that yields subsequent pages on demand.
  ```python
  page = client.hr.list_employees(status="active")
  gen = page["next_page"]
  while gen is not None:
      page = next(gen)
      gen = page["next_page"]
  ```

---

## 3. Implementation & Idiomatic Python Patterns

### Sync/Async Mirror Pattern
Every component has synchronous and asynchronous variants sharing identical logic with only I/O differing.
- **Where**: `Transport` / `AsyncTransport`, `AuthManager` / `AsyncAuthManager`, `BaseResource` / `AsyncBaseResource`.
- **Convention**: Async classes are prefixed with `Async` (e.g., `HRResource` → `AsyncHRResource`).

### Context Manager Lifecycle Pattern
Clients and transports implement `__enter__`/`__exit__` and `__aenter__`/`__aexit__` to guarantee connection pool cleanup.
- **Where**: `client.py`, `transport.py`.

### Dataclass Configuration Pattern
Configuration and credentials are modeled as immutable-by-default `@dataclass` objects with defaults and post-init validation.
- **Where**: `config.py` (`KekaConfig`), `auth.py` (`KekaAuth`).

### Config Coercion Pattern
Client constructors accept either a fully-formed `KekaConfig` instance or a plain URL string.
- **Where**: `client.py` → `_coerce_config()`.

### Parameter Sanitisation (None Filtering) Pattern
All payload/parameter builder functions sanitize input dictionaries by stripping `None` values before dispatching network requests.
- **Where**: Every `_build_*` helper function in `resources/`.
