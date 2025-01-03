from fastapi import APIRouter, Form
from app.services.order_processing import place_order, get_order_book_snapshot
from app.services.order_processing import modify_order, cancel_order, get_order, get_all_orders
from pydantic import BaseModel
from app.models.order import Order
import uuid


router = APIRouter()

@router.post("/place")
async def place_order_endpoint(
    side: int = Form(...),  # Expect side as form parameter
    price: float = Form(...),  # Expect price as form parameter
    quantity: float = Form(...),  # Expect quantity as form parameter
):

    order = Order(side=side, price=price, quantity=quantity)
    order_id = str(uuid.uuid4())
    order.order_id = order_id

    result = await place_order(order)
    return result

@router.get("/order_book_snapshot")
async def order_book_snapshot():
    order_book = await get_order_book_snapshot()
    return order_book

@router.get("/fetch_order")
async def get_order_details(order_id: str):

    result = await get_order(order_id)
    return result

@router.get("/fetch_all_orders")
async def all_orders():
    result = await get_all_orders()
    return result

@router.put("/modify")
async def modify_order_endpoint(
    order_id: str = Form(...),  # Expect order_id as form parameter
    new_quantity: float = Form(...),  # Expect new_quantity as form parameter
):
    result = await modify_order(order_id, new_quantity)
    return result

@router.delete("/cancel")
async def cancel_order_endpoint(
    order_id: str = Form(...),  # Expect order_id as form parameter
):
    result = await cancel_order(order_id)
    return result
