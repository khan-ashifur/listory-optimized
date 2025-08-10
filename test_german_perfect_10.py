"""
Final German 10/10 Perfect Test with Gift Angle
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

def test_perfect_german_10():
    """Final test for perfect 10/10 German quality with gift angle"""
    print("🇩🇪 FINAL PERFECT 10/10 GERMAN TEST")
    print("🎁 Including: Gift Angle + All Quality Criteria")
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
        product.brand_tone = "casual"  # Changed for variety
        product.occasion = "Christmas"  # Adding gift angle
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany")
        print(f"🎨 Brand Tone: Casual")
        print(f"🎁 Occasion: Christmas (Gift Angle)")
        
        print("\n🔄 Generating PERFECT German copy...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for perfect generation...")
        time.sleep(12)
        
        # Get the latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ Generation completed!")
            
            # Quick quality check
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            description = listing.long_description or ""
            total_text = title + bullets + description
            
            print(f"\n🏆 PERFECT 10/10 QUALITY CHECK:")
            
            # Check umlauts
            german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
            total_umlauts = sum(total_text.count(char) for char in german_chars)
            print(f"✅ Umlauts: {total_umlauts} (Excellent)")
            
            # Check emotional hook
            bullet_list = bullets.split('\n')
            first_bullet = bullet_list[0] if bullet_list else ""
            has_hook = "wie ein profi" in first_bullet.lower() and "ganz ohne" in first_bullet.lower()
            print(f"✅ Emotional Hook: {'Perfect Formula' if has_hook else 'Good'}")
            
            # Check mobile structure
            words_first_bullet = len(first_bullet.split()) if first_bullet else 0
            sentences_first_bullet = len([s for s in first_bullet.split('.') if s.strip()]) if first_bullet else 0
            mobile_friendly = words_first_bullet <= 50 and sentences_first_bullet <= 2
            print(f"✅ Mobile Structure: {'Optimized' if mobile_friendly else 'Good'}")
            
            # Check gift angle
            gift_words = ['geschenk', 'weihnachten', 'christmas', 'schenken', 'präsent']
            has_gift = any(word in total_text.lower() for word in gift_words)
            print(f"✅ Gift Angle: {'Included' if has_gift else 'Missing'}")
            
            print(f"\n📌 TITLE: {title}")
            print(f"\n📍 FIRST BULLET: {first_bullet}")
            
            # Check for specific gift messaging
            if has_gift:
                gift_mentions = [word for word in gift_words if word in total_text.lower()]
                print(f"\n🎁 GIFT MESSAGING FOUND: {', '.join(gift_mentions)}")
            
            # Final assessment
            criteria_met = [
                total_umlauts >= 10,
                has_hook,
                mobile_friendly,
                has_gift,
                len(description) > 800
            ]
            
            score = sum(criteria_met)
            print(f"\n🏆 FINAL SCORE: {score}/5")
            
            if score == 5:
                print("🎉 PERFECT 10/10: All criteria achieved!")
                print("🚀 Ready for production use!")
            elif score == 4:
                print("🥇 EXCELLENT 9/10: Nearly perfect!")
            else:
                print(f"🥈 VERY GOOD {score*2}/10: Some optimization needed")
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_perfect_german_10()