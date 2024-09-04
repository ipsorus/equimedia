from django.urls import path

from .views import SliderUpdateView, SliderDeleteView, SliderCreateView

urlpatterns = [
    path('slide/create/', SliderCreateView.as_view(), name='slide_create'),
    path('slide/<int:pk>/update/', SliderUpdateView.as_view(), name='slide_update'),
    path('slide/<int:pk>/delete/', SliderDeleteView.as_view(), name='slide_delete'),
]
