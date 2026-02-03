"""Test Pydantic model validation."""
import pytest
from pydantic import ValidationError


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
            cloid="test-123",
        )
        assert order.instrument_id == 1
        assert order.side == "b"
        assert order.cloid == "test-123"
    
    def test_unit_order_invalid_side(self):
        """Test UnitOrder with invalid side."""
        from hotstuff import UnitOrder
        
        with pytest.raises(ValidationError):
            UnitOrder(
                instrument_id=1,
                side="x",  # Invalid
                position_side="BOTH",
                price="50000.00",
                size="0.01",
                tif="GTC",
                ro=False,
                po=False,
                cloid="test-123",
            )
    
    def test_unit_order_invalid_instrument_id(self):
        """Test UnitOrder with invalid instrument_id."""
        from hotstuff import UnitOrder
        
        with pytest.raises(ValidationError):
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
                    cloid="test-123",
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
    
    def test_instruments_params_invalid_type(self):
        """Test InstrumentsParams with invalid type."""
        from hotstuff import InstrumentsParams
        
        with pytest.raises(ValidationError):
            InstrumentsParams(type="invalid")


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
