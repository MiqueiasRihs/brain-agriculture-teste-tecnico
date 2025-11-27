from django.core.exceptions import ValidationError

from farm.models import Farm
from core.choices import States

from decimal import Decimal

import pytest


pytestmark = pytest.mark.django_db


def test_create_farm_with_valid_areas(producer):
    farm = Farm.objects.create(
        producer=producer,
        name="Fazenda Primavera",
        city="Contagem",
        state=States.MG,
        total_area_ha=Decimal("100.00"),
        arable_area_ha=Decimal("60.00"),
        vegetation_area_ha=Decimal("40.00"),
    )

    assert farm.name == "Fazenda Primavera"
    assert farm.total_area_ha == (farm.arable_area_ha + farm.vegetation_area_ha)
    assert Farm.objects.count() == 1


def test_farm_negative_area_validation(producer):
    farm = Farm(
        producer=producer,
        name="Fazenda Inválida",
        city="Belo Horizonte",
        state=States.MG,
        total_area_ha=Decimal("100.00"),
        arable_area_ha=Decimal("-10.00"),
        vegetation_area_ha=Decimal("40.00"),
    )

    with pytest.raises(ValidationError) as exc:
        farm.full_clean()

    assert "As áreas não podem ser negativas." in str(exc.value)


def test_farm_area_sum_cannot_exceed_total(producer):
    with pytest.raises(ValidationError) as exc:
        Farm.objects.create(
            producer=producer,
            name="Fazenda Limite",
            city="Sao Paulo",
            state=States.SP,
            total_area_ha=Decimal("100.00"),
            arable_area_ha=Decimal("70.00"),
            vegetation_area_ha=Decimal("40.00"),
        )

    assert ("A soma da área agricultável e vegetação não pode exceder a área total." in str(exc.value))
    assert Farm.objects.count() == 0
