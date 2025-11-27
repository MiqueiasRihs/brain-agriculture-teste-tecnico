from farm.models import Farm
from core.choices import States
from cultivation.models import Crop, HarvestSeason, FarmCrop
from producers.factories import ProducerFactory

import pytest
from decimal import Decimal


@pytest.fixture
def producer(user_factory):
    return ProducerFactory(
        name="Produtor Teste",
        document="28753163036",
        user=user_factory(),
    )


@pytest.fixture
def farm(producer):
    return Farm.objects.create(
        producer=producer,
        name="Fazenda Teste",
        city="Contagem",
        state=States.MG,
        total_area_ha=Decimal("120.50"),
        arable_area_ha=Decimal("80.00"),
        vegetation_area_ha=Decimal("40.50"),
    )


@pytest.fixture
def crop():
    return Crop.objects.create(name="Soja", code="SOJA-001")


@pytest.fixture
def other_crop():
    return Crop.objects.create(name="Milho", code="MILHO-001")


@pytest.fixture
def harvest_season():
    return HarvestSeason.objects.create(
        name="Safra 2024/2025",
        start_year=2024,
        end_year=2025,
    )


@pytest.fixture
def farm_crop(farm, harvest_season, crop):
    return FarmCrop.objects.create(
        farm=farm,
        harvest_season=harvest_season,
        crop=crop,
    )
