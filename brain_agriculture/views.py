import logging
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum, Value
from django.db.models.functions import Coalesce
from django.views.generic import TemplateView

from core.choices import States
from cultivation.models import FarmCrop
from farm.models import Farm


logger = logging.getLogger("brain_agriculture.dashboard")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        farms = Farm.objects.all()
        farm_crops = FarmCrop.objects.select_related("farm__producer__user", "crop")

        if not user.is_staff:
            farms = farms.filter(producer__user=user)
            farm_crops = farm_crops.filter(farm__producer__user=user)

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

        crop_counts = farm_crops.values("crop__name").annotate(total=Count("id")).order_by("crop__name")
        context["crop_chart"] = {
            "labels": [item["crop__name"] for item in crop_counts],
            "data": [item["total"] for item in crop_counts],
        }

        context["soil_chart"] = {
            "labels": ["Área agricultável", "Vegetação"],
            "data": [float(totals["arable_area"]), float(totals["vegetation_area"])],
        }

        logger.info(
            "Dashboard accessed by user=%s total_farms=%s total_area=%s",
            getattr(user, "pk", None),
            context["total_farms"],
            context["total_area_ha"],
        )

        return context
