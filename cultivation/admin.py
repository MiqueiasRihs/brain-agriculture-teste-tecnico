from django.contrib import admin

from cultivation.models import Crop, HarvestSeason, FarmCrop


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "created_at")
    search_fields = ("name", "code")
    list_filter = ("is_active",)
    ordering = ("name",)


@admin.register(HarvestSeason)
class HarvestSeasonAdmin(admin.ModelAdmin):
    list_display = ("name", "start_year", "end_year", "is_active")
    search_fields = ("name",)
    list_filter = ("start_year", "end_year", "is_active")
    ordering = ("-start_year", "name")


@admin.register(FarmCrop)
class FarmCropAdmin(admin.ModelAdmin):
    list_display = ("farm", "crop", "harvest_season", "is_active")
    list_filter = ("harvest_season", "crop", "is_active")
    search_fields = ("farm__name", "crop__name")
    ordering = ("-created_at",)
