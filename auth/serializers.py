import logging
from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(label='username')
    password = serializers.CharField(label='password')

    def validate(self, attrs):
        logger.debug(f'{self.context}')
        user = authenticate(self.context['request'], username=attrs['username'], password=attrs['password'])
        if user is None:
            raise ValidationError('Логин и/или пароль указан не верно.')
        return attrs

    def create(self, validated_data):
        user = authenticate(
            self.context['request'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        login(self.context['request'], user)
        return user

    def update(self, instance, validated_data):
        raise NotImplementedError()

