import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from rest_framework.test import APIClient
from rest_framework import status
import json

print("TESTING API WITH DJANGO TEST CLIENT")
print("=" * 40)

# Use Django's test client instead of requests
client = APIClient()

api_data = {
    'name': 'Django Client Test',
    'description': 'Test using Django test client',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 29.99,
    'brand_tone': 'handmade'
}

try:
    response = client.post('/api/core/products/', data=api_data, format='json')
    
    print(f"Django client response: {response.status_code}")
    
    if response.status_code == 201:
        print("SUCCESS with Django test client!")
        response_data = response.data
        print(f"   Product ID: {response_data.get('id')}")
        print(f"   Product Name: {response_data.get('name')}")
        
    else:
        print("Django client also failed:")
        print(f"   Error: {json.dumps(response.data, indent=2)}")
        
except Exception as e:
    print(f"Django client test failed: {e}")

print("\n" + "=" * 40)
print("DJANGO CLIENT TEST COMPLETE")