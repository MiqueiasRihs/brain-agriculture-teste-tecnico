from django.db import models
import uuid

from brain_agriculture.utils import validate_cpf_cnpj

class Producer(models.Model):
    DOCUMENT_TYPES = [
        ("CPF", "CPF"),
        ("CNPJ", "CNPJ"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    document_type = models.CharField(max_length=4, choices=DOCUMENT_TYPES)
    document = models.CharField(max_length=18, unique=True, validators=[validate_cpf_cnpj])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "producers"
        verbose_name = "Produtor"
        verbose_name_plural = "Produtores"

    def __str__(self):
        return self.name
    
    