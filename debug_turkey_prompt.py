"""
Debug Turkey A+ Content Prompt - Check what prompt Turkey actually receives
"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.international_localization_optimizer import InternationalLocalizationOptimizer
from django.contrib.auth.models import User

def debug_turkey_prompt():
    print("🔍 DEBUGGING TURKEY A+ CONTENT PROMPT")
    print("="*60)
    
    test_user, _ = User.objects.get_or_create(username='prompt_debug')
    
    # Create Turkey product
    product = Product.objects.create(
        user=test_user,
        name="Sensei AI Translation Earbuds",
        description="AI-powered translation earbuds",
        brand_name="Sensei",
        brand_tone="professional",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics",
        features="144 languages, 60H battery, IPX7",
        target_audience="Turkish families"
    )
    
    try:
        service = ListingGeneratorService()
        
        # Check international localization optimizer
        print("🌍 CHECKING INTERNATIONAL LOCALIZATION:")
        optimizer = InternationalLocalizationOptimizer()
        
        # Check localization enhancement
        localization_enhancement = optimizer.get_localization_enhancement("tr", "tr")
        print(f"   Localization enhancement length: {len(localization_enhancement)} chars")
        if localization_enhancement:
            print(f"   Enhancement preview: {localization_enhancement[:200]}...")
        else:
            print(f"   ❌ No localization enhancement for Turkey")
        
        # Check A+ content enhancement  
        aplus_enhancement = optimizer.get_aplus_content_enhancement("tr", "tr")
        print(f"   A+ enhancement length: {len(aplus_enhancement)} chars")
        if aplus_enhancement:
            print(f"   A+ enhancement preview: {aplus_enhancement[:200]}...")
            
            # Check if it contains section instructions
            if 'section1_hero' in aplus_enhancement:
                print(f"   ✅ Contains section1_hero")
            else:
                print(f"   ❌ Missing section1_hero")
                
            if 'section8_package' in aplus_enhancement:
                print(f"   ✅ Contains section8_package")
            else:
                print(f"   ❌ Missing section8_package")
        else:
            print(f"   ❌ No A+ enhancement for Turkey")
        
        # Compare with Mexico
        print(f"\n🇲🇽 COMPARING WITH MEXICO:")
        mx_localization = optimizer.get_localization_enhancement("mx", "es-mx")
        mx_aplus = optimizer.get_aplus_content_enhancement("mx", "es-mx")
        print(f"   Mexico localization: {len(mx_localization)} chars")
        print(f"   Mexico A+ enhancement: {len(mx_aplus)} chars")
        
        if len(mx_aplus) > len(aplus_enhancement):
            print(f"   ❌ Mexico has MORE A+ enhancement than Turkey!")
            print(f"   Difference: {len(mx_aplus) - len(aplus_enhancement)} chars")
        else:
            print(f"   ✅ Turkey and Mexico have similar A+ enhancement lengths")
            
        # Check marketplace configurations
        print(f"\n🔧 CHECKING MARKETPLACE CONFIGURATIONS:")
        if "tr" in optimizer.market_configurations:
            print(f"   ✅ Turkey configuration exists")
            tr_config = optimizer.market_configurations["tr"]
            print(f"   Turkey market name: {tr_config.get('market_name', 'N/A')}")
            print(f"   Turkey enforcement rules: {len(tr_config.get('enforcement_rules', []))} rules")
        else:
            print(f"   ❌ Turkey configuration MISSING!")
            
        if "mx" in optimizer.market_configurations:
            print(f"   ✅ Mexico configuration exists")
        else:
            print(f"   ❌ Mexico configuration MISSING!")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        product.delete()

if __name__ == "__main__":
    debug_turkey_prompt()