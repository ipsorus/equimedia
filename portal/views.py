from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.template.loader import render_to_string


def index(request):
    return render(request, 'portal/index.html')


def categories(request, cat_id):
    return HttpResponse("<h1>Статьи по категориям</h1>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
