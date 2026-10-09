from itemadapter import ItemAdapter
from datetime import datetime
import pymongo
import logging


class DataCleaningPipeline:
    """Pipeline for cleaning and validating scraped data"""

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Clean price - remove currency symbols and convert to float
        if adapter.get('price'):
            price_str = str(adapter['price']).replace('£', '').replace('$', '').strip()
            try:
                adapter['price'] = float(price_str)
            except ValueError:
                adapter['price'] = 0.0

        # Clean rating - convert to float
        if adapter.get('rating'):
            try:
                adapter['rating'] = float(adapter['rating'])
            except ValueError:
                adapter['rating'] = 0.0

        # Add scraped timestamp
        adapter['scraped_date'] = datetime.utcnow().isoformat()

        # Set default currency if not present
        if not adapter.get('currency'):
            adapter['currency'] = 'GBP'

        return item


class MongoPipeline:
    """Pipeline for storing items in MongoDB"""

    collection_name = 'products'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'ecommerce_db')
        )

    def open_spider(self, spider):
        """Connect to MongoDB when spider opens"""
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        spider.logger.info(f'Connected to MongoDB: {self.mongo_db}')

    def close_spider(self, spider):
        """Close MongoDB connection when spider closes"""
        self.client.close()
        spider.logger.info('MongoDB connection closed')

    def process_item(self, item, spider):
        """Insert item into MongoDB collection"""
        try:
            # Convert item to dict
            item_dict = ItemAdapter(item).asdict()

            # Update or insert (upsert) based on product_id
            self.db[self.collection_name].update_one(
                {'product_id': item_dict['product_id']},
                {'$set': item_dict},
                upsert=True
            )
            spider.logger.debug(f'Product saved to MongoDB: {item_dict.get("title")}')

        except Exception as e:
            spider.logger.error(f'Error saving to MongoDB: {e}')

        return item
