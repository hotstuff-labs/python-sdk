"""Info API client."""
from typing import Optional, Any, Dict


class InfoClient:
    """Client for querying market data and account information."""
    
    def __init__(self, transport):
        """
        Initialize InfoClient.
        
        Args:
            transport: The transport layer to use
        """
        self.transport = transport
    
    # Global Info Endpoints
    
    async def oracle(self, params: Dict[str, Any], signal: Optional[Any] = None) -> Dict[str, Any]:
        """Get oracle prices."""
        request = {"method": "oracle", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def supported_collateral(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get supported collateral."""
        request = {"method": "supportedCollateral", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def instruments(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get all instruments."""
        request = {"method": "instruments", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def ticker(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get ticker for a specific symbol."""
        request = {"method": "ticker", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def orderbook(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get orderbook with depth."""
        request = {"method": "orderbook", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def trades(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get recent trades."""
        request = {"method": "trades", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def mids(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get mid prices for all instruments."""
        request = {"method": "mids", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def bbo(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get best bid/offer."""
        request = {"method": "bbo", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def chart(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get chart data (candles or funding)."""
        request = {"method": "chart", "params": params}
        return await self.transport.request("info", request, signal)
    
    # Account Info Endpoints
    
    async def open_orders(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get open orders."""
        request = {"method": "openOrders", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def positions(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get current positions."""
        request = {"method": "positions", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def account_summary(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get account summary."""
        request = {"method": "accountSummary", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def referral_summary(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get referral summary."""
        request = {"method": "referralSummary", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def user_fee_info(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get user fee information."""
        request = {"method": "userFees", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def account_history(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get account history."""
        request = {"method": "accountHistory", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def order_history(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get order history."""
        request = {"method": "orderHistory", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def trade_history(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get trade history (fills)."""
        request = {"method": "fills", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def funding_history(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get funding history."""
        request = {"method": "fundingHistory", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def transfer_history(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get transfer history."""
        request = {"method": "transferHistory", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def instrument_leverage(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get instrument leverage settings."""
        request = {"method": "instrumentLeverage", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def get_referral_info(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get referral info."""
        request = {"method": "referralInfo", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def sub_accounts_list(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get sub-accounts list."""
        request = {"method": "subAccountsList", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def agents(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get agents."""
        request = {"method": "allAgents", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def user_balance(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get user balance."""
        request = {"method": "userBalance", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def account_info(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get account info."""
        request = {"method": "accountInfo", "params": params}
        return await self.transport.request("info", request, signal)
    
    # Vault Info Endpoints
    
    async def vaults(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get all vaults."""
        request = {"method": "vaults", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def sub_vaults(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get sub-vaults for a specific vault."""
        request = {"method": "subVaults", "params": params}
        return await self.transport.request("info", request, signal)
    
    async def vault_balances(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get vault balances."""
        request = {"method": "vaultBalance", "params": params}
        return await self.transport.request("info", request, signal)
    
    # Explorer Info Endpoints
    
    async def blocks(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get recent blocks."""
        request = {"method": "blocks", "params": params}
        return await self.transport.request("explorer", request, signal)
    
    async def block_details(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get specific block details."""
        request = {"method": "block", "params": params}
        return await self.transport.request("explorer", request, signal)
    
    async def transactions(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get recent transactions."""
        request = {"method": "transactions", "params": params}
        return await self.transport.request("explorer", request, signal)
    
    async def transaction_details(
        self, params: Dict[str, Any], signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """Get specific transaction details."""
        request = {"method": "transaction", "params": params}
        return await self.transport.request("explorer", request, signal)

