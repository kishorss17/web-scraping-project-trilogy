"""
Selenium browser manager with anti-bot capabilities
"""
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import random
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SeleniumBrowser:
    """Manages Selenium browser with anti-bot features"""

    def __init__(self, headless=True, window_size=(1920, 1080), enable_stealth=True):
        """
        Initialize browser with anti-bot configuration

        Args:
            headless: Run browser in headless mode
            window_size: Browser window size (width, height)
            enable_stealth: Use undetected-chromedriver
        """
        self.headless = headless
        self.window_size = window_size
        self.enable_stealth = enable_stealth
        self.driver = None

    def setup_driver(self):
        """Setup Chrome driver with stealth options"""
        try:
            logger.info("Setting up Chrome driver...")

            # Chrome options for anti-bot
            options = uc.ChromeOptions()

            if self.headless:
                options.add_argument('--headless=new')

            # Anti-detection arguments
            options.add_argument(f'--window-size={self.window_size[0]},{self.window_size[1]}')
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--dns-prefetch-disable')

            # Random user agent
            user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            ]
            options.add_argument(f'user-agent={random.choice(user_agents)}')

            # Initialize undetected Chrome driver
            self.driver = uc.Chrome(options=options, version_main=None)

            # Set page load timeout
            self.driver.set_page_load_timeout(30)

            # Execute stealth JavaScript
            self._apply_stealth_scripts()

            logger.info("✓ Chrome driver setup complete (stealth mode enabled)")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to setup driver: {e}")
            return False

    def _apply_stealth_scripts(self):
        """Apply JavaScript to hide automation indicators"""
        stealth_scripts = [
            # Override navigator.webdriver
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})",

            # Override plugins
            "Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})",

            # Override languages
            "Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})",

            # Chrome property
            "window.chrome = { runtime: {} }",
        ]

        for script in stealth_scripts:
            try:
                self.driver.execute_script(script)
            except:
                pass

    def human_like_delay(self, min_delay=1, max_delay=3):
        """
        Random delay to mimic human behavior

        Args:
            min_delay: Minimum delay in seconds
            max_delay: Maximum delay in seconds
        """
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)

    def random_mouse_movement(self):
        """Simulate random mouse movements"""
        try:
            action = ActionChains(self.driver)
            # Move to random position
            x_offset = random.randint(100, 500)
            y_offset = random.randint(100, 500)
            action.move_by_offset(x_offset, y_offset).perform()
            time.sleep(0.1)
        except:
            pass

    def smooth_scroll(self, scroll_pause=0.5):
        """
        Smoothly scroll page like human

        Args:
            scroll_pause: Pause duration between scrolls
        """
        try:
            # Get page height
            last_height = self.driver.execute_script("return document.body.scrollHeight")

            # Scroll in increments
            current_position = 0
            scroll_increment = 300

            while current_position < last_height:
                current_position += scroll_increment
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                time.sleep(scroll_pause)

                # Check if page height changed (lazy loading)
                new_height = self.driver.execute_script("return document.body.scrollHeight")
                if new_height > last_height:
                    last_height = new_height

        except Exception as e:
            logger.debug(f"Scroll error: {e}")

    def wait_for_element(self, by, value, timeout=10):
        """
        Wait for element to be present

        Args:
            by: Selenium By locator (By.CSS_SELECTOR, By.XPATH, etc.)
            value: Locator value
            timeout: Maximum wait time in seconds

        Returns:
            WebElement if found, None otherwise
        """
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            logger.debug(f"Element not found: {value}")
            return None

    def wait_for_elements(self, by, value, timeout=10):
        """
        Wait for multiple elements to be present

        Args:
            by: Selenium By locator
            value: Locator value
            timeout: Maximum wait time

        Returns:
            List of WebElements
        """
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((by, value))
            )
            return elements
        except Exception as e:
            logger.debug(f"Elements not found: {value}")
            return []

    def get_page(self, url):
        """
        Navigate to URL with human-like behavior

        Args:
            url: Target URL
        """
        try:
            logger.info(f"Navigating to: {url}")
            self.driver.get(url)

            # Wait for page to load
            self.human_like_delay(2, 4)

            # Random mouse movement
            self.random_mouse_movement()

            logger.info("✓ Page loaded successfully")
            return True

        except Exception as e:
            logger.error(f"✗ Failed to load page: {e}")
            return False

    def close(self):
        """Close browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")
