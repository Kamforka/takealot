# -*- coding: utf-8 -*-
"""Takealot daily deals item scraper."""
import datetime as dt
import json
import requests

import scrapy

from takealot.items import TakealotItem

API_DAILY_DEALS_URL = ('https://api.takealot.com/rest/v-1-5-2/productlines/search'
                       '?rows={rows}&start={offset}&backend=arj-fbye-zz-fla-fcenax'
                       '&filter=Promotions:{id}&sort=ReleaseDate%20Descending'
                       '&detail=mlisting&filter=Available:true')

API_PRODUCT_URL = 'https://api.takealot.com/rest/v-1-5-2/productline/{id}'

MOBILE_ITEM_URL_TEMPLATE = 'https://m.takealot.com/#product?id={id}'

SELLER_URL_TEMPLATE = 'https://www.takealot.com/seller-profile.php?sellers={id}'

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
        # last scrape of the day
        self.last_scrape = kwargs.get('last', False)
        # start hour of the daily scrape
        self.start_hour = int(kwargs.get('start_hour', 7))

        # fields to be scraped during hourly scraping
        self.hourly_fields = ['stock_remaining']

        # fields to be exported
        self.export_fields = [
            'id', 'date', 'product_name', 'product_category', 'url_desktop', 'url_mobile',
            'seller_name', 'price_normal', 'price_offer', 'warehouses', 'stock_remaining',
        ]

        self.rows = 199  # number of items to be retrieved (api allows max 199)
        self.daily_id = get_daily_id()  # promo id of the actual daily deal
        self.start_urls = [
            API_DAILY_DEALS_URL.format(rows=self.rows,
                                       offset=0,
                                       id=self.daily_id)
        ]

        super(DealsSpider, self).__init__(*args, **kwargs)


    def parse(self, response):
        """Parse daily deal product."""
        jsonresponse = self.get_jsonresponse(response)
        num_found = jsonresponse['results']['num_found']
        products = jsonresponse['results']['productlines']

        for product in products:
            # the api response of the product doesn't have the seller_name field
            # so it must be recorded here and passed as meta of the product request
            seller_name = product['seller_name']
            yield response.follow(API_PRODUCT_URL.format(id=product['id']),
                                  callback=self.parse_item,
                                  meta={'seller_name': seller_name})

        offset = int(jsonresponse['params']['start'][0]) + self.rows
        if offset < num_found:
            yield response.follow(API_DAILY_DEALS_URL.format(rows=self.rows,
                                                             offset=offset,
                                                             id=self.daily_id))

    def parse_item(self, response):
        """Parse additional properties from product page."""
        jsonresponse = self.get_jsonresponse(response)
        product = jsonresponse['response']

        item = TakealotItem()
        item['seller_name'] = response.meta['seller_name']

        item['id'] = product['id']
        item['date'] = '{:%Y-%m-%d}'.format(dt.datetime.now())
        item['product_name'] = product['title']
        item['url_desktop'] = product['uri']
        item['url_mobile'] = MOBILE_ITEM_URL_TEMPLATE.format(id=product['id'])
        item['price_normal'] = product['old_selling_price'] / 100.
        item['price_offer'] = product['selling_price'] / 100.
        item['stock_remaining'] = product['stock_on_hand']
        item['warehouses'] = product['shipping_information']['stock_warehouses']

        categories = product['categories']
        item['product_category'] = [category['name'] for category in categories]

        yield item

    @staticmethod
    def get_jsonresponse(response, encoding='utf-8'):
        """Retrieve body dictionary from `Response` object."""
        return json.loads(response.body.decode(encoding))
