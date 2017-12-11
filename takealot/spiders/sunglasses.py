# -*- coding: utf-8 -*-
"""Takealot sunglass item scraper."""
import scrapy

from takealot.spiders import API_PRODUCT_URL, SpiderBase


class SunglassSpider(SpiderBase):
    """Spider to crawl sunglasses from takealot.com"""
    name = 'sunglasses'
    allowed_domains = ['api.takealot.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'takealot.pipelines.DefaultValuePipeline': 300,
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
