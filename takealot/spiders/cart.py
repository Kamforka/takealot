
# -*- coding: utf-8 -*-
"""Takealot sunglass item scraper."""
import scrapy

from scrapy_splash import SplashRequest, SplashFormRequest

from takealot.spiders import SpiderBase

# api product lookup url template by product id
API_LOOKUP_URL = 'https://api.takealot.com/rest/v-1-5-2/productlines/lookup?idProduct={prod_id}'

# lua script to retrieve cookies from response
COOKIE_SCRIPT = """function main(splash)
  splash:init_cookies(splash.args.cookies)
  assert(splash:go{
    splash.args.url,
    headers=splash.args.headers,
    http_method=splash.args.http_method,
    body=splash.args.body,
    })
  assert(splash:wait(0.5))

  local entries = splash:history()
  local last_response = entries[#entries].response
  return {
    url = splash:url(),
    cookies = splash:get_cookies(),
    html = splash:html(),
  }
end"""

def get_item_urls(path):
    """Retrieve a list of item urls from a text file."""
    with open(path, 'r') as url_file:
        urls = url_file.readlines()
    return urls


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

    start_urls = get_item_urls('imports/sunglass_urls.txt')
    cart_url = 'https://www.takealot.com/cart'

    def start_requests(self):
        """Request dispatcher."""
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'wait': 0.75, 'lua_source': COOKIE_SCRIPT,},)


    def parse(self, response):
        """Parse the product page.

        Add the product to cart using the add-form on the page.
        Then redirect to the cart page.
        """
        prod_id = response.meta.get('prod_id')
        cookies = response.data['cookies']
        if prod_id is None:
            # get product id
            prod_id = response.xpath('//input[@name="idProduct"]/@value').extract_first()

            try:
                # if product is available, add it to cart
                request = SplashFormRequest.from_response(response, formcss='form.add-form',
                                                          callback=self.parse, endpoint='execute',
                                                          cookies=cookies,
                                                          args={'lua_source': COOKIE_SCRIPT,})
                request.meta['prod_id'] = prod_id
                yield request
                self.logger.info("Prod id found <{0}>".format(prod_id))
            except ValueError:
                # product no longer available, as the product id cannot be found on page
                self.logger.info("No product found at url: <{}>".format(response.url))
        else:
            # product added to cart, redirect to the cart url
            request = SplashRequest(self.cart_url, self.parse_cart, endpoint='execute',
                                    cookies=cookies, dont_filter=True,
                                    args={'wait': 0.75, 'lua_source': COOKIE_SCRIPT},)
            request.meta['prod_id'] = prod_id
            yield request
            self.logger.info("Prod id <{0}> added to cart.".format(prod_id))

    def parse_cart(self, response):
        """Parse the cart page.

        First submit the cart-form with a value of 9999 to get
        the updated quantity of the product stocks.
        Then scrape the updated value of the product.
        """
        cookies = response.data['cookies']
        updated = response.meta.get('updated')
        prod_id = response.meta.get('prod_id')

        if not updated:
            qty_key = 'qty[{}]'.format(prod_id)
            data = {
                qty_key: '9999',
            }


            request = SplashFormRequest.from_response(response, formid='cart-form', formdata=data,
                                                      callback=self.parse_cart, endpoint='execute',
                                                      cookies=cookies, dont_filter=True,
                                                      args={'lua_source': COOKIE_SCRIPT,})
            request.meta['prod_id'] = prod_id
            request.meta['updated'] = True

            yield request
            self.logger.info("Prod id {0} update form sent.".format(prod_id))
        else:
            stock_remaining = response.xpath('//input[@id="{}"]/@value'
                                             .format(prod_id)).extract_first()

            self.logger.info("Prod id {0} updated quantity scraped.".format(prod_id))

            request = scrapy.Request(API_LOOKUP_URL.format(prod_id=prod_id),
                                     callback=self.parse_item)
            request.meta['stock_remaining'] = stock_remaining

            yield request


    def parse_item(self, response):
        """Overriden parse_item method.

        Override the base implementation to replace the original stock_remaining
        field - that is returned by the server - by the cart update value.
        """
        item = self.load_item(response)
        item['stock_remaining'] = response.meta.get('stock_remaining')
        yield item
