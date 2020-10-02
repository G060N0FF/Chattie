from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('select_room', views.select_room, name='select_room'),
]