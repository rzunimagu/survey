import logging

from rest_framework import generics, permissions

from polls.serializers.answers_serializer import UserAnswerSerializer

logger = logging.getLogger(__name__)


class UserAnswerView(generics.CreateAPIView):
    serializer_class = UserAnswerSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'poll_id': self.kwargs['poll_id'],
            'question_id': self.kwargs['question_id'],
        })
        return context
