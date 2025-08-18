"""
Debug A+ Content Display Issue
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

def debug_aplus_display():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='debug_test')
    
    print("🔍 DEBUGGING A+ CONTENT DISPLAY")
    print("="*50)
    
    # Create product
    product = Product.objects.create(
        user=test_user,
        name="Test Headphones",
        description="Test product",
        brand_name="TestBrand",
        brand_tone="premium",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics",
        features="Test feature",
        target_audience="Test audience"
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing and listing.amazon_aplus_content:
            content = listing.amazon_aplus_content
            print(f"✅ A+ Content generated: {len(content)} characters")
            
            # Check key sections
            sections_to_check = [
                "Complete A+ Content Strategy",
                "Profesyonellere ve Ailelere Uyumlu",
                "section1_hero", 
                "section2_features",
                "section3_usage",
                "Overall A+ Strategy"
            ]
            
            print("\n🔍 CHECKING CONTENT SECTIONS:")
            for section in sections_to_check:
                if section in content:
                    print(f"✅ Found: {section}")
                else:
                    print(f"❌ Missing: {section}")
            
            # Show content structure
            print(f"\n📄 CONTENT PREVIEW (first 500 chars):")
            print(content[:500])
            print("...")
            
            print(f"\n📄 CONTENT END (last 500 chars):")
            print("...")
            print(content[-500:])
            
            # Check for HTML structure
            html_elements = [
                '<div class="aplus-introduction',
                '<div class="aplus-section',
                'Complete A+ Content Strategy',
                'Overall A+ Strategy'
            ]
            
            print("\n🔍 CHECKING HTML STRUCTURE:")
            for element in html_elements:
                count = content.count(element)
                print(f"{'✅' if count > 0 else '❌'} {element}: {count} occurrences")
                
        else:
            print("❌ No A+ content generated")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        product.delete()

if __name__ == "__main__":
    debug_aplus_display()