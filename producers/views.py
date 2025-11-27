
from core.views import BaseViewSet
from core.permissions import IsOwnerOrStaff

from producers.models import Producer
from producers.filters import ProducerFilter
from producers.serializers import ProducerSerializer

class ProducerViewSet(BaseViewSet):
    queryset = Producer.objects.select_related("user")
    serializer_class = ProducerSerializer
    filterset_class = ProducerFilter
    ordering_fields = ['name', 'created_at']
    permission_classes = BaseViewSet.permission_classes + [IsOwnerOrStaff]
    owner_lookup_field = "user"
