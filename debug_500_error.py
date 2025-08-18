#!/usr/bin/env python3
"""
Debug script to reproduce the 500 error from frontend
"""
import os
import sys
import django

# Setup Django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

import json
from django.test import Client
from apps.core.models import Product
from apps.listings.services import ListingGeneratorService

def test_full_workflow():
    """Test the complete workflow that the frontend does"""
    print("🧪 TESTING FULL FRONTEND WORKFLOW")
    print("="*60)
    
    client = Client()
    
    # Step 1: Create product (what frontend does)
    product_data = {
        'name': 'N-GEN Professional Kitchen Knife Set 13 Pieces',
        'description': 'Professional kitchen knife set with anti-rust coating',
        'brand_name': 'N-GEN',
        'marketplace': 'se',  # Sweden
        'target_platform': 'amazon',
        'price': 99.99,
        'categories': 'kitchen, knives, cookware',
        'features': 'anti-rust coating, 13 pieces, professional grade',
        'brand_tone': 'professional',
        'occasion': 'everyday',
        'target_keywords': 'kitchen knives, professional knives, knife set',
        'brand_persona': '',
        'target_audience': '',
        'competitor_urls': '',
        'product_urls': '',
        'competitor_asins': '',
        'seo_keywords': '',
        'long_tail_keywords': '',
        'faqs': '',
        'whats_in_box': ''
    }
    
    print("1️⃣ Creating product...")
    try:
        response = client.post(
            '/api/core/products/',
            data=json.dumps(product_data),
            content_type='application/json'
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 201:
            response_data = json.loads(response.content)
            product_id = response_data['id']
            print(f"   ✅ Product created: {product_id}")
        else:
            print(f"   ❌ Failed: {response.content.decode()}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        return False
    
    # Step 2: Generate listing (what frontend does next)
    print("\n2️⃣ Generating listing...")
    try:
        listing_response = client.post(
            f'/api/listings/generate-clean/{product_id}/amazon/',
            data=json.dumps({'platform': 'amazon'}),
            content_type='application/json'
        )
        
        print(f"   Status: {listing_response.status_code}")
        
        if listing_response.status_code == 200:
            listing_data = json.loads(listing_response.content)
            print(f"   ✅ Listing generated: {listing_data.get('id', 'N/A')}")
            print(f"   Title length: {len(listing_data.get('title', ''))}")
            print(f"   A+ content length: {len(listing_data.get('amazon_aplus_content', ''))}")
            return True
        else:
            print(f"   ❌ Failed: {listing_response.content.decode()[:500]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_service():
    """Test the listing service directly"""
    print("\n🔧 TESTING LISTING SERVICE DIRECTLY")
    print("="*60)
    
    try:
        # Create product directly
        from django.contrib.auth.models import User
        user, _ = User.objects.get_or_create(
            username='debug_user',
            defaults={'email': 'debug@test.com'}
        )
        
        product = Product.objects.create(
            user=user,
            name='Debug Kitchen Knife Set',
            description='Test description',
            brand_name='TestBrand',
            marketplace='se',
            target_platform='amazon',
            brand_tone='professional',
            price=99.99
        )
        
        print(f"✅ Product created directly: {product.id}")
        
        # Generate listing directly
        service = ListingGeneratorService()
        listing = service.generate_listing(product.id, platform='amazon')
        
        print(f"✅ Listing generated directly: {listing.id}")
        print(f"   Title: {listing.title[:80]}...")
        print(f"   A+ length: {len(listing.amazon_aplus_content)}")
        
        # Cleanup
        listing.delete()
        product.delete()
        
        return True
        
    except Exception as e:
        print(f"❌ Direct service failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 DEBUGGING 500 ERROR FROM FRONTEND")
    print("="*80)
    
    # Test 1: Full workflow
    workflow_success = test_full_workflow()
    
    # Test 2: Direct service
    direct_success = test_direct_service()
    
    print("\n" + "="*80)
    print("📊 RESULTS:")
    print(f"   Frontend workflow: {'✅ PASS' if workflow_success else '❌ FAIL'}")
    print(f"   Direct service: {'✅ PASS' if direct_success else '❌ FAIL'}")
    
    if workflow_success and direct_success:
        print("\n🎉 NO BACKEND ISSUES FOUND!")
        print("   The 500 error is likely a frontend issue:")
        print("   • Check console logs in browser")
        print("   • Verify frontend is sending correct data")
        print("   • Check CORS settings for port mismatch")
    else:
        print("\n⚠️ BACKEND ISSUES FOUND!")
        print("   Need to fix backend before frontend will work")