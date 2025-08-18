#!/usr/bin/env python3
"""
URGENT: Test Turkey A+ Content Generation Issue
"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing
from django.contrib.auth.models import User

def urgent_turkey_test():
    print("🚨 URGENT: TESTING TURKEY A+ CONTENT ISSUE")
    print("="*60)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='urgent_test')
    
    # Create Turkey product
    product = Product.objects.create(
        user=test_user,
        name="Premium Translation Earbuds",
        description="AI-powered real-time translation earbuds",
        brand_name="TechFlow",
        brand_tone="professional",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics",
        features="Real-time translation, 40 languages, long battery",
        target_audience="Turkish professionals and families"
    )
    
    try:
        print("🇹🇷 Generating Turkey listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            print(f"✅ Listing ID: {listing.id}")
            
            # Check all A+ content fields
            aplus = listing.amazon_aplus_content
            if aplus:
                print(f"✅ A+ Content EXISTS: {len(aplus)} characters")
                
                # Check for key elements
                if 'Complete A+ Content Strategy' in aplus:
                    print(f"✅ Has 'Complete A+ Content Strategy'")
                else:
                    print(f"❌ Missing 'Complete A+ Content Strategy'")
                
                # Check for ENGLISH: prefix in image descriptions
                english_count = aplus.count('ENGLISH:')
                print(f"🖼️ ENGLISH: prefix count: {english_count}")
                
                # Check for English interface labels
                interface_labels = ['Keywords', 'Image Strategy', 'SEO Focus']
                for label in interface_labels:
                    if label in aplus:
                        print(f"✅ {label}: Found")
                    else:
                        print(f"❌ {label}: Missing")
                        
                # Show first 500 chars
                print(f"\n📄 A+ CONTENT PREVIEW:")
                print(aplus[:500])
                
            else:
                print(f"❌ A+ Content is NULL/EMPTY")
                
        else:
            print(f"❌ No listing generated at all")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        product.delete()

if __name__ == "__main__":
    urgent_turkey_test()