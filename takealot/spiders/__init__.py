#-*-coding: utf-8-*-
"""Takealot base spider."""
import json

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import SelectJmes, TakeFirst
from takealot.items import TakealotItem

# API product url template
API_PRODUCT_URL = 'https://api.takealot.com/rest/v-1-5-2/productline/{id}'


class SpiderBase(scrapy.Spider):
    """Takealot base spider."""
    jmes_paths = {
        'id': 'id',
        'product_name': 'title',
        'product_category': 'categories[*].name',
        'url_desktop': 'uri',
        'url_mobile': 'id',
        'seller_name': 'skus[0].seller_name',
        'seller_url': 'skus[0].seller_id',
        'price_normal': 'old_selling_price',
        'price_offer': 'selling_price',
        'stock_remaining': 'stock_on_hand',
        'warehouses': 'shipping_information.stock_warehouses',
    }

    def parse(self, response):
        """Parse stub."""
        pass

    def parse_item(self, response):
        """Parse a takealot item."""
        yield self.load_item(response)

    def load_item(self, response):
        """Load product item from takealot api product response."""
        jsonresponse = self.get_jsonresponse(response)
        product = jsonresponse['response']

        loader = ItemLoader(item=TakealotItem())
        # loader.default_output_processor = TakeFirst()
        for (field, path) in self.jmes_paths.items():
            loader.add_value(field, SelectJmes(path)(product))

        return loader.load_item()



    @staticmethod
    def get_jsonresponse(response, encoding='utf-8'):
        """Retrieve body dictionary from `Response` object."""
        return json.loads(response.body.decode(encoding))
