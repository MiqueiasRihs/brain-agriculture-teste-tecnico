from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from producers.models import Producer
from core.validators.document_validator import DocumentValidatorFactory


class ProducerSerializer(serializers.ModelSerializer):
    document = serializers.CharField(validators=[
        UniqueValidator(
            queryset=Producer.objects.all(),
            message="Já existe um produtor cadastrado com este documento."
        )
    ])
    
    class Meta:
        model = Producer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
        
    def validate_document(self, value):
        return ''.join(filter(str.isdigit, value))


    def validate(self, attrs):
        document_type = attrs.get("document_type") or getattr(self.instance, "document_type", None)
        document = attrs.get("document") or getattr(self.instance, "document", None)

        validator = DocumentValidatorFactory.get_validator(document_type)
        if not validator.validate(document):
            raise serializers.ValidationError({"document": f"{document_type} inválido, por favor verifique se esta correto."})

        return attrs
