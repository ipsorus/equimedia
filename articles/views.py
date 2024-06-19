from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from articles.forms import ArticlePostCreateForm, ArticlePostUpdateForm
from articles.models import Article
from el_pagination.decorators import page_template
from services.mixins import AuthorRequiredMixin


@page_template('articles/articles-list-page.html')
def articles_section(request,
                     template='articles/articles-list.html',
                     extra_context=None):
    context = {
        'articles': Article.objects.filter(is_published=True),
        'title': 'Статьи'
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    articles = Article.objects.filter(is_published=True).exclude(pk=article.id)[:10]

    try:
        previous_post = article.get_previous_by_time_create()
    except Article.DoesNotExist:
        previous_post = None

    try:
        next_post = article.get_next_by_time_create()
    except Article.DoesNotExist:
        next_post = None

    data = {
        'title': article.title,
        'item': article,
        'articles': articles,
        'prev': previous_post,
        'next': next_post
    }

    return render(request, 'articles/article-single.html', data)


class ArticlePostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Article
    template_name = 'articles/article-single-create.html'
    form_class = ArticlePostCreateForm
    login_url = 'articles_list_url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление статьи на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class ArticlePostUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Article
    template_name = 'articles/article-single-update.html'
    context_object_name = 'post'
    form_class = ArticlePostUpdateForm
    login_url = 'articles_list_url'
    success_message = 'Материал был успешно обновлен'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление записи: {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class ArticlePostDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Article
    success_url = reverse_lazy('articles_list_url')
    context_object_name = 'post'
    template_name = 'articles/article-single-delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление записи: {self.object.title}'
        return context
