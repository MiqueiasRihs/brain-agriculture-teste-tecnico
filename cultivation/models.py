from django.db import models
from django.core.exceptions import ValidationError

from core.models import BaseModel
from farm.models import Farm


class Crop(BaseModel):
    name = models.CharField("Nome", max_length=100, unique=True)
    code = models.CharField("Código", max_length=50, unique=True, null=True, blank=True)

    class Meta:
        db_table = "crop"
        verbose_name = "Colheita"
        verbose_name_plural = "Colheitas"
        ordering = ["name"]

    def __str__(self):
        return self.name


class HarvestSeason(BaseModel):
    name = models.CharField("Nome", max_length=50)

    start_year = models.PositiveIntegerField("Ano de início da safra", null=True, blank=True)
    end_year = models.PositiveIntegerField("Ano de término da safra", null=True, blank=True)

    class Meta:
        db_table = "harvest_seasons"
        verbose_name = "Safra agrícola"
        verbose_name_plural = "Safras agrícolas"
        ordering = ["-start_year", "name"]

    def __str__(self):
        return self.name

    def clean(self):
        if self.start_year and self.end_year and self.start_year > self.end_year:
            raise ValidationError({"end_year": "O ano de término deve ser maior ou igual ao de início."})
        return super().clean()
    
    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)


class FarmCrop(BaseModel):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="farm_crop")
    harvest_season = models.ForeignKey(HarvestSeason, on_delete=models.PROTECT, related_name="farm_crop")
    crop = models.ForeignKey(Crop, on_delete=models.PROTECT, related_name="farm_crop")

    class Meta:
        db_table = "farm_crop"
        verbose_name = "Cultivo Agrícola"
        verbose_name_plural = "Cultivos Agrícolas"
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=["farm", "harvest_season", "crop"],
                name="unique_farm_harvest_crop",
            ),
        ]

    def __str__(self):
        return f"{self.farm.name} - {self.crop.name} - {self.harvest_season.name}"
