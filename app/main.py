"""
Main entry point for the FastAPI application.

This module sets up and configures the FastAPI application, including the routing 
for orders, trades, and websockets. It also serves static files (HTML, CSS, JS) 
from the frontend directory at the root URL.

Key functionalities:
- Includes routers for the `/orders`, `/trades`, and `/ws` endpoints, which handle
  order management, trade processing, and websocket communications respectively.
- Serves static files such as HTML, CSS, and JS for the frontend application from 
  the `frontend` directory.

Dependencies:
- fastapi: The FastAPI framework for building the web API.
- app.api: Includes routers for orders, trades, and websockets.

Example usage:
    To run the FastAPI app:
    uvicorn app.main:app --reload
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import orders, trades, websockets

app = FastAPI()

# Include routers for orders, trades, and websockets
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(trades.router, prefix="/trades", tags=["Trades"])
app.include_router(websockets.router, prefix="/ws", tags=["WebSockets"])

# Serve static files (HTML, CSS, JS) at the root URL
app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
