from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView

from broadcast.forms import BroadcastCreateForm, BroadcastUpdateForm
from broadcast.models import Broadcast
from el_pagination.decorators import page_template
from podcast.forms import VideoCreateForm, VideoUpdateForm
from podcast.models import Video
from services.mixins import AuthorRequiredMixin, AdminRequiredMixin


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def broadcast_section(request,
                      template='broadcast/broadcast-list.html',
                      extra_context=None):
    context = {
        'broadcasts': Broadcast.objects.all(),
        'title': 'Трансляции',
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


class BroadcastCreateView(AdminRequiredMixin, LoginRequiredMixin, CreateView):
    """
    Представление: создание трансляций на сайте
    """
    model = Broadcast
    template_name = 'broadcast/broadcast-create.html'
    form_class = BroadcastCreateForm
    login_url = 'broadcast_url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление трансляции на сайт'
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('broadcast_url')


class BroadcastUpdateView(AdminRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления трансляции на сайте
    """
    model = Broadcast
    template_name = 'broadcast/broadcast-update.html'
    context_object_name = 'broadcast'
    form_class = BroadcastUpdateForm
    login_url = 'broadcast_url'
    success_message = 'Трансляция успешно обновлена'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление трансляции: {self.object.title}'
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('broadcast_url')


class BroadcastDeleteView(AdminRequiredMixin, DeleteView):
    """
    Представление: удаления трансляции
    """
    model = Broadcast
    success_url = reverse_lazy('broadcast_url')
    context_object_name = 'broadcast'
    template_name = 'broadcast/broadcast-delete.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление трансляции: {self.object.title}'
        return context

    def get_success_url(self):
        return reverse_lazy('broadcast_url')
