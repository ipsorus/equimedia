from datetime import date
from itertools import chain
from operator import attrgetter

from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView

from articles.models import Article
from blog.models import BlogPost
from event.models import Event, Stage, Tournament
from news.models import NewsPost
from portal.forms import FeedbackCreateForm
from portal.models import Feedback
from services.email import send_contact_email_message
from services.utils import get_client_ip
from slider.models import Slider
from testimonial.models import Testimonial


def index(request):
    news = NewsPost.objects.filter(is_published=True)[:5]
    main_articles = Article.objects.filter(is_published=True)[:2]
    articles = Article.objects.filter(is_published=True)[2:6]
    testimonials = Testimonial.objects.filter(is_published=True)[:5]
    slider = Slider.objects.filter(is_published=True)[:5]
    blogs = BlogPost.objects.filter(is_published=True)[:6]

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
            'events': events,
            'blogs': blogs,
            'title': 'КСК Виват-Россия!'
            }
    return render(request, 'portal/index.html', data)


def page_not_found(request, exception):
    return HttpResponseNotFound("<h1>Страница не найдена</h1>")


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    template_name = 'portal/feedback.html'
    extra_context = {'title': 'Контакты'}
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user
            send_contact_email_message(feedback.subject, feedback.email, feedback.content, feedback.ip_address, feedback.user_id)
        return super().form_valid(form)
