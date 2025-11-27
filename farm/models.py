from django.db import models
from django.core.exceptions import ValidationError

from core.choices import States
from core.models import BaseModel
from producers.models import Producer


class Farm(BaseModel):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name="farms")
    name = models.CharField("Nome", max_length=255)
    city = models.CharField("Cidade", max_length=150)
    state = models.CharField("Estado", max_length=2, choices=States.choices)
    total_area_ha = models.DecimalField("Área total (ha)", max_digits=12, decimal_places=2)
    arable_area_ha = models.DecimalField("Área agricultável (ha)", max_digits=12, decimal_places=2)
    vegetation_area_ha = models.DecimalField("Área de vegetação (ha)", max_digits=12, decimal_places=2)

    class Meta:
        db_table = "farms"
        verbose_name = "Fazenda"
        verbose_name_plural = "Fazendas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.state})"
    
    def clean(self):
        if self.arable_area_ha < 0 or self.vegetation_area_ha < 0 or self.total_area_ha < 0:
            raise ValidationError("As áreas não podem ser negativas.")

        if self.arable_area_ha + self.vegetation_area_ha > self.total_area_ha:
            raise ValidationError("A soma da área agricultável e vegetação não pode exceder a área total.")

    def save(self, *args, **kwargs):
        self.clean()
        return super().save(*args, **kwargs)