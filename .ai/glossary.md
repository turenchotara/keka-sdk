# Glossary

## Business Terminology

| Term | Definition |
|---|---|
| **Tenant** | A company's Keka instance (e.g. `acme.keka.com`). Each tenant is isolated. |
| **Employee** | A person in the HRIS system. Identified by a UUID (`id`) and a human-readable `employeeNumber`. |
| **HRIS** | Human Resource Information System — the core module for employee data. |
| **Helpdesk** | Internal IT/HR support ticketing system within Keka. |
| **Ticket** | A helpdesk support request raised by or on behalf of an employee. |
| **Department** | Organisational unit an employee belongs to. |
| **Business Unit** | Top-level organisational division (e.g. "Engineering", "Sales"). |
| **Legal Entity** | The legal company entity the employee is employed under. |
| **Job Title** | The employee's role designation. |
| **Location** | Physical office location. |
| **Group** | A named organisational grouping (can be system-defined like Department, or custom). |
| **Group Type** | Category of group (BusinessUnit, Department, OrgLocation, CostCenter, etc.). |
| **Leave** | Employee time-off. Managed via leave types, plans, balances, and requests. |
| **Leave Plan** | A policy defining which leave types an employee has access to. |
| **Leave Balance** | Current accrued/consumed/available leave counts per leave type per employee. |
| **Leave Request** | A formal request for time off — has a status lifecycle (Pending → Approved/Rejected/Cancelled). |
| **Leave Type** | Category of leave (e.g. Casual, Sick, Earned). |
| **Attendance** | Daily clock-in/clock-out records for employees. |
| **Capture Scheme** | Configuration defining how attendance is captured (biometric, web, mobile). |
| **Shift Policy** | Rules defining work shift timing. |
| **Tracking Policy** | Penalisation rules for attendance violations. |
| **Weekly Off Policy** | Rules defining which days of the week are off (e.g. Saturday-Sunday). |
| **Holiday Calendar** | A named calendar defining company holidays for a year. |
| **On-Duty (OD)** | A request marking an employee as working outside the office. |
| **WFH** | Work From Home request. |
| **Exit Request** | Formal initiation of employee separation (resignation, termination, etc.). |
| **Notice Period** | The time between resignation submission and last working date. |
| **Exit Reason** | The categorised reason for an employee's departure. |
| **CSAT** | Customer Satisfaction — a score/response on closed helpdesk tickets. |

## Technical Terminology

| Term | Definition |
|---|---|
| **Transport** | The HTTP client layer (`httpx.Client`) that handles connection pooling, retries, and error mapping. |
| **Resource** | A domain-specific class (e.g. `HRResource`) that maps SDK methods to Keka API endpoints. |
| **BaseResource** | Abstract base class providing `_get`, `_post`, `_put`, `_paginate`, `_authorize` helpers. |
| **AuthManager** | Component owning the token lifecycle — acquisition, caching, refresh, expiry tracking. |
| **KekaAuth** | Dataclass holding OAuth credentials (`client_id`, `client_secret`, `api_key`). |
| **KekaConfig** | Dataclass holding instance URL, timeouts, and retry policy. |
| **PaginatedCursor** | Lazy generator-based cursor that fetches pages on demand. |
| **`_RetryCore`** | Shared retry logic (backoff, jitter, status-code check) inherited by sync/async transports. |
| **`_TokenState`** | Shared token storage and expiry logic inherited by sync/async auth managers. |
| **`raise_for_keka_status()`** | Function that maps HTTP status codes to the `KekaError` exception hierarchy. |
| **respx** | HTTP mocking library for `httpx` used in tests. |
| **`py.typed`** | PEP 561 marker file indicating the package ships type information. |

## Internal Names

| Name | Meaning |
|---|---|
| `keka` | The canonical Python package (import as `from keka import KekaClient`). |
| `keka_sdk` | Backward-compatible re-export shim. `from keka_sdk import *` works identically. |
| `_EXPIRY_SKEW_SECONDS` | 30-second buffer before actual token expiry to prevent race conditions. |
| `_SEARCH_PATH` | Constant for the employee search endpoint path (`hris/employees/search`). |
| `_coerce_config()` | Helper that accepts `str | KekaConfig` and normalises to `KekaConfig`. |
| `_validate_auth()` | Helper that type-checks the `auth` parameter is a `KekaAuth` instance. |
| `next_page` | Key in paginated response dict — contains a `Generator` for the next page or `None`. |

## Acronyms

| Acronym | Expansion |
|---|---|
| **SDK** | Software Development Kit |
| **HRIS** | Human Resource Information System |
| **HR** | Human Resources |
| **API** | Application Programming Interface |
| **REST** | Representational State Transfer |
| **OAuth** | Open Authorization |
| **OD** | On-Duty |
| **WFH** | Work From Home |
| **CSAT** | Customer Satisfaction (Score) |
| **PEP** | Python Enhancement Proposal |
| **UUID** | Universally Unique Identifier |

## Status Values / Enums

| Enum | Values |
|---|---|
| `GenderType` | 0=Male, 1=Female, 2=Other, 3=Not specified |
| `MaritalStatusType` | 0=Single, 1=Married, 2=Divorced |
| `EmploymentStatusEnum` | 0=Inactive, 1=Active |
| `AccountStatusEnum` | 0=Inactive, 1=Active, 2=Suspended |
| `ExitTypeEnum` | 0=Resignation, 1=Termination, 2=Retirement, 3=Other |
| `ExitStatusEnum` | 0=Active, 1=Notice Period, 2=Exited |
| `TicketStatusEnum` | 0=Open, 1=Pending, 2=Resolved, 3=Closed, 4=InProgress, 5=OnHold |
| `TicketPriorityEnum` | 0=Low, 1=Medium, 2=High, 3=Critical |
| `LeaveRequestStatusEnum` | 0=Pending, 1=Approved, 2=Rejected, 3=Cancelled, 4=InApprovalProcess |
| `SessionType` | 0=FirstHalf, 1=SecondHalf |
| `ApprovalStatusEnum` | 0=Pending, 1=Approved, 2=Rejected, 3=Cancelled |
| `SystemGroupTypeEnum` | 0=None, 1=BusinessUnit, 2=Department, 3=OrgLocation, 4=CostCenter, 5=Paygroup, 6=ProjectTeam, 7=Team, 8=ClientTeam, 9=LegalEntity |
| `TimeTypeEnum` | 0=FullTime, 1=PartTime, 2=Contract |
| `WorkerTypeEnum` | 0=Employee, 1=Consultant, 2=Intern |

## Domain Concepts

| Concept | Description |
|---|---|
| **Instance URL** | The base URL of a Keka tenant (e.g. `https://acme.keka.com`). All API calls are relative to this. |
| **Login URL** | The OAuth token endpoint, derived as `https://login.<base_domain>/connect/token`. Can be overridden for on-prem deployments. |
| **Token Endpoint** | The OAuth2 `client_credentials` endpoint where the SDK exchanges credentials for a bearer token. |
| **Bearer Token** | The `access_token` returned by the token endpoint, sent as `Authorization: Bearer <token>` on every API request. |
| **Expiry Skew** | The SDK treats tokens as expired 30 seconds early to avoid authentication failures at the boundary. |
| **Retry-After** | HTTP header returned on 429 (rate limit) responses indicating how many seconds to wait before retrying. |
| **Page / Pagination** | Keka API returns paginated lists with `pageNumber`, `totalPages`, `pageSize`, `totalRecords`. Default page size is 100, max 200. |
