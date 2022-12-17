from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

# Context Processor
# Allows us to use functions across all views.
# Add context processors to settings.py, under TEMPLATES.


def bag_contents(request):

    bag_items = []
    total = 0 
    product_count = 0
    bag = request.session.get('bag', {})

    # Iterating through the shopping bag.
    for item_id, quantity in bag.items():
        # Collect Product model and id.
        product = get_object_or_404(Product, pk=item_id)
        # Add up total price.
        total += quantity * product.price
        product_count += quantity
        # Dictionary of variables, allows us to use them in templates.
        bag_items.append({
            'item_id': item_id,
            'quantity': quantity,
            'product': product,
        })
    """ Free delivery threshold = 50, If cost total is less than 50, 
    delivery charge is added."""
    if total < settings.FREE_DELIVERY_THRESHOLD:
        # Standard delivery percentage = 10
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE/100)
        # The remaining amount the customer needs for free delivery.
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        # Free delivery, cost total more than 50 (delivery threshold).
        delivery = 0 
        free_delivery_delta = 0

    # Total cost including delivery.
    grand_total = delivery + total
    
    # Dictionary of variables for use within templates.
    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total
        

    }

    return context