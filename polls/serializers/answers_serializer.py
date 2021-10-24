"""Сериалайзер для ответов на вопросы."""
import logging

from django.http import Http404
from polls import constants
from polls.models import Answer, AnswerOption, Poll, Question
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class BaseAnswerSerializer(serializers.ModelSerializer):
    """Базовый сериалайзер для сохранения ответов пользователя."""

    class Meta:
        model = Answer
        fields = '__all__'


class UserAnswerSerializer(serializers.Serializer):
    """Сериалайзер для ответов на вопросы."""

    user_id = serializers.IntegerField(label='id пользователя')

    def __init__(self, *args, **kwargs):
        """
        Проверим, что переданы актуальные poll_id и question_id.

        Добавим в сериалайзер поля, в зависимости от типа ожидаемого ответа на выбранный вопрос.
        """
        poll_id = kwargs.get('context').pop('poll_id', None)
        question_id = kwargs.get('context').pop('question_id', None)
        try:
            self.poll = Poll.objects_active.get(pk=poll_id)
        except Poll.DoesNotExist:
            raise Http404()
        try:
            self.question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            raise Http404()

        if self.question.type == constants.QUESTION_TYPE_TEXT:
            self.fields['user_answer'] = serializers.CharField(label='Текстовый ответ', required=True)
        else:
            choices = (
                (answer.id, answer.text) for answer in AnswerOption.objects.filter(question_id=question_id)
            )
            if self.question.type == constants.QUESTION_TYPE_MULTIPLE:
                self.fields['user_answer'] = serializers.MultipleChoiceField(
                    label='Вариант ответа', required=True,
                    choices=choices,
                )
            elif self.question.type == constants.QUESTION_TYPE_SINGLE:
                self.fields['user_answer'] = serializers.ChoiceField(
                    label='Вариант ответа', required=True,
                    choices=choices,
                )
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        logger.debug(f'validated data: {data}')
        answer = data.get('user_answer', None)
        data['question'] = self.question
        if self.question.type == constants.QUESTION_TYPE_TEXT:
            data['answer'] = None
            data['text'] = answer
        else:
            data['text'] = None
            data['answer'] = [answer] if self.question.type == constants.QUESTION_TYPE_SINGLE else answer
        return data

    def validate(self, attrs):
        logger.debug(f'validate {attrs}')
        if not attrs['text'] and not attrs['answer']:
            raise ValidationError({'user_answer': 'Необходимо дать ответ'})
        return attrs

    def create(self, validated_data):
        Answer.objects.filter(question=validated_data['question'], user_id=validated_data['user_id']).delete()
        if validated_data['answer']:
            data_to_create = [
                {
                    'question': validated_data['question'].id,
                    'answer': answer,
                    'text': None,
                    'user_id': validated_data['user_id'],
                } for answer in validated_data['answer']
            ]
            answer_serializer = BaseAnswerSerializer(data=data_to_create, many=True)
        else:
            answer_serializer = BaseAnswerSerializer(data={
                'question': validated_data['question'].id,
                'answer': None,
                'text': validated_data['text'],
                'user_id': validated_data['user_id'],
            })
        answer_serializer.is_valid(raise_exception=True)
        answer_serializer.save()

        return validated_data

    def update(self, instance, validated_data):
        raise NotImplementedError()
