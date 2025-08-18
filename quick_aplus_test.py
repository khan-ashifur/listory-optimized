"""
Quick A+ Content Test - Check Frontend Display Issue
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

def quick_test():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='quick_test')
    
    print("🔍 QUICK A+ CONTENT TEST")
    print("="*50)
    
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
            print(f"✅ A+ Content: {len(content)} chars")
            
            # Check for strategy section
            if 'aplus-strategy-summary' in content:
                print("✅ Strategy section found")
                
                # Extract and show strategy content
                import re
                strategy_match = re.search(r'<h3[^>]*>Overall A\+ Strategy</h3>\s*<p[^>]*>(.*?)</p>', content, re.DOTALL)
                if strategy_match:
                    strategy_content = strategy_match.group(1).strip()
                    print(f"📝 Strategy content: {strategy_content[:100]}...")
            else:
                print("❌ Strategy section missing")
                
            # Check if it starts with strategy
            print(f"\n📄 Content starts with:")
            print(content[:300])
            print("...")
            
        else:
            print("❌ No A+ content")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        product.delete()

if __name__ == "__main__":
    quick_test()