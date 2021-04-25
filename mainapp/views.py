from django.shortcuts import render
import datetime


# функции = контроллеры = вьюхи


def index(request):
    context = {'title': 'geekshop',
               'date': datetime.datetime.now()}
    return render(request, 'mainapp/index.html', context)


def products(request):
    context = {'title': 'Geekshop - Каталог',
               'products': [
                   {'name': 'худи черного цвета с монограммами adidas Originals',
                    'price': 6090.00,
                    'description': 'мягкая ткань для свитшотов. Стиль и комфорт – это образ жизни.'},
                   {'name': 'Синяя куртка The North Face',
                    'price': 23725.00,
                    'description': 'гладкая ткань. Водонепроницаемое покрытие. Легкий и теплый пуховый наполнитель. '},
                   {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN',
                    'price': 3390.00,
                    'description': 'материал с плюшевой текстурой. Удобный и мягкий.'},
                   {'name': 'Черный рюкзак Nike Heritage',
                    'price': 2340.00,
                    'description': 'плотная ткань. Легкий материал.'},
                   {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
                    'price': 13590.00,
                    'description': 'гладкий кожаный верх. Натуральный материал.'},
                   {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
                    'price': 2890.00,
                    'description': 'легкая эластичная ткань сирсакер Фактурная ткань.'}]
               }

    return render(request, 'mainapp/products.html', context)
