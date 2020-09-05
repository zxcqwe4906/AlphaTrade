import time
from typing import Optional, Dict, Any, List

from requests import Request, Session, Response
import hmac

class FtxClient():
    _ENDPOINT = 'https://ftx.com/api/'

    def __init__(self, api_key, api_secret, subaccount_name=None) -> None:
        self._session = Session()
        self._api_key = api_key
        self._api_secret = api_secret
        self._subaccount_name = subaccount_name

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('GET', path, params=params)

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('POST', path, json=params)

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request('DELETE', path, json=params)

    def _request(self, method: str, path: str, **kwargs) -> Any:
        time.sleep(0.1) # sleep to avoid frequrnt request
        request = Request(method, self._ENDPOINT + path, **kwargs)
        self._sign_request(request)
        response = self._session.send(request.prepare())
        return self._process_response(response)

    def _sign_request(self, request: Request) -> None:
        ts = int(time.time() * 1000)
        prepared = request.prepare()
        signature_payload = f'{ts}{prepared.method}{prepared.path_url}'.encode()
        if prepared.body:
            signature_payload += prepared.body
        signature = hmac.new(self._api_secret.encode(), signature_payload, 'sha256').hexdigest()
        request.headers['FTX-KEY'] = self._api_key
        request.headers['FTX-SIGN'] = signature
        request.headers['FTX-TS'] = str(ts)

        if self._subaccount_name:
            request.headers['FTX-SUBACCOUNT'] = self._subaccount_name

    def _process_response(self, response: Response) -> Any:
        try:
            data = response.json()
        except ValueError:
            response.raise_for_status()
            raise
        else:
            if not data['success']:
                raise Exception(data['error'])
            return data['result']

    def list_futures(self) -> List[dict]:
        return self._get('futures')

    def get_orderbook(self, symbol_name: str, depth: int = 30) -> dict:
        if '/' in symbol_name:
            return self._get(f'markets/{symbol_name}/orderbook', {'depth': depth})
        else:
            return self._get(f'futures/{symbol_name}/orderbook', {'depth': depth})

    def get_trades(self, future: str) -> dict:
        return self._get(f'futures/{future}/trades')

    def list_markets(self) -> List[dict]:
        return self._get('markets')

    def get_market(self, market_name: str) -> dict:
        return self._get(f'markets/{market_name}')

    def get_account_info(self) -> dict:
        return self._get(f'account')

    def get_positions(self) -> List[dict]:
        return self._get(f'positions')

    def get_open_orders(self) -> List[dict]:
        return self._get(f'orders')

    def get_order(self, order_id) -> dict:
        return self._get(f'orders/{order_id}')

    def get_orders_history(self, market) -> List[dict]:
        return self._get(f'orders/history?market={market}')

    def get_open_trigger_orders(self, market) -> List[dict]:
        return self._get(f'conditional_orders?market={market}')

    def get_trigger_orders_history(self, market) -> List[dict]:
        return self._get(f'conditional_orders/history?market={market}')

    def get_trigger_order_triggers(self, order_id) -> dict:
        return self._get(f'conditional_orders/{order_id}/triggers')

    def get_market_open_orders(self, market) -> List[dict]:
        return self._get(f'orders', {'market': market})

    def place_order(self, market: str, side: str, price: float, size: float, ioc=False, reduceOnly=False) -> dict:
        return self._post('orders', {'market': market,
                                     'side': side,
                                     'price': price,
                                     'size': size,
                                     'ioc': ioc,
                                     'reduceOnly': reduceOnly})

    def place_stop_order(self, market: str, side: str, trigger_price: float, size: float, order_price=None, reduceOnly=False, retryUntilFilled=True):
        return self._post('conditional_orders', {'market': market,
                                                 'side': side,
                                                 'triggerPrice': trigger_price,
                                                 'orderPrice': order_price,
                                                 'size': size,
                                                 'type': 'stop',
                                                 'reduceOnly': reduceOnly,
                                                 'retryUntilFilled': retryUntilFilled})

    def place_trail_order(self, market: str, side: str, trail_value: float, size: float, order_price=None, reduce_only=None):
        if not reduce_only:
            reduce_only = False
        return self._post('conditional_orders', {'market': market,
                                                 'side': side,
                                                 'trailValue': trail_value,
                                                 'orderPrice': order_price,
                                                 'size': size,
                                                 'type': 'trailingStop',
                                                 'reduceOnly': reduce_only})

    def cancel_order(self, order_id: str) -> dict:
        """
        If success, returns 'Order queued for cancellation'.
        """
        return self._delete(f'orders/{order_id}')

    def cancel_trigger_order(self, order_id: str) -> dict:
        return self._delete(f'conditional_orders/{order_id}')

    def cancel_all_orders(self, market=None) -> dict:
        """
        If success, returns 'Order queued for cancellation'.
        """
        return self._delete(f'orders', {'market': market})

    def get_fills(self, market=None, limit=None, start_time=None) -> List[dict]:
        params = {}
        if market:
            params['market'] = market
        if limit:
            params['limit'] = limit
        if start_time:
            params['start_time'] = start_time
        return self._get(f'fills', params=params)

    def get_balances(self) -> List[dict]:
        return self._get('wallet/balances')

    def get_deposit_address(self, ticker: str) -> dict:
        return self._get(f'wallet/deposit_address/{ticker}')

    def get_future(self, future_name: str) -> dict:
        return self._get(f'futures/{future_name}')

    def get_future_stats(self, future: str) -> dict:
        return self._get(f'futures/{future}/stats')

    def get_funding_rates(self, future=None, start_time=None, end_time=None):
        params = {}
        if future:
            params['future'] = future
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        return self._get(f'funding_rates', params=params)

    def get_historical_prices(self, market_name, resolution, limit=None, start_time=None, end_time=None):
        """Resolution: window length in seconds
        """
        params = {'resolution': resolution}
        if limit:
            params['limit'] = limit
        if start_time:
            params['start_time'] = start_time
        if end_time:
            params['end_time'] = end_time
        return self._get(f'markets/{market_name}/candles', params=params)
