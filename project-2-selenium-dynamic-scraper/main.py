"""
Main scraper for quotes.toscrape.com/js
Uses Selenium to handle JavaScript-rendered content
"""
from selenium.webdriver.common.by import By
from scraper.browser import SeleniumBrowser
from scraper.database import MongoDBHandler
import config
import logging
import time
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QuoteScraper:
    """Scrapes quotes from JavaScript-rendered website"""

    def __init__(self):
        """Initialize scraper with browser and database"""
        self.browser = SeleniumBrowser(
            headless=config.HEADLESS_MODE,
            window_size=config.WINDOW_SIZE,
            enable_stealth=config.ENABLE_STEALTH
        )
        self.db = MongoDBHandler(
            config.MONGO_URI,
            config.MONGO_DATABASE,
            config.MONGO_COLLECTION
        )
        self.quotes_scraped = 0
        self.quotes_data = []

    def setup(self):
        """Setup browser and database connections"""
        logger.info("=" * 60)
        logger.info("SELENIUM DYNAMIC SCRAPER - PROJECT 2")
        logger.info("=" * 60)

        # Setup browser
        if not self.browser.setup_driver():
            logger.error("Failed to setup browser. Exiting.")
            return False

        # Connect to database
        if not self.db.connect():
            logger.error("Failed to connect to MongoDB. Exiting.")
            return False

        logger.info("✓ Setup complete. Starting scrape...")
        return True

    def scrape_quotes(self):
        """Scrape quotes from the website"""
        try:
            # Navigate to target URL
            if not self.browser.get_page(config.TARGET_URL):
                return False

            # Wait for JavaScript to render content
            logger.info("Waiting for JavaScript content to load...")
            time.sleep(3)

            page_number = 1
            quotes_on_page = True

            while quotes_on_page and self.quotes_scraped < config.MAX_QUOTES:
                logger.info(f"\n📄 Scraping page {page_number}...")

                # Wait for quote elements to load
                quote_elements = self.browser.wait_for_elements(
                    By.CSS_SELECTOR,
                    'div.quote',
                    timeout=10
                )

                if not quote_elements:
                    logger.warning("No quotes found on page. Stopping.")
                    break

                # Extract quotes from current page
                for quote_elem in quote_elements:
                    if self.quotes_scraped >= config.MAX_QUOTES:
                        break

                    quote_data = self._extract_quote_data(quote_elem)
                    if quote_data:
                        # Save to database
                        self.db.save_quote(quote_data)
                        self.quotes_data.append(quote_data)
                        self.quotes_scraped += 1

                        logger.info(f"✓ Scraped quote {self.quotes_scraped}: \"{quote_data['text'][:60]}...\"")

                    # Human-like delay between quotes
                    self.browser.human_like_delay(
                        config.MIN_DELAY,
                        config.MAX_DELAY
                    )

                # Check for next page button
                try:
                    next_button = self.browser.driver.find_element(
                        By.CSS_SELECTOR,
                        'li.next > a'
                    )

                    if next_button and self.quotes_scraped < config.MAX_QUOTES:
                        logger.info("➡️  Moving to next page...")

                        # Scroll to next button
                        self.browser.driver.execute_script(
                            "arguments[0].scrollIntoView(true);",
                            next_button
                        )
                        time.sleep(1)

                        # Click next button
                        next_button.click()

                        # Wait for new content to load
                        time.sleep(3)

                        page_number += 1
                    else:
                        quotes_on_page = False

                except Exception as e:
                    logger.info("No more pages available.")
                    quotes_on_page = False

            return True

        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            return False

    def _extract_quote_data(self, quote_element):
        """
        Extract data from a single quote element

        Args:
            quote_element: Selenium WebElement for quote

        Returns:
            Dictionary with quote data
        """
        try:
            # Extract text
            text_elem = quote_element.find_element(By.CSS_SELECTOR, 'span.text')
            text = text_elem.text.strip()

            # Extract author
            author_elem = quote_element.find_element(By.CSS_SELECTOR, 'small.author')
            author = author_elem.text.strip()

            # Extract tags
            tag_elements = quote_element.find_elements(By.CSS_SELECTOR, 'div.tags a.tag')
            tags = [tag.text.strip() for tag in tag_elements]

            # Extract author URL (if available)
            try:
                author_link = quote_element.find_element(By.CSS_SELECTOR, 'a[href*="/author/"]')
                author_url = author_link.get_attribute('href')
            except:
                author_url = None

            quote_data = {
                'text': text,
                'author': author,
                'author_url': author_url,
                'tags': tags,
                'source': 'quotes.toscrape.com/js'
            }

            return quote_data

        except Exception as e:
            logger.error(f"Error extracting quote data: {e}")
            return None

    def save_to_json(self, filename='quotes.json'):
        """
        Save scraped quotes to JSON file

        Args:
            filename: Output filename
        """
        try:
            filepath = f"data/{filename}"
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.quotes_data, f, ensure_ascii=False, indent=2)

            logger.info(f"✓ Saved {len(self.quotes_data)} quotes to {filepath}")
            return True

        except Exception as e:
            logger.error(f"Error saving to JSON: {e}")
            return False

    def show_summary(self):
        """Display scraping summary"""
        logger.info("\n" + "=" * 60)
        logger.info("SCRAPING COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"✓ Total quotes scraped: {self.quotes_scraped}")
        logger.info(f"✓ Saved to MongoDB: {config.MONGO_DATABASE}.{config.MONGO_COLLECTION}")
        logger.info(f"✓ Saved to JSON: data/quotes.json")

        # Get database count
        db_count = self.db.get_quote_count()
        logger.info(f"✓ Total quotes in database: {db_count}")
        logger.info("=" * 60)

    def cleanup(self):
        """Close browser and database connections"""
        self.browser.close()
        self.db.close()
        logger.info("Cleanup complete.")


def main():
    """Main execution function"""
    scraper = QuoteScraper()

    try:
        # Setup
        if not scraper.setup():
            return

        # Scrape quotes
        success = scraper.scrape_quotes()

        if success:
            # Save to JSON
            scraper.save_to_json()

            # Show summary
            scraper.show_summary()

    except KeyboardInterrupt:
        logger.info("\n⚠️  Scraping interrupted by user")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")

    finally:
        # Always cleanup
        scraper.cleanup()


if __name__ == "__main__":
    main()
