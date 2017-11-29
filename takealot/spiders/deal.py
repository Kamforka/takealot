# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class DealSpider(scrapy.Spider):
    name = 'deal'
    # allowed_domains = ['www.takealot.com/deals']
    start_urls = [
        # 'http://www.takealot.com/deals/',
        # 'https://m.takealot.com/#deals',
        'https://m.takealot.com/#deals?tab=daily-deals',
        ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 2.0}, )


    def parse(self, response):
        """parse from mobile site"""

        products = response.xpath('//div[@class="product-wrapper"]')

        for product in products:
            deal_title = product.xpath('.//a[@id="deal_title"]')
            product_name = deal_title.xpath('./text()').extract_first()
            url_mobile = response.urljoin(deal_title.xpath('./@href').extract_first())
            url_desktop = ''
            price_normal = product.xpath('.//span[@class="was-price"]/text()').extract_first('')
            price_offer = product.xpath('.//span[@class="amount"]/text()').extract_first('').strip()
            stock_remaining = product.xpath('.//div[@class="only-n-left"]/span/text()').extract_first()

            yield {
                'product_name': product_name,
                'url_mobile': url_mobile,
                'url_desktop': url_desktop,
                'price_normal': price_normal,
                'price_offer': price_offer,
                'stock_remaining': stock_remaining,
            }

    # def parse(self, response):
    # """parse from desktop site"""
    #     deals = response.xpath('//a[@class="get-the-deal"]/@href').extract()
    #
    #     for deal in deals:
    #         ysield {
    #             'url': deal,
    #             }
    #
    #     next_page = response.xpath('//a[@rel="next"]/@href').extract_first('')
    #     next_page = response.urljoin(next_page)
    #     print('next page: {}'.format(next_page))
    #
    #     # yield response.follow(next_page, callback=self.parse, args={'wait': 0.5},)
    #     yield SplashRequest(next_page, self.parse, args={'wait': 0.5}, )

    def parse_deal(self, response):
        """
        -Product Name
        -Product URL (both mobile and Desktop URL)
        -Product Category
        -Seller Name
        -RRP
        -'Normal' Selling Price
        -Offer Price
        -Number of stock remaining
        -Which warehouses hold stock
        """
        pass
