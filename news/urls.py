from django.urls import path

from . import views
from .views import NewsPostCreateView, NewsPostUpdateView, NewsPostDeleteView, NewsPostDetailView, CommentCreateView, \
    RatingCreateView

urlpatterns = [
    path('news/<int:pk>/', NewsPostDetailView.as_view(), name='news_detail_url'),
    path('news', views.news_section, name='news_list_url'),
    path('news/create/', NewsPostCreateView.as_view(), name='news_post_create'),
    path('news/<int:pk>/update/', NewsPostUpdateView.as_view(), name='news_post_update'),
    path('news/<int:pk>/delete/', NewsPostDeleteView.as_view(), name='news_post_delete'),
    path('news/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
    path('news/<int:pk>/news/rating/', RatingCreateView.as_view(), name='news_rating'),
]