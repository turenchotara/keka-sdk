# Keka SDK Installation Guide

## Quick Installation

The Keka SDK package is now properly configured and can be installed using pip.

### Install from Local Directory

```bash
# Navigate to the project directory
cd D:\JetBrains\SDK\keka

# Install the package (this will also install httpx dependency)
pip install .

# Or install in development mode (allows live editing)
pip install -e .
```

### Install with Development Dependencies

```bash
# Install with development tools
pip install -e .[dev]
```

## Verification

After installation, verify the package works:

```python
# Test basic import
import keka_sdk
print(f"Keka SDK version: {keka_sdk.__version__}")

# Test client + auth imports
from keka_sdk import KekaClient, AsyncKekaClient, KekaAuth, KekaConfig
print("Clients imported successfully!")

# Test dependency
import httpx
print(f"httpx version: {httpx.__version__}")
```

## Package Structure

The package includes:

- **Main Components**:
  - `KekaClient` / `AsyncKekaClient` - client facades exposing `.hr` and `.helpdesk`
  - `KekaConfig` - instance URL, timeouts, and retry policy
  - `KekaAuth` + `AuthManager` - single authentication system
  - `transport` - one shared sync/async HTTP transport
  - `KekaError` (+ subclasses) - typed error hierarchy

- **Configuration Files**:
  - `pyproject.toml` - packaging configuration (single source of truth)
  - `MANIFEST.in` - Package file inclusion rules

- **Documentation**:
  - `README.md` - Complete usage documentation
  - `CHANGELOG.md` - Version history
  - `LICENSE` - MIT license

## Building Distribution

To create distribution packages:

```bash
# Build wheel and source distribution
make build

# Or manually
python -m build
```

This creates packages in the `dist/` directory that can be uploaded to PyPI.

## Development Workflow

1. **Setup**: `pip install -e .[dev]`
2. **Make changes** to the code
3. **Test**: `make test` or `python -m pytest`
4. **Format**: `make format`
5. **Check**: `make dev-check`
6. **Build**: `make build`

## Troubleshooting

### Import Errors
If you encounter import errors, ensure all dependencies are installed:
```bash
pip install httpx>=0.24.0
```

### Build Errors
If you get build errors, try:
```bash
pip install --upgrade setuptools wheel build
```

### Version Issues
The package version is defined in `keka_sdk/_version.py` and should be automatically detected.

## Next Steps

- Customize the package metadata in `pyproject.toml`
- Update the repository URLs and author information
- Extend the test suite under `tests/`
- Continuous integration is configured in `.github/workflows/ci.yml`
- Publish to PyPI when ready
