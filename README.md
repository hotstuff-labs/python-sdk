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
# Get all instruments (perps, spot, options)
instruments = await info.instruments({"type": "all"})

# Get supported collateral
collateral = await info.supported_collateral({})

# Get oracle prices
oracle = await info.oracle({})

# Get ticker for a specific symbol
ticker = await info.ticker({"symbol": "BTC-PERP"})

# Get orderbook with depth
orderbook = await info.orderbook({"symbol": "BTC-PERP", "depth": 20})

# Get recent trades
trades = await info.trades({"symbol": "BTC-PERP", "limit": 50})

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
user_address = "0x1234..."

# Get account summary
summary = await info.account_summary({"user": user_address})

# Get account info
account_info = await info.account_info({"user": user_address})

# Get user balance
balance = await info.user_balance({"user": user_address})

# Get open orders
open_orders = await info.open_orders({"user": user_address})

# Get current positions
positions = await info.positions({"user": user_address})

# Get order history
order_history = await info.order_history({
    "user": user_address,
    "limit": 100,
})

# Get trade history (fills)
trade_history = await info.trade_history({"user": user_address})

# Get funding history
funding_history = await info.funding_history({"user": user_address})

# Get transfer history
transfer_history = await info.transfer_history({"user": user_address})

# Get account history with time range
account_history = await info.account_history({
    "user": user_address,
    "from": int(time.time()) - 86400,  # 24h ago
    "to": int(time.time()),
})

# Get user fee information
fee_info = await info.user_fee_info({"user": user_address})

# Get instrument leverage settings
leverage = await info.instrument_leverage({
    "user": user_address,
    "instrumentId": 1,
})

# Get referral info
referral_info = await info.get_referral_info({"user": user_address})

# Get referral summary
referral_summary = await info.referral_summary({"user": user_address})

# Get sub-accounts list
sub_accounts = await info.sub_accounts_list({"user": user_address})

# Get agents
agents = await info.agents({"user": user_address})
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

# Place order(s)
await exchange.place_order({
    "orders": [
        {
            "instrumentId": 1,
            "side": "b",  # 'b' for buy, 's' for sell
            "positionSide": "LONG",  # 'LONG', 'SHORT', or 'BOTH'
            "price": "50000.00",
            "size": "0.1",
            "tif": "GTC",  # 'GTC', 'IOC', or 'FOK'
            "ro": False,  # reduce-only
            "po": False,  # post-only
            "cloid": "my-order-123",  # client order ID
            "triggerPx": "51000.00",  # optional trigger price
            "isMarket": False,  # optional market order flag
            "tpsl": "",  # optional: 'tp', 'sl', or ''
            "grouping": "normal",  # optional: 'position', 'normal', or ''
        },
    ],
    "brokerConfig": {  # optional broker configuration
        "broker": "0x0000000000000000000000000000000000000000",
        "fee": "0.001",
    },
    "expiresAfter": int(time.time()) + 3600,  # 1 hour from now
})

# Cancel order by order ID
await exchange.cancel_by_oid({
    "cancels": [
        {"oid": 123456, "instrumentId": 1},
        {"oid": 123457, "instrumentId": 1},
    ],
    "expiresAfter": int(time.time()) + 3600,
})

# Cancel order by client order ID
await exchange.cancel_by_cloid({
    "cancels": [{"cloid": "my-order-123", "instrumentId": 1}],
    "expiresAfter": int(time.time()) + 3600,
})

# Cancel all orders
await exchange.cancel_all({
    "expiresAfter": int(time.time()) + 3600,
})
```

#### Account Management

```python
# Add an agent (requires agent private key)
await exchange.add_agent({
    "agent_name": "my-trading-bot",
    "agent": "0xagent...",
    "for_account": "",
    "agent_private_key": "0xprivatekey...",
    "signer": "0xsigner...",
    "valid_until": int(time.time()) + 86400,  # 24 hours
})
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
# Subscribe to ticker updates
def handle_ticker(data):
    print(f"Ticker: {data.data}")

ticker_sub = await subscriptions.ticker(
    {"symbol": "BTC-PERP"},
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
    {"symbol": "BTC-PERP"},
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

## Error Handling

### HTTP Errors

HTTP transport raises exceptions with descriptive messages from the server:

```python
try:
    await exchange.place_order({
        # ... order params
    })
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

async def main():
    # Setup
    http_transport = HttpTransport(HttpTransportOptions(is_testnet=True))
    ws_transport = WebSocketTransport(WebSocketTransportOptions(is_testnet=True))

    account = Account.from_key("0xYOUR_PRIVATE_KEY")

    info = InfoClient(transport=http_transport)
    exchange = ExchangeClient(transport=http_transport, wallet=account)
    subscriptions = SubscriptionClient(transport=ws_transport)

    # Get current market data
    ticker = await info.ticker({"symbol": "BTC-PERP"})
    print(f"Current price: {ticker}")

    # Subscribe to live updates
    async def handle_ticker(data):
        price = data.data.get("last")
        print(f"Live price: {price}")

        # Simple trading logic
        if price and price < 50000:
            try:
                await exchange.place_order({
                    "orders": [{
                        "instrumentId": 1,
                        "side": "b",
                        "positionSide": "LONG",
                        "price": str(price),
                        "size": "0.1",
                        "tif": "GTC",
                        "ro": False,
                        "po": False,
                        "cloid": f"order-{int(time.time())}",
                    }],
                    "expiresAfter": int(time.time()) + 3600,
                })
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
