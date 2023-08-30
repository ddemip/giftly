from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import ShoppingCart, Product, Category
from .forms import UserProfileUpdateForm, CustomerProfileUpdateForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth.models import User
from .shopping_cart import ShoppingCart
from .forms import ShoppingCartAddProductForm
from django.core.paginator import Paginator
from random import sample


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


def password_change(request):
    return render(request, 'registration/pwd-reset.html')


def home(request):

    all_products_list = Product.objects.all()

    num_random_products = 6
    random_products = sample(list(all_products_list), num_random_products)

    context = {
        'random_products': random_products,
    }

    return render(request, 'home.html', context)


def product_detail_view(request, product_slug, category_slug=None):
    product = get_object_or_404(Product, slug=product_slug)

    # This checks if the product belongs to the given category, if specified.
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if product.category != category:
            raise Http404()

    cart_product_form = ShoppingCartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'product_detail.html', context)


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        return self.request.user


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


@require_POST
def cart_add(request, product_id):
    products = Product.objects.all()
    cart = ShoppingCart(request)
    product = get_object_or_404(products, id=product_id)
    form = ShoppingCartAddProductForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        cart.add(product=product,
                 quantity=clean_data['quantity'],
                 update_quantity=clean_data['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = ShoppingCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = ShoppingCart(request)
    for item in cart:
        item['update_quantity_form'] = \
            ShoppingCartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


def all_products(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 20)  # Show 20 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'all_products.html', {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
    })


""""""""""
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})
"""""""""
