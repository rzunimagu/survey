"""Отображение результатов опросов."""
from polls.models import Answer
from polls.serializers.user_results import UserResults
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet


class PollResultViewset(ReadOnlyModelViewSet):
    """Viewset для просмотра результатов по пользователям."""

    permission_classes = (permissions.AllowAny,)
    serializer_class = UserResults
    queryset = Answer.objects.values('user_id').distinct()
    lookup_field = 'user_id'
