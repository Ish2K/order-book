from fastapi import APIRouter
from app.services.snapshots import get_trades

router = APIRouter()

@router.get("/all")
async def all_trades() -> list:
    """
    Retrieve all trade records.

    Returns:
    - list: A list of all trade records.
    """
    trades = await get_trades()
    return trades
