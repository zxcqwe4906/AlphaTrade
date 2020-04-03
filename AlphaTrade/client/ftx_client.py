import os
import sys

sys.path.append(os.getcwd())

from steaker_quant.client.base_client import BaseClient
from steaker_quant.exchange.ftx import FtxExchange

# pylint: disable=arguments-differ
class FtxClient(BaseClient):
    def __init__(self, api_key, api_secret, subaccount_name=None):
        self._ftx_exchange = FtxExchange(api_key, api_secret, subaccount_name)

    def get_balances(self, coins=None):
        """Return balance list of dict

        [{'coin': USD, 'free': 10, 'total':10}, ...]
        """
        balances = []
        resp_balances = self._ftx_exchange.get_balances()
        for resp_balance in resp_balances:
            if resp_balance['total'] != 0:
                if not coins or resp_balance['coin'] in coins:
                    balances.append(resp_balance)
        return balances

    def get_future_position(self, future):
        """Return negative size if sell position
        """
        positions = self._ftx_exchange.get_positions()
        for position in positions:
            if position['future'] == future:
                if position['side'] == 'buy':
                    return position['size']
                return -position['size']
        return 0

    def get_current_price(self, symbol_name):
        market = self._ftx_exchange.get_market(symbol_name)
        return market['price']

    def get_ohlcv(self, symbol_name, timeframe_type):
        raise NotImplementedError

    def get_orderbook(self, symbol_name, depth=30):
        """Input: market or future
            BTC-PERP, BTC/USD
        """
        return self._ftx_exchange.get_orderbook(symbol_name, depth)

    def get_open_orders(self):
        return self._ftx_exchange.get_open_orders()

    def get_order(self, order_id):
        return self._ftx_exchange.get_order(order_id)

    def place_limit_order(self, symbol_name, side, price, amount, ioc=False, reduceOnly=False):
        print(f'place limit order {side} {amount} {symbol_name} at {price}, ioc: {ioc}, reduceOnly: {reduceOnly}')
        return self._ftx_exchange.place_order(symbol_name, side, price, amount, ioc, reduceOnly)

    def place_market_order(self, symbol_name, side, amount, ioc=False, reduceOnly=False):
        print(f'place market order {side} {amount} {symbol_name}, ioc: {ioc}, reduceOnly: {reduceOnly}')
        return self._ftx_exchange.place_order(symbol_name, side, None, amount, ioc, reduceOnly)

    def cancel_order(self, order_id):
        return self._ftx_exchange.cancel_order(order_id)

    def get_funding_rates(self, future, start_time=None, end_time=None):
        return self._ftx_exchange.get_funding_rates(future, start_time, end_time)

    def list_futures(self):
        return self._ftx_exchange.list_futures()

    def get_future_states(self, future):
        return self._ftx_exchange.get_future_stats(future)
