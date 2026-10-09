"""
Quotes Router
Connects Project 2 (Selenium dynamic scraper) to the FastAPI ecosystem.
"""
from typing import Optional, List, Dict
import re
from fastapi import APIRouter, Depends, Query, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorCollection

from app.dependencies import get_quotes_col
from app.models import QuoteResponse, PaginatedResponse
from app.utils.helpers import compute_pagination

router = APIRouter(prefix="/api/v1/quotes", tags=["Dynamic Quotes (Project 2 Integration)"])


def normalize_quote_doc(doc: dict) -> dict:
    if not doc:
        return {}
    return {
        "id": str(doc.get("_id", "")),
        "text": doc.get("text", "").strip(),
        "author": doc.get("author", "Unknown"),
        "author_url": doc.get("author_url"),
        "tags": doc.get("tags", []),
        "source": doc.get("source", "quotes.toscrape.com/js"),
        "scraped_date": str(doc.get("scraped_date", ""))
    }


@router.get(
    "",
    response_model=PaginatedResponse[QuoteResponse],
    summary="List scraped quotes with filters & pagination",
    description="Retrieve quotes extracted via Selenium JavaScript scraper with filtering by author and tag."
)
async def list_quotes(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    author: Optional[str] = Query(None, description="Filter quotes by author name"),
    tag: Optional[str] = Query(None, description="Filter quotes by tag"),
    col: AsyncIOMotorCollection = Depends(get_quotes_col)
):
    query = {}
    if author:
        query["author"] = {"$regex": re.escape(author), "$options": "i"}
    if tag:
        query["tags"] = {"$in": [tag.lower()]}

    total = await col.count_documents(query)
    skip = (page - 1) * page_size
    cursor = col.find(query).skip(skip).limit(page_size)
    docs = await cursor.to_list(length=page_size)

    items = [QuoteResponse(**normalize_quote_doc(d)) for d in docs]
    pagination = compute_pagination(total=total, page=page, page_size=page_size)

    return PaginatedResponse[QuoteResponse](
        items=items,
        **pagination
    )


@router.get(
    "/random",
    response_model=QuoteResponse,
    summary="Get a random quote",
    description="Samples a random quote from the collection using MongoDB $sample pipeline stage."
)
async def get_random_quote(
    col: AsyncIOMotorCollection = Depends(get_quotes_col)
):
    pipeline = [{"$sample": {"size": 1}}]
    docs = await col.aggregate(pipeline).to_list(length=1)
    if not docs:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No quotes found in collection."
        )
    return QuoteResponse(**normalize_quote_doc(docs[0]))


@router.get(
    "/tags",
    response_model=List[Dict[str, int]],
    summary="Get popular quote tags with frequencies",
    description="Unwinds tags array and groups by tag name to return top tag usage."
)
async def get_quote_tags(
    limit: int = Query(20, ge=1, le=100),
    col: AsyncIOMotorCollection = Depends(get_quotes_col)
):
    pipeline = [
        {"$unwind": "$tags"},
        {"$group": {"_id": "$tags", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": limit}
    ]
    results = await col.aggregate(pipeline).to_list(length=limit)
    return [{str(item["_id"]): item["count"]} for item in results]
