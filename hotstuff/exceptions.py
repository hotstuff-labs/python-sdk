"""Custom exceptions for the Hotstuff SDK."""


class HotstuffError(Exception):
    """Base exception for all Hotstuff SDK errors."""
    pass


class HotstuffAPIError(HotstuffError):
    """Error returned from the Hotstuff API."""
    
    def __init__(self, message: str, status_code: int = None, error_code: str = None):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self):
        parts = [self.message]
        if self.status_code:
            parts.append(f"(HTTP {self.status_code})")
        if self.error_code:
            parts.append(f"[{self.error_code}]")
        return " ".join(parts)


class HotstuffConnectionError(HotstuffError):
    """Error connecting to the Hotstuff API."""
    pass


class HotstuffTimeoutError(HotstuffError):
    """Request to the Hotstuff API timed out."""
    pass


class HotstuffAuthenticationError(HotstuffAPIError):
    """Authentication error (invalid signature, expired, etc.)."""
    pass


class HotstuffValidationError(HotstuffError):
    """Error validating request parameters."""
    pass


class HotstuffInsufficientFundsError(HotstuffAPIError):
    """Insufficient funds for the requested operation."""
    pass


class HotstuffOrderError(HotstuffAPIError):
    """Error related to order placement or management."""
    pass


class HotstuffRateLimitError(HotstuffAPIError):
    """Rate limit exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: int = None):
        super().__init__(message, status_code=429)
        self.retry_after = retry_after


class HotstuffWebSocketError(HotstuffError):
    """WebSocket-related error."""
    pass


class HotstuffSubscriptionError(HotstuffWebSocketError):
    """Error subscribing to a channel."""
    pass
