from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

#Serializers for all the models

class VendorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vendor
        fields = '__all__'
        
class PurchaseOrderSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'
        read_only_fields = ['acknowledgment_date']
        
class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
        