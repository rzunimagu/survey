"""Ресурсы для редактирования опросов."""
import logging

from django.http import Http404
from polls import constants
from polls.models import AnswerOption, Question
from polls.serializers.answer_option_serializer import AnswerOptionSerializer
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ModelViewSet


logger = logging.getLogger(__name__)


class AnswerOptionViewset(ModelViewSet):
    """Viewset для редактирования вариантов ответа на опрос (доступ только у администраторами системы)."""

    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = AnswerOptionSerializer

    def get_queryset(self):
        """Получим список вариантов ответа для текущего опроса."""
        logger.debug(f'kwargs: {self.kwargs}')
        try:
            question = Question.objects.get(
                id=self.kwargs['question_id'],
                poll_id=self.kwargs['poll_id'],
                type__in=[constants.QUESTION_TYPE_SINGLE, constants.QUESTION_TYPE_MULTIPLE],
            )
        except Question.DoesNotExist:
            raise Http404()

        return AnswerOption.objects.filter(
            question=question,
        ).select_related('question')

    def perform_destroy(self, instance):
        """Запретим удаление вариантов ответа для закрытого опроса."""
        logger.debug(f'Удаление варианта ответа: {instance}')
        if not instance.question.is_editable():
            raise ValidationError({'question': 'Опрос закрыт для редактирования'})

    def get_serializer(self, *args, **kwargs):
        logger.debug(f'get_serializer: {args} {kwargs}, self.kwargs: {self.kwargs}')
        data = kwargs.get('data', None)
        if data:
            data = data.copy()
            data['question'] = int(self.kwargs['question_id'])
        return super().get_serializer(*args, **kwargs)
