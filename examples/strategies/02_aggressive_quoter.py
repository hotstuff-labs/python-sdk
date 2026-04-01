"""Aggressive BTC-PERP quoting strategy using short-term trade flow pressure."""

import math
import threading
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, cast

from examples.utils.example_utils import (
    cleanup_subscriptions,
    setup_info_client,
    setup_subscription_client,
    setup_trading_client,
)
from hotstuff import CancelByInstrumentParams, InstrumentsParams, PlaceOrderParams, UnitOrder
from hotstuff.methods.subscription.channels import BBOSubscriptionParams, TradeSubscriptionParams

Side = Literal["b", "s"]


@dataclass
class TradePoint:
    timestamp: int
    side: Side
    size: float


@dataclass
class BboState:
    bid: float
    ask: float
    timestamp: int


@dataclass
class FlowSignal:
    pressure: float
    total: float


SYMBOL = "BTC-PERP"
RUNTIME_SECONDS = 90
REQUOTE_INTERVAL_MS = 1_500
SIGNAL_WINDOW_MS = 8_000
BBO_STALE_MS = 4_000

BASE_ORDER_SIZE = 0.003
MAX_ORDER_SIZE = 0.02
MIN_FLOW_VOLUME = 0.02

INSIDE_QUOTE_TICKS = 1
MAX_PRESSURE_TICKS = 3
CROSS_ON_STRONG_SIGNAL_TICKS = 1
STRONG_SIGNAL_THRESHOLD = 0.75

SIZE_DECIMALS = 4
FALLBACK_TICK_SIZE = 0.1


def sleep_ms(ms: int) -> None:
    time.sleep(ms / 1000)


def ms_from_now(ms: int) -> int:
    return int(time.time() * 1000) + ms


def wait_for_websocket_setup(transport: Any, label: str, timeout_ms: int = 15_000) -> None:
    deadline = int(time.time() * 1000) + timeout_ms
    while not transport.is_connected() and int(time.time() * 1000) < deadline:
        sleep_ms(100)

    if not transport.is_connected():
        raise RuntimeError(f"{label} websocket was not ready within {timeout_ms}ms.")


def is_record(value: Any) -> bool:
    return isinstance(value, dict)


def to_number(value: Any) -> Optional[float]:
    if isinstance(value, (int, float)):
        parsed = float(value)
        if math.isfinite(parsed):
            return parsed
        return None

    if isinstance(value, str):
        try:
            parsed = float(value)
            if math.isfinite(parsed):
                return parsed
        except ValueError:
            return None

    return None


def normalize_side(value: Any) -> Optional[Side]:
    if not isinstance(value, str):
        return None

    side = value.lower()
    if side in ("b", "buy"):
        return "b"
    if side in ("s", "sell"):
        return "s"
    return None


def normalize_timestamp(value: Any) -> int:
    parsed = to_number(value)
    if parsed is None or parsed <= 0:
        return int(time.time() * 1000)

    # Some feeds return seconds; normalize to milliseconds.
    return int(parsed * 1000 if parsed < 10_000_000_000 else parsed)


def pick_value(candidate: Dict[str, Any], keys: List[str]) -> Any:
    for key in keys:
        if key in candidate:
            return candidate[key]
    return None


def extract_event_payload(event: Any) -> Any:
    if hasattr(event, "data"):
        return getattr(event, "data")
    if is_record(event):
        if "data" in event:
            return event["data"]
        if "detail" in event:
            return event["detail"]
    return event


def parse_bbo(detail: Any) -> Optional[BboState]:
    candidate = detail[0] if isinstance(detail, list) and detail else detail
    if not is_record(candidate):
        return None

    candidate = cast(Dict[str, Any], candidate)
    bid = to_number(pick_value(candidate, ["best_bid_price", "bid", "bid_price"]))
    ask = to_number(pick_value(candidate, ["best_ask_price", "ask", "ask_price"]))
    if bid is None or ask is None or bid <= 0 or ask <= 0 or ask <= bid:
        return None

    timestamp = normalize_timestamp(
        pick_value(candidate, ["timestamp", "time", "last_updated"])
    )
    return BboState(bid=bid, ask=ask, timestamp=timestamp)


def parse_trades(detail: Any) -> List[TradePoint]:
    source_items = detail if isinstance(detail, list) else [detail]
    parsed: List[TradePoint] = []

    for item in source_items:
        if not is_record(item):
            continue
        item_record = cast(Dict[str, Any], item)
        trade_items = item_record["trades"] if isinstance(item_record.get("trades"), list) else [item]

        for trade in trade_items:
            if not is_record(trade):
                continue

            trade_record = cast(Dict[str, Any], trade)
            side = normalize_side(
                pick_value(trade_record, ["side", "taker_side", "direction"])
            )
            size = to_number(pick_value(trade_record, ["size", "amount", "qty"]))
            if side is None or size is None or size <= 0:
                continue

            parsed.append(
                TradePoint(
                    side=side,
                    size=size,
                    timestamp=normalize_timestamp(
                        pick_value(trade_record, ["timestamp", "time", "ts"])
                    ),
                )
            )

    return parsed


def prune_trades(trades: List[TradePoint]) -> None:
    cutoff = int(time.time() * 1000) - SIGNAL_WINDOW_MS
    while trades and trades[0].timestamp < cutoff:
        trades.pop(0)


def build_flow_signal(trades: List[TradePoint]) -> FlowSignal:
    buy_volume = 0.0
    sell_volume = 0.0
    for trade in trades:
        if trade.side == "b":
            buy_volume += trade.size
        else:
            sell_volume += trade.size

    total = buy_volume + sell_volume
    if total < MIN_FLOW_VOLUME:
        return FlowSignal(pressure=0.0, total=total)

    pressure = (buy_volume - sell_volume) / total
    return FlowSignal(pressure=max(-1.0, min(1.0, pressure)), total=total)


def decimals_from_step(step: float) -> int:
    text = f"{step:.10f}".rstrip("0").rstrip(".")
    if "." in text:
        return len(text.split(".")[1])
    return 0


def round_to_step(value: float, step: float) -> float:
    return round(round(value / step) * step, decimals_from_step(step))


def compute_order_size(signal: FlowSignal) -> float:
    scale = 1 + min(signal.total / MIN_FLOW_VOLUME, 5)
    return min(MAX_ORDER_SIZE, BASE_ORDER_SIZE * scale)


def compute_aggressive_quote_prices(
    tick_size: float, bbo: BboState, signal: FlowSignal
) -> Dict[str, float]:
    spread_ticks = max(1, round((bbo.ask - bbo.bid) / tick_size))

    bid_price = bbo.bid
    ask_price = bbo.ask

    if spread_ticks > 1:
        bid_price += INSIDE_QUOTE_TICKS * tick_size
        ask_price -= INSIDE_QUOTE_TICKS * tick_size

    pressure_ticks = round(abs(signal.pressure) * MAX_PRESSURE_TICKS)
    if signal.pressure > 0:
        bid_price += pressure_ticks * tick_size
        ask_price += max(0, pressure_ticks - 1) * tick_size
    elif signal.pressure < 0:
        ask_price -= pressure_ticks * tick_size
        bid_price -= max(0, pressure_ticks - 1) * tick_size

    if signal.pressure >= STRONG_SIGNAL_THRESHOLD:
        bid_price += CROSS_ON_STRONG_SIGNAL_TICKS * tick_size
    elif signal.pressure <= -STRONG_SIGNAL_THRESHOLD:
        ask_price -= CROSS_ON_STRONG_SIGNAL_TICKS * tick_size

    bid_price = round_to_step(bid_price, tick_size)
    ask_price = round_to_step(ask_price, tick_size)

    if ask_price <= bid_price:
        ask_price = round_to_step(bid_price + tick_size, tick_size)

    return {"bid_price": bid_price, "ask_price": ask_price}


def build_quote_orders(
    instrument_id: int, tick_size: float, bbo: BboState, signal: FlowSignal
) -> Dict[str, Any]:
    prices = compute_aggressive_quote_prices(tick_size, bbo, signal)
    bid_price = prices["bid_price"]
    ask_price = prices["ask_price"]
    size = compute_order_size(signal)

    price_decimals = decimals_from_step(tick_size)
    size_text = f"{size:.{SIZE_DECIMALS}f}"
    cloid_base = f"agg-mm-{int(time.time() * 1000)}"

    orders = [
        UnitOrder(
            instrumentId=instrument_id,
            side="b",
            positionSide="BOTH",
            price=f"{bid_price:.{price_decimals}f}",
            size=size_text,
            tif="GTC",
            ro=False,
            po=False,
            cloid=f"{cloid_base}-b",
            triggerPx="",
            isMarket=False,
            tpsl="",
            grouping="",
        ),
        UnitOrder(
            instrumentId=instrument_id,
            side="s",
            positionSide="BOTH",
            price=f"{ask_price:.{price_decimals}f}",
            size=size_text,
            tif="GTC",
            ro=False,
            po=False,
            cloid=f"{cloid_base}-s",
            triggerPx="",
            isMarket=False,
            tpsl="",
            grouping="",
        ),
    ]

    return {
        "orders": orders,
        "bid_price": bid_price,
        "ask_price": ask_price,
        "size": size,
    }


def resolve_btc_perp_instrument() -> Dict[str, float]:
    info, _, ws_transport, _ = setup_info_client()

    try:
        instruments = info.instruments(InstrumentsParams(type="perps"))
        if not is_record(instruments):
            raise RuntimeError("Unexpected instruments response shape.")

        perps = instruments.get("perps", [])
        if not isinstance(perps, list):
            raise RuntimeError("Unexpected instruments.perps response shape.")

        btc_perp = next(
            (
                instrument
                for instrument in perps
                if is_record(instrument) and instrument.get("name") == SYMBOL
            ),
            None,
        )
        if not is_record(btc_perp):
            raise RuntimeError(f"Could not find {SYMBOL} in perps instruments list.")

        instrument_id = btc_perp.get("id")
        tick_size = btc_perp.get("tick_size")

        if not isinstance(instrument_id, int):
            raise RuntimeError("BTC-PERP instrument id is missing or invalid.")

        tick_number = to_number(tick_size)
        if tick_number is None or tick_number <= 0:
            tick_number = FALLBACK_TICK_SIZE

        return {"instrument_id": instrument_id, "tick_size": tick_number}
    finally:
        if ws_transport is not None:
            ws_transport.disconnect()


def main() -> None:
    print("--------------------------------\nAggressive BTC-PERP quoting strategy\n")
    print(f"Market: {SYMBOL}")
    print("Mode: aggressive quoting (can take liquidity when signal is strong)")

    instrument = resolve_btc_perp_instrument()
    instrument_id = int(instrument["instrument_id"])
    tick_size = float(instrument["tick_size"])
    print(f"Instrument id: {instrument_id}, tick size: {tick_size}")

    exchange, _, trading_ws_transport, _ = setup_trading_client()
    subscriptions, subscription_ws_transport = setup_subscription_client()

    active_subscriptions: List[Dict[str, Any]] = []
    recent_trades: List[TradePoint] = []
    latest_bbo_ref: Dict[str, Optional[BboState]] = {"value": None}
    first_bbo_event = threading.Event()

    try:
        print("Waiting for subscription websocket connection...")
        wait_for_websocket_setup(subscription_ws_transport, "Subscription")
        print("Subscription websocket connected.")

        print("Subscribing to BBO...")

        def handle_bbo(event: Any) -> None:
            bbo = parse_bbo(extract_event_payload(event))
            if bbo is not None:
                latest_bbo_ref["value"] = bbo
                first_bbo_event.set()

        bbo_subscription = subscriptions.bbo(BBOSubscriptionParams(symbol=SYMBOL), handle_bbo)
        active_subscriptions.append(bbo_subscription)

        print("Subscribing to trades...")

        def handle_trades(event: Any) -> None:
            updates = parse_trades(extract_event_payload(event))
            if not updates:
                return
            recent_trades.extend(updates)
            prune_trades(recent_trades)

        trades_subscription = subscriptions.trades(
            TradeSubscriptionParams(symbol=SYMBOL), handle_trades
        )
        active_subscriptions.append(trades_subscription)

        print("Waiting for first BBO update...")
        if not first_bbo_event.wait(15):
            raise RuntimeError("No BBO update received within 15 seconds.")

        print(
            f"Starting loop: runtime={RUNTIME_SECONDS}s, "
            f"requote every {REQUOTE_INTERVAL_MS / 1000}s"
        )

        started_at = int(time.time() * 1000)
        while int(time.time() * 1000) - started_at < RUNTIME_SECONDS * 1000:
            latest_bbo = latest_bbo_ref.get("value")
            if latest_bbo is None or int(time.time() * 1000) - latest_bbo.timestamp > BBO_STALE_MS:
                print("Skipping cycle: BBO is stale.")
                sleep_ms(REQUOTE_INTERVAL_MS)
                continue

            prune_trades(recent_trades)
            signal = build_flow_signal(recent_trades)
            quote = build_quote_orders(instrument_id, tick_size, latest_bbo, signal)

            try:
                exchange.cancel_by_instrument(
                    CancelByInstrumentParams(
                        instrumentId=instrument_id,
                        expiresAfter=ms_from_now(10000),
                    )
                )
            except Exception as error:
                print(f"cancel_by_instrument warning (continuing): {error}")

            try:
                exchange.place_order(
                    PlaceOrderParams(
                        orders=quote["orders"],
                        expiresAfter=ms_from_now(10000),
                    )
                )

                print(
                    "[agg-quote] "
                    f"bid={quote['bid_price']} "
                    f"ask={quote['ask_price']} "
                    f"size={quote['size']:.{SIZE_DECIMALS}f} "
                    f"pressure={signal.pressure:.2f} "
                    f"flow={signal.total:.4f}"
                )
            except Exception as error:
                print(f"place_order warning (continuing): {error}")

            sleep_ms(REQUOTE_INTERVAL_MS)
    finally:
        print("Stopping strategy and cleaning up...")

        try:
            exchange.cancel_by_instrument(
                CancelByInstrumentParams(
                    instrumentId=instrument_id,
                    expiresAfter=ms_from_now(10000),
                )
            )
        except Exception as error:
            print(f"Final cancel_by_instrument warning: {error}")

        cleanup_subscriptions(active_subscriptions, subscription_ws_transport)
        if trading_ws_transport is not None:
            trading_ws_transport.disconnect()


if __name__ == "__main__":
    main()
