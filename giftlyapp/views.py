from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product
from .forms import UserProfileUpdateForm, CustomerProfileUpdateForm


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


def home(request):
    return render(request, "home.html")


def all_products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'all_products.html', context)


def product_detail_view(request, product_id):
    products = Product.objects.all()
    product = get_object_or_404(Product, id=product_id)
    context = {'products': products, 'product': product}
    return render(request, 'product_detail.html', context)


@login_required
def profile(request):
    user_form = UserProfileUpdateForm(instance=request.user)
    customer_form = CustomerProfileUpdateForm(instance=request.user.customer)

    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, instance=request.user)
        customer_form = CustomerProfileUpdateForm(request.POST, instance=request.user.customer)

        if user_form.is_valid() and customer_form.is_valid():
            user_form.save()
            customer_form.save()

    context = {
        'user_form': user_form,
        'customer_form': customer_form,
    }
    return render(request, 'profile.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})
