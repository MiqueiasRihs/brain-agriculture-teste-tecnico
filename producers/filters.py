import django_filters

from producers.models import Producer

class ProducerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Producer
        fields = ['name', 'document_type', 'document', 'is_active']