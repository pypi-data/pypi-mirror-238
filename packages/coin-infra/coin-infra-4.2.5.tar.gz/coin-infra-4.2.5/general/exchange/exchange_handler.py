import logging
from typing import Dict


class ExchangeHandler:
    def __init__(self, logger=None):
        if logger:
            self.logger = logger
        else:
            self.logger = logging.Logger(ExchangeHandler.__name__)

    def create_market_order(self, base, quote, side, qty, dry_run):
        pass

    def create_limit_order(self, base, quote, side, qty, price, time_in_force, dry_run):
        pass

    def cancel_all_order(self, base, quote):
        pass

    def get_orderbook(self, base, quote, limit):
        pass

    def get_open_order(self, base, quote):
        pass

    def get_account_trades(self, base, quote):
        pass

    @staticmethod
    def to_market_price(data: Dict) -> Dict:
        """
        Convert exchange orderbook data to schema
        {
            _id: int,
            ex: str,
            a: float
            b: float
            t: int
        }
        """
        return data
