"""Example: Cancel by instrument."""
import json
from examples.utils.example_utils import setup_trading_client
from hotstuff import CancelByInstrumentParams
import time


def main():
    """Main example function."""
    print("--------------------------------\nCancel by instrument\n")
    exchange, _, _, _ = setup_trading_client()
        
    # Cancel order by instrument
    cancel_by_instrument_params = CancelByInstrumentParams(
        instrumentId=1,
        expiresAfter=int(time.time() * 1000) + 3600000,
    )
    result = exchange.cancel_by_instrument(cancel_by_instrument_params)
        
    print(f"Order cancelled successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()
