"""
Test Final 10/10 French Listing Quality
Verify all 3 gaps are fixed: backend 95%+, varied bullets, less brand repetition
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
from apps.listings.backend_keyword_optimizer import BackendKeywordOptimizer

def test_final_10_out_of_10():
    """Generate fresh French listing and verify 10/10 quality"""
    print("🇫🇷 FINAL 10/10 FRENCH LISTING TEST")
    print("🎯 Target: Fix all 3 gaps for perfect 10/10 score")
    print("=" * 70)
    
    try:
        service = ListingGeneratorService()
        optimizer = BackendKeywordOptimizer()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return False
        
        # Configure for French luxury with Christmas
        product.marketplace = "fr"
        product.marketplace_language = "fr" 
        product.brand_tone = "luxury"
        product.occasion = "Christmas"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇫🇷 Market: France (luxury + Christmas)")
        print(f"🔄 Generating FINAL optimized French listing...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        time.sleep(15)
        
        # Get latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ French listing generated!")
            
            # Extract content
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            description = listing.long_description or ""
            backend_kw = listing.amazon_backend_keywords or ""
            aplus = listing.amazon_aplus_content or ""
            
            print(f"\n🎯 FINAL 10/10 QUALITY VERIFICATION:")
            print("=" * 50)
            
            # GAP 1: Backend Keywords 95%+
            print(f"\n✅ GAP 1: BACKEND KEYWORDS TARGET 95%+")
            kw_analysis = optimizer.analyze_keyword_efficiency(backend_kw, 249)
            usage = kw_analysis['usage_percentage']
            
            print(f"   Usage: {usage:.1f}%")
            print(f"   Length: {kw_analysis['current_length']}/249 chars")
            print(f"   Keywords: {kw_analysis['keywords_count']}")
            print(f"   Status: {'✅ FIXED' if usage >= 95 else '❌ STILL UNDER 95%'}")
            
            gap1_fixed = usage >= 95
            
            # GAP 2: Bullet Pattern Variety
            print(f"\n✅ GAP 2: BULLET PATTERN VARIETY")
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            sans_ni_count = 0
            patterns_used = []
            
            for i, bullet in enumerate(bullet_list[:5], 1):
                print(f"\n   BULLET {i}: {bullet[:80]}...")
                
                if 'sans' in bullet.lower() and 'ni' in bullet.lower():
                    sans_ni_count += 1
                    patterns_used.append("sans...ni")
                elif 'avec' in bullet.lower() and 'pour' in bullet.lower():
                    patterns_used.append("avec...pour")
                elif 'qui garantit' in bullet.lower() and 'assure' in bullet.lower():
                    patterns_used.append("qui garantit...assure")
                else:
                    patterns_used.append("other")
            
            print(f"\n   Pattern Analysis:")
            print(f"     'sans...ni' count: {sans_ni_count}/5 ({'✅ Good variety' if sans_ni_count <= 2 else '❌ Too repetitive'})")
            print(f"     Unique patterns: {len(set(patterns_used))}/5")
            print(f"     Patterns: {patterns_used}")
            
            gap2_fixed = sans_ni_count <= 2 and len(set(patterns_used)) >= 3
            print(f"   Status: {'✅ FIXED - Good variety' if gap2_fixed else '❌ STILL REPETITIVE'}")
            
            # GAP 3: Brand Repetition in A+
            print(f"\n✅ GAP 3: A+ BRAND REPETITION")
            brand_mentions = aplus.lower().count(product.brand_name.lower()) if product.brand_name else 0
            
            print(f"   Brand mentions: {brand_mentions}")
            print(f"   A+ Content length: {len(aplus)} chars")
            print(f"   Status: {'✅ FIXED - Balanced' if brand_mentions <= 5 else '❌ STILL TOO REPETITIVE'}")
            
            gap3_fixed = brand_mentions <= 5
            
            # FINAL ASSESSMENT
            print(f"\n🏆 FINAL 10/10 ASSESSMENT:")
            print("=" * 40)
            
            all_gaps_fixed = gap1_fixed and gap2_fixed and gap3_fixed
            fixed_count = sum([gap1_fixed, gap2_fixed, gap3_fixed])
            
            print(f"   Gap 1 (Backend 95%+): {'✅ FIXED' if gap1_fixed else '❌ NOT FIXED'}")
            print(f"   Gap 2 (Bullet Variety): {'✅ FIXED' if gap2_fixed else '❌ NOT FIXED'}")
            print(f"   Gap 3 (A+ Brand Balance): {'✅ FIXED' if gap3_fixed else '❌ NOT FIXED'}")
            
            print(f"\n🎯 RESULTS: {fixed_count}/3 gaps fixed")
            
            if all_gaps_fixed:
                print(f"\n🎉 PERFECT! ALL 3 GAPS FIXED!")
                print(f"🇫🇷 French listing should now be 10/10!")
                print(f"✅ Backend keywords: 95%+ usage")
                print(f"✅ Bullets: Varied patterns (no repetition)")
                print(f"✅ A+ Content: Balanced brand mentions")
                print(f"🚀 PRODUCTION READY FOR FRANCE!")
                return True
            else:
                print(f"\n⚠️ STILL NEEDS WORK: {3-fixed_count} gaps remaining")
                if not gap1_fixed:
                    print(f"   🔧 Backend keywords still under 95%")
                if not gap2_fixed:
                    print(f"   🔧 Bullets still too repetitive")
                if not gap3_fixed:
                    print(f"   🔧 A+ content still has too many brand mentions")
                return False
                
        else:
            print(f"❌ French generation failed: {listing.status if listing else 'Not found'}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_final_10_out_of_10()
    
    if success:
        print(f"\n🎉 FRANCE IS NOW 10/10 READY! 🇫🇷")
    else:
        print(f"\n🔧 MORE OPTIMIZATION NEEDED")