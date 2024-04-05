from django.http import HttpResponse


def index(request):
    return HttpResponse("Страница приложения")


def categories(request):
    return HttpResponse("<h1>Статьи по категориям</h1>")
