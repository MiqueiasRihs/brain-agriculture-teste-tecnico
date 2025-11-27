from rest_framework.test import APIClient

from farm.models import Farm
from core.choices import States
from producers.models import Producer
from cultivation.models import Crop, HarvestSeason, FarmCrop

import pytest
from decimal import Decimal


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def producer():
    return Producer.objects.create(
        name="Produtor Teste",
        document_type="CPF",
        document="28753163036",
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
