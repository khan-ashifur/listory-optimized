"""
Top E-commerce Specialist: Complete French Listing Evaluation
Analyze as expert - identify ALL gaps preventing 10/10 ranking & conversion performance
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

def ecommerce_specialist_analysis():
    """Complete e-commerce specialist evaluation for 10/10 optimization"""
    print("🎯 E-COMMERCE SPECIALIST: COMPLETE FRENCH LISTING ANALYSIS")
    print("📊 Goal: Identify ALL barriers to peak ranking & conversion performance")
    print("=" * 80)
    
    try:
        service = ListingGeneratorService()
        optimizer = BackendKeywordOptimizer()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for French luxury + Christmas (premium showcase)
        product.marketplace = "fr"
        product.marketplace_language = "fr" 
        product.brand_tone = "luxury"
        product.occasion = "Christmas"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇫🇷 Market: France (Luxury + Christmas - Premium segment)")
        print(f"🔄 Generating listing for specialist evaluation...")
        
        # Generate fresh listing for analysis
        service.generate_listing(product.id, 'amazon')
        time.sleep(15)
        
        # Get latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ French listing generated for analysis!")
            
            # Extract all content
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            description = listing.long_description or ""
            backend_kw = listing.amazon_backend_keywords or ""
            aplus = listing.amazon_aplus_content or ""
            
            print(f"\n📋 SPECIALIST EVALUATION FRAMEWORK:")
            print("=" * 60)
            
            # 1. BACKEND KEYWORDS SPECIALIST ANALYSIS
            print(f"\n🔍 1. BACKEND KEYWORDS OPTIMIZATION AUDIT")
            print(f"🎯 Target: Maximum organic reach + competitor conquest")
            
            kw_analysis = optimizer.analyze_keyword_efficiency(backend_kw, 249)
            print(f"📊 Current Performance:")
            print(f"   • Usage: {kw_analysis['usage_percentage']:.1f}% of 249 chars")
            print(f"   • Keywords: {kw_analysis['keywords_count']} terms")
            print(f"   • Content: {backend_kw[:100]}...")
            
            # Specialist keyword audit
            specialist_gaps = []
            
            # Check conquest coverage
            conquest_must_have = ['bambou', 'plastique', 'inox', 'bois', 'alternative', 'mieux', 'superieur']
            conquest_found = [term for term in conquest_must_have if term in backend_kw.lower()]
            conquest_coverage = len(conquest_found) / len(conquest_must_have) * 100
            print(f"   • Conquest Coverage: {conquest_coverage:.1f}% ({len(conquest_found)}/{len(conquest_must_have)})")
            if conquest_coverage < 70:
                specialist_gaps.append(f"Low conquest coverage: {conquest_coverage:.1f}%")
            
            # Check typo variants
            typo_pairs = [('qualité', 'qualite'), ('français', 'francais'), ('électrique', 'electrique')]
            typo_coverage = sum(1 for orig, typo in typo_pairs if orig in backend_kw and typo in backend_kw) / len(typo_pairs) * 100
            print(f"   • Typo Variants: {typo_coverage:.1f}% coverage")
            if typo_coverage < 60:
                specialist_gaps.append(f"Missing typo variants: {typo_coverage:.1f}%")
            
            # Check space efficiency
            if kw_analysis['usage_percentage'] < 95:
                specialist_gaps.append(f"Wasted space: {249-kw_analysis['current_length']} chars unused")
            
            # 2. BULLET POINTS SPECIALIST ANALYSIS  
            print(f"\n🔍 2. BULLET POINTS CONVERSION AUDIT")
            print(f"🎯 Target: Maximum scan-ability + persuasion + differentiation")
            
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            bullet_gaps = []
            
            for i, bullet in enumerate(bullet_list[:5], 1):
                print(f"\n   BULLET {i} ANALYSIS:")
                print(f"   📝 Content: {bullet[:80]}...")
                
                # Length analysis
                length = len(bullet)
                print(f"   📏 Length: {length} chars ({'✅ Optimal' if 180 <= length <= 250 else '❌ Non-optimal'})")
                if not (180 <= length <= 250):
                    bullet_gaps.append(f"Bullet {i}: Length {length} (need 180-250)")
                
                # Scan-ability analysis
                sentences = bullet.count('.') + bullet.count('!') + bullet.count('?') + bullet.count('–')
                print(f"   📱 Scan-ability: {sentences} sentences ({'✅ Mobile-friendly' if 2 <= sentences <= 3 else '❌ Poor scan'})")
                if not (2 <= sentences <= 3):
                    bullet_gaps.append(f"Bullet {i}: {sentences} sentences (need 2-3)")
                
                # Power words analysis
                power_words = ['excellence', 'qualité', 'raffinement', 'luxueux', 'premium', 'sophistiqué', 'français']
                power_count = sum(1 for word in power_words if word.lower() in bullet.lower())
                print(f"   💪 Power Words: {power_count} found ({'✅ Strong' if power_count >= 2 else '❌ Weak'})")
                if power_count < 2:
                    bullet_gaps.append(f"Bullet {i}: Only {power_count} power words (need 2+)")
                
                # Benefit clarity
                benefit_indicators = ['pour', 'permet', 'offre', 'garantit', 'assure', 'procure']
                has_clear_benefit = any(indicator in bullet.lower() for indicator in benefit_indicators)
                print(f"   🎁 Benefit Clarity: {'✅ Clear' if has_clear_benefit else '❌ Unclear'}")
                if not has_clear_benefit:
                    bullet_gaps.append(f"Bullet {i}: Benefit not clear")
            
            # 3. A+ CONTENT SPECIALIST ANALYSIS
            print(f"\n🔍 3. A+ CONTENT BUYER-READINESS AUDIT")
            print(f"🎯 Target: Professional buyer-facing content, zero placeholder text")
            
            aplus_gaps = []
            
            # Check for placeholder indicators
            placeholder_terms = ['placeholder', 'insert', 'TBD', 'TODO', '[', ']', 'example', 'template']
            placeholder_count = sum(aplus.lower().count(term.lower()) for term in placeholder_terms)
            print(f"   🚫 Placeholder Content: {placeholder_count} instances ({'✅ Clean' if placeholder_count == 0 else '❌ Has placeholders'})")
            if placeholder_count > 0:
                aplus_gaps.append(f"Contains {placeholder_count} placeholder elements")
            
            # Check for briefing/instruction language
            briefing_terms = ['requirements:', 'module type:', 'image requirements:', 'display', 'show']
            briefing_count = sum(aplus.lower().count(term.lower()) for term in briefing_terms)
            print(f"   📋 Briefing Language: {briefing_count} instances ({'✅ Buyer-focused' if briefing_count <= 5 else '❌ Too instructional'})")
            if briefing_count > 5:
                aplus_gaps.append(f"Contains {briefing_count} briefing/instruction elements")
            
            # Check content substance
            print(f"   📏 Content Length: {len(aplus)} chars ({'✅ Substantial' if len(aplus) > 2000 else '❌ Too brief'})")
            if len(aplus) < 2000:
                aplus_gaps.append(f"A+ content too brief: {len(aplus)} chars")
            
            # 4. TITLE OPTIMIZATION ANALYSIS
            print(f"\n🔍 4. TITLE SEO + CONVERSION AUDIT")
            print(f"🎯 Target: Maximum visibility + click-through optimization")
            
            title_gaps = []
            
            print(f"   📝 Title: {title}")
            print(f"   📏 Length: {len(title)}/200 chars ({'✅ Optimal' if 150 <= len(title) <= 190 else '❌ Non-optimal'})")
            if not (150 <= len(title) <= 190):
                title_gaps.append(f"Length {len(title)} (need 150-190)")
            
            # Check for French sophistication
            french_indicators = ['français', 'française', 'raffiné', 'élégant', 'qualité']
            french_count = sum(1 for word in french_indicators if word in title.lower())
            print(f"   🇫🇷 French Appeal: {french_count} indicators ({'✅ Sophisticated' if french_count >= 2 else '❌ Generic'})")
            if french_count < 2:
                title_gaps.append(f"Lacks French sophistication: {french_count} indicators")
            
            # 5. DESCRIPTION OPTIMIZATION ANALYSIS
            print(f"\n🔍 5. DESCRIPTION PERSUASION AUDIT")
            print(f"🎯 Target: Complete conversion story + mobile optimization")
            
            desc_gaps = []
            
            print(f"   📏 Length: {len(description)} chars ({'✅ Comprehensive' if len(description) > 1000 else '❌ Too brief'})")
            if len(description) < 1000:
                desc_gaps.append(f"Too brief: {len(description)} chars")
            
            # Check story structure
            paragraphs = description.split('\n\n')
            print(f"   📖 Structure: {len(paragraphs)} paragraphs ({'✅ Well-structured' if len(paragraphs) >= 3 else '❌ Poor structure'})")
            if len(paragraphs) < 3:
                desc_gaps.append(f"Poor structure: {len(paragraphs)} paragraphs")
            
            # FINAL SPECIALIST ASSESSMENT
            print(f"\n🏆 E-COMMERCE SPECIALIST: FINAL ASSESSMENT")
            print("=" * 60)
            
            all_gaps = specialist_gaps + bullet_gaps + aplus_gaps + title_gaps + desc_gaps
            
            if len(all_gaps) == 0:
                print(f"🎉 PERFECT 10/10 OPTIMIZATION!")
                print(f"✅ Ready for peak ranking & conversion performance")
                print(f"🚀 No barriers to organic traffic or conversion gains")
                return True
            else:
                print(f"📈 OPTIMIZATION GAPS IDENTIFIED: {len(all_gaps)} issues")
                print(f"🎯 Current Performance: {max(0, 10 - len(all_gaps)*0.5):.1f}/10")
                
                gap_categories = {
                    'Backend Keywords': len([g for g in all_gaps if any(term in g for term in ['conquest', 'typo', 'space'])]),
                    'Bullet Points': len(bullet_gaps),
                    'A+ Content': len(aplus_gaps), 
                    'Title': len(title_gaps),
                    'Description': len(desc_gaps)
                }
                
                print(f"\n🔍 GAPS BY CATEGORY:")
                for category, count in gap_categories.items():
                    if count > 0:
                        print(f"   • {category}: {count} issues")
                
                print(f"\n📋 SPECIFIC IMPROVEMENTS NEEDED:")
                for i, gap in enumerate(all_gaps, 1):
                    print(f"   {i}. {gap}")
                
                print(f"\n💡 SPECIALIST RECOMMENDATIONS:")
                print(f"   🎯 These gaps are limiting organic reach and conversion potential")
                print(f"   📈 Fixing them will unlock significant performance gains")
                print(f"   🔄 Recommend optimization before launch for maximum ROI")
                
                return False
                
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = ecommerce_specialist_analysis()
    
    if success:
        print(f"\n🏆 SPECIALIST VERDICT: 10/10 READY FOR LAUNCH!")
    else:
        print(f"\n🔧 SPECIALIST VERDICT: OPTIMIZATION REQUIRED FOR PEAK PERFORMANCE")