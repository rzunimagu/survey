"""Доступные ресурсы приложения."""
from rest_framework import generics, permissions, status
from simple_auth.serializers import UserSerializer


class LoginView(generics.CreateAPIView):
    """View для логина пользователей."""

    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        response = super(LoginView, self).create(request, *args, **kwargs)
        response.status_code = status.HTTP_200_OK
        return response
