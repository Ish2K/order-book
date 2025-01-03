import os

class Settings:
    redis_url: str = os.getenv("REDIS_URL", "redis://redis:6379")
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://mongo:27017")

settings = Settings()
