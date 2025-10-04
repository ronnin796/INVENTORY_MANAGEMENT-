from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import   MasterProduct, Product_sales
from django.db import models
@login_required
def dashboard_redirect(request):
    """
    Redirect the user to the appropriate dashboard based on user type.
    """
    if request.user.is_superuser:
        return redirect('dashboard:superuser_dashboard')
    else:
        return redirect('dashboard:user_dashboard')


@login_required
def superuser_dashboard(request):
    """
    Superuser dashboard with inventory stats and management tools.
    """
    # Example context
    context = {
        'total_products': 120,
        'low_stock_products': 15,
        'users_count': 50,
        'recent_orders': [
            {'id': 101, 'product': 'Laptop', 'quantity': 5},
            {'id': 102, 'product': 'Mouse', 'quantity': 20},
        ]
    }
    return render(request, 'dashboard/superuser_dashboard.html', context)


@login_required
def user_dashboard(request):
    low_stock_products = MasterProduct.objects.filter(current_stock__lte=models.F('reorder_threshold'))
    recent_sales = Product_sales.objects.select_related('product').order_by('-order_date')[:10]

    context = {
        "low_stock_products": low_stock_products,
        "recent_sales": recent_sales,
    }
    return render(request, 'dashboard/user_dashboard.html', context)
