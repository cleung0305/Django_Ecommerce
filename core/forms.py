from django import forms
from django_countries.fields import CountryField

# class ContactForm(forms.Form):
#     from_email = forms.EmailField(required=True)
#     subject = forms.CharField(required=True)
#     message = forms.CharField(required=True)

class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment_address = forms.CharField(required=False)
