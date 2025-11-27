from decimal import Decimal

from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView

from core.choices import States
from cultivation.models import FarmCrop
from farm.models import Farm


class DashboardView(TemplateView):
    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        farms = Farm.objects.all()

        context["total_farms"] = farms.count()

        totals = farms.aggregate(
            total_area=Coalesce(Sum("total_area_ha"), Value(Decimal("0"))),
            arable_area=Coalesce(Sum("arable_area_ha"), Value(Decimal("0"))),
            vegetation_area=Coalesce(Sum("vegetation_area_ha"), Value(Decimal("0"))),
        )
        
        context["total_area_ha"] = totals["total_area"]

        state_display = dict(States.choices)
        state_counts = farms.values("state").annotate(total=Count("id")).order_by("state")
        context["state_chart"] = {
            "labels": [state_display.get(item["state"], item["state"]) for item in state_counts],
            "data": [item["total"] for item in state_counts],
        }

        crop_counts = (
            FarmCrop.objects.select_related("crop")
            .values("crop__name")
            .annotate(total=Count("id"))
            .order_by("crop__name")
        )
        context["crop_chart"] = {
            "labels": [item["crop__name"] for item in crop_counts],
            "data": [item["total"] for item in crop_counts],
        }

        context["soil_chart"] = {
            "labels": ["Área agricultável", "Vegetação"],
            "data": [float(totals["arable_area"]), float(totals["vegetation_area"])],
        }

        return context
