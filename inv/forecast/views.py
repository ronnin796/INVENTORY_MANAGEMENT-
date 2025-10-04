from django.shortcuts import render
from inventory.models import Category, SubCategory, MasterProduct, Product_sales
from .forecast import forecast_sales
import json


def forecast_trend_view(request):
    selected_product = None
    forecast_data, forecast_labels, actual_sales, forecast_padded = [], [], [], []
    alert_message, predicted_stock = "", None

    # Filters
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("sub_category")
    product_id = request.GET.get("product")

    categories = Category.objects.all()
    subcategories = SubCategory.objects.filter(category_id=category_id) if category_id else SubCategory.objects.all()
    products = MasterProduct.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    if subcategory_id:
        products = products.filter(sub_category_id=subcategory_id)

    # Forecast
    if product_id:
        try:
            selected_product = MasterProduct.objects.get(id=product_id)
            sales_qs = Product_sales.objects.filter(product=selected_product).order_by("order_date")

            forecast_result = forecast_sales(sales_qs)

            if "error" in forecast_result:
                alert_message = forecast_result["error"]
            else:
                actual_sales = forecast_result["actual_sales"]
                forecast_data = forecast_result["forecast_data"]
                forecast_labels = forecast_result["forecast_labels"]
                forecast_padded = [None] * len(actual_sales) + forecast_data

                # Stock prediction
                total_predicted_sales = sum(forecast_data)
                predicted_stock = selected_product.current_stock - total_predicted_sales
                avg_predicted_sales = total_predicted_sales / len(forecast_data)

                if predicted_stock <= selected_product.reorder_threshold:
                    alert_message = (
                        f"Restock soon! Forecasted average sales is {avg_predicted_sales:.2f}, "
                        f"stock will drop to {predicted_stock:.2f}"
                    )
        except MasterProduct.DoesNotExist:
            alert_message = "Invalid product selected."

    return render(request, "forecast/trends.html", {
        "categories": categories,
        "subcategories": subcategories,
        "products": products,
        "selected_product": selected_product,
        "forecast_data": forecast_padded,
        "forecast_labels": forecast_labels,
        "actual_sales": actual_sales,
        "alert_message": alert_message,
        "predicted_stock": predicted_stock,
        "forecast_labels_json": json.dumps(forecast_labels),
        "actual_sales_json": json.dumps(actual_sales),
        "forecast_data_json": json.dumps(forecast_padded),
    })

from .models import ForecastResult


def restock_status_view(request):
    status_filter = request.GET.get("status", "").lower()  # "alert", "ok", or ""

    # Preload forecasts with related product info
    forecasts = ForecastResult.objects.select_related(
        "product", "product__category", "product__sub_category"
    )

    filtered_products = []
    for forecast in forecasts:
        product = forecast.product
        predicted_stock = forecast.predicted_stock

        # Attach predicted_stock for template display
        product.predicted_stock = predicted_stock

        # Filter according to status_filter
        if status_filter == "alert" and predicted_stock <= product.reorder_threshold:
            filtered_products.append(product)
        elif status_filter == "ok" and predicted_stock > product.reorder_threshold:
            filtered_products.append(product)
        elif status_filter == "":  # show all
            filtered_products.append(product)

    return render(request, "forecast/status.html", {
        "filtered_products": filtered_products,
        "selected_status": status_filter,
    })