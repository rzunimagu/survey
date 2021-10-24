"""Сериалайзер для редактирования вопросов."""
import logging

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from polls import constants
from polls.models import AnswerOption, Question
from polls.serializers.answer_option_serializer import AnswerOptionSerializer

logger = logging.getLogger(__name__)


class QuestionSerializer(serializers.ModelSerializer):
    """Сериалайзер для редактирования опросов."""

    options = AnswerOptionSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        logger.debug(f'create question serializer {args}, {kwargs}')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Question
        fields = ('id', 'poll', 'type', 'text', 'options')
        read_only_fields = ('id',)

    def to_internal_value(self, data):
        logger.debug(f'to_internal_value. instance:{self.instance} original values: {data}')
        data = data.copy()
        options_data = data.pop('options', ())
        options = []
        data = super().to_internal_value(data)
        for option in options_data:
            if self.instance:
                option['question'] = self.instance.pk
            option_id = option.pop('id', None)
            options.append(
                AnswerOptionSerializer(
                    instance=AnswerOption.objects.get(id=int(option_id)) if option_id else None,
                    data=option,
                )
            )
        data['options'] = options
        return data

    @staticmethod
    def _is_options_needed(question_type: str) -> bool:
        """Нужны ли доп. опции для данного типа опроса."""
        return question_type in (constants.QUESTION_TYPE_SINGLE, constants.QUESTION_TYPE_MULTIPLE)

    def validate(self, attrs):
        logger.debug(f'inside validation: {attrs}')
        attrs = super().validate(attrs)
        poll = attrs.get('poll')
        if poll and not poll.is_editable():
            raise ValidationError('Опрос закрыт для редактирования.')

        options = attrs.get('options', [])
        if self._is_options_needed(attrs['type']) and not options:
            raise ValidationError({'options': 'Не указаны варианты ответа.'})
        if not self._is_options_needed(attrs['type']) and options:
            raise ValidationError({'options': 'Для данного типа вопроса не нужны дополнительные опции.'})
        option_errors = {}
        for index, option in enumerate(options, start=1):
            if not option.is_valid():
                option_errors[f'Вариант #{index}'] = option.errors
        if option_errors:
            raise ValidationError({'options': option_errors})

        return attrs

    @staticmethod
    def _delete_unused_options(question, current_options):
        """Удалим неиспользуемые опции."""
        question.options.exclude(pk__in=(option.instance.id for option in current_options if option.instance))

    @staticmethod
    def _save_options(question, current_options):
        """Сохраним варианты ответа на опрос."""
        for option in current_options:
            option.validated_data['question'] = question
            option.save()

    def update(self, instance, validated_data):
        options = validated_data.pop('options')
        logger.debug(f'update model. options: {options}')
        question = super().update(instance, validated_data)
        self._delete_unused_options(question=question, current_options=options)
        self._save_options(question=question, current_options=options)
        return question

    def create(self, validated_data):
        options = validated_data.pop('options')
        logger.debug(f'create model. options: {options}')
        question = super().create(validated_data)
        self._save_options(question, current_options=options)
        return question
