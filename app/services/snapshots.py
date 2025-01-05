"""
Service module for retrieving snapshots of the order book and trades.

This module provides functions to:
1. Retrieve a snapshot of the current order book, including the top 5 bids and asks.
2. Retrieve all trades from the database.

The functions query the MongoDB collections for orders and trades and return 
the relevant data in the form of models like `OrderBook` and `Trade`.

Dependencies:
- app.db.mongodb_client: MongoDB collections for orders and trades.
- app.models.order: Pydantic models for OrderBook and Trade.

Example usage:
    from app.services.snapshots import get_order_book_snapshot, get_trades
"""

import json
from app.db.mongodb_client import mongo_order_collection, mongo_trade_collection
from app.models.order import OrderBook, Trade

async def get_order_book_snapshot() -> OrderBook:
    """
    Retrieves a snapshot of the current order book with the top 5 bids and asks.

    This function queries the MongoDB database for all active orders, filters them based 
    on whether they are buy (bids) or sell (asks) orders, and sorts them by price. 
    The top 5 bids and asks are returned as part of the order book.

    Returns:
        OrderBook: An instance of the OrderBook model containing the top 5 bid and ask orders.
    
    Example:
        order_book = await get_order_book_snapshot()
    """
    bids = mongo_order_collection.find({"is_alive": True, "side": 1})
    asks = mongo_order_collection.find({"is_alive": True, "side": -1})

    # Sort bids in descending order and asks in ascending order, then limit to top 5
    bids = sorted(bids, key=lambda x: x['price'], reverse=True)[:5]
    asks = sorted(asks, key=lambda x: x['price'])[:5]

    return OrderBook(bid=bids, ask=asks)

async def get_trades() -> list[Trade]:
    """
    Retrieves all trades from the database.

    This function queries the MongoDB database for all trades and returns them 
    as a list of `Trade` objects, which include the details of each trade.

    Returns:
        list[Trade]: A list of Trade objects representing all trades in the database.
    
    Example:
        trades = await get_trades()
    """
    trades = mongo_trade_collection.find()
    trades = [Trade(**trade) for trade in trades]
    return trades
