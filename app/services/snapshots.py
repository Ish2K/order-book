import json
from app.db.redis_client import redis_client
from app.models.order import OrderBook

async def get_order_book_snapshot():

    # fetch the order book from redis
    order_book = await redis_client.get('order_book')
    if order_book is None:
        order_book = OrderBook(bid=[], ask=[])
    else:
        order_book = json.loads(order_book)
        order_book = OrderBook(**order_book)        

    return order_book