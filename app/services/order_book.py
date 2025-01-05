"""
Service module for managing the Order Book and processing trades in a trading system.

This module includes functions for interacting with the order book, committing trades,
and modifying orders. The primary tasks include retrieving the order book, matching orders,
executing trades, and updating the database.

Dependencies:
- app.db.mongodb_client: MongoDB collections for orders and trades.
- uuid: Used to generate unique trade IDs.
- datetime: Used to capture the trade execution timestamp.
- app.models.order: Pydantic models for Order, Trade, and OrderBook.

Example usage:
    from app.services.order_book import match_orders, reset_session
"""

from app.db.mongodb_client import mongo_trade_collection, mongo_order_collection
import uuid
from datetime import datetime
from app.models.order import Trade, Order
import json
from app.models.order import OrderBook

async def get_order_book() -> OrderBook:
    """
    Retrieves the current order book, sorted by bid (buy) and ask (sell) prices.

    Queries the database for all active orders and sorts them into bids (buy orders)
    and asks (sell orders) based on their prices. The top 5 bids and asks are returned.

    Returns:
        OrderBook: An instance of the OrderBook model containing the bid and ask orders.
    """
    bids = mongo_order_collection.find({"is_alive": True, "side": 1})
    asks = mongo_order_collection.find({"is_alive": True, "side": -1})

    bids = sorted(bids, key=lambda x: x['price'], reverse=True)
    asks = sorted(asks, key=lambda x: x['price'])

    order_book = OrderBook(bid=bids, ask=asks)

    # return non-str version of order book
    return order_book

async def commit_trade(trade: Trade) -> dict:
    """
    Commits a trade by inserting it into the trade collection in the database.

    Args:
        trade (Trade): The trade object to be committed to the database.

    Returns:
        dict: A success message indicating the trade was committed successfully.
    """
    trade = trade.model_dump_json()
    trade = json.loads(trade)
    mongo_trade_collection.insert_one(trade)

    return {"status": "success", "message": "Trade committed successfully"}

async def modify_order(order: Order) -> dict:
    """
    Modifies an existing order by updating it in the order collection.

    Args:
        order (Order): The order object to be modified.

    Returns:
        dict: A success message indicating the order was modified successfully.
    """
    order = order.model_dump_json()
    order = json.loads(order)
    mongo_order_collection.update_one({"order_id": order["order_id"]}, {"$set": order})

    return {"status": "success", "message": "Order modified successfully"}

async def execute_trade(bid_order: Order, ask_order: Order) -> tuple[Trade, Order, Order]:
    """
    Executes a trade between a bid order and an ask order, updating their quantities and prices.

    Args:
        bid_order (Order): The buy order in the trade.
        ask_order (Order): The sell order in the trade.

    Returns:
        tuple: The created Trade object, and updated bid and ask orders.
    """
    # calculate the trade price
    trade_price = (bid_order.price + ask_order.price) / 2
    trade_quantity = min(bid_order.remaining_quantity, ask_order.remaining_quantity)

    if bid_order.traded_quantity > 0:
        # get the weighted average price
        bid_order.average_traded_price = (bid_order.average_traded_price * bid_order.traded_quantity + trade_price * trade_quantity) / (bid_order.traded_quantity + trade_quantity)
    else:
        bid_order.average_traded_price = trade_price
    
    if ask_order.traded_quantity > 0:
        # get the weighted average price
        ask_order.average_traded_price = (ask_order.average_traded_price * ask_order.traded_quantity + trade_price * trade_quantity) / (ask_order.traded_quantity + trade_quantity)
    else:
        ask_order.average_traded_price = trade_price

    # update the bid order
    bid_order.traded_quantity += trade_quantity
    bid_order.remaining_quantity -= trade_quantity
    bid_order.is_alive = bid_order.remaining_quantity > 0

    # update the ask order
    ask_order.traded_quantity += trade_quantity
    ask_order.remaining_quantity -= trade_quantity
    ask_order.is_alive = ask_order.remaining_quantity > 0

    # create a trade object
    trade_id = str(uuid.uuid4())
    trade = Trade(
        trade_id=trade_id,
        execution_timestamp=datetime.now(),
        price=trade_price,
        quantity=trade_quantity,
        bid_order_id=bid_order.order_id,
        ask_order_id=ask_order.order_id
    )

    await modify_order(bid_order)
    await modify_order(ask_order)

    return trade, bid_order, ask_order

async def match_orders() -> None:
    """
    Matches the best bid and ask orders from the order book, executing trades if possible.

    This function continually matches the highest bid and lowest ask orders, executing
    trades as long as the ask price is less than or equal to the bid price. After each trade,
    the orders are updated and the trade is committed to the database.

    Returns:
        None
    """
    order_book = await get_order_book()
    asks = order_book.ask
    bids = order_book.bid
    # match the orders by treating the order book as a priority queue

    while ((len(asks) > 0 and len(bids) > 0) and (asks[0].price <= bids[0].price)):
        ask_order = asks[0]
        bid_order = bids[0]
        if ask_order.price <= bid_order.price:
            trade, bid_order, ask_order = await execute_trade(bid_order, ask_order)
            if not ask_order.is_alive:
                asks.pop(0)
            if not bid_order.is_alive:
                bids.pop(0)
            await commit_trade(trade)

async def reset_session() -> dict:
    """
    Resets the trading session by clearing all orders and trades from the database.

    This function deletes all documents in the order and trade collections, effectively
    resetting the state of the trading session.

    Returns:
        dict: A success message indicating the session was reset successfully.
    """
    mongo_order_collection.delete_many({})
    mongo_trade_collection.delete_many({})

    return {"status": "success", "message": "Session reset successfully"}
