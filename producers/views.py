
from core.views import BaseViewSet

from producers.models import Producer
from producers.filters import ProducerFilter
from producers.serializers import ProducerSerializer

class ProducerViewSet(BaseViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    filterset_class = ProducerFilter
    ordering_fields = ['name', 'created_at']