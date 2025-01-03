import json
from app.db.mongodb_client import mongo_order_collection
from app.models.order import Order
from app.services.snapshots import get_order_book_snapshot
from fastapi.responses import JSONResponse
from app.services.order_book import match_orders

async def place_order(order: Order):

    order_id = order.order_id
    order.remaining_quantity = order.quantity
    # fetch current order book from redis
    order_book = await get_order_book_snapshot()
    # add the new order to the order book
    order = order.model_dump_json()
    order = json.loads(order)
    
    mongo_order_collection.insert_one(order)
    await match_orders()
    
    return JSONResponse(content={"status": "success", "order_id": order_id})

# this could be modified using priority queues or hashing
async def modify_order(order_id: str, new_quantity: float):
    
    # fetch the order from mongodb
    order = mongo_order_collection.find_one({"order_id": order_id})
    if order is None:
        return JSONResponse(content={"status": "error", "message": "Order not found"})

    order = Order(**order)
    order.quantity = new_quantity
    order.remaining_quantity = new_quantity
    order = order.model_dump_json()
    order = json.loads(order)
    mongo_order_collection.update_one({"order_id": order_id}, {"$set": order})

    return JSONResponse(content={"status": "success", "order_id": order_id})

async def cancel_order(order_id: str):
    
    # fetch the order from mongodb
    order = mongo_order_collection.find_one({"order_id": order_id})
    if order is None:
        return JSONResponse(content={"status": "error", "message": "Order not found"})
    
    order = Order(**order)
    order.is_alive = False
    order = order.model_dump_json()
    order = json.loads(order)
    mongo_order_collection.update_one({"order_id": order_id}, {"$set": order})
    
    return JSONResponse(content={"status": "success", "order_id": order_id})

async def get_order(order_id: str):
    
    # fetch the order from mongodb
    order = mongo_order_collection.find_one({"order_id": order_id, "is_alive": True})
    if order is None:
        return JSONResponse(content={"status": "error", "message": "Order does not exist or has been cancelled/filled"})
    
    order = Order(**order)
    return order

async def get_all_orders():

    # fetch all orders from mongodb
    orders = mongo_order_collection.find({})
    if orders is None:
        return JSONResponse(content={"status": "error", "message": "No orders found"})

    orders = [Order(**order) for order in orders]
    return orders
