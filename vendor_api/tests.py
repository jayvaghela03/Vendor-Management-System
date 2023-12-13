from datetime import timedelta
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Vendor, PurchaseOrder

#Test cases for checking the smooth functioning of endpoints and CRUD operations
class PurchaseOrderViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.vendor = Vendor.objects.create(name='Test Vendor')
        self.purchase_order = PurchaseOrder.objects.create(
            po_number='PO123',
            vendor=self.vendor,
            order_date=timezone.now(),
            delivery_date=timezone.now() + timedelta(days=7),
            items={'item1': 10, 'item2': 5},
            quantity=15,
            status='pending',
            quality_rating=4.5,
        )
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = str(RefreshToken.for_user(self.user).access_token)


    def test_acknowledge_action(self):
        url = reverse('purchase_order-acknowledge', kwargs={'pk': self.purchase_order.pk})
        headers = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}

        response = self.client.get(url, **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        # Check if the acknowledgment_date has been updated in the database
        updated_purchase_order = PurchaseOrder.objects.get(pk=self.purchase_order.pk)
        self.assertIsNotNone(updated_purchase_order.acknowledgment_date)
