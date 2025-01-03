from app.db.mongodb_client import mongo_trade_collection, mongo_order_collection
import uuid
from datetime import datetime
from app.models.order import Trade, Order
import json
from app.models.order import OrderBook

async def get_order_book():

    bids = mongo_order_collection.find({"is_alive": True, "side": 1})
    asks = mongo_order_collection.find({"is_alive": True, "side": -1})

    # get top 5 bids and asks by price

    bids = sorted(bids, key=lambda x: x['price'], reverse=True)
    asks = sorted(asks, key=lambda x: x['price'])

    # return the order book snapshot
    order_book = OrderBook(bid=bids, ask=asks)

    # return non-str version of order book
    return order_book

async def commit_trade(trade: Trade):
    
    trade = trade.model_dump_json()
    trade = json.loads(trade)
    mongo_trade_collection.insert_one(trade)

    return {"status": "success", "message": "Trade committed successfully"}

async def modify_order(order: Order):

    order = order.model_dump_json()
    order = json.loads(order)
    mongo_order_collection.update_one({"order_id": order["order_id"]}, {"$set": order})

    return {"status": "success", "message": "Order modified successfully"}


async def execute_trade(bid_order: Order, ask_order: Order):

    # calculate the trade price
    trade_price = (bid_order.price + ask_order.price) / 2
    trade_quantity = min(bid_order.remaining_quantity, ask_order.remaining_quantity)

    if bid_order.traded_quantity > 0:
        # get the weighted average price
        bid_order.average_traded_price = (bid_order.average_traded_price * bid_order.traded_quantity + trade_price * trade_quantity) / (bid_order.traded_quantity + trade_quantity)
    else:
        bid_order.average_traded_price = trade_price
    
    if ask_order.traded_quantity > 0:
        # get the weighted average price
        ask_order.average_traded_price = (ask_order.average_traded_price * ask_order.traded_quantity + trade_price * trade_quantity) / (ask_order.traded_quantity + trade_quantity)
    else:
        ask_order.average_traded_price = trade_price

    # update the bid order
    bid_order.traded_quantity += trade_quantity
    bid_order.remaining_quantity -= trade_quantity
    bid_order.is_alive = bid_order.remaining_quantity > 0

    # update the ask order
    ask_order.traded_quantity += trade_quantity
    ask_order.remaining_quantity -= trade_quantity
    ask_order.is_alive = ask_order.remaining_quantity > 0

    # create a trade object
    trade_id = str(uuid.uuid4())
    trade = Trade(
        trade_id=trade_id,
        execution_timestamp=datetime.now(),
        price=trade_price,
        quantity=trade_quantity,
        bid_order_id=bid_order.order_id,
        ask_order_id=ask_order.order_id
    )

    await modify_order(bid_order)
    await modify_order(ask_order)

    return trade, bid_order, ask_order
    
async def match_orders():
    
    order_book = await get_order_book()
    asks = order_book.ask
    bids = order_book.bid
    # match the orders by treating the order book as a priority queue

    while (len(asks) > 0 and len(bids) > 0):
        ask_order = asks[0]
        bid_order = bids[0]
        if ask_order.price <= bid_order.price:
            trade, bid_order, ask_order = await execute_trade(bid_order, ask_order)
            if(ask_order.is_alive == False):
                asks.pop(0)
            if(bid_order.is_alive == False):
                bids.pop(0)
            await commit_trade(trade)
            

async def reset_session():

    # remove all orders & trades from the mongodb
    mongo_order_collection.delete_many({})
    mongo_trade_collection.delete_many({})

    return {"status": "success", "message": "Session reset successfully"}
