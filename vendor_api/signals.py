from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from .models import PurchaseOrder

# Signals to trigger the metric update
@receiver(post_save, sender=PurchaseOrder)
def update_metrics_on_purchase_order_update(sender, instance, **kwargs):
    """
    Signal handler to update vendor performance metrics when a PurchaseOrder is saved.

    Args:
        sender: The model class that sends the signal (PurchaseOrder).
        instance: The actual instance being saved (a specific PurchaseOrder).
        **kwargs: Additional keyword arguments.

    Notes:
        This signal is triggered whenever a PurchaseOrder is saved. It checks if the
        status of the PurchaseOrder has changed or if the status is 'completed'. If either
        condition is true, it updates the performance metrics of the associated vendor.
    """
    vendor = instance.vendor
    old_status = instance.status
    new_status = instance.status

    # Check if the status has changed or the status is 'completed'
    if old_status != new_status or new_status == 'completed':
        # Update the performance metrics of the associated vendor
        vendor.update_performance_metrics()
