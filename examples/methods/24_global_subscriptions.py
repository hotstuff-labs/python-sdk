"""Example: Global subscriptions."""
from examples.utils.example_utils import setup_subscription_client
from examples.utils.example_utils import build_listener, wait_for_updates, cleanup_subscriptions
from hotstuff import (
    OrderbookSubscriptionParams,
    TickerSubscriptionParams,
    TradeSubscriptionParams,
)

def main():
    """Main example function."""
    print("--------------------------------\nGlobal subscriptions\n")
    subscriptions, transport = setup_subscription_client()
    active_subscriptions = []

    try:
        print("Subscribing to ticker...")
        ticker_subscription = subscriptions.ticker(
            TickerSubscriptionParams(symbol="BTC-PERP"),
            build_listener("ticker"),
        )
        active_subscriptions.append(ticker_subscription)
        print(f"Ticker subscription: {ticker_subscription}\n")

        print("Subscribing to orderbook...")
        orderbook_subscription = subscriptions.orderbook(
            OrderbookSubscriptionParams(symbol="BTC-PERP"),
            build_listener("orderbook"),
        )
        active_subscriptions.append(orderbook_subscription)
        print(f"Orderbook subscription: {orderbook_subscription}\n")

        print("Subscribing to trades...")
        trades_subscription = subscriptions.trades(
            TradeSubscriptionParams(symbol="BTC-PERP"),
            build_listener("trades"),
        )
        active_subscriptions.append(trades_subscription)
        print(f"Trades subscription: {trades_subscription}\n")

        print("Subscribing to index...")
        index_subscription = subscriptions.index(build_listener("index"))
        active_subscriptions.append(index_subscription)
        print(f"Index subscription: {index_subscription}\n")

        wait_for_updates(seconds=20)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        print("Cleaning up subscriptions...")
        cleanup_subscriptions(active_subscriptions, transport)


if __name__ == "__main__":
    main()
