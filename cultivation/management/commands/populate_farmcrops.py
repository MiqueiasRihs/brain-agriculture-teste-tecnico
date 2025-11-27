from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from cultivation.factories import FarmCropFactory


class Command(BaseCommand):
    help = "Popula o banco gerando registros de FarmCrop com dados sintéticos."

    def add_arguments(self, parser):
        parser.add_argument(
            "count",
            type=int,
            help="Quantidade de registros FarmCrop que deseja gerar",
        )

    def handle(self, *args, **options):
        count = options["count"]
        if count < 1:
            raise CommandError("O parâmetro count deve ser um inteiro positivo.")

        self.stdout.write(self.style.NOTICE(f"Gerando {count} registros de FarmCrop..."))

        with transaction.atomic():
            farm_crops = [FarmCropFactory() for _ in range(count)]

        self.stdout.write(
            self.style.SUCCESS(
                f"{len(farm_crops)} registros de FarmCrop criados com sucesso."
            )
        )
