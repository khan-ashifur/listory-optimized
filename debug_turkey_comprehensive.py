import os
import sys
import django

# Set up the backend path correctly
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
import logging

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_turkey_comprehensive():
    try:
        # Find a Turkey product to test with
        turkey_products = Product.objects.filter(marketplace='tr')
        if not turkey_products.exists():
            print("❌ No Turkey products found. Creating test product...")
            # Update an existing product to Turkey marketplace
            product = Product.objects.first()
            if product:
                product.marketplace = 'tr'
                product.save()
                print(f"✅ Updated product {product.id} to Turkey marketplace")
            else:
                print("❌ No products found at all")
                return
        else:
            product = turkey_products.first()
            print(f"✅ Found Turkey product: {product.id} - {product.name}")

        # Test the generation
        service = ListingGeneratorService()
        print(f"\n🔄 Generating Turkey listing for product {product.id}...")
        
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"\n📊 Generation Results:")
        print(f"   - Listing ID: {listing.id}")
        print(f"   - Title length: {len(listing.title) if listing.title else 0}")
        print(f"   - A+ Content length: {len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0}")
        
        # Check if comprehensive sections exist
        if listing.amazon_aplus_content:
            aplus_content = listing.amazon_aplus_content
            section_count = aplus_content.count('class="aplus-section')
            print(f"   - A+ Sections found: {section_count}")
            
            # Check for specific section indicators
            if 'hero' in aplus_content.lower():
                print("   ✅ Hero section detected")
            if 'features' in aplus_content.lower():
                print("   ✅ Features section detected")
            if 'quality' in aplus_content.lower():
                print("   ✅ Quality section detected")
            if 'trust' in aplus_content.lower():
                print("   ✅ Trust section detected")
                
            # Show first 500 characters
            print(f"\n📝 A+ Content Preview:")
            print(aplus_content[:500] + "..." if len(aplus_content) > 500 else aplus_content)
        else:
            print("   ❌ NO A+ Content generated!")
            
        print(f"\n✅ Test completed for Turkey product {product.id}")
        
    except Exception as e:
        print(f"❌ Error testing Turkey generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_turkey_comprehensive()