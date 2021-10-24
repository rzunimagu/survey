"""Подключение админки."""
from django.contrib import admin

from .models import Answer, AnswerOption, Poll, Question


admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(AnswerOption)
admin.site.register(Poll)
