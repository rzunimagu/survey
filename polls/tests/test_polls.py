"""Тестирование управления опросами."""
import logging
from datetime import date, timedelta

from app.tests.base import BaseTestCase
from django.urls import reverse
from polls.models import Poll
from rest_framework import status


logger = logging.getLogger(__name__)


class PollsTestCase(BaseTestCase):
    """Класс для тестирования работы с опросами."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.active_poll = Poll.objects.create(
            title='active poll # 1',
            start=date.today() - timedelta(100),
            end=date.today() + timedelta(100),
            description='description for poll #1',
        )
        cls.inactive_poll = Poll.objects.create(
            title='inactive poll #2',
            start=date.today() + timedelta(50),
            end=date.today() + timedelta(100),
            description='description for poll #2',
        )

    def test_active_pols_non_authorized(self):
        """Проверка несанкционированного доступа к списку опросов."""
        response = self.non_authorized_client.get(
            path=reverse('polls-list'),
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_active_pols_authorized(self):
        """Проверка доступа к списку опросов."""
        response = self.authorized_client.get(
            path=reverse('polls-list'),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_poll(self):
        """Проверка создания опроса."""
        polls_count = Poll.objects.count()
        response = self.authorized_client.post(
            path=reverse('polls-list'),
            data={
                'title': 'test title',
                'start': date.today(),
                'end': date.today(),
                'description': 'test-description',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(polls_count + 1, Poll.objects.count())

    def test_create_poll_with_wrong_date(self):
        """Проверка создания опроса c неправильной датой."""
        polls_count = Poll.objects.count()
        response = self.authorized_client.post(
            path=reverse('polls-list'),
            data={
                'title': 'test title',
                'start': date.today(),
                'end': date.today() - timedelta(days=10),
                'description': 'test-description',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(polls_count, Poll.objects.count())
        self.assertIsNotNone(response.data.get('end'))

    def test_update_poll(self):
        """Проверка изменения не активного опроса."""
        poll = self.inactive_poll

        data = {
            'title': 'new title',
            'description': 'test-description',
            'start': poll.start,
            'end': poll.end + timedelta(days=11),
        }
        response = self.authorized_client.put(
            path=reverse('polls-detail', args=(poll.id,)),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        poll.refresh_from_db()
        self.assertEqual(poll.title, data['title'])
        self.assertEqual(poll.end, data['end'])
        self.assertEqual(poll.description, data['description'])

    def test_start_update_poll(self):
        """Проверка изменения даты начала не активного опроса."""
        poll = self.inactive_poll

        data = {
            'title': f'{poll.title} new title',
            'description': f'{poll.description} new-test-description',
            'start': poll.start + timedelta(days=11),
            'end': poll.end + timedelta(days=11),
        }
        response = self.authorized_client.put(
            path=reverse('polls-detail', args=(poll.id,)),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        poll.refresh_from_db()
        self.assertNotEqual(poll.title, data['title'])
        self.assertNotEqual(poll.end, data['end'])
        self.assertNotEqual(poll.start, data['start'])
        self.assertNotEqual(poll.description, data['description'])

    def test_update_active_poll(self):
        """Проверка изменения активного опроса."""
        poll = self.active_poll

        data = {
            'title': f'{poll.title} new title',
            'description': f'{poll.description} new-test-description',
            'start': poll.start,
            'end': poll.end + timedelta(days=11),
        }
        response = self.authorized_client.put(
            path=reverse('polls-detail', args=(poll.id,)),
            data=data,
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotEqual(poll.end, data['end'])
