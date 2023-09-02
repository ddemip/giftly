from django.test import TestCase
from django.urls import reverse
from .models import Product, Category
from .shopping_cart import ShoppingCart
from django.contrib.auth.models import User  # Import User model


class ShoppingCartTestCase(TestCase):
    def setUp(self):
        # Create test products
        self.product1 = Product.objects.create(name='Product 1', price=10.0)
        self.product2 = Product.objects.create(name='Product 2', price=20.0)

    def test_add_to_cart(self):
        # Test adding products to the cart
        cart = ShoppingCart(self.client.session)
        cart.add(self.product1)
        cart.add(self.product2, quantity=2)

        self.assertEqual(len(cart), 3)  # Total items in cart
        self.assertEqual(cart.get_total_price(), 50.0)  # Total price

    def test_remove_from_cart(self):
        # Test removing products from the cart
        cart = ShoppingCart(self.client.session)
        cart.add(self.product1)
        cart.add(self.product2, quantity=2)
        cart.remove(self.product1)

        self.assertEqual(len(cart), 2)  # Total items in cart
        self.assertEqual(cart.get_total_price(), 40.0)  # Total price

    def test_clear_cart(self):
        # Test clearing the cart
        cart = ShoppingCart(self.client.session)
        cart.add(self.product1)
        cart.add(self.product2, quantity=2)
        cart.clear()

        self.assertEqual(len(cart), 0)  # Total items in cart
        self.assertEqual(cart.get_total_price(), 0.0)  # Total price


class ShoppingCartViewTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Product 1', price=10.0)
        self.cart = ShoppingCart(self.client.session)
        self.cart.add(self.product)

        # Create a user and set their password
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_cart_detail_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Test the cart detail view
        response = self.client.get(reverse('cart_detail'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Product 1')  # Check if product name is in response HTML
        self.assertContains(response, 'Total Price: $10.00')  # Check total price in HTML

        # Log out the user after the test
        self.client.logout()

    def test_add_to_cart_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Test adding products to the cart via the view
        response = self.client.post(reverse('cart_add', args=[self.product.id]), {'quantity': 2})

        self.assertEqual(response.status_code, 302)  # Redirect after adding to cart
        self.assertEqual(len(self.cart), 3)  # Total items in cart
        self.assertEqual(self.cart.get_total_price(), 30.0)  # Total price

        # Log out the user after the test
        self.client.logout()

    def test_remove_from_cart_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Test removing products from the cart via the view
        response = self.client.post(reverse('cart_remove', args=[self.product.id]))

        self.assertEqual(response.status_code, 302)  # Redirect after removing from cart
        self.assertEqual(len(self.cart), 0)  # Total items in cart
        self.assertEqual(self.cart.get_total_price(), 0.0)  # Total price

        # Log out the user after the test
        self.client.logout()


class CheckoutTestCase(TestCase):
    def setUp(self):
        self.product1 = Product.objects.create(name='Product 1', price=10.0)
        self.product2 = Product.objects.create(name='Product 2', price=20.0)
        self.category = Category.objects.create(name='Category 1')
        self.cart = ShoppingCart(self.client.session)
        self.cart.add(self.product1)
        self.cart.add(self.product2, quantity=2)

        # Create a user and set their password
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_checkout_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Test the checkout view
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

        # Simulate a POST request with checkout form data
        response = self.client.post(reverse('checkout'), {
            'sender_name': 'John Doe',
            'sender_email': 'johndoe@example.com',
            'is_gift': True,
            'gift_recipient_name': 'Gift Recipient',
            'recipient_email': 'gift@example.com',
            'payment_method': 'credit_card',
        })

        self.assertEqual(response.status_code, 302)  # Redirect after successful checkout
        self.assertQuerysetEqual(Product.objects.all(), [])  # All products have been purchased

        # Ensure that the cart is cleared after checkout
        self.assertEqual(len(self.cart), 0)
        self.assertEqual(self.cart.get_total_price(), 0.0)

        # Log out the user after the test
        self.client.logout()

    def test_order_confirmation_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create a test order
        response = self.client.post(reverse('checkout'), {
            'sender_name': 'John Doe',
            'sender_email': 'johndoe@example.com',
            'is_gift': True,
            'gift_recipient_name': 'Gift Recipient',
            'recipient_email': 'gift@example.com',
            'payment_method': 'credit_card',
        })

        self.assertEqual(response.status_code, 302)  # Redirect after successful checkout
        order_id = response.url.split('/')[-2]  # Extract order ID from the URL

        # Test the order confirmation view
        response = self.client.get(reverse('order_confirmation', args=[order_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Order Confirmation')
        self.assertContains(response, 'Total Cost: $30.00')

        # Ensure that an unauthorized user cannot access the order confirmation page
        self.client.logout()
        response = self.client.get(reverse('order_confirmation', args=[order_id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login page
