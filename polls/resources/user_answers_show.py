from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from polls.models import Answer
from polls.serializers.user_results import UserResults


class PollResultViewset(ReadOnlyModelViewSet):
    """Viewset для редактирования опросов (доступ только у администраторами системы)."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserResults
    queryset = Answer.objects.values('user_id').distinct()
    lookup_field = 'user_id'
