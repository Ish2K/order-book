from fastapi import APIRouter
from app.services.snapshots import get_trades

router = APIRouter()

@router.get("/all")
async def all_trades():

    trades = await get_trades()
    return trades
