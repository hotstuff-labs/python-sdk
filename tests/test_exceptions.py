"""Test custom exceptions."""
import pytest
from hotstuff.exceptions import (
    HotstuffError,
    HotstuffAPIError,
    HotstuffConnectionError,
    HotstuffTimeoutError,
    HotstuffAuthenticationError,
    HotstuffRateLimitError,
)


class TestExceptionHierarchy:
    """Test exception class hierarchy."""
    
    def test_base_exception(self):
        """Test base HotstuffError."""
        with pytest.raises(HotstuffError):
            raise HotstuffError("Test error")
    
    def test_api_error_inherits_from_base(self):
        """Test HotstuffAPIError inherits from HotstuffError."""
        with pytest.raises(HotstuffError):
            raise HotstuffAPIError("API error")
    
    def test_connection_error_inherits_from_base(self):
        """Test HotstuffConnectionError inherits from HotstuffError."""
        with pytest.raises(HotstuffError):
            raise HotstuffConnectionError("Connection error")


class TestAPIError:
    """Test HotstuffAPIError."""
    
    def test_api_error_with_message(self):
        """Test API error with message only."""
        error = HotstuffAPIError("Something went wrong")
        assert str(error) == "Something went wrong"
    
    def test_api_error_with_status_code(self):
        """Test API error with status code."""
        error = HotstuffAPIError("Not found", status_code=404)
        assert "404" in str(error)
        assert error.status_code == 404
    
    def test_api_error_with_error_code(self):
        """Test API error with error code."""
        error = HotstuffAPIError("Invalid order", error_code="INVALID_ORDER")
        assert "INVALID_ORDER" in str(error)
        assert error.error_code == "INVALID_ORDER"


class TestRateLimitError:
    """Test HotstuffRateLimitError."""
    
    def test_rate_limit_error_default(self):
        """Test rate limit error with defaults."""
        error = HotstuffRateLimitError()
        assert error.status_code == 429
        assert "rate limit" in str(error).lower()
    
    def test_rate_limit_error_with_retry_after(self):
        """Test rate limit error with retry_after."""
        error = HotstuffRateLimitError("Too many requests", retry_after=60)
        assert error.retry_after == 60


class TestAuthenticationError:
    """Test HotstuffAuthenticationError."""
    
    def test_auth_error(self):
        """Test authentication error."""
        error = HotstuffAuthenticationError("Invalid signature", status_code=401)
        assert error.status_code == 401
        assert isinstance(error, HotstuffAPIError)
