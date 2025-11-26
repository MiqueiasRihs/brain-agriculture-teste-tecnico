from producers.models import Producer
from rest_framework import serializers


class ProducerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Producer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        