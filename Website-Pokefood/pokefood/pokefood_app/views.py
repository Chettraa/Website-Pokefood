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
from .models import LoginRecord, UserProfile
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.forms import UserCreationForm
from .models import Order, OrderItem  # Import your models
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


from .form import RegisterForm
from .models import RegisterRecord

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']

            # Create the user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # Create a registration record in the database
            ip_address = get_client_ip(request)
            RegisterRecord.objects.create(user=user, email=email, ip_address=ip_address)

            messages.success(request, "Registration successful! You can now log in.")
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
@login_required
def profile(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Optionally create the profile here if it's critical
        profile = UserProfile.objects.create(user=request.user)
    return render(request, 'pokefood_app/user_profile.html', {'profile': profile})

from django.shortcuts import render
from django.http import HttpResponse

def order_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(pk__in=cart.keys()) #get all product in the cart
    total = 0
    for item_id, item_data in cart.items():
        product = Product.objects.get(pk=item_id)
        total += product.price * item_data['quantity']
    context = {'cart': cart, 'products': products, 'total': total}
    return render(request, 'pokefood_app/order.html', context)


def process_order(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            address = request.POST.get('address')

            # Get the cart from the session (assuming you're using sessions)
            cart = request.session.get('cart', {})

            if not cart:
                messages.error(request, "Your cart is empty.")
                return redirect('order')  # Redirect back to the order page

            # Create the order
            order = Order.objects.create(
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                customer_address=address,
                # Add other order fields as needed (e.g., order date, status)
            )

            total_price = 0

            # Create order items
            for item_id, item_data in cart.items():
                try:
                    # Assuming you have a Product model
                    from .models import Product  # Import your Product model
                    product = Product.objects.get(pk=item_id)
                    quantity = item_data['quantity']
                    item_price = product.price * quantity
                    total_price += item_price

                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price, #price of product at order time
                        item_price = item_price
                    )
                except Product.DoesNotExist:
                    messages.error(request, f"Product with ID {item_id} not found.")
                    order.delete() #delete order if one of the product not found
                    return redirect('order')

            order.total_price = total_price
            order.save()

            # Clear the cart after successful order
            del request.session['cart']
            messages.success(request, "Order placed successfully!")
            return redirect('index')  # Redirect to a thank you page or home

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('order')

    messages.error(request, "Invalid request")
    return redirect('order')

@staff_member_required
def login_records_view(request):
    records = LoginRecord.objects.all()
    return render(request, 'pokefood_staff/staff.html', {'records': records})
