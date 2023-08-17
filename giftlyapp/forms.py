from django import forms
from django.contrib.auth.models import User
from .models import Customer


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
