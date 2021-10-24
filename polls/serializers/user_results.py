"""Сериалайзеры, необходимые для отображение результатов пользователя с детализацией по опросам."""
import logging

from polls.models import Answer, Poll, Question
from rest_framework import serializers

logger = logging.getLogger(__name__)


class UserAnswersSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения ответа при отображении результатов."""

    answer_text = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ('id', 'text', 'answer', 'answer_text')

    @staticmethod
    def get_answer_text(instance):
        return instance.answer.text if instance.answer else None


class UserQuestionsSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения информации о вопросе при отображении результатов."""

    answers = UserAnswersSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'text', 'type', 'answers')


class UserPollsSerializer(serializers.ModelSerializer):
    """Сериалайзер для отображения информации об опросе при отображении результатов."""

    questions = serializers.SerializerMethodField(label='Вопросы')

    class Meta:
        model = Poll
        fields = ('id', 'title', 'start', 'end', 'description', 'questions')

    def __init__(self, user_id=None, *args, **kwargs):
        self.user_id = user_id
        super().__init__(*args, **kwargs)

    def get_questions(self, instance):
        logger.debug(f'user: {self.user_id}, instance:{instance}')
        queryset = Question.objects.filter(poll=instance, answers__user_id=self.user_id).distinct()
        return UserQuestionsSerializer(queryset, many=True).data


class UserResults(serializers.Serializer):
    """Получим список ответов пользователя."""

    user_id = serializers.IntegerField(label='id пользователя.')
    polls = serializers.SerializerMethodField(label='Опросы')

    def __init__(self, *args, **kwargs):
        logger.debug(f'UserResults {args} {kwargs}')
        super().__init__(*args, **kwargs)

    def create(self, validated_data):
        raise NotImplementedError()

    def update(self, instance, validated_data):
        raise NotImplementedError()

    @staticmethod
    def get_polls(data):
        queryset = Poll.objects.filter(questions__answers__user_id=data['user_id']).distinct()
        return UserPollsSerializer(instance=queryset, user_id=data['user_id'], many=True).data
