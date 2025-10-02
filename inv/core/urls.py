
from django.contrib import admin
from django.urls import path
from .views import index , logout_view
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from . import views
from .forms import LoginForm

urlpatterns = [
    path("", index , name='index'), 
    path('signup/', views.signup , name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html',authentication_form=LoginForm , redirect_authenticated_user=True,next_page='inbox') , name='login' ),
    path('logout/', logout_view, name='logout'),
    path('inbox/', views.inbox, name='inbox'),
    path('custom_redirect/', views.custom_redirect_view, name='custom_redirect'),
]
