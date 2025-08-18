"""
Test API A+ Content Response
"""

import os
import sys
import django
import json

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.models import GeneratedListing
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def test_api_response():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='test_api_response')
    
    print("🔍 TESTING API A+ CONTENT RESPONSE")
    print("="*60)
    
    # Create product for Turkey market
    product = Product.objects.create(
        user=test_user,
        name="Premium Wireless Headphones",
        description="High-quality wireless headphones",
        brand_name="SoundMaster", 
        brand_tone="premium",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics/Audio/Headphones",
        features="Active Noise Cancellation, 40H Battery",
        target_audience="Turkish professionals",
        occasion="kurban_bayrami"
    )
    
    try:
        print("🔄 Generating listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            print("✅ Listing generated successfully!")
            
            # Simulate what the API would return (using correct field names)
            api_response = {
                'id': listing.id,
                'platform': listing.platform,
                'status': listing.status,
                'title': listing.title,
                'bullet_points': listing.bullet_points,
                'long_description': listing.long_description,
                'amazon_aplus_content': listing.amazon_aplus_content,
                'amazon_keywords': listing.amazon_keywords,
                'amazon_backend_keywords': listing.amazon_backend_keywords,
            }
            
            print(f"\n📊 API RESPONSE STRUCTURE:")
            for key, value in api_response.items():
                if value:
                    if key == 'amazon_aplus_content':
                        print(f"✅ {key}: {len(str(value))} characters")
                        # Check if it contains strategy content
                        if 'Complete A+ Content Strategy' in str(value):
                            print(f"   ✅ Contains strategy content")
                        else:
                            print(f"   ❌ Missing strategy content")
                    else:
                        print(f"✅ {key}: {len(str(value))} characters")
                else:
                    print(f"❌ {key}: None/Empty")
            
            # Check the database field directly
            print(f"\n🗄️ DATABASE FIELD CHECK:")
            fresh_listing = GeneratedListing.objects.get(id=listing.id)
            if fresh_listing.amazon_aplus_content:
                print(f"✅ Database amazon_aplus_content: {len(fresh_listing.amazon_aplus_content)} characters")
                if 'Complete A+ Content Strategy' in fresh_listing.amazon_aplus_content:
                    print(f"   ✅ Strategy content exists in database")
                else:
                    print(f"   ❌ Strategy content missing in database")
            else:
                print(f"❌ Database amazon_aplus_content: None/Empty")
                
            # Check for recent changes or truncation
            if listing.amazon_aplus_content and len(listing.amazon_aplus_content) < 1000:
                print(f"\n⚠️ WARNING: A+ content seems very short ({len(listing.amazon_aplus_content)} chars)")
                print(f"📄 Content preview: {listing.amazon_aplus_content[:500]}")
                
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    test_api_response()