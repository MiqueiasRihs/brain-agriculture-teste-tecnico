from django.core.exceptions import ValidationError

from producers.models import Producer
from producers.factories import ProducerFactory

import pytest


pytestmark = pytest.mark.django_db


def test_producer_valid_cpf_creation(user_factory):
    producer = ProducerFactory(
        name="Produtor teste",
        document="60435059084",
        user=user_factory(),
    )
    assert producer.name == "Produtor teste"
    assert Producer.objects.count() == 1


def test_producer_duplicate_cpf_creation(user_factory):
    ProducerFactory(document="60435059084", user=user_factory())

    with pytest.raises(ValidationError):
        producer = Producer(
            name="Produtor teste 2",
            document_type="CPF",
            document="60435059084",
            user=user_factory(),
        )
        producer.full_clean()


def test_producer_invalid_cpf_creation(user_factory):
    producer = Producer(
        name="Produtor Teste",
        document_type="CPF",
        document="12345678900",
        user=user_factory(),
    )

    with pytest.raises(ValidationError):
        producer.full_clean()


def test_producer_valid_cnpj_creation(user_factory):
    producer = ProducerFactory(
        name="Produtor teste",
        document_type="CNPJ",
        document="93997567000165",
        user=user_factory(),
    )
    assert producer.name == "Produtor teste"
    assert Producer.objects.count() == 1


def test_producer_invalid_cnpj_creation(user_factory):
    producer = Producer(
        name="Produtor Teste",
        document_type="CNPJ",
        document="12345678900000",
        user=user_factory(),
    )

    with pytest.raises(ValidationError):
        producer.full_clean()


def test_producer_no_document_mask_creation(user_factory):
    producer = ProducerFactory(
        name="Produtor Teste",
        document_type="CNPJ",
        document="33.680.548/0001-89",
        user=user_factory(),
    )

    assert Producer.objects.count() == 1
    assert producer.document == "33680548000189"


def test_delete_producer(user_factory):
    producer = ProducerFactory(
        name="Produtor teste",
        document_type="CNPJ",
        document="93997567000165",
        user=user_factory(),
    )

    assert Producer.objects.count() == 1
    producer.delete()
    assert Producer.objects.count() == 0
