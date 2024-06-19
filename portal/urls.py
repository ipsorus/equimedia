from django.contrib import admin
from django.urls import path

from . import views
from .views import FeedbackCreateView

urlpatterns = [
    path('', views.index, name='main'),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
]