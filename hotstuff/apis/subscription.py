"""Subscription API client for real-time data."""
from typing import Callable, Dict, Any
from dataclasses import asdict

from hotstuff.methods.subscription import channels as SM


class SubscriptionClient:
    """Client for subscribing to real-time data streams."""
    
    def __init__(self, transport):
        """
        Initialize SubscriptionClient.
        
        Args:
            transport: The WebSocket transport layer to use
        """
        self.transport = transport
    
    def _to_dict(self, obj) -> dict:
        """Convert dataclass to dict."""
        return asdict(obj)
    
    # Market Subscriptions
    
    def ticker(
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
        return self.transport.subscribe("ticker", self._to_dict(params), listener)
    
    def mids(
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
        return self.transport.subscribe("mids", self._to_dict(params), listener)
    
    def bbo(
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
        return self.transport.subscribe("bbo", self._to_dict(params), listener)
    
    def orderbook(
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
        params_dict = self._to_dict(params)
        params_dict["symbol"] = params_dict["instrument_id"]
        return self.transport.subscribe("orderbook", params_dict, listener)
    
    def trade(
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
        params_dict = self._to_dict(params)
        params_dict["symbol"] = params_dict["instrument_id"]
        return self.transport.subscribe("trade", params_dict, listener)
    
    def index(
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
        return self.transport.subscribe("index", {}, listener)
    
    def chart(
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
        return self.transport.subscribe("chart", self._to_dict(params), listener)
    
    # Account Subscriptions
    
    def account_order_updates(
        self,
        params: SM.AccountOrderUpdatesParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to order updates.
        
        Args:
            params: Subscription parameters (user address)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return self.transport.subscribe("accountOrderUpdates", self._to_dict(params), listener)
    
    def account_balance_updates(
        self,
        params: SM.AccountBalanceUpdatesParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to balance updates.
        
        Args:
            params: Subscription parameters (user address)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return self.transport.subscribe("accountBalanceUpdates", self._to_dict(params), listener)
    
    def positions(
        self,
        params: SM.PositionsSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to position updates.
        
        Args:
            params: Subscription parameters (user address)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return self.transport.subscribe("positions", self._to_dict(params), listener)
    
    def fills(
        self,
        params: SM.FillsSubscriptionParams,
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to fills.
        
        Args:
            params: Subscription parameters (user address)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return self.transport.subscribe("fills", self._to_dict(params), listener)
    
    def account_summary(
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
        return self.transport.subscribe("accountSummary", self._to_dict(params), listener)
    
    # Explorer Subscriptions
    
    def blocks(
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
        return self.transport.subscribe("blocks", self._to_dict(params), listener)
    
    def transactions(
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
        return self.transport.subscribe("transactions", self._to_dict(params), listener)
