"""
Test Enhanced French Backend Keywords with Conquest Terms
Verify bambou, plastique, inox conquest terms and 240+ character usage
"""

import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.listings.backend_keyword_optimizer import BackendKeywordOptimizer

def test_enhanced_backend_keywords():
    """Test the enhanced French backend keyword optimization"""
    print("🔧 ENHANCED FRENCH BACKEND KEYWORD TEST")
    print("🎯 Testing: Conquest terms (bambou, plastique, inox) + 240+ chars")
    print("=" * 70)
    
    optimizer = BackendKeywordOptimizer()
    
    # Test with typical cutting board keywords
    base_keywords = [
        "planche", "découper", "titane", "cuisine", "premium", 
        "qualité", "hygiénique", "durable", "professionnel"
    ]
    
    print(f"📦 Base keywords: {base_keywords}")
    print(f"🔄 Optimizing for French market...")
    
    # Optimize for French market
    optimized = optimizer.optimize_backend_keywords(
        primary_keywords=base_keywords,
        marketplace='fr',
        product_category='kitchen'
    )
    
    print(f"\n✅ OPTIMIZED FRENCH BACKEND KEYWORDS:")
    print(f"🔑 Result: {optimized}")
    
    # Analyze results
    analysis = optimizer.analyze_keyword_efficiency(optimized, 249)
    
    print(f"\n📊 KEYWORD ANALYSIS:")
    print(f"   Length: {analysis['current_length']}/249 characters")
    print(f"   Usage: {analysis['usage_percentage']:.1f}%")
    print(f"   Keywords count: {analysis['keywords_count']}")
    print(f"   Efficiency: {analysis['efficiency']}")
    print(f"   Wasted chars: {analysis['wasted_chars']}")
    
    # Check for conquest terms
    print(f"\n🎯 CONQUEST TERMS CHECK:")
    conquest_targets = ['bambou', 'plastique', 'inox', 'bois']
    conquest_found = []
    
    for term in conquest_targets:
        if term in optimized.lower():
            conquest_found.append(term)
            print(f"   ✅ {term.upper()}: Found")
        else:
            print(f"   ❌ {term.upper()}: Missing")
    
    # Check for material alternatives
    print(f"\n🔄 ALTERNATIVE TERMS CHECK:")
    alternative_terms = ['alternative', 'remplace', 'mieux', 'superieur', 'sans plastique']
    alternatives_found = []
    
    for term in alternative_terms:
        if term in optimized.lower():
            alternatives_found.append(term)
            print(f"   ✅ {term.upper()}: Found")
        else:
            print(f"   ❌ {term.upper()}: Missing")
    
    # Check for seasonal terms
    print(f"\n🎁 SEASONAL TERMS CHECK:")
    seasonal_terms = ['cadeau', 'noël', 'noel']
    seasonal_found = []
    
    for term in seasonal_terms:
        if term in optimized.lower():
            seasonal_found.append(term)
            print(f"   ✅ {term.upper()}: Found")
        else:
            print(f"   ❌ {term.upper()}: Missing")
    
    # Check for French accents
    print(f"\n🇫🇷 FRENCH ACCENT CHECK:")
    french_chars = ['é', 'è', 'à', 'ç', 'ù', 'â', 'ê', 'î', 'ô', 'û']
    accent_count = sum(optimized.count(char) for char in french_chars)
    print(f"   French accents found: {accent_count} {'✅' if accent_count >= 5 else '❌'}")
    
    # Check for typo variants (no accents)
    print(f"\n📝 TYPO VARIANTS CHECK:")
    if 'qualite' in optimized.lower() and 'qualité' in optimized.lower():
        print(f"   ✅ Both 'qualité' and 'qualite' variants found")
    else:
        print(f"   ❌ Missing typo variants")
    
    # Overall assessment
    print(f"\n🏆 OVERALL ASSESSMENT:")
    
    criteria = {
        "High usage (95%+)": analysis['usage_percentage'] >= 95,
        "Conquest terms (3+)": len(conquest_found) >= 3,
        "Alternative terms (2+)": len(alternatives_found) >= 2,
        "Seasonal terms (1+)": len(seasonal_found) >= 1,
        "French accents (5+)": accent_count >= 5,
        "Many keywords (25+)": analysis['keywords_count'] >= 25
    }
    
    passed = sum(criteria.values())
    total = len(criteria)
    
    for criterion, result in criteria.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {criterion}: {status}")
    
    score = (passed / total) * 100
    print(f"\n📈 FINAL SCORE: {passed}/{total} ({score:.1f}%)")
    
    if score >= 85:
        print(f"🎉 EXCELLENT! Backend keywords fully optimized with conquest terms!")
        print(f"🚀 Ready to capture traffic from bambou/plastique/inox competitors!")
        return True
    elif score >= 70:
        print(f"🥈 GOOD! Most optimization targets achieved")
        return False
    else:
        print(f"⚠️ NEEDS IMPROVEMENT! Major optimization gaps")
        return False

if __name__ == "__main__":
    success = test_enhanced_backend_keywords()
    
    if success:
        print(f"\n✅ Backend keyword optimization is PRODUCTION READY!")
        print(f"🎯 Maximum 249-byte usage with conquest terms!")
    else:
        print(f"\n🔧 Backend keywords need more optimization work")