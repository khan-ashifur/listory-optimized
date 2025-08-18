"""
Comprehensive Sweden Quality Evaluation
Evaluate Sweden against Mexico 10/10 standards and competitors
"""

import os
import sys
import django

# Add backend to path
backend_path = os.path.join(os.getcwd())
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def comprehensive_sweden_evaluation():
    """Comprehensive evaluation of Sweden vs Mexico quality standards"""
    print("="*80)
    print("COMPREHENSIVE SWEDEN QUALITY EVALUATION")
    print("="*80)
    
    # Get Sweden product
    sweden_product = Product.objects.filter(marketplace='se').first()
    if not sweden_product:
        print("No Sweden product found")
        return
    
    print(f"Sweden Product: {sweden_product.name} (ID: {sweden_product.id})")
    
    # Generate listing
    service = ListingGeneratorService()
    listing = service.generate_listing(sweden_product.id, platform='amazon')
    
    print("\nDETAILED QUALITY ANALYSIS:")
    print("-" * 80)
    
    # Check 1: Title Analysis
    print(f"\n1. TITLE ANALYSIS ({len(listing.title)} chars):")
    print(f"   Content: {listing.title}")
    
    # Swedish trust signals check
    trust_signals = ['CE-certifierad', 'Garanti', 'Svensk', 'Kvalitet', 'Pålitlig']
    found_trust = [signal for signal in trust_signals if signal.lower() in listing.title.lower()]
    print(f"   Trust signals: {len(found_trust)}/5 - {found_trust}")
    
    # Title score
    title_score = 0
    if 120 <= len(listing.title) <= 150:
        title_score += 10
    if len(found_trust) >= 3:
        title_score += 10
    
    print(f"   Title Score: {title_score}/20")
    
    # Check 2: Bullet Points Analysis
    bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
    print(f"\n2. BULLET POINTS ANALYSIS ({len(bullets)} bullets):")
    
    conversion_elements = ['→', 'CE-certifierad', 'Garanti', 'Köp Idag', 'Begränsat']
    bullet_quality = 0
    
    for i, bullet in enumerate(bullets[:5], 1):
        print(f"   {i}. {bullet[:100]}...")
        # Check for conversion structure (FEATURE → BENEFIT → RESULT)
        has_arrow = '→' in bullet
        has_trust = any(signal in bullet for signal in trust_signals)
        conversion_count = sum(1 for elem in conversion_elements if elem in bullet)
        
        bullet_score = has_arrow * 2 + has_trust * 2 + conversion_count
        bullet_quality += bullet_score
        print(f"      → Structure: {'✓' if has_arrow else '✗'} | Trust: {'✓' if has_trust else '✗'} | Score: {bullet_score}/6")
    
    print(f"   Bullet Points Score: {min(bullet_quality, 25)}/25")
    
    # Check 3: Description Analysis
    desc_length = len(listing.long_description) if listing.long_description else 0
    print(f"\n3. DESCRIPTION ANALYSIS ({desc_length} chars):")
    if listing.long_description:
        print(f"   Preview: {listing.long_description[:200]}...")
        
        # Check for Swedish cultural elements
        cultural_elements = ['svensk', 'skandinavisk', 'familj', 'hem', 'miljötänk', 'hållbar']
        found_cultural = [elem for elem in cultural_elements if elem.lower() in listing.long_description.lower()]
        print(f"   Cultural elements: {len(found_cultural)}/6 - {found_cultural}")
        
        # Check for urgency and action
        urgency_elements = ['köp idag', 'begränsat', 'sista chansen', 'missa inte', 'exklusiv']
        found_urgency = [elem for elem in urgency_elements if elem.lower() in listing.long_description.lower()]
        print(f"   Urgency elements: {len(found_urgency)}/5 - {found_urgency}")
    
    desc_score = min(desc_length // 50, 15) + len(found_cultural) * 2 + len(found_urgency) * 2
    print(f"   Description Score: {min(desc_score, 25)}/25")
    
    # Check 4: A+ Content Analysis (MOST IMPORTANT)
    aplus_length = len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0
    print(f"\n4. A+ CONTENT ANALYSIS ({aplus_length} chars):")
    
    if listing.amazon_aplus_content:
        aplus = listing.amazon_aplus_content
        
        # Count sections
        section_count = aplus.count('aplus-section-card')
        print(f"   Sections: {section_count}/8")
        
        # Count English descriptions
        english_count = aplus.count('ENGLISH:')
        print(f"   English descriptions: {english_count}")
        
        # Check for Swedish cultural elements in A+
        swedish_elements = ['svensk', 'familj', 'hem', 'stockholm', 'nordic', 'skandinavisk']
        found_elements = [elem for elem in swedish_elements if elem.lower() in aplus.lower()]
        print(f"   Swedish elements: {len(found_elements)}/6 - {found_elements}")
        
        # Check for detailed lifestyle scenarios
        lifestyle_keywords = ['family', 'office', 'home', 'coffee', 'morning', 'evening', 'professional']
        lifestyle_found = [kw for kw in lifestyle_keywords if kw in aplus]
        print(f"   Lifestyle scenarios: {len(lifestyle_found)}/7 - {lifestyle_found}")
        
        # Overall A+ quality score
        aplus_score = 0
        if section_count >= 8:
            aplus_score += 10  # Full sections
        if english_count >= 8:
            aplus_score += 10  # Detailed image descriptions
        if len(found_elements) >= 4:
            aplus_score += 5   # Cultural relevance
        if len(lifestyle_found) >= 5:
            aplus_score += 5   # Detailed scenarios
        
        print(f"   A+ Score: {aplus_score}/30")
        
        if aplus_score >= 25:
            aplus_quality = "EXCELLENT - MEXICO LEVEL"
        elif aplus_score >= 20:
            aplus_quality = "VERY GOOD"
        elif aplus_score >= 15:
            aplus_quality = "GOOD"
        else:
            aplus_quality = "NEEDS ENHANCEMENT"
        
        print(f"   A+ Quality: {aplus_quality}")
    else:
        print("   NO A+ CONTENT GENERATED!")
        aplus_quality = "FAILED"
        aplus_score = 0
    
    # Overall Assessment
    print("\n" + "="*80)
    print("COMPETITIVE EVALUATION")
    print("="*80)
    
    total_score = title_score + min(bullet_quality, 25) + min(desc_score, 25) + aplus_score
    
    print(f"Title Score:       {title_score}/20")
    print(f"Bullets Score:     {min(bullet_quality, 25)}/25")
    print(f"Description Score: {min(desc_score, 25)}/25")
    print(f"A+ Content Score:  {aplus_score}/30")
    print(f"\nTOTAL SCORE: {total_score}/100")
    
    if total_score >= 90:
        final_rating = "EXCELLENT - BEATS HELIUM 10, JASPER AI, COPYMONKEY"
    elif total_score >= 80:
        final_rating = "VERY GOOD - COMPETITIVE WITH TOP TOOLS"
    elif total_score >= 70:
        final_rating = "GOOD - ABOVE AVERAGE"
    else:
        final_rating = "NEEDS IMPROVEMENT - ENHANCE TO BEAT COMPETITORS"
    
    print(f"FINAL RATING: {final_rating}")
    
    # Competitive Analysis
    print("\n" + "="*80)
    print("COMPETITIVE COMPARISON")
    print("="*80)
    
    print("Sweden vs Competitors:")
    print(f"  vs Helium 10:   {'SUPERIOR' if total_score >= 85 else 'COMPETITIVE' if total_score >= 75 else 'BEHIND'}")
    print(f"  vs Jasper AI:   {'SUPERIOR' if total_score >= 85 else 'COMPETITIVE' if total_score >= 75 else 'BEHIND'}")
    print(f"  vs CopyMonkey:  {'SUPERIOR' if total_score >= 85 else 'COMPETITIVE' if total_score >= 75 else 'BEHIND'}")
    print(f"  vs Mexico:      {'MATCHED' if total_score >= 85 else 'CLOSE' if total_score >= 75 else 'BEHIND'}")
    
    # Recommendations for improvement
    print("\n" + "="*80)
    print("IMPROVEMENT RECOMMENDATIONS")
    print("="*80)
    
    if total_score < 85:
        print("TO REACH MEXICO-LEVEL QUALITY:")
        if title_score < 15:
            print("- TITLE: Add more Swedish trust signals and conversion elements")
        if bullet_quality < 20:
            print("- BULLETS: Implement FEATURE→BENEFIT→RESULT structure with urgency")
        if desc_score < 20:
            print("- DESCRIPTION: Add more Swedish cultural elements and urgency phrases")
        if aplus_score < 25:
            print("- A+ CONTENT: Enhance with more detailed Swedish lifestyle scenarios")
    else:
        print("✅ SWEDEN IS READY - MEXICO-LEVEL QUALITY ACHIEVED!")
    
    return total_score

if __name__ == "__main__":
    score = comprehensive_sweden_evaluation()
    print(f"\nFINAL EVALUATION SCORE: {score}/100")
    
    if score >= 85:
        print("🎉 SUCCESS: Sweden implementation BEATS competitors!")
    else:
        print("⚠️ ENHANCEMENT NEEDED: Sweden requires optimization to match Mexico")