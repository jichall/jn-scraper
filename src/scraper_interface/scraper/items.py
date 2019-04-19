# -*- coding: utf-8 -*-

import scrapy

from scrapy_djangoitem import DjangoItem
from scraper_app.models import ProductItem

class Product():
    django_model = ProductItem
