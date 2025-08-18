#!/usr/bin/env python3
"""
DIRECT A+ CONTENT COMPARISON: MEXICO VS TURKEY
Find exactly why Turkey A+ content is shorter than Mexico
"""

import os
import sys
import django
import json
from datetime import datetime

# Add backend to Python path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def direct_aplus_comparison():
    """Direct comparison of A+ content generation between Mexico and Turkey"""
    
    print("🔍 DIRECT A+ CONTENT COMPARISON: MEXICO VS TURKEY")
    print("=" * 55)
    
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='aplus_comparison')
    
    results = {}
    
    # Test Mexico
    print("🇲🇽 GENERATING MEXICO A+ CONTENT")
    print("-" * 35)
    
    product_mx = Product.objects.create(
        user=user,
        name="Premium Audio Headphones",
        brand_name="TestBrand",
        marketplace="mx",
        marketplace_language="es-mx", 
        price=299.99,
        occasion="navidad",
        brand_tone="luxury",
        categories="Electronics > Audio",
        description="Premium headphones for Mexican families",
        features="Bluetooth 5.3\n30 hour battery\nNoise cancellation"
    )
    
    service = ListingGeneratorService()
    listing_mx = service.generate_listing(product_mx.id, 'amazon')
    
    results['mexico'] = {
        'aplus_length': len(listing_mx.amazon_aplus_content),
        'hero_title': getattr(listing_mx, 'hero_title', ''),
        'hero_content': getattr(listing_mx, 'hero_content', ''),
        'features': getattr(listing_mx, 'features', ''),
        'trust_builders': getattr(listing_mx, 'trust_builders', ''),
        'faqs': getattr(listing_mx, 'faqs', ''),
        'aplus_preview': listing_mx.amazon_aplus_content[:500] if listing_mx.amazon_aplus_content else ''
    }
    
    print(f"✅ Mexico A+ Content: {results['mexico']['aplus_length']:,} characters")
    print(f"📋 Hero Title: {len(results['mexico']['hero_title'])} chars")
    print(f"📋 Hero Content: {len(results['mexico']['hero_content'])} chars") 
    print(f"📋 Features: {len(results['mexico']['features'])} chars")
    print(f"📋 Trust Builders: {len(results['mexico']['trust_builders'])} chars")
    print(f"📋 FAQs: {len(results['mexico']['faqs'])} chars")
    
    product_mx.delete()
    
    print("\n🇹🇷 GENERATING TURKEY A+ CONTENT")
    print("-" * 35)
    
    # Test Turkey with identical structure
    product_tr = Product.objects.create(
        user=user,
        name="Premium Audio Headphones",
        brand_name="TestBrand",
        marketplace="tr",
        marketplace_language="tr", 
        price=299.99,
        occasion="yeni_yil",
        brand_tone="luxury",
        categories="Electronics > Audio",
        description="Premium headphones for Turkish families",
        features="Bluetooth 5.3\n30 hour battery\nNoise cancellation"
    )
    
    listing_tr = service.generate_listing(product_tr.id, 'amazon')
    
    results['turkey'] = {
        'aplus_length': len(listing_tr.amazon_aplus_content),
        'hero_title': getattr(listing_tr, 'hero_title', ''),
        'hero_content': getattr(listing_tr, 'hero_content', ''),
        'features': getattr(listing_tr, 'features', ''),
        'trust_builders': getattr(listing_tr, 'trust_builders', ''),
        'faqs': getattr(listing_tr, 'faqs', ''),
        'aplus_preview': listing_tr.amazon_aplus_content[:500] if listing_tr.amazon_aplus_content else ''
    }
    
    print(f"✅ Turkey A+ Content: {results['turkey']['aplus_length']:,} characters")
    print(f"📋 Hero Title: {len(results['turkey']['hero_title'])} chars")
    print(f"📋 Hero Content: {len(results['turkey']['hero_content'])} chars")
    print(f"📋 Features: {len(results['turkey']['features'])} chars")
    print(f"📋 Trust Builders: {len(results['turkey']['trust_builders'])} chars")
    print(f"📋 FAQs: {len(results['turkey']['faqs'])} chars")
    
    product_tr.delete()
    
    print("\n🔍 DETAILED COMPARISON ANALYSIS")
    print("=" * 35)
    
    # Calculate differences
    length_diff = results['mexico']['aplus_length'] - results['turkey']['aplus_length']
    length_diff_pct = (length_diff / results['mexico']['aplus_length']) * 100 if results['mexico']['aplus_length'] > 0 else 0
    
    print(f"📊 A+ Content Length Difference: {length_diff:,} characters ({length_diff_pct:.1f}%)")
    
    # Compare individual components
    components = ['hero_title', 'hero_content', 'features', 'trust_builders', 'faqs']
    
    for component in components:
        mx_len = len(results['mexico'][component])
        tr_len = len(results['turkey'][component])
        diff = mx_len - tr_len
        print(f"📋 {component.replace('_', ' ').title()}: MX={mx_len} vs TR={tr_len} (diff: {diff:+})")
    
    print("\n🔍 A+ CONTENT STRUCTURE ANALYSIS")
    print("-" * 35)
    
    # Analyze the actual A+ content structure
    mx_aplus = results['mexico']['aplus_preview']
    tr_aplus = results['turkey']['aplus_preview']
    
    print(f"🇲🇽 Mexico A+ Preview (first 300 chars):")
    print(f"   {mx_aplus[:300]}...")
    print()
    print(f"🇹🇷 Turkey A+ Preview (first 300 chars):")
    print(f"   {tr_aplus[:300]}...")
    
    # Check for specific patterns
    print("\n🔍 PATTERN ANALYSIS")
    print("-" * 20)
    
    mx_sections = mx_aplus.count('<div class="aplus-section">')
    tr_sections = tr_aplus.count('<div class="aplus-section">')
    print(f"📊 A+ Sections: MX={mx_sections} vs TR={tr_sections}")
    
    mx_modules = mx_aplus.count('<div class="aplus-module">')
    tr_modules = tr_aplus.count('<div class="aplus-module">')
    print(f"📊 A+ Modules: MX={mx_modules} vs TR={tr_modules}")
    
    mx_intro = mx_aplus.count('<div class="aplus-introduction">')
    tr_intro = tr_aplus.count('<div class="aplus-introduction">')
    print(f"📊 Introduction Blocks: MX={mx_intro} vs TR={tr_intro}")
    
    # Save detailed comparison for further analysis
    comparison_data = {
        'timestamp': datetime.now().isoformat(),
        'mexico_results': results['mexico'],
        'turkey_results': results['turkey'],
        'analysis': {
            'length_difference': length_diff,
            'length_difference_percentage': length_diff_pct,
            'component_differences': {
                comp: len(results['mexico'][comp]) - len(results['turkey'][comp])
                for comp in components
            },
            'structure_differences': {
                'sections': mx_sections - tr_sections,
                'modules': mx_modules - tr_modules,
                'introductions': mx_intro - tr_intro
            }
        }
    }
    
    # Save full A+ content for detailed inspection
    with open(f'mx_aplus_full_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html', 'w', encoding='utf-8') as f:
        f.write(listing_mx.amazon_aplus_content)
    
    with open(f'tr_aplus_full_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html', 'w', encoding='utf-8') as f:
        f.write(listing_tr.amazon_aplus_content)
    
    with open(f'aplus_comparison_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w', encoding='utf-8') as f:
        json.dump(comparison_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Full comparison saved to aplus_comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    print(f"💾 Mexico A+ saved to mx_aplus_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    print(f"💾 Turkey A+ saved to tr_aplus_full_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html")
    
    print("\n🎯 ROOT CAUSE HYPOTHESIS")
    print("=" * 25)
    
    if length_diff > 10000:
        print("❌ SIGNIFICANT A+ CONTENT DIFFERENCE DETECTED")
        print("🔍 Likely causes:")
        if mx_sections != tr_sections:
            print(f"   • Different number of A+ sections (MX:{mx_sections} vs TR:{tr_sections})")
        if abs(len(results['mexico']['features']) - len(results['turkey']['features'])) > 100:
            print("   • Features content generation difference")
        if abs(len(results['mexico']['faqs']) - len(results['turkey']['faqs'])) > 200:
            print("   • FAQ content generation difference")
        print("   • Template generation logic difference between markets")
        print("   • Different prompt responses affecting A+ plan structure")
    else:
        print("✅ A+ Content lengths are similar - no major structural issues")

if __name__ == "__main__":
    direct_aplus_comparison()