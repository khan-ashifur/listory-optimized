"""
Test Current French Listing Quality - Identify 8.86/10 gaps
Analyze backend keywords, A+ content, and mobile readability issues
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

def analyze_french_listing_gaps():
    """Generate fresh French listing and identify remaining gaps"""
    print("🇫🇷 FRENCH LISTING GAP ANALYSIS - Target: 10/10")
    print("🎯 Current: 8.86/10 - Finding remaining optimization gaps")
    print("=" * 80)
    
    try:
        service = ListingGeneratorService()
        optimizer = BackendKeywordOptimizer()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for French luxury with Christmas (best showcase)
        product.marketplace = "fr"
        product.marketplace_language = "fr" 
        product.brand_tone = "luxury"
        product.occasion = "Christmas"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇫🇷 Market: France (luxury + Christmas)")
        print(f"🔄 Generating fresh French listing...")
        
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
            
            # Extract all content
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            description = listing.long_description or ""
            backend_kw = listing.amazon_backend_keywords or ""
            aplus = listing.amazon_aplus_content or ""
            
            print(f"\n🔍 COMPREHENSIVE CONTENT ANALYSIS:")
            print("=" * 60)
            
            # 1. BACKEND KEYWORDS ANALYSIS
            print(f"\n1️⃣ BACKEND KEYWORDS ANALYSIS")
            print(f"📏 Length: {len(backend_kw)}/249 characters")
            print(f"🔑 Content: {backend_kw}")
            
            kw_analysis = optimizer.analyze_keyword_efficiency(backend_kw, 249)
            print(f"\n📊 Backend Analysis:")
            print(f"   Usage: {kw_analysis['usage_percentage']:.1f}%")
            print(f"   Keywords: {kw_analysis['keywords_count']}")
            print(f"   Efficiency: {kw_analysis['efficiency']}")
            
            # Check for conquest terms
            conquest_terms = ['bambou', 'plastique', 'inox', 'bois']
            conquest_found = [term for term in conquest_terms if term in backend_kw.lower()]
            print(f"   Conquest terms: {conquest_found} ({len(conquest_found)}/4)")
            
            # Check for duplicates
            kw_list = [kw.strip() for kw in backend_kw.split(',')]
            duplicates = len(kw_list) - len(set(kw_list))
            print(f"   Duplicates found: {duplicates}")
            
            # 2. BULLETS ANALYSIS
            print(f"\n2️⃣ BULLETS ANALYSIS")
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            print(f"📍 Number of bullets: {len(bullet_list)}")
            
            repetitive_patterns = 0
            dimension_mentions = 0
            competitor_comparisons = 0
            
            for i, bullet in enumerate(bullet_list[:5], 1):
                print(f"\n   BULLET {i}: {bullet[:100]}...")
                
                # Check for repetitive "sans... ni..." pattern
                if 'sans' in bullet.lower() and 'ni' in bullet.lower():
                    repetitive_patterns += 1
                    print(f"      ⚠️ Repetitive 'sans...ni' pattern detected")
                
                # Check for dimensions
                dimension_indicators = ['cm', 'mm', 'x', 'taille', 'dimension']
                if any(dim in bullet.lower() for dim in dimension_indicators):
                    dimension_mentions += 1
                    print(f"      ✅ Contains dimensions/size info")
                
                # Check for competitor comparisons
                competitor_terms = ['bambou', 'plastique', 'inox', 'bois', 'contrairement', 'mieux que', 'supérieur']
                if any(comp in bullet.lower() for comp in competitor_terms):
                    competitor_comparisons += 1
                    print(f"      ✅ Contains competitor comparison")
                
                # Check mobile readability (sentence count)
                sentences = bullet.count('.') + bullet.count('!') + bullet.count('?')
                print(f"      📱 Sentences: {sentences} ({'✅ Mobile-friendly' if 2 <= sentences <= 3 else '❌ Too long/short'})")
            
            print(f"\n📊 Bullets Summary:")
            print(f"   Repetitive patterns: {repetitive_patterns}/5 ({'⚠️ Too many' if repetitive_patterns >= 3 else '✅ Good variety'})")
            print(f"   Dimension mentions: {dimension_mentions}/5 ({'❌ Missing specs' if dimension_mentions == 0 else '✅ Has dimensions'})")
            print(f"   Competitor comparisons: {competitor_comparisons}/5 ({'❌ Missing comparisons' if competitor_comparisons == 0 else '✅ Has comparisons'})")
            
            # 3. A+ CONTENT ANALYSIS
            print(f"\n3️⃣ A+ CONTENT ANALYSIS")
            print(f"📏 A+ Content length: {len(aplus)} characters")
            
            placeholder_indicators = ['[', ']', 'placeholder', 'example', 'insert', 'TBD', 'TODO']
            placeholders_found = sum(aplus.count(indicator) for indicator in placeholder_indicators)
            print(f"   Placeholders found: {placeholders_found} ({'❌ Has placeholders' if placeholders_found > 0 else '✅ No placeholders'})")
            
            # Check for repeated brand copy
            brand_mentions = aplus.lower().count(product.brand_name.lower()) if product.brand_name else 0
            print(f"   Brand mentions: {brand_mentions} ({'⚠️ Repetitive' if brand_mentions > 5 else '✅ Balanced'})")
            
            # Check for consumer-ready content
            consumer_indicators = ['benefits', 'features', 'quality', 'satisfaction', 'guarantee']
            consumer_content = sum(aplus.lower().count(indicator) for indicator in consumer_indicators)
            print(f"   Consumer focus: {consumer_content} mentions ({'❌ Not consumer-ready' if consumer_content < 3 else '✅ Consumer-focused'})")
            
            # 4. DESCRIPTION ANALYSIS  
            print(f"\n4️⃣ DESCRIPTION ANALYSIS")
            print(f"📏 Description length: {len(description)} characters")
            
            # Check mobile formatting
            paragraphs = description.split('\n\n')
            long_paragraphs = sum(1 for p in paragraphs if len(p) > 300)
            print(f"   Long paragraphs (>300 chars): {long_paragraphs} ({'⚠️ Not mobile-optimized' if long_paragraphs > 2 else '✅ Mobile-friendly'})")
            
            # Check for freshness/variation
            repeated_phrases = []
            phrases = description.split('. ')
            for i, phrase in enumerate(phrases):
                if phrase in phrases[i+1:]:
                    repeated_phrases.append(phrase[:50])
            
            print(f"   Repeated phrases: {len(repeated_phrases)} ({'⚠️ Needs freshness' if len(repeated_phrases) > 2 else '✅ Fresh content'})")
            
            # FINAL GAP ASSESSMENT
            print(f"\n🎯 FINAL GAP ASSESSMENT FOR 10/10:")
            print("=" * 50)
            
            gaps = []
            
            # Backend keyword gaps
            if kw_analysis['usage_percentage'] < 95:
                gaps.append("Backend keywords under 95% usage")
            if len(conquest_found) < 4:
                gaps.append("Missing conquest terms in backend")
            if duplicates > 0:
                gaps.append("Backend keyword duplicates")
            
            # Bullet gaps
            if repetitive_patterns >= 3:
                gaps.append("Too many repetitive bullet patterns")
            if dimension_mentions == 0:
                gaps.append("Missing product dimensions in bullets")
            if competitor_comparisons == 0:
                gaps.append("Missing competitor comparisons")
            
            # A+ content gaps
            if placeholders_found > 0:
                gaps.append("A+ content has placeholders")
            if brand_mentions > 5:
                gaps.append("Repetitive brand copy in A+")
            if consumer_content < 3:
                gaps.append("A+ content not consumer-ready")
            
            # Description gaps
            if long_paragraphs > 2:
                gaps.append("Description not mobile-optimized")
            if len(repeated_phrases) > 2:
                gaps.append("Description needs freshness")
            
            print(f"🔍 IDENTIFIED GAPS:")
            for i, gap in enumerate(gaps, 1):
                print(f"   {i}. {gap}")
            
            if len(gaps) == 0:
                print(f"🎉 NO GAPS FOUND! Should be 10/10!")
                return True
            else:
                print(f"\n📈 PRIORITY FIXES NEEDED: {len(gaps)} gaps to address")
                print(f"🎯 Current: 8.86/10 → Target: 10/10")
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
    success = analyze_french_listing_gaps()
    
    if success:
        print(f"\n🎉 FRENCH LISTING IS 10/10 READY!")
    else:
        print(f"\n🔧 GAPS IDENTIFIED - Ready to fix for 10/10!")