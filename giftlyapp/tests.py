from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Product, Category, ShoppingCart, Order, Customer


class UserRegistrationTest(TestCase):
    def test_user_registration_success(self):
        response = self.client.post('/register/', {
            'username': 'testuser',
            'password1': 'securepassword',
            'password2': 'securepassword',
            # Include other required fields in the registration form
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertEqual(User.objects.count(), 1)  # One user should be created

    def test_user_registration_failure(self):
        response = self.client.post('/register/', {
            'username': 'testuser',
            'password1': 'password',
            'password2': 'password',
            # Include other required fields in the registration form
        })
        self.assertEqual(response.status_code, 200)  # Registration form should be displayed
        self.assertEqual(User.objects.count(), 0)  # No user should be created


class UserLoginLogoutTest(TestCase):
    def setUp(self):
        # Create a user for testing login
        self.user = User.objects.create_user(
            username='testuser',
            password='securepassword',
        )

    def test_user_login_success(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'securepassword',
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful login
        self.assertRedirects(response, reverse('home'))  # Use reverse to get the URL name for 'home'

    def test_user_login_failure(self):
        response = self.client.post('/login/', {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Login form should be displayed

    def test_user_logout(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)  # Redirect after logout


class ShoppingCartTest(TestCase):
    def setUp(self):
        # Create a user and a product for testing the shopping cart
        self.user = User.objects.create_user(
            username='testuser',
            password='securepassword',
        )
        self.category = Category.objects.create(name='Test Category')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            price=10.0,
            description='Test product description',
        )
        self.cart = ShoppingCart.objects.create(user=self.user, product=self.product, product_quantity=2)

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.post(f'/add_to_cart/{self.product.id}/', {'quantity': 3})
        self.assertEqual(response.status_code, 200)

    def test_remove_from_cart(self):
        self.client.login(username='testuser', password='securepassword')
        response = self.client.post(f'/remove_from_cart/{self.product.id}/')
        self.assertEqual(response.status_code, 404)


class ProductTestCase(TestCase):
    def setUp(self):
        # Create test categories
        self.category1 = Category.objects.create(name='Category 1', slug='category-1')
        self.category2 = Category.objects.create(name='Category 2', slug='category-2')

        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a customer associated with the user
        self.customer = Customer.objects.create(user=self.user)

        # Create test products
        self.product1 = Product.objects.create(category=self.category1, name='Product 1', price=10.0)
        self.product2 = Product.objects.create(category=self.category2, name='Product 2', price=15.0)

        # Log the user in
        self.client.login(username='testuser', password='testpassword')

    def test_product_detail_page(self):
        # Test if the product detail page loads for a valid product
        response = self.client.get(reverse(
            'product_detail_by_category', args=[self.category1.slug, self.product1.slug]
        ))
        self.assertEqual(response.status_code, 200)

    def test_product_detail_page_invalid_slug(self):
        # Test if the product detail page returns a 404 for an invalid product slug
        response = self.client.get(reverse(
            'product_detail_by_category', args=[self.category1.slug, 'invalid-slug']
        ))
        self.assertEqual(response.status_code, 404)

    def test_product_detail_page_wrong_category(self):
        # Test if the product detail page returns a 404 for a product in the wrong category
        response = self.client.get(reverse(
            'product_detail_by_category', args=[self.category2.slug, self.product1.slug]
        ))
        self.assertEqual(response.status_code, 404)

    def test_checkout_page_access(self):
        # Test access to the checkout page for authenticated users
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

    def test_order_confirmation_page_access(self):
        # Test access to the order confirmation page for an authenticated user with a valid order ID
        self.client.login(username='testuser', password='testpassword')
        order = Order.objects.create(customer=self.user.customer, total_cost=25.0)
        response = self.client.get(reverse('order_confirmation', args=[order.id]))
        self.assertEqual(response.status_code, 200)

    def test_order_confirmation_page_invalid_order_id(self):
        # Test that the order confirmation page returns a 404 for an invalid order ID
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('order_confirmation', args=[999]))  # Invalid order ID
        self.assertEqual(response.status_code, 404)

    def test_user_profile_view_access(self):
        # Test access to the user profile view for an authenticated user
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
