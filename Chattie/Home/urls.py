from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    path('sign_up/', views.sign_up, name='sign_up'),
]