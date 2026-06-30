# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-06-22

### Changed (architecture consolidation)
- Consolidated three competing implementations into a single composition-based design:
  one shared transport (one connection pool) injected into the auth manager and every resource.
- Replaced the inheritance-based resources (`Employee(ApiClient)`, `TicketManagement(ApiClient)`)
  with `HRResource` / `HelpdeskResource` composed over `BaseResource`.
- Unified authentication into a single `AuthManager` + `KekaAuth` credentials object; the OAuth
  token endpoint is now derived from `instance_url` (removing the hardcoded demo host), and the
  grant type defaults to `client_credentials`.
- Added a typed error hierarchy: `KekaError` -> `KekaAuthError`, `KekaAPIError`,
  `KekaRateLimitError`, `KekaNotFoundError`. The transport never returns `None`.
- Hardened retries with jitter, a maximum backoff cap, and `Retry-After` handling on 429.
- Merged the duplicate HR/Helpdesk type modules into a single shared `keka_sdk.types` package.
- Moved to `pyproject.toml`-only packaging with a dynamic version; removed `setup.py`/`setup.cfg`
  and the unused `requests` dependency.

### Removed
- Orphaned `keka_sdk/hr.py` manager layer, the legacy `src/` resource tree, the duplicate auth
  systems, and committed build artifacts.

### Notes
- Version reset to `0.x` to reflect the in-progress public surface; methods whose Keka API
  contract is unverified raise `NotImplementedError`.

### Dependencies
- httpx>=0.24.0

### Supported Python Versions
- Python 3.8, 3.9, 3.10, 3.11, 3.12
