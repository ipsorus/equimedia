from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from portal.models import News


def index(request):
    news = News.objects.filter(is_published=True)[:5]
    data = {'news': news,
            }
    return render(request, 'portal/index.html', data)


def news_section(request):
    news = News.objects.filter(is_published=True)
    data = {'title': news.title,
            'news': news,
            }
    return render(request, 'portal/templates/portal/includes/news4-4.html', data)


def news_detail(request, news_slug):
    single_news = get_object_or_404(News, slug=news_slug)
    news = News.objects.filter(is_published=True)[:10]

    data = {'title': single_news.title,
            'item': single_news,
            'news': news
            }

    return render(request, 'portal/news-single.html', data)



def categories(request, cat_id):
    return HttpResponse("<h1>Статьи по категориям</h1>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
