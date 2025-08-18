"""
Test Turkey vs Mexico A+ Content Generation Comparison
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
from django.contrib.auth.models import User

def test_comparison():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='comparison_test')
    
    print("🔍 TURKEY vs MEXICO A+ CONTENT COMPARISON")
    print("="*60)
    
    # Test Turkey
    print("\n🇹🇷 TESTING TURKEY MARKET:")
    print("-" * 30)
    
    turkey_product = Product.objects.create(
        user=test_user,
        name="Sensei AI Translation Earbuds",
        description="AI-powered translation earbuds",
        brand_name="Sensei",
        brand_tone="premium",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics",
        features="144 languages, 60H battery, IPX7",
        target_audience="Turkish families"
    )
    
    try:
        turkey_listing = service.generate_listing(product_id=turkey_product.id, platform='amazon')
        
        if turkey_listing and turkey_listing.amazon_aplus_content:
            turkey_content = turkey_listing.amazon_aplus_content
            print(f"✅ Turkey A+ Content: {len(turkey_content)} characters")
            
            # Count sections
            turkey_sections = turkey_content.count('class="aplus-section')
            print(f"✅ Turkey A+ Sections: {turkey_sections} sections")
            
            # Check for strategy
            if 'Complete A+ Content Strategy' in turkey_content:
                print("✅ Turkey has Complete A+ Content Strategy")
            else:
                print("❌ Turkey missing Complete A+ Content Strategy")
                
            # Show first section
            if 'section1_hero' in turkey_content or 'Hero' in turkey_content:
                print("✅ Turkey has Hero section")
            
        else:
            print("❌ Turkey A+ content generation failed")
            
    except Exception as e:
        print(f"❌ Turkey error: {e}")
    finally:
        turkey_product.delete()
    
    print("\n" + "="*60)
    
    # Test Mexico  
    print("\n🇲🇽 TESTING MEXICO MARKET:")
    print("-" * 30)
    
    mexico_product = Product.objects.create(
        user=test_user,
        name="Sensei AI Translation Earbuds",
        description="AI-powered translation earbuds", 
        brand_name="Sensei",
        brand_tone="premium",
        target_platform="amazon",
        marketplace="mx", 
        marketplace_language="es-mx",
        categories="Electronics",
        features="144 languages, 60H battery, IPX7",
        target_audience="Mexican families"
    )
    
    try:
        mexico_listing = service.generate_listing(product_id=mexico_product.id, platform='amazon')
        
        if mexico_listing and mexico_listing.amazon_aplus_content:
            mexico_content = mexico_listing.amazon_aplus_content
            print(f"✅ Mexico A+ Content: {len(mexico_content)} characters")
            
            # Count sections
            mexico_sections = mexico_content.count('class="aplus-section')
            print(f"✅ Mexico A+ Sections: {mexico_sections} sections")
            
            # Check for strategy
            if 'Complete A+ Content Strategy' in mexico_content:
                print("✅ Mexico has Complete A+ Content Strategy") 
            else:
                print("❌ Mexico missing Complete A+ Content Strategy")
                
            # Show first section
            if 'section1_hero' in mexico_content or 'Hero' in mexico_content:
                print("✅ Mexico has Hero section")
                
        else:
            print("❌ Mexico A+ content generation failed")
            
    except Exception as e:
        print(f"❌ Mexico error: {e}")
    finally:
        mexico_product.delete()
    
    print("\n" + "="*60)
    print("🎯 COMPARISON SUMMARY:")
    print("Turkey and Mexico should now generate similar comprehensive A+ content!")
    print("Both should have:")
    print("- Complete A+ Content Strategy section")
    print("- 8+ comprehensive sections")
    print("- 20,000+ character content")
    print("- Native language localization")

if __name__ == "__main__":
    test_comparison()