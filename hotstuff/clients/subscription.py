"""Subscription API client for real-time data."""
from typing import Callable, Dict, Any


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
        params: Dict[str, Any],
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
        return await self.transport.subscribe("ticker", params, listener)
    
    async def mids(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("mids", params, listener)
    
    async def bbo(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("bbo", params, listener)
    
    async def orderbook(
        self,
        params: Dict[str, Any],
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to orderbook updates.
        
        Args:
            params: Subscription parameters (symbol)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("orderbook", params, listener)
    
    async def trade(
        self,
        params: Dict[str, Any],
        listener: Callable
    ) -> Dict[str, Any]:
        """
        Subscribe to trades.
        
        Args:
            params: Subscription parameters (symbol)
            listener: Callback function for updates
            
        Returns:
            Subscription object with unsubscribe method
        """
        return await self.transport.subscribe("trade", params, listener)
    
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
        params: Dict[str, Any],
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
        return await self.transport.subscribe("chart", params, listener)
    
    # Account Subscriptions
    
    async def account_order_updates(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("accountOrderUpdates", params, listener)
    
    async def account_balance_updates(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("accountBalanceUpdates", params, listener)
    
    async def positions(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("positions", params, listener)
    
    async def fills(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("fills", params, listener)
    
    async def account_summary(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("accountSummary", params, listener)
    
    # Explorer Subscriptions
    
    async def blocks(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("blocks", params, listener)
    
    async def transactions(
        self,
        params: Dict[str, Any],
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
        return await self.transport.subscribe("transactions", params, listener)

