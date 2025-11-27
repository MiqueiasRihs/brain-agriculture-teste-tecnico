from rest_framework import serializers

from cultivation.models import Crop, HarvestSeason, FarmCrop


class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class HarvestSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = HarvestSeason
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        
    def validate(self, attrs):
        start_year = attrs.get("start_year") or getattr(self.instance, "start_year", None)
        end_year = attrs.get("end_year") or getattr(self.instance, "end_year", None)

        if start_year and end_year and start_year > end_year:
            raise serializers.ValidationError({"end_year": "O ano de término deve ser maior ou igual ao de início."})

        return attrs


class FarmCropSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmCrop
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        
    def validate(self, attrs):
        farm = attrs.get("farm") or getattr(self.instance, "farm", None)
        harvest_season = attrs.get("harvest_season") or getattr(self.instance, "harvest_season", None)
        crop = attrs.get("crop") or getattr(self.instance, "crop", None)

        if not (farm and harvest_season and crop):
            return attrs

        existing_qs = FarmCrop.objects.filter(
            farm=farm,
            harvest_season=harvest_season,
            crop=crop,
        )

        if self.instance:
            existing_qs = existing_qs.exclude(pk=self.instance.pk)

        if existing_qs.exists():
            raise serializers.ValidationError({
                "non_field_errors": [
                    "Já existe um registro para esta combinação de fazenda, safra e cultura."
                ]
            })

        return attrs
