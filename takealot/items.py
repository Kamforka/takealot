# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class TakealotItem(scrapy.Item):
    """Takealot item definition."""
    # define the fields for your item here like:
    id = scrapy.Field()
    product_name = scrapy.Field()
    product_category = scrapy.Field()
    url_desktop = scrapy.Field()
    url_mobile = scrapy.Field()
    seller_name = scrapy.Field()
    price_normal = scrapy.Field()
    price_offer = scrapy.Field()
    stock_remaining = scrapy.Field()
    warehouses = scrapy.Field()
