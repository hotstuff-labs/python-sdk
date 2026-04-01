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


from examples.utils.config import CREDENTIALS, CONFIG

def setup_info_client():
    info = InfoClient(
        websocket=CONFIG["IS_WEBSOCKET"],
        is_testnet=CONFIG["IS_TESTNET"],
    )
    http_transport = info.transport if not CONFIG["IS_WEBSOCKET"] else None
    ws_transport = info.transport if CONFIG["IS_WEBSOCKET"] else None
    return info, http_transport, ws_transport, None

def setup_exchange_client():
    account = Account.from_key(CREDENTIALS["MAIN_ACCOUNT_PRIVATE_KEY"])
    exchange = ExchangeClient(
        wallet=account,
        websocket=CONFIG["IS_WEBSOCKET"],
        is_testnet=CONFIG["IS_TESTNET"],
    )
    http_transport = exchange.transport if not CONFIG["IS_WEBSOCKET"] else None
    ws_transport = exchange.transport if CONFIG["IS_WEBSOCKET"] else None
    return exchange, http_transport, ws_transport, account

def setup_trading_client():
    account = Account.from_key(CREDENTIALS["AGENT_PRIVATE_KEY"])
    exchange = ExchangeClient(
        wallet=account,
        websocket=CONFIG["IS_WEBSOCKET"],
        is_testnet=CONFIG["IS_TESTNET"],
    )
    http_transport = exchange.transport if not CONFIG["IS_WEBSOCKET"] else None
    ws_transport = exchange.transport if CONFIG["IS_WEBSOCKET"] else None
    return exchange, http_transport, ws_transport, account

def setup_subscription_client():
    ws_transport = WebSocketTransport(WebSocketTransportOptions(is_testnet=CONFIG["IS_TESTNET"], auto_connect=True))
    subscriptions = SubscriptionClient(transport=ws_transport)
    return subscriptions, ws_transport
   
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

