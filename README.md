# Hotstuff Python SDK

[![PyPI version](https://img.shields.io/pypi/v/hotstuff-sdk.svg)](https://pypi.org/project/hotstuff-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Versions](https://img.shields.io/pypi/pyversions/hotstuff-sdk.svg)](https://pypi.org/project/hotstuff-sdk/)

> Python SDK for interacting with Hotstuff Labs decentralized exchange

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [API Clients](#api-clients)
  - [InfoClient](#infoclient)
  - [ExchangeClient](#exchangeclient)
  - [SubscriptionClient](#subscriptionclient)
- [Transports](#transports)
  - [HttpTransport](#httptransport)
  - [WebSocketTransport](#websockettransport)
- [Advanced Usage](#advanced-usage)
- [Signing](#signing)
- [Error Handling](#error-handling)
- [Examples](#examples)

## Installation

### Using pip

```bash
pip install hotstuff-python-sdk
```

### Using Poetry

```bash
poetry add hotstuff-python-sdk
```

### Install from source

```bash
git clone https://github.com/hotstuff-labs/python-sdk.git
cd python-sdk

# Using Poetry (recommended)
poetry install

# Or using pip
pip install -e .
```

## Quick Start

```python
import asyncio
from hotstuff import (
    HttpTransport,
    WebSocketTransport,
    InfoClient,
    ExchangeClient,
    SubscriptionClient,
    HttpTransportOptions,
    WebSocketTransportOptions,
)

async def main():
    # Create transports
    http_transport = HttpTransport(
        HttpTransportOptions(is_testnet=True)
    )

    ws_transport = WebSocketTransport(
        WebSocketTransportOptions(is_testnet=True)
    )

    # Query market data (read-only)
    info = InfoClient(transport=http_transport)
    ticker = await info.ticker({"symbol": "BTC-PERP"})
    print(f"Current BTC-PERP ticker: {ticker}")

    # Subscribe to real-time updates
    subscriptions = SubscriptionClient(transport=ws_transport)

    def handle_ticker(data):
        print(f"Live ticker: {data.data}")

    sub = await subscriptions.ticker(
        {"symbol": "BTC-PERP"},
        handle_ticker
    )

    # Keep running for a bit
    await asyncio.sleep(10)

    # Unsubscribe
    await sub["unsubscribe"]()

    # Clean up
    await http_transport.close()
    await ws_transport.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

## API Clients

### InfoClient

Query market data, account information, vault details, and blockchain explorer data.

#### Creating an InfoClient

```python
from hotstuff import HttpTransport, InfoClient, HttpTransportOptions

async def setup():
    transport = HttpTransport(HttpTransportOptions(is_testnet=True))
    info = InfoClient(transport=transport)
    return info
```

#### Market Data Methods

```python
import importlib

global_methods = importlib.import_module("hotstuff.methods.info.global")
InstrumentsParams = global_methods.InstrumentsParams
TickerParams = global_methods.TickerParams
OrderbookParams = global_methods.OrderbookParams
TradesParams = global_methods.TradesParams

# Get all instruments (perps, spot, options)
instruments = await info.instruments(InstrumentsParams(type="all"))

# Get supported collateral
collateral = await info.supported_collateral({})

# Get oracle prices
oracle = await info.oracle({})

# Get ticker for a specific symbol
ticker = await info.ticker(TickerParams(symbol="BTC-PERP"))

# Get orderbook with depth
orderbook = await info.orderbook(OrderbookParams(symbol="BTC-PERP", depth=20))

# Get recent trades
trades = await info.trades(TradesParams(symbol="BTC-PERP", limit=50))

# Get mid prices for all instruments
mids = await info.mids({})

# Get best bid/offer
bbo = await info.bbo({"symbol": "BTC-PERP"})

# Get chart data (candles or funding)
chart = await info.chart({
    "symbol": "BTC-PERP",
    "resolution": "1h",
    "chart_type": "candles",
})
```

#### Account Methods

```python
from hotstuff.methods.info.account import (
    AccountSummaryParams,
    AccountInfoParams,
    UserBalanceParams,
    OpenOrdersParams,
    PositionsParams,
    OrderHistoryParams,
    TradeHistoryParams,
    FundingHistoryParams,
    TransferHistoryParams,
    AccountHistoryParams,
    UserFeeInfoParams,
    InstrumentLeverageParams,
    ReferralInfoParams,
    ReferralSummaryParams,
    SubAccountsListParams,
    AgentsParams,
)

user_address = "0x1234..."

# Get account summary
summary = await info.account_summary(AccountSummaryParams(user=user_address))

# Get account info
account_info = await info.account_info(AccountInfoParams(user=user_address))

# Get user balance
balance = await info.user_balance(UserBalanceParams(user=user_address))

# Get open orders
open_orders = await info.open_orders(OpenOrdersParams(user=user_address))

# Get current positions
positions = await info.positions(PositionsParams(user=user_address))

# Get order history
order_history = await info.order_history(OrderHistoryParams(
    user=user_address,
    limit=100,
))

# Get trade history (fills)
trade_history = await info.trade_history(TradeHistoryParams(user=user_address))

# Get funding history
funding_history = await info.funding_history(FundingHistoryParams(user=user_address))

# Get transfer history
transfer_history = await info.transfer_history(TransferHistoryParams(user=user_address))

# Get account history with time range
account_history = await info.account_history(AccountHistoryParams(
    user=user_address,
    from_time=int(time.time()) - 86400,  # 24h ago
    to_time=int(time.time()),
))

# Get user fee information
fee_info = await info.user_fee_info(UserFeeInfoParams(user=user_address))

# Get instrument leverage settings
leverage = await info.instrument_leverage(InstrumentLeverageParams(
    user=user_address,
    instrumentId=1,
))

# Get referral info
referral_info = await info.get_referral_info(ReferralInfoParams(user=user_address))

# Get referral summary
referral_summary = await info.referral_summary(ReferralSummaryParams(user=user_address))

# Get sub-accounts list
sub_accounts = await info.sub_accounts_list(SubAccountsListParams(user=user_address))

# Get agents
agents = await info.agents(AgentsParams(user=user_address))
```

#### Vault Methods

```python
# Get all vaults
vaults = await info.vaults({})

# Get sub-vaults for a specific vault
sub_vaults = await info.sub_vaults({"vaultId": 1})

# Get vault balances
vault_balances = await info.vault_balances({"vaultId": 1})
```

#### Explorer Methods

```python
# Get recent blocks
blocks = await info.blocks({"limit": 10})

# Get specific block details
block_details = await info.block_details({"blockNumber": 12345})

# Get recent transactions
transactions = await info.transactions({"limit": 20})

# Get specific transaction details
tx_details = await info.transaction_details({"txHash": "0xabc..."})
```

---

### ExchangeClient

Execute signed trading actions and account management operations.

#### Creating an ExchangeClient

```python
from hotstuff import HttpTransport, ExchangeClient, HttpTransportOptions
from eth_account import Account

async def setup():
    transport = HttpTransport(HttpTransportOptions(is_testnet=True))

    # Create account from private key
    account = Account.from_key("0xYOUR_PRIVATE_KEY")

    exchange = ExchangeClient(
        transport=transport,
        wallet=account
    )
    return exchange
```

#### Trading Methods

```python
import time
from hotstuff.methods.exchange.trading import (
    PlaceOrderParams,
    UnitOrder,
    BrokerConfig,
    CancelByOidParams,
    CancelByCloidParams,
    CancelAllParams,
)

# Place order(s)
await exchange.place_order(
    PlaceOrderParams(
        orders=[
            UnitOrder(
                instrument_id=1,
                side="b",  # 'b' for buy, 's' for sell
                position_side="BOTH",  # 'LONG', 'SHORT', or 'BOTH'
                price="50000.00",
                size="0.1",
                tif="GTC",  # 'GTC', 'IOC', or 'FOK'
                ro=False,  # reduce-only
                po=False,  # post-only
                cloid="my-order-123",  # client order ID
                trigger_px="51000.00",  # optional trigger price
                is_market=False,  # optional market order flag
                tpsl="",  # optional: 'tp', 'sl', or ''
                grouping="normal",  # optional: 'position', 'normal', or ''
            ),
        ],
        broker_config=BrokerConfig(  # optional broker configuration
            broker="0x0000000000000000000000000000000000000000",
            fee="0.001",
        ),
        expires_after=int(time.time() * 1000) + 3600000,  # 1 hour from now (in milliseconds)
    )
)

# Cancel order by order ID
await exchange.cancel_by_oid(
    CancelByOidParams(
        cancels=[
            {"oid": 123456, "instrumentId": 1},
            {"oid": 123457, "instrumentId": 1},
        ],
        expires_after=int(time.time() * 1000) + 3600000,
    )
)

# Cancel order by client order ID
await exchange.cancel_by_cloid(
    CancelByCloidParams(
        cancels=[{"cloid": "my-order-123", "instrumentId": 1}],
        expires_after=int(time.time() * 1000) + 3600000,
    )
)

# Cancel all orders
await exchange.cancel_all(
    CancelAllParams(
        expires_after=int(time.time() * 1000) + 3600000,
    )
)
```

#### Account Management

```python
from hotstuff import AddAgentParams
from hotstuff.methods.exchange.account import (
    RevokeAgentParams,
    ApproveBrokerFeeParams,
    UpdatePerpInstrumentLeverageParams,
    CreateReferralCodeParams,
    SetReferrerParams,
    ClaimReferralRewardsParams,
)

# Add an agent (requires agent private key)
await exchange.add_agent(
    AddAgentParams(
        agent_name="my-trading-bot",
        agent="0xagent...",
        for_account="",
        agent_private_key="0xprivatekey...",
        signer="0xsigner...",
        valid_until=int(time.time() * 1000) + 86400000,  # 24 hours (in milliseconds)
    )
)

# Revoke an agent
await exchange.revoke_agent(
    RevokeAgentParams(
        agent="0xagent...",
        for_account="",  # optional: sub-account address
    )
)

# Update leverage for a perpetual instrument
await exchange.update_perp_instrument_leverage(
    UpdatePerpInstrumentLeverageParams(
        instrument_id=1,
        leverage=10,  # 10x leverage
    )
)

# Approve broker fee
await exchange.approve_broker_fee(
    ApproveBrokerFeeParams(
        broker="0xbroker...",
        max_fee_rate="0.001",  # 0.1% max fee
    )
)

# Create a referral code
await exchange.create_referral_code(
    CreateReferralCodeParams(
        code="MY_REFERRAL_CODE",
    )
)

# Set referrer using a referral code
await exchange.set_referrer(
    SetReferrerParams(
        code="FRIEND_REFERRAL_CODE",
    )
)

# Claim referral rewards
await exchange.claim_referral_rewards(
    ClaimReferralRewardsParams(
        collateral_id=1,
        spot=True,  # True for spot account, False for derivatives
    )
)
```

#### Collateral Transfer Methods

```python
from hotstuff.methods.exchange.collateral import (
    AccountSpotWithdrawRequestParams,
    AccountDerivativeWithdrawRequestParams,
    AccountSpotBalanceTransferRequestParams,
    AccountDerivativeBalanceTransferRequestParams,
    AccountInternalBalanceTransferRequestParams,
)

# Request spot collateral withdrawal to external chain
await exchange.account_spot_withdraw_request(
    AccountSpotWithdrawRequestParams(
        collateral_id=1,
        amount="100.0",
        chain_id=1,  # Ethereum mainnet
    )
)

# Request derivative collateral withdrawal to external chain
await exchange.account_derivative_withdraw_request(
    AccountDerivativeWithdrawRequestParams(
        collateral_id=1,
        amount="100.0",
        chain_id=1,
    )
)

# Transfer spot balance to another address on Hotstuff
await exchange.account_spot_balance_transfer_request(
    AccountSpotBalanceTransferRequestParams(
        collateral_id=1,
        amount="50.0",
        destination="0xrecipient...",
    )
)

# Transfer derivative balance to another address on Hotstuff
await exchange.account_derivative_balance_transfer_request(
    AccountDerivativeBalanceTransferRequestParams(
        collateral_id=1,
        amount="50.0",
        destination="0xrecipient...",
    )
)

# Transfer balance between spot and derivatives accounts
await exchange.account_internal_balance_transfer_request(
    AccountInternalBalanceTransferRequestParams(
        collateral_id=1,
        amount="25.0",
        to_derivatives_account=True,  # True: spot -> derivatives, False: derivatives -> spot
    )
)
```

#### Vault Methods

```python
from hotstuff.methods.exchange.vault import (
    DepositToVaultParams,
    RedeemFromVaultParams,
)

# Deposit to a vault
await exchange.deposit_to_vault(
    DepositToVaultParams(
        vault_address="0xvault...",
        amount="1000.0",
    )
)

# Redeem shares from a vault
await exchange.redeem_from_vault(
    RedeemFromVaultParams(
        vault_address="0xvault...",
        shares="500.0",
    )
)
```

---

### SubscriptionClient

Subscribe to real-time data streams via WebSocket.

#### Creating a SubscriptionClient

```python
from hotstuff import WebSocketTransport, SubscriptionClient, WebSocketTransportOptions

async def setup():
    transport = WebSocketTransport(WebSocketTransportOptions(is_testnet=True))
    subscriptions = SubscriptionClient(transport=transport)
    return subscriptions
```

#### Market Subscriptions

```python
import importlib

subscription_methods = importlib.import_module("hotstuff.methods.subscription.global")
TickerSubscriptionParams = subscription_methods.TickerSubscriptionParams
TradeSubscriptionParams = subscription_methods.TradeSubscriptionParams

# Subscribe to ticker updates
def handle_ticker(data):
    print(f"Ticker: {data.data}")

ticker_sub = await subscriptions.ticker(
    TickerSubscriptionParams(symbol="BTC-PERP"),
    handle_ticker
)

# Subscribe to mid prices
mids_sub = await subscriptions.mids(
    {"symbol": "BTC-PERP"},
    lambda data: print(f"Mids: {data.data}")
)

# Subscribe to best bid/offer
bbo_sub = await subscriptions.bbo(
    {"symbol": "BTC-PERP"},
    lambda data: print(f"BBO: {data.data}")
)

# Subscribe to orderbook updates
orderbook_sub = await subscriptions.orderbook(
    {"symbol": "BTC-PERP"},
    lambda data: print(f"Orderbook: {data.data}")
)

# Subscribe to trades
trade_sub = await subscriptions.trade(
    TradeSubscriptionParams(instrument_id="BTC-PERP"),
    lambda data: print(f"Trade: {data.data}")
)

# Subscribe to index prices
index_sub = await subscriptions.index(
    lambda data: print(f"Index: {data.data}")
)

# Subscribe to chart updates
chart_sub = await subscriptions.chart(
    {
        "symbol": "BTC-PERP",
        "chart_type": "candles",
        "resolution": "1m",
    },
    lambda data: print(f"Chart: {data.data}")
)
```

#### Account Subscriptions

```python
user_address = "0x1234..."

# Subscribe to order updates
order_sub = await subscriptions.account_order_updates(
    {"address": user_address},
    lambda data: print(f"Order update: {data.data}")
)

# Subscribe to balance updates
balance_sub = await subscriptions.account_balance_updates(
    {"address": user_address},
    lambda data: print(f"Balance update: {data.data}")
)

# Subscribe to position updates
position_sub = await subscriptions.positions(
    {"address": user_address},
    lambda data: print(f"Position update: {data.data}")
)

# Subscribe to fills
fills_sub = await subscriptions.fills(
    {"address": user_address},
    lambda data: print(f"Fill: {data.data}")
)

# Subscribe to account summary
account_summary_sub = await subscriptions.account_summary(
    {"user": user_address},
    lambda data: print(f"Account summary: {data.data}")
)
```

#### Explorer Subscriptions

```python
# Subscribe to new blocks
blocks_sub = await subscriptions.blocks(
    {},
    lambda data: print(f"New block: {data.data}")
)

# Subscribe to new transactions
tx_sub = await subscriptions.transactions(
    {},
    lambda data: print(f"New transaction: {data.data}")
)
```

#### Unsubscribing

All subscription methods return a dictionary with an `unsubscribe` function:

```python
sub = await subscriptions.ticker(
    {"symbol": "BTC-PERP"},
    handle_ticker
)

# Later...
await sub["unsubscribe"]()
```

---

## Transports

### HttpTransport

HTTP transport for making API requests to the Hotstuff Labs API.

#### Configuration

```python
from hotstuff import HttpTransport, HttpTransportOptions

transport = HttpTransport(
    HttpTransportOptions(
        # Use testnet or mainnet (default: False = mainnet)
        is_testnet=True,

        # Request timeout in seconds (default: 3.0, set None to disable)
        timeout=5.0,

        # Custom server endpoints
        server={
            "mainnet": {
                "api": "https://api.hotstuff.trade/",
                "rpc": "https://rpc.hotstuff.trade/",
            },
            "testnet": {
                "api": "https://testnet-api.hotstuff.trade/",
                "rpc": "https://testnet-api.hotstuff.trade/",
            },
        },

        # Additional headers
        headers={
            "X-Custom-Header": "value",
        },
    )
)
```

#### Default Endpoints

- **Mainnet:** `https://testnet-api.hotstuff.trade/`
- **Testnet:** `https://testnet-api.hotstuff.trade/`

---

### WebSocketTransport

WebSocket transport for real-time subscriptions using JSON-RPC 2.0.

#### Configuration

```python
from hotstuff import WebSocketTransport, WebSocketTransportOptions

transport = WebSocketTransport(
    WebSocketTransportOptions(
        # Use testnet or mainnet (default: False = mainnet)
        is_testnet=True,

        # Request timeout in seconds (default: 10.0)
        timeout=15.0,

        # Custom server endpoints
        server={
            "mainnet": "wss://api.hotstuff.trade/ws/",
            "testnet": "wss://testnet-api.hotstuff.trade/ws/",
        },

        # Keep-alive ping configuration
        keep_alive={
            "interval": 30.0,  # ping every 30 seconds
            "timeout": 10.0,   # timeout after 10 seconds
        },

        # Auto-connect on creation (default: True)
        auto_connect=True,
    )
)
```

#### Connection Management

```python
# Manually connect (if auto_connect is False)
await transport.connect()

# Check connection status
if transport.is_connected():
    print("Connected!")

# Manually disconnect
await transport.disconnect()

# Send ping
pong = await transport.ping()
```

#### Reconnection

The WebSocket transport automatically reconnects with exponential backoff:

- Maximum attempts: 5
- Initial delay: 1 second
- Delay multiplier: attempt number

#### Default Endpoints

- **Mainnet:** `wss://testnet-api.hotstuff.trade/ws/`
- **Testnet:** `wss://testnet-api.hotstuff.trade/ws/`

---

## Advanced Usage

### Using Context Managers

Both transports support async context managers for automatic cleanup:

```python
async with HttpTransport(HttpTransportOptions(is_testnet=True)) as transport:
    info = InfoClient(transport=transport)
    ticker = await info.ticker({"symbol": "BTC-PERP"})
    print(ticker)
# Transport is automatically closed

async with WebSocketTransport(WebSocketTransportOptions(is_testnet=True)) as transport:
    subscriptions = SubscriptionClient(transport=transport)
    # Use subscriptions...
# Transport is automatically disconnected
```

### Managing Multiple Subscriptions

```python
subscriptions = SubscriptionClient(transport=ws_transport)
active_subs = []

# Subscribe to multiple channels
symbols = ["BTC-PERP", "ETH-PERP", "SOL-PERP"]
for symbol in symbols:
    sub = await subscriptions.ticker(
        {"symbol": symbol},
        lambda data: print(f"{symbol}: {data.data}")
    )
    active_subs.append(sub)

# Unsubscribe from all
for sub in active_subs:
    await sub["unsubscribe"]()
```

### Environment-Specific Configuration

```python
import os

is_production = os.getenv("ENV") == "production"

http_transport = HttpTransport(
    HttpTransportOptions(
        is_testnet=not is_production,
        timeout=5.0 if is_production else 10.0,
    )
)

ws_transport = WebSocketTransport(
    WebSocketTransportOptions(
        is_testnet=not is_production,
        keep_alive={
            "interval": 30.0 if is_production else 60.0,
            "timeout": 10.0,
        },
    )
)
```

---

## Signing

### How Signing Works

The SDK uses EIP-712 typed data signing for all exchange actions. Here's what happens under the hood:

1. **Action Encoding**: The action payload is encoded using MessagePack
2. **Hashing**: The encoded bytes are hashed with keccak256
3. **EIP-712 Signing**: The hash is signed using EIP-712 typed data with the following structure:

```python
from eth_account import Account
from eth_account.messages import encode_structured_data
from eth_utils import keccak
import msgpack

# EIP-712 Domain
domain = {
    "name": "HotstuffCore",
    "version": "1",
    "chainId": 1,
    "verifyingContract": "0x1234567890123456789012345678901234567890",
}

# EIP-712 Types
types = {
    "EIP712Domain": [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
        {"name": "chainId", "type": "uint256"},
        {"name": "verifyingContract", "type": "address"},
    ],
    "Action": [
        {"name": "source", "type": "string"},    # "Testnet" or "Mainnet"
        {"name": "hash", "type": "bytes32"},     # keccak256 of msgpack-encoded action
        {"name": "txType", "type": "uint16"},    # transaction type identifier
    ],
}

# Encode action to msgpack
action_bytes = msgpack.packb(action)

# Hash the payload
payload_hash = keccak(action_bytes)

# Message
message = {
    "source": "Testnet",  # or "Mainnet"
    "hash": payload_hash,
    "txType": tx_type,
}

# Create structured data
structured_data = {
    "types": types,
    "primaryType": "Action",
    "domain": domain,
    "message": message,
}

# Encode and sign
encoded_data = encode_structured_data(structured_data)
signed_message = wallet.sign_message(encoded_data)
signature = signed_message.signature.hex()
```

### Debugging Signature Issues

It is recommended to use an existing SDK instead of manually generating signatures. There are many potential ways in which signatures can be wrong. An incorrect signature results in recovering a different signer based on the signature and payload and results in one of the following errors:

```
"Error: account does not exist."
```

```
"invalid order signer"
```

where the returned address does not match the public address of the wallet you are signing with. The returned address also changes for different inputs.

An incorrect signature does not indicate why it is incorrect which makes debugging more challenging. To debug this it is recommended to read through the SDK carefully and make sure the implementation matches exactly. If that doesn't work, add logging to find where the output diverges.

---

## Error Handling

### HTTP Errors

HTTP transport raises exceptions with descriptive messages from the server:

```python
try:
    await exchange.place_order(
        PlaceOrderParams(
            # ... order params
        )
    )
except Exception as e:
    print(f"Failed to place order: {e}")
```

### WebSocket Errors

WebSocket subscriptions can fail during subscribe:

```python
try:
    sub = await subscriptions.ticker(
        {"symbol": "BTC-PERP"},
        handle_ticker
    )
except Exception as e:
    print(f"Subscription failed: {e}")
```

---

## Examples

### Complete Trading Bot Example

```python
import asyncio
import time
import os
from hotstuff import (
    HttpTransport,
    WebSocketTransport,
    InfoClient,
    ExchangeClient,
    SubscriptionClient,
    HttpTransportOptions,
    WebSocketTransportOptions,
)
from eth_account import Account
import importlib

global_methods = importlib.import_module("hotstuff.methods.info.global")
TickerParams = global_methods.TickerParams

from hotstuff.methods.exchange.trading import (
    PlaceOrderParams,
    UnitOrder,
    BrokerConfig,
)

async def main():
    # Setup
    http_transport = HttpTransport(HttpTransportOptions(is_testnet=True))
    ws_transport = WebSocketTransport(WebSocketTransportOptions(is_testnet=True))

    account = Account.from_key(os.getenv("PRIVATE_KEY"))

    info = InfoClient(transport=http_transport)
    exchange = ExchangeClient(transport=http_transport, wallet=account)
    subscriptions = SubscriptionClient(transport=ws_transport)

    # Get current market data
    ticker = await info.ticker(TickerParams(symbol="BTC-PERP"))
    print(f"Current price: {ticker}")

    # Subscribe to live updates
    def handle_ticker(data):
        price = data.data.get("last")
        print(f"Live price: {price}")

        # Simple trading logic
        if price and price < 50000:
            asyncio.create_task(place_order(exchange, price))

    async def place_order(exchange, price):
        try:
            await exchange.place_order(
                PlaceOrderParams(
                    orders=[
                        UnitOrder(
                            instrument_id=1,
                            side="b",
                            position_side="BOTH",
                            price=str(price),
                            size="0.1",
                            tif="GTC",
                            ro=False,
                            po=False,
                            cloid=f"order-{int(time.time())}",
                            trigger_px=None,
                            is_market=False,
                            tpsl="",
                            grouping="",
                        )
                    ],
                    broker_config=BrokerConfig(broker="", fee=""),
                    expires_after=int(time.time() * 1000) + 3600000,
                )
            )
            print("Order placed!")
        except Exception as e:
            print(f"Order failed: {e}")

    ticker_sub = await subscriptions.ticker(
        {"symbol": "BTC-PERP"},
        handle_ticker
    )

    # Run for 1 hour then cleanup
    await asyncio.sleep(3600)
    await ticker_sub["unsubscribe"]()
    await http_transport.close()
    await ws_transport.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
```

### Broker Fee with Agent Trading Example

This example demonstrates the full flow of approving a broker fee from the main account, creating an agent, and placing orders through the agent with broker configuration.

```python
import asyncio
import time
import os
from hotstuff import (
    HttpTransport,
    ExchangeClient,
    HttpTransportOptions,
)
from eth_account import Account
from hotstuff.methods.exchange.account import (
    AddAgentParams,
    ApproveBrokerFeeParams,
)
from hotstuff.methods.exchange.trading import (
    PlaceOrderParams,
    UnitOrder,
    BrokerConfig,
)


async def broker_agent_trading_example():
    transport = HttpTransport(HttpTransportOptions(is_testnet=True))

    # Main account setup (the account that will approve broker fees and create agent)
    main_account = Account.from_key(os.getenv("MAIN_PRIVATE_KEY"))
    main_exchange = ExchangeClient(transport=transport, wallet=main_account)

    # Broker address that will receive fees
    broker_address = "0xBrokerAddress..."

    # Step 1: Approve broker fee from main account
    print("Approving broker fee...")
    await main_exchange.approve_broker_fee(
        ApproveBrokerFeeParams(
            broker=broker_address,
            max_fee_rate="0.001",  # 0.1% max fee rate
        )
    )
    print("Broker fee approved!")

    # Step 2: Generate agent credentials and add agent
    agent_account = Account.create()
    agent_private_key = agent_account.key.hex()

    print("Adding agent...")
    await main_exchange.add_agent(
        AddAgentParams(
            agent_name="broker-trading-agent",
            agent=agent_account.address,
            for_account="",
            agent_private_key=agent_private_key,
            signer=main_account.address,
            valid_until=int(time.time() * 1000) + 86400000 * 30,  # Valid for 30 days
        )
    )
    print(f"Agent added: {agent_account.address}")

    # Step 3: Create exchange client for the agent
    agent_exchange = ExchangeClient(transport=transport, wallet=agent_account)

    # Step 4: Place order from agent with broker config
    print("Placing order with broker fee...")
    await agent_exchange.place_order(
        PlaceOrderParams(
            orders=[
                UnitOrder(
                    instrument_id=1,
                    side="b",
                    position_side="BOTH",
                    price="50000.00",
                    size="0.1",
                    tif="GTC",
                    ro=False,
                    po=False,
                    cloid=f"broker-order-{int(time.time())}",
                    trigger_px=None,
                    is_market=False,
                    tpsl="",
                    grouping="",
                )
            ],
            broker_config=BrokerConfig(
                broker=broker_address,
                fee="0.0005",  # 0.05% fee (must be <= approved maxFeeRate)
            ),
            expires_after=int(time.time() * 1000) + 3600000,
        )
    )
    print("Order placed with broker fee!")

    # Optional: Revoke agent when done
    # await main_exchange.revoke_agent(RevokeAgentParams(agent=agent_account.address))

    await transport.close()


if __name__ == "__main__":
    asyncio.run(broker_agent_trading_example())
```

### WebSocket Subscriptions Example

```python
import asyncio
import importlib
from hotstuff import (
    WebSocketTransport,
    SubscriptionClient,
    WebSocketTransportOptions,
)

subscription_methods = importlib.import_module("hotstuff.methods.subscription.global")
TickerSubscriptionParams = subscription_methods.TickerSubscriptionParams
TradeSubscriptionParams = subscription_methods.TradeSubscriptionParams


async def main():
    # Create WebSocket transport for testnet
    transport = WebSocketTransport(
        WebSocketTransportOptions(is_testnet=True)
    )

    # Create SubscriptionClient
    subscriptions = SubscriptionClient(transport=transport)

    try:
        # Subscribe to ticker updates
        def handle_ticker(data):
            print(f"Ticker update: {data.data}")

        print("Subscribing to BTC-PERP ticker...")
        ticker_sub = await subscriptions.ticker(
            TickerSubscriptionParams(symbol="BTC-PERP"),
            handle_ticker
        )

        # Subscribe to trades
        def handle_trade(data):
            print(f"Trade: {data.data}")

        print("Subscribing to BTC-PERP trades...")
        trade_sub = await subscriptions.trade(
            TradeSubscriptionParams(instrument_id="BTC-PERP"),
            handle_trade
        )

        # Run for 30 seconds
        print("\nListening to updates for 30 seconds...\n")
        await asyncio.sleep(30)

        # Unsubscribe
        print("\nUnsubscribing...")
        await ticker_sub["unsubscribe"]()
        await trade_sub["unsubscribe"]()

    finally:
        # Clean up
        await transport.disconnect()


if __name__ == "__main__":
    asyncio.run(main())
```

### Collateral Transfer Example

```python
import asyncio
import os
from hotstuff import (
    HttpTransport,
    ExchangeClient,
    HttpTransportOptions,
)
from eth_account import Account
from hotstuff.methods.exchange.collateral import (
    AccountSpotWithdrawRequestParams,
    AccountDerivativeWithdrawRequestParams,
    AccountSpotBalanceTransferRequestParams,
    AccountDerivativeBalanceTransferRequestParams,
    AccountInternalBalanceTransferRequestParams,
)


async def main():
    transport = HttpTransport(HttpTransportOptions(is_testnet=True))
    account = Account.from_key(os.getenv("PRIVATE_KEY"))
    exchange = ExchangeClient(transport=transport, wallet=account)

    try:
        # Request spot collateral withdrawal to external chain
        result = await exchange.account_spot_withdraw_request(
            AccountSpotWithdrawRequestParams(
                collateral_id=1,  # USDC
                amount="100.0",
                chain_id=1,  # Ethereum mainnet
            )
        )
        print(f"Spot withdraw request result: {result}")

        # Request derivative collateral withdrawal to external chain
        result = await exchange.account_derivative_withdraw_request(
            AccountDerivativeWithdrawRequestParams(
                collateral_id=1,  # USDC
                amount="50.0",
                chain_id=1,  # Ethereum mainnet
            )
        )
        print(f"Derivative withdraw request result: {result}")

        # Transfer spot balance to another address on Hotstuff
        recipient_address = "0x1234567890123456789012345678901234567890"
        result = await exchange.account_spot_balance_transfer_request(
            AccountSpotBalanceTransferRequestParams(
                collateral_id=1,  # USDC
                amount="25.0",
                destination=recipient_address,
            )
        )
        print(f"Spot balance transfer result: {result}")

        # Internal transfer between spot and derivatives accounts
        result = await exchange.account_internal_balance_transfer_request(
            AccountInternalBalanceTransferRequestParams(
                collateral_id=1,  # USDC
                amount="10.0",
                to_derivatives_account=True,  # Transfer from spot to derivatives
            )
        )
        print(f"Internal transfer result: {result}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await transport.close()


if __name__ == "__main__":
    asyncio.run(main())
```

### Vault Operations Example

```python
import asyncio
import os
from hotstuff import (
    HttpTransport,
    ExchangeClient,
    HttpTransportOptions,
)
from eth_account import Account
from hotstuff.methods.exchange.vault import (
    DepositToVaultParams,
    RedeemFromVaultParams,
)


async def main():
    transport = HttpTransport(HttpTransportOptions(is_testnet=True))
    account = Account.from_key(os.getenv("PRIVATE_KEY"))
    exchange = ExchangeClient(transport=transport, wallet=account)

    vault_address = "0x1234567890123456789012345678901234567890"

    try:
        # Deposit to a vault
        result = await exchange.deposit_to_vault(
            DepositToVaultParams(
                vault_address=vault_address,
                amount="1000.0",
            )
        )
        print(f"Deposit result: {result}")

        # Redeem shares from a vault
        result = await exchange.redeem_from_vault(
            RedeemFromVaultParams(
                vault_address=vault_address,
                shares="500.0",
            )
        )
        print(f"Redeem result: {result}")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        await transport.close()


if __name__ == "__main__":
    asyncio.run(main())
```
