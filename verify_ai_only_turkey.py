#!/usr/bin/env python3
"""
Verify Turkey A+ Content is AI-only (no fallback sections)
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

def verify_turkey_ai_only():
    print("🇹🇷 VERIFYING TURKEY A+ CONTENT IS AI-ONLY")
    print("=" * 60)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='ai_only_test')
    
    # Create Turkey product
    product = Product.objects.create(
        user=test_user,
        name="AI Test Product Turkey",
        description="Testing AI-only content generation",
        brand_name="AITestBrand",
        brand_tone="professional",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics",
        features="AI-generated features only",
        target_audience="Turkish customers"
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing and listing.amazon_aplus_content:
            aplus = listing.amazon_aplus_content
            print(f"✅ A+ Content Generated: {len(aplus):,} characters")
            
            # Check for fallback indicators
            fallback_indicators = [
                "Default section with detailed content and optimization",
                "premium quality, trusted brand, customer satisfaction",
                "ENGLISH: Turkish family lifestyle image showing product in use"
            ]
            
            fallback_found = []
            for indicator in fallback_indicators:
                if indicator in aplus:
                    fallback_found.append(indicator)
            
            if fallback_found:
                print("❌ FALLBACK DETECTED:")
                for fb in fallback_found:
                    print(f"   • {fb}")
                print("\n❌ RESULT: Using fallback sections (NOT AI-only)")
            else:
                print("✅ NO FALLBACK DETECTED")
                print("✅ RESULT: Pure AI-generated content")
                
            # Check content structure
            section_count = aplus.count('<div class="aplus-section-card')
            strategy_sections = aplus.count('Complete A+ Content Strategy')
            
            print(f"\n📊 Content Analysis:")
            print(f"   Section cards: {section_count}")
            print(f"   Strategy sections: {strategy_sections}")
            
            # Show first 300 chars to verify
            print(f"\n📄 Content Preview:")
            print(aplus[:300] + "...")
            
        else:
            print("❌ No A+ content generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        product.delete()

if __name__ == "__main__":
    verify_turkey_ai_only()