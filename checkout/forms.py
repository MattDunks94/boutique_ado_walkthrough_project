from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # Setting form up as default via the __init__ method.
        super().__init__(*args, **kwargs)
        # Dictionary of placeholders for the fields.
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # Cursor will be automatically placed on the 'full_name' field.
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # Iterating through the fields, 
        for field in self.fields:
            # If the field is required a '*' will be added to it.
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Adds css class to the fields.
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            # Removes labels as we have placeholders.
            self.fields[field].label = False