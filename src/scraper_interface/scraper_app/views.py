# coding: utf-8

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.core import serializers

from .models import ProductItem


def index(request):
    """Returns the front page"""
    context = {}
    return render(request, 'index.html', context)


def products(request):
    """Returns a list of all scraped products"""
    context = {'products': ProductItem.objects.all()}
    return render(request, 'products.html', context)


def product(request, product_id):
    """Returns a single product"""
    try:
        item = ProductItem.objects.get(pk=product_id)
    except(Exception):
        context = {'error': 'O item ' + str(product_id) + ' não foi encontrado.'}
        return render(request, 'index.html', context)
    else:
        context = {'product': item}
        return render(request, 'product.html', context)


def json(request):
    products = ProductItem.objects.all()
    objects = []

    for product in products:
        product_dict = {}
        product_dict['title'] = product.name
        product_dict['img(s)'] = [str(img) for img in product.image_set.all()]
        product_dict['price'] = product.price
        objects.append(product_dict)

    context = {'objects': objects}
    return render(request, 'json.html', context)
