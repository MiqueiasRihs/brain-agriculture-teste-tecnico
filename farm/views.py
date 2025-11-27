from core.views import BaseViewSet
from core.permissions import IsOwnerOrStaff

from farm.models import Farm
from farm.filters import FarmFilter
from farm.serializers import FarmSerializer


class FarmViewSet(BaseViewSet):
    queryset = Farm.objects.select_related("producer__user")
    serializer_class = FarmSerializer
    filterset_class = FarmFilter
    ordering_fields = ['name', 'created_at']
    permission_classes = BaseViewSet.permission_classes + [IsOwnerOrStaff]
    owner_lookup_field = "producer__user"
