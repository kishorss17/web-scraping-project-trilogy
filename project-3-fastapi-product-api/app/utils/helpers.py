"""
Data normalization, parsing, and pagination helpers
"""
import re
import math
from datetime import datetime, timezone
from typing import Any, Dict, Optional


RATING_MAP = {
    "one": 1.0,
    "two": 2.0,
    "three": 3.0,
    "four": 4.0,
    "five": 5.0,
}


def clean_price(price_val: Any) -> float:
    """
    Safely convert price to float.
    Handles float, int, or dirty strings like '£51.77', '$45.17', '45.17'.
    """
    if price_val is None:
        return 0.0
    if isinstance(price_val, (int, float)):
        return float(price_val)
    
    val_str = str(price_val).strip()
    # Extract numeric portion including decimal
    match = re.search(r"(\d+(\.\d+)?)", val_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0
    return 0.0


def clean_rating(rating_val: Any) -> float:
    """
    Safely convert rating to float between 0.0 and 5.0.
    Handles numbers, fraction strings like '3/5', or words like 'Three'.
    """
    if rating_val is None:
        return 0.0
    if isinstance(rating_val, (int, float)):
        return float(rating_val)
    
    val_str = str(rating_val).strip().lower()
    
    # Check word map
    for word, num in RATING_MAP.items():
        if word in val_str:
            return num
            
    # Check fraction format e.g., '3/5' or '4.5/5'
    if "/" in val_str:
        parts = val_str.split("/")
        try:
            return float(parts[0].strip())
        except ValueError:
            pass

    # Generic number match
    match = re.search(r"(\d+(\.\d+)?)", val_str)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return 0.0

    return 0.0


def clean_availability(avail_val: Any) -> str:
    """
    Clean availability string, removing messy newlines and excessive whitespace.
    """
    if not avail_val:
        return "Unknown"
    
    text = str(avail_val)
    # Take the first non-empty line
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    if lines:
        first_line = lines[0]
        # Clean up repeated spaces
        return re.sub(r"\s+", " ", first_line)
    return "Unknown"


def clean_scraped_date(date_val: Any) -> str:
    """
    Normalize scraped timestamp to ISO 8601 string.
    """
    if isinstance(date_val, datetime):
        return date_val.isoformat()
    if isinstance(date_val, str) and date_val.strip():
        return date_val.strip()
    return datetime.now(timezone.utc).isoformat()


def normalize_product_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalize a raw MongoDB product document into a standard dictionary.
    Handles schema differences across crawler revisions.
    """
    if not doc:
        return {}

    doc_id = str(doc.get("_id", "")) if "_id" in doc else None
    product_id = doc.get("product_id") or (f"prod_{doc_id}" if doc_id else "unknown")
    title = doc.get("title") or doc.get("name") or "Untitled Product"
    price = clean_price(doc.get("price"))
    rating = clean_rating(doc.get("rating"))
    availability = clean_availability(doc.get("availability"))
    category = doc.get("category") or "Default"
    currency = doc.get("currency") or "GBP"
    discount = float(doc.get("discount", 0.0) or 0.0)
    reviews_count = int(doc.get("reviews_count", 0) or 0)
    url = doc.get("url")
    image_url = doc.get("image_url")
    scraped_date = clean_scraped_date(doc.get("scraped_date") or doc.get("scraped_at"))
    source_website = doc.get("source_website") or doc.get("platform") or "books.toscrape.com"
    original_price = doc.get("original_price")
    if original_price is not None:
        try:
            original_price = float(original_price)
        except (ValueError, TypeError):
            original_price = price
    else:
        original_price = price

    return {
        "id": doc_id,
        "product_id": str(product_id),
        "title": title,
        "url": url,
        "price": price,
        "original_price": original_price,
        "discount": discount,
        "currency": currency,
        "rating": rating,
        "reviews_count": reviews_count,
        "availability": availability,
        "category": category,
        "image_url": image_url,
        "scraped_date": scraped_date,
        "source_website": source_website,
    }


def compute_pagination(total: int, page: int, page_size: int) -> Dict[str, Any]:
    """
    Calculate pagination metadata.
    """
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1,
    }
