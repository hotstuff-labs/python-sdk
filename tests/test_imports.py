"""Test that all imports work correctly."""
import pytest


def test_main_imports():
    """Test main package imports."""
    from hotstuff import (
        HttpTransport,
        WebSocketTransport,
        InfoClient,
        ExchangeClient,
        SubscriptionClient,
        HttpTransportOptions,
        WebSocketTransportOptions,
    )
    assert HttpTransport is not None
    assert WebSocketTransport is not None
    assert InfoClient is not None
    assert ExchangeClient is not None
    assert SubscriptionClient is not None


def test_exception_imports():
    """Test exception imports."""
    from hotstuff import (
        HotstuffError,
        HotstuffAPIError,
        HotstuffConnectionError,
        HotstuffTimeoutError,
        HotstuffAuthenticationError,
        HotstuffValidationError,
        HotstuffRateLimitError,
    )
    assert issubclass(HotstuffAPIError, HotstuffError)
    assert issubclass(HotstuffConnectionError, HotstuffError)
    assert issubclass(HotstuffTimeoutError, HotstuffError)


def test_method_type_imports():
    """Test method type imports."""
    from hotstuff import (
        PlaceOrderParams,
        UnitOrder,
        BrokerConfig,
        CancelAllParams,
        AddAgentParams,
    )
    assert PlaceOrderParams is not None
    assert UnitOrder is not None


def test_market_data_imports():
    """Test market data type imports from new clean module."""
    from hotstuff import (
        TickerParams,
        Ticker,
        OrderbookParams,
        OrderbookResponse,
        InstrumentsParams,
        InstrumentsResponse,
    )
    assert TickerParams is not None
    assert Ticker is not None


def test_subscription_imports():
    """Test subscription type imports from new clean module."""
    from hotstuff import (
        TickerSubscriptionParams,
        TradeSubscriptionParams,
        OrderbookSubscriptionParams,
    )
    assert TickerSubscriptionParams is not None


def test_backward_compatible_imports():
    """Test that old importlib-style imports still work."""
    import importlib
    
    # Old style (deprecated but should still work)
    global_methods = importlib.import_module("hotstuff.methods.info.global")
    assert hasattr(global_methods, "TickerParams")
    assert hasattr(global_methods, "Ticker")
    
    subscription_methods = importlib.import_module("hotstuff.methods.subscription.global")
    assert hasattr(subscription_methods, "TickerSubscriptionParams")


def test_new_clean_imports():
    """Test new clean imports without 'global' keyword."""
    from hotstuff.methods.info import market
    assert hasattr(market, "TickerParams")
    assert hasattr(market, "Ticker")
    
    from hotstuff.methods.subscription import channels
    assert hasattr(channels, "TickerSubscriptionParams")
