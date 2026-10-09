"""
FastAPI dependencies for database access and authentication
"""
from typing import Optional
from fastapi import Header, HTTPException, status, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection
from app.config import get_settings, Settings
from app.database import get_database, get_products_collection, get_quotes_collection


async def get_db() -> AsyncIOMotorDatabase:
    """Dependency for obtaining the MongoDB database instance."""
    db = get_database()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection is not initialized"
        )
    return db


async def get_products_col() -> AsyncIOMotorCollection:
    """Dependency for accessing the products collection."""
    col = get_products_collection()
    if col is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Products collection is not available"
        )
    return col


async def get_quotes_col() -> AsyncIOMotorCollection:
    """Dependency for accessing the quotes collection."""
    col = get_quotes_collection()
    if col is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Quotes collection is not available"
        )
    return col


async def verify_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-API-Key", description="API Key for protected write operations"),
    settings: Settings = Depends(get_settings)
) -> str:
    """
    Security dependency to verify X-API-Key header.
    Protects write operations (POST, PUT, DELETE, admin sync).
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing 'X-API-Key' header. Write operations require authorization."
        )
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key provided."
        )
    return x_api_key
