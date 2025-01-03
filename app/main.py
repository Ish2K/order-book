from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import orders, trades, websockets

app = FastAPI()

# Include routers for orders, trades, and websockets
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(trades.router, prefix="/trades", tags=["Trades"])
app.include_router(websockets.router, prefix="", tags=["WebSockets"])

# Serve static files (HTML, CSS, JS) at the root URL
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
