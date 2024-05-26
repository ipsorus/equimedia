from datetime import date
from itertools import chain
from operator import attrgetter

from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404

from articles.models import Article
from event.models import Event, Stage, Tournament
from news.models import NewsPost
from slider.models import Slider
from testimonial.models import Testimonial


def index(request):
    news = NewsPost.objects.filter(is_published=True)[:5]
    main_articles = Article.objects.filter(is_published=True)[:2]
    articles = Article.objects.filter(is_published=True)[2:6]
    testimonials = Testimonial.objects.filter(is_published=True)[:5]
    slider = Slider.objects.filter(is_published=True)[:5]

    current_date = date.today()
    events = Event.objects.filter(is_published=True, date_start__gt=current_date)

    current_events = Event.objects.filter(is_published=True, date_start__lte=current_date, date_end__gte=current_date)
    stages = Stage.objects.filter(is_published=True, date_start__lte=current_date, date_end__gte=current_date)
    tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True,date_start__lte=current_date, date_end__gte=current_date)
    result_list = sorted(list(chain(current_events, stages, tournaments)), key=attrgetter('date_start'))

    future_stages = Stage.objects.filter(is_published=True, date_start__gt=current_date)
    future_tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True, date_start__gt=current_date)
    future_result_list = sorted(list(chain(future_stages, future_tournaments)), key=attrgetter('date_start'))

    data = {'news': news,
            'main_articles': main_articles,
            'articles': articles,
            'testimonials': testimonials,
            'slider': slider,
            'current_contests': result_list,
            'future_contests': future_result_list,
            'events': events
            }
    return render(request, 'portal/index.html', data)


def categories(request, cat_id):
    return HttpResponse("<h1>Статьи по категориям</h1>")


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")
