from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    side: int
    price: float
    quantity: float
    order_id: str = None
    is_alive: bool = True
    traded_quantity: float = 0
    average_traded_price: float = 0

class Trade(BaseModel):
    trade_id: str
    execution_timestamp: datetime
    price: float
    quantity: int
    bid_order_id: str
    ask_order_id: str

class OrderBook(BaseModel):
    bid: list[Order]
    ask: list[Order]
