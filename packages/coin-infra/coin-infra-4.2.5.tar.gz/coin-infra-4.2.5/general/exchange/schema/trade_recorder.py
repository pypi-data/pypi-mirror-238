from dataclasses import dataclass


@dataclass
class TradeRecorder:
    exchange: str
    timestamp: int
    base: str
    quote: str
    side: str
    price: float
    qty: float
