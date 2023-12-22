from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from .models import Product, Cart
from django.http import JsonResponse


def base(request):
  return render (request, 'base.html')

def SignupPage(request):
  if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        pass1 = request.POST.get('password')
        pass2 = request.POST.get('confirm_password')

        if pass1 == pass2:
            existing_user = User.objects.filter(username=uname).exists()
            if not existing_user:
                my_user = User.objects.create_user(username=uname, email=email, password=pass1)
                UserProfile.objects.create(user=my_user, firstname=firstname, lastname=lastname)
                return redirect('login')
            else:
                return render(request, 'signup.html', {'error_message': 'Username already exists'})
        else:
            print("Passwords do not match")
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})

  return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success (request, ('You were logged out.'))
    return redirect('base')

@login_required
def user_home(request):
    return render(request, 'home.html')

def product(request):
    return render(request, 'product.html')

def upload_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')

        product = Product.objects.create(
            name=name,
            description=description,
            price=price,
            image=image
        )
        product.save()

        return redirect('product_list')  # Redirect to the product list page

    return render(request, 'product.html')
def product_list(request):
    latest_products = Product.objects.all().order_by('-id')[:15]  # Fetch the latest 5 products
    return render(request, 'home.html', {'latest_products': latest_products})

def view_cart(request):
    user_cart = Cart.objects.get_or_create(user=request.user)[0]
    products_in_cart = user_cart.products.all()

    # Calculate the total price of all products in the cart
    total_price = sum(product.price for product in products_in_cart)

    return render(request, 'cart.html', {'products_in_cart': products_in_cart, 'total_price': total_price})

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user_cart = Cart.objects.get_or_create(user=request.user)[0]
    user_cart.products.add(product)

    return redirect('home')

def purchase_cart(request):
    user_cart = Cart.objects.get_or_create(user=request.user)[0]
    user_cart.products.clear()  # Clear the products in the cart after purchase
    purchase_message = "Item(s) purchased."

    return render(request, 'cart.html', {'products_in_cart': [], 'total_price': 0, 'purchase_message': purchase_message})