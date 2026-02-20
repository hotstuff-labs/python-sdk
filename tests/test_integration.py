"""Integration tests for Hotstuff SDK (requires network access)."""
import pytest
import time

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture
def http_transport():
    """Create HTTP transport for testing."""
    from hotstuff import HttpTransport, HttpTransportOptions
    
    transport = HttpTransport(HttpTransportOptions(is_testnet=True))
    yield transport
    transport.close()


@pytest.fixture
def info_client(http_transport):
    """Create InfoClient for testing."""
    from hotstuff import InfoClient
    return InfoClient(transport=http_transport)


class TestInfoClientIntegration:
    """Integration tests for InfoClient."""
    
    def test_get_instruments(self, info_client):
        """Test fetching instruments."""
        from hotstuff import InstrumentsParams
        
        instruments = info_client.instruments(InstrumentsParams(type="all"))
        assert instruments is not None
        assert hasattr(instruments, "perps")
        assert hasattr(instruments, "spot")
        assert len(instruments.perps) > 0
    
    def test_get_ticker(self, info_client):
        """Test fetching ticker."""
        from hotstuff import TickerParams
        
        ticker = info_client.ticker(TickerParams(symbol="BTC-PERP"))
        assert ticker is not None
        assert len(ticker) > 0
        assert ticker[0].symbol == "BTC-PERP"
    
    def test_get_orderbook(self, info_client):
        """Test fetching orderbook."""
        from hotstuff import OrderbookParams
        
        orderbook = info_client.orderbook(OrderbookParams(symbol="BTC-PERP", depth=10))
        assert orderbook is not None
        assert hasattr(orderbook, "bids")
        assert hasattr(orderbook, "asks")


class TestWebSocketIntegration:
    """Integration tests for WebSocket subscriptions."""
    
    def test_ticker_subscription(self):
        """Test subscribing to ticker updates."""
        from hotstuff import (
            WebSocketTransport,
            SubscriptionClient,
            WebSocketTransportOptions,
            TickerSubscriptionParams,
        )
        
        transport = WebSocketTransport(WebSocketTransportOptions(is_testnet=True))
        subscriptions = SubscriptionClient(transport=transport)
        
        received = []
        
        def handler(data):
            received.append(data)
        
        try:
            sub = subscriptions.ticker(
                TickerSubscriptionParams(symbol="BTC-PERP"),
                handler
            )
            
            # Wait for some data
            time.sleep(5)
            
            # Should have received at least one update
            assert len(received) > 0
            
            sub["unsubscribe"]()
        finally:
            transport.disconnect()
