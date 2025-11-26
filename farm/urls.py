from rest_framework.routers import SimpleRouter

from farm.views import FarmViewSet

router = SimpleRouter()
router.register(r'farms', FarmViewSet)

urlpatterns = router.urls