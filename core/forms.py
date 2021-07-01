from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

# class ContactForm(forms.Form):
#     from_email = forms.EmailField(required=True)
#     subject = forms.CharField(required=True)
#     message = forms.CharField(required=True)


STATES_CHOICES = (
    ("Alabama","Alabama"),("Alaska","Alaska"),("Arizona","Arizona"),("Arkansas","Arkansas"),("California","California"),("Colorado","Colorado"),("Connecticut","Connecticut"),("Delaware","Delaware"),("Florida","Florida"),("Georgia","Georgia"),("Hawaii","Hawaii"),("Idaho","Idaho"),("Illinois","Illinois"),("Indiana","Indiana"),("Iowa","Iowa"),("Kansas","Kansas"),("Kentucky","Kentucky"),("Louisiana","Louisiana"),("Maine","Maine"),("Maryland","Maryland"),("Massachusetts","Massachusetts"),("Michigan","Michigan"),("Minnesota","Minnesota"),("Mississippi","Mississippi"),("Missouri","Missouri"),("Montana","Montana"),("Nebraska","Nebraska"),("Nevada","Nevada"),("New Hampshire","New Hampshire"),("New Jersey","New Jersey"),("New Mexico","New Mexico"),("New York","New York"),("North Carolina","North Carolina"),("North Dakota","North Dakota"),("Ohio","Ohio"),("Oklahoma","Oklahoma"),("Oregon","Oregon"),("Pennsylvania","Pennsylvania"),("Rhode Island","Rhode Island"),("South Carolina","South Carolina"),("South Dakota","South Dakota"),("Tennessee","Tennessee"),("Texas","Texas"),("Utah","Utah"),("Vermont","Vermont"),("Virginia","Virginia"),("Washington","Washington"),("West Virginia","West Virginia"),("Wisconsin","Wisconsin"),("Wyoming","Wyoming")
    )


PAYMENT_CHOICES = (
    ('C', 'Card'),
    ('P', 'Paypal')
)


class CheckoutForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'id':'email',
        'class':'form-control'
    }), required=False)

    street_address = forms.CharField(widget=forms.TextInput(attrs={
            'id':'address',
            'class':'form-control'
        }), required=True)
    
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
            'id':'address-2',
            'class':'form-control'
        }))

    city = forms.CharField(widget=forms.TextInput(attrs={
            'id':'city',
            'class':'form-control'
        }), required=True)
    
    country = CountryField(blank_label='(select country)').formfield(widget=forms.Select(attrs={
            'class':'custom-select d-block w-100',
            'id':'country'
        }))
    
    states = forms.ChoiceField(choices=STATES_CHOICES, widget=forms.Select(attrs={
            'class':'custom-select d-block w-100',
            'id':'state'
        }))
    
    zip_address = forms.CharField(widget=forms.TextInput(attrs={
            'id':'zip',
            'class':'form-control'
        }))

    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Promo Code',
        'aria-label':'Recipient\'s username',
        'aria-describedby':'basic-addon2'
    }))