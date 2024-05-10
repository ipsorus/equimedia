from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

from articles.models import Article
from portal.models import NewsPost


def index(request):
    news = NewsPost.objects.filter(is_published=True)[:5]
    main_articles = Article.objects.filter(is_published=True)[:2]
    articles = Article.objects.filter(is_published=True)[2:6]
    data = {'news': news,
            'main_articles': main_articles,
            'articles': articles,
            }
    return render(request, 'portal/index.html', data)


def news_section(request):
    news = NewsPost.objects.filter(is_published=True)
    data = {'title': news.title,
            'news': news,
            }
    return render(request, 'portal/templates/portal/includes/news4-4.html', data)


def news_detail(request, news_slug):
    single_news = get_object_or_404(NewsPost, slug=news_slug)
    news = NewsPost.objects.filter(is_published=True).exclude(pk=single_news.id)[:10]

    data = {'title': single_news.title,
            'item': single_news,
            'news': news
            }

    return render(request, 'portal/news-single.html', data)


def categories(request, cat_id):
    return HttpResponse("<h1>Статьи по категориям</h1>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
