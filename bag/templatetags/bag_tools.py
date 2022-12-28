from django import template

# Library is part of django library.
register = template.Library()


# This is a custom tamplate filter.
@register.filter(name='calc_subtotal')
# Function that we want to target in bag.html
def calc_subtotal(price, quantity):
    return price * quantity