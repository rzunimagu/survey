"""Тестирование управления опросами."""
from app.tests.base import BaseTestCase
from django.urls import reverse
from rest_framework import status


class AdminPollsTestCase(BaseTestCase):
    """Класс для тестирования управления опросами."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

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
