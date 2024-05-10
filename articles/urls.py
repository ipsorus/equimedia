from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('articles/<slug:article_slug>/', views.article_detail, name='article_detail_url'),
]