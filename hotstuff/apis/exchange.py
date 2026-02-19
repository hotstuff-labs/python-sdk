"""Exchange API client for trading operations."""
from typing import Optional, Any, Dict, Callable
from dataclasses import asdict
from eth_account import Account

from hotstuff.utils import sign_action, NonceManager
from hotstuff.methods.exchange import (
    trading as TM,
    account as AM,
    collateral as CM,
    vault as VM,
)
from hotstuff.methods.exchange.op_codes import EXCHANGE_OP_CODES


class ExchangeClient:
    """Client for executing trading actions and account management."""
    
    def __init__(
        self,
        transport,
        wallet: Account,
        nonce: Optional[Callable[[], int]] = None
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
    
    def add_agent(
        self,
        params: AM.AddAgentParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Add an agent.
        
        Args:
            params: Agent parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        nonce = self.nonce()
        
        # Create agent account from private key
        agent_account = Account.from_key(params.agent_private_key)
        
        # Sign with agent account
        agent_signature = sign_action(
            wallet=agent_account,
            action={
                "signer": params.signer,
                "nonce": nonce,
            },
            tx_type=EXCHANGE_OP_CODES["addAgent"],
            is_testnet=self.transport.is_testnet,
        )
        
        # Prepare params for API
        params_dict = {
            "agentName": params.agent_name,
            "agent": params.agent,
            "forAccount": params.for_account if params.for_account else "",
            "signature": agent_signature,
            "validUntil": params.valid_until,
            "nonce": nonce,
        }
        
        return self._execute_action(
            {"action": "addAgent", "params": params_dict},
            signal
        )

    def revoke_agent(
        self,
        params: AM.RevokeAgentParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Revoke an agent.
        
        Args:
            params: Revoke agent parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "revokeAgent", "params": params_dict},
            signal
        )

    def update_perp_instrument_leverage(
        self,
        params: AM.UpdatePerpInstrumentLeverageParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Update perp instrument leverage.
        
        Args:
            params: Update leverage parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "updatePerpInstrumentLeverage", "params": params_dict},
            signal
        )

    def approve_broker_fee(
        self,
        params: AM.ApproveBrokerFeeParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Approve broker fee.
        
        Args:
            params: Approve broker fee parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "approveBrokerFee", "params": params_dict},
            signal
        )

    def create_referral_code(
        self,
        params: AM.CreateReferralCodeParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Create a referral code.
        
        Args:
            params: Create referral code parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "createReferralCode", "params": params_dict},
            signal
        )

    def set_referrer(
        self,
        params: AM.SetReferrerParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Set a referrer.
        
        Args:
            params: Set referrer parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "setReferrer", "params": params_dict},
            signal
        )

    def claim_referral_rewards(
        self,
        params: AM.ClaimReferralRewardsParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Claim referral rewards.
        
        Args:
            params: Claim referral rewards parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "claimReferralRewards", "params": params_dict},
            signal
        )
    
    # Trading Actions
    
    def place_order(
        self,
        params: TM.PlaceOrderParams,
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
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        ordered_params = {
            "orders": params_dict["orders"],
            "brokerConfig": params_dict.get("broker_config"),
            "expiresAfter": params_dict["expires_after"],
        }
        if ordered_params["brokerConfig"] is None:
            ordered_params.pop("brokerConfig")
        return self._execute_action(
            {"action": "placeOrder", "params": ordered_params},
            signal
        )
    
    def cancel_by_oid(
        self,
        params: TM.CancelByOidParams,
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
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "cancelByOid", "params": params_dict},
            signal
        )
    
    def cancel_by_cloid(
        self,
        params: TM.CancelByCloidParams,
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
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "cancelByCloid", "params": params_dict},
            signal
        )
    
    def cancel_all(
        self,
        params: TM.CancelAllParams,
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
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "cancelAll", "params": params_dict},
            signal
        )

    # Collateral Transfer Methods

    def account_spot_withdraw_request(
        self,
        params: CM.AccountSpotWithdrawRequestParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Request spot account withdrawal.
        
        Args:
            params: Spot withdraw request parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "accountSpotWithdrawRequest", "params": params_dict},
            signal
        )

    def account_derivative_withdraw_request(
        self,
        params: CM.AccountDerivativeWithdrawRequestParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Request derivative account withdrawal.
        
        Args:
            params: Derivative withdraw request parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "accountDerivativeWithdrawRequest", "params": params_dict},
            signal
        )

    def account_spot_balance_transfer_request(
        self,
        params: CM.AccountSpotBalanceTransferRequestParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Request spot balance transfer.
        
        Args:
            params: Spot balance transfer request parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "accountSpotBalanceTransferRequest", "params": params_dict},
            signal
        )

    def account_derivative_balance_transfer_request(
        self,
        params: CM.AccountDerivativeBalanceTransferRequestParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Request derivative balance transfer.
        
        Args:
            params: Derivative balance transfer request parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "accountDerivativeBalanceTransferRequest", "params": params_dict},
            signal
        )

    def account_internal_balance_transfer_request(
        self,
        params: CM.AccountInternalBalanceTransferRequestParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Request internal balance transfer between spot and derivative accounts.
        
        Args:
            params: Internal balance transfer request parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "accountInternalBalanceTransferRequest", "params": params_dict},
            signal
        )

    # Vault Methods

    def deposit_to_vault(
        self,
        params: VM.DepositToVaultParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Deposit to a vault.
        
        Args:
            params: Deposit to vault parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "depositToVault", "params": params_dict},
            signal
        )

    def redeem_from_vault(
        self,
        params: VM.RedeemFromVaultParams,
        signal: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Redeem from a vault.
        
        Args:
            params: Redeem from vault parameters
            signal: Optional abort signal
            
        Returns:
            Response from the server
        """
        params_dict = self._to_api_dict(params, exclude={"nonce"})
        return self._execute_action(
            {"action": "redeemFromVault", "params": params_dict},
            signal
        )
    
    # Private Methods
    
    def _to_api_dict(self, obj, exclude=None) -> Dict[str, Any]:
        """Convert dataclass to dict, excluding specified fields."""
        exclude = exclude or set()
        result = {}
        for key, value in asdict(obj).items():
            if key not in exclude:
                # Handle nested dataclasses (lists of dataclasses)
                if isinstance(value, list):
                    result[key] = [
                        asdict(item) if hasattr(item, '__dataclass_fields__') else item
                        for item in value
                    ]
                else:
                    result[key] = value
        return result
    
    def _execute_action(
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
            params["nonce"] = self.nonce()
        
        # Sign the action
        signature = sign_action(
            wallet=self.wallet,
            action=params,
            tx_type=EXCHANGE_OP_CODES[action],
            is_testnet=self.transport.is_testnet,
        )
        
        if execute:
            # Send to server
            response = self.transport.request(
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
