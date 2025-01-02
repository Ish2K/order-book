from fastapi import APIRouter, WebSocket
from app.services.snapshots import get_order_book_snapshot

router = APIRouter()

@router.websocket("/ws/order_book")
async def order_book_snapshot(websocket: WebSocket):
    await websocket.accept()
    while True:
        snapshot = await get_order_book_snapshot(levels=5)
        await websocket.send_json(snapshot)
