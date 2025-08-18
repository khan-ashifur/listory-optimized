"""
Compare A+ Content Image Strategy - Brazil vs Mexico
Shows the image strategy descriptions that should be generated
"""

import os
import sys
import json
import django
import re

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def extract_image_strategies(aplus_content):
    """Extract image strategy descriptions from A+ content"""
    image_strategies = []
    
    # Find all image strategy sections
    image_pattern = r'Image Strategy</strong>\s*</div>\s*<p class="text-gray-600">([^<]+)</p>'
    matches = re.findall(image_pattern, aplus_content)
    
    for match in matches:
        image_strategies.append(match.strip())
    
    # Also check for any remaining English phrases
    english_patterns = ['image of', 'photo of', 'picture of', 'shows', 'featuring', 
                       'product image', 'lifestyle image', 'demonstration of']
    
    english_found = []
    for pattern in english_patterns:
        if pattern.lower() in aplus_content.lower():
            english_found.append(pattern)
    
    return image_strategies, english_found

def extract_keywords_and_seo(aplus_content):
    """Extract keywords and SEO focus from A+ content"""
    keywords = []
    seo_focus = []
    
    # Find keywords sections
    keyword_pattern = r'Keywords</strong>\s*</div>\s*<p class="text-gray-600">([^<]+)</p>'
    keyword_matches = re.findall(keyword_pattern, aplus_content)
    
    for match in keyword_matches:
        keywords.append(match.strip())
    
    # Find SEO focus sections
    seo_pattern = r'SEO Focus</strong>\s*</div>\s*<p class="text-gray-600">([^<]+)</p>'
    seo_matches = re.findall(seo_pattern, aplus_content)
    
    for match in seo_matches:
        seo_focus.append(match.strip())
    
    return keywords, seo_focus

def generate_and_compare_listing(market_code, language, market_name):
    """Generate listing and extract A+ content details"""
    print(f"\n{'='*70}")
    print(f"🌍 {market_name.upper()} MARKET A+ CONTENT ANALYSIS")
    print(f"{'='*70}")
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username=f'{market_code}_aplus_compare')
    
    product = Product.objects.create(
        user=test_user,
        name="Premium Bluetooth Headphones",
        description="High-quality wireless headphones with noise cancellation and premium sound",
        brand_name="AudioMax",
        brand_tone="premium",
        target_platform="amazon",
        marketplace=market_code,
        marketplace_language=language,
        categories="Electronics/Audio/Headphones",
        features="Noise Canceling, 30H Battery, Wireless, Premium Sound",
        target_audience=f"{market_name} music lovers and professionals",
        occasion="general"
    )
    
    try:
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing and listing.amazon_aplus_content:
            aplus_content = listing.amazon_aplus_content
            
            # Extract image strategies
            image_strategies, english_found = extract_image_strategies(aplus_content)
            
            # Extract keywords and SEO
            keywords, seo_focus = extract_keywords_and_seo(aplus_content)
            
            print(f"\n📸 IMAGE STRATEGY DESCRIPTIONS FOUND:")
            print("-" * 50)
            
            if image_strategies:
                for i, strategy in enumerate(image_strategies, 1):
                    print(f"\n{i}. {strategy}")
                    # Check if it's actually describing an image
                    if any(word in strategy.lower() for word in ['image', 'photo', 'picture']):
                        print(f"   ❌ PROBLEM: Contains English image words!")
                    else:
                        print(f"   ✅ Properly describes what to show")
            else:
                print("❌ No image strategies found!")
            
            print(f"\n🔍 KEYWORDS SECTIONS:")
            print("-" * 50)
            for i, kw in enumerate(keywords, 1):
                print(f"{i}. {kw}")
                if any(c.isascii() and c.isalpha() for word in kw.split() for c in word):
                    if market_code != 'us':
                        has_english = any(word.lower() in ['premium', 'quality', 'best', 'professional'] 
                                        for word in kw.split())
                        if has_english:
                            print(f"   ⚠️ Contains English keywords")
            
            print(f"\n🎯 SEO FOCUS SECTIONS:")
            print("-" * 50)
            for i, seo in enumerate(seo_focus, 1):
                print(f"{i}. {seo}")
            
            if english_found:
                print(f"\n❌ ENGLISH PHRASES DETECTED IN A+ CONTENT:")
                for phrase in english_found:
                    print(f"   - {phrase}")
            
            # Show what image descriptions SHOULD look like
            print(f"\n✅ WHAT IMAGE DESCRIPTIONS SHOULD BE:")
            print("-" * 50)
            
            if market_code == 'br':
                print("HERO: Pessoa usando fones em ambiente moderno, destaque para design premium")
                print("FEATURES: Close-up dos controles, almofadas macias, dobradiças ajustáveis")
                print("TRUST: Certificações, garantia, embalagem premium com acessórios")
            elif market_code == 'mx':
                print("HERO: Usuario disfrutando música en oficina moderna, diseño elegante visible")
                print("FEATURES: Detalle de cancelación ruido, batería larga duración, controles táctiles")
                print("TRUST: Certificados calidad, garantía 2 años, empaque premium incluido")
            
            return {
                'market': market_name,
                'image_strategies': image_strategies,
                'keywords': keywords,
                'seo_focus': seo_focus,
                'english_issues': english_found
            }
        
        else:
            print("❌ No A+ content generated")
            return None
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None
    
    finally:
        product.delete()

def main():
    print("\n🔍 A+ CONTENT IMAGE STRATEGY COMPARISON")
    print("Comparing Brazil and Mexico markets line by line")
    
    # Test Brazil
    brazil_result = generate_and_compare_listing('br', 'pt-br', 'Brazil')
    
    # Test Mexico  
    mexico_result = generate_and_compare_listing('mx', 'es-mx', 'Mexico')
    
    # Line by line comparison
    print(f"\n{'='*70}")
    print("📊 SIDE-BY-SIDE COMPARISON")
    print(f"{'='*70}")
    
    if brazil_result and mexico_result:
        print("\n🇧🇷 BRAZIL vs 🇲🇽 MEXICO\n")
        
        print("IMAGE STRATEGIES:")
        print("-" * 50)
        max_strategies = max(len(brazil_result['image_strategies']), 
                           len(mexico_result['image_strategies']))
        
        for i in range(max_strategies):
            print(f"\nSection {i+1}:")
            if i < len(brazil_result['image_strategies']):
                print(f"BR: {brazil_result['image_strategies'][i]}")
            else:
                print(f"BR: [Missing]")
            
            if i < len(mexico_result['image_strategies']):
                print(f"MX: {mexico_result['image_strategies'][i]}")
            else:
                print(f"MX: [Missing]")
        
        print("\n\nKEYWORDS COMPARISON:")
        print("-" * 50)
        max_keywords = max(len(brazil_result['keywords']), 
                          len(mexico_result['keywords']))
        
        for i in range(max_keywords):
            print(f"\nSection {i+1}:")
            if i < len(brazil_result['keywords']):
                print(f"BR: {brazil_result['keywords'][i]}")
            else:
                print(f"BR: [Missing]")
            
            if i < len(mexico_result['keywords']):
                print(f"MX: {mexico_result['keywords'][i]}")
            else:
                print(f"MX: [Missing]")
        
        print("\n\nISSUES SUMMARY:")
        print("-" * 50)
        print(f"Brazil English issues: {len(brazil_result['english_issues'])}")
        print(f"Mexico English issues: {len(mexico_result['english_issues'])}")
        
        if brazil_result['english_issues'] or mexico_result['english_issues']:
            print("\n⚠️ These markets have English content in A+ sections!")
            print("Image strategies should describe WHAT to show, not use English phrases")

if __name__ == "__main__":
    main()