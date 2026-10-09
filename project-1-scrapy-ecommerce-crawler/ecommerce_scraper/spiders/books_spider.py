import scrapy
from ecommerce_scraper.items import ProductItem
from urllib.parse import urljoin


class BooksSpider(scrapy.Spider):
    """Spider for scraping books from books.toscrape.com"""

    name = 'books_spider'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    custom_settings = {
        'FEEDS': {
            'products.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True,
            }
        }
    }

    def parse(self, response):
        """Parse product listing page"""
        self.logger.info(f'Parsing page: {response.url}')

        # Extract all product links
        products = response.css('article.product_pod')

        for product in products:
            # Get product detail page URL
            product_url = product.css('h3 a::attr(href)').get()
            if product_url:
                yield response.follow(product_url, callback=self.parse_product)

        # Follow pagination
        next_page = response.css('li.next a::attr(href)').get()
        if next_page:
            self.logger.info(f'Following next page: {next_page}')
            yield response.follow(next_page, callback=self.parse)

    def parse_product(self, response):
        """Parse individual product page"""

        # Extract product ID from URL
        product_id = response.url.split('/')[-2]

        # Initialize item
        item = ProductItem()

        # Basic information
        item['product_id'] = product_id
        item['title'] = response.css('div.product_main h1::text').get()
        item['url'] = response.url

        # Price information
        price_text = response.css('p.price_color::text').get()
        item['price'] = price_text.replace('£', '').strip() if price_text else '0'
        item['currency'] = 'GBP'

        # Check for original price (if on sale)
        original_price = response.css('p.price_color + p.price_color::text').get()
        item['original_price'] = original_price if original_price else item['price']

        # Rating
        rating_class = response.css('p.star-rating::attr(class)').get()
        rating_map = {
            'One': 1.0,
            'Two': 2.0,
            'Three': 3.0,
            'Four': 4.0,
            'Five': 5.0
        }
        rating_text = rating_class.split()[-1] if rating_class else 'Zero'
        item['rating'] = rating_map.get(rating_text, 0.0)

        # Availability
        availability_text = response.css('p.availability::text').getall()
        item['availability'] = ''.join(availability_text).strip()

        # Category
        breadcrumb = response.css('ul.breadcrumb li a::text').getall()
        item['category'] = breadcrumb[-1] if len(breadcrumb) > 1 else 'Unknown'

        # Image URL
        image_url = response.css('div.item.active img::attr(src)').get()
        item['image_url'] = urljoin(response.url, image_url) if image_url else ''

        # Reviews count (not available on this site, set to 0)
        item['reviews_count'] = 0

        # Source website
        item['source_website'] = 'books.toscrape.com'

        # Calculate discount if applicable
        try:
            current_price = float(item['price'])
            orig_price = float(str(item['original_price']).replace('£', ''))
            if orig_price > current_price:
                item['discount'] = round(((orig_price - current_price) / orig_price) * 100, 2)
            else:
                item['discount'] = 0.0
        except:
            item['discount'] = 0.0

        self.logger.info(f'Scraped product: {item["title"]}')

        yield item
