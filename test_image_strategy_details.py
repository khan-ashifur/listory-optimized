"""
Test Detailed Image Strategy Descriptions
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

def test_detailed_image_strategy():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='image_strategy_test')
    
    print("🔍 TESTING DETAILED IMAGE STRATEGY DESCRIPTIONS")
    print("="*60)
    
    # Create product for Turkey market
    product = Product.objects.create(
        user=test_user,
        name="Premium Wireless Headphones",
        description="High-quality wireless headphones",
        brand_name="SoundMaster",
        brand_tone="premium", 
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics/Audio/Headphones",
        features="Active Noise Cancellation, 40H Battery",
        target_audience="Turkish professionals",
        occasion="kurban_bayrami"
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing and listing.amazon_aplus_content:
            content = listing.amazon_aplus_content
            
            # Extract image strategy sections
            import re
            image_pattern = r'<span class="mr-2">📸</span>\s*<strong[^>]*>([^<]+)</strong>\s*</div>\s*<p[^>]*>([^<]+)</p>'
            image_strategies = re.findall(image_pattern, content, re.DOTALL)
            
            print(f"📸 FOUND {len(image_strategies)} IMAGE STRATEGY SECTIONS:")
            print("="*60)
            
            for i, (label, description) in enumerate(image_strategies, 1):
                print(f"\n{i}. 🏷️ LABEL: {label.strip()}")
                print(f"   📝 DESCRIPTION: {description.strip()}")
                
                # Check if description is detailed (more than basic description)
                if len(description.strip()) > 100:
                    print("   ✅ DETAILED (Good length)")
                else:
                    print("   ❌ TOO SHORT")
                    
                # Check for specific detailed elements
                detailed_elements = [
                    'specific', 'lighting', 'setting', 'demographics', 'composition',
                    'Turkish', 'professional', 'lifestyle', 'family', 'conversion'
                ]
                
                found_elements = [elem for elem in detailed_elements if elem.lower() in description.lower()]
                print(f"   🎯 DETAILED ELEMENTS: {len(found_elements)}/10 - {', '.join(found_elements)}")
                
                if len(found_elements) >= 3:
                    print("   🎉 EXCELLENT DETAIL LEVEL")
                elif len(found_elements) >= 1:
                    print("   ⚡ GOOD DETAIL LEVEL")
                else:
                    print("   ⚠️ NEEDS MORE DETAIL")
            
            if not image_strategies:
                print("❌ No image strategy sections found")
                # Look for any image-related content
                if 'image' in content.lower():
                    print("🔍 Found some image content, but not in expected format")
                    # Show a snippet
                    import re
                    image_snippets = re.findall(r'[^.]*image[^.]*\.', content.lower())
                    for snippet in image_snippets[:3]:
                        print(f"   📄 {snippet}")
                
        else:
            print("❌ No A+ content generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    test_detailed_image_strategy()