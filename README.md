# Vendor-Management-System

# Vendor Management System API

## Overview

This is a Django and Django Rest Framework based Vendor Management System API allows you to manage vendor profiles, track purchase orders, and evaluate vendor performance metrics.

## Setup Instructions

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jayvaghela03/Vendor-Management-System-with-Performance-Metrics.git
   cd vendor_management_system

2. Install Dependencies:
"pip install -r requirements.txt"
3. Apply Migrations:
  "python manage.py migrate" and python "manage.py makemigrations"
4. Create Superuser:
"python manage.py createsuperuser"
5. Run Development Server:
"python manage.py runserver"
Access Admin Panel:

Visit http://127.0.0.1:8000/admin/ and log in with the superuser credentials.

Obtain Token:

Go to http://127.0.0.1:8000/api/token/ to obtain the access token

## API Endpoints 

### Vendor Management:
-  Endpoint: /api/vendors/  
   Method: GET (List all vendors) / POST (Create a new vendor)
  
- Endpoint: /api/vendors/{vendor_id}/  
  Method: GET (Retrieve) / PUT (Update) / DELETE (Delete)

#### Vendor Performance Metrics:

- Endpoint: /api/vendors/{vendor_id}/performance/   
  Method: GET

### Purchase Order Tracking
-  Endpoint: /api/purchase_orders/    
   Method: GET (List all purchase orders) / POST (Create a new purchase order)

-  Endpoint: /api/purchase_orders/{po_id}/   
   Method: GET (Retrieve) / PUT (Update) / DELETE (Delete)

#### Acknowledge Purchase Order:

- Endpoint: /api/purchase_orders/{po_id}/acknowledge/   
  Method: GET(Retrieve)

## Models
### Vendor Model
- name: CharField - Vendor's name.
- contact_details: TextField - Contact information of the vendor.
- address: TextField - Physical address of the vendor.
- vendor_code: CharField - A unique identifier for the vendor.
- on_time_delivery_rate: FloatField - Tracks the percentage of on-time deliveries.
- quality_rating_avg: FloatField - Average rating of quality based on purchase orders.
- average_response_time: FloatField - Average time taken to acknowledge purchase orders.
- fulfillment_rate: FloatField - Percentage of purchase orders fulfilled successfully.

### Purchase Order Model
-  po_number: CharField - Unique number identifying the PO.
-  vendor: ForeignKey - Link to the Vendor model.
-  order_date: DateTimeField - Date when the order was placed.
-  delivery_date: DateTimeField - Expected or actual delivery date of the order.
-  items: JSONField - Details of items ordered.
-  quantity: IntegerField - Total quantity of items in the PO.
-  status: CharField - Current status of the PO (e.g., pending, completed, canceled).
-  quality_rating: FloatField - Rating given to the vendor for this PO (nullable).
-  issue_date: DateTimeField - Timestamp when the PO was issued to the vendor.
-  acknowledgment_date: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.

### Historical Performance Model
- vendor: ForeignKey - Link to the Vendor model.
- date: DateTimeField - Date of the performance record.
- on_time_delivery_rate: FloatField - Historical record of the on-time delivery rate.
- quality_rating_avg: FloatField - Historical record of the quality rating average.
- average_response_time: FloatField - Historical record of the average response time.
- fulfillment_rate: FloatField - Historical record of the fulfilment rate.

### Token Authentication
I have used JWT simple to apply token based authentication, it is widely used for industry ready products.
To access secured endpoints, include the token in the Authorization header:       

-  Authorization: Bearer &lt;Token&gt;

### Test Suite
- A comprehensive test suite is available in the tests directory.
- Run tests using:  "python manage.py test"

### Additional Details
- I've implemented Django Signals to trigger the metrics updation in real time whenever a PO changes.
- I've implemented all the required validations and exception handlers for smooth API use. 

\# This README file provides basic setup instructions, details on API endpoints, and mentions a test suite.
