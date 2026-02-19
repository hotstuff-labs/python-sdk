import os
from hotstuff import (
    HttpTransport,
    ExchangeClient,
    InfoClient,
    HttpTransportOptions,
    WebSocketTransportOptions,
    WebSocketTransport,
)
from eth_account import Account

def setup_clients(is_testnet: bool = True, is_websocket: bool = False, main_account: bool = True):

    if is_websocket:
        transport = WebSocketTransport(WebSocketTransportOptions(is_testnet=is_testnet))
    else:
        transport = HttpTransport(HttpTransportOptions(is_testnet=is_testnet))

    account = Account.from_key(os.getenv("PRIVATE_KEY") if main_account else os.getenv("AGENT_PRIVATE_KEY"))

    info = InfoClient(transport=transport)
    
    exchange = ExchangeClient(transport=transport, wallet=account)
        
    return info, exchange
  

    