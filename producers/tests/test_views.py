import pytest
from django.urls import reverse
from rest_framework import status

from producers.models import Producer
from producers.factories import ProducerFactory


pytestmark = pytest.mark.django_db


@pytest.fixture
def producer_list_url():
    return reverse("producer-list")


@pytest.fixture
def producer_detail_url():
    def _build(producer):
        return reverse("producer-detail", args=[str(producer.id)])

    return _build


def test_list_producers_returns_paginated_response(api_client, producer_list_url):
    ProducerFactory(name="Produtor 1", document="60435059084")
    ProducerFactory(name="Produtor 2", document_type="CNPJ", document="93997567000165")

    response = api_client.get(producer_list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert {result["name"] for result in response.data["results"]} == {
        "Produtor 1",
        "Produtor 2",
    }
    

def test_filter_producers_by_name(api_client, producer_list_url):
    ProducerFactory(name="Joao da Silva", document="11144477735")
    ProducerFactory(name="Maria Oliveira", document_type="CNPJ", document="24970180000100")

    response = api_client.get(producer_list_url, {"name": "joao"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Joao da Silva"


def test_create_producer_with_valid_cpf(api_client, producer_list_url, user_factory):
    owner = user_factory()
    payload = {
        "name": "Produtor Teste",
        "document_type": "CPF",
        "document": "11144477735",
        "user": owner.id,
    }

    response = api_client.post(producer_list_url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Produtor Teste"
    assert response.data["document_type"] == "CPF"
    assert response.data["document"] == "11144477735"
    assert response.data["is_active"] is True
    assert Producer.objects.filter(document="11144477735").exists()


def test_delete_producer(api_client, producer_detail_url):
    producer = ProducerFactory(document="60435059084")

    response = api_client.delete(producer_detail_url(producer))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Producer.objects.filter(id=producer.id).exists()


def test_create_producer_with_invalid_cpf(api_client, producer_list_url, user_factory):
    owner = user_factory()
    payload = {
        "name": "Produtor Teste",
        "document_type": "CPF",
        "document": "11111111111",
        "user": owner.id,
    }

    response = api_client.post(producer_list_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "document" in response.data
    assert response.data["document"][0].code == "invalid"


def test_update_producer(api_client, producer_detail_url):
    producer = ProducerFactory(document="60435059084")

    payload = {
        "name": "Produtor Atualizado",
    }

    response = api_client.patch(producer_detail_url(producer), payload, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Produtor Atualizado"
    producer.refresh_from_db()
    assert producer.name == "Produtor Atualizado"


def test_create_producer_with_valid_cnpj(api_client, producer_list_url, user_factory):
    owner = user_factory()
    payload = {
        "name": "Produtor Teste",
        "document_type": "CNPJ",
        "document": "24970180000100",
        "user": owner.id,
    }

    response = api_client.post(producer_list_url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Produtor Teste"
    assert response.data["document_type"] == "CNPJ"
    assert response.data["document"] == "24970180000100"
    assert response.data["is_active"] is True
    assert Producer.objects.filter(document="24970180000100").exists()


def test_create_producer_with_duplicate_document(api_client, producer_list_url, user_factory):
    ProducerFactory(document="60435059084")

    owner = user_factory()
    payload = {
        "name": "Produtor Teste 2",
        "document_type": "CPF",
        "document": "60435059084",
        "user": owner.id,
    }

    response = api_client.post(producer_list_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "document" in response.data
    assert response.data["document"][0].code == "unique"
