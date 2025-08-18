"""
Debug Frontend Flow - Simulate exact user workflow
"""

import os
import sys
import django
import requests
import json

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.models import GeneratedListing
from django.contrib.auth.models import User

def debug_frontend_flow():
    print("🔍 DEBUGGING FRONTEND FLOW - EXACT USER WORKFLOW")
    print("="*70)
    
    test_user, _ = User.objects.get_or_create(username='frontend_debug')
    
    # STEP 1: Create Product (what user does in form)
    print("\n📝 STEP 1: Creating product...")
    try:
        product_data = {
            "name": "Sensei AI Translation Earbuds",
            "description": "AI-powered translation earbuds",
            "brand_name": "Sensei", 
            "brand_tone": "professional",
            "target_platform": "amazon",
            "marketplace": "tr",
            "marketplace_language": "tr",
            "categories": "Electronics",
            "features": "144 languages, 60H battery, IPX7",
            "target_audience": "Turkish families",
            "user": test_user.id
        }
        
        # API call to create product
        response = requests.post('http://localhost:8000/api/core/products/', json=product_data)
        if response.status_code == 201:
            product_api_data = response.json()
            product_id = product_api_data['id']
            print(f"✅ Product created via API: ID {product_id}")
        else:
            print(f"❌ Product creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Product creation error: {e}")
        return
    
    # STEP 2: Generate Listing (what happens when user clicks generate)
    print(f"\n🤖 STEP 2: Generating listing for Turkey...")
    try:
        response = requests.post(f'http://localhost:8000/api/listings/generate/{product_id}/amazon/')
        if response.status_code == 201 or response.status_code == 200:
            listing_data = response.json()
            listing_id = listing_data['id']
            print(f"✅ Listing generated via API: ID {listing_id}")
            
            # Check if A+ content exists in generation response
            if 'amazon_aplus_content' in listing_data:
                aplus_len = len(listing_data.get('amazon_aplus_content', ''))
                print(f"✅ A+ Content in generation response: {aplus_len} chars")
            else:
                print(f"❌ A+ Content missing from generation response")
                print(f"   Available fields: {list(listing_data.keys())}")
                
        else:
            print(f"❌ Listing generation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Listing generation error: {e}")
        return
    
    # STEP 3: Fetch Listing (what frontend does to display results)
    print(f"\n🌐 STEP 3: Fetching listing for display...")
    try:
        response = requests.get(f'http://localhost:8000/api/listings/generated/{listing_id}/')
        if response.status_code == 200:
            display_data = response.json()
            print(f"✅ Listing fetched for display")
            
            # Check A+ content in display response
            aplus_content = display_data.get('amazon_aplus_content', '')
            if aplus_content:
                print(f"✅ A+ Content in display response: {len(aplus_content)} chars")
                
                # Check content language
                if 'Türk' in aplus_content or 'müşteri' in aplus_content:
                    print(f"✅ Turkish content detected in A+ content")
                elif 'Mexican' in aplus_content or 'México' in aplus_content:
                    print(f"❌ Spanish content detected - language mixing issue!")
                elif 'ENGLISH:' in aplus_content:
                    print(f"❌ English template detected - language issue!")
                else:
                    print(f"⚠️ Unknown language content")
                    
                # Show first 200 chars of A+ content
                print(f"\n📄 A+ CONTENT PREVIEW:")
                print(aplus_content[:200])
                print("...")
                
            else:
                print(f"❌ A+ Content empty or missing in display response")
                print(f"   Available fields: {list(display_data.keys())}")
                
        else:
            print(f"❌ Listing fetch failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
            
    except Exception as e:
        print(f"❌ Listing fetch error: {e}")
        return
    
    # STEP 4: Check database directly
    print(f"\n💾 STEP 4: Checking database directly...")
    try:
        listing = GeneratedListing.objects.get(id=listing_id)
        db_aplus = listing.amazon_aplus_content or ''
        print(f"✅ Database A+ Content: {len(db_aplus)} chars")
        
        if db_aplus:
            print(f"✅ A+ Content exists in database")
            # Check database content language
            if 'Türk' in db_aplus or 'müşteri' in db_aplus:
                print(f"✅ Turkish content in database")
            else:
                print(f"❌ Non-Turkish content in database")
        else:
            print(f"❌ A+ Content empty in database")
            
    except Exception as e:
        print(f"❌ Database check error: {e}")
    
    # STEP 5: Frontend URL simulation
    print(f"\n🖥️ STEP 5: Frontend URL check...")
    print(f"   User should navigate to: http://localhost:3000/results/{listing_id}")
    print(f"   A+ Content tab should show the content")
    
    # Cleanup
    try:
        Product.objects.get(id=product_id).delete()
        print(f"\n🧹 Cleanup: Product {product_id} deleted")
    except:
        pass

if __name__ == "__main__":
    debug_frontend_flow()