import requests
import json

from scripts.database import get_addresses

import yfinance as yf


def return_address_balance(address: int) -> float:
    # Return address balance in euros.
    r       = requests.get(f"https://blockchain.info/rawaddr/{address}")
    data    = json.loads(r.text)

    btc_value = yf.Ticker('BTC-EUR').history(period='1d')['Close'][0]

    if "final_balance" in data.keys():
        return data["final_balance"]*btc_value*1e-8
    raise ValueError("'address' is not valid or have not been found")


def return_personal_crypto_balance() -> float:
    # Return balance of all addresses in address.txt
    balance = 0
    for address in get_addresses():
        balance += return_address_balance(address)
    return balance
