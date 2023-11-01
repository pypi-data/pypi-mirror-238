import time

from general.exchange.schema import (
    TradeRecorder, Order, Orderbook
)

def to_side(side: str):  # either 'buy' or 'sell'
    return side.lower()


def to_symbol(base: str, quote: str, instrument: str = 'SWAP'):
    return f'{base}-{quote}-{instrument}'


def to_trade_recorder(record) -> TradeRecorder:
    base, quote, inst = record['instId'].split('-')
    return TradeRecorder(
        exchange='OKX',
        timestamp=record['ts'],
        base=base,
        quote=quote,
        side=record['side'].upper(),
        price=float(record['px']),
        qty=float(record['sz'])
    )


def to_order(order) -> Order:
    base, quote, inst = order['instId'].split('-')
    return Order(
        exchange='OKX',
        order_id=order['ordId'],
        status=order['state'],
        updated_time=int(order['uTime']),
        base=base,
        quote=quote,
        qty=float(order['sz']),
        side=order['side'].upper(),
        filled=float(order['fillSz']),
        price=float(order['px'])
    )


def to_orderbook(orderbook) -> Orderbook:
    return Orderbook(
        exchange='OKX',
        timestamp=int(orderbook['ts']),
        ask=[(float(price), float(qty)) for price, qty, _, _ in orderbook['asks']],
        bid=[(float(price), float(qty)) for price, qty, _, _ in orderbook['bids']],
    )
