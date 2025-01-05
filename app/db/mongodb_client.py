"""
MongoDB Client for interacting with the Order and Trade collections.

This module initializes a connection to MongoDB using the URL specified
in the application settings. It sets up two collections:
- "orders" in the "order_db" database
- "trades" in the "trade_db" database

The connection is established using the MongoClient from pymongo. This module
can be imported wherever interaction with the Order or Trade collections is required.

Dependencies:
- pymongo.MongoClient: MongoDB client to interact with the database.
- app.config.settings.settings: Application settings containing the MongoDB URL.

Example usage:
    from app.db.mongodb_client import mongo_order_collection, mongo_trade_collection
"""

from pymongo import MongoClient
from app.config.settings import settings

# Establish a connection to the MongoDB client using the provided URL from settings.
mongo_client = MongoClient(settings.mongo_url)

# Define the databases and their respective collections.
mongo_order_db = mongo_client["order_db"]
mongo_order_collection = mongo_order_db["orders"]

mongo_trade_db = mongo_client["trade_db"]
mongo_trade_collection = mongo_trade_db["trades"]
