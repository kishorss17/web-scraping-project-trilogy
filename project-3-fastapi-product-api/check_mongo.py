from pymongo import MongoClient
import sys

try:
    c = MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000)
    ping_result = c.admin.command('ping')
    print('MongoDB ping:', ping_result)
    db = c['ecommerce_db']
    products_count = db['products'].count_documents({})
    quotes_count = db['quotes'].count_documents({})
    print('products count:', products_count)
    print('quotes count:', quotes_count)
    print('SUCCESS: MongoDB is reachable')
except Exception as e:
    print('ERROR: MongoDB NOT reachable:', e)
    sys.exit(1)