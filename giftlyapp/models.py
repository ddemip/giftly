from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_uuid = models.CharField(max_length=255)

    def __str__(self):
        return self.session_uuid

    def get_absolute_url(self):
        return reverse("customer_detail", args=[str(self.pk)])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',  on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.CharField(max_length=150, db_index=True, unique=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        index_together = (('id', 'slug'), )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id, self.slug])


class ShoppingCart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    product_quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Basket for {self.user.name}  and product : {self.product.name}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    basket_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
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
