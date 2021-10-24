"""Модели, необходимые для работы приложения."""
from datetime import date

from django.db import models
from polls import constants


class ActivePollsManager(models.Manager):
    """Manager для активного queryset."""

    def get_queryset(self):
        return super().get_queryset().filter(start__lte=date.today(), end__gte=date.today())


class Poll(models.Model):
    """Опросы."""

    title = models.CharField(verbose_name='Название', max_length=200)
    start = models.DateField(verbose_name='Дата начала')
    end = models.DateField(verbose_name='Дата окончания')
    description = models.TextField(verbose_name='Описание')

    objects = models.Manager()
    objects_active = ActivePollsManager()

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return f'#{self.pk}. [{self.start} <-> {self.end}] {self.title}'

    def is_active(self) -> bool:
        """Возвращаем True если опрос активен."""
        return self.start >= date.today() <= self.end

    def is_editable(self) -> bool:
        """Возвращаем True если разрешено редактировать опрос."""
        return self.pk is None or self.start > date.today()


class Question(models.Model):
    """Вопросы к опросникам."""

    poll = models.ForeignKey(Poll, verbose_name='Опрос', on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(verbose_name='Описание')
    type = models.CharField(  # noqa: VNE003,A003
        verbose_name='Вид ответа', choices=constants.QUESTION_TYPE, max_length=10,
    )

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ('poll',)

    def __str__(self):
        return f'[#{self.pk}] {self.text}'

    def is_editable(self) -> bool:
        """Возвращаем True если разрешено редактировать опрос."""
        return self.poll is None or self.poll.is_editable()


class AnswerOption(models.Model):
    """Допустимые варианты ответа на вопрос."""

    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
        related_name='options',
        blank=True,
    )
    text = models.TextField(verbose_name='Текст')

    class Meta:
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответа'
        ordering = ('question',)

    def __str__(self):
        return f'question #{self.question_id}. {self.text}'


class Answer(models.Model):
    """Модель для хранения ответов пользователей."""

    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    answer = models.ForeignKey(
        AnswerOption,
        verbose_name='Вариант ответа',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    text = models.CharField(verbose_name='Текст ответа', max_length=200, blank=True, null=True)
    user_id = models.IntegerField(verbose_name='ID пользователя')

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'
        ordering = ('question', 'user_id')

    def __str__(self):
        return f'Вопрос: {self.question}. Пользователь: {self.user_id}'
