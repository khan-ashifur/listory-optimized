"""
Detailed Turkey A+ Content Verification
Line-by-line analysis of Turkey implementation
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

def detailed_turkey_verification():
    """Detailed line-by-line verification of Turkey A+ content"""
    print("="*80)
    print("DETAILED TURKEY A+ CONTENT VERIFICATION")
    print("="*80)
    
    # Get Turkey product
    turkey_product = Product.objects.filter(marketplace='tr').first()
    if not turkey_product:
        print("No Turkey product found")
        return
    
    print(f"Turkey Product: {turkey_product.name} (ID: {turkey_product.id})")
    
    # Generate listing
    service = ListingGeneratorService()
    listing = service.generate_listing(turkey_product.id, platform='amazon')
    
    print("\nLINE-BY-LINE ANALYSIS:")
    print("-" * 80)
    
    # Check 1: Title
    print(f"\n1. TITLE ({len(listing.title)} chars):")
    print(f"   {listing.title}")
    
    title_quality = "EXCELLENT" if 120 <= len(listing.title) <= 150 else "GOOD" if len(listing.title) >= 100 else "NEEDS WORK"
    print(f"   Quality: {title_quality}")
    
    # Check 2: Bullets
    bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
    print(f"\n2. BULLET POINTS ({len(bullets)} bullets):")
    for i, bullet in enumerate(bullets[:5], 1):
        print(f"   {i}. {bullet}")
    
    bullet_quality = "EXCELLENT" if len(bullets) >= 5 else "GOOD" if len(bullets) >= 3 else "NEEDS WORK"
    print(f"   Quality: {bullet_quality}")
    
    # Check 3: Description
    desc_length = len(listing.long_description) if listing.long_description else 0
    print(f"\n3. DESCRIPTION ({desc_length} chars):")
    if listing.long_description:
        print(f"   Preview: {listing.long_description[:200]}...")
    
    desc_quality = "EXCELLENT" if desc_length >= 1000 else "GOOD" if desc_length >= 500 else "NEEDS WORK"
    print(f"   Quality: {desc_quality}")
    
    # Check 4: Keywords
    keyword_count = len(listing.keywords.split(',')) if listing.keywords else 0
    print(f"\n4. KEYWORDS ({keyword_count} keywords):")
    if listing.keywords:
        keywords = listing.keywords.split(',')[:10]
        print(f"   Sample: {', '.join(keywords)}")
    
    keyword_quality = "EXCELLENT" if keyword_count >= 40 else "GOOD" if keyword_count >= 20 else "NEEDS WORK"
    print(f"   Quality: {keyword_quality}")
    
    # Check 5: A+ Content (MOST IMPORTANT)
    aplus_length = len(listing.amazon_aplus_content) if listing.amazon_aplus_content else 0
    print(f"\n5. A+ CONTENT ({aplus_length} chars):")
    
    if listing.amazon_aplus_content:
        aplus = listing.amazon_aplus_content
        
        # Count sections
        section_count = aplus.count('aplus-section-card')
        print(f"   Sections: {section_count}/8")
        
        # Count English descriptions
        english_count = aplus.count('ENGLISH:')
        print(f"   English descriptions: {english_count}")
        
        # Check for Turkish cultural elements
        turkish_elements = ['aile', 'misafir', 'bayram', 'Türk', 'hijyen', 'kalite']
        found_elements = [elem for elem in turkish_elements if elem in aplus]
        print(f"   Turkish elements: {len(found_elements)}/6 - {found_elements}")
        
        # Check for family-focused content
        family_keywords = ['aile', 'çocuk', 'misafir', 'sofra', 'buluşma']
        family_found = [kw for kw in family_keywords if kw in aplus]
        print(f"   Family focus: {len(family_found)}/5 - {family_found}")
        
        # Check for trust signals
        trust_signals = ['garanti', 'sertifika', 'CE', 'orijinal', 'güven']
        trust_found = [signal for signal in trust_signals if signal in aplus]
        print(f"   Trust signals: {len(trust_found)}/5 - {trust_found}")
        
        # Overall A+ quality
        aplus_score = 0
        if section_count >= 8:
            aplus_score += 30
        if english_count >= 10:
            aplus_score += 30
        if len(found_elements) >= 4:
            aplus_score += 20
        if len(family_found) >= 3:
            aplus_score += 10
        if len(trust_found) >= 3:
            aplus_score += 10
        
        print(f"   A+ Score: {aplus_score}/100")
        
        if aplus_score >= 90:
            aplus_quality = "EXCELLENT - BEATS COMPETITORS"
        elif aplus_score >= 70:
            aplus_quality = "VERY GOOD"
        elif aplus_score >= 50:
            aplus_quality = "GOOD"
        else:
            aplus_quality = "NEEDS WORK"
        
        print(f"   A+ Quality: {aplus_quality}")
    else:
        print("   NO A+ CONTENT GENERATED!")
        aplus_quality = "FAILED"
    
    # Overall Assessment
    print("\n" + "="*80)
    print("FINAL ASSESSMENT")
    print("="*80)
    
    total_score = 0
    components = [
        ("Title", title_quality),
        ("Bullets", bullet_quality), 
        ("Description", desc_quality),
        ("Keywords", keyword_quality),
        ("A+ Content", aplus_quality)
    ]
    
    for component, quality in components:
        if quality == "EXCELLENT" or "BEATS" in quality:
            score = 20
        elif quality == "VERY GOOD":
            score = 16
        elif quality == "GOOD":
            score = 12
        else:
            score = 8
        
        total_score += score
        print(f"{component:12}: {quality:30} ({score}/20)")
    
    print(f"\nTOTAL SCORE: {total_score}/100")
    
    if total_score >= 90:
        final_rating = "EXCELLENT - READY TO BEAT HELIUM 10, JASPER AI, COPYMONKEY"
    elif total_score >= 80:
        final_rating = "VERY GOOD - COMPETITIVE QUALITY"
    elif total_score >= 70:
        final_rating = "GOOD - ABOVE AVERAGE"
    else:
        final_rating = "NEEDS IMPROVEMENT"
    
    print(f"FINAL RATING: {final_rating}")
    
    # Competitive Analysis
    print("\n" + "="*80)
    print("COMPETITIVE ANALYSIS")
    print("="*80)
    
    print("Turkey vs Competitors:")
    print(f"  vs Helium 10:   {'SUPERIOR' if total_score >= 85 else 'COMPETITIVE' if total_score >= 75 else 'BEHIND'}")
    print(f"  vs Jasper AI:   {'SUPERIOR' if total_score >= 85 else 'COMPETITIVE' if total_score >= 75 else 'BEHIND'}")
    print(f"  vs CopyMonkey:  {'SUPERIOR' if total_score >= 85 else 'COMPETITIVE' if total_score >= 75 else 'BEHIND'}")
    print(f"  vs Mexico:      {'MATCHED' if total_score >= 80 else 'CLOSE' if total_score >= 75 else 'BEHIND'}")
    
    return total_score

if __name__ == "__main__":
    score = detailed_turkey_verification()
    print(f"\nFINAL VERIFICATION SCORE: {score}/100")
    
    if score >= 90:
        print("SUCCESS: Turkey implementation is EXCELLENT!")
    elif score >= 80:
        print("SUCCESS: Turkey implementation is VERY GOOD!")
    else:
        print("ATTENTION: Turkey needs optimization")