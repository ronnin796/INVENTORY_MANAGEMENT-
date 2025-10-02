from django.urls import path
from . import views 
app_name = "dashboard"
urlpatterns = [
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('dashboard/superuser/', views.superuser_dashboard, name='superuser_dashboard'),
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
]
