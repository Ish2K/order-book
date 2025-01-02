import os

class Settings:
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")

settings = Settings()
