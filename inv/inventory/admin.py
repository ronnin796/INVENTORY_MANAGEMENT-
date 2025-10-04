from django.contrib import admin
from .models import  Category, SubCategory , MasterProduct, Product_sales
# admin.py
from django.contrib import admin
from django.utils.html import format_html
from django.db.models import F
from .models import MasterProduct, Product_sales
from forecast.forecast import forecast_sales , forecast_sales_safe

from django.contrib import admin
from django.db.models import F
from .models import MasterProduct, Product_sales
from forecast.models import ForecastResult

class PredictedLowStockFilter(admin.SimpleListFilter):
    title = 'Predicted Low Stock'
    parameter_name = 'predicted_low_stock'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Will be low'),
            ('no', 'Safe'),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset

        # Preload forecasts in a single query
        forecasts = {f.product_id: f for f in ForecastResult.objects.filter(product_id__in=queryset.values_list('id', flat=True))}

        filtered_ids = []
        for product in queryset:
            forecast = forecasts.get(product.id)
            predicted_stock = forecast.predicted_stock if forecast else product.current_stock

            if self.value() == 'yes' and predicted_stock <= product.reorder_threshold:
                filtered_ids.append(product.id)
            elif self.value() == 'no' and predicted_stock > product.reorder_threshold:
                filtered_ids.append(product.id)

        return queryset.filter(id__in=filtered_ids)



class ProductSalesInline(admin.TabularInline):
    model = Product_sales
    extra = 0

    
@admin.register(MasterProduct)
class MasterProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'sub_category',
        'current_stock',
        'reorder_threshold',
        'predicted_stock_status'
    )
    list_filter = ('category', 'sub_category', PredictedLowStockFilter)
    search_fields = ('name',)

    def predicted_stock_status(self, obj):
        try:
            forecast = ForecastResult.objects.get(product=obj)
            predicted_stock = forecast.predicted_stock
        except ForecastResult.DoesNotExist:
            predicted_stock = obj.current_stock

        if predicted_stock <= obj.reorder_threshold:
            return format_html(
                '<span style="color: red;">⚠ Restock soon (predicted: {})</span>',
                predicted_stock
            )
        return format_html(
            '<span style="color: green;">✔ OK (predicted: {})</span>',
            predicted_stock
    )


    predicted_stock_status.short_description = "Predicted Stock"

    # Override to inject request into admin instance (needed for cache)
    def changelist_view(self, request, extra_context=None):
        self.request = request
        return super().changelist_view(request, extra_context)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)

@admin.register(Product_sales)
class ProductSalesAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'product', 'quantity', 'sales', 'order_date')  # ✅ All fields explicitly listed
    search_fields = ('order_id', 'product__name')
    list_filter = ('order_date','product__category', 'product__sub_category')

