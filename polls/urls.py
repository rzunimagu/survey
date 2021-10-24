"""Доступные роуты."""
from django.urls import include, path
from rest_framework import routers

from .resources.admin_answer_options import AnswerOptionViewset
from .resources.admin_polls import PollEditViewset
from .resources.admin_questions import QuestionEditViewset
from .resources.user_answer_question import UserAnswerView
from .resources.user_answers_show import PollResultViewset
from .resources.user_polls import UserActivePollViewset

admin_router = routers.DefaultRouter()
admin_router.register('active-polls', PollEditViewset, basename='polls')

admin_router.register(
    'active-polls/(?P<poll_id>\d+)/questions',
    QuestionEditViewset,
    basename='questions',
)

admin_router.register(
    'active-polls/(?P<poll_id>\d+)/questions/(?P<question_id>\d+)/options',
    AnswerOptionViewset,
    basename='answer-options',
)

user_router = routers.DefaultRouter()
user_router.register('active-polls', UserActivePollViewset, basename='user-polls')
user_router.register(
    'results',
    PollResultViewset,
    basename='user-results'
)


urlpatterns = [
    path('admin/', include(admin_router.urls)),
    path('user/active-polls/<int:poll_id>/questions/<int:question_id>/', UserAnswerView.as_view()),
    path('user/', include(user_router.urls)),
]
