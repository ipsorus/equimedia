from django.http import JsonResponse
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from el_pagination.decorators import page_template
from el_pagination.views import AjaxListView
from services.mixins import AuthorRequiredMixin
from .models import Comment, BlogPost
from .forms import CommentCreateForm, BlogPostUpdateForm, BlogPostCreateForm


class BlogPostListView(AjaxListView):
    context_object_name = "posts"
    template_name = "blog/posts_list.html"
    page_template = 'blog/posts-list-page.html'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True)


@page_template('blog/posts-list-page.html')
def blogs_section(request,
                  template='blog/posts_list.html',
                  extra_context=None):
    context = {
        'posts': BlogPost.objects.filter(is_published=True),
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


# class BlogPostListView(ListView):
#     model = BlogPost
#     template_name = 'blog/posts_list.html'
#     context_object_name = 'posts'
#
#     # paginate_by = 10
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Страница блогов'
#         return context


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    queryset = model.objects.detail()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
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


class BlogPostDeleteView(AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = BlogPost
    success_url = reverse_lazy('posts_list_url')
    context_object_name = 'post'
    template_name = 'blog/post_delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление записи: {self.object.title}'
        return context


# def posts_list(request):
#     posts = BlogPost.objects.all()
#     paginator = Paginator(posts, per_page=5)
#     page_number = request.GET.get('page')
#     page_object = paginator.get_page(page_number)
#     context = {'page_obj': page_object}
#     return render(request, 'blog/posts_list.html', {'posts': posts})
#     # return render(request, 'blog/posts_list.html', context)


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
        comment.save()

        if self.is_ajax():
            return JsonResponse({
                'is_child': comment.is_child_node(),
                'id': comment.id,
                'author': comment.author.username,
                'parent_id': comment.parent_id,
                'time_create': comment.time_create.strftime('%d %b %Y %H:%M'),
                'avatar': comment.author.profile.avatar.url,
                'content': comment.content,
                'get_absolute_url': comment.author.profile.get_absolute_url()
            }, status=200)

        return redirect(comment.post.get_absolute_url())

    def handle_no_permission(self):
        return JsonResponse({'error': 'Необходимо авторизоваться для добавления комментариев'}, status=400)
