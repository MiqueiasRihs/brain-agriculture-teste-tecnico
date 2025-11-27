from decimal import Decimal

import pytest

from core.choices import States
from farm.models import Farm
from farm.serializers import FarmSerializer


pytestmark = pytest.mark.django_db


def build_farm_payload(producer, **overrides):
    payload = {
        "producer": str(producer.id),
        "name": "Fazenda Teste",
        "city": "Belo Horizonte",
        "state": States.MG,
        "total_area_ha": Decimal("100.00"),
        "arable_area_ha": Decimal("60.00"),
        "vegetation_area_ha": Decimal("40.00"),
    }
    payload.update(overrides)
    return payload


def test_serializer_accepts_valid_data(producer):
    serializer = FarmSerializer(data=build_farm_payload(producer))

    assert serializer.is_valid() is True
    assert serializer.validated_data["producer"] == producer


def test_serializer_rejects_negative_areas(producer):
    payload = build_farm_payload(producer, arable_area_ha=Decimal("-5.00"))

    serializer = FarmSerializer(data=payload)

    assert serializer.is_valid() is False
    assert serializer.errors["non_field_errors"][0].code == "invalid"
    assert serializer.errors["non_field_errors"][0] == "As áreas não podem ser negativas."


def test_serializer_rejects_sum_greater_than_total(producer):
    payload = build_farm_payload(
        producer,
        arable_area_ha=Decimal("80.00"),
        vegetation_area_ha=Decimal("30.00"),
    )

    serializer = FarmSerializer(data=payload)

    assert serializer.is_valid() is False
    assert serializer.errors["non_field_errors"][0].code == "invalid"
    assert (serializer.errors["non_field_errors"][0] == "A soma da área agricultável e vegetação não pode exceder a área total.")


def test_serializer_partial_update_uses_instance_values(producer):
    farm = Farm.objects.create(
        producer=producer,
        name="Fazenda Primavera",
        city="Belo Horizonte",
        state=States.MG,
        total_area_ha=Decimal("100.00"),
        arable_area_ha=Decimal("60.00"),
        vegetation_area_ha=Decimal("40.00"),
    )

    serializer = FarmSerializer(
        instance=farm,
        data={"vegetation_area_ha": Decimal("70.00")},
        partial=True,
    )

    assert serializer.is_valid() is False
    assert serializer.errors["non_field_errors"][0].code == "invalid"
    assert (serializer.errors["non_field_errors"][0] == "A soma da área agricultável e vegetação não pode exceder a área total.")

