from django import forms
from django.contrib.auth.models import User
from .models import Customer, PaymentDetail
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


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


class PasswordChangeCustomForm(PasswordChangeForm):
    class Meta:
        model = User


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
    class Meta:
        model = PaymentDetail
        fields = ['sender_name', 'sender_email', 'is_gift', 'gift_recipient_name', 'recipient_email', 'payment_method']

    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Pangalingiga'),
        ('credit_card', 'Krediitkaart'),
        ('paypal', 'PayPal'),
        ('apple_pay', 'Apple Pay'),
        ('google_pay', 'Google Pay'),
        # Add more payment methods here
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect
    )

    sender_name = forms.CharField(max_length=255, required=True)
    sender_email = forms.EmailField(max_length=255, required=True)

    is_gift = forms.BooleanField(initial=False, required=False)
    gift_recipient_name = forms.CharField(max_length=255, required=False)
    recipient_email = forms.EmailField(max_length=255, required=False)

    def clean(self):
        cleaned_data = super().clean()
        is_gift = cleaned_data.get('is_gift')
        gift_recipient_name = cleaned_data.get('gift_recipient_name')

        if is_gift and not gift_recipient_name:
            self.add_error('gift_recipient_name', 'This field is required for gift orders.')

        return cleaned_data
