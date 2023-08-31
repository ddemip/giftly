from django import forms

class WeatherForm(forms.Form):
    location = forms.CharField(label="Enter a city", max_length=100)
