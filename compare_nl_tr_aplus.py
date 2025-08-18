"""
Compare Netherlands vs Turkey A+ Content Generation
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

def test_aplus_comparison():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='nl_tr_comparison')
    
    markets = [
        ('nl', 'nl', 'Netherlands', 'koningsdag'),
        ('tr', 'tr', 'Turkey', 'kurban_bayrami')
    ]
    
    for market_code, language, market_name, occasion in markets:
        print(f"\n{'='*60}")
        print(f"🌍 {market_name.upper()} A+ CONTENT TEST")
        print(f"{'='*60}")
        
        product = Product.objects.create(
            user=test_user,
            name="Premium Wireless Headphones",
            description="High-quality wireless headphones with noise cancellation",
            brand_name="AudioMax",
            brand_tone="premium",
            target_platform="amazon",
            marketplace=market_code,
            marketplace_language=language,
            categories="Electronics/Audio/Headphones",
            features="Noise Canceling, 30H Battery, Wireless, Premium Sound",
            target_audience=f"{market_name} music lovers",
            occasion=occasion
        )
        
        try:
            listing = service.generate_listing(product_id=product.id, platform='amazon')
            
            if listing and listing.amazon_aplus_content:
                aplus_content = listing.amazon_aplus_content
                print(f"📄 A+ Content Length: {len(aplus_content)} characters")
                
                # Show first 800 characters to see structure
                print(f"\n📝 A+ Content Preview:")
                print("-" * 50)
                print(aplus_content[:800])
                print("...")
                
                # Check for specific patterns
                if 'Keywords' in aplus_content:
                    # Extract keywords sections
                    import re
                    keyword_sections = re.findall(r'Keywords</strong>.*?<p class="text-gray-600">(.*?)</p>', aplus_content, re.DOTALL)
                    print(f"\n🔍 Keywords Sections Found: {len(keyword_sections)}")
                    for i, section in enumerate(keyword_sections[:3], 1):
                        print(f"  {i}. {section.strip()}")
                
                if 'Image Strategy' in aplus_content:
                    # Extract image strategy sections
                    image_sections = re.findall(r'Image Strategy</strong>.*?<p class="text-gray-600">(.*?)</p>', aplus_content, re.DOTALL)
                    print(f"\n📸 Image Strategy Sections Found: {len(image_sections)}")
                    for i, section in enumerate(image_sections[:3], 1):
                        print(f"  {i}. {section.strip()}")
                
                # Check language
                if market_code == 'nl':
                    dutch_words = ['Nederlandse', 'kwaliteit', 'garantie', 'betrouwbaar']
                    dutch_found = sum(1 for word in dutch_words if word in aplus_content)
                    print(f"\n🇳🇱 Dutch language indicators: {dutch_found}/4")
                elif market_code == 'tr':
                    turkish_words = ['Türk', 'kalite', 'garanti', 'güvenilir']
                    turkish_found = sum(1 for word in turkish_words if word in aplus_content)
                    print(f"\n🇹🇷 Turkish language indicators: {turkish_found}/4")
                
            else:
                print("❌ No A+ content generated")
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        finally:
            product.delete()

if __name__ == "__main__":
    test_aplus_comparison()