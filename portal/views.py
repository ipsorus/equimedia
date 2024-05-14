from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from articles.models import Article
from news.models import NewsPost
from slider.models import Slider
from testimonial.models import Testimonial


def index(request):
    news = NewsPost.objects.filter(is_published=True)[:5]
    main_articles = Article.objects.filter(is_published=True)[:2]
    articles = Article.objects.filter(is_published=True)[2:6]
    testimonials = Testimonial.objects.filter(is_published=True)[:5]
    slider = Slider.objects.filter(is_published=True)[:5]
    data = {'news': news,
            'main_articles': main_articles,
            'articles': articles,
            'testimonials': testimonials,
            'slider': slider,
            }
    return render(request, 'portal/index.html', data)


def categories(request, cat_id):
    return HttpResponse("<h1>Статьи по категориям</h1>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
