# coding: utf-8

from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

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
