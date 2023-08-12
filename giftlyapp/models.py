from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# class GiftUser(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     email = models.CharField(max_length=255)
#     password = models.CharField(max_length=64)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     role = models.CharField(max_length=10)
#
#     def __str__(self):
#         return self.user
#
#     def get_absolute_url(self):
#         return reverse("user_detail", args=[str(self.pk)])

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    session_uuid = models.CharField(max_length=255)

    def __str__(self):
        return self.session_uuid

    def get_absolute_url(self):
        return reverse("customer_detail", args=[str(self.pk)])

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.title


class ShoppingCart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    product_quantity = models.IntegerField()

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shopping_cart_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
    recipient_email = models.CharField(max_length=255)
    total_cost = models.DecimalField(max_digits=7, decimal_places=2)
    date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.total_cost


class PaymentDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=64)
    status = models.CharField(max_length=10)

    def __str__(self):
        return self.status











