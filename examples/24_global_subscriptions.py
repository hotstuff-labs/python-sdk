"""Example: Global subscriptions."""
import example_utils

from hotstuff import (
    OrderbookSubscriptionParams,
    TickerSubscriptionParams,
    TradeSubscriptionParams,
)

def main():
    """Main example function."""
    print("--------------------------------\nGlobal subscriptions\n")
    subscriptions, transport = example_utils.setup_subscription_client(is_testnet=False)
    active_subscriptions = []

    try:
        print("Subscribing to ticker...")
        ticker_subscription = subscriptions.ticker(
            TickerSubscriptionParams(symbol="BTC-PERP"),
            example_utils.build_listener("ticker"),
        )
        active_subscriptions.append(ticker_subscription)
        print(f"Ticker subscription: {ticker_subscription}\n")

        print("Subscribing to orderbook...")
        orderbook_subscription = subscriptions.orderbook(
            OrderbookSubscriptionParams(symbol="BTC-PERP"),
            example_utils.build_listener("orderbook"),
        )
        active_subscriptions.append(orderbook_subscription)
        print(f"Orderbook subscription: {orderbook_subscription}\n")

        print("Subscribing to trades...")
        trades_subscription = subscriptions.trades(
            TradeSubscriptionParams(symbol="BTC-PERP"),
            example_utils.build_listener("trades"),
        )
        active_subscriptions.append(trades_subscription)
        print(f"Trades subscription: {trades_subscription}\n")

        print("Subscribing to index...")
        index_subscription = subscriptions.index(example_utils.build_listener("index"))
        active_subscriptions.append(index_subscription)
        print(f"Index subscription: {index_subscription}\n")

        example_utils.wait_for_updates(seconds=20)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        print("Cleaning up subscriptions...")
        example_utils.cleanup_subscriptions(active_subscriptions, transport)


if __name__ == "__main__":
    main()
