from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('articles/<int:article_id>/', views.article_detail, name='article_detail_url'),
    path('articles', views.articles_section, name='articles_list_url'),
]