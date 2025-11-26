from rest_framework import serializers

from producers.models import Producer


class ProducerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Producer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


    def create(self, validated_data):
        return Producer.objects.create(**validated_data)
    
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    
    def destroy(self, instance):
        instance.is_active = False
        instance.save()
        return instance
