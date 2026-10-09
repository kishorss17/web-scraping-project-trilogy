"""
Admin and Catalog Management Router
Endpoints for data synchronization, crawler ingestion, and index maintenance.
"""
from typing import Optional
from fastapi import APIRouter, Depends, status
from app.dependencies import verify_api_key
from app.models import MessageResponse
from app.database import create_indexes
from app.utils.data_loader import sync_products_from_file, normalize_existing_collection

router = APIRouter(prefix="/api/v1/admin", tags=["Admin & Data Management"])


@router.post(
    "/sync-from-crawler",
    response_model=MessageResponse,
    summary="Sync products from Scrapy crawler JSON export",
    description="Loads products from Project 1's products.json, normalizes all attributes, and performs bulk upserts into MongoDB. Requires X-API-Key."
)
async def sync_from_crawler(
    file_path: Optional[str] = None,
    _: str = Depends(verify_api_key)
):
    result = sync_products_from_file(file_path=file_path)
    if not result.get("success"):
        return MessageResponse(
            message=f"Sync failed: {result.get('error')}",
            success=False,
            details=result
        )

    # Automatically ensure indexes after sync
    await create_indexes()

    return MessageResponse(
        message=f"Successfully synced {result.get('total_items_in_file')} products from crawler file.",
        success=True,
        details=result
    )


@router.post(
    "/normalize-catalog",
    response_model=MessageResponse,
    summary="Normalize existing catalog documents in MongoDB",
    description="Transforms legacy uncleaned fields (string prices, fractional ratings) in MongoDB to typed values. Requires X-API-Key."
)
async def normalize_catalog(
    _: str = Depends(verify_api_key)
):
    result = normalize_existing_collection()
    if not result.get("success"):
        return MessageResponse(
            message=f"Normalization failed: {result.get('error')}",
            success=False,
            details=result
        )

    return MessageResponse(
        message=f"Successfully normalized {result.get('records_normalized')} catalog records in MongoDB.",
        success=True,
        details=result
    )


@router.post(
    "/create-indexes",
    response_model=MessageResponse,
    summary="Rebuild MongoDB database indexes",
    description="Rebuilds compound, unique, and full-text indexes for optimal query execution. Requires X-API-Key."
)
async def rebuild_indexes(
    _: str = Depends(verify_api_key)
):
    await create_indexes()
    return MessageResponse(
        message="MongoDB indexes successfully verified and built.",
        success=True
    )
