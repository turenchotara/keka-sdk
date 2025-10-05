# Keka SDK - API Client with Authentication and CRUD Operations

A modern Python SDK for the Keka HR API that supports authentication, CRUD operations, and built-in retry logic for transient errors. Includes both synchronous and asynchronous versions with comprehensive authentication support.

## Features

- **Authentication**: Complete support for Keka authentication methods (API key, username/password, token-based)
- **Token Management**: Automatic token refresh, validation, and lifecycle management
- **CRUD Operations**: Complete support for Create, Read, Update, and Delete operations
- **Automatic Retry Logic**: Exponential backoff for transient errors (timeouts, 5xx, 429 responses)
- **Modern HTTP Client**: Built with `httpx` for better performance and features
- **Async Support**: Both synchronous and asynchronous clients available
- **Configurable**: Customizable retry parameters, headers, and timeouts
- **Clean API**: Simple and intuitive interface
- **Context Manager Support**: Use with `with` statements for automatic cleanup
- **Error Handling**: Comprehensive error handling with custom exceptions

## Installation

### Install from PyPI (Recommended)

```bash
pip install keka-sdk
```

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/keka-sdk.git
cd keka-sdk

# Install in development mode
pip install -e .

# Or install normally
pip install .
```

### Install with Development Dependencies

```bash
# For development
pip install keka-sdk[dev]

# For documentation
pip install keka-sdk[docs]

# For both
pip install keka-sdk[dev,docs]
```

### Install from Requirements File

If you have a requirements.txt file:

```bash
pip install -r requirements.txt
```

## Package Development and Installation

### Local Development Setup

```bash
# Clone and navigate to the project
git clone https://github.com/yourusername/keka-sdk.git
cd keka-sdk

# Install in development mode
pip install -e .[dev]

# Set up pre-commit hooks (optional)
pre-commit install
```

### Building and Distribution

```bash
# Clean previous builds
make clean

# Build the package
make build

# Install locally built package
pip install dist/keka_sdk-*.whl

# Publish to PyPI (requires authentication)
make publish
```

### Using the Makefile

The project includes a Makefile with common development tasks:

```bash
# See all available commands
make help

# Install in development mode
make install-dev

# Run tests
make test

# Format code
make format

# Check code quality
make dev-check

# Build documentation
make docs
```

## Quick Start

### Authentication

```python
from keka_sdk import ApiClient, create_authenticator

# Initialize the client and authenticator
base_url = "https://login.your-environment.keka.com"
api_client = ApiClient(base_url=base_url)
authenticator = create_authenticator(base_url, api_client)

# Authenticate with API key, client credentials, and scope
auth_response = authenticator.authenticate_with_api_key(
    api_key="your-api-key",
    client_id="your-client-id", 
    client_secret="your-client-secret",
    scope="kekaapi"
)

# Get authentication headers for API requests
auth_headers = authenticator.get_auth_headers()
```

### Synchronous Client with Authentication

```python
from keka_sdk import ApiClient, create_authenticator

# Initialize the client
base_url = "https://login.your-environment.keka.com"
api_client = ApiClient(base_url=base_url)

# Authenticate
authenticator = create_authenticator(base_url, api_client)
authenticator.authenticate_with_api_key(
    api_key="your-api-key",
    client_id="your-client-id",
    client_secret="your-client-secret",
    scope="kekaapi"
)

# Use authenticated client for CRUD operations
auth_headers = authenticator.get_auth_headers()
response = api_client.get("/api/v1/employees", headers=auth_headers)
response = api_client.post("/api/v1/employees", data={"name": "John"}, headers=auth_headers)

# Clean up
api_client.close()
```

### Asynchronous Client with Authentication

```python
import asyncio
from keka_sdk import AsyncApiClient, create_authenticator

async def main():
    base_url = "https://login.your-environment.keka.com"
    async with AsyncApiClient(base_url=base_url) as api_client:
        
        # Authenticate
        authenticator = create_authenticator(base_url, api_client)
        await authenticator.authenticate_with_api_key(
            api_key="your-api-key",
            client_id="your-client-id",
            client_secret="your-client-secret",
            scope="kekaapi"
        )
        
        # Use authenticated client for CRUD operations
        auth_headers = authenticator.get_auth_headers()
        response = await api_client.get("/api/v1/employees", headers=auth_headers)
        response = await api_client.post("/api/v1/employees", data={"name": "John"}, headers=auth_headers)
        


# Run the async function
asyncio.run(main())
```

## Authentication

The Keka SDK supports API key authentication using Keka's OAuth2 endpoint at `https://login.{environment}.keka.com/connect/token`.

For more details, visit the [Keka API documentation](https://developers.keka.com/reference).

### API Key Authentication

Uses the `client_credentials` grant type with API key in the `X-API-Key` header as per [Keka API documentation](https://developers.keka.com/reference/token-1).

```python
from keka_sdk import ApiClient, create_authenticator

api_client = ApiClient(base_url="https://login.your-environment.keka.com")
authenticator = create_authenticator(base_url, api_client)

# Authenticate with API key, client credentials, and scope
auth_response = authenticator.authenticate_with_api_key(
    api_key="your-api-key",
    client_id="your-client-id",
    client_secret="your-client-secret",
    scope="kekaapi"
)
print(f"Access Token: {authenticator.token_manager.access_token}")
```









### Token Manager

```python
from keka_sdk import TokenManager

# Create token manager
token_manager = TokenManager()

# Set tokens manually
token_manager.set_tokens(
    access_token="your-access-token",
    refresh_token="your-refresh-token",
    expires_in=3600,  # 1 hour
    token_type="Bearer"
)

# Check token validity
if token_manager.is_token_valid:
    auth_header = token_manager.get_auth_header()
    print(f"Authorization: {auth_header}")

# Clear tokens
token_manager.clear_tokens()
```

### Error Handling

```python
from keka_sdk import KekaAuthError

try:
    authenticator.authenticate_with_api_key(
        api_key="invalid-key",
        client_id="invalid-client-id",
        client_secret="invalid-client-secret"
    )
except KekaAuthError as e:
    print(f"Authentication failed: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Configuration Options

### ApiClient Parameters

- `base_url` (str): The base URL for all API requests
- `headers` (dict, optional): Default headers for all requests
- `timeout` (float): Request timeout in seconds (default: 30.0)
- `max_retries` (int): Maximum retry attempts (default: 3)
- `retry_delay` (float): Initial delay between retries in seconds (default: 1.0)
- `backoff_factor` (float): Multiplier for exponential backoff (default: 2.0)
- `retry_status_codes` (set): Status codes to retry on (default: {429, 500, 502, 503, 504})

### Retry Logic

The client automatically retries requests on:
- **Connection errors** (network issues, timeouts)
- **HTTP status codes**: 429 (Too Many Requests), 500 (Internal Server Error), 502 (Bad Gateway), 503 (Service Unavailable), 504 (Gateway Timeout)

Retry behavior:
- Exponential backoff: delay increases by `backoff_factor` each attempt
- Maximum retries: `max_retries` attempts
- Logging: Warning messages for retry attempts, error messages when all retries fail

## API Methods

### GET Request
```python
response = api_client.get(
    endpoint="/users",
    params={"page": 1, "limit": 10},
    headers={"Custom-Header": "value"}
)
```

### POST Request (Create)
```python
response = api_client.post(
    endpoint="/users",
    data={"name": "John", "email": "john@example.com"},
    headers={"Content-Type": "application/json"}
)
```

### PUT Request (Update/Replace)
```python
response = api_client.put(
    endpoint="/users/1",
    data={"name": "Jane", "email": "jane@example.com"}
)
```

### PATCH Request (Partial Update)
```python
response = api_client.patch(
    endpoint="/users/1",
    data={"name": "Jane"}
)
```

### DELETE Request
```python
response = api_client.delete(
    endpoint="/users/1",
    headers={"Authorization": "Bearer token"}
)
```

## Context Manager Usage

### Synchronous Client

```python
with ApiClient("https://api.example.com") as client:
    response = client.get("/users")
    # Client automatically closed when exiting the context
```

### Asynchronous Client

```python
async with AsyncApiClient("https://api.example.com") as client:
    response = await client.get("/users")
    # Client automatically closed when exiting the context
```

## Error Handling

```python
try:
    response = api_client.get("/users/999")
    if response.status_code == 404:
        print("User not found")
    elif response.status_code == 200:
        user_data = response.json()
        print(f"User: {user_data}")
except Exception as e:
    print(f"Request failed: {e}")
```

## Example Usage

### Synchronous Client

See `example_usage.py` for a complete demonstration of all CRUD operations using the JSONPlaceholder API.

Run the example:
```bash
python example_usage.py
```

### Authentication Examples

See `auth_example_usage.py` for a complete demonstration of all authentication methods including API key, username/password, token refresh, and error handling.

Run the authentication example:
```bash
python auth_example_usage.py
```

### Asynchronous Client

See `async_example_usage.py` for a complete demonstration of async CRUD operations, including concurrent requests.

Run the async example:
```bash
python async_example_usage.py
```

## Response Object

All methods return an `httpx.Response` object with standard properties:
- `response.status_code`: HTTP status code
- `response.json()`: Parse JSON response
- `response.text`: Raw response text
- `response.headers`: Response headers

## Logging

The client logs retry attempts and errors. Configure logging to see retry behavior:

```python
import logging
logging.basicConfig(level=logging.INFO)
```

## Best Practices

### Authentication
1. **Store credentials securely** - Use environment variables or secure credential storage
2. **Handle token expiration** - Check `token_manager.is_token_valid` before making requests
3. **Implement token refresh** - Use refresh tokens to maintain long-running sessions
4. **Logout when done** - Always call `logout()` to invalidate tokens
5. **Validate tokens** - Use `validate_token()` to check token status before critical operations

### API Usage
1. **Always close the client** when done or use context manager
2. **Handle exceptions** appropriately for your use case
3. **Configure retry parameters** based on your API's characteristics
4. **Use appropriate HTTP methods** (PUT for full updates, PATCH for partial)
5. **Set reasonable timeouts** to avoid hanging requests
6. **Use async client for concurrent operations** to improve performance
7. **Leverage `asyncio.gather()`** for multiple concurrent requests

## Dependencies

- `httpx>=0.24.0`: Modern HTTP client library

## License

This implementation is provided as-is for educational and development purposes.