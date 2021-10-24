"""Редактирование вопросов (доступ только у администраторами системы)."""
from polls.models import Question
from polls.serializers.question_serializer import QuestionSerializer
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet


class QuestionEditViewset(ModelViewSet):
    """Viewset для редактирования вопросов (доступ только у администраторами системы)."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = QuestionSerializer

    def get_queryset(self):
        """Получим список вопросов для текущего опроса."""
        return Question.objects.filter(poll_id=self.kwargs['poll_id']).prefetch_related('options')

    def get_serializer(self, *args, **kwargs):
        data = kwargs.get('data', None)
        if data:
            data = data.copy()
            data['poll'] = int(self.kwargs['poll_id'])
        return super().get_serializer(*args, **kwargs)

    def perform_destroy(self, instance):
        """Запретим удаление вопросов для закрытого опроса."""
        if not instance.poll.is_editable():
            raise ValidationError({'poll': 'Опрос закрыт для редактирования'})
