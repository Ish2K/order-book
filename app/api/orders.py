from fastapi import APIRouter, Form
from app.services.order_processing import (
    place_order, 
    get_order_book_snapshot, 
    modify_order, 
    cancel_order, 
    get_order, 
    get_all_orders
)
from app.services.order_book import reset_session
from app.models.order import Order, OrderBook
import uuid
from typing import Union

router = APIRouter()

#--------------------
# Endpoint Functions
#--------------------

@router.post("/place", response_model = dict)
async def place_order_endpoint(
    side: int = Form(...),  # Expect side as form parameter
    price: float = Form(...),  # Expect price as form parameter
    quantity: float = Form(...)  # Expect quantity as form parameter
):
    """
    Place a new order in the order book.

    Parameters:
    - side (int): The side of the order (1 for buy, 0 for sell).
    - price (float): The price of the order.
    - quantity (float): The quantity of the order.

    Returns:
    - dict: The result of the order placement process.
    """
    order = Order(side=side, price=price, quantity=quantity)
    order_id = str(uuid.uuid4())
    order.order_id = order_id

    result = await place_order(order)
    return result

@router.get("/order_book_snapshot", response_model = OrderBook)
async def order_book_snapshot():
    """
    Retrieve a snapshot of the current order book.

    Returns:
    - OrderBook: The current state of the order book.
    """
    order_book = await get_order_book_snapshot()
    return order_book

@router.get("/fetch_order", response_model = Union[Order, dict])
async def get_order_details(order_id: str):
    """
    Fetch details of a specific order by its order ID.

    Parameters:
    - order_id (str): The unique identifier of the order.

    Returns:
    - Order Object: The details of the order.
    - dict: A JSON response indicating an error if the operation fails.
    """
    result = await get_order(order_id)
    return result

@router.get("/fetch_all_orders", response_model=Union[list[Order], dict])
async def all_orders():
    """
    Retrieve a list of all orders in the system.

    Returns:
    - list: A list of all orders.
    - dict: A JSON response indicating an error if the operation fails.
    """
    result = await get_all_orders()
    return result

@router.put("/modify", response_model = dict)
async def modify_order_endpoint(
    order_id: str = Form(...),  # Expect order_id as form parameter
    new_price: float = Form(...)  # Expect new_price as form parameter
):
    """
    Modify an existing order with a new price.

    Parameters:
    - order_id (str): The unique identifier of the order to modify.
    - new_price (float): The new price for the order.

    Returns:
    - dict: The result of the order modification process.
    """
    result = await modify_order(order_id, new_price)
    return result

@router.delete("/cancel", response_model = dict)
async def cancel_order_endpoint(
    order_id: str = Form(...)  # Expect order_id as form parameter
):
    """
    Cancel an existing order by its order ID.

    Parameters:
    - order_id (str): The unique identifier of the order to cancel.

    Returns:
    - dict: The result of the order cancellation process.
    """
    result = await cancel_order(order_id)
    return result

@router.post("/reset", response_model = dict)
async def reset_current_session():
    """
    Reset the current order book session.
    This will delete all orders and trades from the system.

    Returns:
    - dict: The result of the session reset operation.
    """
    result = await reset_session()
    return result
