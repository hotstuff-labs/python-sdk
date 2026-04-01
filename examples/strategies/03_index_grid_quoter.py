"""Index-anchored grid quoter for BTC-PERP."""

import math
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Literal, Optional, cast

from examples.utils.example_utils import setup_info_client, setup_trading_client
from hotstuff import (
    CancelByInstrumentParams,
    InstrumentsParams,
    PlaceOrderParams,
    TickerParams,
    UnitOrder,
)


@dataclass
class TickerSnapshot:
    index_price: float
    bid: Optional[float]
    ask: Optional[float]
    timestamp: int


SYMBOL = "BTC-PERP"
RUNTIME_SECONDS = 120
REQUOTE_INTERVAL_MS = 4_000

GRID_LEVELS_PER_SIDE = 4
BASE_GRID_DISTANCE_BPS = 6
GRID_STEP_BPS = 5
BBO_GUARD_TICKS = 1

BASE_ORDER_SIZE = 0.0015
SIZE_SCALE_PER_LEVEL = 0.4
MAX_LEVEL_SIZE = 0.008
SIZE_DECIMALS = 4

FALLBACK_TICK_SIZE = 0.1


def sleep_ms(ms: int) -> None:
    time.sleep(ms / 1000)


def ms_from_now(ms: int) -> int:
    return int(time.time() * 1000) + ms


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


def pick_value(candidate: Dict[str, Any], keys: List[str]) -> Any:
    for key in keys:
        if key in candidate:
            return candidate[key]
    return None


def decimals_from_step(step: float) -> int:
    text = f"{step:.10f}".rstrip("0").rstrip(".")
    if "." in text:
        return len(text.split(".")[1])
    return 0


def round_to_step(value: float, step: float, mode: Literal["up", "down"]) -> float:
    if step <= 0:
        raise ValueError("step must be > 0")

    steps = value / step
    rounded_steps = math.ceil(steps) if mode == "up" else math.floor(steps)
    return round(rounded_steps * step, decimals_from_step(step))


def resolve_btc_perp_instrument() -> Dict[str, float]:
    info, info_http_transport, info_ws_transport, _ = setup_info_client()

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
        tick_size = to_number(btc_perp.get("tick_size"))

        if not isinstance(instrument_id, int):
            raise RuntimeError("BTC-PERP instrument id is missing or invalid.")
        if tick_size is None or tick_size <= 0:
            tick_size = FALLBACK_TICK_SIZE

        return {"instrument_id": instrument_id, "tick_size": tick_size}
    finally:
        if info_ws_transport is not None:
            info_ws_transport.disconnect()
        elif info_http_transport is not None and hasattr(info_http_transport, "close"):
            info_http_transport.close()


def extract_ticker_record(payload: Any) -> Optional[Dict[str, Any]]:
    candidates: List[Any] = []

    if isinstance(payload, list):
        candidates = payload
    elif is_record(payload):
        payload_record = cast(Dict[str, Any], payload)
        data = payload_record.get("data")
        if isinstance(data, list):
            candidates = data
        elif is_record(data):
            candidates = [data]
        else:
            candidates = [payload]

    for item in candidates:
        if is_record(item) and item.get("symbol") == SYMBOL:
            return cast(Dict[str, Any], item)
    for item in candidates:
        if is_record(item):
            return cast(Dict[str, Any], item)

    return None


def parse_ticker_snapshot(payload: Any) -> Optional[TickerSnapshot]:
    record = extract_ticker_record(payload)
    if record is None:
        return None

    index_price = to_number(
        pick_value(record, ["index_price", "indexPrice", "index", "price"])
    )
    bid = to_number(pick_value(record, ["best_bid_price", "bid", "bid_price"]))
    ask = to_number(pick_value(record, ["best_ask_price", "ask", "ask_price"]))

    if bid is not None and ask is not None and (bid <= 0 or ask <= 0 or ask <= bid):
        bid = None
        ask = None

    if (index_price is None or index_price <= 0) and bid is not None and ask is not None:
        index_price = (bid + ask) / 2

    if index_price is None or index_price <= 0:
        return None

    timestamp_value = to_number(
        pick_value(record, ["last_updated", "timestamp", "time", "ts"])
    )
    timestamp = (
        int(timestamp_value)
        if timestamp_value is not None and timestamp_value > 0
        else int(time.time() * 1000)
    )

    # Normalize likely-second timestamps.
    if timestamp < 10_000_000_000:
        timestamp *= 1000

    return TickerSnapshot(
        index_price=index_price,
        bid=bid,
        ask=ask,
        timestamp=timestamp,
    )


def build_grid_orders(
    instrument_id: int,
    tick_size: float,
    snapshot: TickerSnapshot,
) -> Dict[str, Any]:
    price_decimals = decimals_from_step(tick_size)
    cloid_base = f"idx-grid-{int(time.time() * 1000)}"

    orders: List[UnitOrder] = []
    levels: List[Dict[str, float]] = []
    used_bid_prices = set()
    used_ask_prices = set()

    for level in range(1, GRID_LEVELS_PER_SIDE + 1):
        distance_bps = BASE_GRID_DISTANCE_BPS + (level - 1) * GRID_STEP_BPS
        raw_bid = snapshot.index_price * (1 - distance_bps / 10_000)
        raw_ask = snapshot.index_price * (1 + distance_bps / 10_000)

        bid_price = round_to_step(raw_bid, tick_size, "down")
        ask_price = round_to_step(raw_ask, tick_size, "up")

        if snapshot.bid is not None:
            max_passive_bid = round_to_step(
                snapshot.bid - (BBO_GUARD_TICKS * tick_size), tick_size, "down"
            )
            bid_price = min(bid_price, max_passive_bid)

        if snapshot.ask is not None:
            min_passive_ask = round_to_step(
                snapshot.ask + (BBO_GUARD_TICKS * tick_size), tick_size, "up"
            )
            ask_price = max(ask_price, min_passive_ask)

        if bid_price <= 0:
            continue
        if ask_price <= bid_price:
            ask_price = round_to_step(bid_price + tick_size, tick_size, "up")

        bid_text = f"{bid_price:.{price_decimals}f}"
        ask_text = f"{ask_price:.{price_decimals}f}"
        if bid_text in used_bid_prices or ask_text in used_ask_prices:
            continue

        used_bid_prices.add(bid_text)
        used_ask_prices.add(ask_text)

        size = min(
            MAX_LEVEL_SIZE,
            BASE_ORDER_SIZE * (1 + (level - 1) * SIZE_SCALE_PER_LEVEL),
        )
        size_text = f"{size:.{SIZE_DECIMALS}f}"

        orders.append(
            UnitOrder(
                instrumentId=instrument_id,
                side="b",
                positionSide="BOTH",
                price=bid_text,
                size=size_text,
                tif="GTC",
                ro=False,
                po=True,
                cloid=f"{cloid_base}-b-{level}",
                triggerPx="",
                isMarket=False,
                tpsl="",
                grouping="",
            )
        )
        orders.append(
            UnitOrder(
                instrumentId=instrument_id,
                side="s",
                positionSide="BOTH",
                price=ask_text,
                size=size_text,
                tif="GTC",
                ro=False,
                po=True,
                cloid=f"{cloid_base}-s-{level}",
                triggerPx="",
                isMarket=False,
                tpsl="",
                grouping="",
            )
        )

        levels.append(
            {
                "level": float(level),
                "bid": bid_price,
                "ask": ask_price,
                "size": size,
            }
        )

    return {"orders": orders, "levels": levels}


def main() -> None:
    print("--------------------------------\nIndex-anchored grid quoter\n")
    print(f"Market: {SYMBOL}")

    instrument = resolve_btc_perp_instrument()
    instrument_id = int(instrument["instrument_id"])
    tick_size = float(instrument["tick_size"])
    print(f"Instrument id: {instrument_id}, tick size: {tick_size}")

    exchange, _, trading_ws_transport, _ = setup_trading_client()
    info, info_http_transport, info_ws_transport, _ = setup_info_client()

    try:
        print(
            "Starting loop: "
            f"runtime={RUNTIME_SECONDS}s, requote every {REQUOTE_INTERVAL_MS / 1000}s"
        )
        started_at = int(time.time() * 1000)

        while int(time.time() * 1000) - started_at < RUNTIME_SECONDS * 1000:
            try:
                ticker_payload = info.ticker(TickerParams(symbol=SYMBOL))
            except Exception as error:
                print(f"ticker warning (skipping cycle): {error}")
                sleep_ms(REQUOTE_INTERVAL_MS)
                continue

            snapshot = parse_ticker_snapshot(ticker_payload)
            if snapshot is None:
                print("Skipping cycle: could not parse ticker snapshot.")
                sleep_ms(REQUOTE_INTERVAL_MS)
                continue

            quote = build_grid_orders(instrument_id, tick_size, snapshot)
            orders = quote["orders"]
            levels = quote["levels"]

            if not orders:
                print("Skipping cycle: no valid passive grid levels produced.")
                sleep_ms(REQUOTE_INTERVAL_MS)
                continue

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
                        orders=orders,
                        expiresAfter=ms_from_now(10000),
                    )
                )

                top = levels[0]
                far = levels[-1]
                print(
                    "[index-grid] "
                    f"index={snapshot.index_price:.2f} "
                    f"orders={len(orders)} "
                    f"near=({top['bid']:.2f}/{top['ask']:.2f}) "
                    f"far=({far['bid']:.2f}/{far['ask']:.2f})"
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

        if info_ws_transport is not None:
            info_ws_transport.disconnect()
        elif info_http_transport is not None and hasattr(info_http_transport, "close"):
            info_http_transport.close()

        if trading_ws_transport is not None:
            trading_ws_transport.disconnect()


if __name__ == "__main__":
    main()
