from rest_framework.routers import SimpleRouter

from producers.views import ProducerViewSet

router = SimpleRouter()
router.register(r'producers', ProducerViewSet)

urlpatterns = router.urls