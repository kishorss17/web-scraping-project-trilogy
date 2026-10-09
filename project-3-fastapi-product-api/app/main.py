"""
FastAPI Application Entry Point
Rubick Product Intelligence API
"""
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import get_settings
from app.database import connect_to_mongo, close_mongo_connection
from app.routers import health, products, analytics, quotes, admin

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager to initialize and cleanup MongoDB connections."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()


tags_metadata = [
    {
        "name": "System & Health",
        "description": "Liveness probes, MongoDB connection verification, and API metadata."
    },
    {
        "name": "Products Catalog",
        "description": "Comprehensive CRUD, paginated browsing, faceted filtering, and full-text search for scraped e-commerce products."
    },
    {
        "name": "Catalog Analytics",
        "description": "High-performance MongoDB aggregation pipelines delivering catalog metrics, price distributions, and category breakdowns."
    },
    {
        "name": "Dynamic Quotes (Project 2 Integration)",
        "description": "Endpoints serving JavaScript-rendered quotes collected via the Selenium stealth scraper."
    },
    {
        "name": "Admin & Data Management",
        "description": "Batch ingestion, crawler JSON synchronization, and index maintenance."
    }
]

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
# 🛍️ Rubick Product Intelligence API

High-performance, asynchronous REST API serving structured e-commerce catalog data extracted by Scrapy and Selenium web crawlers.

---

### 🚀 Capabilities:
* **Asynchronous High Throughput**: Powered by FastAPI & Motor async MongoDB driver.
* **Faceted Product Filtering**: Filter by category, price ranges, star rating, availability, and sort dynamically.
* **Full-Text & Regex Search**: Fast keyword matching across product titles and categories.
* **MongoDB Aggregation Pipelines**: Real-time business analytics including price distribution buckets and category metrics.
* **Trilogy Integration**: Serves both Scrapy e-commerce data (Project 1) and Selenium dynamic quotes (Project 2).
* **Enterprise Security**: Header-based API key authentication for mutation endpoints.

---
**Candidate:** Kish Siddammanavar  
**Target Position:** Rubick.ai SDE I Application
    """,
    openapi_tags=tags_metadata,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# -------------------------------------------------------------
# Middleware
# -------------------------------------------------------------

# 1. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2. Process Timing Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    response.headers["X-Process-Time-Ms"] = f"{process_time:.2f}"
    return response


# -------------------------------------------------------------
# Exception Handlers
# -------------------------------------------------------------

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join([str(loc) for loc in err.get("loc", [])])
        errors.append({
            "field": field,
            "message": err.get("msg"),
            "type": err.get("type")
        })
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": "Validation Error",
            "details": errors
        }
    )


# -------------------------------------------------------------
# Register Routers
# -------------------------------------------------------------

app.include_router(health.router)
app.include_router(products.router)
app.include_router(analytics.router)
app.include_router(quotes.router)
app.include_router(admin.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
