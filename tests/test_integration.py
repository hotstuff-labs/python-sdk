"""Integration tests for Hotstuff SDK (requires network access)."""
import pytest
import asyncio

# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def http_transport():
    """Create HTTP transport for testing."""
    from hotstuff import HttpTransport, HttpTransportOptions
    
    transport = HttpTransport(HttpTransportOptions(is_testnet=True))
    yield transport
    await transport.close()


@pytest.fixture
async def info_client(http_transport):
    """Create InfoClient for testing."""
    from hotstuff import InfoClient
    return InfoClient(transport=http_transport)


class TestInfoClientIntegration:
    """Integration tests for InfoClient."""
    
    @pytest.mark.asyncio
    async def test_get_instruments(self, info_client):
        """Test fetching instruments."""
        from hotstuff import InstrumentsParams
        
        instruments = await info_client.instruments(InstrumentsParams(type="all"))
        assert instruments is not None
        assert hasattr(instruments, "perps")
        assert hasattr(instruments, "spot")
        assert len(instruments.perps) > 0
    
    @pytest.mark.asyncio
    async def test_get_ticker(self, info_client):
        """Test fetching ticker."""
        from hotstuff import TickerParams
        
        ticker = await info_client.ticker(TickerParams(symbol="BTC-PERP"))
        assert ticker is not None
        assert len(ticker) > 0
        assert ticker[0].symbol == "BTC-PERP"
    
    @pytest.mark.asyncio
    async def test_get_orderbook(self, info_client):
        """Test fetching orderbook."""
        from hotstuff import OrderbookParams
        
        orderbook = await info_client.orderbook(OrderbookParams(symbol="BTC-PERP", depth=10))
        assert orderbook is not None
        assert hasattr(orderbook, "bids")
        assert hasattr(orderbook, "asks")


class TestWebSocketIntegration:
    """Integration tests for WebSocket subscriptions."""
    
    @pytest.mark.asyncio
    async def test_ticker_subscription(self):
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
            sub = await subscriptions.ticker(
                TickerSubscriptionParams(symbol="BTC-PERP"),
                handler
            )
            
            # Wait for some data
            await asyncio.sleep(5)
            
            # Should have received at least one update
            assert len(received) > 0
            
            await sub["unsubscribe"]()
        finally:
            await transport.disconnect()
