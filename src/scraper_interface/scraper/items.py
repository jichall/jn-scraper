# -*- coding: utf-8 -*-

from scrapy_djangoitem import DjangoItem
from scraper_app.models import ProductItem


class Product(DjangoItem):
    django_model = ProductItem
