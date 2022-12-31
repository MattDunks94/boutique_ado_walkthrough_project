from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm


# Checkout view.
def checkout(request):
    # Getting the user's shopping bag session.
    bag = request.session.get('bag', {})
    if not bag:
        # Displays error message if bag doesn't exist.
        messages.error(request, "There's nothing in your bag at the moment")
        # Redirects back to products page.
        return redirect(reverse('products'))
    
    # Order form instance.
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form
    }
    return render(request, template, context)
