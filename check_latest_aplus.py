"""
Check Latest A+ Content Generated for German Market
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.models import GeneratedListing

def check_latest_aplus():
    """Check the latest A+ content generated"""
    print("🔍 CHECKING LATEST A+ CONTENT")
    print("="*50)
    
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
    print(f"🗣️ Language: {getattr(latest_listing.product, 'marketplace_language', 'unknown')}")
    print(f"🎨 Brand Tone: {getattr(latest_listing.product, 'brand_tone', 'unknown')}")
    print(f"💝 Occasion: {getattr(latest_listing.product, 'occasion', 'unknown')}")
    print(f"✅ Status: {latest_listing.status}")
    
    # Check A+ content
    aplus_content = latest_listing.amazon_aplus_content or ""
    
    print(f"\n📊 A+ CONTENT ANALYSIS:")
    print(f"  📏 Length: {len(aplus_content)} characters")
    
    if len(aplus_content) > 0:
        # Check for key sections
        sections_check = {
            "Hero Section": "hero" in aplus_content.lower(),
            "Features": "features" in aplus_content.lower(),
            "Strategy": "strategy" in aplus_content.lower(),
            "PPC": "ppc" in aplus_content.lower(),
            "Visual Templates": "visual" in aplus_content.lower() or "template" in aplus_content.lower(),
            "Keywords": "keyword" in aplus_content.lower(),
            "Trust Builders": "trust" in aplus_content.lower(),
            "FAQs": "faq" in aplus_content.lower() or "questions" in aplus_content.lower()
        }
        
        present_count = sum(1 for present in sections_check.values() if present)
        print(f"  📋 Sections detected: {present_count}/{len(sections_check)}")
        
        for section, present in sections_check.items():
            print(f"    {section}: {'✅' if present else '❌'}")
        
        # Check for German market adaptation
        german_indicators = [
            "germany" in aplus_content.lower(),
            "german" in aplus_content.lower(),
            "deutschland" in aplus_content.lower(),
            "european" in aplus_content.lower(),
        ]
        
        german_adaptation = sum(german_indicators)
        print(f"  🇩🇪 German adaptation indicators: {german_adaptation}/4")
        
        # Show structure overview
        lines = aplus_content.split('\n')
        structural_elements = [
            line.strip() for line in lines[:20] 
            if line.strip() and ('<' in line or 'class=' in line or 'div' in line)
        ]
        
        print(f"  🏗️ HTML structure elements: {len(structural_elements)}")
        
        # Overall quality assessment
        if len(aplus_content) >= 5000 and present_count >= 6:
            print(f"\n🎉 EXCELLENT: A+ content is comprehensive!")
            quality = "Excellent"
        elif len(aplus_content) >= 3000 and present_count >= 4:
            print(f"\n✅ GOOD: A+ content is substantial!")
            quality = "Good"
        elif len(aplus_content) >= 1000 and present_count >= 2:
            print(f"\n⚠️ BASIC: A+ content present but minimal")
            quality = "Basic"
        else:
            print(f"\n❌ POOR: A+ content insufficient")
            quality = "Poor"
        
        print(f"📊 Quality Rating: {quality}")
        print(f"🔢 Content Score: {present_count}/8 sections present")
        print(f"📏 Length Score: {min(len(aplus_content)//1000, 10)}/10")
        
        # Show first 300 characters as preview
        print(f"\n📄 CONTENT PREVIEW:")
        preview = aplus_content[:300].replace('<', '\\<').replace('>', '\\>')
        print(f"   {preview}...")
        
    else:
        print("  ❌ No A+ content found")
        
    # Check other fields for completeness
    print(f"\n📋 OTHER FIELDS CHECK:")
    print(f"  Title: {len(latest_listing.title or '')} chars {'✅' if latest_listing.title else '❌'}")
    print(f"  Description: {len(latest_listing.long_description or '')} chars {'✅' if latest_listing.long_description else '❌'}")
    print(f"  Bullets: {len(latest_listing.bullet_points or '')} chars {'✅' if latest_listing.bullet_points else '❌'}")
    print(f"  Keywords: {len(latest_listing.amazon_backend_keywords or '')} chars {'✅' if latest_listing.amazon_backend_keywords else '❌'}")

if __name__ == "__main__":
    check_latest_aplus()