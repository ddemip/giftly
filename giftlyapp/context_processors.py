from .models import Category
from .shopping_cart import ShoppingCart


def cart(request):
    return {'cart': ShoppingCart(request)}


def categories(request):
    return {'categories': Category.objects.all()}
