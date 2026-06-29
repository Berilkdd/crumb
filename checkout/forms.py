from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'address_line1', 'address_line2',
                  'town_or_city', 'postcode', 'phone_number',
                  )

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'address_line1': 'Address Line 1',
            'address_line2': 'Address Line 2',
            'town_or_city': 'Town or City',            
            'postcode': 'Postcode',
            'phone_number': 'Phone Number',       
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:           
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False