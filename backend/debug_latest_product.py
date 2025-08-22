import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product

# Check the latest created products
latest_products = Product.objects.all().order_by('-id')[:5]

print("LATEST 5 PRODUCTS:")
print("=" * 50)

for product in latest_products:
    print(f"ID: {product.id}")
    print(f"  Name: {product.name}")
    print(f"  Brand Tone: '{product.brand_tone}'")
    print(f"  Marketplace: '{product.marketplace}'")
    print(f"  Target Platform: '{product.target_platform}'")
    print(f"  Created: {product.created_at}")
    print()

# Check if the brand_tone field can accept the new values
print("\nCHECKING BRAND_TONE FIELD:")
print("=" * 30)
field = Product._meta.get_field('brand_tone')
print(f"Max length: {field.max_length}")
print(f"Choices: {field.choices[:5]}...")  # Show first 5 choices

# Test creating a product directly
print("\nTEST DIRECT PRODUCT CREATION:")
print("=" * 35)

from django.contrib.auth.models import User
user, created = User.objects.get_or_create(username='debug_user')

try:
    test_product = Product.objects.create(
        user=user,
        name='Debug Test Product',
        description='Test description',
        brand_name='TestBrand',
        brand_tone='handmade_artisan',
        target_platform='etsy',
        marketplace='etsy',
        price=29.99
    )
    
    print(f"SUCCESS! Created product ID: {test_product.id}")
    print(f"  Brand Tone: '{test_product.brand_tone}'")
    print(f"  Marketplace: '{test_product.marketplace}'")
    
    # Clean up
    test_product.delete()
    
except Exception as e:
    print(f"ERROR: {e}")

print("\nDEBUG COMPLETE")