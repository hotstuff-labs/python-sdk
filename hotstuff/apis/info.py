"""Info API client."""
from typing import Optional, Any, List
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
    ) -> GM.OracleResponse:
        """Get oracle prices."""
        request = {"method": "oracle", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return GM.OracleResponse(**response)
    
    def supported_collateral(
        self, params: GM.SupportedCollateralParams, signal: Optional[Any] = None
    ) -> List[GM.SupportedCollateral]:
        """Get supported collateral."""
        request = {"method": "supportedCollateral", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return [GM.SupportedCollateral(**item) for item in response]
    
    def instruments(
        self, params: GM.InstrumentsParams, signal: Optional[Any] = None
    ) -> GM.InstrumentsResponse:
        """Get all instruments."""
        request = {"method": "instruments", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return GM.InstrumentsResponse(**response)
    
    def ticker(
        self, params: GM.TickerParams, signal: Optional[Any] = None
    ) -> List[GM.Ticker]:
        """Get ticker for a specific symbol."""
        request = {"method": "ticker", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return [GM.Ticker(**item) for item in response]
    
    def orderbook(
        self, params: GM.OrderbookParams, signal: Optional[Any] = None
    ) -> GM.OrderbookResponse:
        """Get orderbook with depth."""
        request = {"method": "orderbook", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return GM.OrderbookResponse(**response)
    
    def trades(
        self, params: GM.TradesParams, signal: Optional[Any] = None
    ) -> List[GM.Trade]:
        """Get recent trades."""
        request = {"method": "trades", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return [GM.Trade(**item) for item in response]
    
    def mids(
        self, params: GM.MidsParams, signal: Optional[Any] = None
    ) -> List[GM.Mid]:
        """Get mid prices for all instruments."""
        request = {"method": "mids", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return [GM.Mid(**item) for item in response]
    
    def bbo(
        self, params: GM.BBOParams, signal: Optional[Any] = None
    ) -> List[GM.BBO]:
        """Get best bid/offer."""
        request = {"method": "bbo", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return [GM.BBO(**item) for item in response]
    
    def chart(
        self, params: GM.ChartParams, signal: Optional[Any] = None
    ) -> List[GM.ChartPoint]:
        """Get chart data (candles or funding)."""
        # Convert from_ to "from" for API
        params_dict = self._to_dict(params)
        if "from_" in params_dict:
            params_dict["from"] = params_dict.pop("from_")
        request = {"method": "chart", "params": params_dict}
        response = self.transport.request("info", request, signal)
        return [GM.ChartPoint(**item) for item in response]
    
    # Account Info Endpoints
    
    def open_orders(
        self, params: AM.OpenOrdersParams, signal: Optional[Any] = None
    ) -> AM.OpenOrdersResponse:
        """Get open orders."""
        request = {"method": "openOrders", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        if isinstance(response, dict) and "data" in response:
            response = {"orders": response["data"]}
        return AM.OpenOrdersResponse(**response)
    
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
    ) -> AM.AccountSummaryResponse:
        """Get account summary."""
        request = {"method": "accountSummary", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return AM.AccountSummaryResponse(**response)
    
    def referral_summary(
        self, params: AM.ReferralSummaryParams, signal: Optional[Any] = None
    ) -> AM.ReferralSummaryResponse:
        """Get referral summary."""
        request = {"method": "referralSummary", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return AM.ReferralSummaryResponse(**response)
    
    def user_fee_info(
        self, params: AM.UserFeeInfoParams, signal: Optional[Any] = None
    ) -> AM.UserFeeInfoResponse:
        """Get user fee information."""
        request = {"method": "userFees", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return AM.UserFeeInfoResponse(**response)
    
    def account_history(
        self, params: AM.AccountHistoryParams, signal: Optional[Any] = None
    ) -> AM.AccountHistoryResponse:
        """Get account history."""
        request = {"method": "accountHistory", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # API returns a list directly
        if isinstance(response, list):
            return [AM.AccountHistory(**item) for item in response]
        return []
    
    def order_history(
        self, params: AM.OrderHistoryParams, signal: Optional[Any] = None
    ) -> AM.OrderHistoryResponse:
        """Get order history."""
        request = {"method": "orderHistory", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # API returns {"data": [...], "page", "limit", "total_count", ...}; map data -> orders
        if isinstance(response, list):
            response = {"orders": response}
        elif isinstance(response, dict) and "data" in response and isinstance(response.get("data"), list):
            response = {**response, "orders": response["data"]}
            del response["data"]
        return AM.OrderHistoryResponse(**response)
    
    def fills(
        self, params: AM.FillsParams, signal: Optional[Any] = None
    ) -> AM.FillsResponse:
        """Get trade history (fills)."""
        request = {"method": "fills", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # API returns {"data": [...], "page", "limit", "total_count", ...}; map data -> entries
        if isinstance(response, list):
            response = {"entries": response}
        elif isinstance(response, dict) and "data" in response and isinstance(response.get("data"), list):
            response = {**response, "entries": response["data"]}
            del response["data"]
        return AM.FillsResponse(**response)
    
    def funding_history(
        self, params: AM.FundingHistoryParams, signal: Optional[Any] = None
    ) -> AM.FundingHistoryResponse:
        """Get funding history."""
        request = {"method": "fundingHistory", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # API returns {"data": [...], "page", "limit", "total_count", ...}; map data -> entries
        if isinstance(response, list):
            response = {"entries": response}
        elif isinstance(response, dict) and "data" in response and isinstance(response.get("data"), list):
            response = {**response, "entries": response["data"]}
            del response["data"]
        return AM.FundingHistoryResponse(**response)
    
    def transfer_history(
        self, params: AM.TransferHistoryParams, signal: Optional[Any] = None
    ) -> AM.TransferHistoryResponse:
        """Get transfer history."""
        request = {"method": "transferHistory", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # API returns a list directly; rename 'from' to 'from_address' (reserved keyword)
        if isinstance(response, list):
            return [AM.TransferHistory(
                from_address=item.get("from", ""),
                to=item.get("to", ""),
                collateral_id=item.get("collateral_id", 0),
                amount=item.get("amount", ""),
                tx_hash=item.get("tx_hash", ""),
                type=item.get("type", "deposit"),
                timestamp=item.get("timestamp", ""),
            ) for item in response]
        return []
    
    def instrument_leverage(
        self, params: AM.InstrumentLeverageParams, signal: Optional[Any] = None
    ) -> AM.InstrumentLeverageResponse:
        """Get instrument leverage settings."""
        request = {"method": "instrumentLeverage", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return AM.InstrumentLeverageResponse(**response)
    
    def agents(
        self, params: AM.AgentsParams, signal: Optional[Any] = None
    ) -> AM.AgentsResponse:
        """Get agents."""
        request = {"method": "allAgents", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        if isinstance(response, list):
            return [AM.Agent(**item) for item in response]
        return AM.AgentsResponse(**response)
    
    def account_info(
        self, params: AM.AccountInfoParams, signal: Optional[Any] = None
    ) -> AM.AccountInfoResponse:
        """Get account info."""
        request = {"method": "accountInfo", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        return AM.AccountInfoResponse(**response)
    
    # Vault Info Endpoints
    
    def vaults(
        self, params: VM.VaultsParams, signal: Optional[Any] = None
    ) -> VM.VaultsResponse:
        """Get all vaults."""
        request = {"method": "vaults", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # Parse nested vault objects
        vaults_list = response.get("vaults", []) if isinstance(response, dict) else []
        return VM.VaultsResponse(vaults=[VM.Vault(**v) for v in vaults_list])
    
    def sub_vaults(
        self, params: VM.SubVaultsParams, signal: Optional[Any] = None
    ) -> VM.SubVaultsResponse:
        """Get sub-vaults for a specific vault."""
        request = {"method": "subVaults", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # API returns a list directly
        if isinstance(response, list):
            return [VM.SubVault(**item) for item in response]
        return []
    
    def vault_balances(
        self, params: VM.VaultBalancesParams, signal: Optional[Any] = None
    ) -> VM.VaultBalancesResponse:
        """Get vault balances."""
        request = {"method": "vaultBalance", "params": self._to_dict(params)}
        response = self.transport.request("info", request, signal)
        # API returns single VaultBalance if user is passed, List[VaultBalance] otherwise
        if isinstance(response, list):
            return [VM.VaultBalance(**item) for item in response]
        elif isinstance(response, dict):
            return VM.VaultBalance(**response)
        return []
    
    # Explorer Info Endpoints
    
    def blocks(
        self, params: EM.BlocksParams, signal: Optional[Any] = None
    ) -> EM.BlocksResponse:
        """Get recent blocks."""
        request = {"method": "blocks", "params": self._to_dict(params)}
        response = self.transport.request("explorer", request, signal)
        return EM.BlocksResponse(**response)
    
    def block_details(
        self, params: EM.BlockDetailsParams, signal: Optional[Any] = None
    ) -> EM.BlockDetailsResponse:
        """Get specific block details."""
        request = {"method": "block", "params": self._to_dict(params)}
        response = self.transport.request("explorer", request, signal)
        # Parse nested transactions
        transactions = [EM.BlockTransaction(**tx) for tx in response.get("transactions", [])]
        return EM.BlockDetailsResponse(
            block_height=response.get("block_height", 0),
            block_hash=response.get("block_hash", ""),
            parent_hash=response.get("parent_hash", ""),
            change_log_hash=response.get("change_log_hash", ""),
            timestamp=response.get("timestamp", 0),
            tx_count=response.get("tx_count", 0),
            created_at=response.get("created_at", 0),
            transactions=transactions,
        )
    
    def transactions(
        self, params: EM.TransactionsParams, signal: Optional[Any] = None
    ) -> EM.TransactionsResponse:
        """Get recent transactions."""
        request = {"method": "transactions", "params": self._to_dict(params)}
        response = self.transport.request("explorer", request, signal)
        return EM.TransactionsResponse(**response)
    
    def transaction_details(
        self, params: EM.TransactionDetailsParams, signal: Optional[Any] = None
    ) -> EM.TransactionDetailsResponse:
        """Get specific transaction details."""
        request = {"method": "transaction", "params": self._to_dict(params)}
        response = self.transport.request("explorer", request, signal)
        return EM.TransactionDetailsResponse(**response)
