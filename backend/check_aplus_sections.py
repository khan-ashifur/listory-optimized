#!/usr/bin/env python3
"""
Check what A+ content sections are actually generated.
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def check_aplus_sections():
    """Check what A+ content sections are present in the latest listing."""
    print("🔍 CHECKING A+ CONTENT SECTIONS")
    print("=" * 50)
    
    # Get the most recent listing
    listing = GeneratedListing.objects.filter(platform='amazon').order_by('-created_at').first()
    
    if not listing:
        print("❌ No Amazon listings found")
        return
    
    print(f"📄 Latest Listing: {listing.product.name}")
    print(f"📅 Created: {listing.created_at}")
    
    if listing.amazon_aplus_content:
        print(f"\n🎨 A+ Content Length: {len(listing.amazon_aplus_content)} characters")
        content = listing.amazon_aplus_content.lower()
        
        # Check for specific sections mentioned in the prompt
        sections_to_check = [
            ("hero_section", "hero section"),
            ("features_section", "features section"),
            ("comparison_section", "comparison section"),
            ("usage_section", "usage section"),
            ("lifestyle_section", "lifestyle section"),
            ("aplus_content_suggestions", "content enhancement suggestions"),
            ("ppc strategy", "ppc strategy"),
            ("brand summary", "brand summary")
        ]
        
        print("\n📋 SECTION ANALYSIS:")
        found_sections = []
        missing_sections = []
        
        for section_key, section_name in sections_to_check:
            if section_key in content or section_name in content:
                found_sections.append(section_name)
                print(f"   ✅ {section_name.title()}")
            else:
                missing_sections.append(section_name)
                print(f"   ❌ {section_name.title()}")
        
        print(f"\n📊 SUMMARY:")
        print(f"   Found: {len(found_sections)}/{len(sections_to_check)} sections")
        if missing_sections:
            print(f"   Missing: {', '.join(missing_sections)}")
        
        # Show a sample of the A+ content to understand structure
        print(f"\n📄 A+ CONTENT SAMPLE (first 500 chars):")
        print("-" * 50)
        print(listing.amazon_aplus_content[:500])
        print("...")
        
        # Check if it's HTML or JSON structure
        if listing.amazon_aplus_content.strip().startswith('<'):
            print("\n📝 FORMAT: HTML")
        elif listing.amazon_aplus_content.strip().startswith('{'):
            print("\n📝 FORMAT: JSON")
        else:
            print("\n📝 FORMAT: Unknown")
    else:
        print("❌ No A+ content found")

if __name__ == "__main__":
    check_aplus_sections()