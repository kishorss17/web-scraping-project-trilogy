"""
Health and System Status endpoints
"""
import time
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.config import get_settings, Settings
from app.dependencies import get_db
from app.models import HealthResponse

router = APIRouter(tags=["System & Health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check and database ping",
    description="Validates MongoDB connectivity, measures round-trip latency, and counts documents across crawled collections."
)
async def health_check(
    db: AsyncIOMotorDatabase = Depends(get_db),
    settings: Settings = Depends(get_settings)
):
    start_time = time.time()
    db_connected = False
    products_count = 0
    quotes_count = 0

    try:
        # Ping MongoDB
        await db.command("ping")
        db_connected = True
        products_count = await db[settings.PRODUCTS_COLLECTION].count_documents({})
        quotes_count = await db[settings.QUOTES_COLLECTION].count_documents({})
    except Exception:
        db_connected = False

    latency_ms = round((time.time() - start_time) * 1000, 2)

    return HealthResponse(
        status="healthy" if db_connected else "degraded",
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        database_connected=db_connected,
        products_count=products_count,
        quotes_count=quotes_count,
        response_time_ms=latency_ms,
        timestamp=datetime.now(timezone.utc).isoformat()
    )


@router.get(
    "/",
    summary="Root API info",
    description="Provides API documentation links, available feature routes, and metadata."
)
async def root(settings: Settings = Depends(get_settings)):
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "features": {
            "products": "/api/v1/products",
            "search": "/api/v1/products/search",
            "analytics": "/api/v1/analytics/overview",
            "quotes": "/api/v1/quotes",
            "health": "/health"
        },
        "developer": "Kish Siddammanavar",
        "target_role": "Rubick.ai SDE I Application"
    }
