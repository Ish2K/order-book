import os

class Settings:
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://mongo:27017")

settings = Settings()
