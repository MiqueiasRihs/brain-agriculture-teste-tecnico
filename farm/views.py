from core.views import BaseViewSet

from farm.models import Farm
from farm.filters import FarmFilter
from farm.serializers import FarmSerializer


class FarmViewSet(BaseViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    filterset_class = FarmFilter
    ordering_fields = ['name', 'created_at']