from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product  # Product model missing

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"You are now logged in as {user.username}")
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


@login_required
def home(request):
    return render(request, "home.html")


def product_detail(self):
    return get_object_or_404(Gift, id=self.request.query_params['id'])


def all_products(request):
    products = Product.objects.all()  # Retrieve all products from the database
    context = {'products': products}
    return render(request, 'all_products.html', context)


def product_detail_view(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)
