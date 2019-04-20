# -*- coding: utf-8 -*-

from scrapy_djangoitem import DjangoItem
from scraper_app.models import ProductItem, Image


class Product(DjangoItem):
    django_model = ProductItem

class Image(DjangoItem):
    django_model = Image
