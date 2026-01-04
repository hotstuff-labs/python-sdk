"""Exchange API client for trading operations."""
from typing import Optional, Any, Dict, Callable, Awaitable
from eth_account import Account

from hotstuff.utils import sign_action, EXCHANGE_OP_CODES, NonceManager
from hotstuff.types import (
    PlaceOrderParams,
    CancelByOidParams,
    CancelByCloidParams,
    CancelAllParams,
    AddAgentParams,
)


class ExchangeClient:
    """Client for executing trading actions and account management."""
    
    def __init__(
        self,
        transport,
        wallet: Account,
        nonce: Optional[Callable[[], Awaitable[int]]] = None
    ):
        """
        Initialize ExchangeClient.
        
        Args:
            transport: The transport layer to use
            wallet: The wallet/account for signing
            nonce: Optional nonce generator function
        """
        self.transport = transport
        self.wallet = wallet
        self.nonce = nonce or NonceManager().get_nonce
    
    # Account Actions
    
    async def add_agent(
        self,
        params: Dict[str, Any],
        execute: bool = True,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Add an agent.
        
        Args:
            params: Agent parameters
            execute: Whether to execute the action
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        nonce = await self.nonce()
        
        # Create agent account from private key
        agent_account = Account.from_key(params["agent_private_key"])
        
        # Sign with agent account
        agent_signature = await sign_action(
            wallet=agent_account,
            action={
                "signer": params["signer"],
                "nonce": nonce,
            },
            tx_type=EXCHANGE_OP_CODES["addAgent"],
        )
        
        params = {
            "agentName": params["agent_name"],
            "agent": params["agent"],
            "forAccount": params["for_account"],
            "signature": agent_signature,
            "validUntil": params["valid_until"],
            "nonce": nonce,
        }
        
        return await self._execute_action(
            {"action": "addAgent", "params": params},
            signal,
            execute
        )
    
    # Trading Actions
    
    async def place_order(
        self,
        params: Dict[str, Any],
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Place order(s).
        
        Args:
            params: Order parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        return await self._execute_action(
            {"action": "placeOrder", "params": params},
            signal
        )
    
    async def cancel_by_oid(
        self,
        params: Dict[str, Any],
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Cancel order by order ID.
        
        Args:
            params: Cancel parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        return await self._execute_action(
            {"action": "cancelByOid", "params": params},
            signal
        )
    
    async def cancel_by_cloid(
        self,
        params: Dict[str, Any],
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Cancel order by client order ID.
        
        Args:
            params: Cancel parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        return await self._execute_action(
            {"action": "cancelByCloid", "params": params},
            signal
        )
    
    async def cancel_all(
        self,
        params: Dict[str, Any],
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Cancel all orders.
        
        Args:
            params: Cancel parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        return await self._execute_action(
            {"action": "cancelAll", "params": params},
            signal
        )
    
    # Private Methods
    
    async def _execute_action(
        self,
        request: Dict[str, Any],
        signal: Optional[Any] = None,
        execute: bool = True
    ) -> Dict[str, Any]:
        """
        Execute an action.
        
        Args:
            request: Action request
            signal: Optional abort signal
            execute: Whether to execute the action
            
        Returns:
            Response or signature data
        """
        action = request["action"]
        params = request["params"]
        
        # Set nonce if not present
        if "nonce" not in params or params["nonce"] is None:
            params["nonce"] = await self.nonce()
        
        # Sign the action
        signature = await sign_action(
            wallet=self.wallet,
            action=params,
            tx_type=EXCHANGE_OP_CODES[action],
            is_testnet=True,
        )
        
        if execute:
            # Send to server
            response = await self.transport.request(
                "exchange",
                {
                    "action": {
                        "data": params,
                        "type": str(EXCHANGE_OP_CODES[action]),
                    },
                    "signature": signature,
                    "nonce": params["nonce"],
                },
                signal,
            )
            return response
        
        return {"params": params, "signature": signature}

