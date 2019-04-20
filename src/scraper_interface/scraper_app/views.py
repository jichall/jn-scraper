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
        # TODO: Improve error handling over this piece of code
        return HttpResponse('There\'s no such product in the database')
    else:
        context = {'products': item}
        return render(request, 'product.html', context)
