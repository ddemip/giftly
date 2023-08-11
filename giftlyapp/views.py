from django.shortcuts import render
from .models import Product  # Product model missing


def all_products(request):
    products = Product.objects.all()  # Retrieve all products from the database
    context = {'products': products}
    return render(request, 'all_products.html', context)


def product_detail_view(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {'product': product}
    return render(request, 'product_detail.html', context)
