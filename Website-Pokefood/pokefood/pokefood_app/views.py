from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout  # Add authenticate to imports
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import LoginRecord
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm

from .form import LoginForm, RegisterForm
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
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password!")
    else:
        form = LoginForm()

    return render(request, 'pokefood_app/login.html', {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password1']
            )
            messages.success(request, "Registration successful!")
            return redirect('login')
        else:
            messages.error(request, form.errors)
    else:
        form = RegisterForm()

    return render(request, 'pokefood_app/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@staff_member_required
def login_records_view(request):
    records = LoginRecord.objects.all()
    return render(request, 'pokefood_staff/staff.html', {'records': records})
