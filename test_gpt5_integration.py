import os
import sys
import django

# Set up Django environment
sys.path.insert(0, 'backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

print("Testing GPT-5 Integration in Listory AI...")
print("=" * 50)

# Initialize the service
service = ListingGeneratorService()

if service.client:
    print("✅ OpenAI client initialized successfully")
    
    # Get or create a test product
    try:
        product = Product.objects.first()
        if product:
            print(f"\nTesting with product: {product.name}")
            print(f"Product ID: {product.id}")
            
            # Test the generate listing function
            print("\nGenerating Amazon listing with GPT-5...")
            
            try:
                listing_id = service.generate_listing(product.id, 'amazon')
                print(f"✅ Listing generation initiated! ID: {listing_id}")
                
                # Check the listing
                from apps.listings.models import GeneratedListing
                listing = GeneratedListing.objects.get(id=listing_id)
                
                print(f"\nListing Status: {listing.status}")
                if listing.title:
                    print(f"Title Generated: {listing.title[:100]}...")
                if listing.bullet_points:
                    print(f"Bullet Points: {listing.bullet_points[:200]}...")
                    
            except Exception as e:
                print(f"❌ Error generating listing: {e}")
                
        else:
            print("No products found in database. Creating a test product...")
            
            # Create a test product
            product = Product.objects.create(
                name="Premium Wireless Bluetooth Headphones",
                description="High-quality noise-cancelling headphones with 30-hour battery life",
                category="Electronics",
                brand="TestBrand",
                price=99.99,
                current_stock=100
            )
            print(f"✅ Test product created: {product.name}")
            
            # Now test with the new product
            print("\nGenerating Amazon listing with GPT-5...")
            try:
                listing_id = service.generate_listing(product.id, 'amazon')
                print(f"✅ Listing generation initiated! ID: {listing_id}")
            except Exception as e:
                print(f"❌ Error generating listing: {e}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
else:
    print("❌ OpenAI client not initialized - check API key in .env file")

print("\n" + "=" * 50)
print("GPT-5 Integration Test Complete!")