import random
from itertools import chain

from django.db.models import Q
from django.http import JsonResponse
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from el_pagination.views import AjaxListView
from services.mixins import AuthorRequiredMixin
from services.utils import get_client_ip
from .models import Comment, BlogPost, Rating
from .forms import CommentCreateForm, BlogPostUpdateForm, BlogPostCreateForm


class BlogPostListView(AjaxListView):
    context_object_name = "posts"
    template_name = "blog/posts_list.html"
    page_template = 'blog/posts-list-page.html'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Блоги'
        context['subtitle'] = 'Истории наших пользователей о лошадях и не только...'
        context['posts'] = self.get_queryset()

        return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = model.objects.detail()

    def get_similar_articles(self, obj):
        article_title = obj.title.split()
        similar_articles_list = list()
        for word in article_title:
            if len(word) > 4:
                similar_articles = BlogPost.objects.filter(Q(title__icontains=word) | Q(content__icontains=word)).exclude(id=obj.id)

                if similar_articles:
                    similar_articles_list += similar_articles.all()
        random.shuffle(similar_articles_list)
        return similar_articles_list[:2]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['form'] = CommentCreateForm
        context['similar_articles'] = set(chain(self.get_similar_articles(self.object)))

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


class BlogPostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = BlogPost
    template_name = 'blog/post_create.html'
    form_class = BlogPostCreateForm
    login_url = 'posts_list_url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление поста на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class BlogPostUpdateView(AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = BlogPost
    template_name = 'blog/post_update.html'
    context_object_name = 'post'
    form_class = BlogPostUpdateForm
    login_url = 'posts_list_url'
    success_message = 'Материал был успешно обновлен'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление записи: {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)


class BlogPostDeleteView(AuthorRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = BlogPost
    success_url = reverse_lazy('posts_list_url')
    context_object_name = 'post'
    template_name = 'blog/post_delete.html'
    success_message = 'Материал был успешно удален'

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
