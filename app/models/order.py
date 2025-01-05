"""
Models representing Order, Trade, and OrderBook for the trading system.

This module defines the data models using Pydantic's BaseModel to enforce type validation
and structure. The models include:
- `Order`: Represents a trade order with details such as price, quantity, and order status.
- `Trade`: Represents an individual trade that is executed between two orders.
- `OrderBook`: Represents a collection of orders, categorized into bid and ask sides.

Dependencies:
- pydantic.BaseModel: Provides base functionality for data validation and parsing.
- datetime.datetime: Used for timestamps in the `Trade` model.

Example usage:
    from app.models.orders import Order, Trade, OrderBook
"""

from pydantic import BaseModel
from datetime import datetime

class Order(BaseModel):
    """
    Represents a trading order in the system.

    Attributes:
        side (int): The side of the order, where 1 might represent a buy order and -1 represents a sell order.
        price (float): The price at which the order is placed.
        quantity (float): The quantity of the asset to be traded.
        order_id (str, optional): A unique identifier for the order (default is None).
        is_alive (bool): A flag indicating whether the order is still active (default is True).
        traded_quantity (float): The quantity of the order that has already been traded (default is 0).
        average_traded_price (float): The average price at which the order has been traded (default is 0).
        remaining_quantity (float): The remaining quantity of the order to be traded (default is 0).
    """
    side: int
    price: float
    quantity: float
    order_id: str = None
    is_alive: bool = True
    traded_quantity: float = 0
    average_traded_price: float = 0
    remaining_quantity: float = 0

class Trade(BaseModel):
    """
    Represents a trade between two orders.

    Attributes:
        trade_id (str): A unique identifier for the trade.
        execution_timestamp (datetime): The timestamp when the trade was executed.
        price (float): The price at which the trade occurred.
        quantity (int): The quantity of the asset traded.
        bid_order_id (str): The order ID of the bid side (buy order).
        ask_order_id (str): The order ID of the ask side (sell order).
    """
    trade_id: str
    execution_timestamp: datetime
    price: float
    quantity: int
    bid_order_id: str
    ask_order_id: str

class OrderBook(BaseModel):
    """
    Represents an order book, with bid and ask sides for trading.

    Attributes:
        bid (list[Order]): A list of `Order` objects representing buy orders.
        ask (list[Order]): A list of `Order` objects representing sell orders.
    """
    bid: list[Order]
    ask: list[Order]
