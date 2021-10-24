"""Сериалайзер для редактирования опросов."""
import logging

from polls.models import Poll
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class EditPollSerializer(serializers.ModelSerializer):
    """Сериалайзер для редактирования опросов."""

    questions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start', 'end', 'description', 'questions')
        read_only_fields = ('id',)

    def validate_start(self, value):
        logger.debug(f'validate "start" field. value: {value}, instance:{self.instance}')
        if self.instance and self.instance.start != value:
            raise ValidationError({'start': 'Запрещено менять дату начала'})
        return value

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if attrs['end'] < attrs['start']:
            raise ValidationError({'end': 'Дата окончания опроса не может быть меньше даты начала.'})
        if self.instance and not self.instance.is_editable():
            raise ValidationError('Опрос закрыт для редактирования.')
        return attrs


class ViewPollSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра опросов."""

    questions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start', 'end', 'description', 'questions')
        read_only_fields = ('id', 'title', 'start', 'end', 'description', 'questions')
