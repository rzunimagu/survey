"""Ресурсы для редактирования опросов. (доступ только у администраторами системы)."""
from polls.models import Poll
from polls.serializers.poll_serializer import EditPollSerializer
from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet


class PollEditViewset(ModelViewSet):
    """Viewset для редактирования опросов (доступ только у администраторами системы)."""

    permission_classes = (permissions.IsAuthenticated,)
    queryset = Poll.objects.all()
    serializer_class = EditPollSerializer
