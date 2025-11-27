from django.db import models
from django.core.exceptions import ValidationError

from core.models import BaseModel
from core.validators.document_validator import DocumentValidatorFactory

class Producer(BaseModel):
    DOCUMENT_TYPES = [
        ("CPF", "CPF"),
        ("CNPJ", "CNPJ"),
    ]
    
    name = models.CharField("Nome", max_length=255)
    document_type = models.CharField("Tipo de Documento", max_length=4, choices=DOCUMENT_TYPES)
    document = models.CharField("Documento", max_length=18, unique=True)

    class Meta:
        db_table = "producers"
        verbose_name = "Produtor"
        verbose_name_plural = "Produtores"
        ordering = ["-created_at"]
        

    def __str__(self):
        return self.name
    
    def clean(self):
        document = self.document
        document_type = self.document_type

        document_validator = DocumentValidatorFactory.get_validator(document_type)
        if not document_validator.validate(document):
            raise ValidationError({ "document": f"{document_type} inválido, por favor verifique se esta correto." })

        if not self.pk and Producer.objects.filter(document=document).exists():
            raise ValidationError({ "document": "Já existe um produtor cadastrado com este documento." })

    def save(self, *args, **kwargs):
        self.clean()
        
        self.document = ''.join(filter(str.isdigit, self.document))
        return super().save(*args, **kwargs)
    
    