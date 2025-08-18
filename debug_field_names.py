"""
Debug Field Names - Check what fields are actually being returned
"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing
from django.contrib.auth.models import User

def debug_field_names():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='field_debug')
    
    print("🔍 DEBUGGING FIELD NAMES")
    print("="*50)
    
    # Create product
    product = Product.objects.create(
        user=test_user,
        name="Test Headphones",
        description="Test product",
        brand_name="TestBrand",
        brand_tone="premium",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics",
        features="Test feature",
        target_audience="Test audience"
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            print("✅ Listing generated successfully")
            print(f"📋 Listing ID: {listing.id}")
            
            # Check all A+ content related fields
            aplus_fields = [
                'amazon_aplus_content',
                'aplus_content',
                'amazon_aplus_content_plan',
                'aplus_content_plan'
            ]
            
            print("\n🔍 CHECKING A+ CONTENT FIELDS:")
            for field in aplus_fields:
                if hasattr(listing, field):
                    value = getattr(listing, field, None)
                    if value:
                        print(f"✅ {field}: {len(str(value))} characters")
                    else:
                        print(f"❌ {field}: Empty or None")
                else:
                    print(f"❌ {field}: Field doesn't exist")
            
            # Show all available fields on the listing model
            print(f"\n📋 ALL AVAILABLE FIELDS ON LISTING:")
            for field in listing._meta.fields:
                field_name = field.name
                value = getattr(listing, field_name, None)
                if value and 'aplus' in field_name.lower():
                    print(f"✅ {field_name}: {len(str(value))} chars")
                elif 'aplus' in field_name.lower():
                    print(f"❌ {field_name}: Empty")
                    
            # Check the actual API response format
            print(f"\n🔍 API SERIALIZATION CHECK:")
            from apps.listings.serializers import GeneratedListingSerializer
            serializer = GeneratedListingSerializer(listing)
            data = serializer.data
            
            for key, value in data.items():
                if 'aplus' in key.lower() and value:
                    print(f"✅ API returns '{key}': {len(str(value))} chars")
                elif 'aplus' in key.lower():
                    print(f"❌ API returns '{key}': Empty or None")
                    
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        product.delete()

if __name__ == "__main__":
    debug_field_names()