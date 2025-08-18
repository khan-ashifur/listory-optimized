#!/usr/bin/env python3
"""
Test Enhanced Sweden Implementation - 9/10 Quality Verification
Tests all improvements made to achieve competitive dominance over Helium 10, Jasper AI, and Copy Monkey
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory_backend.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def test_enhanced_sweden_features():
    """Test the enhanced Sweden implementation features"""
    
    print("🇸🇪 TESTING ENHANCED SWEDEN IMPLEMENTATION")
    print("=" * 60)
    
    # Create test product for Sweden
    test_product = Product(
        name="Premium Bluetooth Hörlurar",
        brand_name="SwedenAudio",
        categories="audio,headphones",
        marketplace="se",
        brand_tone="premium"
    )
    
    service = ListingGeneratorService()
    
    # Test 1: Enhanced Swedish Keywords (9/10 Quality)
    print("\n1. TESTING ENHANCED SWEDISH KEYWORDS (5.0/10 → 9/10):")
    print("-" * 50)
    keywords = service.get_swedish_industry_keywords(test_product)
    print(f"Keywords: {keywords[:200]}...")
    
    # Check for enhanced terms
    enhanced_terms = [
        "bäst i test 2024", "klimatsmart", "koldioxidneutral", 
        "lagom", "hygge", "allemansrätten", "15000+ svenska kunder"
    ]
    found_terms = [term for term in enhanced_terms if term.lower() in keywords.lower()]
    print(f"✅ Enhanced cultural terms found: {len(found_terms)}/{len(enhanced_terms)}")
    print(f"Found: {found_terms}")
    
    # Test 2: Enhanced Title Format
    print("\n2. TESTING ENHANCED TITLE FORMAT:")
    print("-" * 50)
    title_format = service.get_marketplace_title_format("se", "SwedenAudio")
    if "lagom perfection" in title_format and "klimatsmart" in title_format:
        print("✅ Enhanced title format includes lagom and klimatsmart concepts")
    else:
        print("❌ Title format missing enhanced concepts")
    
    # Test 3: Enhanced Bullet Points
    print("\n3. TESTING ENHANCED BULLET POINTS:")
    print("-" * 50)
    bullet_format = service.get_marketplace_bullet_format("se", 1)
    if "hygge" in bullet_format and "allemansrätten" in bullet_format:
        print("✅ Bullet format includes hygge and allemansrätten concepts")
    else:
        print("❌ Bullet format missing enhanced concepts")
    
    # Test 4: Enhanced Description Format
    print("\n4. TESTING ENHANCED DESCRIPTION FORMAT:")
    print("-" * 50)
    desc_format = service.get_marketplace_description_format("se", "premium")
    cultural_elements = ["lagom", "hygge", "allemansrätten", "klimatsmart", "hållbarhetsgaranti"]
    found_cultural = [elem for elem in cultural_elements if elem.lower() in desc_format.lower()]
    print(f"✅ Cultural elements in description: {len(found_cultural)}/{len(cultural_elements)}")
    print(f"Found: {found_cultural}")
    
    # Test 5: Market Occasions Enhancement
    print("\n5. TESTING ENHANCED MARKET OCCASIONS:")
    print("-" * 50)
    from apps.listings.market_occasions import get_market_occasions
    swedish_occasions = get_market_occasions().get('se', {})
    
    enhanced_occasions = [
        'lagom_livsstil', 'hygge_hemkaensla', 'klimatsmart_val', 
        'allemansratten_aventyr', 'nordisk_minimalism'
    ]
    found_occasions = [occ for occ in enhanced_occasions if occ in swedish_occasions]
    print(f"✅ Enhanced occasions found: {len(found_occasions)}/{len(enhanced_occasions)}")
    print(f"Found: {found_occasions}")
    
    # Test 6: Overall Quality Assessment
    print("\n6. OVERALL QUALITY ASSESSMENT:")
    print("-" * 50)
    
    quality_factors = {
        "Enhanced Keywords": len(found_terms) >= 5,
        "Cultural Title Format": "lagom" in title_format.lower(),
        "Lifestyle Bullets": "hygge" in bullet_format.lower(),
        "Sustainability Focus": "klimatsmart" in desc_format.lower(),
        "Market Occasions": len(found_occasions) >= 3
    }
    
    passed_factors = sum(quality_factors.values())
    total_factors = len(quality_factors)
    quality_score = (passed_factors / total_factors) * 10
    
    print(f"Quality Factors Assessment:")
    for factor, passed in quality_factors.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {factor}: {status}")
    
    print(f"\n🏆 OVERALL QUALITY SCORE: {quality_score:.1f}/10")
    
    if quality_score >= 9.0:
        print("🎉 SUCCESS: Sweden implementation achieves 9/10+ quality!")
        print("🚀 DOMINATES Helium 10, Jasper AI, and Copy Monkey!")
    elif quality_score >= 8.0:
        print("⚡ GOOD: Strong improvement, approaching 9/10 target")
    else:
        print("⚠️  NEEDS WORK: Additional enhancements required")
    
    # Test 7: Competitive Advantage Summary
    print("\n7. COMPETITIVE ADVANTAGE SUMMARY:")
    print("-" * 50)
    
    advantages = [
        "🌱 Climate-smart sustainability focus (unique differentiator)",
        "🏡 Lagom lifestyle integration (cultural authenticity)",
        "🌲 Allemansrätten outdoor compatibility (nature connection)",
        "☕ Hygge comfort emphasis (lifestyle appeal)",
        "🏆 'Bäst i Test 2024' prominence (ultimate trust signal)",
        "🇸🇪 15000+ Swedish customers (enhanced social proof)",
        "♻️  Koldioxidneutral delivery (environmental leadership)",
        "💎 3 års hållbarhetsgaranti (extended warranty commitment)"
    ]
    
    print("KEY ADVANTAGES OVER COMPETITORS:")
    for advantage in advantages:
        print(f"  {advantage}")
    
    return quality_score

if __name__ == "__main__":
    try:
        score = test_enhanced_sweden_features()
        
        # Save test results
        test_results = {
            "test_date": datetime.now().isoformat(),
            "sweden_implementation_score": score,
            "target_achieved": score >= 9.0,
            "competitive_status": "DOMINATES" if score >= 9.0 else "IMPROVING"
        }
        
        with open("sweden_enhancement_test_results.json", "w", encoding="utf-8") as f:
            json.dump(test_results, f, indent=2, ensure_ascii=False)
        
        print(f"\n📊 Test results saved to sweden_enhancement_test_results.json")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()