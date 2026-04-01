"""Unit tests for websocket transport request behavior."""
import pytest

from hotstuff import WebSocketTransport, WebSocketTransportOptions
from hotstuff.types import WSMethod


class _AbortedSignal:
    aborted = True


def test_request_exchange_uses_post_action_and_normalizes_data():
    """Exchange websocket requests should use POST and normalize wrapped data."""
    transport = WebSocketTransport(WebSocketTransportOptions(auto_connect=False))
    captured = {}

    def fake_send(message):
        captured["message"] = message
        return {"data": {"ok": True}}

    transport._send_jsonrpc_message = fake_send  # type: ignore[attr-defined]

    result = transport.request("exchange", {"action": "placeOrder"})

    assert result == {"ok": True}
    assert captured["message"]["method"] == WSMethod.POST
    assert captured["message"]["params"]["type"] == "action"
    assert captured["message"]["params"]["payload"] == {"action": "placeOrder"}
    assert captured["message"]["jsonrpc"] == "2.0"
    assert "id" in captured["message"]


def test_request_returns_raw_result_when_data_wrapper_is_missing():
    """Websocket requests should return raw result when no data wrapper is present."""
    transport = WebSocketTransport(WebSocketTransportOptions(auto_connect=False))

    def fake_send(_message):
        return [{"symbol": "BTC-PERP"}]

    transport._send_jsonrpc_message = fake_send  # type: ignore[attr-defined]

    result = transport.request("info", {"method": "ticker", "params": {"symbol": "BTC-PERP"}})

    assert result == [{"symbol": "BTC-PERP"}]


def test_request_aborted_signal_short_circuits_before_send():
    """Aborted signals should fail fast and avoid sending websocket messages."""
    transport = WebSocketTransport(WebSocketTransportOptions(auto_connect=False))
    send_called = {"value": False}

    def fake_send(_message):
        send_called["value"] = True
        return {"data": {"ok": True}}

    transport._send_jsonrpc_message = fake_send  # type: ignore[attr-defined]

    with pytest.raises(Exception, match="aborted"):
        transport.request("info", {"method": "oracle", "params": {}}, signal=_AbortedSignal())

    assert send_called["value"] is False
