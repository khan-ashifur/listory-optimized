import os
import sys
import django
import json
import requests

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.core.serializers import ProductSerializer
from django.contrib.auth.models import User

print("🔍 COMPREHENSIVE ETSY MARKETPLACE DEBUGGING")
print("=" * 50)

# 1. Check model choices directly
print("\n1. MODEL CHOICES VERIFICATION:")
print("-" * 30)
marketplace_choices = Product._meta.get_field('marketplace').choices
print(f"Total marketplace choices: {len(marketplace_choices)}")
etsy_choices = [choice for choice in marketplace_choices if 'etsy' in choice[0]]
print(f"Etsy choices found: {etsy_choices}")

# 2. Test serializer validation directly
print("\n2. SERIALIZER VALIDATION TEST:")
print("-" * 30)
test_data = {
    'name': 'Test Etsy Product',
    'description': 'Test description',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 29.99
}

serializer = ProductSerializer(data=test_data)
is_valid = serializer.is_valid()
print(f"Serializer validation result: {is_valid}")
if not is_valid:
    print(f"Serializer errors: {serializer.errors}")
else:
    print("✅ Serializer validation passed!")

# 3. Test Django model creation directly
print("\n3. DIRECT MODEL CREATION TEST:")
print("-" * 30)
try:
    user, created = User.objects.get_or_create(
        username='debug_user',
        defaults={'email': 'debug@test.com'}
    )
    
    product = Product.objects.create(
        user=user,
        name='Direct Model Test',
        description='Test description',
        brand_name='TestBrand',
        target_platform='etsy',
        marketplace='etsy',
        price=29.99
    )
    print(f"✅ Direct model creation successful! Product ID: {product.id}")
    print(f"   Product marketplace: {product.marketplace}")
    print(f"   Product target_platform: {product.target_platform}")
    
    # Clean up
    product.delete()
    
except Exception as e:
    print(f"❌ Direct model creation failed: {e}")

# 4. Test API endpoint directly with requests
print("\n4. API ENDPOINT TEST:")
print("-" * 30)

api_data = {
    'name': 'API Test Product',
    'description': 'Test description',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 29.99
}

try:
    response = requests.post(
        'http://localhost:8000/api/core/products/',
        json=api_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"API Response Status: {response.status_code}")
    print(f"API Response Headers: {dict(response.headers)}")
    
    try:
        response_json = response.json()
        print(f"API Response Body: {json.dumps(response_json, indent=2)}")
    except:
        print(f"API Response Text: {response.text}")
        
except Exception as e:
    print(f"❌ API request failed: {e}")

# 5. Compare with working marketplace
print("\n5. WORKING MARKETPLACE COMPARISON:")
print("-" * 40)

# Test with 'us' marketplace that we know works
working_data = api_data.copy()
working_data['marketplace'] = 'us'

try:
    response = requests.post(
        'http://localhost:8000/api/core/products/',
        json=working_data,
        headers={'Content-Type': 'application/json'}
    )
    
    print(f"US marketplace response: {response.status_code}")
    if response.status_code == 201:
        print("✅ US marketplace works correctly")
        # Clean up if created
        try:
            created_product = response.json()
            if 'id' in created_product:
                Product.objects.filter(id=created_product['id']).delete()
        except:
            pass
    else:
        print(f"❌ US marketplace also fails: {response.text}")
        
except Exception as e:
    print(f"❌ US marketplace test failed: {e}")

# 6. Check serializer field definition
print("\n6. SERIALIZER FIELD INSPECTION:")
print("-" * 35)
serializer_instance = ProductSerializer()
marketplace_field = serializer_instance.fields.get('marketplace')
if marketplace_field:
    print(f"Marketplace field type: {type(marketplace_field)}")
    print(f"Marketplace field choices: {getattr(marketplace_field, 'choices', 'No choices attr')}")
else:
    print("❌ No marketplace field found in serializer")

print("\n" + "=" * 50)
print("DEBUGGING COMPLETE")