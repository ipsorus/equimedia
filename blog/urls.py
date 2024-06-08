from django.urls import path

from blog.views import BlogPostListView, CommentCreateView, BlogPostDetailView, BlogPostDeleteView, \
    BlogPostUpdateView, BlogPostCreateView

urlpatterns = [
    path('posts/', BlogPostListView.as_view(), name='posts_list_url'),
    path('posts/create/', BlogPostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/update/', BlogPostUpdateView.as_view(), name='post_update'),
    path('posts/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),
    path('posts/<int:pk>/', BlogPostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/comments/create/', CommentCreateView.as_view(), name='comment_create_view'),
]