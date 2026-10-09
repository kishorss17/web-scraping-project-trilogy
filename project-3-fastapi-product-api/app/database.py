"""
Async MongoDB Database handler using Motor
"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
import pymongo
from app.config import get_settings

logger = logging.getLogger("uvicorn.error")


class Database:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db_instance = Database()


async def connect_to_mongo():
    """Establish async MongoDB connection pool and ensure required indexes."""
    settings = get_settings()
    logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}...")
    try:
        db_instance.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,
            maxPoolSize=50,
            minPoolSize=10
        )
        # Verify connectivity
        await db_instance.client.admin.command("ping")
        db_instance.db = db_instance.client[settings.DATABASE_NAME]
        logger.info(f"✓ Connected to MongoDB database: {settings.DATABASE_NAME}")

        # Automatically create performance indexes
        await create_indexes()

    except Exception as e:
        logger.error(f"✗ Failed to connect to MongoDB: {e}")
        raise e


async def close_mongo_connection():
    """Gracefully close MongoDB connection pool."""
    if db_instance.client:
        logger.info("Closing MongoDB connection...")
        db_instance.client.close()
        logger.info("MongoDB connection closed.")


async def create_indexes():
    """Create optimized indexes for fast querying, filtering, and text search."""
    settings = get_settings()
    try:
        products_col = db_instance.db[settings.PRODUCTS_COLLECTION]
        
        # 1. Unique index on product_id
        await products_col.create_index(
            [("product_id", pymongo.ASCENDING)],
            unique=True,
            background=True,
            sparse=True
        )

        # 2. Compound index on category + price for filtered catalog queries
        await products_col.create_index(
            [("category", pymongo.ASCENDING), ("price", pymongo.ASCENDING)],
            background=True
        )

        # 3. Index on price
        await products_col.create_index(
            [("price", pymongo.ASCENDING)],
            background=True
        )

        # 4. Index on rating
        await products_col.create_index(
            [("rating", pymongo.DESCENDING)],
            background=True
        )

        # 5. Text search index on title and category
        existing_indexes = await products_col.index_information()
        if "product_text_search" not in existing_indexes:
            await products_col.create_index(
                [("title", pymongo.TEXT), ("category", pymongo.TEXT), ("name", pymongo.TEXT)],
                name="product_text_search",
                background=True
            )

        # 6. Quotes indexes
        quotes_col = db_instance.db[settings.QUOTES_COLLECTION]
        await quotes_col.create_index([("author", pymongo.ASCENDING)], background=True)
        await quotes_col.create_index([("tags", pymongo.ASCENDING)], background=True)

        logger.info("✓ MongoDB indexes successfully verified/created.")
    except Exception as e:
        logger.warning(f"Notice during index creation: {e}")


def get_database() -> AsyncIOMotorDatabase:
    """Dependency helper to get the database instance."""
    return db_instance.db


def get_products_collection() -> AsyncIOMotorCollection:
    """Dependency helper to get products collection."""
    settings = get_settings()
    return db_instance.db[settings.PRODUCTS_COLLECTION]


def get_quotes_collection() -> AsyncIOMotorCollection:
    """Dependency helper to get quotes collection."""
    settings = get_settings()
    return db_instance.db[settings.QUOTES_COLLECTION]
