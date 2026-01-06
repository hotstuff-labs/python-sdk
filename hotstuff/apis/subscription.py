"""Subscription API client for real-time data."""
from typing import Callable, Dict, Any
import importlib

SM = importlib.import_module("hotstuff.methods.subscription.global")


class SubscriptionClient:
    """Client for subscribing to real-time data streams."""
    
    def __init__(self, transport):
        """
        Initialize SubscriptionClient.
        
        Args:
            transport: The WebSocket transport layer to use
        """
        self.transport = transport
    
    # Market Subscriptions
    
    async def ticker(
        self,
        params: SM.TickerSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to ticker updates.
        
        Args:
            params: Subscription parameters (symbol)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("ticker", params.model_dump(), listener)
    
    async def mids(
        self,
        params: SM.MidsSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to mid prices.
        
        Args:
            params: Subscription parameters (symbol)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("mids", params.model_dump(), listener)
    
    async def bbo(
        self,
        params: SM.BBOSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to best bid/offer.
        
        Args:
            params: Subscription parameters (symbol)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("bbo", params.model_dump(), listener)
    
    async def orderbook(
        self,
        params: SM.OrderbookSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to orderbook updates.
        
        Args:
            params: Subscription parameters (instrument_id)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        # Convert to format expected by API (both instrumentId and symbol)
        params_dict = params.model_dump()
        params_dict["symbol"] = params_dict["instrument_id"]
        return await self.transport.subscribe("orderbook", params_dict, listener)
    
    async def trade(
        self,
        params: SM.TradeSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to trades.
        
        Args:
            params: Subscription parameters (instrument_id)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        # Convert to format expected by API (both instrumentId and symbol)
        params_dict = params.model_dump()
        params_dict["symbol"] = params_dict["instrument_id"]
        return await self.transport.subscribe("trade", params_dict, listener)
    
    async def index(
        self,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to index prices.
        
        Args:
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("index", {}, listener)
    
    async def chart(
        self,
        params: SM.ChartSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to chart updates.
        
        Args:
            params: Subscription parameters (symbol, chart_type, resolution)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("chart", params.model_dump(), listener)
    
    # Account Subscriptions
    
    async def account_order_updates(
        self,
        params: SM.AccountOrderUpdatesParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to order updates.
        
        Args:
            params: Subscription parameters (address)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        # Convert to format expected by API (both address and user)
        params_dict = params.model_dump()
        params_dict["user"] = params_dict["address"]
        return await self.transport.subscribe("accountOrderUpdates", params_dict, listener)
    
    async def account_balance_updates(
        self,
        params: SM.AccountBalanceUpdatesParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to balance updates.
        
        Args:
            params: Subscription parameters (address)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        # Convert to format expected by API (both address and user)
        params_dict = params.model_dump()
        params_dict["user"] = params_dict["address"]
        return await self.transport.subscribe("accountBalanceUpdates", params_dict, listener)
    
    async def positions(
        self,
        params: SM.PositionsSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to position updates.
        
        Args:
            params: Subscription parameters (address)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        # Convert to format expected by API (both address and user)
        params_dict = params.model_dump()
        params_dict["user"] = params_dict["address"]
        return await self.transport.subscribe("positions", params_dict, listener)
    
    async def fills(
        self,
        params: SM.FillsSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to fills.
        
        Args:
            params: Subscription parameters (address)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        # Convert to format expected by API (both address and user)
        params_dict = params.model_dump()
        params_dict["user"] = params_dict["address"]
        return await self.transport.subscribe("fills", params_dict, listener)
    
    async def account_summary(
        self,
        params: SM.AccountSummarySubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to account summary.
        
        Args:
            params: Subscription parameters (user)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("accountSummary", params.model_dump(), listener)
    
    # Explorer Subscriptions
    
    async def blocks(
        self,
        params: SM.BlocksSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to new blocks.
        
        Args:
            params: Subscription parameters
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("blocks", params.model_dump(), listener)
    
    async def transactions(
        self,
        params: SM.TransactionsSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to new transactions.
        
        Args:
            params: Subscription parameters
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("transactions", params.model_dump(), listener)
