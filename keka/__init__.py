"""
Keka SDK

A Python SDK for interacting with the Keka HR API.
Provides authentication, HR operations, and API client functionality.
"""

# Import version first
from ._version import __version__, __version_info__

from keka_sdk.src import KekaClient, KekaAuth

__all__ = [
    # Version information
    "__version__",
    "__version_info__",
    
    # Authentication
    # "KekaAuthenticator",
    # "AsyncKekaAuthenticator",
    # "TokenManager",
    # "KekaAuthError",
    # "create_authenticator",
    
    # API Clients
    # "ApiClient",
    # "AsyncApiClient",
    
    # HR Operations
    # "HRClient",
    # "AsyncHRClient",

    # main client
    "KekaClient",
    "KekaAuth",
]
