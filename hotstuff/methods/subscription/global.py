"""Global subscription method types.

DEPRECATED: This module is deprecated. Import from hotstuff.methods.subscription.channels instead.
This module exists for backward compatibility only.
"""
# Re-export everything from channels.py for backward compatibility
from hotstuff.methods.subscription.channels import (
    SupportedChartResolutions,
    SupportedChartTypes,
    TickerSubscriptionParams,
    MidsSubscriptionParams,
    BBOSubscriptionParams,
    OrderbookSubscriptionParams,
    TradeSubscriptionParams,
    ChartSubscriptionParams,
    PositionsSubscriptionParams,
    FillsSubscriptionParams,
    FundingPaymentsSubscriptionParams,
    AgentsSubscriptionParams,
    AccountSummarySubscriptionParams,
    BlocksSubscriptionParams,
    TransactionsSubscriptionParams,
    OrdersSubscriptionParams,
    OrderbookItem,
    Orderbook,
    Trade,
    OrderUpdate,
    BalanceItem,
    AccountBalanceUpdate,
    ChartUpdate,
)

__all__ = [
    "SupportedChartResolutions",
    "SupportedChartTypes",
    "TickerSubscriptionParams",
    "MidsSubscriptionParams",
    "BBOSubscriptionParams",
    "OrderbookSubscriptionParams",
    "TradeSubscriptionParams",
    "ChartSubscriptionParams",
    "PositionsSubscriptionParams",
    "FillsSubscriptionParams",
    "FundingPaymentsSubscriptionParams",
    "AgentsSubscriptionParams",
    "AccountSummarySubscriptionParams",
    "BlocksSubscriptionParams",
    "TransactionsSubscriptionParams",
    "OrdersSubscriptionParams",
    "OrderbookItem",
    "Orderbook",
    "Trade",
    "OrderUpdate",
    "BalanceItem",
    "AccountBalanceUpdate",
    "ChartUpdate",
]
