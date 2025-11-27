from rest_framework.routers import SimpleRouter

from cultivation.views import CropViewSet, HarvestSeasonViewSet, FarmCropViewSet


router = SimpleRouter()
router.register(r"crops", CropViewSet)
router.register(r"harvest-seasons", HarvestSeasonViewSet)
router.register(r"farm-crops", FarmCropViewSet)

urlpatterns = router.urls
