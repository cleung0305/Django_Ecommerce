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

    shipping_address = forms.CharField(required=False)
    shipping_address2 = forms.CharField(required=False)
    shipping_city = forms.CharField(widget=forms.TextInput(attrs={
            'id':'city',
            'class':'form-control'
        }), required=False)
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=forms.Select(attrs={
            'class':'custom-select d-block w-100',
            'id':'country'
        }))
    shipping_state = forms.ChoiceField(choices=STATES_CHOICES, widget=forms.Select(attrs={
            'class':'custom-select d-block w-100',
            'id':'state'
        }))
    shipping_zip = forms.CharField(required=False)




    billing_address = forms.CharField(required=False)
    billing_address2 = forms.CharField(required=False)
    billing_city = forms.CharField(widget=forms.TextInput(attrs={
            'id':'city',
            'class':'form-control'
        }), required=False)
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=forms.Select(attrs={
            'class':'custom-select d-block w-100',
            'id':'country'
        }))
    billing_state = forms.ChoiceField(choices=STATES_CHOICES, widget=forms.Select(attrs={
            'class':'custom-select d-block w-100',
            'id':'state'
        }))
    billing_zip = forms.CharField(required=False)

    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    same_billing_address = forms.BooleanField(required=False)
    
    payment_option = forms.ChoiceField(widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control',
        'placeholder':'Promo Code',
        'aria-label':'Recipient\'s username',
        'aria-describedby':'basic-addon2'
    }))


class RefundForm(forms.Form):
    order_number = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': '4'
    }))
    email = forms.EmailField()