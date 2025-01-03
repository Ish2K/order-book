import json
import redis
from fastapi import WebSocket
from typing import List

from app.db.redis_client import redis_client

# Active WebSocket connections
active_connections: List[WebSocket] = []

async def broadcast_order_book_update():
    
    # fetch the order book from redis
    order_book = await redis_client.get('order_book')
    if order_book is None:
        return
    
    # broadcast the order book to all active connections
    for connection in active_connections:
        await connection.send_text(order_book)