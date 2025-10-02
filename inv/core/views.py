from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse , JsonResponse
from django.urls import reverse

def index(request):
    return render(request , 'core/landing.html', {
    "login_url": "/login",   # later replace with {% url 'login' %}
    "signup_url": "/signup",  # later replace with {% url 'signup' %}
    "logout_url": "/logout",  # later replace with {% url 'logout' %}
    "index_url": reverse("index"),
})


from django.contrib.auth.decorators import login_required
from .forms import SignupForm
# Create your views here.

from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
def logout_view(request):
    logout(request)  # clears the session
    return redirect('index')

def signup(request):
    if request.method =='POST':
        form = SignupForm(request.POST  )

        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request , 'core/signup.html', {'form':form})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def inbox(request):
    # Replace with actual message logic later
    messages = [
        {"title": "Welcome to Puddle!", "body": "Thanks for joining our platform."},
        {"title": "Item update", "body": "Your recent item listing has been approved."}
    ]
    return render(request, "core/inbox.html", {"messages": messages})

def custom_redirect_view(request):
    if request.user.is_staff:  # Check if the user is an admin (staff member)
        return redirect('/admin/')  # Redirect to the admin panel
    else:
        # If not admin, proceed to the custom panel
        return redirect('core/index.html')  # Replace with your custom panel URL