from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

import os
import uuid
import pytest
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "brain_agriculture.settings")
django.setup()


@pytest.fixture
def user_factory():
    User = get_user_model()

    def _create_user(**kwargs):
        username = kwargs.pop("username", f"user_{uuid.uuid4().hex[:8]}")
        password = kwargs.pop("password", "testpass123")
        return User.objects.create_user(username=username, password=password, **kwargs)

    return _create_user


@pytest.fixture
def api_client(user_factory):
    user = user_factory(is_staff=True)
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def producer_client(user_factory):
    user = user_factory(is_staff=False)
    client = APIClient()
    client.force_authenticate(user=user)
    return client, user
