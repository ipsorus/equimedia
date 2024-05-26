from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('news/<int:news_id>/', views.news_detail, name='news_detail_url'),
    path('news', views.news_section, name='news_list_url'),
]