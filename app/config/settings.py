import os

class Settings:
    """
    A class to manage application settings and configuration.

    Attributes:
    - mongo_url (str): The URL for connecting to the MongoDB database. Defaults to "mongodb://mongo:27017" if not provided as an environment variable.
    """
    mongo_url: str = os.getenv("MONGO_URL", "mongodb://mongo:27017")

settings = Settings()
