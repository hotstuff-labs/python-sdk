"""HTTP transport implementation."""
from typing import Optional, Any
import requests

from hotstuff.types import HttpTransportOptions
from hotstuff.utils import ENDPOINTS_URLS
from hotstuff.exceptions import (
    HotstuffAPIError,
    HotstuffConnectionError,
    HotstuffTimeoutError,
    HotstuffRateLimitError,
    HotstuffAuthenticationError,
)


class HttpTransport:
    """HTTP transport for making API requests."""
    
    def __init__(self, options: Optional[HttpTransportOptions] = None):
        """
        Initialize HTTP transport.
        
        Args:
            options: Transport configuration options
        """
        options = options or HttpTransportOptions()
        
        self.is_testnet = options.is_testnet
        self.timeout = options.timeout
        
        # Setup server endpoints
        self.server = {
            "mainnet": {
                "api": ENDPOINTS_URLS["mainnet"]["api"],
                "rpc": ENDPOINTS_URLS["mainnet"]["rpc"],
            },
            "testnet": {
                "api": ENDPOINTS_URLS["testnet"]["api"],
                "rpc": ENDPOINTS_URLS["testnet"]["rpc"],
            },
        }
        
        if options.server:
            if "mainnet" in options.server:
                self.server["mainnet"].update(options.server["mainnet"])
            if "testnet" in options.server:
                self.server["testnet"].update(options.server["testnet"])
        
        self.headers = options.headers or {}
        self.on_request = options.on_request
        self.on_response = options.on_response
        
        # Session for connection pooling
        self._session: Optional[requests.Session] = None
    
    def _get_session(self) -> requests.Session:
        """Get or create requests session."""
        if self._session is None:
            self._session = requests.Session()
        return self._session
    
    def request(
        self,
        endpoint: str,
        payload: Any,
        signal: Optional[Any] = None,
        method: str = "POST"
    ) -> Any:
        """
        Make an HTTP request.
        
        Args:
            endpoint: The endpoint to call ('info', 'exchange', or 'explorer')
            payload: The request payload
            signal: Optional abort signal (not used in sync version)
            method: HTTP method (GET or POST)
            
        Returns:
            The response data
            
        Raises:
            HotstuffAPIError: If the API returns an error
            HotstuffConnectionError: If connection fails
            HotstuffTimeoutError: If request times out
            HotstuffRateLimitError: If rate limit is exceeded
        """
        try:
            # Determine the base URL
            network = "testnet" if self.is_testnet else "mainnet"
            base_url = self.server[network]["rpc" if endpoint == "explorer" else "api"]
            url = f"{base_url}{endpoint}"
            
            # Prepare headers
            headers = {
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                **self.headers,
            }
            
            # Get session
            session = self._get_session()
            
            # Make request
            if method == "POST":
                response = session.post(
                    url,
                    json=payload,
                    headers=headers,
                    timeout=self.timeout
                )
            else:
                response = session.get(
                    url,
                    headers=headers,
                    timeout=self.timeout
                )
            
            # Handle rate limiting
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                raise HotstuffRateLimitError(
                    "Rate limit exceeded",
                    retry_after=int(retry_after) if retry_after else None
                )
            
            # Handle authentication errors
            if response.status_code in (401, 403):
                raise HotstuffAuthenticationError(
                    response.text or "Authentication failed",
                    status_code=response.status_code
                )
            
            # Check if response is OK
            if not response.ok:
                raise HotstuffAPIError(
                    response.text or f"HTTP {response.status_code}",
                    status_code=response.status_code
                )
            
            # Check content type
            content_type = response.headers.get("Content-Type", "")
            if "application/json" not in content_type:
                raise HotstuffAPIError(f"Unexpected content type: {response.text}")
            
            # Parse response
            body = response.json()
            
            # Check for error in response
            if isinstance(body, dict) and body.get("type") == "error":
                raise HotstuffAPIError(body.get("message", "Unknown error"))
            
            return body
        
        except requests.Timeout:
            raise HotstuffTimeoutError(f"Request to {endpoint} timed out")
        except requests.ConnectionError as e:
            raise HotstuffConnectionError(f"Failed to connect to {url}: {str(e)}")
        except requests.RequestException as e:
            raise HotstuffConnectionError(f"HTTP request failed: {str(e)}")
        except (HotstuffAPIError, HotstuffConnectionError, HotstuffTimeoutError, HotstuffRateLimitError):
            raise
        except Exception as e:
            raise HotstuffAPIError(str(e))
    
    def close(self):
        """Close the HTTP session."""
        if self._session:
            self._session.close()
            self._session = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
