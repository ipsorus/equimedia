from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView

from el_pagination.decorators import page_template
from podcast.forms import VideoCreateForm, VideoUpdateForm
from podcast.models import Video
from services.mixins import AuthorRequiredMixin, AdminRequiredMixin


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@page_template('podcast/video-list-page.html')
def video_section(request,
                  template='podcast/video-list.html',
                  extra_context=None):
    context = {
        'videos': Video.objects.filter(is_published=True),
        'title': 'Подкасты, Видео',
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


class VideoCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Video
    template_name = 'podcast/video-single-create.html'
    form_class = VideoCreateForm
    login_url = 'video_list_url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление видео на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('video_list_url')


class VideoUpdateView(AdminRequiredMixin, AuthorRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления материала на сайте
    """
    model = Video
    template_name = 'podcast/video-single-update.html'
    context_object_name = 'post'
    form_class = VideoUpdateForm
    login_url = 'video_list_url'
    success_message = 'Видео было успешно обновлено'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление записи: {self.object.title}'
        return context

    def form_valid(self, form):
        # form.instance.updater = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('video_list_url')


class VideoDeleteView(AdminRequiredMixin, AuthorRequiredMixin, DeleteView):
    """
    Представление: удаления материала
    """
    model = Video
    success_url = reverse_lazy('video_list_url')
    context_object_name = 'post'
    template_name = 'podcast/video-single-delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление записи: {self.object.title}'
        return context

    def get_success_url(self):
        return reverse_lazy('video_list_url')
