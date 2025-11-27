import pytest

from producers.models import Producer


@pytest.fixture
def producer():
    return Producer.objects.create(
        name="Produtor Padrão",
        document_type="CPF",
        document="60435059084",
    )
