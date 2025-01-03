from fastapi import APIRouter
from app.db.mongodb_client import mongo_client
from app.models.order import Trade

router = APIRouter()

@router.get("/all")
async def all_trades():
    trades = []
    return trades
