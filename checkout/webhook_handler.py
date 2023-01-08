from django.http import HttpResponse

from .models import Order, OrderLineItem
from products.models import Product

import json
import time


class StripeWH_Handler:
    """ Handle Stripe webhooks """
    # Webhooks notifies user about payment events ie. 
    # successful, dispute or recurring payments.
    # They are sent out whenever an event occurs, such as a payment.

    # Assigning request as an attribute of the class.
    def __init__(self, request):
        self.request = request

    # Takes the stripe event and return a http response.
    def handle_event(self, event):
        """
        Handle a generic/unexpected/unknown webhook event.
        """

        return HttpResponse(
            content=f'Webhook received:{event["type"]}', 
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe.
        """

        # Creating a mockup order form.
        # Assigning the payment intent to variable.
        intent = event.data.object
        # Getting the payment intent id.
        pid = intent.id
        # Getting the bag.
        bag = intent.metadata.bag
        # User's save info preference.
        save_info = intent.metadata.save_info
    
        billing_details = intent.charges.data[0].billing_details
        shipping_details = intent.shipping
        grand_total = round(intent.charges.data[0].amount / 100, 2)
        # Clean data in the shipping details.
        for field, value in shipping_details.address.items():
            if value == '':
                shipping_details.address[field] = None

        # Order doesn't exist.
        order_exists = False
        # Attempt is for a delay for when the order is not found.
        attempt = 1 
        # This will execute 5 times.
        # It will try and find the order 5 times over 5 seconds.
        while attempt <= 5:
            try:
                order = Order.objects.get(
                    full_name__iexact=shipping_details.name,
                    email__iexact=billing_details.email,
                    phone_number__iexact=shipping_details.phone_number,
                    country__iexact=shipping_details.address.country,
                    postcode__iexact=shipping_details.address.postal_code,
                    town_or_city__iexact=shipping_details.address.city,
                    street_address1__iexact=shipping_details.address.line1,
                    street_address2__iexact=shipping_details.address.line2,
                    county__iexact=shipping_details.address.state,
                    grand_total=grand_total,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                order_exists = True
                return HttpResponse(
                    content=f'Webhook received:{event["type"]} | SUCCESS: Verified order ', 
                    status=200)
            except Order.DoesNotExist:
                # Incrementing attempt by 1.
                attempt += 1
                # Adding 1 second timer before trying again.
                time.sleep(1)
        if order_exists:
            return HttpResponse(
                content=f'Webhook received:{event["type"]} | SUCCESS: Verified order ', 
                status=200)
        else:
            order = None
            try:
                # Creating an order.
                order = Order.objects.create(
                    full_name=shipping_details.name,
                    email=billing_details.email,
                    phone_number=shipping_details.phone_number,
                    country=shipping_details.address.country,
                    postcode=shipping_details.address.postal_code,
                    town_or_city=shipping_details.address.city,
                    street_address1=shipping_details.address.line1,
                    street_address2=shipping_details.address.line2,
                    county=shipping_details.address.state,
                    original_bag=bag,
                    stripe_pid=pid,
                )
                # Getting the bag from the json version.
                for item_id, item_data in json.loads(bag).items():
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
            except Exception as e:
                if order:
                    # Delete the order.
                    order.delete()
                    # Return Error with content, and status code 500.
                return HttpResponse(
                     content=f'Webhook received:{event["type"]} | ERROR: {e}', 
                     status=500)
        # Return successful response.
        return HttpResponse(
            content=f'Webhook received:{event["type"]} | SUCCESS: Created order in webhook', 
            status=200)
                
    def handle_payment_intent_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe.
        """

        return HttpResponse(
            content=f'Webhook received:{event["type"]}', 
            status=200)