# -*- coding: utf-8 -*-

from sys import path
import scrapy
from scraper.items import Product, Image

path.append('../../scraper_app/')
from scraper_app.models import ProductItem
from scraper_app.models import Image as ImageItem


class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://nerdstore.com.br/categoria/especiais/game-of-thrones/'
    ]

    def parse(self, response):
        # Delete all the objects before parsing the page because I don't want to
        # fill repeated data into the database
        ProductItem.objects.all().delete()
        ImageItem.objects.all().delete()
        # Dictionary containing all the images related to a specific product
        images = {}

        for product in response.css('li.product'):
            p = Product()

            # The title is not encoded in UTF-8.
            p['name'] = product.css('h2.woocommerce-loop-product__title::text').get()
            p['price'] = product.css('span.price > span::text').get()
            images[p['name']] = product.xpath('.//img/@src').getall()

            yield p

        for p in ProductItem.objects.all():
            for img in images[p.name]:
                i = Image()
                i['item'] = p
                i['src'] = img
                yield i


    """
    To generate a JSON of the scraped products you can use the crawler directly
    using also the parse2 function.

    $ scrapy runspider products_spider.py -o products.json

    def parse2(self, response):
        for product in response.css('li.product'):
            product = {}
            # The title is not encoded in UTF-8.
            product['title'] = product.css('h2.woocommerce-loop-product__title::text').get()
            product.['price'] = product.css('span.price > span::text').get()
            product['images'] = product.xpath('.//img/@src').getall()
            yield product
    """
