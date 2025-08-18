#!/usr/bin/env python3
"""
FIX TURKEY-MEXICO ALIGNMENT
Ensure Turkey follows EXACTLY the same structure as Mexico
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

def test_mexico_turkey_alignment():
    """Test both Mexico and Turkey to ensure exact same structure"""
    
    print("🔍 TESTING MEXICO-TURKEY ALIGNMENT")
    print("=" * 50)
    
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='test_alignment')
    
    # Test Mexico first
    print("🇲🇽 TESTING MEXICO:")
    print("-" * 20)
    
    product_mx = Product.objects.create(
        user=user,
        name="Premium Bluetooth Audífonos",
        brand_name="TechPro",
        marketplace="mx",
        marketplace_language="es-mx", 
        price=299.99,
        occasion="navidad",
        brand_tone="luxury",
        categories="Electronics > Audio",
        description="Audífonos premium para familia mexicana.",
        features="Bluetooth 5.3\n30 horas\nCancelación ruido"
    )
    
    service = ListingGeneratorService()
    listing_mx = service.generate_listing(product_mx.id, 'amazon')
    
    # Analyze Mexico results
    mx_bullets = listing_mx.bullet_points.split('\n') if listing_mx.bullet_points else []
    mx_bullets_clean = [b.strip() for b in mx_bullets if b.strip()]
    
    print(f"✅ MX Generated:")
    print(f"   Status: {listing_mx.status}")
    print(f"   Title: {len(listing_mx.title)} chars")
    print(f"   Bullets: {len(mx_bullets_clean)} bullets")
    for i, bullet in enumerate(mx_bullets_clean[:3], 1):
        print(f"     {i}. {bullet[:80]}...")
    print(f"   Description: {len(listing_mx.long_description)} chars")
    print(f"   A+ Content: {len(listing_mx.amazon_aplus_content)} chars")
    
    product_mx.delete()
    
    print()
    print("🇹🇷 TESTING TURKEY:")
    print("-" * 20)
    
    # Test Turkey with same structure
    product_tr = Product.objects.create(
        user=user,
        name="Premium Bluetooth Kulaklık",
        brand_name="TechPro",
        marketplace="tr",
        marketplace_language="tr", 
        price=299.99,
        occasion="yeni_yil",
        brand_tone="luxury",
        categories="Electronics > Audio",
        description="Türk ailesi için premium kulaklık.",
        features="Bluetooth 5.3\n30 saat\nGürültü engelleme"
    )
    
    listing_tr = service.generate_listing(product_tr.id, 'amazon')
    
    # Analyze Turkey results
    tr_bullets = listing_tr.bullet_points.split('\n') if listing_tr.bullet_points else []
    tr_bullets_clean = [b.strip() for b in tr_bullets if b.strip()]
    
    print(f"✅ TR Generated:")
    print(f"   Status: {listing_tr.status}")
    print(f"   Title: {len(listing_tr.title)} chars")
    print(f"   Bullets: {len(tr_bullets_clean)} bullets")
    for i, bullet in enumerate(tr_bullets_clean[:3], 1):
        print(f"     {i}. {bullet[:80]}...")
    print(f"   Description: {len(listing_tr.long_description)} chars")
    print(f"   A+ Content: {len(listing_tr.amazon_aplus_content)} chars")
    
    product_tr.delete()
    
    print()
    print("🔍 ALIGNMENT ANALYSIS:")
    print("=" * 30)
    
    # Compare structures
    mx_structure = {
        "bullets": len(mx_bullets_clean),
        "description_length": len(listing_mx.long_description),
        "aplus_length": len(listing_mx.amazon_aplus_content),
        "title_length": len(listing_mx.title)
    }
    
    tr_structure = {
        "bullets": len(tr_bullets_clean), 
        "description_length": len(listing_tr.long_description),
        "aplus_length": len(listing_tr.amazon_aplus_content),
        "title_length": len(listing_tr.title)
    }
    
    print(f"Mexico Structure: {mx_structure}")
    print(f"Turkey Structure: {tr_structure}")
    print()
    
    # Check alignment
    issues = []
    
    if mx_structure["bullets"] != tr_structure["bullets"]:
        issues.append(f"Bullet mismatch: MX={mx_structure['bullets']} vs TR={tr_structure['bullets']}")
    
    if abs(mx_structure["description_length"] - tr_structure["description_length"]) > 200:
        issues.append(f"Description length gap: MX={mx_structure['description_length']} vs TR={tr_structure['description_length']}")
        
    if abs(mx_structure["aplus_length"] - tr_structure["aplus_length"]) > 2000:
        issues.append(f"A+ content gap: MX={mx_structure['aplus_length']} vs TR={tr_structure['aplus_length']}")
    
    if issues:
        print("❌ ALIGNMENT ISSUES FOUND:")
        for issue in issues:
            print(f"   • {issue}")
        
        print()
        print("🔧 RECOMMENDATIONS:")
        if any("Bullet" in issue for issue in issues):
            print("   • Fix bullet point parsing for Turkey")
        if any("Description" in issue for issue in issues):
            print("   • Align description generation prompts")
        if any("A+" in issue for issue in issues):
            print("   • Ensure A+ content follows same template")
    else:
        print("✅ PERFECT ALIGNMENT - Turkey matches Mexico structure!")
    
    # Save comparison
    comparison_data = {
        "timestamp": datetime.now().isoformat(),
        "mexico_structure": mx_structure,
        "turkey_structure": tr_structure,
        "alignment_issues": issues,
        "mexico_bullets_preview": mx_bullets_clean[:3],
        "turkey_bullets_preview": tr_bullets_clean[:3]
    }
    
    with open(f'mexico_turkey_alignment_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json', 'w', encoding='utf-8') as f:
        json.dump(comparison_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Alignment analysis saved to mexico_turkey_alignment_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

if __name__ == "__main__":
    test_mexico_turkey_alignment()