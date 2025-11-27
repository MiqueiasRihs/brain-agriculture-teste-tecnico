import factory
from factory.django import DjangoModelFactory

from cultivation.models import Crop, HarvestSeason, FarmCrop
from farm.factories import FarmFactory


class CropFactory(DjangoModelFactory):
    class Meta:
        model = Crop

    name = factory.Sequence(lambda n: f"Cultura {n}")
    code = factory.Sequence(lambda n: f"CROP-{n:04d}")


class HarvestSeasonFactory(DjangoModelFactory):
    class Meta:
        model = HarvestSeason

    start_year = factory.Sequence(lambda n: 2020 + n)
    end_year = factory.LazyAttribute(lambda obj: obj.start_year + 1)
    name = factory.LazyAttribute(lambda obj: f"Safra {obj.start_year}/{obj.end_year}")


class FarmCropFactory(DjangoModelFactory):
    class Meta:
        model = FarmCrop

    farm = factory.SubFactory(FarmFactory)
    harvest_season = factory.SubFactory(HarvestSeasonFactory)
    crop = factory.SubFactory(CropFactory)
