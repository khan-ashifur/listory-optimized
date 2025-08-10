"""
Debug A+ Content Generation for International Markets
Check what the AI is actually generating for A+ content
"""

import os
import sys
import django
import json

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.models import GeneratedListing

def debug_aplus_content():
    """Debug what's in the A+ content fields"""
    print("🔍 DEBUGGING A+ CONTENT GENERATION")
    print("="*60)
    
    # Get the latest listing
    latest_listing = GeneratedListing.objects.filter(
        platform='amazon'
    ).order_by('-created_at').first()
    
    if not latest_listing:
        print("❌ No listings found")
        return
    
    print(f"📅 Latest listing: {latest_listing.created_at}")
    print(f"📦 Product: {latest_listing.product.name}")
    print(f"🌍 Marketplace: {getattr(latest_listing.product, 'marketplace', 'unknown')}")
    
    # Check A+ content related fields
    print(f"\n📊 A+ CONTENT FIELDS ANALYSIS:")
    
    # 1. Check hero fields
    print(f"\n1️⃣ HERO SECTION:")
    print(f"   hero_title: {latest_listing.hero_title[:100] if latest_listing.hero_title else 'None'}")
    print(f"   hero_content: {latest_listing.hero_content[:200] if latest_listing.hero_content else 'None'}...")
    
    # 2. Check features
    print(f"\n2️⃣ FEATURES:")
    print(f"   features: {latest_listing.features[:200] if latest_listing.features else 'None'}...")
    
    # 3. Check trust builders
    print(f"\n3️⃣ TRUST BUILDERS:")
    print(f"   trust_builders: {latest_listing.trust_builders[:200] if latest_listing.trust_builders else 'None'}...")
    
    # 4. Check FAQs
    print(f"\n4️⃣ FAQs:")
    print(f"   faqs: {latest_listing.faqs[:200] if latest_listing.faqs else 'None'}...")
    
    # 5. Check the actual A+ content HTML
    print(f"\n5️⃣ A+ CONTENT HTML:")
    aplus_html = latest_listing.amazon_aplus_content or ""
    print(f"   Length: {len(aplus_html)} characters")
    
    # Look for actual content vs template
    is_template = "Complete A+ content plan" in aplus_html
    has_actual_hero = latest_listing.hero_title and len(latest_listing.hero_title) > 20
    has_actual_features = latest_listing.features and len(latest_listing.features) > 50
    
    print(f"\n🔍 CONTENT TYPE DETECTION:")
    print(f"   Is using template: {'❌ YES (Static)' if is_template else '✅ NO (Dynamic)'}")
    print(f"   Has actual hero content: {'✅' if has_actual_hero else '❌'}")
    print(f"   Has actual features: {'✅' if has_actual_features else '❌'}")
    
    # Check if A+ sections exist in HTML
    if aplus_html:
        sections_in_html = {
            "Hero Module": "section1_hero" in aplus_html or "hero-module" in aplus_html,
            "Features Module": "section2_features" in aplus_html or "features-module" in aplus_html,
            "Trust Module": "section3_trust" in aplus_html or "trust-module" in aplus_html,
            "FAQs Module": "section4_faqs" in aplus_html or "faqs-module" in aplus_html,
            "Comparison Module": "section5_comparison" in aplus_html or "comparison-module" in aplus_html
        }
        
        print(f"\n📋 A+ HTML SECTIONS CHECK:")
        for section, present in sections_in_html.items():
            print(f"   {section}: {'✅' if present else '❌'}")
    
    # Extract A+ content data to see what AI generated
    print(f"\n🔬 EXTRACTING A+ PLAN FROM HTML:")
    
    # Try to find the actual content in the HTML
    if "section1_hero" in aplus_html:
        # Extract hero title from HTML
        import re
        hero_match = re.search(r'<h3[^>]*>([^<]+)</h3>', aplus_html)
        if hero_match:
            print(f"   Hero title in HTML: {hero_match.group(1)[:100]}")
        
        # Look for actual product-specific content
        if latest_listing.product.name in aplus_html:
            print(f"   ✅ Product name found in A+ HTML")
        else:
            print(f"   ❌ Product name NOT found in A+ HTML (generic content)")
            
        if latest_listing.product.brand_name in aplus_html:
            print(f"   ✅ Brand name found in A+ HTML")
        else:
            print(f"   ❌ Brand name NOT found in A+ HTML (generic content)")
    
    # Final assessment
    print(f"\n🏆 A+ CONTENT QUALITY ASSESSMENT:")
    
    quality_score = 0
    if len(aplus_html) > 5000:
        quality_score += 3
        print(f"   ✅ Length: Comprehensive ({len(aplus_html)} chars)")
    elif len(aplus_html) > 2000:
        quality_score += 2
        print(f"   ⚠️ Length: Moderate ({len(aplus_html)} chars)")
    else:
        quality_score += 1
        print(f"   ❌ Length: Minimal ({len(aplus_html)} chars)")
    
    if has_actual_hero and has_actual_features:
        quality_score += 3
        print(f"   ✅ Content: Dynamic product-specific")
    elif has_actual_hero or has_actual_features:
        quality_score += 2
        print(f"   ⚠️ Content: Partially dynamic")
    else:
        quality_score += 1
        print(f"   ❌ Content: Static template")
    
    sections_count = sum(1 for present in sections_in_html.values() if present) if aplus_html else 0
    if sections_count >= 4:
        quality_score += 3
        print(f"   ✅ Sections: Complete ({sections_count}/5)")
    elif sections_count >= 2:
        quality_score += 2
        print(f"   ⚠️ Sections: Partial ({sections_count}/5)")
    else:
        quality_score += 1
        print(f"   ❌ Sections: Minimal ({sections_count}/5)")
    
    print(f"\n📊 FINAL SCORE: {quality_score}/9")
    
    if quality_score >= 8:
        print("🎉 EXCELLENT: Full A+ content with dynamic data")
    elif quality_score >= 6:
        print("✅ GOOD: A+ content present but needs enhancement")
    elif quality_score >= 4:
        print("⚠️ BASIC: Minimal A+ content")
    else:
        print("❌ POOR: A+ content not properly generated")

if __name__ == "__main__":
    debug_aplus_content()