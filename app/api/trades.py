from fastapi import APIRouter
from app.services.snapshots import get_trades

router = APIRouter()

@router.get("/all", response_model = list)
async def all_trades():
    """
    Retrieve all trade records.

    Returns:
    - list: A list of all trade records.
    """
    trades = await get_trades()
    return trades
