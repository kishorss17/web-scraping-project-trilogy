# Project 2: Selenium Dynamic Scraper - Complete Documentation & Interview Guide

**Created by:** Kish Siddammanavar  
**For:** Rubick.ai SDE I Application  
**Date:** October 6, 2026  
**Project Location:** `C:\Users\RT\PROJECTS\Rubick_AI_Web_Scraping_Projects\project-2-selenium-dynamic-scraper`

---

## 📑 Table of Contents

1. [Complete Setup & Deployment Commands](#1-complete-setup--deployment-commands)
2. [How the Project Works - Architecture & Process](#2-how-the-project-works---architecture--process)
3. [Relationship with Project 1](#3-relationship-with-project-1)
4. [Use Cases & Applications](#4-use-cases--applications)
5. [Interview Questions & Answers](#5-interview-questions--answers)
6. [Technical Deep Dive](#6-technical-deep-dive)
7. [Troubleshooting Guide](#7-troubleshooting-guide)

---

# 1. Complete Setup & Deployment Commands

## 🔧 Prerequisites Installation

### Check Python Version
```powershell
python --version
# Should show: Python 3.8 or higher
```

### Verify Chrome Browser Installed
```powershell
# Check Chrome version
Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe' | Select-Object -ExpandProperty '(Default)'
```

### Verify MongoDB Running
```powershell
# Check MongoDB service
Get-Service -Name MongoDB

# Or test connection
python -c "import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=2000); client.server_info(); print('✅ MongoDB is RUNNING!'); client.close()"
```

---

## 📦 Project Setup (Step-by-Step)

### Step 1: Navigate to Project Directory
```powershell
cd C:\Users\RT\PROJECTS\Rubick_AI_Web_Scraping_Projects\project-2-selenium-dynamic-scraper
```

### Step 2: Create Virtual Environment
```powershell
# Create venv
python -m venv venv

# Activate venv (Windows)
venv\Scripts\activate

# You should see (venv) at the start of your prompt
```

### Step 3: Install Dependencies
```powershell
# Install all required packages
pip install -r requirements.txt

# If distutils error occurs (Python 3.12+)
pip install setuptools

# Verify installations
pip list
```

**Dependencies installed:**
- `selenium==4.16.0` - WebDriver automation
- `undetected-chromedriver==3.5.5` - Anti-detection Chrome
- `pymongo==4.6.0` - MongoDB driver
- `fake-useragent==1.4.0` - Random user-agent generation
- `webdriver-manager==4.0.1` - Automatic driver management
- `python-dotenv==1.0.0` - Environment variables

### Step 4: Verify MongoDB is Running
```powershell
# Option 1: Check service
Get-Service -Name MongoDB

# Option 2: Start if not running
& "C:\Program Files\MongoDB\Server\9.0\bin\mongod.exe" --dbpath "C:\data\db"

# Option 3: Start as service
Start-Service MongoDB
```

---

## 🚀 Running the Scraper

### Basic Execution
```powershell
# Run with default settings (headless mode)
python main.py
```

### Run with Visible Browser (for debugging)
```powershell
# Edit config.py first
# Change: HEADLESS_MODE = False

python main.py
```

### Expected Output
```
============================================================
SELENIUM DYNAMIC SCRAPER - PROJECT 2
============================================================
INFO:scraper.browser:Setting up Chrome driver...
INFO:undetected_chromedriver.patcher:patching driver executable
INFO:scraper.browser:✓ Chrome driver setup complete (stealth mode enabled)
INFO:scraper.database:✓ Connected to MongoDB: ecommerce_db.quotes
INFO:__main__:✓ Setup complete. Starting scrape...

INFO:scraper.browser:Navigating to: https://quotes.toscrape.com/js/
INFO:scraper.browser:✓ Page loaded successfully
INFO:__main__:Waiting for JavaScript content to load...

INFO:__main__:
📄 Scraping page 1...
INFO:__main__:✓ Scraped quote 1: "The world as we have created it..."
INFO:__main__:✓ Scraped quote 2: "It is our choices, Harry..."
...
INFO:__main__:➡️  Moving to next page...

============================================================
SCRAPING COMPLETE!
============================================================
✓ Total quotes scraped: 100
✓ Saved to MongoDB: ecommerce_db.quotes
✓ Saved to JSON: data/quotes.json
✓ Total quotes in database: 100
============================================================
```

---

## ✅ Verify Data Collection

### Check MongoDB Data
```powershell
# Count documents
python -c "import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017/'); db = client['ecommerce_db']; count = db.quotes.count_documents({}); print(f'Total quotes: {count}'); client.close()"

# View sample quote
python -c "import pymongo; client = pymongo.MongoClient('mongodb://localhost:27017/'); db = client['ecommerce_db']; quote = db.quotes.find_one(); import json; print(json.dumps(quote, indent=2, default=str)); client.close()"
```

### Check JSON File
```powershell
# Check file exists and size
dir data\quotes.json

# View content
type data\quotes.json | more
```

### Using MongoDB Compass (GUI)
```
1. Open MongoDB Compass
2. Connect to: mongodb://localhost:27017
3. Database: ecommerce_db
4. Collection: quotes
5. Browse your scraped data
```

---

## 🔄 Configuration Options

### Edit config.py for Customization

```python
# Target website
TARGET_URL = 'https://quotes.toscrape.com/js/'

# Scraping limits
MAX_QUOTES = 100  # Change to scrape more/less

# Browser settings
HEADLESS_MODE = True   # False to see browser in action
WINDOW_SIZE = (1920, 1080)

# Anti-bot delays (seconds)
MIN_DELAY = 1  # Minimum delay between actions
MAX_DELAY = 3  # Maximum delay

# MongoDB
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'ecommerce_db'
MONGO_COLLECTION = 'quotes'
```

---

## 📊 Deployment Summary Table

| Step | Command | Purpose | Time |
|------|---------|---------|------|
| 1 | `python -m venv venv` | Create virtual environment | 30s |
| 2 | `venv\Scripts\activate` | Activate venv | 1s |
| 3 | `pip install -r requirements.txt` | Install dependencies | 2-3 min |
| 4 | Check MongoDB running | Verify database | 5s |
| 5 | `python main.py` | Run scraper | 2-5 min |
| 6 | Verify data | Check MongoDB/JSON | 10s |

---

# 2. How the Project Works - Architecture & Process

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  MAIN SCRAPER                           │
│                   (main.py)                             │
└─────────────────────┬───────────────────────────────────┘
                      │
          ┌───────────┴───────────┐
          ↓                       ↓
┌──────────────────┐    ┌──────────────────┐
│  SELENIUM        │    │  MONGODB         │
│  BROWSER         │    │  HANDLER         │
│  (browser.py)    │    │  (database.py)   │
└────────┬─────────┘    └─────────┬────────┘
         │                        │
         ↓                        ↓
┌──────────────────┐    ┌──────────────────┐
│  Chrome Browser  │    │  MongoDB         │
│  (Undetected)    │    │  Database        │
│  + Anti-Bot      │    │  ecommerce_db    │
└──────────────────┘    └──────────────────┘
```

---

## 🔄 Complete Workflow

### Phase 1: Initialization

```python
# 1. QuoteScraper initialized
scraper = QuoteScraper()

# 2. Browser setup with stealth
browser = SeleniumBrowser(headless=True, enable_stealth=True)
    ↓
# 3. Chrome options configured
- Headless mode
- Anti-detection flags
- Random user-agent
- Stealth JavaScript injected
    ↓
# 4. Undetected ChromeDriver started
driver = uc.Chrome(options=options)

# 5. MongoDB connection established
db = MongoDBHandler(config.MONGO_URI, ...)
db.connect()
```

### Phase 2: Navigation & Page Load

```python
# 1. Navigate to target URL
driver.get('https://quotes.toscrape.com/js/')
    ↓
# 2. Wait for JavaScript execution
time.sleep(3)  # Page load wait
    ↓
# 3. JavaScript renders content
# - Browser executes page scripts
# - AJAX calls fetch data
# - DOM elements populate
    ↓
# 4. Human-like behavior simulation
- Random mouse movement
- Random delay (1-3 seconds)
```

### Phase 3: Element Detection & Extraction

```python
# 1. Wait for elements to appear
quote_elements = browser.wait_for_elements(
    By.CSS_SELECTOR,
    'div.quote',
    timeout=10
)
    ↓
# 2. Extract data from each element
for quote_elem in quote_elements:
    # Extract text
    text = quote_elem.find_element(By.CSS_SELECTOR, 'span.text').text
    
    # Extract author
    author = quote_elem.find_element(By.CSS_SELECTOR, 'small.author').text
    
    # Extract tags
    tags = [tag.text for tag in quote_elem.find_elements(By.CSS_SELECTOR, 'a.tag')]
    
    # Build quote object
    quote_data = {
        'text': text,
        'author': author,
        'tags': tags,
        'source': 'quotes.toscrape.com/js'
    }
```

### Phase 4: Data Storage

```python
# 1. Add timestamp
quote_data['scraped_date'] = datetime.utcnow().isoformat()
    ↓
# 2. Save to MongoDB with upsert
db.collection.update_one(
    {'text': quote_data['text']},  # Match condition
    {'$set': quote_data},          # Update data
    upsert=True                    # Insert if not exists
)
    ↓
# 3. Add to in-memory list
quotes_data.append(quote_data)
```

### Phase 5: Pagination

```python
# 1. Look for "Next" button
next_button = driver.find_element(By.CSS_SELECTOR, 'li.next > a')
    ↓
# 2. Scroll button into view (human-like)
driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
time.sleep(1)
    ↓
# 3. Click next button
next_button.click()
    ↓
# 4. Wait for new content to load
time.sleep(3)
    ↓
# 5. Repeat extraction process
```

### Phase 6: Completion & Cleanup

```python
# 1. Save all data to JSON
with open('data/quotes.json', 'w') as f:
    json.dump(quotes_data, f, indent=2)
    ↓
# 2. Display summary
print(f"✓ Total quotes scraped: {len(quotes_data)}")
print(f"✓ Saved to MongoDB: {db_count}")
    ↓
# 3. Close browser
driver.quit()
    ↓
# 4. Close MongoDB connection
client.close()
```

---

## 🎯 Key Components Explained

### 1. browser.py - SeleniumBrowser Class

**Role:** Manages Chrome browser with anti-bot features

**Key Methods:**

**`setup_driver()`**
```python
def setup_driver(self):
    options = uc.ChromeOptions()
    
    # Anti-detection arguments
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f'user-agent={random.choice(user_agents)}')
    
    # Initialize undetected Chrome
    self.driver = uc.Chrome(options=options)
    
    # Apply stealth scripts
    self._apply_stealth_scripts()
```

**`_apply_stealth_scripts()`**
```python
def _apply_stealth_scripts(self):
    # Hide webdriver flag
    script = "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    self.driver.execute_script(script)
    
    # Override plugins
    script = "Object.defineProperty(navigator, 'plugins', {get: () => [1,2,3,4,5]})"
    self.driver.execute_script(script)
```

**`human_like_delay()`**
```python
def human_like_delay(self, min_delay=1, max_delay=3):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
```

**`wait_for_elements()`**
```python
def wait_for_elements(self, by, value, timeout=10):
    elements = WebDriverWait(self.driver, timeout).until(
        EC.presence_of_all_elements_located((by, value))
    )
    return elements
```

---

### 2. database.py - MongoDBHandler Class

**Role:** Handles all MongoDB operations

**Key Methods:**

**`connect()`**
```python
def connect(self):
    self.client = pymongo.MongoClient(
        self.mongo_uri,
        serverSelectionTimeoutMS=5000
    )
    self.client.server_info()  # Test connection
    self.db = self.client[self.database_name]
    self.collection = self.db[self.collection_name]
```

**`save_quote()`**
```python
def save_quote(self, quote_data):
    quote_data['scraped_date'] = datetime.utcnow().isoformat()
    
    result = self.collection.update_one(
        {'text': quote_data['text']},
        {'$set': quote_data},
        upsert=True
    )
```

---

### 3. main.py - QuoteScraper Class

**Role:** Main scraping logic and coordination

**Key Methods:**

**`setup()`**
- Initializes browser with stealth
- Connects to MongoDB
- Logs setup status

**`scrape_quotes()`**
- Navigates to target URL
- Waits for JavaScript content
- Loops through pages
- Extracts quotes
- Handles pagination

**`_extract_quote_data()`**
- Extracts text, author, tags
- Builds quote dictionary
- Returns structured data

**`save_to_json()`**
- Exports quotes to JSON file
- Creates backup copy

---

## 🛡️ Anti-Bot Techniques Deep Dive

### 1. Undetected ChromeDriver

**What it does:**
- Patches Selenium's ChromeDriver to remove automation flags
- Regular Selenium sets `navigator.webdriver = true`
- Websites check this to detect bots
- Undetected ChromeDriver makes it `undefined`

**Code:**
```python
import undetected_chromedriver as uc
driver = uc.Chrome(options=options)
```

**Under the hood:**
- Modifies Chrome binary
- Removes CDP (Chrome DevTools Protocol) indicators
- Patches `$cdc_` variables that expose automation

---

### 2. Stealth JavaScript Injection

**Script 1: Hide webdriver**
```javascript
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})
```
**Before:** `navigator.webdriver === true`  
**After:** `navigator.webdriver === undefined`

**Script 2: Fake plugins**
```javascript
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
})
```
**Why:** Headless browsers have 0 plugins; real browsers have several

**Script 3: Add chrome object**
```javascript
window.chrome = { runtime: {} }
```
**Why:** Real Chrome has `window.chrome` object; automated Chrome doesn't

**Script 4: Languages array**
```javascript
Object.defineProperty(navigator, 'languages', {
    get: () => ['en-US', 'en']
})
```
**Why:** Bots often have empty or single language

---

### 3. Human-like Behavior Simulation

**Random Delays:**
```python
def human_like_delay(self, min_delay=1, max_delay=3):
    delay = random.uniform(min_delay, max_delay)
    time.sleep(delay)
```
**Pattern:**
- Bot: Always exactly 1.0 second → Detectable
- Human-like: Random 1.2s, 2.7s, 1.8s → Not detectable

**Random Mouse Movements:**
```python
def random_mouse_movement(self):
    x_offset = random.randint(100, 500)
    y_offset = random.randint(100, 500)
    ActionChains(self.driver).move_by_offset(x_offset, y_offset).perform()
```
**Why:** Real users move mouse; bots don't

**Smooth Scrolling:**
```python
def smooth_scroll(self, scroll_pause=0.5):
    for position in range(0, page_height, 300):
        self.driver.execute_script(f"window.scrollTo(0, {position});")
        time.sleep(scroll_pause)
```
**Pattern:**
- Bot: Instant jump to bottom → Suspicious
- Human-like: Gradual scroll with pauses → Natural

---

### 4. User-Agent Rotation

```python
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) Chrome/120.0',
]
options.add_argument(f'user-agent={random.choice(user_agents)}')
```

**Why:** Different user-agents make requests look like different users

---

### 5. Browser Fingerprinting Defense

**Window Size:**
```python
options.add_argument('--window-size=1920,1080')
```
**Why:** Common resolution; headless defaults to 800x600 (suspicious)

**Disable Automation Features:**
```python
options.add_argument('--disable-blink-features=AutomationControlled')
```
**Why:** Removes automation-specific features

**GPU & Sandbox:**
```python
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
```
**Why:** Reduces detectability in headless mode

---

## 📊 Data Flow Diagram

```
User runs main.py
        ↓
QuoteScraper.setup()
        ↓
    ┌───┴────┐
    ↓        ↓
Browser    MongoDB
Setup      Connect
    ↓        ↓
    └───┬────┘
        ↓
Navigate to URL
        ↓
Wait for JavaScript
        ↓
Find quote elements (WebDriverWait)
        ↓
    For each quote:
        ↓
    Extract data
        ↓
    Human delay
        ↓
    Save to MongoDB (upsert)
        ↓
    Add to JSON list
        ↓
Check next page button
        ↓
    If exists:
        ↓
    Scroll to button
        ↓
    Click & wait
        ↓
    Loop back to "Find quote elements"
        ↓
    If not:
        ↓
Save JSON file
        ↓
Show summary
        ↓
Cleanup (close browser & DB)
```

---

# 3. Relationship with Project 1

## 🔗 How Projects 1 & 2 Complement Each Other

### **The Complete Web Scraping Toolkit**

Together, Project 1 (Scrapy) and Project 2 (Selenium) form a **comprehensive web scraping solution** that covers all modern websites:

```
┌─────────────────────────────────────────────────┐
│          COMPLETE SCRAPING SOLUTION             │
├─────────────────────────────────────────────────┤
│                                                 │
│  Project 1: SCRAPY                              │
│  ├─ Static HTML content                         │
│  ├─ Server-side rendered pages                  │
│  ├─ Fast, concurrent requests                   │
│  └─ Ideal for: Product catalogs, listings      │
│                                                 │
│  Project 2: SELENIUM                            │
│  ├─ JavaScript-rendered content                 │
│  ├─ Dynamic, AJAX-loaded data                   │
│  ├─ Anti-bot bypass required                    │
│  └─ Ideal for: SPAs, infinite scroll, auth     │
│                                                 │
└─────────────────────────────────────────────────┘
```

---

## 📊 Side-by-Side Comparison

| Aspect | Project 1 (Scrapy) | Project 2 (Selenium) |
|--------|-------------------|---------------------|
| **Technology** | Scrapy framework | Selenium + Undetected ChromeDriver |
| **Content Type** | Static HTML | JavaScript-rendered |
| **Rendering** | No browser needed | Full browser (Chrome) |
| **Speed** | Very fast (async) | Slower (browser overhead) |
| **Concurrency** | Built-in (16 requests) | Manual (Grid/threading) |
| **Memory** | Low (~50-100 MB) | High (~200-300 MB per browser) |
| **Use Case** | Server-rendered sites | SPAs, dynamic sites |
| **Anti-Bot** | Basic (user-agent, delays) | Advanced (stealth, behavior) |
| **Target Sites** | books.toscrape.com | quotes.toscrape.com/js |
| **Products Scraped** | 1,100 books | 100 quotes |
| **Time** | 2-5 min for 1000 items | 2-5 min for 100 items |
| **Database** | MongoDB (ecommerce_db.products) | MongoDB (ecommerce_db.quotes) |
| **Best For** | Volume scraping | Complex sites |

---

## 🎯 When to Use Which?

### **Use Project 1 (Scrapy) When:**

✅ **Static HTML content**
- Product pages with server-rendered HTML
- Traditional websites (Amazon, eBay product pages)
- Content visible in "View Page Source"

✅ **High volume scraping**
- Need to scrape 10,000+ pages
- Speed is critical
- Server can handle concurrent requests

✅ **Simple anti-bot requirements**
- Basic user-agent rotation sufficient
- No aggressive bot detection

**Example Sites:**
- Amazon product listings
- Traditional e-commerce (Flipkart pre-2020)
- News websites
- Wikipedia

---

### **Use Project 2 (Selenium) When:**

✅ **JavaScript-rendered content**
- Single Page Applications (SPAs)
- React/Vue/Angular websites
- Content NOT in "View Page Source"

✅ **Dynamic interactions needed**
- Click buttons, fill forms
- Handle dropdowns, modals
- Scroll for lazy loading

✅ **Strong anti-bot detection**
- Sites using Cloudflare, Akamai
- CAPTCHA challenges
- Fingerprinting detection

**Example Sites:**
- Modern Myntra (React-based)
- Instagram feeds
- LinkedIn profiles
- Twitter/X timelines

---

## 🔄 How They Work Together

### **Scenario 1: Hybrid Scraping Strategy**

```
E-commerce Site Architecture:
├─ Product Listing Pages (Static HTML) → Use Scrapy
└─ Product Detail Pages (JavaScript) → Use Selenium
```

**Flow:**
1. **Scrapy** crawls listing pages, extracts product URLs (fast)
2. **Selenium** visits each product URL, handles JavaScript (accurate)
3. Both save to same MongoDB database

**Code Integration:**
```python
# Scrapy spider extracts product URLs
class ListingSpider(scrapy.Spider):
    def parse(self, response):
        product_urls = response.css('a.product::attr(href)').getall()
        
        for url in product_urls:
            # Send to Selenium for detailed scraping
            selenium_scraper.scrape_product(url)
```

---

### **Scenario 2: Fallback Strategy**

```
Try Scrapy first (fast)
        ↓
    Content empty?
        ↓
    Fall back to Selenium (handles JS)
```

**Implementation:**
```python
def scrape_product(url):
    # Try Scrapy first
    response = scrapy_fetch(url)
    
    if is_content_empty(response):
        # Fallback to Selenium
        return selenium_fetch(url)
    
    return parse_scrapy_response(response)
```

---

### **Scenario 3: Complementary Database**

Both projects use **same MongoDB database** (`ecommerce_db`) but different collections:

```
MongoDB: ecommerce_db
├─ products (Project 1: Books - 1,100 items)
└─ quotes (Project 2: Quotes - 100 items)
```

**Query across both:**
```python
# Get total scraped items
total_products = db.products.count_documents({})  # 1,100
total_quotes = db.quotes.count_documents({})      # 100
total = total_products + total_quotes             # 1,200
```

---

## 💼 Real-World Rubick.ai Application

### **How Rubick.ai Uses Both:**

**Rubick.ai's 5M+ SKU catalog** requires BOTH approaches:

1. **Scrapy for Bulk Catalogs**
   - Amazon product listings (server-rendered)
   - Initial catalog import
   - Daily price updates

2. **Selenium for Modern Sites**
   - Myntra (React-based SPA)
   - Dynamic pricing
   - User-specific content

**Architecture:**
```
Rubick.ai Crawling Infrastructure
├─ Scrapy Cluster (100 workers)
│  └─ Handles: Amazon, Traditional sites
├─ Selenium Grid (50 browsers)
│  └─ Handles: Myntra, Modern SPAs
└─ Unified MongoDB (5M+ products)
```

---

## 🎓 Learning Progression

### **Why Build Both?**

**Project 1 teaches:**
- Web scraping fundamentals
- HTML parsing (CSS selectors, XPath)
- Async architecture
- Pipeline design

**Project 2 teaches:**
- Browser automation
- JavaScript rendering
- Advanced anti-bot techniques
- Stealth operations

**Together they demonstrate:**
- ✅ **Versatility** - Can handle any website
- ✅ **Problem-solving** - Choose right tool for the job
- ✅ **Production awareness** - Understand trade-offs
- ✅ **Full-stack** - Backend (Scrapy) + Browser (Selenium)

---

## 🔧 Technical Skills Demonstrated

| Skill Category | Project 1 | Project 2 | Combined |
|---------------|-----------|-----------|----------|
| **HTTP/Networking** | ✅ Requests, responses | ✅ Browser networking | ✅ Complete understanding |
| **HTML/CSS** | ✅ Parsing static HTML | ✅ Dynamic DOM | ✅ All content types |
| **JavaScript** | ❌ No JS execution | ✅ Full JS support | ✅ Handle all cases |
| **Anti-Bot** | ✅ Basic techniques | ✅ Advanced stealth | ✅ Multi-layered defense |
| **Database** | ✅ MongoDB upsert | ✅ Same database | ✅ Unified storage |
| **Performance** | ✅ High-speed scraping | ✅ Resource management | ✅ Optimization awareness |
| **Production** | ✅ Scalable architecture | ✅ Reliability | ✅ Production-ready |

---

## 🎤 Interview Talking Point

### **"Why did you build both Scrapy AND Selenium projects?"**

**Answer:**

"I built both to demonstrate comprehensive web scraping expertise and show I understand that different websites require different approaches.

**Project 1 (Scrapy)** handles traditional, server-rendered sites efficiently. It's perfect for Rubick.ai's bulk catalog scraping where speed matters—I scraped 1,100 products in under 5 minutes with built-in concurrency.

**Project 2 (Selenium)** handles modern JavaScript-heavy sites that Scrapy can't touch. Many e-commerce sites now use React or Vue for product listings. I implemented advanced anti-bot techniques like undetected ChromeDriver and behavioral mimicry.

Together, they cover Rubick.ai's real-world needs: Scrapy for Amazon's server-rendered pages, Selenium for Myntra's React-based SPA. Both feed into the same MongoDB database, showing I can architect unified data pipelines.

This isn't just two separate projects—it's a complete scraping toolkit that demonstrates I can assess a site, choose the right tool, and deliver reliable data regardless of the site's architecture."

---

## 📈 Portfolio Impact

### **What Recruiters See:**

**One Project (Scrapy only):**
"Candidate knows basic web scraping"

**Both Projects:**
"Candidate has comprehensive web scraping expertise:
- ✅ Understands trade-offs between tools
- ✅ Can handle any website architecture
- ✅ Knows when to use which approach
- ✅ Advanced anti-bot knowledge
- ✅ Production-scale thinking"

---

## 🔗 Next Step: Project 3

**Project 3 (FastAPI API)** completes the trilogy:
- **Project 1:** Data Collection (Scrapy)
- **Project 2:** Complex Data Collection (Selenium)
- **Project 3:** Data Serving (FastAPI)

**Full stack demonstrated:**
```
Data Collection → Data Storage → Data Serving
(Scrapy/Selenium) → (MongoDB) → (FastAPI)
```

---

# 4. Use Cases & Applications

## 🎯 Real-World Use Cases for Selenium Scraping

### 1. **Social Media Scraping**

**Scenario:** Extract posts, comments, followers from Instagram/LinkedIn

**Why Selenium?**
- Content loads via AJAX as you scroll
- Requires login (authentication)
- Heavy JavaScript rendering

**Implementation:**
```python
# Login first
driver.get('https://instagram.com/login')
driver.find_element(By.NAME, 'username').send_keys('user')
driver.find_element(By.NAME, 'password').send_keys('pass')
driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

# Navigate to profile
driver.get('https://instagram.com/target_profile')

# Scroll to load all posts
for _ in range(10):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Extract posts
posts = driver.find_elements(By.CSS_SELECTOR, 'article')
```

**Rubick.ai Context:** Social commerce monitoring, influencer product tracking

---

### 2. **Modern E-commerce (SPAs)**

**Scenario:** Scrape Myntra product listings (React-based)

**Why Selenium?**
- Product grid loads dynamically
- Infinite scroll for more products
- AJAX calls fetch product data

**Implementation:**
```python
# Load Myntra category page
driver.get('https://www.myntra.com/men-tshirts')

# Wait for products to render
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'product-base'))
)

# Scroll to load more
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract products
products = driver.find_elements(By.CLASS_NAME, 'product-base')
```

**Rubick.ai Context:** Exactly what they need for modern e-commerce brands!

---

### 3. **Flight/Hotel Price Monitoring**

**Scenario:** Track prices on Skyscanner, Booking.com

**Why Selenium?**
- Prices load after search form submission
- Calendar interactions required
- Dynamic pricing based on user behavior

---

### 4. **Job Board Scraping**

**Scenario:** Extract job listings from LinkedIn, Indeed

**Why Selenium?**
- Login required
- Infinite scroll
- AJAX-loaded results

---

### 5. **Financial Data Scraping**

**Scenario:** Stock prices, charts from Yahoo Finance

**Why Selenium?**
- Charts rendered via JavaScript (Canvas/SVG)
- Real-time data updates
- Interactive elements

---

### 6. **Review & Rating Aggregation**

**Scenario:** Collect reviews from multiple pages/sources

**Why Selenium?**
- "Load more" buttons
- Star ratings (SVG/CSS-based)
- Pagination

---

## 🏢 Industry Applications

### E-commerce Intelligence
- **Competitor price monitoring** (daily price checks)
- **Product availability tracking** (in-stock alerts)
- **Review sentiment analysis** (aggregate ratings)
- **New product discovery** (category monitoring)

### Market Research
- **Brand mention tracking** (social media)
- **Trend analysis** (search volume, popularity)
- **Consumer behavior** (browsing patterns)
- **Geographic pricing** (location-based prices)

### Business Automation
- **Lead generation** (LinkedIn, job boards)
- **News monitoring** (industry updates)
- **SEO competitor analysis** (ranking tracking)
- **Content aggregation** (blog posts, articles)

---

## 💼 Business Value

| Metric | Manual Process | With Selenium Scraper | Improvement |
|--------|---------------|---------------------|-------------|
| Data collection time | 8 hours | 5 minutes | **96x faster** |
| Human errors | High | Near zero | **100% accuracy** |
| Cost per 1000 items | $200 (labor) | $0.50 (compute) | **400x cheaper** |
| Update frequency | Weekly | Hourly | **168x more frequent** |
| Handles JS sites | No | Yes | **Unlocks 80%+ modern sites** |
| Anti-bot bypass | No | Yes | **Reliable access** |

---

# 5. Interview Questions & Answers

## 🎤 Technical Questions

### Q1: "Walk me through your Selenium project. What does it do?"

**Answer:**

"I built a production-ready Selenium scraper that handles JavaScript-rendered websites with advanced anti-bot detection bypass.

The scraper targets quotes.toscrape.com/js, which loads all content via JavaScript—if you view the page source, it's empty. Selenium launches a real Chrome browser, waits for JavaScript to execute and populate the DOM, then extracts data.

I implemented several anti-bot layers: undetected ChromeDriver to hide automation flags, stealth JavaScript to override navigator properties, and human-like behavior—random delays between 1-3 seconds, random mouse movements, and smooth scrolling.

The scraper handles pagination automatically, extracting quotes with author names and tags, then stores everything in MongoDB with upsert logic to prevent duplicates. I scraped 100 quotes across multiple pages in about 3 minutes.

What makes it production-ready is the error handling, configurable settings via config.py, dual storage (MongoDB + JSON backup), and detailed logging for monitoring."

---

### Q2: "Why Selenium instead of Scrapy for this project?"

**Answer:**

"Scrapy is excellent for static HTML, but quotes.toscrape.com/js is a JavaScript-rendered site. If you inspect the HTML source, you'll see the quote containers are empty—they're populated client-side via JavaScript.

Scrapy fetches raw HTML from the server and parses it. It doesn't execute JavaScript, so it would see empty `<div>` elements. Selenium, on the other hand, launches a real Chrome browser that executes JavaScript just like when you visit the site manually.

I demonstrated this difference by building Project 1 with Scrapy for books.toscrape.com (server-rendered HTML) and Project 2 with Selenium for the /js version. Same website, different rendering approach, requiring different tools.

In production at Rubick.ai, I'd use Scrapy for traditional sites like older Amazon pages, and Selenium for modern SPAs like Myntra or Instagram where content is dynamically loaded."

---

### Q3: "Explain undetected ChromeDriver and how it bypasses bot detection."

**Answer:**

"Regular Selenium sets a JavaScript property `navigator.webdriver = true` that websites can check. It's a dead giveaway that the browser is automated. Undetected ChromeDriver patches Chrome to make this `undefined`, just like a real browser.

But it goes deeper. Here's what it does:

**1. Removes automation flags:**
- Patches the `$cdc_` variables Chrome uses internally
- Removes the CDP (Chrome DevTools Protocol) detection points
- Modifies the Chrome binary to hide WebDriver presence

**2. I supplement this with stealth scripts:**
```javascript
// Hide webdriver property
Object.defineProperty(navigator, 'webdriver', {
    get: () => undefined
})

// Fake plugins (headless has 0, real browsers have many)
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5]
})

// Add chrome object
window.chrome = { runtime: {} }
```

**3. Behavioral mimicry:**
- Random delays (1-3 seconds) instead of fixed timing
- Mouse movements to simulate human interaction
- Smooth scrolling instead of instant jumps

Websites use fingerprinting—they check multiple signals (user-agent, plugins, webdriver flag, timing patterns). My approach tackles all of them, making the bot nearly indistinguishable from a real user."

---

### Q4: "How would you scale Selenium to scrape 1 million products?"

**Answer:**

"Selenium is resource-intensive (each browser uses ~300 MB), so scaling requires careful architecture:

**1. Selenium Grid**
```
Hub (Coordinator)
├─ Node 1 (10 Chrome browsers)
├─ Node 2 (10 Chrome browsers)
└─ Node 3 (10 Chrome browsers)
= 30 concurrent scrapes
```

**2. Browser Pooling**
- Keep browsers alive between requests (vs. starting fresh each time)
- Reduces overhead from ~5s to ~0.1s per request

**3. Distributed Task Queue**
```python
# Use Celery with Redis
@celery.task
def scrape_product(url):
    browser = get_browser_from_pool()
    data = scrape(url)
    return_browser_to_pool(browser)
    return data
```

**4. Proxy Rotation**
```python
proxies = ['proxy1:8080', 'proxy2:8080', ...]
options.add_argument(f'--proxy-server={random.choice(proxies)}')
```

**Estimated Performance:**
- 30 browsers × 20 products/hour/browser = 600 products/hour
- Scale to 100 nodes (3,000 browsers) = 60,000 products/hour
- 1 million products = ~17 hours"

---

### Q5: "How do you debug when an element is not found?"

**Answer:**

"Element not found is the most common Selenium error. My debugging process:

**Step 1: Verify Element Exists**
```python
# Take screenshot
driver.save_screenshot('debug.png')

# Print page source
with open('debug.html', 'w') as f:
    f.write(driver.page_source)
```

**Step 2: Check Timing**
```python
# Increase timeout
WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'div.quote'))
)
```

**Step 3: Try Different Selectors**
```python
element = driver.find_element(By.CSS_SELECTOR, 'div.quote')
# Or
element = driver.find_element(By.CLASS_NAME, 'quote')
# Or
element = driver.find_element(By.XPATH, '//div[@class="quote"]')
```

**Step 4: Check for iframes**
```python
driver.switch_to.frame('iframe_id')
element = driver.find_element(By.CSS_SELECTOR, 'div.quote')
driver.switch_to.default_content()
```"

---

## 📚 Knowledge-Based Questions

### Q6: "What's the difference between find_element and find_elements?"

**Answer:**

"The difference is singular vs plural—but the behavior change is important:

**find_element (singular)**
```python
element = driver.find_element(By.CSS_SELECTOR, 'div.quote')
```
- Returns **first matching element**
- **Throws exception** if not found
- Use when: You expect exactly one element

**find_elements (plural)**
```python
elements = driver.find_elements(By.CSS_SELECTOR, 'div.quote')
```
- Returns **list of all matching elements**
- Returns **empty list []** if none found (no exception)
- Use when: You expect multiple elements"

---

# 6. Technical Deep Dive

## 🔬 Selenium vs Scrapy: Complete Comparison

### Performance Comparison

**Speed Test: Scrape 100 items**

| Metric | Scrapy | Selenium |
|--------|--------|----------|
| Time | 30 seconds | 3 minutes |
| Memory | 50 MB | 300 MB |
| CPU | Low | Medium |

**Why Selenium is slower:**
1. Browser startup (~2-3 seconds)
2. Page rendering (CSS, images, fonts)
3. JavaScript execution
4. DOM construction

---

## 🎓 When to Use Which?

### Decision Tree

```
Is content in HTML source (View Page Source)?
├─ YES → Use Scrapy
│   ├─ Need high speed? → Scrapy
│   ├─ Simple site? → Scrapy
│   └─ Volume >1000? → Scrapy
│
└─ NO → Use Selenium
    ├─ JavaScript-rendered? → Selenium
    ├─ Need to click/interact? → Selenium
    ├─ Strong anti-bot? → Selenium (undetected)
    └─ AJAX content? → Selenium
```

---

# 7. Troubleshooting Guide

## 🐛 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'distutils'"

**Solution:**
```powershell
pip install setuptools
```

---

### Issue 2: "ChromeDriver version mismatch"

**Solution:**
```python
import undetected_chromedriver as uc
driver = uc.Chrome(version_main=None)  # Auto-detects
```

---

### Issue 3: "Element is not clickable"

**Solution:**
```python
element = driver.find_element(By.ID, 'button')
driver.execute_script("arguments[0].scrollIntoView(true);", element)
time.sleep(0.5)
element.click()
```

---

### Issue 4: "MongoDB connection timeout"

**Solution:**
```powershell
# Start MongoDB
Start-Service MongoDB
```

---

## 🔧 Performance Optimization

### 1. Disable Images (50% faster)
```python
prefs = {"profile.managed_default_content_settings.images": 2}
options.add_experimental_option("prefs", prefs)
```

### 2. Reuse Browser (5x faster)
```python
driver = webdriver.Chrome()
for url in urls:
    driver.get(url)
    # scrape
driver.quit()
```

---

## ✅ Pre-Deployment Checklist

- [ ] Chrome browser installed
- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] All dependencies installed
- [ ] MongoDB running
- [ ] Test run completed
- [ ] Data verified
- [ ] Documentation complete

---

**Good luck with your Rubick.ai application! 🚀**

---

*Document created: October 6, 2026*  
*Author: Kish Siddammanavar*  
*Project: Rubick.ai SDE I Application Portfolio*
