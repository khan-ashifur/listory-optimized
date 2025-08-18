"""
Test API Endpoint - Simulate what frontend does
"""

import os
import sys
import django
import requests

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing
from django.contrib.auth.models import User

def test_api_endpoint():
    print("🔍 TESTING API ENDPOINT - SIMULATE FRONTEND")
    print("="*60)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='api_test')
    
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
        # Generate listing (what happens when user clicks generate)
        print("\n📝 STEP 1: Generate listing")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            print(f"✅ Listing generated with ID: {listing.id}")
            print(f"✅ A+ Content length: {len(listing.amazon_aplus_content or '')} chars")
            
            # Test API call (what frontend does)
            print(f"\n🌐 STEP 2: Test API endpoint")
            try:
                # Try to fetch the listing via API
                response = requests.get(f'http://localhost:8000/api/listings/generated/{listing.id}/')
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ API call successful")
                    print(f"📋 API Response keys: {list(data.keys())}")
                    
                    # Check A+ content in API response
                    if 'amazon_aplus_content' in data:
                        aplus_content = data['amazon_aplus_content']
                        if aplus_content:
                            print(f"✅ A+ Content in API: {len(aplus_content)} chars")
                            print(f"📄 A+ Content preview: {aplus_content[:200]}...")
                        else:
                            print(f"❌ A+ Content in API: Empty or None")
                    else:
                        print(f"❌ A+ Content field missing from API response")
                        
                    # Show what frontend would see
                    print(f"\n🖥️ FRONTEND WOULD SEE:")
                    print(f"   Title: {data.get('title', 'Missing')}")
                    print(f"   Description: {len(data.get('long_description', ''))} chars") 
                    print(f"   A+ Content: {len(data.get('amazon_aplus_content', ''))} chars")
                    
                else:
                    print(f"❌ API call failed: {response.status_code}")
                    print(f"❌ Response: {response.text}")
                    
            except Exception as api_error:
                print(f"❌ API call error: {api_error}")
            
            # Check database directly
            print(f"\n💾 STEP 3: Check database directly")
            db_listing = GeneratedListing.objects.get(id=listing.id)
            print(f"✅ Database A+ Content: {len(db_listing.amazon_aplus_content or '')} chars")
            
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        product.delete()

if __name__ == "__main__":
    test_api_endpoint()