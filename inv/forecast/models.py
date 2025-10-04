from django.db import models

# Create your models here.
from django.db import models
from inventory.models import MasterProduct

class ForecastResult(models.Model):
    product = models.OneToOneField(MasterProduct, on_delete=models.CASCADE, related_name="forecast_result")
    forecast_data = models.JSONField(default=list)  # store list of predictions
    predicted_stock = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Forecast for {self.product.name}"
