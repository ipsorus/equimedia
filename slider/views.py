from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView
from services.mixins import AdminRequiredMixin
from slider.forms import SliderCreateForm, SliderUpdateForm
from slider.models import Slider


class SliderCreateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Представление: создание материалов на сайте
    """
    model = Slider
    template_name = 'slider/slide-create.html'
    form_class = SliderCreateForm
    login_url = 'main'
    success_message = 'Слайд успешно добавлен'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление слайда в слайдер на главной странице'
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main')


class SliderUpdateView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Представление: обновления слайда на сайте
    """
    model = Slider
    template_name = 'slider/slide-update.html'
    context_object_name = 'post'
    form_class = SliderUpdateForm
    login_url = 'main'
    success_message = 'Слайд успешно обновлен'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Обновление слайда: {self.object.title}'
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('main')


class SliderDeleteView(AdminRequiredMixin, LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    """
    Представление: удаления слайда
    """
    model = Slider
    success_url = reverse_lazy('main')
    context_object_name = 'post'
    template_name = 'slider/slide-delete.html'
    success_message = 'Слайд успешно удален'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Удаление слайда: {self.object.title}'
        return context

    def get_success_url(self):
        return reverse_lazy('main')
