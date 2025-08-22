import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.serializers import ProductSerializer
from apps.core.models import Product

print("DEBUGGING SERIALIZER VALIDATION STEP BY STEP")
print("=" * 50)

# 1. Check what choices the serializer actually sees
serializer = ProductSerializer()
print("1. SERIALIZER FIELD INSPECTION:")
print("-" * 35)
marketplace_field = serializer.fields.get('marketplace')
print(f"   Field type: {type(marketplace_field)}")
print(f"   Field max_length: {getattr(marketplace_field, 'max_length', 'No max_length')}")

# 2. Check model choices directly
print("\n2. MODEL CHOICES INSPECTION:")
print("-" * 30)
model_choices = Product.ALL_MARKETPLACES
print(f"   ALL_MARKETPLACES count: {len(model_choices)}")
etsy_in_choices = any(choice[0] == 'etsy' for choice in model_choices)
print(f"   Etsy in ALL_MARKETPLACES: {etsy_in_choices}")

# 3. Test custom validation method directly
print("\n3. CUSTOM VALIDATION TEST:")
print("-" * 27)
try:
    result = serializer.validate_marketplace('etsy')
    print(f"   validate_marketplace('etsy') returned: {result}")
except Exception as e:
    print(f"   validate_marketplace('etsy') failed: {e}")

# 4. Test the full serializer validation
print("\n4. FULL SERIALIZER VALIDATION:")
print("-" * 32)
test_data = {
    'name': 'Test Validation',
    'description': 'Test description',
    'brand_name': 'TestBrand',
    'target_platform': 'etsy',
    'marketplace': 'etsy',
    'price': 29.99
}

try:
    serializer = ProductSerializer(data=test_data)
    is_valid = serializer.is_valid()
    print(f"   is_valid(): {is_valid}")
    if not is_valid:
        print(f"   Errors: {serializer.errors}")
        
        # Check if the error is coming from the field itself or our custom validation
        if 'marketplace' in serializer.errors:
            marketplace_errors = serializer.errors['marketplace']
            print(f"   Marketplace specific errors: {marketplace_errors}")
            for error in marketplace_errors:
                if 'not a valid choice' in str(error):
                    print("   ERROR SOURCE: Built-in ChoiceField validation")
                elif 'not a valid marketplace choice' in str(error):
                    print("   ERROR SOURCE: Our custom validation")
                    
except Exception as e:
    print(f"   Exception during validation: {e}")

print("\n" + "=" * 50)
print("SERIALIZER DEBUGGING COMPLETE")