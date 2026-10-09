"""
Products API Router
Provides paginated listings, advanced filtering, full-text search, and full CRUD operations.
"""
import re
from typing import Optional, List
from bson import ObjectId
from fastapi import APIRouter, Depends, Query, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection
import pymongo

from app.dependencies import get_products_col, verify_api_key
from app.models import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    PaginatedResponse,
    MessageResponse,
)
from app.utils.helpers import normalize_product_doc, compute_pagination

router = APIRouter(prefix="/api/v1/products", tags=["Products Catalog"])


@router.get(
    "",
    response_model=PaginatedResponse[ProductResponse],
    summary="List products with filters & pagination",
    description="Retrieve paginated product catalog with dynamic filtering by category, price range, minimum rating, and availability."
)
async def list_products(
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    category: Optional[str] = Query(None, description="Filter by category name"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    min_rating: Optional[float] = Query(None, ge=0, le=5.0, description="Minimum star rating filter"),
    availability: Optional[str] = Query(None, description="Availability status keyword (e.g. 'In stock')"),
    search: Optional[str] = Query(None, description="Keyword search in title, name, or category"),
    sort_by: str = Query("price", pattern="^(price|rating|title|scraped_date)$", description="Field to sort by"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort direction ('asc' or 'desc')"),
    col: AsyncIOMotorCollection = Depends(get_products_col)
):
    query = {}

    if category:
        query["category"] = {"$regex": f"^{re.escape(category)}$", "$options": "i"}

    if min_price is not None or max_price is not None:
        price_cond = {}
        if min_price is not None:
            price_cond["$gte"] = min_price
        if max_price is not None:
            price_cond["$lte"] = max_price
        query["price"] = price_cond

    if min_rating is not None:
        query["rating"] = {"$gte": min_rating}

    if availability:
        query["availability"] = {"$regex": re.escape(availability), "$options": "i"}

    if search:
        search_rgx = {"$regex": re.escape(search), "$options": "i"}
        query["$or"] = [
            {"title": search_rgx},
            {"name": search_rgx},
            {"category": search_rgx}
        ]

    total = await col.count_documents(query)

    direction = pymongo.ASCENDING if sort_order.lower() == "asc" else pymongo.DESCENDING
    # Handle sorting field mapping (title vs name)
    sort_field = sort_by
    if sort_by == "title":
        sort_field = "title"

    skip = (page - 1) * page_size
    cursor = col.find(query).sort(sort_field, direction).skip(skip).limit(page_size)
    docs = await cursor.to_list(length=page_size)

    items = [ProductResponse(**normalize_product_doc(doc)) for doc in docs]
    pagination = compute_pagination(total=total, page=page, page_size=page_size)

    return PaginatedResponse[ProductResponse](
        items=items,
        **pagination
    )


@router.get(
    "/search",
    response_model=PaginatedResponse[ProductResponse],
    summary="Search products by keyword",
    description="Fast regex or text index query matching against product titles and categories."
)
async def search_products(
    q: str = Query(..., min_length=1, description="Search keyword"),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
    col: AsyncIOMotorCollection = Depends(get_products_col)
):
    search_rgx = {"$regex": re.escape(q), "$options": "i"}
    query = {
        "$or": [
            {"title": search_rgx},
            {"name": search_rgx},
            {"category": search_rgx}
        ]
    }

    total = await col.count_documents(query)
    skip = (page - 1) * page_size
    cursor = col.find(query).skip(skip).limit(page_size)
    docs = await cursor.to_list(length=page_size)

    items = [ProductResponse(**normalize_product_doc(doc)) for doc in docs]
    pagination = compute_pagination(total=total, page=page, page_size=page_size)

    return PaginatedResponse[ProductResponse](
        items=items,
        **pagination
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Get single product details",
    description="Retrieve full details for a product by its unique product_id or MongoDB ObjectId."
)
async def get_product(
    product_id: str,
    col: AsyncIOMotorCollection = Depends(get_products_col)
):
    # Try by product_id
    doc = await col.find_one({"product_id": product_id})
    if not doc and ObjectId.is_valid(product_id):
        doc = await col.find_one({"_id": ObjectId(product_id)})

    if not doc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' was not found in catalog"
        )

    return ProductResponse(**normalize_product_doc(doc))


@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create / ingest a new product",
    description="Add a new crawled or manual product item to the catalog. Requires X-API-Key header authorization."
)
async def create_product(
    product: ProductCreate,
    col: AsyncIOMotorCollection = Depends(get_products_col),
    _: str = Depends(verify_api_key)
):
    # Check if product_id already exists
    existing = await col.find_one({"product_id": product.product_id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Product with product_id '{product.product_id}' already exists."
        )

    product_dict = product.model_dump()
    result = await col.insert_one(product_dict)
    product_dict["_id"] = result.inserted_id

    return ProductResponse(**normalize_product_doc(product_dict))


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Replace / update entire product",
    description="Completely update an existing product record. Requires X-API-Key header."
)
async def update_product(
    product_id: str,
    product: ProductCreate,
    col: AsyncIOMotorCollection = Depends(get_products_col),
    _: str = Depends(verify_api_key)
):
    existing = await col.find_one({"product_id": product_id})
    if not existing and ObjectId.is_valid(product_id):
        existing = await col.find_one({"_id": ObjectId(product_id)})

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' was not found to update."
        )

    product_dict = product.model_dump()
    # Keep the matching product_id
    product_dict["product_id"] = existing.get("product_id", product_id)

    await col.replace_one({"_id": existing["_id"]}, product_dict)
    product_dict["_id"] = existing["_id"]

    return ProductResponse(**normalize_product_doc(product_dict))


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
    summary="Partially update product",
    description="Update specific fields of an existing product (e.g. price, rating, stock status). Requires X-API-Key header."
)
async def patch_product(
    product_id: str,
    update_data: ProductUpdate,
    col: AsyncIOMotorCollection = Depends(get_products_col),
    _: str = Depends(verify_api_key)
):
    existing = await col.find_one({"product_id": product_id})
    if not existing and ObjectId.is_valid(product_id):
        existing = await col.find_one({"_id": ObjectId(product_id)})

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' was not found to patch."
        )

    updates = {k: v for k, v in update_data.model_dump(exclude_unset=True).items() if v is not None}
    if not updates:
        return ProductResponse(**normalize_product_doc(existing))

    await col.update_one({"_id": existing["_id"]}, {"$set": updates})
    updated_doc = await col.find_one({"_id": existing["_id"]})

    return ProductResponse(**normalize_product_doc(updated_doc))


@router.delete(
    "/{product_id}",
    response_model=MessageResponse,
    summary="Delete a product",
    description="Remove a product from the database catalog. Requires X-API-Key header."
)
async def delete_product(
    product_id: str,
    col: AsyncIOMotorCollection = Depends(get_products_col),
    _: str = Depends(verify_api_key)
):
    query = {"product_id": product_id}
    existing = await col.find_one(query)
    if not existing and ObjectId.is_valid(product_id):
        query = {"_id": ObjectId(product_id)}
        existing = await col.find_one(query)

    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID '{product_id}' was not found to delete."
        )

    await col.delete_one(query)

    return MessageResponse(
        message=f"Product '{product_id}' deleted successfully.",
        success=True,
        details={"product_id": product_id}
    )
