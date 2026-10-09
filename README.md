# Web Scraping Trilogy: Scrapy + Selenium + FastAPI

Three production-ready projects demonstrating end-to-end web scraping, dynamic content extraction, and high-performance API serving — built for the **Rubick.ai SDE I Application**.

---

## 📦 Projects

| # | Project | Tech Stack | Description |
|---|---------|------------|-------------|
| **1** | [Scrapy E-commerce Crawler](./project-1-scrapy-ecommerce-crawler/) | Python, Scrapy, MongoDB | Async crawler with pagination, user-agent rotation, data cleaning pipelines, JSON export |
| **2** | [Selenium Dynamic Scraper](./project-2-selenium-dynamic-scraper/) | Python, Selenium,undetected-chromedriver | JavaScript-rendered content extraction with stealth browsing, anti-detection measures |
| **3** | [FastAPI Product Intelligence API](./project-3-fastapi-product-api/) | Python, FastAPI, Motor (async MongoDB), Pydantic | Async REST API with CRUD, faceted filtering, aggregation analytics, auth, Swagger docs |

---

## 🏗️ Architecture

```
┌─────────────────────┐     ┌──────────────────────────┐
│  Project 1: Scrapy  │     │  Project 2: Selenium     │
│  Static HTML Crawl  │     │  Dynamic JS Rendering    │
│  ─────────────────  │     │  ──────────────────────  │
│  • Product listings │     │  • Quotes from JS pages  │
│  • Pagination       │     │  • Stealth browser       │
│  • MongoDB upsert   │     │  • Anti-bot evasion      │
└──────────┬──────────┘     └───────────┬──────────────┘
           │                            │
           ▼                            ▼
┌─────────────────────────────────────────────────────┐
│              MongoDB: ecommerce_db                  │
│  ┌──────────────┐  ┌──────────────┐                 │
│  │  products    │  │  quotes      │                 │
│  │  (1100 docs) │  │  (100 docs)  │                 │
│  └──────────────┘  └──────────────┘                 │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│           Project 3: FastAPI + Motor                │
│  ─────────────────────────────────────────────      │
│  • /api/v1/products    – CRUD, filter, search       │
│  • /api/v1/analytics   – aggregation pipelines      │
│  • /api/v1/quotes      – Project 2 integration      │
│  • /api/v1/admin       – sync, normalize, indexes   │
│  • Swagger UI: /docs  │  ReDoc: /redoc              │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- MongoDB running locally (`mongodb://localhost:27017`)

### 1. Run Project 1 — Scrapy Crawler
```bash
cd project-1-scrapy-ecommerce-crawler
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
scrapy crawl books_spider
# Outputs: MongoDB + products.json
```

### 2. Run Project 2 — Selenium Scraper
```bash
cd project-2-selenium-dynamic-scraper
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
# Outputs: MongoDB quotes collection
```

### 3. Run Project 3 — FastAPI Server
```bash
cd project-3-fastapi-product-api
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# Server: http://127.0.0.1:8000
# Swagger: http://127.0.0.1:8000/docs
```

### 4. Test the Full Pipeline
```bash
# Health check
curl http://127.0.0.1:8000/health

# List products with filters
curl "http://127.0.0.1:8000/api/v1/products?page=1&page_size=5&category=Fiction"

# Analytics
curl http://127.0.0.1:8000/api/v1/analytics/overview

# Random quote (from Project 2)
curl http://127.0.0.1:8000/api/v1/quotes/random

# Sync Project 1 data into API
curl -X POST http://127.0.0.1:8000/api/v1/admin/sync-from-crawler \
  -H "X-API-Key: your-configured-api-key"
```

---

## 🧪 Testing

```bash
# Project 3 tests (all 15 pass)
cd project-3-fastapi-product-api
source venv/Scripts/activate
pytest tests/ -v
```

---

## 📁 Repository Structure

```
web-scraping-trilogy/
├── .gitignore
├── README.md
├── project-1-scrapy-ecommerce-crawler/
│   ├── README.md
│   ├── requirements.txt
│   ├── scrapy.cfg
│   ├── products.json          # 488 scraped products
│   └── ecommerce_scraper/
│       ├── settings.py
│       ├── items.py
│       ├── middlewares.py
│       ├── pipelines.py
│       └── spiders/books_spider.py
├── project-2-selenium-dynamic-scraper/
│   ├── README.md
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   ├── scraper/
│   └── data/
└── project-3-fastapi-product-api/
    ├── README.md
    ├── requirements.txt
    ├── .env.example
    ├── app/
    │   ├── main.py
    │   ├── config.py
    │   ├── database.py
    │   ├── dependencies.py
    │   ├── models.py
    │   ├── routers/
    │   │   ├── admin.py
    │   │   ├── analytics.py
    │   │   ├── health.py
    │   │   ├── products.py
    │   │   └── quotes.py
    │   └── utils/
    │       ├── helpers.py
    │       └── data_loader.py
    └── tests/
        ├── conftest.py
        ├── test_analytics.py
        ├── test_health.py
        ├── test_products.py
        └── test_quotes.py
```

---

## 🎤 Interview Talking Points

### Project 1 — Scrapy
- "Built a production Scrapy crawler with middleware for user-agent rotation"
- "Item pipelines separate data cleaning from MongoDB storage"
- "Upsert on `product_id` prevents duplicates across re-runs"

### Project 2 — Selenium
- "Used `undetected-chromedriver` for stealth scraping of JS-heavy sites"
- "Implemented retry logic with exponential backoff for flaky pages"
- "Headless mode with realistic viewport and navigator spoofing"

### Project 3 — FastAPI
- "Async FastAPI + Motor serves unified data from both crawlers"
- "MongoDB aggregation pipelines compute analytics server-side"
- "Pydantic v2 schemas validate every request/response"
- "API key auth protects mutation endpoints; read endpoints are public"
- "Background index creation with `background=True` avoids collection locks"

---

## 🔧 Configuration

Each project has its own `.env.example` — copy to `.env` and adjust:
- MongoDB URI
- API keys
- Server host/port
- Browser settings (Project 2)

---

## 📜 License

MIT License — feel free to use for learning or as a portfolio foundation.

---

## 👤 Author

**Kishore Siddamannavar**  
— October 2026

---

## 🌟 Star this repo if you found it useful!
