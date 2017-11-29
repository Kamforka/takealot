# -*- coding: utf-8 -*-
import json
import requests

import scrapy

from takealot.items import TakealotItem

ITEM_ROWS = 100
MOBILE_URL_TEMPLATE = 'https://m.takealot.com/#product?id={id}'

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
    rows = ITEM_ROWS
    daily_id = get_daily_id()
    daily_url = ('https://api.takealot.com/rest/v-1-5-2/productlines/search'
                '?rows={rows}&start={offset}&backend=arj-fbye-zz-fla-fcenax'
                '&filter=Promotions:{id}&sort=BestSelling%20Descending'
                '&detail=mlisting&filter=Available:true')
    allowed_domains = ['api.takealot.com']
    start_urls = [
        daily_url.format(rows=rows, offset=0, id=daily_id),
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'takealot.pipelines.DailyDealsPipeline': 300,
        }
    }

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
