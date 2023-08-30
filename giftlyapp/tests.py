from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product


class GiftlyAppTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product', price=10.00)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_product_detail_view(self):
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_login_required_views(self):
        # Ensure that certain views are accessible only to authenticated users
        login_required_views = ['profile', 'update_profile', 'cart_detail']
        for view_name in login_required_views:
            response = self.client.get(reverse(view_name))
            self.assertEqual(response.status_code, 302)  # Redirect to login page for unauthenticated users

    def test_cart_add_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 1})
        self.assertEqual(response.status_code, 302)  # Redirect after adding to cart
        self.assertEqual(self.client.session['cart'][str(self.product.id)]['quantity'], 1)

    def test_all_products_view(self):
        response = self.client.get(reverse('all_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'all_products.html')
        self.assertContains(response, self.product.name)
