"""
Database handler for MongoDB operations
"""
import pymongo
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MongoDBHandler:
    """Handles all MongoDB operations"""

    def __init__(self, mongo_uri, database_name, collection_name):
        """
        Initialize MongoDB connection

        Args:
            mongo_uri: MongoDB connection string
            database_name: Database name
            collection_name: Collection name
        """
        self.mongo_uri = mongo_uri
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    def connect(self):
        """Establish connection to MongoDB"""
        try:
            self.client = pymongo.MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=5000
            )
            # Test connection
            self.client.server_info()
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]
            logger.info(f"✓ Connected to MongoDB: {self.database_name}.{self.collection_name}")
            return True
        except Exception as e:
            logger.error(f"✗ MongoDB connection failed: {e}")
            return False

    def save_quote(self, quote_data):
        """
        Save quote to MongoDB with upsert

        Args:
            quote_data: Dictionary containing quote information
        """
        try:
            # Add timestamp
            quote_data['scraped_date'] = datetime.utcnow().isoformat()

            # Upsert (update if exists, insert if new)
            result = self.collection.update_one(
                {'text': quote_data['text']},  # Match on quote text
                {'$set': quote_data},
                upsert=True
            )

            if result.upserted_id:
                logger.debug(f"Inserted new quote: {quote_data['text'][:50]}...")
            else:
                logger.debug(f"Updated existing quote: {quote_data['text'][:50]}...")

            return True
        except Exception as e:
            logger.error(f"Error saving quote: {e}")
            return False

    def get_quote_count(self):
        """Get total number of quotes in database"""
        try:
            count = self.collection.count_documents({})
            return count
        except Exception as e:
            logger.error(f"Error counting quotes: {e}")
            return 0

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")
