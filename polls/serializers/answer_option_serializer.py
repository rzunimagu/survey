import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from polls.models import AnswerOption

logger = logging.getLogger(__name__)


class AnswerOptionSerializer(serializers.ModelSerializer):
    """Сериалайзер для редактирования вариантов ответа на опрос."""

    class Meta:
        model = AnswerOption
        fields = ('id', 'question', 'text')

    def validate_question(self, value):
        """Запретим привязывать вариант ответа к другому опросу."""
        logger.debug(f'inside validate_question. instance:{self.instance} value: {value}')
        if self.instance and self.instance.question != value:
            raise ValidationError('Данный вариант ответа уже привязан к другому опросу.')
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        logger.debug(f'validate: {attrs}')
        question = attrs.get('question')
        if question and not question.is_editable():
                raise ValidationError({'question': 'Опрос закрыт для редактирования'})
        return attrs
