# Project 3: FastAPI Product Intelligence API

## 🎯 Project Overview

A high-performance, asynchronous REST API built with FastAPI and Motor (async MongoDB driver) that serves structured e-commerce catalog data extracted by the Scrapy crawler (Project 1) and Selenium dynamic scraper (Project 2). This is the serving layer of the Rubick scraping trilogy — exposing CRUD, filtering, search, analytics, and admin endpoints.

**Built for:** Rubick.ai SDE I Position  
**Tech Stack:** Python, FastAPI, Uvicorn, Motor (async MongoDB), Pydantic, Pytest

---

## 📋 Features

- ✅ **Async FastAPI + Motor** - Non-blocking API with MongoDB aggregation pipelines
- ✅ **Full Product CRUD** - Create, Read, Update, Delete with product_id + MongoDB ObjectId support
- ✅ **Faceted Filtering** - Filter by category, price range, minimum rating, and availability
- ✅ **Full-Text & Regex Search** - Fast keyword search across titles and categories
- ✅ **Paginated Listings** - Cursor-based pagination with metadata (page, total, has_next/prev)
- ✅ **Catalog Analytics** - Aggregation pipelines for overview, per-category stats, and price distribution
- ✅ **Dynamic Quotes (Project 2)** - Serve JavaScript-rendered quotes with random/sample and tag endpoints
- ✅ **Admin & Data Management** - Sync from crawler JSON, normalize dirty data, rebuild indexes
- ✅ **Enterprise Security** - X-API-Key header authentication for write operations
- ✅ **Health & Readiness Probes** - MongoDB connectivity checks and round-trip latency measurement

---

## 🏗️ Project Structure

```
project-3-fastapi-product-api/
├── .env                         # Environment configuration
├── .env.example                 # Template for environment variables
├── requirements.txt             # Python dependencies
├── app/
│   ├── __init__.py
│   ├── config.py                # Pydantic settings loader
│   ├── database.py              # Async MongoDB (Motor) connection & index management
│   ├── dependencies.py          # FastAPI dependency injection (DB, API key auth)
│   ├── main.py                  # FastAPI app entry point
│   ├── models.py                # Pydantic request/response schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── admin.py             # Sync/normalize/index admin endpoints
│   │   ├── analytics.py         # Catalog aggregation endpoints
│   │   ├── health.py            # Health check & root info
│   │   ├── products.py          # Product CRUD & search
│   │   └── quotes.py            # Project 2 quote endpoints
│   └── utils/
│       ├── __init__.py
│       ├── data_loader.py       # Bulk upsert & normalization utilities
│       └── helpers.py           # Price/rating normalization & pagination
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures + test DB setup
│   ├── test_analytics.py
│   ├── test_health.py
│   ├── test_products.py
│   └── test_quotes.py
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.13+
- MongoDB installed and running locally (`mongodb://localhost:27017`)

### 2. Create Virtual Environment

```bash
cd C:\Users\RT\PROJECTS\Rubick_AI_Web_Scraping_Projects\project-3-fastapi-product-api
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Mac/Linux
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🎮 Usage

### Start the Server

```bash
# Development with auto-reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Example Requests

```bash
# Health check
curl http://localhost:8000/health

# List products (paginated, filtered)
curl "http://localhost:8000/api/v1/products?page=1&page_size=20&category=Fiction&min_price=10&max_price=30&sort_by=rating&sort_order=desc"

# Full-text search
curl "http://localhost:8000/api/v1/products/search?q=science"

# Catalog analytics
curl http://localhost:8000/api/v1/analytics/overview
curl http://localhost:8000/api/v1/analytics/categories
curl http://localhost:8000/api/v1/analytics/price-distribution

# Project 2 quotes
curl http://localhost:8000/api/v1/quotes/random
curl "http://localhost:8000/api/v1/quotes?page_size=10&tag=humor"

# Create a product (authenticated)
curl -X POST "http://localhost:8000/api/v1/products" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-configured-api-key" \
  -d '{"product_id":"new-book-123","title":"New Book","url":"http://example.com","price":15.99,"rating":4.5}'

# Sync crawler data from Project 1
curl -X POST "http://localhost:8000/api/v1/admin/sync-from-crawler" \
  -H "X-API-Key: your-configured-api-key"

# Normalize dirty records already in MongoDB
curl -X POST "http://localhost:8000/api/v1/admin/normalize-catalog" \
  -H "X-API-Key: your-configured-api-key"
```

---

## 🧪 Testing

Run the test suite (uses an isolated in-memory MongoDB via motor):

```bash
pytest tests/ -v
```

All 15 tests pass, covering:
- Products CRUD lifecycle, pagination, category/price filtering, search
- Analytics overview, categories, price distribution, top-rated
- Health & root endpoints
- Quotes listing, random sampling, tag aggregation

---

## 📊 Data Schema

### Product Document
| Field | Type | Description |
|-------|------|-------------|
| `product_id` | String | Unique product identifier (unique index) |
| `title` / `name` | String | Product name |
| `url` | String | Source page URL |
| `price` | Float | Current price (ge 0) |
| `original_price` | Float | Original list price |
| `discount` | Float | Discount percentage |
| `currency` | String | Currency code |
| `rating` | Float | Star rating (0-5) |
| `reviews_count` | Integer | Number of reviews |
| `availability` | String | Stock status |
| `category` | String | Product category (TEXT index) |
| `image_url` | String | Direct image URL |
| `scraped_date` | String | ISO timestamp |
| `source_website` | String | Source domain |

### Quote Document
| Field | Type | Description |
|-------|------|-------------|
| `text` | String | Quote text |
| `author` | String | Author name (indexed) |
| `author_url` | String | Author page URL |
| `tags` | Array | List of tag strings (indexed) |
| `source` | String | Source site |
| `scraped_date` | String | ISO timestamp |

---

## 📈 API Endpoints

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/health` | GET | Health check + DB ping | No |
| `/` | GET | Root API info | No |
| `/api/v1/products` | GET | List products (paginated + filtered) | No |
| `/api/v1/products` | POST | Create product | X-API-Key |
| `/api/v1/products/search` | GET | Full-text/regex search | No |
| `/api/v1/products/{id}` | GET | Get product | No |
| `/api/v1/products/{id}` | PUT/PATCH | Update product | X-API-Key |
| `/api/v1/products/{id}` | DELETE | Delete product | X-API-Key |
| `/api/v1/analytics/overview` | GET | Catalog-wide stats | No |
| `/api/v1/analytics/categories` | GET | Per-category stats | No |
| `/api/v1/analytics/price-distribution` | GET | Price buckets | No |
| `/api/v1/analytics/top-rated` | GET | Top N rated products | No |
| `/api/v1/quotes` | GET | List quotes (filtered) | No |
| `/api/v1/quotes/random` | GET | Random quote | No |
| `/api/v1/quotes/tags` | GET | Tag frequencies | No |
| `/api/v1/admin/sync-from-crawler` | POST | Ingest products.json | X-API-Key |
| `/api/v1/admin/normalize-catalog` | POST | Clean dirty records | X-API-Key |
| `/api/v1/admin/create-indexes` | POST | Rebuild indexes | X-API-Key |

---

## 🐛 Troubleshooting

**MongoDB Connection Error:**
```bash
# Ensure MongoDB is running
mongod
```

**Uvicorn Not Found:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate
pip install uvicorn
```

**503 Service Unavailable:**
- The app starts async but the dependency checks happen at runtime; restart uvicorn.

**Duplicate product_id Conflict:**
- Create errors with HTTP 409 Conflict if the product_id already exists.

---

## 📚 Key Libraries

- **FastAPI 0.110.0+** - Modern async web framework
- **Uvicorn 0.28.0+** - ASGI server
- **Motor 3.3.0+** - Async MongoDB driver
- **Pydantic 2.6.0+** - Data validation & settings
- **Pytest 8.0.0+ / httpx 0.27.0+** - Testing

---

## 🎤 Interview Talking Points

### Architecture
- "Built an async FastAPI serving layer that unifies data from two crawlers (Scrapy + Selenium)"
- "Used Motor for non-blocking MongoDB access with aggregation pipelines for real-time analytics"
- "Implemented dependency injection for DB access and API-key authentication"

### Technical Decisions
- "Chose async/await over synchronous frameworks for throughput"
- "Pydantic models enforce schema validation on every request/response"
- "MongoDB indexes (unique, compound, TEXT) optimized for the query patterns"

### Scale & Performance
- "Aggregation pipelines compute analytics server-side instead of fetching raw documents"
- "Server-side pagination with skip/limit to handle large catalogs"
- "Background index creation with `background=True` to avoid locking"

### Production Readiness
- "Lifespan event manager for connection pool lifecycle"
- "Global exception handlers (validation errors) for consistent error shapes"
- "Process-time middleware headers for observability"
- "Structured health probes for load balancers"

---

## 🎯 Next Steps

1. ✅ Complete Project 1: Scrapy E-commerce Crawler
2. ✅ Complete Project 2: Selenium Dynamic Scraper
3. ✅ Complete Project 3: FastAPI Product API
4. Push all projects to GitHub
5. Update resume with project links

---

## 📞 Contact

**Built by:** Kish Siddammanavar  
**For:** Rubick.ai SDE I Application  
**Date:** October 2026

---

## 🔗 Related Projects

- [Project 1: E-commerce Product Crawler (Scrapy)](../project-1-scrapy-ecommerce-crawler/)
- [Project 2: Selenium Dynamic Scraper](../project-2-selenium-dynamic-scraper/)
