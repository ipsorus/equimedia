from django.contrib import admin
from django.urls import path

from . import views
from .views import EventCreateView, EventUpdateView, EventDeleteView

urlpatterns = [
    path('event/<int:event_id>/', views.event_detail, name='event_detail_url'),
    path('calendar/', views.calendar_view, name='calendar_page'),
    path('get_events/', views.get_events, name='get_events'),
    path('get_weekly_events/', views.get_weekly_events, name='get_weekly_events'),
    path('get_monthly_events/', views.get_monthly_events, name='get_monthly_events'),
    path('tournaments/', views.tournaments, name='tournaments'),
    path('tournaments/<int:tournament_id>/', views.tournament_detail, name='tournament_detail_url'),
    path('tournaments/<int:tournament_id>/stage/<int:stage_id>/', views.stage_detail, name='stage_detail_url'),
    path('tournaments/contest/<int:tournament_id>/', views.contest_detail, name='contest_detail_url'),
    path('event/create/', EventCreateView.as_view(), name='event_create'),
    path('event/<int:pk>/update/', EventUpdateView.as_view(), name='event_update_url'),
    path('event/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete_url'),
]