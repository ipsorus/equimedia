from django.urls import path

from . import views
from .views import BroadcastCreateView, BroadcastUpdateView, BroadcastDeleteView

urlpatterns = [
    path('broadcast', views.broadcast_section, name='broadcast_url'),
    path('broadcast/create/', BroadcastCreateView.as_view(), name='broadcast_create'),
    path('broadcast/<int:pk>/update/', BroadcastUpdateView.as_view(), name='broadcast_update'),
    path('broadcast/<int:pk>/delete/', BroadcastDeleteView.as_view(), name='broadcast_delete'),
]
