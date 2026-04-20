"""Example: Account subscriptions."""
from hotstuff import (
    AgentsSubscriptionParams,
    FundingPaymentsSubscriptionParams,
    OrdersSubscriptionParams,
    AccountSummarySubscriptionParams,
    PositionsSubscriptionParams,
)
from examples.utils.example_utils import setup_subscription_client
from examples.utils.example_utils import build_listener, wait_for_updates, cleanup_subscriptions
from examples.utils.config import ADDRESSES

DEFAULT_ACCOUNT_ADDRESS = ADDRESSES["MAIN_ACCOUNT_ADDRESS"]



def main():
    """Main example function."""
    print("--------------------------------\nAccount subscriptions\n")
    user_address = DEFAULT_ACCOUNT_ADDRESS
    print(f"Using user address: {user_address}\n")

    subscriptions, transport = setup_subscription_client()
    active_subscriptions = []

    try:
        print("Subscribing to account summary...")
        account_summary_subscription = subscriptions.account_summary(
            AccountSummarySubscriptionParams(user=user_address),
            build_listener("account_summary"),
        )
        active_subscriptions.append(account_summary_subscription)
        print(f"Account summary subscription: {account_summary_subscription}\n")


        print("Subscribing to positions...")
        positions_subscription = subscriptions.positions(
            PositionsSubscriptionParams(user=user_address),
            build_listener("positions"),
        )
        active_subscriptions.append(positions_subscription)
        print(f"Positions subscription: {positions_subscription}\n")

        print("Subscribing to orders...")
        orders_subscription = subscriptions.orders(
            OrdersSubscriptionParams(user=user_address),
            build_listener("orders"),
        )
        active_subscriptions.append(orders_subscription)
        print(f"Orders subscription: {orders_subscription}\n")

        print("Subscribing to funding payments...")
        funding_subscription = subscriptions.funding_payments(
            FundingPaymentsSubscriptionParams(user=user_address),
            build_listener("funding_payments"),
        )
        active_subscriptions.append(funding_subscription)
        print(f"Funding payments subscription: {funding_subscription}\n")

        print("Subscribing to agents...")
        agents_subscription = subscriptions.agents(
            AgentsSubscriptionParams(user=user_address),
            build_listener("agents"),
        )
        active_subscriptions.append(agents_subscription)
        print(f"Agents subscription: {agents_subscription}\n")

        wait_for_updates(seconds=20)
    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        print("Cleaning up subscriptions...")
        cleanup_subscriptions(active_subscriptions, transport)


if __name__ == "__main__":
    main()
