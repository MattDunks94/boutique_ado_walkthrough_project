from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


# Updates order_total everytime user adds new line item.
@receiver(post_save, sender=OrderLineItem)
def update_on_save(sender, instance, created, **kwargs):
    """Update order total on lineitem update/create"""

    instance.order.update_total()


# Updates order_total when item is removed. 
@receiver(post_delete, sender=OrderLineItem)
def update_on_save(sender, instance, **kwargs):
    """Update order total on lineitem delete"""

    instance.order.update_total()