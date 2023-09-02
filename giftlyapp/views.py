from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, Category, Order, PaymentDetail, ShoppingCartItem, Customer
from .forms import UserProfileUpdateForm, UserCreationForm, CheckoutForm
from .shopping_cart import ShoppingCart as CustomShoppingCart
from .forms import ShoppingCartAddProductForm, AddToCartForm
from django.core.paginator import Paginator
from random import sample
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Kasutaja {user} on loodud')
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
            messages.info(request, 'Kasutajanimi VÕI parool on vale')
    context = {}
    return render(request, 'registration/login.html', context)


def user_logout(request):
    logout(request)
    messages.success(request, "Oled välja logitud")
    return redirect("home")


def home(request):
    all_products_list = Product.objects.all()

    num_random_products = min(6, len(all_products_list))
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


@login_required
def user_profile_view(request):
    user = request.user
    user_form = UserProfileUpdateForm(instance=user)

    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profiil on edukalt uuendatud!')

    context = {
        'user_form': user_form,
        'user': user,
    }
    return render(request, 'profile.html', context)


@login_required
def profile(request):
    user_form = UserProfileUpdateForm(instance=request.user)
    user_orders = Order.objects.filter(customer__user=request.user).order_by('-date')

    if request.method == 'POST':
        user_form = UserProfileUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Profiil on edukalt uuendatud!')

    context = {
        'user_form': user_form,
        'user_orders': user_orders
    }
    return render(request, 'profile.html', context)


@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profiil on edukalt uuendatud!')
            return redirect('profile')
    else:
        form = UserProfileUpdateForm(instance=request.user)

    context = {'form': form}
    return render(request, 'update_profile.html', context)


@login_required
@require_POST
def cart_add(request, product_id):
    # Retrieve the product and form data
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))  # Get the quantity from the form data

    # Add or update the item in the cart
    cart = CustomShoppingCart(request)
    cart.add(product=product, quantity=quantity, update_quantity=True)

    return redirect('cart_view')


@login_required
def cart_remove(request, product_id):
    cart = CustomShoppingCart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    user_id = request.user.id  # Extract the user's ID
    cart_items = ShoppingCartItem.objects.filter(shopping_cart__user=user_id)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    for item in cart_items:
        item.update_quantity_form = ShoppingCartAddProductForm(
            initial={'quantity': item.quantity, 'update': True}
        )
    return render(request, 'cart/detail.html', {'cart_items': cart_items, 'total_price': total_price})


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


def search_products(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )
        context = {'products': products, 'query': query}
    else:
        context = {}

    return render(request, 'search_result.html', context)


@login_required
def checkout(request):
    cart = CustomShoppingCart(request)
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Create an order
            user = request.user if request.user.is_authenticated else None
            customer = None
            if user:
                customer, created = Customer.objects.get_or_create(user=user)

            order = Order(
                customer=customer,
                sender_name=form.cleaned_data['sender_name'],
                sender_email=form.cleaned_data['sender_email'],
                is_gift=form.cleaned_data['is_gift'],
                gift_recipient_name=form.cleaned_data['gift_recipient_name']
                if form.cleaned_data['is_gift'] else form.cleaned_data['sender_name'],
                recipient_email=form.cleaned_data['recipient_email']
                if form.cleaned_data['is_gift'] else form.cleaned_data['sender_email'],
                total_cost=cart.get_total_price()
            )
            order.save()

            # Create order items and associate them with the order
            for item in cart:
                order_item = ShoppingCartItem(order=order, product=item['product'], quantity=item['quantity'])
                order_item.save()

            # Create payment detail (you may need to handle payment processing here)
            payment_detail = PaymentDetail(
                order=order,
                payment_method=form.cleaned_data['payment_method'],
                status='Pending'  # You can set the initial payment status here
            )
            payment_detail.save()

            # Clear the shopping cart
            cart.clear()

            # Redirect to the order confirmation page
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm()

    context = {'cart': cart, 'form': form}
    return render(request, 'cart/checkout.html', context)


@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Ensure that the user has permission to view this order (e.g., if they are logged in)
    if request.user.is_authenticated and (request.user == order.customer.user):
        # New list from items
        shoppingcart_items = list(order.shoppingcartitem_set.all())
        # Add the total price as an attribute to each item
        for item in shoppingcart_items:
            item.total_price = item.quantity * item.product.price

        context = {'order': order, 'shoppingcart_items': shoppingcart_items}
        return render(request, 'cart/order_confirmation.html', context)
    else:
        # Handle unauthorized access to the order confirmation page
        messages.error(request, 'Ligipääs puudub.')
        return redirect('home')


@login_required
def update_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Parool on edukalt uuendatud!')
            return redirect('profile')
        else:
            messages.error(request, 'Palun paranda vead.')
    else:
        form = PasswordChangeForm(request.user)

    context = {'form': form}
    return render(request, 'update_password.html', context)


@login_required
def check_orders(request):
    user = request.user
    try:
        customer = Customer.objects.get(user=user)
    except Customer.DoesNotExist:
        customer = None

    if customer:
        orders = Order.objects.filter(customer=customer)
    else:
        orders = []

    context = {
        'user': user,
        'orders': orders,
    }

    return render(request, 'check_orders.html', context)


def info(request):
    return render(request, "info.html")


def add_to_cart(request, product_id):
    # Retrieve the product and form data
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)  # Create an instance of your form

        if form.is_valid():
            quantity = form.cleaned_data['quantity']

            # Add or update the item in the cart
            cart = CustomShoppingCart(request)
            cart.add(product=product, quantity=quantity, update_quantity=True)

            # Render the same product_detail.html template with the form and a success message
            context = {
                'product': product,
                'cart_product_form': form,  # Include your form here
                'product_added_to_cart': True,  # Add a flag to indicate success
            }

            return render(request, 'product_detail.html', context)

    # Handle GET requests or form validation errors
    else:
        form = AddToCartForm(initial={'quantity': 1})  # Create a form with initial data

    # Render the product_detail.html template with the form
    context = {
        'product': product,
        'cart_product_form': form,
    }

    return render(request, 'product_detail.html', context)
