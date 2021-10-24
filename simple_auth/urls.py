"""Доступные роуты."""
from django.urls import path

from .resources import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='simple-user-login'),
]
