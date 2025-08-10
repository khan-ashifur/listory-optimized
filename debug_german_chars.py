"""
Debug German Character Detection
Check if German characters are actually present in the generated content
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

def debug_german_characters():
    """Debug German character presence in generated content"""
    print("🔍 DEBUGGING GERMAN CHARACTER DETECTION")
    print("="*60)
    
    # Get the latest German listing
    product = Product.objects.filter(name__icontains="misting fan").first()
    if not product:
        print("❌ No test product found")
        return
        
    listing = GeneratedListing.objects.filter(
        product=product,
        platform='amazon'
    ).order_by('-created_at').first()
    
    if not listing:
        print("❌ No listing found")
        return
    
    print(f"📦 Product: {product.name}")
    print(f"🌍 Market: {product.marketplace} ({product.marketplace_language})")
    print(f"📅 Created: {listing.created_at}")
    
    # Check title
    if listing.title:
        title = listing.title
        print(f"\n📝 TITLE ANALYSIS:")
        print(f"   Content: {title}")
        print(f"   Length: {len(title)} chars")
        
        # Check for German characters
        german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        found_chars = [char for char in german_chars if char in title]
        print(f"   German chars found: {found_chars if found_chars else 'None'}")
        
        # Check all characters with high Unicode values
        unicode_chars = [(char, ord(char)) for char in title if ord(char) > 127]
        print(f"   All Unicode chars: {unicode_chars[:10]}...")  # Show first 10
        
        # Check for common German words
        german_words = ['der', 'die', 'das', 'und', 'mit', 'für', 'von', 'zu', 'ist', 'haben']
        found_words = [word for word in german_words if word.lower() in title.lower()]
        print(f"   German words found: {found_words}")
    
    # Check bullets  
    if listing.bullet_points:
        bullets = listing.bullet_points
        print(f"\n🎯 BULLETS ANALYSIS:")
        print(f"   Length: {len(bullets)} chars")
        
        # Check for German characters
        german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        found_chars = [char for char in german_chars if char in bullets]
        print(f"   German chars found: {found_chars if found_chars else 'None'}")
        
        # Sample bullet
        first_bullet = bullets.split('\n')[0] if '\n' in bullets else bullets[:100]
        print(f"   Sample: {first_bullet}...")
        
        # Check all characters with high Unicode values in first bullet
        unicode_chars = [(char, ord(char)) for char in first_bullet if ord(char) > 127]
        print(f"   Unicode chars in sample: {unicode_chars}")
    
    # Check description
    if listing.long_description:
        desc = listing.long_description
        print(f"\n📄 DESCRIPTION ANALYSIS:")
        print(f"   Length: {len(desc)} chars")
        
        # Check for German characters
        german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
        found_chars = [char for char in german_chars if char in desc]
        print(f"   German chars found: {found_chars if found_chars else 'None'}")
        
        # Sample description
        desc_sample = desc[:200]
        print(f"   Sample: {desc_sample}...")
        
        # Check all characters with high Unicode values in sample
        unicode_chars = [(char, ord(char)) for char in desc_sample if ord(char) > 127]
        print(f"   Unicode chars in sample: {unicode_chars}")
    
    # Overall assessment
    all_text = ' '.join([listing.title or '', listing.bullet_points or '', listing.long_description or ''])
    german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
    total_german_chars = sum(all_text.count(char) for char in german_chars)
    total_unicode_chars = sum(1 for char in all_text if ord(char) > 127)
    
    print(f"\n🏆 OVERALL ASSESSMENT:")
    print(f"   Total text length: {len(all_text)} chars")
    print(f"   German chars (ä,ö,ü,ß): {total_german_chars}")
    print(f"   All Unicode chars: {total_unicode_chars}")
    print(f"   Is German content: {'✅' if total_german_chars > 0 else '❌'}")

if __name__ == "__main__":
    debug_german_characters()