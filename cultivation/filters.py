import django_filters

from cultivation.models import Crop, HarvestSeason, FarmCrop


class CropFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Crop
        fields = ["name", "code", "is_active"]


class HarvestSeasonFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = HarvestSeason
        fields = ["name", "start_year", "end_year", "is_active"]


class FarmCropFilter(django_filters.FilterSet):
    class Meta:
        model = FarmCrop
        fields = ["farm", "harvest_season", "crop", "is_active"]
