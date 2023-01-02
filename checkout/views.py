from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings

import stripe

from .forms import OrderForm

from bag.contexts import bag_contents


# Checkout view.
def checkout(request):
    # Assigning stripe variables to new variables.
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Getting the user's shopping bag session.
    bag = request.session.get('bag', {})
    if not bag:
        # Displays error message if bag doesn't exist.
        messages.error(request, "There's nothing in your bag at the moment")
        # Redirects back to products page.
        return redirect(reverse('products'))

    # Assigning bag_contents to variable.
    current_bag = bag_contents(request)
    # Getting the bag grand total.
    total = current_bag['grand_total']
    # Sets the total to 2 decimal places.
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        # Currency set in settings.
        currency=settings.STRIPE_CURRENCY,
    )

    # Order form instance.
    order_form = OrderForm()

    # Warning message if stripe_public_key doesn't exist.
    if not stripe_public_key:
        messages.warning(
            request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?'
            )

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }
    return render(request, template, context)
