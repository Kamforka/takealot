# -*- coding: utf-8 -*-
"""Takealot daily deals item scraper."""
import json
import requests

import scrapy

from takealot.items import TakealotItem

API_DAILY_DEALS_URL = ('https://api.takealot.com/rest/v-1-5-2/productlines/search'
                       '?rows={rows}&start={offset}&backend=arj-fbye-zz-fla-fcenax'
                       '&filter=Promotions:{id}&sort=Price%20Descending'
                       '&detail=mlisting&filter=Available:true')

API_PRODUCT_URL = 'https://api.takealot.com/rest/v-1-5-2/productline/{id}'

MOBILE_ITEM_URL_TEMPLATE = 'https://m.takealot.com/#product?id={id}'

def get_daily_id():
    """Retrieve daily deal id from takealot api."""
    promo_url = 'https://api.takealot.com/rest/v-1-5-2/promotions'
    response = requests.get(promo_url)
    for resp in response.json()['response']:
        if resp['name'] == 'Daily Deal':
            return resp['id']


class DealsSpider(scrapy.Spider):
    """Spider to crawl daily deals from takealot.com/deals"""
    name = 'deals'
    allowed_domains = ['api.takealot.com']
    custom_settings = {
        'FEED_EXPORT_FIELDS': ['id', 'product_name'],
        'ITEM_PIPELINES': {
            'takealot.pipelines.DailyDealsPipeline': 300,
        }
    }

    def __init__(self, *args, **kwargs):
        """Constructor."""
        self.rows = 100
        self.daily_id = get_daily_id()
        self.start_urls = [
            API_DAILY_DEALS_URL.format(rows=self.rows,
                                       offset=0,
                                       id=self.daily_id)
        ]

        super(DealsSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        """Parse daily deal product."""
        body = json.loads(response.body.decode('utf-8'))
        num_found = body['results']['num_found']
        products = body['results']['productlines']

        for product in products:
            item = TakealotItem()
            item['id'] = product['id']
            item['product_name'] = product['title']
            item['url_desktop'] = product['uri']
            item['url_mobile'] = MOBILE_URL_TEMPLATE.format(id=product['id'])
            # item['product_category'] = ''
            item['seller_name'] = product['seller_name']
            item['price_normal'] = product['old_selling_price'] / 100.
            item['price_offer'] = product['selling_price'] / 100.
            item['stock_remaining'] = product['stock_on_hand']
            item['warehouses'] = product['shipping_information']['stock_warehouses']

            yield item

        offset = int(body['params']['start'][0]) + ITEM_ROWS
        if offset < num_found:
            yield response.follow(self.daily_url.format(rows=self.rows,
                                                        offset=offset,
                                                        id=self.daily_id))
