from django.shortcuts import render


def index(request):
    return render(request, 'adminapp/admin.html')

# CRUD - Create Read Update Delete