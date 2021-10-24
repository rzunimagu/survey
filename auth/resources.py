from rest_framework import generics, permissions

from auth.serializers import UserSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
