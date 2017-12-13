# -*- coding: utf-8 -*-
"""Takealot sunglass item scraper."""
import scrapy

from takealot.spiders import API_PRODUCT_URL, SpiderBase


class SunglassSpider(SpiderBase):
    """Spider to crawl sunglasses from takealot.com"""
    name = 'sunglasses'
    allowed_domains = ['api.takealot.com']
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            'id', 'date', 'product_name', 'product_category', 'url_desktop', 'url_mobile',
            'seller_name', 'seller_url', 'price_normal', 'price_offer', 'warehouses',
            'stock_remaining',
            ],
        'ITEM_PIPELINES': {
            'takealot.pipelines.DefaultValuePipeline': 300,
            'takealot.pipelines.DailyDealsPipeline': 301,
        }
    }
    sunglass_ids = [
        'PLID46853383',
        'PLID45216917',
        'PLID42070777',
        'PLID40758214',
    ]

    def start_requests(self):
        for id_ in self.sunglass_ids:
            yield scrapy.Request(API_PRODUCT_URL.format(id=id_),
                                 callback=self.parse_item)
