from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings

import stripe
import json

from products.models import Product
from .models import Order, OrderLineItem
from .forms import OrderForm
from bag.contexts import bag_contents


@require_POST
def cache_checkout_data(request):
    """ Checking if the user ticked the 'save_info' box. """
    try:
        # Getting the client secret, splitting it after 'client'.
        # That will be replaced with the payment_intent id.
        pid = request.POST.get('client_secret').split('_secret')[0]
        # Setting up Stripe with the SECRET_KEY
        stripe.api_key = settings.STRIPE_SECRET_KEY
        # Modifying metadata.
        # Collecting user, save_info decision and user's shopping bag.
        stripe.PaymentIntent.modify(pid, metdata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        # Return a successful response.
        return HttpResponse(status=200)
    
    except Exception as e:
        # If any errors occur, add error message and return the error message 
        # content, along with a status of 400, bad request.
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)



# Checkout view.
def checkout(request):
    # Assigning stripe variables to new variables.
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        # Requesting the shopping bag.
        bag = request.session.get('bag', {})
        # Placing form data into dictionary.
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        # If form is valid, save form and iterate through bag items, 
        # to create line items.
        if order_form.is_valid():
            # Commit=False stops the save from happening.
            order.order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe = pid
            order.original_bag = json.dumps(bag)
            order.save()
            for item_id, item_data in bag.items():
                try:
                    # Get product id.
                    product = Product.objects.get(id=item_id)
                    # If product id value is integer, product has no sizes.
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    # Otherwise if product id isn't integer, product has sizes.
                    else:
                        for size, quantity in item_data['items_by_size'].items():
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_line_item.save()
                # Very rare, but in case of product does not exist.
                except Product.DoesNotExist:
                    # Displays error message.
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our \
                        database."
                        "Please call us for assistance!")
                    )
                    # Deletes order.
                    order.delete()
                    # Redirects back to view_bag.
                    return redirect(reverse('view_bag'))
            # Give user option to save form info.
            request.session['save_info'] = 'save_info' in request.POST
            # Redirects to checkout_success url, via order number.
            return redirect(
                reverse('checkout_success', args=[order.order_number])
                )
        # If form is not valid, display an error.
        else:
            messages.error(request, 'There was an error with your form. \
                Please check your information.')

    else:
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


def checkout_success(request, order_number):
    """ Handle successful checkouts """
    # Checking if user wanted to save form info from session.
    save_info = request.session.get('save_info')
    # Getting order.
    order = get_object_or_404(Order, order_number=order_number)
    # Display successful order message.
    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
            email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']
    
    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)