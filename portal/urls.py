from django.urls import path

from testimonial.views import TestimonialCreateView
from . import views
from .views import FeedbackCreateView, about_us

urlpatterns = [
    path('', views.index, name='main'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    path('about_us/', TestimonialCreateView.as_view(), name='about_us'),
]
