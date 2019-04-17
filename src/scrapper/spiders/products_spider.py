import scrapy

class ProductsSpider(scrapy.Spider):
    name = "products"
    start_urls = [
        'https://nerdstore.com.br/categoria/especiais/game-of-thrones/'
    ]

    def parse(self, response):
        for product in response.css('li.product'):
            yield {
                # The title is not encoded in UTF-8 as well.
                'title': product.css('h2.woocommerce-loop-product__title::text').get(),
                'img': product.xpath('.//img/@src').getall(),
                'price': product.css('span.price > span::text').get()

            }
