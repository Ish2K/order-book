"""
Service module for managing order processing in a trading system.

This module includes functions for placing, modifying, canceling, retrieving,
and fetching all orders from the order collection in the database. It also interacts
with the order book and triggers order matching after placing or modifying orders.

Dependencies:
- app.db.mongodb_client: MongoDB collections for orders.
- app.models.order: Pydantic models for Order.
- app.services.snapshots: Function to get a snapshot of the order book.
- app.services.order_book: Function to match orders in the order book.
- fastapi.responses: Used to send JSON responses.

Example usage:
    from app.services.order_processing import place_order, modify_order, cancel_order
"""

import json
from app.db.mongodb_client import mongo_order_collection
from app.models.order import Order
from app.services.snapshots import get_order_book_snapshot
from fastapi.responses import JSONResponse
from app.services.order_book import match_orders

async def place_order(order: Order) -> JSONResponse:
    """
    Places a new order by adding it to the order book and triggering the order matching process.

    The order is inserted into the MongoDB collection, and the order book is updated. Afterward,
    the matching process is triggered to execute possible trades.

    Args:
        order (Order): The order to be placed.

    Returns:
        JSONResponse: A JSON response indicating the success of the order placement, along with the order ID.
    """
    order_id = order.order_id
    order.remaining_quantity = order.quantity
    # fetch current order book from the snapshot
    order_book = await get_order_book_snapshot()
    # add the new order to the order book
    order = order.model_dump_json()
    order = json.loads(order)
    
    mongo_order_collection.insert_one(order)
    await match_orders()
    
    return JSONResponse(content={"status": "success", "order_id": order_id})

async def modify_order(order_id: str, new_price: float) -> JSONResponse:
    """
    Modifies the price of an existing order and triggers the order matching process.

    The order's price is updated in the MongoDB collection. Afterward, the matching process is triggered
    to ensure trades are executed where applicable.

    Args:
        order_id (str): The ID of the order to be modified.
        new_price (float): The new price for the order.

    Returns:
        JSONResponse: A JSON response indicating the success of the modification, along with the order ID.
    """
    # fetch the order from mongodb
    order = mongo_order_collection.find_one({"order_id": order_id})
    if order is None:
        return JSONResponse(content={"status": "error", "message": "Order not found"})

    order = Order(**order)
    order.price = new_price
    order = order.model_dump_json()
    order = json.loads(order)
    mongo_order_collection.update_one({"order_id": order_id}, {"$set": order})
    await match_orders()

    return JSONResponse(content={"status": "success", "order_id": order_id})

async def cancel_order(order_id: str) -> JSONResponse:
    """
    Cancels an existing order by marking it as inactive in the database.

    The order's `is_alive` status is set to `False` in the MongoDB collection to mark it as canceled.

    Args:
        order_id (str): The ID of the order to be canceled.

    Returns:
        JSONResponse: A JSON response indicating the success of the cancellation, along with the order ID.
    """
    # fetch the order from mongodb
    order = mongo_order_collection.find_one({"order_id": order_id})
    if order is None:
        return JSONResponse(content={"status": "error", "message": "Order not found"})
    
    order = Order(**order)
    order.is_alive = False
    order = order.model_dump_json()
    order = json.loads(order)
    mongo_order_collection.update_one({"order_id": order_id}, {"$set": order})
    
    return JSONResponse(content={"status": "success", "order_id": order_id})

async def get_order(order_id: str) -> Order | JSONResponse:
    """
    Retrieves an order by its ID from the database.

    This function returns the order if found, or a JSON error response if the order doesn't exist.

    Args:
        order_id (str): The ID of the order to retrieve.

    Returns:
        Order or JSONResponse: The retrieved order if found, or an error response if not.
    """
    # fetch the order from mongodb
    order = mongo_order_collection.find_one({"order_id": order_id})
    if order is None:
        return JSONResponse(content={"status": "error", "message": "Order does not exist"})
    
    order = Order(**order)
    return order

async def get_all_orders() -> list[Order] | JSONResponse:
    """
    Retrieves all orders from the database.

    This function returns a list of all orders in the database or a JSON error response if no orders are found.

    Returns:
        list[Order] or JSONResponse: A list of all orders if found, or an error response if no orders exist.
    """
    # fetch all orders from mongodb
    orders = mongo_order_collection.find({})
    if orders is None:
        return JSONResponse(content={"status": "error", "message": "No orders found"})

    orders = [Order(**order) for order in orders]
    return orders
