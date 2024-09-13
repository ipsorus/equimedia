from datetime import date
from itertools import chain
from operator import attrgetter

from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from articles.models import Article
from blog.models import BlogPost
from event.models import Event, Stage, Tournament
from news.models import NewsPost
from podcast.models import Video
from portal.forms import FeedbackCreateForm
from portal.models import Feedback, SiteSettings
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
    blogs = BlogPost.objects.all()[:6]
    videos = Video.objects.all()[:5]

    current_date = date.today()

    current_events = Event.objects.filter(is_published=True, date_start__lte=current_date, date_end__gte=current_date)
    stages = Stage.objects.filter(is_published=True, date_start__lte=current_date, date_end__gte=current_date)
    tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True, date_start__lte=current_date,
                                            date_end__gte=current_date)
    result_list = sorted(list(chain(current_events, stages, tournaments)), key=attrgetter('date_start'))[:5]

    future_stages = Stage.objects.filter(is_published=True, date_start__gt=current_date)
    future_tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True, date_start__gt=current_date)
    future_events = Event.objects.filter(is_published=True, date_start__gt=current_date)
    future_result_list = sorted(list(chain(future_stages, future_tournaments, future_events)),
                                key=attrgetter('date_start'))[:5]

    past_stages = Stage.objects.filter(is_published=True, date_start__lt=current_date)
    past_tournaments = Tournament.objects.filter(is_published=True, stages__isnull=True, date_start__lt=current_date)
    past_events = Event.objects.filter(is_published=True, date_start__lt=current_date)
    past_result_list = sorted(list(chain(past_stages, past_tournaments, past_events)), key=attrgetter('date_start'))[:5]

    data = {
        'news': news,
        'main_articles': main_articles,
        'articles': articles,
        'testimonials': testimonials,
        'slider': slider,
        'current_events': result_list,
        'future_events': future_result_list,
        'past_events': past_result_list,
        'blogs': blogs,
        'videos': videos,
        'title': SiteSettings.objects.defer('title').get().title
    }
    return render(request, 'portal/index.html', data)


def redirect_to_home(request):
    return redirect('http://127.0.0.1:8000/')


def tr_handler404(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request=request, template_name='portal/errors/404.html', status=404, context={
        'title': 'Страница не найдена: 404',
        'error_message': 'К сожалению, эта страница не найдена или она перемещена',
    })


def tr_handler500(request):
    """
    Обработка ошибки 500
    """
    return render(request=request, template_name='portal/errors/500.html', status=500, context={
        'title': 'Ошибка сервера: 500',
        'error_message': 'Внутренняя ошибка сайта, вернитесь на главную страницу, отчет об ошибке мы направим администрации сайта',
    })


def tr_handler403(request, exception):
    """
    Обработка ошибки 403
    """
    return render(request=request, template_name='portal/errors/403.html', status=403, context={
        'title': 'Ошибка доступа: 403',
        'error_message': 'Доступ к этой странице ограничен',
    })


class FeedbackCreateView(SuccessMessageMixin, CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    success_message = 'Ваше письмо успешно отправлено администрации сайта'
    template_name = 'portal/feedback.html'
    extra_context = {'title': 'Контакты'}
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                feedback.user = self.request.user
            send_contact_email_message(feedback.subject, feedback.email, feedback.content, feedback.ip_address,
                                       feedback.user_id)
        return super().form_valid(form)


def about_us(request):
    testimonials = Testimonial.objects.filter(is_published=True)[:5]

    data = {
        'title': "О нас",
        'testimonials': testimonials,
    }
    return render(request, 'portal/about_us.html', data)
