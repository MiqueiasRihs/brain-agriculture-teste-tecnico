from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction

from rest_framework import serializers

from core.validators.document_validator import DocumentValidatorFactory
from producers.models import Producer


User = get_user_model()


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    name = serializers.CharField(max_length=255)
    document_type = serializers.ChoiceField(choices=Producer.DOCUMENT_TYPES)
    document = serializers.CharField(max_length=18)

    def validate_username(self, value):
        username = value.strip()
        if not username:
            raise serializers.ValidationError("O nome de usuário não pode ser vazio.")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Já existe um usuário com este nome.")

        return username

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(exc.messages)
        return value

    def validate_document(self, value):
        return ''.join(filter(str.isdigit, value))

    def validate(self, attrs):
        document_type = attrs.get("document_type")
        document = attrs.get("document")

        validator = DocumentValidatorFactory.get_validator(document_type)
        if not validator.validate(document):
            raise serializers.ValidationError({
                "document": f"{document_type} inválido, por favor verifique se esta correto."
            })

        if Producer.objects.filter(document=document).exists():
            raise serializers.ValidationError({
                "document": "Já existe um produtor cadastrado com este documento."
            })

        return attrs

    def create(self, validated_data):
        user_data = {
            "username": validated_data["username"],
            "email": validated_data.get("email") or "",
        }
        password = validated_data["password"]

        producer_data = {
            "name": validated_data["name"],
            "document_type": validated_data["document_type"],
            "document": validated_data["document"],
        }

        with transaction.atomic():
            user = User.objects.create_user(password=password, **user_data)
            Producer.objects.create(user=user, **producer_data)

        return user
