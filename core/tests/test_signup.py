import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from producers.models import Producer


pytestmark = pytest.mark.django_db


@pytest.fixture
def signup_url():
    return reverse("signup")


@pytest.fixture
def unauthenticated_client():
    return APIClient()


def build_signup_payload(**overrides):
    payload = {
        "username": "new_user",
        "password": "Testepass123",
        "email": "new_user@example.com",
        "name": "Produtor Novo",
        "document_type": "CPF",
        "document": "111.444.777-35",
    }
    payload.update(overrides)
    return payload


def test_signup_creates_user_and_producer(unauthenticated_client, signup_url):
    response = unauthenticated_client.post(
        signup_url,
        build_signup_payload(),
        format="json",
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert {"access", "refresh", "user", "producer"}.issubset(response.data.keys())

    user = get_user_model().objects.get(username="new_user")
    producer = Producer.objects.get(user=user)

    assert producer.name == "Produtor Novo"
    assert producer.document == "11144477735"


def test_signup_rejects_duplicate_username(unauthenticated_client, signup_url, user_factory):
    user_factory(username="existing_user")

    response = unauthenticated_client.post(
        signup_url,
        build_signup_payload(username="existing_user", document="24970180000100", document_type="CNPJ"),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "username" in response.data


def test_signup_rejects_invalid_document(unauthenticated_client, signup_url):
    response = unauthenticated_client.post(
        signup_url,
        build_signup_payload(document="11111111111"),
        format="json",
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "document" in response.data
