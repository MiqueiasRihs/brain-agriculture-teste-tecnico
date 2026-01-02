import random

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError

from core.factories import UserFactory
from cultivation.factories import FarmCropFactory
from farm.factories import FarmFactory
from producers.factories import ProducerFactory


class Command(BaseCommand):
    help = "Popula o banco gerando registros de FarmCrop com dados sintéticos."

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Quantidade de produtores e seus respectivos FarmCrops a serem gerados",
        )

    def handle(self, *args, **options):
        producer_count = options["count"]
        if producer_count < 1:
            raise CommandError("O parâmetro count deve ser um inteiro positivo.")

        self.stdout.write(
            self.style.WARNING(
                f"Gerando {producer_count} produtores com quantidades variadas de FarmCrops..."
            )
        )

        farmcrops_created = []
        with transaction.atomic():
            for i in range(producer_count):
                user = UserFactory(username=f"producer_user_{i}")
                producer = ProducerFactory(user=user)
                farms = [
                    FarmFactory(producer=producer)
                    for _ in range(random.randint(1, 2))
                ]

                target = random.randint(1, max(2, len(farms) * 2))
                produced = 0
                attempts = 0

                while produced < target and attempts < target * 5:
                    farm = random.choice(farms)
                    try:
                        farmcrops_created.append(FarmCropFactory(farm=farm))
                    except IntegrityError:
                        attempts += 1
                        continue
                    produced += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{producer_count} produtores e {len(farmcrops_created)} FarmCrops criados com sucesso."
            )
        )
