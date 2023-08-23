from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Customer, ShoppingCart, Product
from .forms import UserProfileUpdateForm, CustomerProfileUpdateForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth.models import User


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for: {user}')
            return redirect('login')

    context = {'form': form}
    return render(request, "registration/register.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, 'username OR password is incorrect')
    context = {}
    return render(request, 'registration/login.html', context)


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


def product_detail_view(request, slug):
    products = Product.objects.all()
    product = get_object_or_404(Product, slug=slug)
    context = {'products': products, 'product': product}
    return render(request, 'product_detail.html', context)


def cart_view(request):
    customer = None

    if request.user.is_authenticated:
        try:
            customer = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            pass

    cart_items = []
    if customer:
        cart_items = ShoppingCart.objects.filter(customer=customer)

    context = {
        'cart_items': cart_items
    }

    return render(request, 'shopping_cart.html', context)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'


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

    context = {'form': form}
    return render(request, 'update_profile.html', context)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user
