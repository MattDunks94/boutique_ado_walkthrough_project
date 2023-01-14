from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category


class ProductForm(forms.ModelForm):

    class Meta:
        # Getting all fields from Product model.
        model = Product
        fields = '__all__'
    # Adding our own 'add image' file input.
    image = forms.ImageField(
        label='Image', required=False, widget=CustomClearableFileInput
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Getting all categories.
        categories = Category.objects.all()
        # This syntax is called 'list comprehension'.
        # Shorthand for loop adding items to a list.
        # Iterates through categories and gets friendly names.
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # Updating the 'category' field from Products fields.
        self.fields['category'].choices = friendly_names
        # Iterating through the rest of the fields and adding classes to them.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'