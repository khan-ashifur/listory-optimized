import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.core.serializers import ProductSerializer

print("DEBUGGING MODEL AND SERIALIZER CHOICES")
print("=" * 45)

print("1. Product.ALL_MARKETPLACES:")
for choice in Product.ALL_MARKETPLACES:
    print(f"   {choice}")

etsy_found = any(choice[0] == 'etsy' for choice in Product.ALL_MARKETPLACES)
print(f"\nEtsy in ALL_MARKETPLACES: {etsy_found}")

print("\n2. Model field choices:")
field_choices = Product._meta.get_field('marketplace').choices
etsy_in_field = any(choice[0] == 'etsy' for choice in field_choices)
print(f"Etsy in field choices: {etsy_in_field}")

print("\n3. Test serializer validation:")
serializer = ProductSerializer()
try:
    result = serializer.validate_marketplace('etsy')
    print(f"Serializer validate_marketplace('etsy'): {result}")
except Exception as e:
    print(f"Serializer validation error: {e}")

print("\n4. Full serializer test:")
test_data = {
    'name': 'Test Product',
    'description': 'Test description',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 29.99
}

serializer = ProductSerializer(data=test_data)
is_valid = serializer.is_valid()
print(f"Serializer is_valid(): {is_valid}")
if not is_valid:
    print(f"Errors: {serializer.errors}")

print("\n" + "=" * 45)
print("DEBUG COMPLETE")