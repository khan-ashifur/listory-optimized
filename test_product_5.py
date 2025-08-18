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

def test_product_5():
    try:
        # Get product 5
        product = Product.objects.get(id=5)
        print(f"✅ Product 5: {product.name}")
        print(f"   Marketplace: {product.marketplace}")
        print(f"   Brand: {product.brand_name}")
        
        # Test the generation
        service = ListingGeneratorService()
        print(f"\n🔄 Generating listing for product 5...")
        
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"\n📊 Generation Results:")
        print(f"   - Listing ID: {listing.id}")
        print(f"   - Status: {listing.status}")
        print(f"   - Title length: {len(listing.title) if listing.title else 0}")
        print(f"   - A+ Content length: {len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0}")
        
        print(f"\n✅ Test completed successfully for product 5")
        return True
        
    except Exception as e:
        print(f"❌ Error testing product 5: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_product_5()