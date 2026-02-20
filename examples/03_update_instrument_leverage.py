"""Example: Update instrument leverage."""
import json
import example_utils
from hotstuff import UpdatePerpInstrumentLeverageParams



def main():
    """Main example function."""
    print("--------------------------------\nUpdating instrument leverage\n")
    _, exchange = example_utils.setup_clients(is_testnet=True, main_account=False)
    
    result = exchange.update_perp_instrument_leverage(UpdatePerpInstrumentLeverageParams(instrumentId=1, leverage="10"))
        
    print(f"Instrument leverage updated successfully!\n\nResponse: {json.dumps(result, indent=2)}\n--------------------------------\n")
        
if __name__ == "__main__":
    main()
