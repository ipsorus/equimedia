from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('cats/<int:cat_id>/', views.categories),
    # path('news/<slug:news_slug>/', views.news_detail, name='news_detail_url'),
    # path('article/<slug:article_slug>/', views.article, name='article_detail_url'),
    # path('post/<slug:post_slug>/', views.post, name='post_detail_url'),

]