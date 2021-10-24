"""Базовые настройки для тестов."""
from uuid import uuid4

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class BaseTestCase(TestCase):
    """Базовый класс для тестов."""

    @staticmethod
    def _create_user_and_api_client(**kwargs):
        default_params = {
            'username': str(uuid4()),
            'email': '{0}@test.ru'.format(uuid4()),
            'password': 'password',
            'is_active': True,
        }
        if kwargs:
            default_params.update(kwargs)

        created_user = User.objects.create_user(**default_params)
        created_api_client = APIClient()
        created_api_client.login(username=default_params['username'], password=default_params['password'])
        return created_user, created_api_client

    @classmethod
    def setUpTestData(cls):
        cls.non_authorized_client = APIClient()
        cls.user, cls.authorized_client = cls._create_user_and_api_client(
            username='user',
            email='user@user.com',
            password='password',
            is_active=True,
        )
