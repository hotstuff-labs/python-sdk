"""Info API client."""
from typing import Optional, Any
from dataclasses import asdict

from hotstuff.methods.info import market as GM
from hotstuff.methods.info import account as AM
from hotstuff.methods.info import vault as VM
from hotstuff.methods.info import explorer as EM

from hotstuff.transports import HttpTransport, WebSocketTransport
from hotstuff.types import HttpTransportOptions, WebSocketTransportOptions


class InfoClient:
    """Client for querying market data and account information."""
    
    def __init__(self, websocket: bool = False, is_testnet: bool = False):
        """
        Initialize InfoClient.
        
        Args:
            transport: The transport layer to use
        """
        self.websocket = websocket
        if websocket:
            self.transport = WebSocketTransport(WebSocketTransportOptions(is_testnet=is_testnet))
        else:
            self.transport = HttpTransport(HttpTransportOptions(is_testnet=is_testnet))
    
    def _to_dict(self, obj) -> dict:
        """Convert dataclass to dict."""
        return asdict(obj)
    
    def oracle(
        self, params: GM.OracleParams, signal: Optional[Any] = None
    ) -> Any:
        """Get oracle prices."""
        request = {"method": "oracle", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def supported_collateral(
        self, params: GM.SupportedCollateralParams, signal: Optional[Any] = None
    ) -> Any:
        """Get supported collateral."""
        request = {"method": "supported_collateral", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def instruments(
        self, params: GM.InstrumentsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get all instruments."""
        request = {"method": "instruments", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def ticker(
        self, params: GM.TickerParams, signal: Optional[Any] = None
    ) -> Any:
        """Get ticker for a specific symbol."""
        request = {"method": "ticker", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def orderbook(
        self, params: GM.OrderbookParams, signal: Optional[Any] = None
    ) -> Any:
        """Get orderbook with depth."""
        request = {"method": "orderbook", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def trades(
        self, params: GM.TradesParams, signal: Optional[Any] = None
    ) -> Any:
        """Get recent trades."""
        request = {"method": "trades", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def mids(
        self, params: GM.MidsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get mid prices for all instruments."""
        request = {"method": "mids", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def bbo(
        self, params: GM.BBOParams, signal: Optional[Any] = None
    ) -> Any:
        """Get best bid/offer."""
        request = {"method": "bbo", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def chart(
        self, params: GM.ChartParams, signal: Optional[Any] = None
    ) -> Any:
        """Get chart data (candles or funding)."""
        # Convert from_ to "from" for API
        params_dict = self._to_dict(params)
        if "from_" in params_dict:
            params_dict["from"] = params_dict.pop("from_")
        request = {"method": "chart", "params": params_dict}
        response = self.transport.request("info", request, signal)
        return response
    
    # Account Info Endpoints
    
    def open_orders(
        self, params: AM.OpenOrdersParams, signal: Optional[Any] = None
    ) -> Any:
        """Get open orders."""
        request = {"method": "open_orders", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def positions(
        self, params: AM.PositionsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get current positions."""
        request = {"method": "positions", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # Returns a list of positions
        return response
    
    def account_summary(
        self, params: AM.AccountSummaryParams, signal: Optional[Any] = None
    ) -> Any:
        """Get account summary."""
        request = {"method": "account_summary", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def referral_summary(
        self, params: AM.ReferralSummaryParams, signal: Optional[Any] = None
    ) -> Any:
        """Get referral summary."""
        request = {"method": "referral_summary", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def user_fee_info(
        self, params: AM.UserFeeInfoParams, signal: Optional[Any] = None
    ) -> Any:
        """Get user fee information."""
        request = {"method": "user_fees", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def account_history(
        self, params: AM.AccountHistoryParams, signal: Optional[Any] = None
    ) -> Any:
        """Get account history."""
        request = {"method": "account_history", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def order_history(
        self, params: AM.OrderHistoryParams, signal: Optional[Any] = None
    ) -> Any:
        """Get order history."""
        request = {"method": "order_history", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def fills(
        self, params: AM.FillsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get trade history (fills)."""
        request = {"method": "fills", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def funding_history(
        self, params: AM.FundingHistoryParams, signal: Optional[Any] = None
    ) -> Any:
        """Get funding history."""
        request = {"method": "funding_history", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def transfer_history(
        self, params: AM.TransferHistoryParams, signal: Optional[Any] = None
    ) -> Any:
        """Get transfer history."""
        request = {"method": "transfer_history", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def instrument_leverage(
        self, params: AM.InstrumentLeverageParams, signal: Optional[Any] = None
    ) -> Any:
        """Get instrument leverage settings."""
        request = {"method": "instrument_leverage", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def all_agents(
        self, params: AM.AgentsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get all agents."""
        request = {"method": "all_agents", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def account_info(
        self, params: AM.AccountInfoParams, signal: Optional[Any] = None
    ) -> Any:
        """Get account info."""
        request = {"method": "account_info", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def brokers_check(
        self, params: AM.BrokersCheckParams, signal: Optional[Any] = None
    ) -> Any:
        """Get brokers check."""
        request = {"method": "brokers_check", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
        
    # Vault Info Endpoints
    
    def vaults(
        self, params: VM.VaultsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get all vaults."""
        request = {"method": "vaults", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return response
    
    def sub_vaults(
        self, params: VM.SubVaultsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get sub-vaults for a specific vault."""
        params_dict = self._to_dict(params)
        params_dict.pop("vaultAddress", None)
        request = {"method": "sub_vaults", "params": params_dict}
        response = self.transport.request("info", request, signal)
        return response
    
    def vault_balances(
        self, params: VM.VaultBalancesParams, signal: Optional[Any] = None
    ) -> Any:
        """Get vault balances."""
        params_dict = self._to_dict(params)
        params_dict.pop("vaultAddress", None)
        request = {"method": "vault_balance", "params": params_dict}
        response = self.transport.request("info", request, signal)
        return response
    
    # Explorer Info Endpoints
    
    def blocks(
        self, params: EM.BlocksParams, signal: Optional[Any] = None
    ) -> Any:
        """Get recent blocks."""
        request = {"method": "blocks", "params": self._to_dict(params)}
        response = self.transport.request("explorer", request, signal)
        return response
    
    def block_details(
        self, params: EM.BlockDetailsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get specific block details."""
        request = {"method": "block", "params": self._to_dict(params)}
        response = self.transport.request("explorer", request, signal)
        return response
    
    def transactions(
        self, params: EM.TransactionsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get recent transactions."""
        request = {"method": "transactions", "params": self._to_dict(params)}
        response = self.transport.request("explorer", request, signal)
        return response
    
    def transaction_details(
        self, params: EM.TransactionDetailsParams, signal: Optional[Any] = None
    ) -> Any:
        """Get specific transaction details."""
        request = {"method": "transaction", "params": self._to_dict(params)}
        response = self.transport.request("explorer", request, signal)
        return response
