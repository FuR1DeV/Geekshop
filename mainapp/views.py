from django.shortcuts import render
import datetime

from mainapp.models import Product, ProductCategory

# функции = контроллеры = вьюхи


def index(request):
    context = {'title': 'geekshop',
               'date': datetime.datetime.now()}
    return render(request, 'mainapp/index.html', context)


def products(request, category_id=None):
    context = {'title': 'Geekshop - Каталог', 'categories': ProductCategory.objects.all()}
    if category_id:
        products = Product.objects.filter(category_id=category_id)
        context.update({'products': products})
    else:
        context.update({'products': Product.objects.all()})
    return render(request, 'mainapp/products.html', context)
