from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from polls.models import Poll
from polls.serializers.poll_serializer import EditPollSerializer


class PollEditViewset(ModelViewSet):
    """Viewset для редактирования опросов (доступ только у администраторами системы)."""

    permission_classes = (permissions.IsAdminUser,)
    queryset = Poll.objects.all()
    serializer_class = EditPollSerializer
