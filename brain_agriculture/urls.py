from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include("producers.urls")),
    path('api/v1/', include("farm.urls")),
    
]
