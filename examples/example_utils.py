import os
from hotstuff import (
    ExchangeClient,
    InfoClient,
)
from eth_account import Account

def setup_clients(is_testnet: bool = True, is_websocket: bool = False, main_account: bool = True):


    account = Account.from_key(os.getenv("PRIVATE_KEY") if main_account else os.getenv("AGENT_PRIVATE_KEY"))

    info = InfoClient(websocket=is_websocket, is_testnet=is_testnet)
    
    exchange = ExchangeClient(websocket=is_websocket, is_testnet=is_testnet, wallet=account)
        
    return info, exchange
  

    