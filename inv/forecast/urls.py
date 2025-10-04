from django.urls import path
from . views import forecast_trend_view , restock_status_view
app_name = 'forecast'
urlpatterns = [
    path("trend/", forecast_trend_view, name="forecast_trend"),
    path("status/", restock_status_view, name="forecast_status"),
]
