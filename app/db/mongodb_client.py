from pymongo import MongoClient

mongo_client = MongoClient("mongodb://mongo:27017")
mongo_order_db = mongo_client["order_db"]
mongo_order_collection = mongo_order_db["orders"]

mongo_trade_db = mongo_client["trade_db"]
mongo_trade_collection = mongo_trade_db["trades"]