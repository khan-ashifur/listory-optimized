"""
Test French Backend Keyword Optimization ONLY
Verify France market gets optimized keywords while USA/Germany remain untouched
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

def test_france_backend_optimization():
    """Test that ONLY France gets backend keyword optimization"""
    print("🇫🇷 FRANCE BACKEND KEYWORD OPTIMIZATION TEST")
    print("🎯 Goal: Optimize ONLY France, keep USA/Germany untouched")
    print("=" * 70)
    
    results = []
    
    try:
        service = ListingGeneratorService()
        optimizer = BackendKeywordOptimizer()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return False
        
        # Test 1: France - SHOULD BE OPTIMIZED
        print(f"\n🇫🇷 TEST 1: FRANCE - SHOULD GET OPTIMIZATION")
        print("=" * 50)
        
        product.marketplace = "fr"
        product.marketplace_language = "fr"
        product.brand_tone = "luxury"
        product.occasion = "Christmas"
        product.save()
        
        print(f"🔄 Generating French listing with backend optimization...")
        service.generate_listing(product.id, 'amazon')
        time.sleep(10)
        
        # Get French listing
        listing_fr = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing_fr and listing_fr.status == 'completed':
            backend_fr = listing_fr.amazon_backend_keywords or ""
            
            print(f"✅ French listing generated!")
            print(f"🔑 French Backend: {backend_fr[:100]}...")
            
            # Analyze French optimization
            fr_analysis = optimizer.analyze_keyword_efficiency(backend_fr, 249)
            
            print(f"\n📊 FRENCH ANALYSIS:")
            print(f"   Length: {fr_analysis['current_length']}/249 ({fr_analysis['usage_percentage']:.1f}%)")
            print(f"   Keywords: {fr_analysis['keywords_count']}")
            print(f"   Efficiency: {fr_analysis['efficiency']}")
            
            # Check for French optimization markers
            has_french_accents = any(char in backend_fr for char in ['é', 'è', 'à', 'ç', 'ù'])
            has_christmas_fr = any(word in backend_fr.lower() for word in ['noël', 'cadeau'])
            has_high_usage = fr_analysis['usage_percentage'] >= 90
            
            print(f"   French accents: {'✅' if has_french_accents else '❌'}")
            print(f"   Christmas terms: {'✅' if has_christmas_fr else '❌'}")
            print(f"   High usage (90%+): {'✅' if has_high_usage else '❌'}")
            
            fr_optimized = has_french_accents and has_high_usage
            print(f"   ✅ France properly optimized: {'YES' if fr_optimized else 'NO'}")
            
            results.append({
                "market": "France",
                "optimized": fr_optimized,
                "usage": fr_analysis['usage_percentage'],
                "keywords": backend_fr
            })
        else:
            print(f"❌ French generation failed")
            results.append({"market": "France", "optimized": False, "usage": 0, "keywords": ""})
        
        # Test 2: USA - SHOULD NOT BE OPTIMIZED (kept original)
        print(f"\n🇺🇸 TEST 2: USA - SHOULD KEEP ORIGINAL")
        print("=" * 50)
        
        product.marketplace = "com"
        product.marketplace_language = "en"
        product.brand_tone = "professional"
        product.occasion = "Christmas"
        product.save()
        
        print(f"🔄 Generating USA listing (should keep original backend)...")
        service.generate_listing(product.id, 'amazon')
        time.sleep(10)
        
        # Get USA listing
        listing_us = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing_us and listing_us.status == 'completed':
            backend_us = listing_us.amazon_backend_keywords or ""
            
            print(f"✅ USA listing generated!")
            print(f"🔑 USA Backend: {backend_us[:100]}...")
            
            # Analyze USA (should be original, not optimized)
            us_analysis = optimizer.analyze_keyword_efficiency(backend_us, 249)
            
            print(f"\n📊 USA ANALYSIS:")
            print(f"   Length: {us_analysis['current_length']}/249 ({us_analysis['usage_percentage']:.1f}%)")
            print(f"   Keywords: {us_analysis['keywords_count']}")
            
            # Check that USA was NOT over-optimized (should be normal)
            is_normal_length = us_analysis['usage_percentage'] < 80  # Should not be maximized
            no_french_chars = not any(char in backend_us for char in ['é', 'è', 'à', 'ç'])
            
            print(f"   Normal length (not maxed): {'✅' if is_normal_length else '❌'}")
            print(f"   No French chars: {'✅' if no_french_chars else '❌'}")
            
            us_untouched = is_normal_length and no_french_chars
            print(f"   ✅ USA kept original: {'YES' if us_untouched else 'NO'}")
            
            results.append({
                "market": "USA",
                "optimized": not us_untouched,  # Should NOT be optimized
                "usage": us_analysis['usage_percentage'],
                "keywords": backend_us
            })
        else:
            print(f"❌ USA generation failed")
            results.append({"market": "USA", "optimized": False, "usage": 0, "keywords": ""})
        
        # Test 3: Germany - SHOULD NOT BE OPTIMIZED (kept original)
        print(f"\n🇩🇪 TEST 3: GERMANY - SHOULD KEEP ORIGINAL")
        print("=" * 50)
        
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "professional"
        product.occasion = "Christmas"
        product.save()
        
        print(f"🔄 Generating Germany listing (should keep original backend)...")
        service.generate_listing(product.id, 'amazon')
        time.sleep(10)
        
        # Get German listing
        listing_de = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing_de and listing_de.status == 'completed':
            backend_de = listing_de.amazon_backend_keywords or ""
            
            print(f"✅ Germany listing generated!")
            print(f"🔑 German Backend: {backend_de[:100]}...")
            
            # Analyze Germany (should be original, not optimized)
            de_analysis = optimizer.analyze_keyword_efficiency(backend_de, 249)
            
            print(f"\n📊 GERMANY ANALYSIS:")
            print(f"   Length: {de_analysis['current_length']}/249 ({de_analysis['usage_percentage']:.1f}%)")
            print(f"   Keywords: {de_analysis['keywords_count']}")
            
            # Check that Germany was NOT over-optimized (should be normal)
            is_normal_length = de_analysis['usage_percentage'] < 80  # Should not be maximized
            has_natural_german = any(word in backend_de.lower() for word in ['für', 'mit', 'und'])
            
            print(f"   Normal length (not maxed): {'✅' if is_normal_length else '❌'}")
            print(f"   Natural German words: {'✅' if has_natural_german else '❌'}")
            
            de_untouched = is_normal_length
            print(f"   ✅ Germany kept original: {'YES' if de_untouched else 'NO'}")
            
            results.append({
                "market": "Germany",
                "optimized": not de_untouched,  # Should NOT be optimized
                "usage": de_analysis['usage_percentage'],
                "keywords": backend_de
            })
        else:
            print(f"❌ Germany generation failed")
            results.append({"market": "Germany", "optimized": False, "usage": 0, "keywords": ""})
        
        # Final Assessment
        print(f"\n{'='*70}")
        print(f"🏆 BACKEND KEYWORD OPTIMIZATION RESULTS")
        print(f"{'='*70}")
        
        for result in results:
            market = result['market']
            usage = result['usage']
            
            if market == "France":
                # France SHOULD be optimized
                status = "✅ OPTIMIZED" if result['optimized'] else "❌ NOT OPTIMIZED"
                expected = "(Should be optimized)"
            else:
                # USA/Germany should NOT be optimized
                status = "✅ UNTOUCHED" if not result['optimized'] else "❌ OVER-OPTIMIZED"  
                expected = "(Should be untouched)"
            
            print(f"   {market}: {usage:.1f}% usage - {status} {expected}")
        
        print(f"\n🎯 VALIDATION RESULTS:")
        
        # Check if implementation is correct
        france_result = next((r for r in results if r['market'] == 'France'), None)
        usa_result = next((r for r in results if r['market'] == 'USA'), None)
        germany_result = next((r for r in results if r['market'] == 'Germany'), None)
        
        france_correct = france_result and france_result['optimized']  # Should be optimized
        usa_correct = usa_result and not usa_result['optimized']      # Should NOT be optimized
        germany_correct = germany_result and not germany_result['optimized']  # Should NOT be optimized
        
        print(f"   France optimized correctly: {'✅' if france_correct else '❌'}")
        print(f"   USA kept original: {'✅' if usa_correct else '❌'}")
        print(f"   Germany kept original: {'✅' if germany_correct else '❌'}")
        
        all_correct = france_correct and usa_correct and germany_correct
        
        if all_correct:
            print(f"\n🎉 PERFECT! Backend keyword optimization working correctly!")
            print(f"✅ France gets optimized keywords (90%+ usage)")
            print(f"✅ USA and Germany keep their working originals")
            print(f"🚀 Implementation is PRODUCTION READY!")
            return True
        else:
            print(f"\n⚠️ ISSUES DETECTED!")
            if not france_correct:
                print(f"   🔧 France needs better optimization")
            if not usa_correct:
                print(f"   🔧 USA should not be optimized (keep original)")
            if not germany_correct:
                print(f"   🔧 Germany should not be optimized (keep original)")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Testing France-Only Backend Keyword Optimization")
    
    success = test_france_backend_optimization()
    
    if success:
        print(f"\n🎉 SUCCESS! France backend keywords optimized, USA/Germany untouched!")
    else:
        print(f"\n⚠️ FAILED! Need to fix implementation")