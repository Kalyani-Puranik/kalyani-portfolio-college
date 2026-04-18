"""MongoDB connection using Motor (async driver)."""

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
import os
from models.blog import Blog
from models.project import Project
from models.contact import Contact
from models.analytics import Analytics
from models.photo import Photo


_client: AsyncIOMotorClient = None


async def connect_db():
    global _client
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    _client = AsyncIOMotorClient(mongo_uri)
    db = _client[os.getenv("DB_NAME", "kalyani_portfolio")]

    await init_beanie(
        database=db,
        document_models=[Blog, Project, Contact, Analytics, Photo]
    )
    print("✅ MongoDB connected successfully")


async def disconnect_db():
    global _client
    if _client:
        _client.close()
        print("🔌 MongoDB disconnected")


def get_database():
    global _client
    return _client[os.getenv("DB_NAME", "kalyani_portfolio")]
