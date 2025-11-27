import pytest

from cultivation.serializers import (
    CropSerializer,
    HarvestSeasonSerializer,
    FarmCropSerializer,
)


pytestmark = pytest.mark.django_db


def test_crop_serializer_creates_crop_successfully():
    payload = {
        "name": "Algodão",
        "code": "ALG-001",
    }

    serializer = CropSerializer(data=payload)

    assert serializer.is_valid() is True
    instance = serializer.save()
    assert instance.name == "Algodão"
    assert instance.code == "ALG-001"


def test_harvest_season_serializer_validates_year_order():
    payload = {
        "name": "Safra 2025/2024",
        "start_year": 2025,
        "end_year": 2024,
    }

    serializer = HarvestSeasonSerializer(data=payload)

    assert serializer.is_valid() is False
    assert "end_year" in serializer.errors
    assert serializer.errors['end_year'] == ["O ano de término deve ser maior ou igual ao de início."]


def test_farm_crop_serializer_accepts_new_combination(farm, harvest_season, other_crop):
    payload = {
        "farm": str(farm.id),
        "harvest_season": str(harvest_season.id),
        "crop": str(other_crop.id),
    }

    serializer = FarmCropSerializer(data=payload)

    assert serializer.is_valid() is True


def test_farm_crop_serializer_rejects_duplicate_combination(farm_crop, farm, harvest_season, crop):
    payload = {
        "farm": str(farm.id),
        "harvest_season": str(harvest_season.id),
        "crop": str(crop.id),
    }

    serializer = FarmCropSerializer(data=payload)

    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors
