import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.snapshots import get_order_book_snapshot  # Assuming this function gets order book from Redis or in-memory

router = APIRouter()

# WebSocket endpoint to stream the order book every 5 seconds
@router.websocket("/ws/orderbook")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Get the current snapshot of the order book
            order_book = await get_order_book_snapshot()  # A function that fetches the current order book
            order_book.bid = order_book.bid[:5]
            order_book.ask = order_book.ask[:5]
            
            # Send the order book as a JSON object to the client
            await websocket.send_json(order_book.model_dump_json())

            # Wait for 5 seconds before sending the next update
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print("Client disconnected")

# WebSocket endpoint to listen for trades updates
@router.websocket("/trades")
async def websocket_trades_endpoint(websocket: WebSocket):
    pass
