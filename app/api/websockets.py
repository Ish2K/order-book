import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.snapshots import get_order_book_snapshot, get_trades

router = APIRouter()

# WebSocket endpoint to stream the order book every 5 seconds
@router.websocket("/orderbook")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Get the current snapshot of the order book
            order_book = await get_order_book_snapshot()  # A function that fetches the current order book
            
            # Send the order book as a JSON object to the client
            await websocket.send_json(order_book.model_dump_json())

            # Wait for 5 seconds before sending the next update
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        print("Client disconnected")

# WebSocket endpoint to listen for trades updates
@router.websocket("/trades")
async def websocket_trades_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        current_trades_size = 0
        while True:
            trades = await get_trades()  # A function that fetches the current trades
                
            # Send the order book as a JSON object to the client
            if current_trades_size != len(trades):
                current_trades_size = len(trades)
                
                # Send the trades as a JSON object to the client
                await websocket.send_json([trade.model_dump_json() for trade in trades])
            
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        print("Client disconnected")
