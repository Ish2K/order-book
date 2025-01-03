import redis.asyncio as redis

redis_client = redis.Redis(host="redis", port=6379, db=0)
# connect to Redis server
# print(redis_client.ping())

# Redis order operations (e.g., zadd, hset, zrem, etc.)
