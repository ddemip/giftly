from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            orig_slug = slugify(self.name)
            unique_slug = orig_slug
            counter = 1

            while Category.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(orig_slug, counter)
                counter += 1

            self.slug = unique_slug

        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        return reverse('category_list', args=[self.slug])

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
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
    thumbnail = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            orig_slug = slugify(self.title)
            unique_slug = orig_slug
            counter = 1

            while Product.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(orig_slug, counter)
                counter += 1

            self.slug = unique_slug

        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'products'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])

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
