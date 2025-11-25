from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('producers/', include("producers.urls")),
    path('farm/', include("farm.urls")),
    
]
