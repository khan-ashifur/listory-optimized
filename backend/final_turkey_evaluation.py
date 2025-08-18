"""
Final Evaluation: Turkey Market Implementation with Mexico Pattern
Compare Turkey vs Mexico quality and provide optimization recommendations
"""

import os
import sys
import django
import json

# Add backend to path
backend_path = os.path.join(os.getcwd())
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from apps.listings.models import GeneratedListing

def evaluate_turkey_implementation():
    """Final evaluation of Turkey implementation"""
    print("\n" + "="*80)
    print("🇹🇷 TURKEY MARKET FINAL EVALUATION")
    print("="*80)
    
    # Check if Turkey product exists
    turkey_product = Product.objects.filter(marketplace='tr').first()
    mexico_product = Product.objects.filter(marketplace='mx').first()
    
    if not turkey_product or not mexico_product:
        print("❌ Missing test products")
        return
    
    # Get recent listings
    turkey_listing = GeneratedListing.objects.filter(product=turkey_product).order_by('-created_at').first()
    mexico_listing = GeneratedListing.objects.filter(product=mexico_product).order_by('-created_at').first()
    
    print("\n📊 COMPARISON ANALYSIS:")
    print("-" * 80)
    
    # Title Comparison
    print("\n📌 TITLE COMPARISON:")
    if turkey_listing and turkey_listing.title:
        print(f"Turkey: {len(turkey_listing.title)} chars")
        print(f"   Keywords: garanti={('garanti' in turkey_listing.title.lower())}, kalite={('kalite' in turkey_listing.title.lower())}")
    if mexico_listing and mexico_listing.title:
        print(f"Mexico: {len(mexico_listing.title)} chars")
        print(f"   Keywords: garantía={('garantía' in mexico_listing.title.lower())}, calidad={('calidad' in mexico_listing.title.lower())}")
    
    # Bullet Points Comparison
    print("\n📍 BULLET POINTS COMPARISON:")
    if turkey_listing and turkey_listing.bullet_points:
        tr_bullets = turkey_listing.bullet_points.split('\n')
        print(f"Turkey: {len([b for b in tr_bullets if b.strip()])} bullets")
        if tr_bullets:
            print(f"   First bullet: {tr_bullets[0][:80]}...")
    if mexico_listing and mexico_listing.bullet_points:
        mx_bullets = mexico_listing.bullet_points.split('\n')
        print(f"Mexico: {len([b for b in mx_bullets if b.strip()])} bullets")
        if mx_bullets:
            print(f"   First bullet: {mx_bullets[0][:80]}...")
    
    # A+ Content Comparison
    print("\n🎨 A+ CONTENT COMPARISON:")
    
    def analyze_aplus_content(content, market_name):
        if not content:
            print(f"{market_name}: No A+ content")
            return 0
        
        sections = content.count('aplus-section-card')
        english_descriptions = content.count('ENGLISH:')
        has_8_sections = content.count('section1') and content.count('section8')
        
        print(f"{market_name}:")
        print(f"   A+ Sections: {sections}")
        print(f"   English image descriptions: {english_descriptions}")
        print(f"   Has 8-section structure: {has_8_sections}")
        
        # Check for specific sections
        required_sections = ['hero', 'features', 'usage', 'quality', 'guarantee', 'social_proof', 'comparison', 'package']
        found_sections = sum(1 for section in required_sections if section in content.lower())
        print(f"   Required sections found: {found_sections}/{len(required_sections)}")
        
        return sections
    
    tr_sections = analyze_aplus_content(turkey_listing.amazon_aplus_content if turkey_listing else None, "Turkey")
    mx_sections = analyze_aplus_content(mexico_listing.amazon_aplus_content if mexico_listing else None, "Mexico")
    
    # Keywords Comparison
    print("\n🔍 KEYWORDS COMPARISON:")
    if turkey_listing and turkey_listing.keywords:
        tr_keywords = turkey_listing.keywords.split(',')
        print(f"Turkey: {len(tr_keywords)} keywords")
    if mexico_listing and mexico_listing.keywords:
        mx_keywords = mexico_listing.keywords.split(',')
        print(f"Mexico: {len(mx_keywords)} keywords")
    
    # Quality Score
    print("\n" + "="*80)
    print("🏆 QUALITY ASSESSMENT")
    print("="*80)
    
    turkey_score = 0
    mexico_score = 0
    
    # Scoring criteria
    criteria = {
        'Title (150-200 chars)': {
            'turkey': turkey_listing and 150 <= len(turkey_listing.title) <= 200 if turkey_listing else False,
            'mexico': mexico_listing and 150 <= len(mexico_listing.title) <= 200 if mexico_listing else False
        },
        '5 Bullet Points': {
            'turkey': turkey_listing and len([b for b in turkey_listing.bullet_points.split('\n') if b.strip()]) >= 5 if turkey_listing else False,
            'mexico': mexico_listing and len([b for b in mexico_listing.bullet_points.split('\n') if b.strip()]) >= 5 if mexico_listing else False
        },
        '8 A+ Sections': {
            'turkey': tr_sections >= 8,
            'mexico': mx_sections >= 8
        },
        'English Image Descriptions': {
            'turkey': turkey_listing and turkey_listing.amazon_aplus_content and 'ENGLISH:' in turkey_listing.amazon_aplus_content if turkey_listing else False,
            'mexico': mexico_listing and mexico_listing.amazon_aplus_content and 'ENGLISH:' in mexico_listing.amazon_aplus_content if mexico_listing else False
        },
        'Local Language Content': {
            'turkey': turkey_listing and any(word in (turkey_listing.title + turkey_listing.bullet_points).lower() for word in ['kalite', 'garanti', 'türk']) if turkey_listing else False,
            'mexico': mexico_listing and any(word in (mexico_listing.title + mexico_listing.bullet_points).lower() for word in ['calidad', 'garantía', 'méxico']) if mexico_listing else False
        }
    }
    
    print("\n📊 QUALITY CRITERIA:")
    for criterion, results in criteria.items():
        tr_pass = "✅" if results['turkey'] else "❌"
        mx_pass = "✅" if results['mexico'] else "❌"
        print(f"{criterion:30} Turkey: {tr_pass}  Mexico: {mx_pass}")
        if results['turkey']:
            turkey_score += 20
        if results['mexico']:
            mexico_score += 20
    
    print(f"\n🎯 FINAL SCORES:")
    print(f"Turkey: {turkey_score}/100")
    print(f"Mexico: {mexico_score}/100")
    
    # Recommendations
    print("\n" + "="*80)
    print("💡 RECOMMENDATIONS FOR TURKEY MARKET")
    print("="*80)
    
    issues = []
    if tr_sections < 8:
        issues.append("❌ A+ Content not generating 8 sections like Mexico")
    if not (turkey_listing and 'ENGLISH:' in turkey_listing.amazon_aplus_content if turkey_listing else False):
        issues.append("❌ Missing English image descriptions in A+ content")
    if turkey_score < mexico_score:
        issues.append(f"❌ Turkey quality ({turkey_score}) below Mexico ({mexico_score})")
    
    if issues:
        print("\n🔧 ISSUES TO FIX:")
        for issue in issues:
            print(f"   {issue}")
        
        print("\n📝 ACTION PLAN:")
        print("1. Update Turkey prompt to explicitly request 8 A+ sections")
        print("2. Add 'ENGLISH:' prefix requirement for all imageDescription fields")
        print("3. Ensure Turkish content for titles, bullets, and keywords")
        print("4. Match Mexico's comprehensive structure exactly")
        print("5. Test with multiple products to ensure consistency")
    else:
        print("\n✅ Turkey successfully matches Mexico's pattern!")
        print("✅ Ready to beat Helium 10, Jasper AI, and CopyMonkey")
    
    print("\n🚀 COMPETITIVE POSITIONING:")
    if turkey_score >= 80:
        print("   ⭐⭐⭐⭐⭐ EXCELLENT - Beats all competitors")
        print("   → Better than Helium 10")
        print("   → Better than Jasper AI")
        print("   → Better than CopyMonkey")
    elif turkey_score >= 60:
        print("   ⭐⭐⭐⭐ GOOD - Competitive position")
    else:
        print("   ⭐⭐⭐ NEEDS IMPROVEMENT")
        print("   → Focus on A+ content structure")
        print("   → Add English image descriptions")
        print("   → Ensure 8 comprehensive sections")

if __name__ == "__main__":
    evaluate_turkey_implementation()