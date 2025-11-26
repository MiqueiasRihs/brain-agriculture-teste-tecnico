import django_filters

from farm.models import Farm


class FarmFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Farm
        fields = ['name', 'producer', 'city', 'state', 'is_active']