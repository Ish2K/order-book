from app.db.redis_client import redis_client
from app.db.mongodb_client import mongo_trade_collection, mongo_order_collection
import uuid
from datetime import datetime
from app.services.snapshots import get_order_book_snapshot
from app.models.order import Trade

async def align_order_book():
    
    order_book = await get_order_book_snapshot()
    # sort the bid and ask orders by price
    order_book.bid = sorted(order_book.bid, key=lambda x: x.price, reverse=True)
    order_book.ask = sorted(order_book.ask, key=lambda x: x.price)
    # update the order book in redis
    order_book = order_book.model_dump_json()
    await redis_client.set('order_book', order_book)

    
async def match_orders():
    
    order_book = await get_order_book_snapshot()
    asks = order_book.ask
    bids = order_book.bid
    # match the orders by treating the order book as a priority queue

    while len(asks) > 0 and len(bids) > 0:
        ask_order = asks[0]
        bid_order = bids[0]
        if ask_order.price <= bid_order.price:
            # match the orders and commit the trade to mongodb
            if ask_order.quantity == bid_order.quantity:
                trade = Trade(
                    trade_id=str(uuid.uuid4()),
                    execution_timestamp=datetime.now(),
                    price=ask_order.price,
                    quantity=ask_order.quantity,
                    bid_order_id=bid_order.order_id,
                    ask_order_id=ask_order.order_id
                )

                if(ask_order.traded_quantity > 0):
                    # get weighted average price
                    ask_order.average_traded_price = (ask_order.average_traded_price * ask_order.traded_quantity + ask_order.quantity * ask_order.price) / (ask_order.traded_quantity + ask_order.quantity)
                else:
                    ask_order.average_traded_price = ask_order.price
                
                if(bid_order.traded_quantity > 0):
                    # get weighted average price
                    bid_order.average_traded_price = (bid_order.average_traded_price * bid_order.traded_quantity + bid_order.quantity * bid_order.price) / (bid_order.traded_quantity + bid_order.quantity)
                else:
                    bid_order.average_traded_price = bid_order.price
                    

                ask_order.traded_quantity += ask_order.quantity
                bid_order.traded_quantity += bid_order.quantity
                                
                ask_order.is_alive = False
                bid_order.is_alive = False

                mongo_trade_collection.insert_one(trade.model_dump())
                asks.pop(0)
                bids.pop(0)

                

            elif ask_order.quantity < bid_order.quantity:
                
                trade = Trade(
                    trade_id=str(uuid.uuid4()),
                    execution_timestamp=datetime.now(),
                    price=ask_order.price,
                    quantity=ask_order.quantity,
                    bid_order_id=bid_order.order_id,
                    ask_order_id=ask_order.order_id
                )

                if(ask_order.traded_quantity > 0):
                    # get weighted average price
                    ask_order.average_traded_price = (ask_order.average_traded_price * ask_order.traded_quantity + ask_order.quantity * ask_order.price) / (ask_order.traded_quantity + ask_order.quantity)
                
                else:
                    ask_order.average_traded_price = ask_order.price
                
                if(bid_order.traded_quantity > 0):
                    # get weighted average price
                    bid_order.average_traded_price = (bid_order.average_traded_price * bid_order.traded_quantity + ask_order.quantity * ask_order.price) / (bid_order.traded_quantity + ask_order.quantity)
                
                else:
                    bid_order.average_traded_price = ask_order.price

                ask_order.traded_quantity += ask_order.quantity
                bid_order.traded_quantity += ask_order.quantity

                ask_order.is_alive = False
                bid_order.quantity -= ask_order.quantity
                mongo_trade_collection.insert_one(trade)
                
            else:
                trade = {
                    "trade_id": str(uuid.uuid4()),
                    "timestamp": datetime.now(),
                    "price": ask_order.price,
                    "quantity": bid_order.quantity,
                    "buyer": bid_order.user_id,
                    "seller": ask_order.user_id,
                    "symbol": ask_order.symbol
                }
                mongo_trade_collection.insert_one(trade)
                ask_order.quantity -= bid_order.quantity
                bids.pop(0)
        else:
            break
