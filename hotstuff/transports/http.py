"""HTTP transport implementation."""
import json
from typing import Optional, Any, Dict, Callable, Awaitable
import aiohttp

from hotstuff_sdk.types import HttpTransportOptions
from hotstuff_sdk.utils import ENDPOINTS_URLS


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
            Exception: If the request fails
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
                # Check if response is OK
                if not response.ok:
                    text = await response.text()
                    raise Exception(text or f"HTTP {response.status}")
                
                # Check content type
                content_type = response.headers.get("Content-Type", "")
                if "application/json" not in content_type:
                    text = await response.text()
                    raise Exception(text)
                
                # Parse response
                body = await response.json()
                
                # Check for error in response
                if isinstance(body, dict) and body.get("type") == "error":
                    raise Exception(body.get("message", "Unknown error"))
                
                return body
        
        except aiohttp.ClientError as e:
            raise Exception(f"HTTP request failed: {str(e)}")
        except Exception as e:
            raise e
    
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

