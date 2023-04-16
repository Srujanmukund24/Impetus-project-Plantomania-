from django import forms

class BillingForm(forms.Form):
    full_name = forms.CharField(label='Full Name', max_length=100)
    email = forms.EmailField(label='Email')
    address = forms.CharField(label='Address', max_length=200)
    country = forms.CharField(label='Country', max_length=50)
    state = forms.CharField(label='State', max_length=50)
    city = forms.CharField(label='City', max_length=50)
    zip_code = forms.CharField(label='Zip Code', max_length=10)
    card_number = forms.CharField(label='Card Number', max_length=20)
    exp_month = forms.CharField(label='Expiration Month', max_length=2)
    exp_year = forms.CharField(label='Expiration Year', max_length=4)
    cvv = forms.CharField(label='CVV', max_length=3)
