import os
import time
from typing import Any, Callable, Dict, List
from hotstuff import (
    ExchangeClient,
    InfoClient,
    SubscriptionClient,
    WebSocketTransport,
    WebSocketTransportOptions,
)
from eth_account import Account

def setup_clients(is_testnet: bool = True, is_websocket: bool = False, main_account: bool = True):


    account = Account.from_key(os.getenv("PRIVATE_KEY") if main_account else os.getenv("AGENT_PRIVATE_KEY"))

    info = InfoClient(websocket=is_websocket, is_testnet=is_testnet)
    
    exchange = ExchangeClient(websocket=is_websocket, is_testnet=is_testnet, wallet=account)
        
    return info, exchange
  

    
def setup_subscription_client(
    is_testnet: bool = True,
):
    """Create a subscription client backed by WebSocket transport."""
    transport = WebSocketTransport(WebSocketTransportOptions(is_testnet=is_testnet))
    subscription = SubscriptionClient(transport=transport)
    return subscription, transport


def build_listener(channel_name: str) -> Callable[[Any], None]:
    """Create a simple listener that prints incoming updates."""

    def _listener(message: Any) -> None:
        print(f"[{channel_name}] {message}")

    return _listener


def wait_for_updates(seconds: int = 20) -> None:
    """Block and wait while updates are received."""
    print(f"Listening for {seconds} seconds. Press Ctrl+C to stop early.")
    time.sleep(seconds)


def cleanup_subscriptions(
    active_subscriptions: List[Dict[str, Any]],
    transport: WebSocketTransport,
) -> None:
    """Unsubscribe all active subscriptions and close transport."""
    for subscription in active_subscriptions:
        unsubscribe = subscription.get("unsubscribe")
        if not callable(unsubscribe):
            continue

        try:
            unsubscribe()
        except Exception as exc:
            print(f"Failed to unsubscribe cleanly: {exc}")

    transport.disconnect()

