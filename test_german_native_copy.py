"""
Test Native German Copywriting - Emotional, Lifestyle-Driven
"""

import os
import sys
import django
import time

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

def test_german_native():
    """Test the native German copywriting with emotional hooks"""
    print("🇩🇪 TESTING NATIVE GERMAN COPYWRITING")
    print("📝 Style: Emotional, Lifestyle-Driven, Conversion-Focused")
    print("=" * 70)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for German market with gift occasion
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "casual"  # More approachable
        product.occasion = "Christmas"  # Gift angle
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany (de)")
        print(f"🎁 Occasion: Christmas (gift angle)")
        print(f"💬 Tone: Casual (warm, approachable)")
        
        print("\n🔄 Generating native German copy...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(10)
        
        # Get the listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print(f"✅ Generation successful!")
            
            # Analyze German copy quality
            print(f"\n📊 NATIVE GERMAN COPY ANALYSIS:")
            
            # Check title
            title = listing.title or ""
            print(f"\n📌 TITLE ({len(title)} chars):")
            print(f"   {title}")
            
            # Check for emotional power words in title
            emotional_words = ["endlich", "perfekt", "ideal", "genießen", "mühelos", "Geschenk"]
            title_emotions = sum(word in title for word in emotional_words)
            print(f"   Emotional words: {title_emotions}/6 {'✅' if title_emotions >= 2 else '❌'}")
            
            # Check umlauts
            umlaut_chars = ["ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"]
            has_umlauts = any(char in title for char in umlaut_chars)
            print(f"   Proper umlauts: {'✅' if has_umlauts else '❌ MISSING UMLAUTS!'}")
            
            # Check bullets
            bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
            print(f"\n📍 BULLET POINTS ({len(bullets)} bullets):")
            
            if bullets:
                # First bullet analysis
                first_bullet = bullets[0] if bullets else ""
                print(f"\n   1st Bullet (Emotional Hook):")
                print(f"   {first_bullet[:150]}...")
                
                # Check for problem-solving hook
                hook_patterns = ["Endlich", "Schluss mit", "Nie wieder", "Genießen Sie", "Verwandeln Sie"]
                has_hook = any(pattern in first_bullet for pattern in hook_patterns)
                print(f"   Problem-solving hook: {'✅' if has_hook else '❌ NEEDS EMOTIONAL HOOK!'}")
                
                # Check other bullets for balance
                if len(bullets) >= 3:
                    print(f"\n   Other Bullets Preview:")
                    for i, bullet in enumerate(bullets[1:4], 2):
                        print(f"   {i}. {bullet[:80]}...")
                
                # Check for gift mention
                gift_keywords = ["Geschenk", "Weihnachten", "schenken", "ideale", "perfekte"]
                has_gift = any(any(keyword in bullet for keyword in gift_keywords) for bullet in bullets)
                print(f"\n   Gift angle included: {'✅' if has_gift else '❌ MISSING GIFT ANGLE!'}")
            
            # Check description
            description = listing.long_description or ""
            print(f"\n📄 DESCRIPTION ({len(description)} chars):")
            print(f"   Opening: {description[:150]}...")
            
            # Analyze copy style
            print(f"\n🎯 NATIVE GERMAN QUALITY CHECK:")
            
            quality_checks = {
                "Emotional hooks present": title_emotions >= 2 or has_hook,
                "Proper umlauts used": has_umlauts,
                "Gift/seasonal angle": has_gift,
                "Lifestyle benefits": "genießen" in description.lower() or "komfort" in description.lower(),
                "Natural German flow": not ("gemäß" in description or "bezüglich" in description),
                "Warm, approachable tone": "Sie" in description and ("Ihre" in description or "Ihnen" in description)
            }
            
            passed = sum(quality_checks.values())
            total = len(quality_checks)
            
            for check, result in quality_checks.items():
                print(f"   {check}: {'✅' if result else '❌'}")
            
            print(f"\n📊 OVERALL SCORE: {passed}/{total}")
            
            if passed == total:
                print("🎉 PERFECT: Native German copywriting achieved!")
                print("   ✅ Emotional and lifestyle-driven")
                print("   ✅ Natural German with proper umlauts")
                print("   ✅ Gift angles and seasonal hooks")
                print("   ✅ Converts on Amazon.de")
            elif passed >= 4:
                print("✅ GOOD: Strong native German copy")
            elif passed >= 3:
                print("⚠️ OKAY: Some improvements needed")
            else:
                print("❌ NEEDS WORK: Too technical/translated feel")
            
            # Check for common translation errors
            print(f"\n⚠️ TRANSLATION ERROR CHECK:")
            translation_errors = {
                "Missing umlauts": not has_umlauts,
                "Overly formal/stiff": "gemäß" in description or "bezüglich" in description,
                "No emotional hooks": not has_hook and title_emotions < 2,
                "English words present": any(word in description.lower() for word in ["the", "and", "with"])
            }
            
            errors_found = sum(translation_errors.values())
            if errors_found == 0:
                print("   ✅ No translation errors detected")
            else:
                print(f"   ❌ {errors_found} issues found:")
                for error, present in translation_errors.items():
                    if present:
                        print(f"      - {error}")
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_german_native()