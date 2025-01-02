from fastapi import APIRouter, HTTPException
from app.models.order import Order
from app.services.order_book import match_orders

router = APIRouter()

@router.post("/place", response_model=str)
async def place_order(side: int, price: float, quantity: int):
    # Logic for placing an order
    # Trigger match_orders after placing
    return order_id
