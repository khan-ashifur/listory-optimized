"""
WORKING GENERATOR - BYPASSES API ISSUES
This script generates listings directly and saves them to the database
"""
import os
import sys
import django

# Set up Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

def generate_any_product(product_id):
    """Generate listing for any product ID"""
    try:
        print(f"🔄 Generating listing for product {product_id}...")
        
        # Get product
        product = Product.objects.get(id=product_id)
        print(f"✅ Product: {product.name} ({product.marketplace})")
        
        # Generate using working method
        service = ListingGeneratorService()
        listing = service.generate_listing(product_id, 'amazon')
        
        print(f"✅ SUCCESS! Generated listing ID: {listing.id}")
        print(f"   - Title: {listing.title[:100]}...")
        print(f"   - A+ Content: {len(listing.amazon_aplus_content)} characters")
        print(f"   - Status: {listing.status}")
        
        return {
            'success': True,
            'listing_id': listing.id,
            'title': listing.title,
            'aplus_length': len(listing.amazon_aplus_content),
            'status': listing.status
        }
        
    except Product.DoesNotExist:
        print(f"❌ Product {product_id} not found")
        return {'success': False, 'error': 'Product not found'}
    except Exception as e:
        print(f"❌ Error: {e}")
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    # Generate for the requested product
    result = generate_any_product(12)
    print(f"\nFinal result: {result}")