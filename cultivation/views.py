from core.views import BaseViewSet
from core.permissions import IsOwnerOrStaff

from cultivation.models import Crop, HarvestSeason, FarmCrop
from cultivation.serializers import (
    CropSerializer,
    HarvestSeasonSerializer,
    FarmCropSerializer,
)
from cultivation.filters import CropFilter, HarvestSeasonFilter, FarmCropFilter


class CropViewSet(BaseViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    filterset_class = CropFilter
    ordering_fields = ["name", "created_at"]


class HarvestSeasonViewSet(BaseViewSet):
    queryset = HarvestSeason.objects.all()
    serializer_class = HarvestSeasonSerializer
    filterset_class = HarvestSeasonFilter
    ordering_fields = ["name", "start_year", "created_at"]


class FarmCropViewSet(BaseViewSet):
    queryset = FarmCrop.objects.select_related("farm", "harvest_season", "crop")
    serializer_class = FarmCropSerializer
    filterset_class = FarmCropFilter
    ordering_fields = ["created_at"]
    permission_classes = BaseViewSet.permission_classes + [IsOwnerOrStaff]
    owner_lookup_field = "farm__producer__user"
