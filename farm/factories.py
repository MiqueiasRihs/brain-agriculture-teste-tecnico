from decimal import Decimal

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from core.choices import States
from farm.models import Farm
from producers.factories import ProducerFactory


def _state_choices():
    return [choice[0] for choice in States.choices]


class FarmFactory(DjangoModelFactory):
    class Meta:
        model = Farm

    producer = factory.SubFactory(ProducerFactory)
    name = factory.Faker("company")
    city = factory.Faker("city")
    state = fuzzy.FuzzyChoice(_state_choices())
    total_area_ha = fuzzy.FuzzyDecimal(10, 1000, precision=2)
    arable_area_ha = factory.LazyAttribute(lambda obj: (obj.total_area_ha * Decimal("0.6")).quantize(Decimal("0.01")))
    vegetation_area_ha = factory.LazyAttribute(lambda obj: (obj.total_area_ha - obj.arable_area_ha).quantize(Decimal("0.01")))
