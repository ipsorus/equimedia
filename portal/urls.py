from django.urls import path

from testimonial.views import TestimonialCreateView
from . import views
from .views import FeedbackCreateView, about_us

urlpatterns = [
    path('', views.index, name='main'),
    path('index.html', views.redirect_to_home, name='main'),
    path('contacts/', FeedbackCreateView.as_view(), name='contacts'),
    path('about_us/', TestimonialCreateView.as_view(), name='about_us'),
]
