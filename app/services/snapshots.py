import json
from app.db.mongodb_client import mongo_order_collection, mongo_trade_collection
from app.models.order import OrderBook, Trade

async def get_order_book_snapshot():
   
    bids = mongo_order_collection.find({"is_alive": True, "side": 1})
    asks = mongo_order_collection.find({"is_alive": True, "side": -1})

    # get top 5 bids and asks by price

    bids = sorted(bids, key=lambda x: x['price'], reverse=True)[:5]
    asks = sorted(asks, key=lambda x: x['price'])[:5]

    return OrderBook(bid=bids, ask=asks)

async def get_trades():
    
    trades = mongo_trade_collection.find()
    trades = [Trade(**trade) for trade in trades]
    return trades