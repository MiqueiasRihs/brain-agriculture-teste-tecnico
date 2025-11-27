import random

import factory
from factory.django import DjangoModelFactory

from producers.models import Producer


def _calculate_cpf_digit(digits):
    weight_sequence = range(len(digits) + 1, 1, -1)
    total = sum(digit * weight for digit, weight in zip(digits, weight_sequence))
    remainder = total % 11
    return 0 if remainder < 2 else 11 - remainder


def _generate_valid_cpf():
    base_numbers = [random.randint(0, 9) for _ in range(9)]
    if len(set(base_numbers)) == 1:
        base_numbers[0] = (base_numbers[0] + 1) % 10

    base_numbers.append(_calculate_cpf_digit(base_numbers))
    base_numbers.append(_calculate_cpf_digit(base_numbers))

    return "".join(str(digit) for digit in base_numbers)


def _generate_unique_cpf():
    while True:
        cpf = _generate_valid_cpf()
        if not Producer.objects.filter(document=cpf).exists():
            return cpf


class ProducerFactory(DjangoModelFactory):
    class Meta:
        model = Producer

    name = factory.Faker("name")
    document_type = "CPF"
    document = factory.LazyFunction(_generate_unique_cpf)
