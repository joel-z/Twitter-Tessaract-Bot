import hashlib
import hmac
from time import time

import requests

from src.settings import volitality_threshold, bitcoin_buy_quantity, BittrexAuth


def sell(coin_abbr, price):
    nonce = str(int(time() * 1000))

    market = "BTC-{coin}".format(coin=coin_abbr)
    uri = "https://bittrex.com/api/v1.1/account/getbalance?" + "apikey=" + BittrexAuth.api_key + "&nonce=" + nonce + "&currency=" + coin_abbr
    apisign = hmac.new(BittrexAuth.api_secret.encode(), uri.encode(), hashlib.sha512).hexdigest()
    response = requests.get(uri, headers={"apisign": apisign})
    j = response.json()
    available_funds = str(j['result']['Available'])

    uri = "https://bittrex.com/api/v1.1/market/selllimit?" + "apikey=" + BittrexAuth.api_key + "&nonce=" + nonce + "&market=" + market \
          + "&quantity=" + str(available_funds) + "&rate=" + str(price)
    apisign = hmac.new(BittrexAuth.api_secret.encode(), uri.encode(), hashlib.sha512).hexdigest()
    response = requests.get(uri, headers={"apisign": apisign})
    response_data = response.json()
    print(response_data)
    if response_data['success'] is True:
        print("SET A SELL ORDER FOR {0} AT APPROXIMATELY {1}".format(market, price))
    else:
        print("error selling {0} at approximately {1}, check Bittrex balance and API keys".format(market, bid_price))


# TODO: Make buy receive qty and price instead of being global variable
def buy(coin_abbr):
    nonce = str(int(time() * 1000))

    market = "BTC-{coin}".format(coin=coin_abbr)
    response = requests.get("https://bittrex.com/api/v1.1/public/getticker", params={"market": market})
    coin_data = response.json()

    bid_price = coin_data['result']['Ask']
    adjusted_price = bid_price * volitality_threshold
    buy_qty = str(bitcoin_buy_quantity / adjusted_price)
    adjusted_price = str(adjusted_price)

    uri = "https://bittrex.com/api/v1.1/market/buylimit?" + "apikey=" + BittrexAuth.api_key + "&nonce=" + nonce + "&market=" + market \
          + "&quantity=" + buy_qty + "&rate=" + adjusted_price

    apisign = hmac.new(BittrexAuth.api_secret.encode(), uri.encode(), hashlib.sha512).hexdigest()
    response = requests.get(uri, headers={"apisign": apisign})
    response_data = response.json()
    print(response_data)
    if response_data['success'] is True:
        print("SUCCESSFULLY BOUGHT {0} AT APPROXIMATELY {1}".format(market, bid_price))
    else:
        print("error buying {0} at approximately {1}, check Bittrex balance and API keys".format(market, bid_price))

    return bid_price
