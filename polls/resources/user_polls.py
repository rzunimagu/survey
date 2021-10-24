from datetime import date

from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet

from polls.models import Poll
from polls.serializers.poll_serializer import ViewPollSerializer


class UserActivePollViewset(ReadOnlyModelViewSet):
    """Viewset для просмотра опросов."""

    permission_classes = (permissions.AllowAny,)
    queryset = Poll.objects_active.all()
    serializer_class = ViewPollSerializer
