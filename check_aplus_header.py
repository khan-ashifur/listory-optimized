"""
Check what's in the A+ Content header
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
from django.contrib.auth.models import User

def check_header():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='check_header')
    
    # Create simple product
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
        
        if listing and listing.amazon_aplus_content:
            content = listing.amazon_aplus_content
            
            # Extract first 1000 characters to see the header
            print("📄 A+ CONTENT HEADER:")
            print("="*50)
            print(content[:1000])
            print("="*50)
            
            # Look for specific text patterns
            patterns = [
                'A+ Content Suggestions',
                'Complete A+ Content Strategy', 
                'Professional Amazon A+ content',
                'content-strategy',
                'aplus-introduction'
            ]
            
            print("\n🔍 PATTERN SEARCH:")
            for pattern in patterns:
                if pattern in content:
                    print(f"✅ Found: {pattern}")
                else:
                    print(f"❌ Missing: {pattern}")
            
        else:
            print("❌ No A+ content")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        product.delete()

if __name__ == "__main__":
    check_header()