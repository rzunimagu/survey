"""Приложение для работы с опросами."""
from django.apps import AppConfig


class AppConfig(AppConfig):
    """Настройки приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
