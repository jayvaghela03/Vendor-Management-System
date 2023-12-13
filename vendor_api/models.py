from loguru import logger
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, F, ExpressionWrapper, fields

class Vendor(models.Model):
    """
    Model representing a vendor with various performance metrics.
    """
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_average = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
    
    def update_performance_metrics(self):
        """
        Update vendor's performance metrics based on associated purchase orders.
        """
        total_orders = self.purchaseorder_set.count()
        if total_orders > 0:
            
            try:
                # Calculate On-Time Delivery Rate
                self.on_time_delivery_rate = (
                    self.purchaseorder_set.filter(status='completed').count() / total_orders
                ) * 100
            except ZeroDivisionError as e:
                logger.error(f"In ON TIME DELIVERY -> {e}")
            
            try:
                # Calculate Quality Rating Average
                self.quality_rating_average = (
                    self.purchaseorder_set.exclude(quality_rating__isnull=True)
                    .aggregate(models.Avg('quality_rating'))['quality_rating__avg'] or 0
                )
            except Exception as e:
                logger.error(f"In QUALITY RATING -> {e}")
                
            try:
                # Calculate Average Response Time
                self.average_response_time = (
                    self.purchaseorder_set.exclude(acknowledgment_date__isnull=True)
                    .aggregate(
                        avg_response_time=ExpressionWrapper(
                            Avg(F('acknowledgment_date') - F('order_date')),
                            output_field=fields.FloatField()
                        )
                    )['avg_response_time']/3600
                )
            except Exception as e:
                logger.error(f"In average_response_time -> {e}")
            
            
            try:
                # Calculate Fulfillment Rate
                self.fulfillment_rate = (
                    self.purchaseorder_set.filter(status='completed').count() / total_orders
                ) * 100
            except ZeroDivisionError as e:
                logger.error(f"In fulfillment_rate -> {e}")
            
             # Save historical performance data
            history = HistoricalPerformance(
                vendor = self,
                on_time_delivery_rate = self.on_time_delivery_rate,
                quality_rating_average = self.quality_rating_average,
                average_response_time = self.average_response_time,
                fulfillment_rate = self.fulfillment_rate
            )
            history.save()
        self.save()
    


class PurchaseOrder(models.Model):
    """
    Model representing a purchase order with various attributes.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]
    
    po_number = models.CharField(max_length=255, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quality_rating = models.FloatField(null=True, blank=True, validators=[MaxValueValidator(10.0), MinValueValidator(0.0)]) 
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Purchase order {self.po_number} - {self.vendor.name}"
    

class HistoricalPerformance(models.Model):
    """
    Model representing historical performance metrics for a vendor.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_average = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)
    
    def __str__(self):
        return f"{self.vendor.name} - {self.date}"