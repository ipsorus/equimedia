from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from news.forms import NewsPostUpdateForm, NewsPostCreateForm
from news.models import NewsPost
from el_pagination.decorators import page_template
from services.mixins import AuthorRequiredMixin


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@page_template('news/news-list-page.html')
def news_section(request,
                 template='news/news-list.html',
                 extra_context=None):
    context = {
        'news': NewsPost.objects.filter(is_published=True),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def news_detail(request, news_id):
    single_news = get_object_or_404(NewsPost, pk=news_id)
    news = NewsPost.objects.filter(is_published=True).exclude(pk=single_news.id)[:10]

    try:
        previous_post = single_news.get_previous_by_time_create()
    except NewsPost.DoesNotExist:
        previous_post = None

    try:
        next_post = single_news.get_next_by_time_create()
    except NewsPost.DoesNotExist:
        next_post = None

    data = {'title': single_news.title,
            'item': single_news,
            'news': news,
            'prev': previous_post,
            'next': next_post
            }

    return render(request, 'news/news-single.html', data)


class NewsPostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = NewsPost
    template_name = 'news/news-single-create.html'
    form_class = NewsPostCreateForm
    login_url = 'news_list_url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление новости на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class NewsPostUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = NewsPost
    template_name = 'news/news-single-update.html'
    context_object_name = 'post'
    form_class = NewsPostUpdateForm
    login_url = 'news_list_url'
    success_message = 'Материал был успешно обновлен'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление записи: {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class NewsPostDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = NewsPost
    success_url = reverse_lazy('news_list_url')
    context_object_name = 'post'
    template_name = 'news/news-single-delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление записи: {self.object.title}'
        return context
