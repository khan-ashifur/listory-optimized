"""
Final German Native Copy Test with Umlauts
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

def final_german_test():
    """Final comprehensive test of German copy with umlauts and emotional hooks"""
    print("🇩🇪 FINAL GERMAN NATIVE COPYWRITING TEST")
    print("📝 Checking: Umlauts + Emotional Hooks + Gift Angles")
    print("=" * 80)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for German market
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "luxury"
        product.occasion = "Valentine's Day"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany")
        print(f"💝 Occasion: Valentine's Day")
        print(f"🎨 Tone: Luxury")
        
        print("\n🔄 Generating final German copy...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(10)
        
        # Get the latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ Generation completed!")
            
            # Comprehensive German quality check
            print(f"\n🏆 COMPREHENSIVE GERMAN QUALITY ASSESSMENT:")
            
            # Title analysis
            title = listing.title or ""
            print(f"\n📌 TITLE: {title}")
            
            # Umlaut check
            german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
            title_umlauts = sum(title.count(char) for char in german_chars)
            print(f"   Umlauts in title: {title_umlauts} ({'✅' if title_umlauts > 0 else '❌'})")
            
            # Emotional words check
            emotional_words = ['endlich', 'genießen', 'perfekt', 'ideal', 'mühelos', 'wunderbar']
            title_emotions = sum(word in title.lower() for word in emotional_words)
            print(f"   Emotional words: {title_emotions} ({'✅' if title_emotions > 0 else '❌'})")
            
            # Bullets analysis
            bullets = listing.bullet_points or ""
            print(f"\n📍 BULLETS:")
            bullet_list = bullets.split('\n')[:3]
            
            for i, bullet in enumerate(bullet_list, 1):
                print(f"   {i}. {bullet[:100]}...")
                
                # Check first bullet for hook
                if i == 1:
                    hooks = ['endlich', 'nie wieder', 'schluss mit', 'verwandeln sie']
                    has_hook = any(hook in bullet.lower() for hook in hooks)
                    print(f"      Problem-solving hook: {'✅' if has_hook else '❌'}")
            
            # Count total umlauts
            total_text = title + bullets
            total_umlauts = sum(total_text.count(char) for char in german_chars)
            print(f"\n🔤 TOTAL UMLAUTS: {total_umlauts}")
            
            # Check for specific German words that need umlauts
            problem_words = {
                'fr ': 'für ', 'grere': 'größere', 'heien': 'heißen',
                'mhelose': 'mühelos', 'qualitat': 'qualität', 'zuverlas': 'zuverlässig'
            }
            
            issues_found = []
            for wrong, correct in problem_words.items():
                if wrong in total_text.lower():
                    issues_found.append(f"'{wrong}' should be '{correct}'")
            
            if issues_found:
                print(f"   ❌ Missing umlauts found: {len(issues_found)} issues")
                for issue in issues_found[:3]:
                    print(f"      - {issue}")
            else:
                print(f"   ✅ No obvious missing umlaut patterns detected")
            
            # Description check
            description = listing.long_description or ""
            desc_umlauts = sum(description.count(char) for char in german_chars)
            print(f"\n📄 DESCRIPTION umlauts: {desc_umlauts}")
            
            # Gift angle check
            gift_words = ['geschenk', 'weihnachten', 'valentinstag', 'schenken']
            has_gift = any(word in (title + bullets + description).lower() for word in gift_words)
            print(f"   Gift angle: {'✅' if has_gift else '❌'}")
            
            # Final score
            criteria = {
                "Title has umlauts": title_umlauts > 0,
                "Title is emotional": title_emotions > 0,
                "First bullet has hook": i == 1 and has_hook if 'has_hook' in locals() else False,
                "Content has umlauts": total_umlauts >= 5,
                "Gift angle included": has_gift,
                "No obvious errors": len(issues_found) == 0
            }
            
            score = sum(criteria.values())
            total_criteria = len(criteria)
            
            print(f"\n📊 FINAL ASSESSMENT:")
            for criterion, passed in criteria.items():
                print(f"   {criterion}: {'✅' if passed else '❌'}")
            
            print(f"\n🏆 SCORE: {score}/{total_criteria}")
            
            if score == total_criteria:
                print("🎉 PERFECT: Native German copy with proper umlauts!")
            elif score >= total_criteria - 1:
                print("🥈 EXCELLENT: High-quality German copy, minor improvements possible")
            elif score >= total_criteria - 2:
                print("🥉 GOOD: Solid German copy, some areas need work")
            else:
                print("⚠️ NEEDS IMPROVEMENT: Several issues to fix")
            
            return score, total_criteria
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            return 0, 6
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 0, 6

if __name__ == "__main__":
    score, total = final_german_test()
    print(f"\n🎯 FINAL RESULT: {score}/{total} ({'PASS' if score >= total - 1 else 'NEEDS WORK'})")