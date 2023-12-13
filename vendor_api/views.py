from datetime import timedelta
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Vendor
from .models import PurchaseOrder
from .serializers import VendorSerializer
from .serializers import PurchaseOrderSerializer

"""
Views are made using ModelViewSet beacause it streamlines API development, offering a consistent 
and reusable approach for CRUD operations on Django models. It minimizes boilerplate code, handles 
querysets and serializers, integrates well with Django's ORM, and allows for easy customization.
"""


"""
The VendorViewSet is a DRF viewset designed for CRUD operations on the Vendor model. It inherits
from ModelViewSet, providing standard functionalities(CRUD) for vendors.
"""
class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer
    
    """
    Custom action performance, accessible through a GET request.
    This action retrieves and returns performance metrics for a specific vendor, 
    including on-time delivery rate, quality rating average, average response time, 
    and fulfillmentrate. The metrics are obtained from the associated Vendor model.
    """
    @action(detail=True, methods=['GET'])
    def performance(self, request, pk=None):
        vendor = self.get_object()
        performance_data = {
            'on_time_delivery_rate': vendor.on_time_delivery_rate,
            'quality_rating_average': vendor.quality_rating_average,
            'average_response_time': vendor.average_response_time,
            'fulfillment_rate': vendor.fulfillment_rate,
        }
        return Response(performance_data)
    
class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
    """
    Custom action acknowledge, accessible through a GET request.
    This action acknowledges a purchase order, updating the acknowledgment date
    and the average_response_time field of the associated vendor model.
    """
    @action(detail=True, methods=['GET'])
    def acknowledge(self, request, pk=None):
        purchase_order = self.get_object()
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()

        # Update the average_response_time field of the vendor model
        purchase_order.vendor.average_response_time = calculate_average_response_time(purchase_order.vendor)
        purchase_order.vendor.save()
            
        return Response({'message': 'Purchase order acknowledged successfully.'})


def calculate_average_response_time(vendor):
    """
    Calculate the average response time for a vendor based on their purchase orders.
    Returns the average response time in hours.
    Returns None if there are no purchase orders.
    """
    # Retrieve all purchase orders of the vendor
    vendor_purchase_orders = PurchaseOrder.objects.filter(vendor=vendor)
    
    if not vendor_purchase_orders:
        return None

    # Calculate the total response time in seconds
    total_response_time_seconds = sum(
        (po.acknowledgment_date - po.issue_date).total_seconds()
        for po in vendor_purchase_orders
    )

    # Calculate the average response time in seconds
    average_response_time_seconds = total_response_time_seconds / len(vendor_purchase_orders)

    # Create a new timedelta object from the average in seconds
    average_response_time = timedelta(seconds=average_response_time_seconds)
    
    return round(average_response_time.total_seconds() / 3600, 2)

