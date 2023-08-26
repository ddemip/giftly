from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


def generate_unique_slug(model, field_name, value, max_length=255):
    orig_slug = slugify(value)[:max_length]
    unique_slug = orig_slug
    counter = 1

    while model.objects.filter(**{field_name: unique_slug}).exists():
        unique_slug = f"{orig_slug}-{counter}"
        counter += 1

    return unique_slug


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Category, 'slug', self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    session_uuid = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.session_uuid

    def get_absolute_url(self):
        return reverse("customer_detail", args=[str(self.pk)])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, db_index=True, blank=True, null=True)
    slug = models.SlugField(max_length=150, db_index=True, unique=True, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    thumbnail = models.ImageField(upload_to='products/', blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(Product, 'slug', self.name, max_length=150)
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'products'
        ordering = ('name',)
        index_together = (('id', 'slug'), )

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    product_quantity = models.PositiveSmallIntegerField(default=0, blank=True, null=True)
    created_timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'Basket for {self.user.username} and product: {self.product.name}'


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True)
    basket_id = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, blank=True, null=True)
    recipient_email = models.CharField(max_length=255, blank=True, null=True)
    total_cost = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    date = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.total_cost)


class PaymentDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
    payment_method = models.CharField(max_length=64, blank=True, null=True)
    status = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.status
