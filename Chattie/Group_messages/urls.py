from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_group, name='select_group'),
    path('chat/<path:id>', views.chat, name='chat'),
    path('settings/<path:id>', views.settings, name='settings')
]
