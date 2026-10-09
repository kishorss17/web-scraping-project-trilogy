import scrapy


class ProductItem(scrapy.Item):
    """Product Item for storing scraped product data"""

    # Product identification
    product_id = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()

    # Pricing information
    price = scrapy.Field()
    original_price = scrapy.Field()
    discount = scrapy.Field()
    currency = scrapy.Field()

    # Product details
    rating = scrapy.Field()
    reviews_count = scrapy.Field()
    availability = scrapy.Field()
    category = scrapy.Field()

    # Images
    image_url = scrapy.Field()

    # Metadata
    scraped_date = scrapy.Field()
    source_website = scrapy.Field()
