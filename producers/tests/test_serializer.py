from producers.serializers import ProducerSerializer

import pytest


pytestmark = pytest.mark.django_db


def test_serializer_valid_cpf(user_factory):
    user = user_factory()
    data = {
        "name": "João da Silva",
        "document_type": "CPF",
        "document": "11144477735",
        "user": user.id,
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is True


def test_serializer_invalid_cpf(user_factory):
    user = user_factory()
    data = {
        "name": "João da Silva",
        "document_type": "CPF",
        "document": "11111111111",
        "user": user.id,
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is False
    assert "document" in serializer.errors


def test_serializer_duplicate_cpf(user_factory):
    user_1 = user_factory()
    user_2 = user_factory()
    data = {
        "name": "João da Silva",
        "document_type": "CPF",
        "document": "11144477735",
        "user": user_1.id,
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is True
    serializer.save()

    duplicate_data = {**data, "user": user_2.id}
    duplicate_serializer = ProducerSerializer(data=duplicate_data)
    assert duplicate_serializer.is_valid() is False
    assert "document" in duplicate_serializer.errors


def test_serializer_valid_cnpj(user_factory):
    user = user_factory()
    data = {
        "name": "João da Silva",
        "document_type": "CNPJ",
        "document": "24970180000100",
        "user": user.id,
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is True


def test_serializer_invalid_cnpj(user_factory):
    user = user_factory()
    data = {
        "name": "João da Silva",
        "document_type": "CNPJ",
        "document": "11111111111111",
        "user": user.id,
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is False
    assert "document" in serializer.errors


def test_serializer_normalizes_document(user_factory):
    user = user_factory()
    data = {
        "name": "João Silva",
        "document_type": "CPF",
        "document": "123.456.789-09",
        "user": user.id,
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is True
    assert serializer.validated_data["document"] == "12345678909"


def test_serializer_without_document(user_factory):
    user = user_factory()
    data = {
        "name": "João Silva",
        "document_type": "CPF",
        "user": user.id,
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is False
    assert "document" in serializer.errors
    assert serializer.errors["document"][0].code == "required"
