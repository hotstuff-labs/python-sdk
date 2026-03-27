"""Test dataclass model validation."""
import pytest


class TestOrderModels:
    """Test order-related models."""
    
    def test_unit_order_valid(self):
        """Test valid UnitOrder creation."""
        from hotstuff import UnitOrder
        
        order = UnitOrder(
            instrument_id=1,
            side="b",
            position_side="BOTH",
            price="50000.00",
            size="0.01",
            tif="GTC",
            ro=False,
            po=False,
            cloid="0x1234567890abcdef1234567890abcdef",
        )
        assert order.instrument_id == 1
        assert order.side == "b"
        assert order.cloid == "0x1234567890abcdef1234567890abcdef"
    
    def test_unit_order_without_cloid(self):
        """Test UnitOrder creation without cloid (optional field)."""
        from hotstuff import UnitOrder
        
        order = UnitOrder(
            instrument_id=1,
            side="b",
            position_side="BOTH",
            price="50000.00",
            size="0.01",
            tif="GTC",
            ro=False,
            po=False,
        )
        assert order.instrument_id == 1
        assert order.cloid is None
    
    def test_unit_order_valid_cloid_format(self):
        """Test UnitOrder with valid cloid format (0x + 32 hex digits)."""
        from hotstuff import UnitOrder
        
        order = UnitOrder(
            instrument_id=1,
            side="b",
            position_side="BOTH",
            price="50000.00",
            size="0.01",
            tif="GTC",
            ro=False,
            po=False,
            cloid="0x1234567890abcdef1234567890abcdef",
        )
        assert order.cloid == "0x1234567890abcdef1234567890abcdef"
    
    def test_unit_order_invalid_instrument_id(self):
        """Test UnitOrder with invalid instrument_id."""
        from hotstuff import UnitOrder
        
        with pytest.raises(ValueError):
            UnitOrder(
                instrument_id=0,  # Must be > 0
                side="b",
                position_side="BOTH",
                price="50000.00",
                size="0.01",
                tif="GTC",
                ro=False,
                po=False,
                cloid="test-123",
            )
    
    def test_place_order_params(self):
        """Test PlaceOrderParams creation."""
        from hotstuff import PlaceOrderParams, UnitOrder, BrokerConfig
        
        order = PlaceOrderParams(
            orders=[
                UnitOrder(
                    instrument_id=1,
                    side="b",
                    position_side="BOTH",
                    price="50000.00",
                    size="0.01",
                    tif="GTC",
                    ro=False,
                    po=False,
                    cloid="0xabcdef1234567890abcdef1234567890",
                )
            ],
            broker_config=BrokerConfig(broker="", fee="0"),
            expires_after=1700000000000,
        )
        assert len(order.orders) == 1
        assert order.expires_after == 1700000000000


class TestMarketModels:
    """Test market data models."""
    
    def test_ticker_params(self):
        """Test TickerParams creation."""
        from hotstuff import TickerParams
        
        params = TickerParams(symbol="BTC-PERP")
        assert params.symbol == "BTC-PERP"
    
    def test_instruments_params(self):
        """Test InstrumentsParams creation."""
        from hotstuff import InstrumentsParams
        
        params = InstrumentsParams(type="all")
        assert params.type == "all"
        
        params = InstrumentsParams(type="perps")
        assert params.type == "perps"


class TestAddressValidation:
    """Test Ethereum address validation."""
    
    def test_valid_address(self):
        """Test valid Ethereum address."""
        from hotstuff.utils.address import validate_ethereum_address
        
        # Valid checksummed address
        addr = "0x1234567890123456789012345678901234567890"
        result = validate_ethereum_address(addr)
        assert result.startswith("0x")
        assert len(result) == 42
    
    def test_invalid_address(self):
        """Test invalid Ethereum address."""
        from hotstuff.utils.address import validate_ethereum_address
        
        with pytest.raises(ValueError):
            validate_ethereum_address("invalid")
        
        with pytest.raises(ValueError):
            validate_ethereum_address("0x123")  # Too short
    
    def test_address_checksumming(self):
        """Test that addresses are properly checksummed."""
        from hotstuff.utils.address import validate_ethereum_address
        
        # Lowercase address
        addr = "0xabcdef0123456789abcdef0123456789abcdef01"
        result = validate_ethereum_address(addr)
        # Should be checksummed (mixed case)
        assert result != addr.lower()


class TestSubscriptionModels:
    """Test subscription models."""
    
    def test_ticker_subscription_params(self):
        """Test TickerSubscriptionParams creation."""
        from hotstuff import TickerSubscriptionParams
        
        params = TickerSubscriptionParams(symbol="BTC-PERP")
        assert params.symbol == "BTC-PERP"
    
    def test_account_subscription_params_with_user(self):
        """Test subscription params use 'user' field."""
        from hotstuff.methods.subscription.channels import AccountOrderUpdatesParams
        
        params = AccountOrderUpdatesParams(user="0x1234567890123456789012345678901234567890")
        assert params.user.startswith("0x")


class _StubTransport:
    """Stub transport returning a fixed payload."""

    def __init__(self, payload):
        self.payload = payload

    def request(self, endpoint, payload, signal=None):
        return self.payload


class TestResponsePassthrough:
    """Test that InfoClient returns raw server payloads."""

    def test_info_response_is_returned_as_is(self):
        """InfoClient should return raw dict response without dataclass wrapping."""
        from hotstuff import InfoClient, OracleParams

        payload = {
            "symbol": "BTC-PERP",
            "index_price": "50000",
            "ext_mark_price": "50010",
            "updated_at": 1700000000,
            "new_server_field": "keep-me",
        }

        client = InfoClient()
        client.transport = _StubTransport(payload)

        result = client.oracle(OracleParams(symbol="BTC-PERP"))
        assert result == payload

    def test_list_response_is_returned_as_is(self):
        """InfoClient should return raw list responses as-is."""
        from hotstuff import InfoClient, TickerParams

        payload = [
            {
                "symbol": "BTC-PERP",
                "mark_price": "50000",
                "mid_price": "50001",
                "index_price": "50002",
                "best_bid_price": "49999",
                "best_ask_price": "50003",
                "best_bid_size": "1",
                "best_ask_size": "2",
                "volume_24h": "100",
                "change_24h": "2",
                "last_updated": 1700000000,
                "extra_liquidity_hint": "server-value",
            }
        ]

        client = InfoClient()
        client.transport = _StubTransport(payload)

        result = client.ticker(TickerParams(symbol="BTC-PERP"))
        assert result == payload

    def test_response_with_untyped_shape_is_returned_as_is(self):
        """Untyped response payloads should be returned unchanged."""
        from hotstuff import InfoClient, BlocksParams

        payload = {
            "data": [{"height": 1}],
            "next_cursor": "cursor-1",
        }

        client = InfoClient()
        client.transport = _StubTransport(payload)

        result = client.blocks(BlocksParams(offset=0, limit=10))
        assert result == payload

    def test_websocket_result_ignores_unknown_fields(self):
        """Websocket result models should ignore unknown fields without raising."""
        from hotstuff.types import SubscribeResult, UnsubscribeResult

        subscribe = SubscribeResult(status="subscribed", channels=["ticker"], request_id="abc-1")
        unsubscribe = UnsubscribeResult(status="unsubscribed", channels=["ticker"], request_id="abc-2")

        assert subscribe.status == "subscribed"
        assert unsubscribe.status == "unsubscribed"
        assert not hasattr(subscribe, "request_id")
        assert not hasattr(unsubscribe, "request_id")
