"""
Check actual A+ HTML structure being generated
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.listings.models import GeneratedListing

def check_aplus_html():
    """Check the actual A+ HTML structure"""
    print("🔍 CHECKING ACTUAL A+ HTML STRUCTURE")
    print("=" * 60)
    
    # Get the latest listing
    listing = GeneratedListing.objects.filter(
        platform='amazon'
    ).order_by('-created_at').first()
    
    if not listing:
        print("❌ No listings found")
        return
    
    aplus_content = listing.amazon_aplus_content or ""
    
    print(f"📅 Listing: {listing.created_at}")
    print(f"📏 A+ Content Length: {len(aplus_content)} characters")
    
    if aplus_content:
        # Show the first 2000 characters to see the structure
        print(f"\n📄 A+ HTML STRUCTURE (First 2000 chars):")
        print("=" * 60)
        print(aplus_content[:2000])
        print("=" * 60)
        
        # Look for key patterns
        patterns = {
            "aplus-module": aplus_content.count("aplus-module"),
            "section1_hero": aplus_content.count("section1_hero"),
            "section2_features": aplus_content.count("section2_features"),
            "section3_trust": aplus_content.count("section3_trust"),
            "section4_faqs": aplus_content.count("section4_faqs"),
            "hero-module": aplus_content.count("hero-module"),
            "features-module": aplus_content.count("features-module"),
            "English instructions": aplus_content.count("Professional") + aplus_content.count("image") + aplus_content.count("showing"),
            "German content": aplus_content.count("der") + aplus_content.count("die") + aplus_content.count("und")
        }
        
        print(f"\n📊 PATTERN ANALYSIS:")
        for pattern, count in patterns.items():
            print(f"    {pattern}: {count} occurrences")
        
        # Check if it's dynamic content
        has_product_name = listing.product.name.lower() in aplus_content.lower()
        has_brand_name = listing.product.brand_name.lower() in aplus_content.lower()
        
        print(f"\n🎯 DYNAMIC CONTENT CHECK:")
        print(f"    Product name in HTML: {'✅' if has_product_name else '❌'}")
        print(f"    Brand name in HTML: {'✅' if has_brand_name else '❌'}")
        
        # Extract some key content snippets
        import re
        headings = re.findall(r'<h[1-6][^>]*>([^<]+)</h[1-6]>', aplus_content)
        if headings:
            print(f"\n📝 HTML HEADINGS FOUND:")
            for i, heading in enumerate(headings[:5]):
                print(f"    {i+1}. {heading}")
        
    else:
        print("❌ No A+ content found")

if __name__ == "__main__":
    check_aplus_html()