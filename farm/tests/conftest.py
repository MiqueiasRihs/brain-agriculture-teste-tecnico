import pytest

from producers.factories import ProducerFactory


@pytest.fixture
def producer(user_factory):
    return ProducerFactory(
        name="Produtor Padrão",
        document="60435059084",
        user=user_factory(),
    )
