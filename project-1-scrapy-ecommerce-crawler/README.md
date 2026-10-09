# Project 1: E-commerce Product Crawler with Scrapy

## 🎯 Project Overview

A production-ready web scraper built with Scrapy framework to extract product data from e-commerce websites. Features include MongoDB integration, user-agent rotation, data cleaning pipelines, and scalable architecture suitable for crawling thousands of products.

**Built for:** Rubick.ai SDE I Position  
**Tech Stack:** Python, Scrapy, MongoDB, PyMongo

---

## 📋 Features

- ✅ **Scrapy Spider** - Crawls product listings with pagination support
- ✅ **MongoDB Pipeline** - Automatic storage with duplicate prevention (upsert)
- ✅ **User-Agent Rotation** - Middleware to avoid bot detection
- ✅ **Data Cleaning** - Validates and cleans product data
- ✅ **JSON Export** - Backup export to local JSON file
- ✅ **Scalable Architecture** - Handles concurrent requests efficiently
- ✅ **Rate Limiting** - Configurable delays to respect server resources

---

## 🏗️ Project Structure

```
project-1-scrapy-ecommerce-crawler/
├── scrapy.cfg                          # Scrapy configuration file
├── requirements.txt                    # Python dependencies
├── products.json                       # Scraped data (generated)
├── ecommerce_scraper/
│   ├── __init__.py
│   ├── settings.py                     # Scrapy settings & configuration
│   ├── items.py                        # Data models (ProductItem)
│   ├── middlewares.py                  # User-Agent rotation middleware
│   ├── pipelines.py                    # Data cleaning & MongoDB pipeline
│   └── spiders/
│       ├── __init__.py
│       └── books_spider.py             # Main spider
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.8+
- MongoDB installed and running locally
- pip package manager

### 2. Install MongoDB (if not installed)

**Windows:**
```powershell
# Download from: https://www.mongodb.com/try/download/community
# Or use Chocolatey:
choco install mongodb
```

**Start MongoDB:**
```powershell
mongod
```

### 3. Create Virtual Environment
```bash
cd C:\Users\RT\PROJECTS\Rubick_AI_Web_Scraping_Projects\project-1-scrapy-ecommerce-crawler
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🎮 Usage

### Run the Spider

```bash
# Basic run (saves to MongoDB + products.json)
scrapy crawl books_spider

# Run with custom output file
scrapy crawl books_spider -o output.json

# Run with logging
scrapy crawl books_spider -L INFO
```

### Check Scraped Data

**MongoDB (using MongoDB Compass or CLI):**
```bash
mongosh
use ecommerce_db
db.products.find().pretty()
db.products.countDocuments()
```

**JSON File:**
```bash
# View products.json in your project folder
cat products.json
```

---

## 📊 Data Schema

Each product contains:

| Field | Type | Description |
|-------|------|-------------|
| `product_id` | String | Unique product identifier |
| `title` | String | Product name |
| `url` | String | Product page URL |
| `price` | Float | Current price |
| `original_price` | Float | Original price (before discount) |
| `discount` | Float | Discount percentage |
| `currency` | String | Currency code (GBP, USD, etc.) |
| `rating` | Float | Star rating (0-5) |
| `reviews_count` | Integer | Number of reviews |
| `availability` | String | Stock status |
| `category` | String | Product category |
| `image_url` | String | Product image URL |
| `scraped_date` | String | ISO timestamp of scrape |
| `source_website` | String | Source domain |

---

## ⚙️ Configuration

### Key Settings (in `settings.py`)

```python
# Concurrency
CONCURRENT_REQUESTS = 16  # Adjust based on target site

# Rate Limiting
DOWNLOAD_DELAY = 1  # Seconds between requests

# MongoDB
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'ecommerce_db'

# User Agent Pool
USER_AGENT_LIST = [...]  # Rotates automatically
```

---

## 🔧 Customization

### Scrape Different Website

1. Create new spider in `ecommerce_scraper/spiders/`:
```python
# myntra_spider.py
class MyntraSpider(scrapy.Spider):
    name = 'myntra_spider'
    allowed_domains = ['myntra.com']
    start_urls = ['https://www.myntra.com/']
    # ... implement parse methods
```

2. Run it:
```bash
scrapy crawl myntra_spider
```

### Modify Data Fields

Edit `items.py` to add/remove fields:
```python
class ProductItem(scrapy.Item):
    # Add new field
    brand = scrapy.Field()
    size = scrapy.Field()
```

---

## 🧪 Testing

### Test Spider Without Saving
```bash
scrapy crawl books_spider -s ITEM_PIPELINES={}
```

### Verify MongoDB Connection
```python
python -c "import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017'); print('Connected!'); client.close()"
```

### Check Spider Output
```bash
scrapy parse --spider=books_spider http://books.toscrape.com/
```

---

## 📈 Performance

- **Speed:** ~100 products in 2-3 minutes
- **Concurrency:** 16 simultaneous requests
- **Rate Limiting:** 1 second delay between requests
- **Scalability:** Can handle 10,000+ products with proper configuration

---

## 🎤 Interview Talking Points

### Architecture
- "Built a production-ready Scrapy crawler with modular pipeline architecture"
- "Implemented middleware for user-agent rotation to avoid bot detection"
- "Used MongoDB with upsert operations to prevent duplicate data"

### Technical Decisions
- "Chose Scrapy over BeautifulSoup for better concurrency and built-in features"
- "Implemented item pipelines for separation of concerns (cleaning vs storage)"
- "Used XPath/CSS selectors for robust data extraction"

### Scale & Performance
- "Configured concurrent requests and rate limiting for optimal performance"
- "Spider can handle pagination automatically across multiple pages"
- "MongoDB indexing on product_id for fast duplicate detection"

### Production Readiness
- "Proper error handling in pipelines"
- "Logging at different levels for debugging"
- "Data validation and cleaning before storage"
- "Exportable to multiple formats (JSON, CSV, XML)"

---

## 🐛 Troubleshooting

**MongoDB Connection Error:**
```bash
# Ensure MongoDB is running
mongod

# Check connection
mongosh
```

**Scrapy Not Found:**
```bash
# Ensure virtual environment is activated
venv\Scripts\activate
pip install scrapy
```

**No Data Scraped:**
```bash
# Check if site is accessible
curl http://books.toscrape.com

# Run with verbose logging
scrapy crawl books_spider -L DEBUG
```

---

## 📚 Key Libraries

- **Scrapy 2.11.0** - Web crawling framework
- **PyMongo 4.6.0** - MongoDB driver
- **itemadapter 0.8.0** - Item handling utility

---

## 🎯 Next Steps

1. ✅ Complete Project 2: Selenium Dynamic Scraper
2. ✅ Complete Project 3: FastAPI Product API
3. ✅ Push all projects to GitHub
4. ✅ Update resume with project links

---

## 📞 Contact

**Built by:** Kish Siddammanavar  
**For:** Rubick.ai SDE I Application  
**Date:** October 2026

---

## 🔗 Related Projects

- [Project 2: Selenium Dynamic Scraper](../project-2-selenium-dynamic-scraper/)
- [Project 3: FastAPI Product API](../project-3-fastapi-product-api/)
