"""Тестируем login."""
import logging

from app.tests.base import BaseTestCase
from django.urls import reverse
from rest_framework import status


logger = logging.getLogger(__name__)


class AuthTestCase(BaseTestCase):
    """Класс для тестирования авторизации."""

    def test_wrong_login(self):
        """Проверка ошибочного login."""
        response = self.non_authorized_client.post(
            path=reverse('simple-user-login'),
            data={
                'username': self.user.username + '-wrong-username',
                'password': 'password',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIsNotNone(response.data.get('non_field_errors'))

    def test_correct_login(self):
        """Проверка корректного login."""
        response = self.non_authorized_client.post(
            path=reverse('simple-user-login'),
            data={
                'username': self.user.username,
                'password': 'password',
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
