from django.contrib import admin

from farm.models import Farm

@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ('name', 'producer', 'city', 'state', 'updated_at')
    list_filter = ('state', 'is_active')
    search_fields = ('id', 'name', 'producer__name', 'producer__document')
    ordering = ('-updated_at',)
    readonly_fields = ('created_at', 'updated_at')