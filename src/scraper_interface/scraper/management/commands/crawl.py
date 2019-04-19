from django.core.management.base import BaseCommand

from scraper.spiders import ProductSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class Command(BaseCommand):
    help = "Initialize the scraper spider"

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())

        process.crawl(ProductSpider)
        process.start()
