"""HTTP transport implementation."""
import json
from typing import Optional, Any, Dict, Callable, Awaitable
import aiohttp
import asyncio

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
        
        # Session will be created lazily
        self._session: Optional[aiohttp.ClientSession] = None
    
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self.timeout) if self.timeout else None
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session
    
    async def request(
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
            signal: Optional abort signal
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
            session = await self._get_session()
            
            # Prepare request kwargs
            kwargs: Dict[str, Any] = {
                "headers": headers,
            }
            
            if method == "POST":
                kwargs["json"] = payload
            
            # Make request
            async with session.request(method, url, **kwargs) as response:
                # Handle rate limiting
                if response.status == 429:
                    retry_after = response.headers.get("Retry-After")
                    raise HotstuffRateLimitError(
                        "Rate limit exceeded",
                        retry_after=int(retry_after) if retry_after else None
                    )
                
                # Handle authentication errors
                if response.status in (401, 403):
                    text = await response.text()
                    raise HotstuffAuthenticationError(text or "Authentication failed", status_code=response.status)
                
                # Check if response is OK
                if not response.ok:
                    text = await response.text()
                    raise HotstuffAPIError(text or f"HTTP {response.status}", status_code=response.status)
                
                # Check content type
                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    text = await response.text()
                    raise HotstuffAPIError(f"Unexpected content type: {text}")
                
                # Parse response
                body = await response.json()
                
                # Check for error in response
                if isinstance(body, dict) and body.get("type") == "error":
                    raise HotstuffAPIError(body.get("message", "Unknown error"))
                
                return body
        
        except asyncio.TimeoutError:
            raise HotstuffTimeoutError(f"Request to {endpoint} timed out")
        except aiohttp.ClientConnectorError as e:
            raise HotstuffConnectionError(f"Failed to connect to {url}: {str(e)}")
        except aiohttp.ClientError as e:
            raise HotstuffConnectionError(f"HTTP request failed: {str(e)}")
        except (HotstuffAPIError, HotstuffConnectionError, HotstuffTimeoutError, HotstuffRateLimitError):
            raise
        except Exception as e:
            raise HotstuffAPIError(str(e))
    
    async def close(self):
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()
    
    async def __aenter__(self):
        """Async context manager entry."""
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

