from producers.serializers import ProducerSerializer

import pytest


@pytest.mark.django_db
def test_serializer_valid_cpf():
    data = {
        "name": "João da Silva",
        "document_type": "CPF",
        "document": "11144477735",
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_serializer_invalid_cpf():
    data = {
        "name": "João da Silva",
        "document_type": "CPF",
        "document": "11111111111",
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is False
    assert "document" in serializer.errors
    
    
@pytest.mark.django_db
def test_serializer_valid_cnpj():
    data = {
        "name": "João da Silva",
        "document_type": "CNPJ",
        "document": "24970180000100",
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_serializer_invalid_cnpj():
    data = {
        "name": "João da Silva",
        "document_type": "CNPJ",
        "document": "11111111111111",
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is False
    assert "document" in serializer.errors
    

@pytest.mark.django_db
def test_serializer_normalizes_document():
    data = {
        "name": "João Silva",
        "document_type": "CPF",
        "document": "123.456.789-09",
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is True
    assert serializer.validated_data["document"] == "12345678909"
    

@pytest.mark.django_db
def test_serializer_without_document():
    data = {
        "name": "João Silva",
        "document_type": "CPF",
    }

    serializer = ProducerSerializer(data=data)
    assert serializer.is_valid() is False
    assert "document" in serializer.errors
    assert serializer.errors["document"][0].code == "required"