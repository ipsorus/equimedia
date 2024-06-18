from django.contrib import admin
from django.urls import path

from . import views
from .views import FeedbackCreateView

urlpatterns = [
    path('', views.index, name='main'),
    path('cats/<int:cat_id>/', views.categories),
    path('feedback/', FeedbackCreateView.as_view(), name='feedback'),
    # path('article/<slug:article_slug>/', views.article, name='article_detail_url'),
    # path('post/<slug:post_slug>/', views.post, name='post_detail_url'),

]