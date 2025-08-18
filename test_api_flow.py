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
from apps.listings.models import GeneratedListing

def test_api_flow():
    """Test the exact flow that the API uses"""
    try:
        print("=== API FLOW TEST ===")
        
        # Test with product 7 (the one causing 500 error)
        product_id = 7
        platform = 'amazon'
        
        product = Product.objects.get(id=product_id)
        print(f"Product {product_id}: {product.name}")
        print(f"   Marketplace: {product.marketplace}")
        print(f"   Brand: {product.brand_name}")
        
        # Create listing (same as API does)
        listing = GeneratedListing.objects.create(
            product=product,
            platform=platform,
            status='processing'
        )
        print(f"Created listing with ID: {listing.id}")
        
        # Generate content (same as API does)
        service = ListingGeneratorService()
        service._generate_amazon_listing(product, listing)
        
        # Update status (same as API does)
        listing.status = 'completed'
        listing.save()
        
        print(f"\nGeneration Results:")
        print(f"   - Listing ID: {listing.id}")
        print(f"   - Status: {listing.status}")
        print(f"   - Title length: {len(listing.title) if listing.title else 0}")
        print(f"   - A+ Content length: {len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0}")
        
        return {
            'id': listing.id,
            'status': 'success',
            'title': listing.title,
            'aplus_length': len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0
        }
        
    except Exception as e:
        print(f"Error in API flow test: {e}")
        import traceback
        traceback.print_exc()
        return {'status': 'error', 'error': str(e)}

if __name__ == "__main__":
    result = test_api_flow()
    print(f"\nFinal result: {result}")
