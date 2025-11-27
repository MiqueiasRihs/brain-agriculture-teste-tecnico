from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from brain_agriculture.views import DashboardView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    
    path("api/auth/", include("core.auth_urls")),

    path('api/', include("producers.urls"), name="producers"),
    path('api/', include("farm.urls"), name="farm"),
    path('api/', include("cultivation.urls"), name="cultivation"),
    
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
]
