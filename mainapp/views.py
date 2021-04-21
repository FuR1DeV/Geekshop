from django.shortcuts import render

# Lesson_1
# Create your views here.
# функции = контроллеры = вьюхи


def index(request):
    return render(request, 'mainapp/index.html')


def products(request):
    return render(request, 'mainapp/products.html')