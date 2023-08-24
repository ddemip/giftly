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


def product_detail_view(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug)
    cart_product_form = ShoppingCartAddProductForm()
    return render(request, 'product_detail.html', {'product': product,
                                                    'cart_product_form': cart_product_form})


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
    print('Siin ma peaks tooteid printima')
    print(products)
    cart = ShoppingCart(request)
    product = get_object_or_404(products, id=product_id)
    form = ShoppingCartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = ShoppingCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = ShoppingCart(request)
    for item in cart:
        item['update_quantity_form'] = ShoppingCartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'all_products.html',
                  {
                      'category': category,
                      'categories': categories,
                      'products': products
                  })