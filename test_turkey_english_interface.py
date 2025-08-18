#!/usr/bin/env python3
"""
Test Turkey A+ Content English Interface Elements
Verify: Keywords, Image Strategy, SEO Focus labels are in English
Verify: Detailed English image descriptions with ENGLISH: prefix
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
from django.contrib.auth.models import User

def test_turkey_english_interface():
    print("🇹🇷 TESTING TURKEY ENGLISH INTERFACE ELEMENTS")
    print("=" * 60)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='english_interface_test')
    
    # Create Turkey product
    product = Product.objects.create(
        user=test_user,
        name="Premium Translation Earbuds",
        description="AI-powered translation earbuds for Turkish market",
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
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing and listing.amazon_aplus_content:
            aplus = listing.amazon_aplus_content
            print(f"✅ A+ Content Generated: {len(aplus):,} characters")
            
            # Check for English interface labels
            english_labels = ['Keywords', 'Image Strategy', 'SEO Focus']
            turkish_labels = ['Anahtar Kelimeler', 'Görsel Strateji', 'SEO Odak']
            
            print(f"\n📋 ENGLISH INTERFACE LABELS:")
            for label in english_labels:
                if label in aplus:
                    print(f"   ✅ {label}: Found")
                else:
                    print(f"   ❌ {label}: Missing")
            
            print(f"\n❌ TURKISH LABELS CHECK (should not be found):")
            for label in turkish_labels:
                if label in aplus:
                    print(f"   ❌ {label}: Still found (should be removed)")
                else:
                    print(f"   ✅ {label}: Correctly removed")
            
            # Check for ENGLISH: prefix in image descriptions
            english_prefix_count = aplus.count('ENGLISH:')
            print(f"\n🖼️ IMAGE DESCRIPTIONS:")
            print(f"   ENGLISH: prefix count: {english_prefix_count}")
            
            if english_prefix_count > 0:
                print(f"   ✅ Found ENGLISH: prefixed descriptions")
                # Show examples
                lines = aplus.split('\n')
                english_lines = [line.strip() for line in lines if 'ENGLISH:' in line]
                for i, line in enumerate(english_lines[:3], 1):
                    if len(line) > 100:
                        print(f"   {i}. {line[:100]}...")
                    else:
                        print(f"   {i}. {line}")
            else:
                print(f"   ⚠️ No ENGLISH: prefixed descriptions found")
            
            # Check section descriptions
            ai_generated_desc = "AI-generated content and optimization"
            if ai_generated_desc in aplus:
                print(f"\n📝 SECTION DESCRIPTIONS:")
                print(f"   ✅ 'AI-generated content and optimization' found")
            else:
                print(f"\n📝 SECTION DESCRIPTIONS:")
                print(f"   ❌ Expected description not found")
            
            # Overall assessment
            english_score = sum(1 for label in english_labels if label in aplus)
            turkish_score = sum(1 for label in turkish_labels if label in aplus)
            
            print(f"\n🏆 INTERFACE ASSESSMENT:")
            print(f"   English Labels: {english_score}/3 ({'✅ PASS' if english_score == 3 else '❌ FAIL'})")
            print(f"   Turkish Labels Removed: {3-turkish_score}/3 ({'✅ PASS' if turkish_score == 0 else '❌ FAIL'})")
            print(f"   ENGLISH: Image Descriptions: {'✅ PASS' if english_prefix_count > 0 else '❌ FAIL'}")
            
            overall_pass = english_score == 3 and turkish_score == 0 and english_prefix_count > 0
            print(f"   OVERALL: {'✅ PASS - English Interface Ready' if overall_pass else '⚠️ NEEDS IMPROVEMENT'}")
            
        else:
            print("❌ No A+ content generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        product.delete()

if __name__ == "__main__":
    test_turkey_english_interface()