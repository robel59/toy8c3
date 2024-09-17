from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:email>/', views.chat_room, name='chat_room'),
    path('team/', views.team_dashboard, name='team_dashboard'),
    path('team/room/<str:email>/', views.team_chat_room, name='team_chat_room'),
]
