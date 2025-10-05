"""
Keka Authentication Module

This module provides authentication functionality for the Keka SDK.
Supports various authentication methods including API key, username/password,
and token-based authentication.
"""

from abc import ABC, abstractmethod
import logging
import time
from typing import Any, Dict, Optional, Union
from urllib.parse import urljoin

from ....client import ApiClient, AsyncApiClient
from keka_sdk.utils.helpers import get_auth_headers, get_token_headers

logger = logging.getLogger(__name__)


class KekaAuthError(Exception):
    """Custom exception for Keka authentication errors."""
    pass


class TokenManager:
    """Manages authentication tokens for Keka API."""
    
    def __init__(self):
        self._access_token: Optional[str] = None
        self._refresh_token: Optional[str] = None
        self._token_expires_at: Optional[float] = None
        self._token_type: str = "Bearer"
    
    @property
    def access_token(self) -> Optional[str]:
        """Get the current access token."""
        return self._access_token
    
    @property
    def refresh_token(self) -> Optional[str]:
        """Get the current refresh token."""
        return self._refresh_token
    
    @property
    def token_type(self) -> str:
        """Get the token type (usually 'Bearer')."""
        return self._token_type
    
    @property
    def is_token_valid(self) -> bool:
        """Check if the current token is valid and not expired."""
        if not self._access_token:
            return False
        
        if self._token_expires_at is None:
            return True  # No expiration set
        
        return time.time() < self._token_expires_at
    
    def set_tokens(self, access_token: str, refresh_token: Optional[str] = None, 
                   expires_in: Optional[int] = None, token_type: str = "Bearer") -> None:
        """
        Set authentication tokens.
        
        Args:
            access_token: The access token
            refresh_token: The refresh token (optional)
            expires_in: Token expiration time in seconds (optional)
            token_type: Type of token (default: "Bearer")
        """
        self._access_token = access_token
        self._refresh_token = refresh_token
        self._token_type = token_type
        
        if expires_in:
            self._token_expires_at = time.time() + expires_in
        else:
            self._token_expires_at = None
        
        logger.info("Authentication tokens set successfully")
    
    def clear_tokens(self) -> None:
        """Clear all stored tokens."""
        self._access_token = None
        self._refresh_token = None
        self._token_expires_at = None
        logger.info("Authentication tokens cleared")
    
    def get_auth_header(self) -> Optional[str]:
        """Get the Authorization header value."""
        if self.is_token_valid and self._access_token:
            return f"{self._token_type} {self._access_token}"
        return None


class KekaAuthenticator:
    """Handles authentication with Keka API."""
    
    def __init__(self, base_url: str, client: Union[ApiClient, AsyncApiClient]):
        """
        Initialize the Keka authenticator.
        
        Args:
            base_url: Base URL for Keka API
            client: API client instance (sync or async)
        """
        self.base_url = base_url.rstrip('/')
        self.client = client
        self.token_manager = TokenManager()
        
        # Authentication endpoint - using Keka's API endpoint
        self.auth_endpoint = '/connect/token'
    
    def _build_auth_url(self, endpoint: str) -> str:
        """Build full URL for authentication endpoints."""
        return urljoin(self.base_url + '/', endpoint.lstrip('/'))
    
    def authenticate_with_api_key(self, api_key: str, client_id: str, client_secret: str, scope: str = "kekaapi") -> Dict[str, Any]:
        """
        Authenticate using API key as per Keka API documentation.
        
        Args:
            api_key: Keka API key
            client_id: OAuth client ID
            client_secret: OAuth client secret
            scope: OAuth scope (default: "kekaapi")
            
        Returns:
            Dictionary containing authentication response
            
        Raises:
            KekaAuthError: If authentication fails
        """
        try:
            headers = get_token_headers()
            headers['X-API-Key'] = api_key
            
            data = {
                'grant_type': 'client_credentials',
                'scope': scope,
                'client_id': client_id,
                'client_secret': client_secret
            }
            
            response = self.client.post(
                self.auth_endpoint,
                data=data,
                headers=headers
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                self._process_auth_response(auth_data)
                return auth_data
            else:
                error_msg = f"API key authentication failed: {response.status_code}"
                try:
                    error_data = response.json()
                    if 'error_description' in error_data:
                        error_msg += f" - {error_data['error_description']}"
                except:
                    pass
                raise KekaAuthError(error_msg)
                
        except Exception as e:
            logger.error(f"API key authentication error: {str(e)}")
            raise KekaAuthError(f"Authentication failed: {str(e)}")
    

    

    
    def _process_auth_response(self, auth_data: Dict[str, Any]) -> None:
        """
        Process authentication response and store tokens.
        
        Args:
            auth_data: Authentication response data
        """
        access_token = auth_data.get('access_token')
        refresh_token = auth_data.get('refresh_token')
        token_type = auth_data.get('token_type', 'Bearer')
        expires_in = auth_data.get('expires_in')
        
        if not access_token:
            raise KekaAuthError("No access token in authentication response")
        
        self.token_manager.set_tokens(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            token_type=token_type
        )
    
    def get_auth_headers(self) -> Dict[str, str]:
        """
        Get authentication headers for API requests.
        
        Returns:
            Dictionary containing authentication headers
        """
        auth_header = self.token_manager.get_auth_header()
        if auth_header:
            return get_auth_headers(auth_header)
        else:
            return get_auth_headers()


class AsyncKekaAuthenticator(KekaAuthenticator):
    """Async version of Keka authenticator."""
    
    async def authenticate_with_api_key(self, api_key: str, client_id: str, client_secret: str, scope: str = "kekaapi") -> Dict[str, Any]:
        """Async version of API key authentication."""
        try:
            headers = get_token_headers()
            headers['X-API-Key'] = api_key
            
            data = {
                'grant_type': 'client_credentials',
                'scope': scope,
                'client_id': client_id,
                'client_secret': client_secret
            }
            
            response = await self.client.post(
                self.auth_endpoint,
                data=data,
                headers=headers
            )
            
            if response.status_code == 200:
                auth_data = response.json()
                self._process_auth_response(auth_data)
                return auth_data
            else:
                error_msg = f"API key authentication failed: {response.status_code}"
                try:
                    error_data = response.json()
                    if 'error_description' in error_data:
                        error_msg += f" - {error_data['error_description']}"
                except:
                    pass
                raise KekaAuthError(error_msg)
                
        except Exception as e:
            logger.error(f"API key authentication error: {str(e)}")
            raise KekaAuthError(f"Authentication failed: {str(e)}")
    

    



def create_authenticator(base_url: str, client: Union[ApiClient, AsyncApiClient]) -> Union[KekaAuthenticator, AsyncKekaAuthenticator]:
    """
    Factory function to create appropriate authenticator based on client type.
    
    Args:
        base_url: Base URL for Keka API
        client: API client instance (sync or async)
        
    Returns:
        Appropriate authenticator instance
    """
    if isinstance(client, AsyncApiClient):
        return AsyncKekaAuthenticator(base_url, client)
    else:
        return KekaAuthenticator(base_url, client)




class BaseAuth(ABC):
    """
    Keka Authentication Class
    
    This class provides authentication functionality for the Keka SDK.
    Supports various authentication methods including API key, username/password,
    and token-based authentication.
    """

    __login_url = "https://login.kekademo.com/connect/token"

    def __init__(self, client_id: str, client_secret: str, api_key: str, scope: str = "kekaapi", grant_type: str = "kekaapi") -> None:
        self.instant_url = self.__login_url
        self.scope = scope
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_key = api_key

        self.__auth_token = None

    @property
    def auth_token(self) -> Optional[str]:
        """Get the current access token."""
        return self.__auth_token
    
    @auth_token.setter
    def auth_token(self, value: str) -> None:
        self.__auth_token = value

    @auth_token.deleter
    def auth_token(self) -> None:
        self.__auth_token = None

    @abstractmethod
    def refresh_auth_token(self) -> None:
        pass
    
    @abstractmethod
    def generate_auth_token(self) -> None:
        pass


class KekaAuth(BaseAuth, ApiClient):
    """
    Keka Authentication Class
    
    This class provides authentication functionality for the Keka SDK.
    Supports various authentication methods including API key, username/password,
    and token-based authentication.
    """

    def __init__(self, client_id: str, client_secret: str, api_key: str, scope: str = "kekaapi", grant_type: str = "kekaapi") -> None:
        BaseAuth.__init__(self, client_id, client_secret, api_key, scope, grant_type)
        ApiClient.__init__(self, self.instant_url)

    def refresh_auth_token(self) -> None:
        pass

    def generate_auth_token(self) -> bool:
        json_data = {
            "grant_type": self.grant_type,
            "scope": self.scope,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "api_key": self.api_key
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        response = self.post("", data=json_data, headers=headers)
        result = response.json()
        if response.status_code == 200:
            self.auth_token = result.get("access_token")
            return True
        else:
            return False


class AsyncKekaAuth(BaseAuth):
    """
    Async Keka Authentication Class
    
    This class provides authentication functionality for the Keka SDK.
    Supports various authentication methods including API key, username/password,
    and token-based authentication.
    """

    def __init__(self, client_id: str, client_secret: str, api_key: str, scope: str = "kekaapi", grant_type: str = "kekaapi") -> None:
        super().__init__(client_id, client_secret, api_key, scope, grant_type)

    async def refresh_auth_token(self) -> None:
        pass

    async def generate_auth_token(self) -> None:
        pass

