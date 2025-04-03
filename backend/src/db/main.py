from motor.motor_asyncio import AsyncIOMotorClient
from ..config import Config  
from typing import AsyncGenerator
from pymongo import MongoClient

client = AsyncIOMotorClient(Config.DATABASE_URL)
db = client["QQ"]

async def init_db():
    try:
        await client.server_info()
        print("connect success")
    except Exception as e:
        print("Connection failed:", e)

async def get_db() -> AsyncGenerator:
    yield db
class MongoDB:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017")
        self.db = self.client["QQ"]
        self.device_collection = self.db["record_device"]
        self.user_collection = self.db["user"]