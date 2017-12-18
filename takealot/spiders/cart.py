
# -*- coding: utf-8 -*-
"""Takealot sunglass item scraper."""
import scrapy

from scrapy.http import FormRequest
from scrapy_splash import SplashRequest

from takealot.spiders import API_PRODUCT_URL, SpiderBase

API_LOOKUP_URL = 'https://api.takealot.com/rest/v-1-5-2/productlines/lookup?idProduct={prod_id}'

class CartSpider(SpiderBase):
    """Test"""
    name = 'cart'
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
    start_urls = [
        'http://www.takealot.com/lentes-marcos-avenida-de-la-paz-polarised-black-cat-eye-sunglass/PLID45086316',
        'http://www.takealot.com/lentes-marcos-anton-martin-uv400-black-silver-pilot-sunglasses/PLID45086305',
        'http://www.takealot.com/lentes-marcos-avatcha-uv400-gun-pilot-sunglasses/PLID45086306',
        'http://www.takealot.com/lentes-marcos-legazpi-uv400-navy-white-wayfarer-sunglasses/PLID45086307',
        'http://www.takealot.com/lentes-marcos-delicias-uv400-silver-round-sunglasses/PLID45086308',
        'http://www.takealot.com/lentes-marcos-conde-de-casal-uv400-amber-black-cat-eye-sunglasse/PLID45086310',
        'http://www.takealot.com/lentes-marcos-mendez-alvaro-polarised-tortoise-shell-black-gold-/PLID45086311',
        'http://www.takealot.com/lentes-marcos-piramides-polarised-amber-grey-cat-eye-sunglasses/PLID45086318',
        'http://www.takealot.com/lentes-marcos-o-donnell-polarised-amber-gold-cat-eye-sunglasses/PLID45086312',
        'http://www.takealot.com/lentes-marcos-gran-via-polarised-black-flat-top-mirrored-sunglas/PLID45086321',
        'http://www.takealot.com/lentes-marcos-carpetana-polarised-mirrored-cat-eye-sunglasses/PLID45086327',
        'http://www.takealot.com/lentes-marcos-rios-rosas-polarised-black-oversized-sunglasses/PLID42070594',
        'http://www.takealot.com/lentes-marcos-pinar-de-campoverde-amber-tortoise-shell-wayfarer-/PLID45086325',
        'http://www.takealot.com/lentes-marcos-el-carmen-polarised-white-green-sports-sunglasses/PLID42070602',
        'http://www.takealot.com/lentes-marcos-delicias-uv400-amber-black-round-sunglasses/PLID45086309',
        'http://www.takealot.com/lentes-marcos-alvarado-uv400-black-shield-sunglasses/PLID42070624',
        'http://www.takealot.com/lentes-marcos-la-elipa-uv400-mirrored-club-master-sunglasses/PLID45086315',
        'http://www.takealot.com/lentes-marcos-vista-alegra-uv400-black-wayfarer-sunglasses/PLID42070691',
        'http://www.takealot.com/lentes-marcos-la-gavia-uv400-black-rectangle-sunglasses/PLID45086324',
        'http://www.takealot.com/lentes-marcos-tirso-de-molina-polarised-black-wrap-sunglasses/PLID42070615',
        'http://www.takealot.com/lentes-marcos-atocha-polarised-silver-rectangle-sunglasses/PLID42070675',
        'http://www.takealot.com/lentes-marcos-menendez-pelayo-polarised-silver-grey-pilot-sungla/PLID42070613',
    ]
    cart_url = 'https://www.takealot.com/cart'

    def start_requests(self):
        """Request dispatchers."""
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html')

    def parse(self, response):
        """Parse the product page.

        Add the product to cart using the add-form on the page.
        Then redirect to the cart page.
        """
        prod_id = response.meta.get('prod_id')
        if prod_id:
            yield SplashRequest(self.cart_url, self.parse_cart,
                                endpoint='render.html', dont_filter=True,
                                meta=response.meta.copy())
        else:
            prod_id = response.xpath('//input[@name="idProduct"]/@value').extract_first()
            yield FormRequest.from_response(response, formcss='form.add-form',
                                            meta={'prod_id': prod_id})

    def parse_cart(self, response):
        """Parse the cart page.

        First submit the cart-form with a value of 9999 to get
        the updated quantity of the product stocks.
        Then scrape the updated value of the product.
        """
        updated = response.meta.get('updated')
        prod_id = response.meta.get('prod_id')

        if not updated:
            qty_key = 'qty[{}]'.format(prod_id)
            data = {
                qty_key: '9999',
            }

            update_meta = response.meta.copy()
            update_meta['updated'] = True

            yield FormRequest.from_response(response, formid='cart-form', formdata=data,
                                            callback=self.parse_cart, meta=update_meta)
        else:
            stock_remaining = response.xpath('//input[@id="{}"]/@value'
                                             .format(prod_id)).extract_first()

            yield scrapy.Request(API_LOOKUP_URL.format(prod_id=prod_id),
                                 callback=self.parse_item,
                                 meta={'stock_remaining': stock_remaining})


    def parse_item(self, response):
        """Overriden parse_item method.

        Override the base implementation to replace the original stock_remaining
        field - that is returned by the server - by the cart update value.
        """
        item = self.load_item(response)
        item['stock_remaining'] = response.meta.get('stock_remaining')
        yield item
