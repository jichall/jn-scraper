# -*- coding: utf-8 -*-

import scrapy
from scraper.items import ProductItem


class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://nerdstore.com.br/categoria/especiais/game-of-thrones/'
    ]

    def parse(self, response):
        for product in response.css('li.product'):
            product = ProductItem()
            # The title is not encoded in UTF-8.
            product.name = product.css('h2.woocommerce-loop-product__title::text').get()
            product.price = product.css('span.price > span::text').get()

            images = product.xpath('.//img/@src').getall()
            for image in images:
                product.image_set.create(image)

            yield product


    """
    To generate a JSON of the scraped products
    def parse(self, response):
        for product in response.css('li.product'):
            product = {}
            # The title is not encoded in UTF-8.
            product['title'] = product.css('h2.woocommerce-loop-product__title::text').get()
            product.['price'] = product.css('span.price > span::text').get()
            product['images'] = product.xpath('.//img/@src').getall()
            yield product
    """
