from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.select_group, name='select_group'),
    path('chat/<path:id>', views.chat, name='chat'),
    path('settings/<path:id>', views.settings, name='settings'),
    path('add/<path:group_id>/<path:user_id>', views.add, name='add'),
    path('remove/<path:group_id>/<path:user_id>', views.remove, name='remove'),
    path('load_messages/', views.load_messages, name='load_messages')
]
