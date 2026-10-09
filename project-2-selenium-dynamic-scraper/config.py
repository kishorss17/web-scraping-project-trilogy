"""
Configuration settings for Selenium scraper
"""

# MongoDB Configuration
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DATABASE = 'ecommerce_db'
MONGO_COLLECTION = 'quotes'

# Scraping Configuration
TARGET_URL = 'https://quotes.toscrape.com/js/'
MAX_QUOTES = 100  # Maximum quotes to scrape

# Browser Configuration
HEADLESS_MODE = True  # Set to False to see browser in action
WINDOW_SIZE = (1920, 1080)

# Anti-Bot Configuration
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
]

# Human-like behavior settings
MIN_DELAY = 1  # Minimum delay between actions (seconds)
MAX_DELAY = 3  # Maximum delay between actions (seconds)
SCROLL_PAUSE = 0.5  # Pause after scrolling

# Stealth settings
ENABLE_STEALTH = True  # Enable undetected-chromedriver
BLOCK_IMAGES = False  # Block image loading for faster scraping
