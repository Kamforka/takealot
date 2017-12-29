
# -*- coding: utf-8 -*-
"""Takealot sunglass item scraper."""
import scrapy

from scrapy_splash import SplashRequest, SplashFormRequest

from takealot.spiders import SpiderBase

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
        'https://fashion.takealot.com/fashion-bad-boy-army-sunglasses-in-black/PLID40758214',
        'https://fashion.takealot.com/fashion-bad-boy-no-limit-sunglasses-in-grey-and-red/PLID40758228',
        'https://fashion.takealot.com/fashion-bad-boy-victory-sunglasses-in-gun/PLID40758222',
        'https://fashion.takealot.com/fashion-bad-boy-no-limit-sunglasses-in-white-and-red/PLID40758229',
        'https://fashion.takealot.com/fashion-lakota-inspirations-rose-gold-aviator-retro-sunglasses/PLID45068411',
        'https://fashion.takealot.com/fashion-priv-revaux-the-conquistador-polarized-sunglasses-black-white/PLID46853363',
        'https://fashion.takealot.com/fashion-priv-revaux-the-cougar-sunglasses-tortoise/PLID46853366',
        'https://fashion.takealot.com/fashion-priv-revaux-the-dutchess-sunglasses-gold-grey/PLID46853369',
        'https://fashion.takealot.com/fashion-priv-revaux-the-entrepreneur-sunglasses-red/PLID46853373',
        'https://fashion.takealot.com/fashion-priv-revaux-the-explorer-polarized-sunglasses-tortoise/PLID46853380',
        'https://fashion.takealot.com/fashion-priv-revaux-the-feminist-sunglasses-black-gold/PLID46853381',
        'https://fashion.takealot.com/fashion-priv-revaux-the-godfather-polarized-sunglasses-black/PLID46853383',
        'https://fashion.takealot.com/fashion-priv-revaux-the-heartbreaker-polarized-sunglasses-brown/PLID46853386',
        'https://fashion.takealot.com/fashion-priv-revaux-the-heroine-polarized-sunglasses-tortoise/PLID46853389',
        'https://fashion.takealot.com/fashion-priv-revaux-the-jetsetter-polarized-sunglasses-gold/PLID46853393',
        'https://fashion.takealot.com/fashion-priv-revaux-the-judge-polarized-sunglasses-flower/PLID46853396',
        'https://fashion.takealot.com/fashion-priv-revaux-the-king-polarized-sunglasses-black/PLID46853398',
        'https://fashion.takealot.com/fashion-priv-revaux-the-marquise-polarized-sunglasses-silver/PLID46853408',
        'https://fashion.takealot.com/fashion-priv-revaux-the-milf-sunglasses-tortoise/PLID46853411',
        'https://fashion.takealot.com/fashion-priv-revaux-the-mogul-polarized-sunglasses-purple/PLID46853413',
        'https://fashion.takealot.com/fashion-priv-revaux-the-warrior-sunglasses-black/PLID46853443',
        'https://fashion.takealot.com/fashion-priv-revaux-the-underdog-square-polarized-sunglasses-tortoise/PLID46853442',
        'https://fashion.takealot.com/fashion-priv-revaux-the-sweetheart-polarized-sunglasses-woodgrain/PLID46853439',
        'https://fashion.takealot.com/fashion-priv-revaux-the-sweetheart-polarized-sunglasses-pink/PLID46853438',
        'https://fashion.takealot.com/fashion-priv-revaux-the-supermodel-polarized-sunglasses-flower/PLID46853436',
        'https://fashion.takealot.com/fashion-priv-revaux-the-socialite-sunglasses-tortoise/PLID46853434',
        'https://fashion.takealot.com/fashion-priv-revaux-the-shark-polarized-sunglasses-woodgrain/PLID46853431',
        'https://fashion.takealot.com/fashion-priv-revaux-the-scholar-sunglasses-tortoise/PLID46853429',
        'https://fashion.takealot.com/fashion-priv-revaux-the-rockstar-sunglasses-brown/PLID46853428',
        'https://fashion.takealot.com/fashion-priv-revaux-the-queen-polarized-sunglasses-black/PLID46853424',
        'https://fashion.takealot.com/fashion-priv-revaux-the-nasty-woman-polarized-sunglasses-black-silver/PLID46853416',
        'https://fashion.takealot.com/fashion-priv-revaux-the-milf-sunglasses-tortoise/PLID46853411',
        'https://fashion.takealot.com/fashion-priv-revaux-the-godfather-polarized-sunglasses-off-white/PLID46853384',
        'https://fashion.takealot.com/fashion-lentes-marcos-avenida-de-la-paz-polarised-black-cat-eye-sunglass/PLID45086316',
        'https://fashion.takealot.com/fashion-lentes-marcos-anton-martin-uv400-black-silver-pilot-sunglasses/PLID45086305',
        'https://fashion.takealot.com/fashion-lentes-marcos-avatcha-uv400-gun-pilot-sunglasses/PLID45086306',
        'https://fashion.takealot.com/fashion-lentes-marcos-legazpi-uv400-navy-white-wayfarer-sunglasses/PLID45086307',
        'https://fashion.takealot.com/fashion-lentes-marcos-delicias-uv400-silver-round-sunglasses/PLID45086308',
        'https://fashion.takealot.com/fashion-lentes-marcos-delicias-uv400-amber-black-round-sunglasses/PLID45086309',
        'https://fashion.takealot.com/fashion-lentes-marcos-conde-de-casal-uv400-amber-black-cat-eye-sunglasse/PLID45086310',
        'https://fashion.takealot.com/fashion-lentes-marcos-mendez-alvaro-polarised-tortoise-shell-black-gold/PLID45086311',
        'https://fashion.takealot.com/fashion-lentes-marcos-o-donnell-polarised-amber-gold-cat-eye-sunglasses/PLID45086312',
        'https://fashion.takealot.com/fashion-lentes-marcos-la-elipa-uv400-mirrored-club-master-sunglasses/PLID45086315',
        'https://fashion.takealot.com/fashion-lentes-marcos-piramides-polarised-amber-grey-cat-eye-sunglasses/PLID45086318',
        'https://fashion.takealot.com/fashion-lentes-marcos-gran-via-polarised-black-flat-top-mirrored-sunglas/PLID45086321',
        'https://fashion.takealot.com/fashion-lentes-marcos-la-gavia-uv400-black-rectangle-sunglasses/PLID45086324',
        'https://fashion.takealot.com/fashion-lentes-marcos-pinar-de-campoverde-amber-tortoise-shell-wayfarer/PLID45086325',
        'https://fashion.takealot.com/fashion-lentes-marcos-carpetana-polarised-mirrored-cat-eye-sunglasses/PLID45086327',
        'https://fashion.takealot.com/fashion-lentes-marcos-rios-rosas-polarised-black-oversized-sunglasses/PLID42070594',
        'https://fashion.takealot.com/fashion-lentes-marcos-el-carmen-polarised-white-green-sports-sunglasses/PLID42070602',
        'https://fashion.takealot.com/fashion-lentes-marcos-menendez-pelayo-polarised-silver-grey-pilot-sungla/PLID42070613',
        'https://fashion.takealot.com/fashion-lentes-marcos-tirso-de-molina-polarised-black-wrap-sunglasses/PLID42070615',
        'https://fashion.takealot.com/fashion-lentes-marcos-alvarado-uv400-black-shield-sunglasses/PLID42070624',
        'https://fashion.takealot.com/fashion-lentes-marcos-atocha-polarised-silver-rectangle-sunglasses/PLID42070675',
        'https://fashion.takealot.com/fashion-lentes-marcos-vista-alegra-uv400-black-wayfarer-sunglasses/PLID42070691',
        'https://fashion.takealot.com/fashion-ray-ban-wayfarer-rb2140-902-50/PLID44815106',
        'https://fashion.takealot.com/fashion-ray-ban-new-wayfarer-rb2132-902-58-55/PLID44815120',
        'https://fashion.takealot.com/fashion-ray-ban-aviator-rb3025-001-57-58/PLID44815124',
        'https://fashion.takealot.com/fashion-oakley-trillbe-x-oo9340-02-sunglasses-polished-black-with-ruby-i/PLID47901486',
        'https://fashion.takealot.com/fashion-oakley-turbine-rotor-prizm-daily-polarized-matte-black/PLID44815166',
        'https://fashion.takealot.com/fashion-oakley-turbine-oo9263-36-sunglasses-sapphire-fade-with-prizm-sap/PLID47901428',
        'https://fashion.takealot.com/fashion-slaughter-fox-ladies-eyewear-manhattan-limited-edition-c1-flamin/PLID44898637',
        'https://fashion.takealot.com/fashion-slaughter-fox-ladies-eyewear-brooklyn-c2-ocean-blue/PLID44898645',
        'https://fashion.takealot.com/fashion-slaughter-fox-eyewear-yorkville-c1-gunmetal-silver/PLID44898647',
        'https://fashion.takealot.com/fashion-slaughter-fox-ladies-eyewear-upper-east-side-c4-marbled-cinnamon/PLID44898653',
        'https://fashion.takealot.com/fashion-slaughter-fox-eyewear-hell-s-kitchen-c2-coastal-blue/PLID44898655',
        'https://fashion.takealot.com/fashion-polaroid-eyewear-sunglasses-unisex-pld6012-n-j5g-jb-3/PLID44797227',
        'https://fashion.takealot.com/fashion-vonzipper-howl-sunglasses-black-buff-crystal-grey/PLID46623716',
        'https://fashion.takealot.com/fashion-vonzipper-queenie-sunglasses-black-gloss-grey-polipolar/PLID46623728',
        'https://fashion.takealot.com/fashion-vonzipper-donmega-sunglasses-black-tortoise-bronze/PLID46623722',
        'https://fashion.takealot.com/fashion-vonzipper-wooster-sunglasses-black-tortoise-vintage-grey/PLID46623724',
        'https://fashion.takealot.com/fashion-vonzipper-castaway-sunglasses-black-gloss-grey-polipolar/PLID46623727',
        'https://fashion.takealot.com/fashion-salice-014-rw-black-black-sunglasses/PLID41200783',
        'https://sport.takealot.com/sport-salice-012-rw-white-red-sunglasses/PLID41200774',
        'https://sport.takealot.com/sport-salice-006-rw-white-blue-sunglasses/PLID41200786',
        'https://sport.takealot.com/sport-salice-006-photochromatic-black-sunglasses/PLID41200764',
        'https://fashion.takealot.com/fashion-salice-3047-black-red-sunglasses/PLID41200785',
        'https://sport.takealot.com/sport-salice-012-photochromatic-black-sunglasses/PLID41200778',
        'https://fashion.takealot.com/fashion-polarized-glider-casanova-sunglasses-rubber-black/PLID41402432',
        'https://fashion.takealot.com/fashion-polarized-glider-bella-sunglasses-tortoise/PLID41402429',
        'https://fashion.takealot.com/fashion-glider-cutter-sunglasses-matt-brown/PLID41531505',
        'https://fashion.takealot.com/fashion-polarized-glider-amoroso-sunglasses-black/PLID41402430',
        'https://fashion.takealot.com/fashion-polarized-glider-trooper-sunglasses-gun/PLID41402419',
        'https://fashion.takealot.com/fashion-polarized-glider-bella-sunglasses-black/PLID41402425',
        'https://fashion.takealot.com/fashion-polarized-glider-casanovasunglasses-shiny-black/PLID41402426',
        'https://fashion.takealot.com/fashion-polarized-glider-trooper-sunglasses-gold/PLID41402415',
        'https://fashion.takealot.com/fashion-polarized-glider-amoroso-sunglasses-grey-cateye/PLID41402433',
        'https://fashion.takealot.com/fashion-polarized-glider-viper-sunglasses-silver/PLID41402412',
    ]
    cart_url = 'https://www.takealot.com/cart'

    def start_requests(self):
        """Request dispatchers."""
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='render.html',
                                args={'wait': 0.75})

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
            try:
                yield FormRequest.from_response(response, formcss='form.add-form',
                                                meta={'prod_id': prod_id})
            except ValueError:
                self.logger.info("No product found at url: <{}>".format(response.url))

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
