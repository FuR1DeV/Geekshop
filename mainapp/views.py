from django.shortcuts import render
import datetime

from mainapp.models import Product, ProductCategory

# функции = контроллеры = вьюхи


def index(request):
    context = {'title': 'geekshop',
               'date': datetime.datetime.now()}
    return render(request, 'mainapp/index.html', context)


def products(request):
    context = {'title': 'Geekshop - Каталог',
               'products': Product.objects.all(),
               'categories': ProductCategory.objects.all(),
               }
    return render(request, 'mainapp/products.html', context)
