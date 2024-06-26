from django.urls import path

from . import views
from .views import ArticlePostCreateView, ArticlePostUpdateView, ArticlePostDeleteView

urlpatterns = [
    path('articles/<int:article_id>/', views.article_detail, name='article_detail_url'),
    path('articles', views.articles_section, name='articles_list_url'),
    path('articles/create/', ArticlePostCreateView.as_view(), name='article_post_create'),
    path('articles/<int:pk>/update/', ArticlePostUpdateView.as_view(), name='article_update_url'),
    path('articles/<int:pk>/delete/', ArticlePostDeleteView.as_view(), name='article_delete_url'),
]