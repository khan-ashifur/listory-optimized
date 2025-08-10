"""
German Market Check - Verify if Germany is using old optimization
Check backend keyword usage and optimization patterns
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

def test_german_market():
    """Check German market optimization status"""
    print("🇩🇪 GERMAN MARKET OPTIMIZATION CHECK")
    print("🎯 Verifying if Germany is using updated backend optimization")
    print("="*70)
    
    try:
        service = ListingGeneratorService()
        optimizer = BackendKeywordOptimizer()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return False
        
        # Configure for German market
        product.marketplace = "de"
        product.marketplace_language = "de" 
        product.brand_tone = "luxury"
        product.occasion = "Christmas"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany (luxury + Christmas)")
        print(f"🔄 Generating German listing to check optimization...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        time.sleep(15)
        
        # Get latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ German listing generated!")
            
            # Extract content
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            description = listing.long_description or ""
            backend_kw = listing.amazon_backend_keywords or ""
            aplus = listing.amazon_aplus_content or ""
            
            print(f"\n📊 GERMAN OPTIMIZATION ANALYSIS:")
            print("="*50)
            
            # 1. Backend Keywords Analysis
            print(f"\n🔍 1. BACKEND KEYWORDS OPTIMIZATION CHECK:")
            kw_analysis = optimizer.analyze_keyword_efficiency(backend_kw, 249)
            usage = kw_analysis['usage_percentage']
            
            print(f"   • Current Usage: {usage:.1f}% of 249 chars")
            print(f"   • Length: {kw_analysis['current_length']}/249 chars") 
            print(f"   • Keywords Count: {kw_analysis['keywords_count']} terms")
            print(f"   • Efficiency: {kw_analysis['efficiency']}")
            
            if usage < 80:
                print(f"   ❌ LOW USAGE - Germany appears to be using OLD optimization")
                print(f"   🔧 Need to apply NEW backend keyword optimization")
            elif usage < 95:
                print(f"   🔶 MODERATE USAGE - Partial optimization applied") 
                print(f"   🔧 Could benefit from enhanced optimization")
            else:
                print(f"   ✅ HIGH USAGE - Germany has NEW optimization applied")
            
            # Check for German-specific patterns
            print(f"\n🔍 2. GERMAN PATTERNS CHECK:")
            german_terms = ['geschenk', 'weihnachten', 'lüfter', 'ventilator', 'kühlung', 'büro']
            german_found = [term for term in german_terms if term.lower() in backend_kw.lower()]
            
            print(f"   • German terms found: {len(german_found)}/{len(german_terms)}")
            print(f"   • Terms: {german_found}")
            
            # Check for typos (umlaut variants)
            umlaut_pairs = [('für', 'fuer'), ('kühlung', 'kuehlung'), ('lüfter', 'luefter')]
            umlaut_coverage = 0
            for orig, typo in umlaut_pairs:
                if orig in backend_kw and typo in backend_kw:
                    umlaut_coverage += 1
            
            print(f"   • Umlaut variants: {umlaut_coverage}/{len(umlaut_pairs)} pairs")
            
            # Show actual backend keywords
            print(f"\n📋 CURRENT BACKEND KEYWORDS:")
            print(f"   Content: {backend_kw[:150]}...")
            print(f"   Full length: {len(backend_kw)} chars")
            
            # Test what optimized version would look like
            print(f"\n🔧 OPTIMIZATION POTENTIAL:")
            base_keywords = ["handventilator", "mini ventilator", "lüfter", "usb", "akku", "leise", "büro"]
            optimized_kw = optimizer.optimize_backend_keywords(base_keywords, 'de')
            opt_analysis = optimizer.analyze_keyword_efficiency(optimized_kw, 249)
            
            print(f"   • Optimized would be: {opt_analysis['usage_percentage']:.1f}% usage")
            print(f"   • Potential keywords: {opt_analysis['keywords_count']} terms")
            print(f"   • Sample optimized: {optimized_kw[:100]}...")
            
            # 3. Title Analysis
            print(f"\n🔍 3. TITLE ANALYSIS:")
            print(f"   • Length: {len(title)}/200 chars")
            print(f"   • Contains umlauts: {'Yes' if any(c in title for c in 'üäöß') else 'No'}")
            print(f"   • German keywords: {sum(1 for term in german_terms if term.lower() in title.lower())}/{len(german_terms)}")
            
            # 4. Overall Assessment
            print(f"\n🏆 GERMAN MARKET ASSESSMENT:")
            print("="*40)
            
            if usage >= 95:
                print(f"✅ Germany HAS updated optimization (usage: {usage:.1f}%)")
                print(f"🎯 Backend keywords are well optimized")
                status = "OPTIMIZED"
            elif usage >= 80:
                print(f"🔶 Germany has PARTIAL optimization (usage: {usage:.1f}%)")
                print(f"🔧 Could benefit from enhancement")
                status = "PARTIAL"
            else:
                print(f"❌ Germany appears to have OLD optimization (usage: {usage:.1f}%)")
                print(f"🚨 Needs backend keyword optimization update")
                status = "OLD"
            
            print(f"\n💡 RECOMMENDATION:")
            if status == "OLD":
                print(f"   🔧 Apply new backend keyword optimization to Germany")
                print(f"   📈 Could improve from {usage:.1f}% to 95%+ usage")
            elif status == "PARTIAL":
                print(f"   🔧 Fine-tune German backend optimization")
                print(f"   📈 Could improve from {usage:.1f}% to 95%+ usage")
            else:
                print(f"   ✅ Germany is well optimized, no changes needed")
            
            return status
                
        else:
            print(f"❌ German generation failed: {listing.status if listing else 'Not found'}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    result = test_german_market()
    
    if result == "OPTIMIZED":
        print(f"\n✅ GERMANY IS CURRENT: No action needed")
    elif result == "PARTIAL": 
        print(f"\n🔶 GERMANY NEEDS MINOR UPDATES")
    elif result == "OLD":
        print(f"\n🚨 GERMANY NEEDS BACKEND OPTIMIZATION UPDATE")
    else:
        print(f"\n❌ UNABLE TO DETERMINE GERMANY STATUS")