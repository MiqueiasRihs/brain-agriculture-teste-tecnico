from decimal import Decimal
import random

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory

from core.choices import States
from farm.models import Farm
from producers.factories import ProducerFactory


CITY_STATE_CHOICES = [
    ("São Paulo", States.SP),
    ("Belo Horizonte", States.MG),
    ("Curitiba", States.PR),
    ("Porto Alegre", States.RS),
    ("Goiânia", States.GO),
]


class FarmFactory(DjangoModelFactory):
    class Meta:
        model = Farm

    class Params:
        city_state_choice = factory.LazyFunction(lambda: random.choice(CITY_STATE_CHOICES))

    producer = factory.SubFactory(ProducerFactory)
    name = factory.Faker("company")
    city = factory.LazyAttribute(lambda obj: obj.city_state_choice[0])
    state = factory.LazyAttribute(lambda obj: obj.city_state_choice[1])
    total_area_ha = fuzzy.FuzzyDecimal(10, 1000, precision=2)
    arable_area_ha = factory.LazyAttribute(lambda obj: (obj.total_area_ha * Decimal("0.6")).quantize(Decimal("0.01")))
    vegetation_area_ha = factory.LazyAttribute(lambda obj: (obj.total_area_ha - obj.arable_area_ha).quantize(Decimal("0.01")))
