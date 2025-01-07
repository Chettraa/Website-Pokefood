from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpRequest
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, 'pokefood_app/index.html')

def about(request):
    return render(request, 'pokefood_app/about.html')

def book(request):
    return render(request, 'pokefood_app/book.html') 

def menu(request):
    return render(request, 'pokefood_app/menu.html')