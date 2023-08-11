from django.db import models
from django.urls import reverse


class User(models.Model):
    user_id = models.IntegerField
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
    customer_id = models.IntegerField
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    session_uuid = models.CharField(max_lenght=255)

    def __str__(self):
        return self.customer_id

    def get_absolute_url(self):
        return reverse("customer_detail", args=[str(self.pk)])