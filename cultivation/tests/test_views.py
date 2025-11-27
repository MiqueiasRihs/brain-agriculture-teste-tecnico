import pytest
from django.urls import reverse
from rest_framework import status

from cultivation.models import Crop, HarvestSeason, FarmCrop


pytestmark = pytest.mark.django_db


def test_list_crops_returns_paginated_response(api_client, crop, other_crop):
    url = reverse("crop-list")

    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert {item["name"] for item in response.data["results"]} == {
        crop.name,
        other_crop.name,
    }


def test_create_crop(api_client):
    url = reverse("crop-list")
    payload = {
        "name": "Cana de Açúcar",
        "code": "CANA-2024",
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Crop.objects.filter(name="Cana de Açúcar").exists()


def test_filter_crops_by_name(api_client):
    Crop.objects.create(name="Soja", code="SOJA")
    Crop.objects.create(name="Milho", code="MILHO")

    url = reverse("crop-list")
    response = api_client.get(url, {"name": "soj"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Soja"


def test_create_harvest_season(api_client):
    url = reverse("harvestseason-list")
    payload = {"name": "Safra 2024/2025", "start_year": 2024, "end_year": 2025}

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert HarvestSeason.objects.filter(name="Safra 2024/2025").exists()


def test_create_harvest_season_invalid_years(api_client):
    url = reverse("harvestseason-list")
    payload = {"name": "Safra 2025/2024", "start_year": 2025, "end_year": 2024}

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "end_year" in response.data


def test_list_farm_crops_can_be_filtered(api_client, farm, harvest_season, crop, other_crop):
    FarmCrop.objects.create(farm=farm, harvest_season=harvest_season, crop=crop)
    FarmCrop.objects.create(farm=farm, harvest_season=harvest_season, crop=other_crop)

    url = reverse("farmcrop-list")
    response = api_client.get(url, {"crop": str(other_crop.id)})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert str(response.data["results"][0]["crop"]) == str(other_crop.id)


def test_create_farm_crop(api_client, farm, harvest_season, crop):
    url = reverse("farmcrop-list")
    payload = {
        "farm": str(farm.id),
        "harvest_season": str(harvest_season.id),
        "crop": str(crop.id),
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert FarmCrop.objects.filter(farm=farm, harvest_season=harvest_season, crop=crop).exists()


def test_prevent_duplicate_farm_crop(api_client, farm_crop, farm, harvest_season, crop):
    url = reverse("farmcrop-list")
    payload = {
        "farm": str(farm.id),
        "harvest_season": str(harvest_season.id),
        "crop": str(crop.id),
    }

    response = api_client.post(url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response.data
