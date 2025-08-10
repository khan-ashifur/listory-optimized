"""
Debug where umlauts are being lost
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

def debug_umlauts():
    """Debug where the umlauts are being lost"""
    print("🔍 DEBUGGING UMLAUT PRESERVATION")
    print("=" * 60)
    
    # Get the latest listing
    listing = GeneratedListing.objects.filter(
        platform='amazon'
    ).order_by('-created_at').first()
    
    if not listing:
        print("❌ No listings found")
        return
    
    print(f"📅 Latest listing: {listing.created_at}")
    
    # Test string with umlauts
    test_string = "Höhenverstellbar für größere Bildschirme - müheloser Übergang"
    print(f"\n📝 Test string: {test_string}")
    print(f"   Contains ä: {'ä' in test_string}")
    print(f"   Contains ö: {'ö' in test_string}")
    print(f"   Contains ü: {'ü' in test_string}")
    print(f"   Contains ß: {'ß' in test_string}")
    
    # Check title
    title = listing.title or ""
    print(f"\n📌 TITLE ANALYSIS:")
    print(f"   Title: {title[:80]}...")
    print(f"   Length: {len(title)} chars")
    
    # Character analysis
    print(f"\n🔤 CHARACTER ANALYSIS:")
    
    # Check for specific problem words
    problem_words = {
        "Abkhlung": "Should be 'Abkühlung'",
        "khle": "Should be 'kühle'",
        "heiesten": "Should be 'heißesten'",
        "Sprhnebel": "Should be 'Sprühnebel'",
        "genieen": "Should be 'genießen'",
        "grere": "Should be 'größere'",
        "fr": "Should be 'für'",
        "mheloser": "Should be 'müheloser'"
    }
    
    found_problems = 0
    for wrong, correct in problem_words.items():
        if wrong in title or wrong in listing.bullet_points[:200]:
            print(f"   ❌ Found '{wrong}' - {correct}")
            found_problems += 1
    
    if found_problems == 0:
        print("   ✅ No obvious missing umlauts detected")
    else:
        print(f"   ❌ {found_problems} missing umlaut issues found")
    
    # Check bullet points
    bullets = listing.bullet_points or ""
    print(f"\n📍 BULLET POINTS ANALYSIS:")
    first_bullet = bullets.split('\n')[0] if bullets else ""
    print(f"   First bullet: {first_bullet[:80]}...")
    
    # Count actual umlauts
    umlaut_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
    title_umlauts = sum(title.count(char) for char in umlaut_chars)
    bullets_umlauts = sum(bullets[:500].count(char) for char in umlaut_chars)
    
    print(f"\n📊 UMLAUT COUNT:")
    print(f"   Title umlauts: {title_umlauts}")
    print(f"   Bullets umlauts (first 500 chars): {bullets_umlauts}")
    
    if title_umlauts == 0 and bullets_umlauts == 0:
        print(f"\n❌ CRITICAL ISSUE: No umlauts found at all!")
        print("   This indicates umlauts are being stripped somewhere in the process")
        
        # Show what characters are actually present
        print(f"\n🔍 UNIQUE CHARACTERS IN TITLE:")
        unique_chars = set(title)
        non_ascii = [c for c in unique_chars if ord(c) > 127]
        if non_ascii:
            print(f"   Non-ASCII chars found: {non_ascii}")
        else:
            print(f"   ❌ Only ASCII characters present - all umlauts removed!")
    else:
        print(f"\n✅ Umlauts are preserved in the content")

if __name__ == "__main__":
    debug_umlauts()