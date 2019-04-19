from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render

from .models import *

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
    name = "<b>%s</b>" % product_id
    return HttpResponse(name)
