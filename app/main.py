from fastapi import FastAPI
from app.api import orders, trades, websockets

app = FastAPI()

# Include routers for orders, trades, and websockets
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(trades.router, prefix="/trades", tags=["Trades"])
app.include_router(websockets.router, prefix="/ws", tags=["WebSockets"])
