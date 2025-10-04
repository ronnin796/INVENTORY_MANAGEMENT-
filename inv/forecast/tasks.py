from celery import shared_task
from inventory.models import MasterProduct, Product_sales
from .models import ForecastResult
from .forecast import forecast_sales_safe  # put your ARIMA logic in utils.py

@shared_task
def update_forecasts_for_all_products(steps=7):
    products = MasterProduct.objects.all()
    for product in products:
        sales_qs = Product_sales.objects.filter(product=product).order_by("order_date")
        result = forecast_sales_safe(sales_qs, steps=steps)

        forecast_data = result.get("forecast_data", [])
        total_predicted_sales = sum(forecast_data)
        predicted_stock = product.current_stock - total_predicted_sales if forecast_data else product.current_stock

        ForecastResult.objects.update_or_create(
            product=product,
            defaults={
                "forecast_data": forecast_data,
                "predicted_stock": predicted_stock,
            },
        )
    return f"Updated forecasts for {products.count()} products"
