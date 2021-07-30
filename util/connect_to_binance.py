import requests
import json
import os
from binance.client import Client


def get_binance_client():
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')
    top_level_domain = os.getenv('TOP_LEVEL_DOMAIN')

    client = Client(api_key, api_secret, tld=top_level_domain)

    client.API_URL = os.getenv('BASE_BINANCE_URL')
    return client


def get_symbol(asset):
    '''
    :param asset: asset like BTC, DOGE, USD etc
    :return symbol: BTCUSD, DOGEUSD, USDTUSD ...
    '''
    if asset == 'USD':
        return asset + 'TUSD'
    else:
        return asset + 'USD'


def compute_balances():
    client = get_binance_client()
    account_info = client.get_account()
    print('client info: {}'.format(account_info))

    balances = account_info['balances']

    assets = {}

    current_usd_values = client.get_symbol_ticker()

    for item in balances:
        asset = item['asset']
        free = float(item['free'])
        locked = float(item['locked'])

        total = free + locked

        if total > 0:
            assets[asset] = {'volume': total}
            # all_orders = client.get_all_orders(symbol=asset)
            # print(all_orders)
            symbol = get_symbol(asset)
            for value in current_usd_values:
                if value['symbol'] == symbol:
                    assets[asset]['current_price'] = float(value['price'])
                    assets[asset]['current_value'] = assets[asset]['current_price'] * \
                        assets[asset]['volume']

    print(assets)
    return assets
