# -*- coding: utf-8 -*-
"""Takealot item models."""
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

MOBILE_ITEM_URL_TEMPLATE = 'https://m.takealot.com/#product?id={id}'
SELLER_URL_TEMPLATE = 'https://www.takealot.com/seller-profile.php?sellers={id}'

def seller_url_processor(seller_id):
    """Input processor for `seller_url`."""
    return SELLER_URL_TEMPLATE.format(id=seller_id) if seller_id else None

def mobile_url_processor(prod_id):
    """Input processor for `mobile_url`."""
    return MOBILE_ITEM_URL_TEMPLATE.format(id=prod_id)

def price_processor(price):
    """Input processor for product price."""
    return price / 100.

class TakealotItem(scrapy.Item):
    """Takealot item definition."""
    id = scrapy.Field(output_processor=TakeFirst())
    date = scrapy.Field()
    product_name = scrapy.Field(output_processor=TakeFirst())
    product_category = scrapy.Field()
    url_desktop = scrapy.Field(output_processor=TakeFirst())
    url_mobile = scrapy.Field(input_processor=MapCompose(mobile_url_processor),
                              output_processor=TakeFirst())
    seller_name = scrapy.Field(output_processor=TakeFirst())
    seller_url = scrapy.Field(input_processor=MapCompose(seller_url_processor),
                              output_processor=TakeFirst())
    price_normal = scrapy.Field(input_processor=MapCompose(price_processor),
                                output_processor=TakeFirst())
    price_offer = scrapy.Field(input_processor=MapCompose(price_processor),
                               output_processor=TakeFirst())
    stock_remaining = scrapy.Field(output_processor=TakeFirst())
    warehouses = scrapy.Field()
