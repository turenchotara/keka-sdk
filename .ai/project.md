# Project Overview

## Purpose

Keka SDK is a composition-based Python SDK for the [Keka HR API](https://developers.keka.com/reference). It wraps the Keka REST API into a typed, ergonomic Python client with automatic authentication, pagination, retries, and a structured error hierarchy.

## Business Domain

**Human Resources (HR) / People Operations** — Keka is a cloud-based HR management platform used by companies for employee management, payroll, attendance tracking, leave management, and internal helpdesk ticketing. This SDK enables programmatic integration with Keka tenants.

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.8+ |
| HTTP Client | `httpx >= 0.24.0` (sync + async) |
| Type System | `TypedDict`, `Literal` types, `py.typed` marker |
| Packaging | `pyproject.toml` (setuptools backend, dynamic version) |
| Testing | `pytest`, `pytest-asyncio`, `respx` (httpx mocking) |
| Linting | `flake8`, `mypy` (strict mode), `black`, `isort` |
| CI | GitHub Actions (planned) |
| License | MIT |

## Runtime Dependencies

- `httpx >= 0.24.0` — the sole runtime dependency.

## Dev Dependencies

- `pytest >= 7.0.0`, `pytest-asyncio >= 0.21.0`, `pytest-cov >= 4.0.0`
- `respx >= 0.20.0` — httpx contract mocking
- `black >= 23.0.0`, `flake8 >= 6.0.0`, `mypy >= 1.0.0`
- `pre-commit >= 3.0.0`

## Folder Structure

```
keka-sdk/
├── keka/                        # ← active package (import name: keka / keka_sdk)
│   ├── __init__.py              # public exports
│   ├── _version.py              # __version__ = "0.1.0"
│   ├── auth.py                  # KekaAuth, AuthManager, AsyncAuthManager
│   ├── client.py                # KekaClient, AsyncKekaClient
│   ├── config.py                # KekaConfig, derive_login_url()
│   ├── exceptions.py            # KekaError hierarchy
│   ├── transport.py             # Transport, AsyncTransport, _RetryCore
│   ├── py.typed                 # PEP 561 marker
│   ├── resources/
│   │   ├── __init__.py          # re-exports all resources
│   │   ├── base.py              # BaseResource, AsyncBaseResource
│   │   ├── hr.py                # HRResource, AsyncHRResource
│   │   ├── helpdesk.py          # HelpdeskResource, AsyncHelpdeskResource
│   │   ├── hris.py              # Groups, Departments, Locations, etc.
│   │   ├── leave.py             # LeaveResource, AsyncLeaveResource
│   │   └── attendance.py        # AttendanceResource, AsyncAttendanceResource
│   ├── types/
│   │   └── __init__.py          # all TypedDicts and Literal enum types
│   └── utils/
│       ├── __init__.py
│       └── pagination.py        # PaginatedCursor, AsyncPaginatedCursor
├── keka_sdk/                    # ← compatibility shim (re-exports from keka)
│   ├── __init__.py              # `from keka import *`
│   ├── resources/
│   ├── types/
│   └── utils/
├── tests/
│   ├── test_auth.py
│   ├── test_client.py
│   ├── test_config.py
│   ├── test_transport.py
│   ├── test_pagination_generator.py
│   └── test_attendance.py
├── pyproject.toml               # authoritative packaging config
├── setup.py                     # legacy (slated for removal)
├── setup.cfg                    # legacy (slated for removal)
├── Makefile                     # dev workflow targets
├── AGENTS.md                    # AI agent instructions
├── CHANGELOG.md
├── INTEGRATED_MODULES.md
├── README.md
└── LICENSE
```

## Main Services / Domains

| Domain | Client Accessor | Source |
|---|---|---|
| Employee Management (HR) | `client.hr` | `keka/resources/hr.py` |
| Helpdesk Ticketing | `client.helpdesk` | `keka/resources/helpdesk.py` |
| Leave Management | `client.leave` | `keka/resources/leave.py` |
| Attendance & Time | `client.attendance` | `keka/resources/attendance.py` |
| HRIS Lookups | `client.groups`, `.departments`, `.locations`, `.job_titles`, `.currencies`, `.notice_periods`, `.exit_reasons` | `keka/resources/hris.py` |

## External Integrations

- **Keka REST API v1** — `https://<tenant>.keka.com/api/v1/...`
- **Keka OAuth Token Endpoint** — `https://login.keka.com/connect/token` (derived from `instance_url`)
- No database, no message queues, no third-party SaaS integrations.

## Environment Setup

```bash
# Clone
git clone https://github.com/turenchotara/keka-sdk.git
cd keka-sdk

# Install (editable with dev extras)
pip install -e .[dev]

# Pre-commit hooks
pre-commit install
```

No environment variables are required for the SDK itself. Consumers supply `client_id`, `client_secret`, `api_key`, and `instance_url` at runtime.

## Build Commands

```bash
make build          # clean + python -m build (sdist + wheel)
make publish        # build + twine upload dist/*
make clean          # remove build artifacts and __pycache__
```

## Development Commands

```bash
make install-dev    # pip install -e .[dev,docs]
make dev-setup      # install-dev + pre-commit install
make format         # black + isort
make check-format   # black --check + isort --check-only
```

## Test Commands

```bash
make test           # pytest tests/ -v
make lint           # flake8 + mypy
make type-check     # mypy keka_sdk/
make dev-check      # check-format + lint + type-check + test
```

## Current Version

`0.1.0` — Beta status. The public API surface is stabilising; some endpoint contracts are not yet verified against the live Keka API.
