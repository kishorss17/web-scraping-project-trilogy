"""
Catalog Sync & Data Ingestion Utility
Loads crawled products from products.json or raw sources into MongoDB with deduplication.
"""
import os
import json
import logging
from typing import Dict, Any
from pymongo import MongoClient, UpdateOne
from app.config import get_settings
from app.utils.helpers import normalize_product_doc

logger = logging.getLogger("uvicorn.error")


def sync_products_from_file(file_path: str = None) -> Dict[str, Any]:
    """
    Synchronizes product records from Scrapy JSON export into MongoDB.
    Normalizes dirty values and performs bulk upsert operations.
    """
    settings = get_settings()

    if file_path is None:
        # Default relative path from project-3 to project-1 products.json
        # __file__ is project-3/app/utils/data_loader.py -> dirname 4 times reaches workspace root
        workspace_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        file_path = os.path.join(workspace_dir, "project-1-scrapy-ecommerce-crawler", "products.json")

    if not os.path.exists(file_path):
        return {
            "success": False,
            "error": f"File not found: {file_path}",
            "processed": 0,
            "upserted": 0
        }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            items = json.load(f)

        client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        db = client[settings.DATABASE_NAME]
        col = db[settings.PRODUCTS_COLLECTION]

        operations = []
        for raw_item in items:
            normalized = normalize_product_doc(raw_item)
            # Remove MongoDB internal string id to let MongoDB generate or preserve its own _id
            normalized.pop("id", None)
            
            operations.append(
                UpdateOne(
                    {"product_id": normalized["product_id"]},
                    {"$set": normalized},
                    upsert=True
                )
            )

        if operations:
            result = col.bulk_write(operations, ordered=False)
            upserted_count = result.upserted_count + result.modified_count
        else:
            upserted_count = 0

        client.close()

        return {
            "success": True,
            "file_source": file_path,
            "total_items_in_file": len(items),
            "operations_executed": len(operations),
            "upserted_or_modified": upserted_count
        }

    except Exception as e:
        logger.error(f"Error during catalog synchronization: {e}")
        return {
            "success": False,
            "error": str(e),
            "processed": 0,
            "upserted": 0
        }


def normalize_existing_collection() -> Dict[str, Any]:
    """
    Cleans up any un-normalized records already in the MongoDB collection
    (e.g., converts string prices '£51.77' to floats, cleans '3/5' ratings, etc.)
    """
    settings = get_settings()
    try:
        client = MongoClient(settings.MONGODB_URL, serverSelectionTimeoutMS=5000)
        db = client[settings.DATABASE_NAME]
        col = db[settings.PRODUCTS_COLLECTION]

        cursor = col.find({})
        operations = []
        updated_count = 0

        for doc in cursor:
            normalized = normalize_product_doc(doc)
            doc_id = doc["_id"]
            normalized.pop("id", None)
            
            operations.append(
                UpdateOne(
                    {"_id": doc_id},
                    {"$set": normalized}
                )
            )

            if len(operations) >= 500:
                col.bulk_write(operations, ordered=False)
                updated_count += len(operations)
                operations = []

        if operations:
            col.bulk_write(operations, ordered=False)
            updated_count += len(operations)

        client.close()
        return {
            "success": True,
            "records_normalized": updated_count
        }
    except Exception as e:
        logger.error(f"Error during catalog normalization: {e}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    print("Executing standalone Catalog Sync...")
    sync_res = sync_products_from_file()
    print("Sync Result:", sync_res)
    norm_res = normalize_existing_collection()
    print("Normalization Result:", norm_res)
