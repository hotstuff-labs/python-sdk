"""Info API client."""
from typing import Optional, Any, List
import importlib

GM = importlib.import_module("hotstuff.methods.info.global")
AM = importlib.import_module("hotstuff.methods.info.account")
VM = importlib.import_module("hotstuff.methods.info.vault")
EM = importlib.import_module("hotstuff.methods.info.explorer")


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
    
    async def oracle(
        self, params: GM.OracleParams, signal: Optional[Any] = None
    ) -> GM.OracleResponse:
        """Get oracle prices."""
        request = {"method": "oracle", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return GM.OracleResponse.model_validate(response)
    
    async def supported_collateral(
        self, params: GM.SupportedCollateralParams, signal: Optional[Any] = None
    ) -> List[GM.SupportedCollateral]:
        """Get supported collateral."""
        request = {"method": "supportedCollateral", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return [GM.SupportedCollateral.model_validate(item) for item in response]
    
    async def instruments(
        self, params: GM.InstrumentsParams, signal: Optional[Any] = None
    ) -> GM.InstrumentsResponse:
        """Get all instruments."""
        request = {"method": "instruments", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return GM.InstrumentsResponse.model_validate(response)
    
    async def ticker(
        self, params: GM.TickerParams, signal: Optional[Any] = None
    ) -> List[GM.Ticker]:
        """Get ticker for a specific symbol."""
        request = {"method": "ticker", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return [GM.Ticker.model_validate(item) for item in response]
    
    async def orderbook(
        self, params: GM.OrderbookParams, signal: Optional[Any] = None
    ) -> GM.OrderbookResponse:
        """Get orderbook with depth."""
        request = {"method": "orderbook", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return GM.OrderbookResponse.model_validate(response)
    
    async def trades(
        self, params: GM.TradesParams, signal: Optional[Any] = None
    ) -> List[GM.Trade]:
        """Get recent trades."""
        request = {"method": "trades", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return [GM.Trade.model_validate(item) for item in response]
    
    async def mids(
        self, params: GM.MidsParams, signal: Optional[Any] = None
    ) -> List[GM.Mid]:
        """Get mid prices for all instruments."""
        request = {"method": "mids", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return [GM.Mid.model_validate(item) for item in response]
    
    async def bbo(
        self, params: GM.BBOParams, signal: Optional[Any] = None
    ) -> List[GM.BBO]:
        """Get best bid/offer."""
        request = {"method": "bbo", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return [GM.BBO.model_validate(item) for item in response]
    
    async def chart(
        self, params: GM.ChartParams, signal: Optional[Any] = None
    ) -> List[GM.ChartPoint]:
        """Get chart data (candles or funding)."""
        # Convert from_ to "from" for API
        params_dict = params.model_dump(by_alias=True)
        request = {"method": "chart", "params": params_dict}
        response = await self.transport.request("info", request, signal)
        return [GM.ChartPoint.model_validate(item) for item in response]
    
    # Account Info Endpoints
    
    async def open_orders(
        self, params: AM.OpenOrdersParams, signal: Optional[Any] = None
    ) -> AM.OpenOrdersResponse:
        """Get open orders."""
        request = {"method": "openOrders", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.OpenOrdersResponse.model_validate(response)
    
    async def positions(
        self, params: AM.PositionsParams, signal: Optional[Any] = None
    ) -> AM.PositionsResponse:
        """Get current positions."""
        request = {"method": "positions", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.PositionsResponse.model_validate(response)
    
    async def account_summary(
        self, params: AM.AccountSummaryParams, signal: Optional[Any] = None
    ) -> AM.AccountSummaryResponse:
        """Get account summary."""
        request = {"method": "accountSummary", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.AccountSummaryResponse.model_validate(response)
    
    async def referral_summary(
        self, params: AM.ReferralSummaryParams, signal: Optional[Any] = None
    ) -> AM.ReferralSummaryResponse:
        """Get referral summary."""
        request = {"method": "referralSummary", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.ReferralSummaryResponse.model_validate(response)
    
    async def user_fee_info(
        self, params: AM.UserFeeInfoParams, signal: Optional[Any] = None
    ) -> AM.UserFeeInfoResponse:
        """Get user fee information."""
        request = {"method": "userFees", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.UserFeeInfoResponse.model_validate(response)
    
    async def account_history(
        self, params: AM.AccountHistoryParams, signal: Optional[Any] = None
    ) -> AM.AccountHistoryResponse:
        """Get account history."""
        request = {"method": "accountHistory", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.AccountHistoryResponse.model_validate(response)
    
    async def order_history(
        self, params: AM.OrderHistoryParams, signal: Optional[Any] = None
    ) -> AM.OrderHistoryResponse:
        """Get order history."""
        request = {"method": "orderHistory", "params": params.model_dump(by_alias=True)}
        response = await self.transport.request("info", request, signal)
        return AM.OrderHistoryResponse.model_validate(response)
    
    async def trade_history(
        self, params: AM.TradeHistoryParams, signal: Optional[Any] = None
    ) -> AM.TradeHistoryResponse:
        """Get trade history (fills)."""
        request = {"method": "fills", "params": params.model_dump(by_alias=True)}
        response = await self.transport.request("info", request, signal)
        return AM.TradeHistoryResponse.model_validate(response)
    
    async def funding_history(
        self, params: AM.FundingHistoryParams, signal: Optional[Any] = None
    ) -> AM.FundingHistoryResponse:
        """Get funding history."""
        request = {"method": "fundingHistory", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.FundingHistoryResponse.model_validate(response)
    
    async def transfer_history(
        self, params: AM.TransferHistoryParams, signal: Optional[Any] = None
    ) -> AM.TransferHistoryResponse:
        """Get transfer history."""
        request = {"method": "transferHistory", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.TransferHistoryResponse.model_validate(response)
    
    async def instrument_leverage(
        self, params: AM.InstrumentLeverageParams, signal: Optional[Any] = None
    ) -> AM.InstrumentLeverageResponse:
        """Get instrument leverage settings."""
        request = {"method": "instrumentLeverage", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.InstrumentLeverageResponse.model_validate(response)
    
    async def get_referral_info(
        self, params: AM.ReferralInfoParams, signal: Optional[Any] = None
    ) -> AM.ReferralInfoResponse:
        """Get referral info."""
        request = {"method": "referralInfo", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.ReferralInfoResponse.model_validate(response)
    
    async def sub_accounts_list(
        self, params: AM.SubAccountsListParams, signal: Optional[Any] = None
    ) -> AM.SubAccountsListResponse:
        """Get sub-accounts list."""
        request = {"method": "subAccountsList", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.SubAccountsListResponse.model_validate(response)
    
    async def agents(
        self, params: AM.AgentsParams, signal: Optional[Any] = None
    ) -> AM.AgentsResponse:
        """Get agents."""
        request = {"method": "allAgents", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.AgentsResponse.model_validate(response)
    
    async def user_balance(
        self, params: AM.UserBalanceInfoParams, signal: Optional[Any] = None
    ) -> AM.UserBalanceInfoResponse:
        """Get user balance."""
        request = {"method": "userBalance", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return AM.UserBalanceInfoResponse.model_validate(response)
    
    async def account_info(
        self, params: AM.AccountInfoParams, signal: Optional[Any] = None
    ) -> AM.AccountInfoResponse:
        """Get account info."""
        request = {"method": "accountInfo", "params": params.model_dump(by_alias=True)}
        response = await self.transport.request("info", request, signal)
        return AM.AccountInfoResponse.model_validate(response)
    
    # Vault Info Endpoints
    
    async def vaults(
        self, params: VM.VaultsParams, signal: Optional[Any] = None
    ) -> VM.VaultsResponse:
        """Get all vaults."""
        request = {"method": "vaults", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return VM.VaultsResponse.model_validate(response)
    
    async def sub_vaults(
        self, params: VM.SubVaultsParams, signal: Optional[Any] = None
    ) -> VM.SubVaultsResponse:
        """Get sub-vaults for a specific vault."""
        request = {"method": "subVaults", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return VM.SubVaultsResponse.model_validate(response)
    
    async def vault_balances(
        self, params: VM.VaultBalancesParams, signal: Optional[Any] = None
    ) -> VM.VaultBalancesResponse:
        """Get vault balances."""
        request = {"method": "vaultBalance", "params": params.model_dump()}
        response = await self.transport.request("info", request, signal)
        return VM.VaultBalancesResponse.model_validate(response)
    
    # Explorer Info Endpoints
    
    async def blocks(
        self, params: EM.BlocksParams, signal: Optional[Any] = None
    ) -> EM.BlocksResponse:
        """Get recent blocks."""
        request = {"method": "blocks", "params": params.model_dump()}
        response = await self.transport.request("explorer", request, signal)
        return EM.BlocksResponse.model_validate(response)
    
    async def block_details(
        self, params: EM.BlockDetailsParams, signal: Optional[Any] = None
    ) -> EM.BlockDetailsResponse:
        """Get specific block details."""
        request = {"method": "block", "params": params.model_dump()}
        response = await self.transport.request("explorer", request, signal)
        return EM.BlockDetailsResponse.model_validate(response)
    
    async def transactions(
        self, params: EM.TransactionsParams, signal: Optional[Any] = None
    ) -> EM.TransactionsResponse:
        """Get recent transactions."""
        request = {"method": "transactions", "params": params.model_dump()}
        response = await self.transport.request("explorer", request, signal)
        return EM.TransactionsResponse.model_validate(response)
    
    async def transaction_details(
        self, params: EM.TransactionDetailsParams, signal: Optional[Any] = None
    ) -> EM.TransactionDetailsResponse:
        """Get specific transaction details."""
        request = {"method": "transaction", "params": params.model_dump()}
        response = await self.transport.request("explorer", request, signal)
        return EM.TransactionDetailsResponse.model_validate(response)
