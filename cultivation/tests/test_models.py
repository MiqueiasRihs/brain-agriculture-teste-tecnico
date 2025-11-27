from django.db import IntegrityError
from django.core.exceptions import ValidationError

from cultivation.models import HarvestSeason, FarmCrop

import pytest


pytestmark = pytest.mark.django_db


def test_harvest_season_allows_equal_years():
    season = HarvestSeason.objects.create(
        name="Safra 2023/2023",
        start_year=2023,
        end_year=2023,
    )

    assert season.start_year == 2023
    assert HarvestSeason.objects.count() == 1


def test_harvest_season_invalid_end_year_raises_validation_error():
    season = HarvestSeason(
        name="Safra 2025/2024",
        start_year=2025,
        end_year=2024,
    )

    with pytest.raises(ValidationError):
        season.full_clean()


def test_farm_crop_unique_constraint(farm_crop, farm, harvest_season, crop):
    with pytest.raises(IntegrityError):
        FarmCrop.objects.create(
            farm=farm,
            harvest_season=harvest_season,
            crop=crop,
        )
