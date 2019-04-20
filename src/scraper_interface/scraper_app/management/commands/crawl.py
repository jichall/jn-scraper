from sys import path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from django.core.management.base import BaseCommand

path.append('../../../scraper/spiders/')
from scraper.spiders import products_spider


class Command(BaseCommand):
    help = "Initialize the scraper spider"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        process.crawl(products_spider.ProductsSpider)
        process.start()
