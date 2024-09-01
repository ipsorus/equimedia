from django.urls import path

from . import views
from .views import VideoDeleteView, VideoCreateView, VideoUpdateView

urlpatterns = [
    path('video', views.video_section, name='video_list_url'),
    path('video/create/', VideoCreateView.as_view(), name='video_create'),
    path('video/<int:pk>/update/', VideoUpdateView.as_view(), name='video_update'),
    path('video/<int:pk>/delete/', VideoDeleteView.as_view(), name='video_delete'),
]
