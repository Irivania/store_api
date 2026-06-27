import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from store.core.config import settings

class MongoClient:
    def __init__(self):
        self._client = None
        self._db = None
        self._loop = None

    def get(self):
        loop = asyncio.get_running_loop()

        if self._client is not None and self._loop is not loop:
            self._client.close()
            self._client = None
            self._db = None
            self._loop = None

        if self._client is None:
            self._client = AsyncIOMotorClient(
                settings.DATABASE_URL,
                uuidRepresentation='standard',
            )
            self._db = self._client.get_database("store")
            self._loop = loop

        return self._db

    def close(self):
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
            self._loop = None

db_client = MongoClient()