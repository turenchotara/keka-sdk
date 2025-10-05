# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial package structure setup
- Support for modern Python packaging (pyproject.toml)
- Comprehensive installation instructions

## [1.0.0] - 2024-01-XX

### Added
- Initial release of Keka SDK
- Authentication support with API key
- Token management with automatic refresh
- CRUD operations for Keka API
- Automatic retry logic with exponential backoff
- Synchronous and asynchronous client support
- Context manager support
- Comprehensive error handling
- HR operations support
- Helpdesk operations support
- Type hints and py.typed marker
- Documentation and examples

### Features
- **Authentication**: Complete support for Keka authentication methods
- **Token Management**: Automatic token refresh, validation, and lifecycle management
- **CRUD Operations**: Complete support for Create, Read, Update, and Delete operations
- **Automatic Retry Logic**: Exponential backoff for transient errors
- **Modern HTTP Client**: Built with httpx for better performance
- **Async Support**: Both synchronous and asynchronous clients available
- **Configurable**: Customizable retry parameters, headers, and timeouts
- **Clean API**: Simple and intuitive interface

### Dependencies
- httpx>=0.24.0

### Supported Python Versions
- Python 3.8+
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12
