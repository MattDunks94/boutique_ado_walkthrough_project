from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

import stripe

from .forms import OrderForm

from bag.contexts import bag_contents


# Checkout view.
def checkout(request):
    # Getting the user's shopping bag session.
    bag = request.session.get('bag', {})
    if not bag:
        # Displays error message if bag doesn't exist.
        messages.error(request, "There's nothing in your bag at the moment")
        # Redirects back to products page.
        return redirect(reverse('products'))

    current_bag = bag_contents(request)
    total = current_bag['grand_total']
    stripe_total = round(total * 100)

    # Order form instance.
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51MLVZwFjejZeJgUo3dWSgHcDyWfFbwRJ3DNh3b3yFAfKa3QgeYAxQgUIkUB8ipqIxW8sjr5JLFJA9kJR34BDia1400yCf0Lk0I',
        'client_secret': 'test client secret',
    }
    return render(request, template, context)
