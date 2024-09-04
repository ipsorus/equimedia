from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView

from articles.forms import ArticlePostCreateForm, ArticlePostUpdateForm, CommentCreateForm
from articles.mixins import ViewCountMixin
from articles.models import Article, Comment, Rating
from el_pagination.decorators import page_template
from services.mixins import AuthorRequiredMixin
from services.utils import get_client_ip
from slider.models import Slider


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


class ArticleDetailView(ViewCountMixin, DetailView):
    model = Article
    template_name = 'articles/article-single.html'
    context_object_name = 'post'

    def get_other_articles(self, obj):
        other_news = Article.objects.filter(is_published=True).exclude(pk=obj.id)[:10]
        return other_news

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['other_articles'] = self.get_other_articles(self.object)
        context['form'] = CommentCreateForm

        try:
            previous_post = self.object.get_previous_by_time_create()
        except self.model.DoesNotExist:
            previous_post = None

        try:
            next_post = self.object.get_next_by_time_create()
        except self.model.DoesNotExist:
            next_post = None

        context['prev'] = previous_post
        context['next'] = next_post

        return context


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
        with transaction.atomic():
            form.instance.author = self.request.user
            self.object = form.save()

            if self.object.slider:
                slide = Slider.objects.create(title=self.object.title,
                                              poster=self.object.image,
                                              is_published=True,
                                              url=self.object.get_absolute_url())
                slide.save()
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


class ArticlePostDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Article
    success_url = reverse_lazy('articles_list_url')
    context_object_name = 'post'
    template_name = 'articles/article-single-delete.html'
    success_message = 'Статья была успешно удалена'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление записи: {self.object.title}'
        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentCreateForm

    def is_ajax(self):
        return self.request.headers.get('X-Requested-With') == 'XMLHttpRequest'

    def form_invalid(self, form):
        if self.is_ajax():
            return JsonResponse({'error': form.errors}, status=400)
        return super().form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post_id = self.kwargs.get('pk')
        comment.author = self.request.user
        comment.parent_id = form.cleaned_data.get('parent')
        comment.parent_author = form.cleaned_data.get('parent')
        comment.parent_content = form.cleaned_data.get('parent')
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username,
                'parent_id': comment.parent_id,
                'parent_author': comment.parent.author.username if comment.parent else None,
                'parent_content': comment.parent.content if comment.parent else None,
                'time_create': comment.time_create.strftime('%d %b %Y %H:%M'),
                'avatar': comment.author.profile.avatar.url,
                'content': comment.content,
                'get_absolute_url': comment.author.profile.get_absolute_url()
            }, status=200)

        return redirect(comment.post.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментариев'}, status=400)


class RatingCreateView(View):
    model = Rating

    def post(self, request, *args, **kwargs):
        post_id = request.POST.get('post_id')
        value = int(request.POST.get('value'))
        ip_address = get_client_ip(request)
        user = request.user if request.user.is_authenticated else None

        rating, created = self.model.objects.get_or_create(
            post_id=post_id,
            ip_address=ip_address,
            defaults={'value': value, 'user': user},
        )

        if not created:
            if rating.value == value:
                rating.delete()
                return JsonResponse({'status': 'deleted', 'rating_sum': rating.post.get_sum_rating()})
            else:
                rating.value = value
                rating.user = user
                rating.save()
                return JsonResponse({'status': 'updated', 'rating_sum': rating.post.get_sum_rating()})
        return JsonResponse({'status': 'created', 'rating_sum': rating.post.get_sum_rating()})
