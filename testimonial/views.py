from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from services.email import send_testimonial_email_message
from services.utils import get_client_ip
from testimonial.forms import TestimonialCreateForm
from testimonial.models import Testimonial


class TestimonialCreateView(SuccessMessageMixin, CreateView):
    """
    Представление: создание отзыва на сайте
    """
    model = Testimonial
    template_name = 'portal/about_us.html'
    form_class = TestimonialCreateForm
    login_url = 'about_us'
    success_message = 'Ваш отзыв успешно отправлен администрации сайта'
    success_url = reverse_lazy('about_us')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['testimonials'] = self.model.objects.filter(is_published=True)[:5]
        context['title'] = "О нас"
        return context

    def form_valid(self, form):
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.ip_address = get_client_ip(self.request)
            if self.request.user.is_authenticated:
                testimonial.author = self.request.user
            else:
                testimonial.author = testimonial.author

            subject = 'Новый отзыв на сайте'
            send_testimonial_email_message(subject, testimonial.email, testimonial.content, testimonial.ip_address,
                                           testimonial.author)
        return super().form_valid(form)
