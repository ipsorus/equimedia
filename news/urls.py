from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('news/<slug:news_slug>/', views.news_detail, name='news_detail_url'),
    path('news', views.news_section, name='news_list_url'),
]