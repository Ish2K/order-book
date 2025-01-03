import json
from app.db.redis_client import redis_client
from app.db.mongodb_client import mongo_order_collection
from app.models.order import Order, OrderBook
from app.service.order_book import align_order_book
from app.services.snapshots import get_order_book_snapshot
from fastapi.responses import JSONResponse

async def place_order(order: Order):

    # fetch current order book from redis
    order_book = await get_order_book_snapshot()
    # add the new order to the order book
    if order.side == 1:
        order_book.bid.append(order)
    elif order.side == -1:
        order_book.ask.append(order)
    
    order_id = order.order_id

    # serialize the order book
    order_book = order_book.model_dump_json()

    # store the order book in redis
    await redis_client.set('order_book', order_book)
    await align_order_book()
    
    # store the order in mongodb
    order = order.model_dump_json()
    order = json.loads(order)
    
    mongo_order_collection.insert_one(order)
    
    return JSONResponse(content={"status": "success", "order_id": order_id})

# this could be modified using priority queues or hashing
async def modify_order(order_id: str, new_quantity: float):
    
    order_book = await get_order_book_snapshot()
    found = False
    for order in order_book.bid:
        if order.order_id == order_id:
            order.quantity = new_quantity
            found = True
            break

    if not found:
        for order in order_book.ask:
            if order.order_id == order_id:
                order.quantity = new_quantity
                found = True
                break
    
    if(not found):
        return JSONResponse(content={"status": "error", "message": "Order not found"})

    order_book = order_book.model_dump_json()
    await redis_client.set('order_book', order_book)
    await align_order_book()

    return JSONResponse(content={"status": "success", "order_id": order_id})

async def cancel_order(order_id: str):
    
    order_book = await get_order_book_snapshot()
    found = False
    for order in order_book.bid:
        if order.order_id == order_id:
            order_book.bid.remove(order)
            found = True
            break

    if not found:
        for order in order_book.ask:
            if order.order_id == order_id:
                order_book.ask.remove(order)
                break
    
    if(not found):
        return JSONResponse(content={"status": "error", "message": "Order not found"})

    order_book = order_book.model_dump_json()
    await redis_client.set('order_book', order_book)
    await align_order_book()

    return JSONResponse(content={"status": "success", "order_id": order_id})

async def get_order(order_id: str):
    
    # fetch the order from mongodb
    order = mongo_order_collection.find_one({"order_id": order_id})
    if order is None:
        return JSONResponse(content={"status": "error", "message": "Order not found"})
    
    order = Order(**order)
    return order

async def get_all_orders():

    # fetch all orders from mongodb
    orders = mongo_order_collection.find({})
    if orders is None:
        return JSONResponse(content={"status": "error", "message": "No orders found"})

    orders = [Order(**order) for order in orders]
    return orders
