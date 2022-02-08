import json
import os

from binance.client import Client
from google.cloud import secretmanager


def get_binance_client():
    if os.getenv('ENVIRONMENT') == 'local':
        api_key = os.getenv('API_KEY')
        api_secret = os.getenv('API_SECRET')
    elif os.getenv('ENVIRONMENT') == 'gcp':
        # for GCP environment, secrets are stored in Secret Manager
        client = secretmanager.SecretManagerServiceClient()
        api_key_secret = 'projects/binance-connect-22/secrets/API_KEY/versions/1'
        api_secret_secret = 'projects/binance-connect-22/secrets/API_SECRET/versions/1'
        api_key = client.access_secret_version(
            request={"name": api_key_secret}).payload.data.decode("UTF-8")
        api_secret = client.access_secret_version(
            request={"name": api_secret_secret}).payload.data.decode("UTF-8")

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
    elif asset == 'SHIB':
        return asset + 'USDT'
    else:
        return asset + 'USD'


def get_purchase_value(symbol, client):
    # hard-coding for now since API is broken
    if symbol == 'BTCUSD':
        return 500
    elif symbol == 'DOGEUSD':
        return 566.02
    elif symbol == 'SHIBUSDT':
        return 20


def compute_balances():
    client = get_binance_client()
    account_info = client.get_account()
    # print('client info: {}'.format(account_info))

    balances = account_info['balances']

    assets = {}
    result = {}

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
                    # TODO: compute total purchase value based on prev orders for asset
                    # (API needs fixing, client.get_my_trades(symbol=<symbol>) returns [])
                    if asset == 'USD':
                        purchase_value = assets[asset]['current_value']
                    else:
                        purchase_value = get_purchase_value(
                            symbol, client)
                    assets[asset]['average_purchase_price'] = purchase_value / \
                        assets[asset]['volume']
                    assets[asset]['purchase_value'] = purchase_value
                    assets[asset]['change'] = assets[asset]['current_value'] - \
                        assets[asset]['purchase_value']

    result['assets'] = assets
    result['stats'] = {}
    result['stats']['total_current_value'] = sum(
        [assets[a]['current_value'] for a in assets])
    result['stats']['total_purchase_value'] = sum(
        [assets[a]['purchase_value'] for a in assets])
    result['stats']['total_change'] = result['stats']['total_current_value'] - \
        result['stats']['total_purchase_value']

    return result
