"""
Debug Turkey A+ Content Generation
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

def test_turkey_aplus():
    """Test Turkey A+ content generation"""
    try:
        print("🇹🇷 Testing Turkey A+ Content Generation...")
        
        # Get a Turkey product or create one
        try:
            product = Product.objects.filter(marketplace='tr').first()
            if not product:
                print("Creating Turkey test product...")
                product = Product.objects.create(
                    name="Gaming Chair Pro",
                    description="Professional gaming chair with ergonomic design",
                    brand_name="TechPro",
                    marketplace='tr',
                    price=499.99,
                    categories="Gaming Furniture",
                    features="Ergonomic, Adjustable, Comfortable"
                )
        except Exception as e:
            print(f"Error with product: {e}")
            return
        
        print(f"✅ Product: {product.name} (ID: {product.id}, Market: {product.marketplace})")
        
        # Generate using service
        service = ListingGeneratorService()
        print("🔄 Generating listing...")
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"✅ Generated listing ID: {listing.id}")
        print(f"   - Title: {listing.title[:100]}...")
        print(f"   - A+ Content length: {len(listing.amazon_aplus_content)} characters")
        
        # Check if A+ content has proper sections
        aplus_content = listing.amazon_aplus_content or ""
        if aplus_content:
            print(f"📋 A+ Content Preview (first 500 chars):")
            print(aplus_content[:500])
            print("...")
            
            # Count sections
            section_count = aplus_content.count('<div class="aplus-section"')
            print(f"🔍 A+ Sections found: {section_count}")
            
            # Check for specific Turkey markers
            if "TURKEY:" in aplus_content:
                print("✅ Turkey-specific content detected")
            else:
                print("⚠️ No Turkey markers found")
                
        else:
            print("❌ No A+ content generated!")
            
        return listing
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_turkey_aplus()