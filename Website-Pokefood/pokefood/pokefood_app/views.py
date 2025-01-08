from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import LoginRecord
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
# Create your views here.


def index(request):
    return render(request, 'pokefood_app/index.html')

def about(request):
    return render(request, 'pokefood_app/about.html')

def book(request):
    return render(request, 'pokefood_app/book.html') 

def menu(request):
    return render(request, 'pokefood_app/menu.html')


#def login(request):
#    return render(request, 'pokefood_app/login.html')

def register(request):
    return render(request, 'pokefood_app/register.html')

def login_view(request):
    if request.user.is_authenticated:  # Redirect if already logged in
        return redirect('index')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()  # Authenticate user
            login(request, user)  # Log the user in

            # Record login details
            ip = get_client_ip(request)
            LoginRecord.objects.create(user=user, ip_address=ip)

            # Check if user exists in the database
            if User.objects.filter(username=user.username).exists():
                return redirect('index')  # Redirect to homepage
    else:
        form = AuthenticationForm()

    return render(request, 'pokefood_app/login.html', {'form': form})

def get_client_ip(request):
    """Helper function to get client IP address."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def register(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email is already registered')
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=full_name)
                user.save()
                messages.success(request, 'Registration successful')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'pokefood_app/register.html')


def logout_view(request):
    logout(request)
    return redirect('login') 

@staff_member_required
def login_records_view(request):
    records = LoginRecord.objects.all()
    return render(request, 'pokefood_staff/staff.html', {'records': records})
