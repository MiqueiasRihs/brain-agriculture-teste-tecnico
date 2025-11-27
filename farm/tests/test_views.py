from django.urls import reverse

from rest_framework import status

from farm.models import Farm
from core.choices import States
from producers.factories import ProducerFactory

import pytest
from decimal import Decimal


pytestmark = pytest.mark.django_db


@pytest.fixture
def farm_list_url():
    return reverse("farm-list")


@pytest.fixture
def farm_detail_url():
    def _build(farm):
        return reverse("farm-detail", args=[str(farm.id)])

    return _build


def create_farm(producer, **overrides):
    defaults = {
        "producer": producer,
        "name": "Fazenda Modelo",
        "city": "Belo Horizonte",
        "state": States.MG,
        "total_area_ha": Decimal("100.00"),
        "arable_area_ha": Decimal("60.00"),
        "vegetation_area_ha": Decimal("40.00"),
    }
    defaults.update(overrides)
    return Farm.objects.create(**defaults)


def test_list_farms_returns_paginated_response(api_client, farm_list_url, producer):
    second_producer = ProducerFactory(
        name="Produtor Secundário",
        document_type="CNPJ",
        document="93997567000165",
    )
    create_farm(producer=producer, name="Fazenda 1")
    create_farm(producer=second_producer, name="Fazenda 2", city="Sao Paulo", state=States.SP)

    response = api_client.get(farm_list_url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2
    assert {result["name"] for result in response.data["results"]} == {
        "Fazenda 1",
        "Fazenda 2",
    }


def test_filter_farms_by_name(api_client, farm_list_url, producer):
    create_farm(producer=producer, name="Fazenda Primavera")
    create_farm(producer=producer, name="Sítio Bom Lugar", city="Rio de Janeiro", state=States.RJ)

    response = api_client.get(farm_list_url, {"name": "primavera"})

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 1
    assert response.data["results"][0]["name"] == "Fazenda Primavera"


def test_create_farm_with_valid_payload(api_client, farm_list_url, producer):
    payload = {
        "producer": str(producer.id),
        "name": "Fazenda Aurora",
        "city": "Ouro Preto",
        "state": States.MG,
        "total_area_ha": Decimal("120.00"),
        "arable_area_ha": Decimal("80.00"),
        "vegetation_area_ha": Decimal("40.00"),
    }

    response = api_client.post(farm_list_url, payload, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Fazenda Aurora"
    assert response.data["state"] == States.MG
    assert Farm.objects.filter(name="Fazenda Aurora").exists()


def test_create_farm_rejects_invalid_area_combination(api_client, farm_list_url, producer):
    payload = {
        "producer": str(producer.id),
        "name": "Fazenda Limite",
        "city": "Florianopolis",
        "state": States.SC,
        "total_area_ha": Decimal("100.00"),
        "arable_area_ha": Decimal("70.00"),
        "vegetation_area_ha": Decimal("40.00"),
    }

    response = api_client.post(farm_list_url, payload, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (response.data["non_field_errors"][0] == "A soma da área agricultável e vegetação não pode exceder a área total.")


def test_update_farm_changes_requested_fields(api_client, farm_detail_url, producer):
    farm = create_farm(producer=producer)

    response = api_client.patch(farm_detail_url(farm), {"city": "Ipatinga"}, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert response.data["city"] == "Ipatinga"
    farm.refresh_from_db()
    assert farm.city == "Ipatinga"


def test_partial_update_with_invalid_areas_returns_error(api_client, farm_detail_url, producer):
    farm = create_farm(producer=producer)

    response = api_client.patch(farm_detail_url(farm), {"vegetation_area_ha": "80.00"}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert (response.data["non_field_errors"][0] == "A soma da área agricultável e vegetação não pode exceder a área total.")
