from general.exchange.schema import (
    TradeRecorder, Order, Orderbook
)

def to_side(side: str):  # either 'buy' or 'sell'
    return side.upper()


def to_symbol(base: str, quote: str):
    return f'{base}{quote}'


def to_trade_recorder(record) -> TradeRecorder:
    return TradeRecorder(
        exchange='BinanceUM',
        timestamp=record['time'],
        base=record['symbol'][:-4],
        quote=record['symbol'][-4:],
        side=record['side'],
        price=float(record['price']),
        qty=float(record['qty'])
    )


def to_order(order) -> Order:
    return Order(
        exchange='BinanceUM',
        order_id=order['orderId'],
        status=order['status'],
        updated_time=order['updateTime'],
        base=order['symbol'][:-4],
        quote=order['symbol'][-4:],
        qty=0 if order['origQty'] == '' else float(order['origQty']),
        side=order['side'],
        filled=0 if order['executedQty'] == '' else float(order['executedQty']),
        price=0 if order['price'] == '' else float(order['price'])
    )


def to_orderbook(orderbook) -> Orderbook:
    return Orderbook(
        exchange='BinanceUM',
        timestamp=orderbook['T'],
        ask=[(float(price), float(qty)) for price, qty in orderbook['asks']],
        bid=[(float(price), float(qty)) for price, qty in orderbook['bids']]
    )
