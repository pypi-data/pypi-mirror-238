import traceback
from dataclasses import asdict
from okx.Trade import TradeAPI
from okx.MarketData import MarketAPI
from general.exchange.type_enum import OKX
from general.exchange.exchange_handler import ExchangeHandler
from general.exchange.type_enum import (
    GTC
)
from .utils import to_symbol, to_side, to_order, to_orderbook, to_trade_recorder


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            args[0].logger.error(f"Missing key in message: {e}\n{traceback.format_exc()}")
    return wrapper


class OKXHandler(ExchangeHandler):
    NAME = OKX

    def __init__(self, api_key='', api_secret='', passphrase='', logger=None):
        super().__init__(logger)
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_passphrase = passphrase
        self.okx_trade_demo = TradeAPI('30fb4bfc-d3ed-43ca-9656-ced5ea3e7a41',
                                       '9BFD52327F88CD251CE1FCEC0BFF495A',
                                       '2rYHFKwhxvtBKBZ$$', False, '1', debug=False)
        self.okx_market = MarketAPI(api_key, api_secret, passphrase, False, '0',
                                    domain='https://aws.okx.com', debug=False)
        self.okx_trade = TradeAPI(api_key, api_secret, passphrase, False, '0',
                                  domain='https://aws.okx.com', debug=False)

    @exception_handler
    def create_market_order(self, base, quote, side, qty, dry_run=False):
        if dry_run:
            res = self.okx_trade_demo.place_order(to_symbol(base, quote), 'cross', to_side(side),
                                                  'market', qty, posSide='long')  # not require in net mode
        else:
            res = self.okx_trade.place_order(to_symbol(base, quote), 'cross', to_side(side),
                                             'market', qty)
        return res

    @exception_handler
    def create_limit_order(self, base, quote, side, qty, price, time_in_force=GTC, dry_run=False):
        if dry_run:
            res = self.okx_trade_demo.place_order(to_symbol(base, quote), 'cross', to_side(side),
                                                  'limit', qty, px=price, posSide='long')
        else:
            res = self.okx_trade.place_order(to_symbol(base, quote), 'cross', to_side(side), 'limit',
                                             qty, px=price)
        return res

    @exception_handler
    def cancel_all_order(self, base, quote):
        orders = self.get_open_order(base, quote)
        inst = to_symbol(base, quote)
        order_id_list = [{"instId": inst, "ordId": order.order_id} for order in orders]
        ret = self.okx_trade.cancel_multiple_orders(order_id_list)
        return ret

    @exception_handler
    def get_open_order(self, base, quote):
        ret = self.okx_trade.get_order_list(instType='SWAP')
        res = filter(lambda order: order['instId'] == to_symbol(base, quote), ret['data'])
        return list(map(to_order, res))

    @exception_handler
    def get_orderbook(self, base, quote, limit=10):
        ret = self.okx_market.get_orderbook(to_symbol(base, quote), str(limit))
        return to_orderbook(ret['data'][0])

    @exception_handler
    def get_account_trades(self, base, quote, limit=100):
        ret = self.okx_market.get_trades(to_symbol(base, quote), limit=limit)
        res = list(map(to_trade_recorder, ret['data']))
        return res

    @staticmethod
    def to_market_price(data):
        data = data['data'][0]
        return {
            '_id': data['seqId'],
            'ex': OKXHandler.NAME,
            'b': float(data['bids'][0][0]),
            'bv': float(data['bids'][0][1]),
            'a': float(data['asks'][0][0]),
            'av': float(data['asks'][0][1]),
            't': int(data['ts'])
        }

