from fastapi import APIRouter
from app.db.mongodb_client import mongo_client
from app.models.order import Trade

router = APIRouter()

@router.get("/all_trades")
async def all_trades():
    trades = await mongo_client.db["trades"].find().to_list(100)
    return trades
