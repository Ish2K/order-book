from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    order_id: str
    side: int
    price: float
    quantity: int
    traded_quantity: int = 0
    alive: bool = True

class Trade(BaseModel):
    trade_id: str
    execution_timestamp: datetime
    price: float
    quantity: int
    bid_order_id: str
    ask_order_id: str
