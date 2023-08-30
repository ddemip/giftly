from django import forms
from django.contrib.auth.models import User
from .models import Customer, Order
from django.contrib.auth.forms import UserCreationForm


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class CustomerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Customer
        exclude = ['user', 'session_uuid', 'first_name', 'last_name', 'email']

    def save(self, commit=True):
        customer = super().save(commit=False)
        user = customer.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.save()
        if commit:
            customer.save()
        return customer


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 30)]


class ShoppingCartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                coerce=int)
    update = forms.BooleanField(required=False,
                                initial=False,
                                widget=forms.HiddenInput
                                )


class CheckoutForm(forms.ModelForm):
    total_amount = forms.DecimalField(disabled=True)
    PAYMENT_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('google_pay', 'Google Pay'),
        # Add more payment options here
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Order
        fields = ['recipient_name', 'recipient_email', 'payment_method', 'total_amount']
