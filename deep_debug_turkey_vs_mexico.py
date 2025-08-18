#!/usr/bin/env python3
"""
DEEP DEBUG: TURKEY VS MEXICO EXACT DIFFERENCES
Find the exact root cause of why Turkey fails JSON parsing while Mexico succeeds
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

def deep_debug_turkey_vs_mexico():
    """Deep debug to find exact differences between Turkey and Mexico generation"""
    
    print("🔍 DEEP DEBUG: TURKEY VS MEXICO ROOT CAUSE ANALYSIS")
    print("=" * 60)
    
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='deep_debug_user')
    
    # Test identical products for both markets
    
    print("🇲🇽 STEP 1: ANALYZE MEXICO GENERATION PROCESS")
    print("-" * 50)
    
    product_mx = Product.objects.create(
        user=user,
        name="Test Bluetooth Product",
        brand_name="TestBrand",
        marketplace="mx",
        marketplace_language="es-mx", 
        price=199.99,
        occasion="navidad",
        brand_tone="luxury",
        categories="Electronics",
        description="Test product",
        features="Feature 1\nFeature 2"
    )
    
    print(f"🇲🇽 Product MX Created: {product_mx.id}")
    
    # Manually trace the generation process
    service = ListingGeneratorService()
    
    # Check if the service uses different prompts for different markets
    print("🔍 Checking Mexico prompt generation...")
    
    try:
        # This will show us the exact AI response before parsing
        import logging
        logging.basicConfig(level=logging.DEBUG)
        
        listing_mx = service.generate_listing(product_mx.id, 'amazon')
        print(f"✅ Mexico generation completed: {listing_mx.status}")
        
    except Exception as e:
        print(f"❌ Mexico generation failed: {e}")
    
    product_mx.delete()
    
    print("\n🇹🇷 STEP 2: ANALYZE TURKEY GENERATION PROCESS") 
    print("-" * 50)
    
    product_tr = Product.objects.create(
        user=user,
        name="Test Bluetooth Product",
        brand_name="TestBrand", 
        marketplace="tr",
        marketplace_language="tr",
        price=199.99,
        occasion="yeni_yil",
        brand_tone="luxury",
        categories="Electronics",
        description="Test product",
        features="Feature 1\nFeature 2"
    )
    
    print(f"🇹🇷 Product TR Created: {product_tr.id}")
    
    try:
        listing_tr = service.generate_listing(product_tr.id, 'amazon')
        print(f"✅ Turkey generation completed: {listing_tr.status}")
        
    except Exception as e:
        print(f"❌ Turkey generation failed: {e}")
    
    product_tr.delete()
    
    print("\n🔍 STEP 3: ANALYZE PROMPT DIFFERENCES")
    print("-" * 40)
    
    # Let's check what prompts are being generated for each market
    from apps.listings.international_localization_optimizer import InternationalLocalizationOptimizer
    
    optimizer = InternationalLocalizationOptimizer()
    
    # Check Mexico localization - using the correct method
    try:
        mx_enhancement = optimizer.get_localization_enhancement("mx", "es-mx")
        print(f"🇲🇽 Mexico localization enhancement: {len(mx_enhancement) if mx_enhancement else 0} chars")
    except Exception as e:
        print(f"❌ Error getting Mexico enhancement: {e}")
    
    # Check Turkey localization  
    try:
        tr_enhancement = optimizer.get_localization_enhancement("tr", "tr")
        print(f"🇹🇷 Turkey localization enhancement: {len(tr_enhancement) if tr_enhancement else 0} chars")
    except Exception as e:
        print(f"❌ Error getting Turkey enhancement: {e}")
    
    print("\n🔍 STEP 4: CHECK LOCALIZATION DIFFERENCES")
    print("-" * 45)
    
    # Check if the localization enhancement is different
    mx_enhancement = optimizer.get_localization_enhancement("mx", "es-mx")
    tr_enhancement = optimizer.get_localization_enhancement("tr", "tr")
    
    print(f"🇲🇽 Mexico enhancement length: {len(mx_enhancement) if mx_enhancement else 0}")
    print(f"🇹🇷 Turkey enhancement length: {len(tr_enhancement) if tr_enhancement else 0}")
    
    if mx_enhancement and tr_enhancement:
        print(f"🇲🇽 Mexico enhancement preview: {mx_enhancement[:200]}...")
        print(f"🇹🇷 Turkey enhancement preview: {tr_enhancement[:200]}...")
    
    print("\n🔍 STEP 5: CHECK A+ CONTENT ENHANCEMENT")
    print("-" * 42)
    
    mx_aplus = optimizer.get_aplus_content_enhancement("mx", "es-mx")
    tr_aplus = optimizer.get_aplus_content_enhancement("tr", "tr")
    
    print(f"🇲🇽 Mexico A+ enhancement length: {len(mx_aplus) if mx_aplus else 0}")
    print(f"🇹🇷 Turkey A+ enhancement length: {len(tr_aplus) if tr_aplus else 0}")
    
    if mx_aplus and tr_aplus:
        print(f"🇲🇽 Mexico A+ preview: {mx_aplus[:200]}...")
        print(f"🇹🇷 Turkey A+ preview: {tr_aplus[:200]}...")
    
    print("\n🔍 STEP 6: DETAILED CHARACTER ANALYSIS")
    print("-" * 41)
    
    # Let's see if there are specific Turkish characters causing JSON issues
    if tr_enhancement:
        turkish_chars = set(tr_enhancement)
        problematic_chars = []
        
        for char in turkish_chars:
            if ord(char) > 127:  # Non-ASCII
                problematic_chars.append(f"'{char}' (U+{ord(char):04X})")
        
        print(f"🇹🇷 Turkish special characters found: {len(problematic_chars)}")
        if problematic_chars:
            print(f"🇹🇷 Problematic chars: {', '.join(problematic_chars[:10])}")
    
    print("\n🔍 STEP 7: CHECK SERVICES.PY MARKETPLACE HANDLING")
    print("-" * 49)
    
    # Let's check if services.py handles tr differently than mx
    print("Checking bullet examples in services.py...")
    
    # Read and compare bullet examples
    import apps.listings.services as services_module
    
    # We need to inspect the get_marketplace_bullet_format method
    temp_service = ListingGeneratorService()
    
    try:
        mx_bullet_format = temp_service.get_marketplace_bullet_format("mx", 1)
        print(f"🇲🇽 Mexico bullet format length: {len(mx_bullet_format)}")
        print(f"🇲🇽 Mexico bullet preview: {mx_bullet_format[:150]}...")
    except Exception as e:
        print(f"❌ Error getting Mexico bullet format: {e}")
    
    try:
        tr_bullet_format = temp_service.get_marketplace_bullet_format("tr", 1) 
        print(f"🇹🇷 Turkey bullet format length: {len(tr_bullet_format)}")
        print(f"🇹🇷 Turkey bullet preview: {tr_bullet_format[:150]}...")
    except Exception as e:
        print(f"❌ Error getting Turkey bullet format: {e}")
    
    print("\n🎯 ROOT CAUSE ANALYSIS SUMMARY")
    print("=" * 35)
    
    differences = []
    
    if mx_config and tr_config:
        if len(mx_config.get('enforcement_rules', [])) != len(tr_config.get('enforcement_rules', [])):
            differences.append("Different number of enforcement rules")
    
    if mx_enhancement and tr_enhancement:
        if len(mx_enhancement) != len(tr_enhancement):
            differences.append(f"Enhancement length difference: MX={len(mx_enhancement)} vs TR={len(tr_enhancement)}")
    
    if mx_aplus and tr_aplus:
        if len(mx_aplus) != len(tr_aplus):
            differences.append(f"A+ enhancement difference: MX={len(mx_aplus)} vs TR={len(tr_aplus)}")
    
    if differences:
        print("❌ KEY DIFFERENCES FOUND:")
        for diff in differences:
            print(f"   • {diff}")
    else:
        print("🤔 No obvious differences found - need deeper investigation")
    
    print(f"\n💾 Analysis timestamp: {datetime.now().isoformat()}")

if __name__ == "__main__":
    deep_debug_turkey_vs_mexico()