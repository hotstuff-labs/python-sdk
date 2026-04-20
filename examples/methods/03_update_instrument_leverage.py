"""Example: Update instrument leverage."""
import json
from examples.utils.example_utils import setup_trading_client
from hotstuff import UpdatePerpInstrumentLeverageParams



def main():
    """Main example function."""
    print("--------------------------------\nUpdating instrument leverage\n")
    exchange, _, _, _ = setup_trading_client()
    
    result = exchange.update_perp_instrument_leverage(UpdatePerpInstrumentLeverageParams(instrumentId=1, leverage="10"))
        
    print(f"Instrument leverage updated successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()
