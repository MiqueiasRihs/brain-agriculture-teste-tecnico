from rest_framework import serializers

from farm.models import Farm


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
        
        
    def validate(self, attrs):
        total_area_ha = attrs.get("total_area_ha") or getattr(self.instance, "total_area_ha", None)
        arable_area_ha = attrs.get("arable_area_ha") or getattr(self.instance, "arable_area_ha", None)
        vegetation_area_ha = attrs.get("vegetation_area_ha") or getattr(self.instance, "vegetation_area_ha", None)

        if arable_area_ha < 0 or vegetation_area_ha < 0 or total_area_ha < 0:
            raise serializers.ValidationError("As áreas não podem ser negativas.")

        if arable_area_ha + vegetation_area_ha > total_area_ha:
            raise serializers.ValidationError("A soma da área agricultável e vegetação não pode exceder a área total.")

        return attrs