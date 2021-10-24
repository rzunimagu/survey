"""View для принятия ответов пользователя."""
from polls.serializers.answers_serializer import UserAnswerSerializer
from rest_framework import generics, permissions


class UserAnswerView(generics.CreateAPIView):
    """View для принятия ответов пользователя."""

    serializer_class = UserAnswerSerializer
    permission_classes = (permissions.AllowAny,)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'poll_id': self.kwargs['poll_id'],
            'question_id': self.kwargs['question_id'],
        })
        return context
