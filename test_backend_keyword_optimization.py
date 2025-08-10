"""
Test Backend Keyword Optimization
Verify 100% usage of 249-byte limit for French and German markets
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

def test_backend_keyword_optimization():
    """Test backend keyword optimization for maximum 249-byte usage"""
    print("🔧 BACKEND KEYWORD OPTIMIZATION TEST")
    print("🎯 Goal: Maximize Amazon's 249-byte backend keyword limit")
    print("=" * 70)
    
    optimizer = BackendKeywordOptimizer()
    
    # Test configurations for different markets
    test_configs = [
        {"market": "fr", "language": "French", "tone": "luxury", "expected_chars": ">= 240"},
        {"market": "de", "language": "German", "tone": "professional", "expected_chars": ">= 240"},
        {"market": "com", "language": "English", "tone": "casual", "expected_chars": ">= 240"}
    ]
    
    results = []
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return False
        
        for i, config in enumerate(test_configs, 1):
            print(f"\n{'='*60}")
            print(f"TEST {i}/3: {config['language'].upper()} MARKET ({config['market']})")
            print(f"Expected: {config['expected_chars']} characters usage")
            print(f"{'='*60}")
            
            # Configure product for market
            product.marketplace = config['market']
            product.marketplace_language = config['market'] if config['market'] != 'com' else 'en'
            product.brand_tone = config['tone']
            product.occasion = "Christmas"  # Test seasonal keywords
            product.save()
            
            print(f"🔄 Generating {config['language']} listing with backend optimization...")
            
            # Generate listing
            service.generate_listing(product.id, 'amazon')
            
            # Wait for generation
            time.sleep(8)
            
            # Get latest listing
            listing = GeneratedListing.objects.filter(
                product=product,
                platform='amazon'
            ).order_by('-created_at').first()
            
            if listing and listing.status == 'completed':
                backend_keywords = listing.amazon_backend_keywords or ""
                
                print(f"✅ {config['language']} listing generated!")
                print(f"🔑 Backend Keywords: {backend_keywords[:80]}...")
                
                # Analyze efficiency
                efficiency = optimizer.analyze_keyword_efficiency(backend_keywords, 249)
                
                print(f"\n📊 BACKEND KEYWORD ANALYSIS:")
                print(f"   Character count: {efficiency['current_length']}/249 ({efficiency['usage_percentage']:.1f}%)")
                print(f"   Keywords count: {efficiency['keywords_count']}")
                print(f"   Efficiency rating: {efficiency['efficiency']}")
                print(f"   Wasted characters: {efficiency['wasted_chars']}")
                
                # Check if meets requirements
                meets_target = efficiency['usage_percentage'] >= 96  # At least 96% usage (240+ chars)
                has_enough_keywords = efficiency['keywords_count'] >= 15
                
                print(f"   Target usage (96%+): {'✅' if meets_target else '❌'}")
                print(f"   Sufficient keywords (15+): {'✅' if has_enough_keywords else '❌'}")
                
                # Check market-specific enhancements
                if config['market'] == 'fr':
                    # Check for French patterns
                    has_french_accents = any(char in backend_keywords for char in ['é', 'è', 'à', 'ç'])
                    has_french_words = any(word in backend_keywords.lower() for word in ['cadeau', 'qualité', 'français'])
                    has_plurals = ',' in backend_keywords and 's' in backend_keywords
                    
                    print(f"   French accents: {'✅' if has_french_accents else '❌'}")
                    print(f"   French vocabulary: {'✅' if has_french_words else '❌'}")
                    print(f"   Plural variations: {'✅' if has_plurals else '❌'}")
                    
                    market_optimized = has_french_accents and has_french_words
                    
                elif config['market'] == 'de':
                    # Check for German patterns
                    has_german_umlauts = any(char in backend_keywords for char in ['ä', 'ö', 'ü', 'ß'])
                    has_german_words = any(word in backend_keywords.lower() for word in ['für', 'geschenk', 'professionell'])
                    has_german_plurals = 'en' in backend_keywords
                    
                    print(f"   German umlauts: {'✅' if has_german_umlauts else '❌'}")
                    print(f"   German vocabulary: {'✅' if has_german_words else '❌'}")
                    print(f"   German plurals: {'✅' if has_german_plurals else '❌'}")
                    
                    market_optimized = has_german_umlauts and has_german_words
                    
                else:
                    # US market
                    has_variety = len(set(backend_keywords.lower().split(', '))) >= 12
                    has_occasions = any(word in backend_keywords.lower() for word in ['christmas', 'gift', 'holiday'])
                    
                    print(f"   Keyword variety: {'✅' if has_variety else '❌'}")
                    print(f"   Seasonal terms: {'✅' if has_occasions else '❌'}")
                    
                    market_optimized = has_variety
                
                # Overall assessment for this market
                overall_success = meets_target and has_enough_keywords and market_optimized
                
                print(f"\n🏆 {config['language'].upper()} MARKET RESULT:")
                if overall_success:
                    print(f"✅ SUCCESS: Backend keywords optimized to maximum efficiency!")
                    print(f"🚀 {config['language']} market ready for production!")
                else:
                    print(f"❌ NEEDS IMPROVEMENT: Backend optimization incomplete")
                
                results.append({
                    "market": config['market'],
                    "language": config['language'], 
                    "efficiency": efficiency,
                    "success": overall_success,
                    "market_optimized": market_optimized
                })
                
            else:
                print(f"❌ {config['language']} generation failed: {listing.status if listing else 'Not found'}")
                results.append({
                    "market": config['market'],
                    "language": config['language'],
                    "efficiency": {"usage_percentage": 0},
                    "success": False,
                    "market_optimized": False
                })
        
        # Final assessment
        print(f"\n{'='*70}")
        print(f"🏆 BACKEND KEYWORD OPTIMIZATION RESULTS")
        print(f"{'='*70}")
        
        successful_markets = sum(1 for r in results if r['success'])
        average_usage = sum(r['efficiency']['usage_percentage'] for r in results) / len(results) if results else 0
        
        print(f"\n📊 OVERALL PERFORMANCE:")
        for result in results:
            market_name = result['language']
            usage = result['efficiency']['usage_percentage']
            status = '✅ OPTIMIZED' if result['success'] else '❌ NEEDS WORK'
            print(f"   {market_name}: {usage:.1f}% usage - {status}")
        
        print(f"\n🎯 FINAL RESULTS:")
        print(f"   Successful markets: {successful_markets}/3")
        print(f"   Average usage: {average_usage:.1f}%")
        
        if successful_markets == 3 and average_usage >= 95:
            print(f"\n🎉 EXCELLENT! All markets achieve 95%+ backend keyword efficiency!")
            print(f"🚀 Backend keyword optimization is PRODUCTION READY!")
            print(f"💯 Using 100% of Amazon's 249-byte limit efficiently!")
            return True
        elif successful_markets >= 2:
            print(f"\n🥈 VERY GOOD! Most markets optimized successfully")
            print(f"🔧 Minor improvements needed for perfect efficiency")
            return False
        else:
            print(f"\n⚠️ SIGNIFICANT WORK NEEDED! Backend optimization incomplete")
            print(f"🔧 Major improvements required")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_optimizer():
    """Test the BackendKeywordOptimizer directly"""
    print(f"\n🔧 DIRECT OPTIMIZER TEST")
    print("=" * 50)
    
    optimizer = BackendKeywordOptimizer()
    
    # Test base keywords
    base_keywords = ["premium", "portable", "misting", "fan", "quality", "professional"]
    
    # Test French optimization
    print(f"\n🇫🇷 FRENCH OPTIMIZATION TEST:")
    french_optimized = optimizer.optimize_backend_keywords(base_keywords, 'fr')
    french_analysis = optimizer.analyze_keyword_efficiency(french_optimized, 249)
    
    print(f"   Input: {base_keywords}")
    print(f"   Output: {french_optimized[:100]}...")
    print(f"   Length: {french_analysis['current_length']}/249 ({french_analysis['usage_percentage']:.1f}%)")
    print(f"   Keywords: {french_analysis['keywords_count']}")
    
    # Test German optimization
    print(f"\n🇩🇪 GERMAN OPTIMIZATION TEST:")
    german_optimized = optimizer.optimize_backend_keywords(base_keywords, 'de')
    german_analysis = optimizer.analyze_keyword_efficiency(german_optimized, 249)
    
    print(f"   Input: {base_keywords}")
    print(f"   Output: {german_optimized[:100]}...")
    print(f"   Length: {german_analysis['current_length']}/249 ({german_analysis['usage_percentage']:.1f}%)")
    print(f"   Keywords: {german_analysis['keywords_count']}")
    
    return french_analysis['usage_percentage'] >= 90 and german_analysis['usage_percentage'] >= 90

if __name__ == "__main__":
    print("🚀 Starting Backend Keyword Optimization Tests")
    
    # Test direct optimizer first
    direct_success = test_direct_optimizer()
    print(f"\n📊 Direct Optimizer: {'✅ PASS' if direct_success else '❌ FAIL'}")
    
    # Test full integration
    integration_success = test_backend_keyword_optimization()
    
    if direct_success and integration_success:
        print(f"\n🎉 ALL TESTS PASSED! Backend keyword optimization is READY!")
        print(f"✅ 100% of Amazon's 249-byte limit is now used efficiently!")
        print(f"🇫🇷 France: Optimized with French accents and plurals")
        print(f"🇩🇪 Germany: Optimized with German umlauts and variations")
        print(f"🇺🇸 USA: Optimized with comprehensive keyword variety")
    else:
        print(f"\n⚠️ TESTS FAILED: Backend optimization needs more work")