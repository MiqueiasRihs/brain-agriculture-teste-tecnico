from django.db import models

from core.models import BaseModel

class Producer(BaseModel):
    DOCUMENT_TYPES = [
        ("CPF", "CPF"),
        ("CNPJ", "CNPJ"),
    ]
    
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=4, choices=DOCUMENT_TYPES)
    document = models.CharField(max_length=18, unique=True, validators=[])

    class Meta:
        db_table = "producers"
        verbose_name = "Produtor"
        verbose_name_plural = "Produtores"

    def __str__(self):
        return self.name
    
    