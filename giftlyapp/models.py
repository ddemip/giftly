from django.db import models
from django.urls import reverse


class User(models.Model):
    email = models.CharField(max_lenght=255)
    password = models.CharField(max_lenght=64)
    first_name = models.CharField(max_lenght=255)
    last_name = models.CharField(max_lenght=255)
    role = models.CharField(max_lenght=10)

    def __str__(self):
        return self.user_id

    def get_absolute_url(self):
        return reverse("user_detail", args=[str(self.pk)])


class Customer(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    session_uuid = models.CharField(max_lenght=255)

    def __str__(self):
        return self.customer_id

    def get_absolute_url(self):
        return reverse("customer_detail", args=[str(self.pk)])

class Shopping_cart(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.shopping_card_id

    def get_absolute_url(self):
        return reverse("user_detail", args=[str(self.pk)])


class Order(models.Model):
    customer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    shopping_cart_id = models.ForeignKey(User, on_delete=models.CASCADE)
    recipient_email = models.CharField(max_lenght=255)








