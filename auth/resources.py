"""Доступные ресурсы приложения."""
from auth.serializers import UserSerializer
from rest_framework import generics, permissions


class LoginView(generics.CreateAPIView):
    """View для логина пользователей."""

    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
