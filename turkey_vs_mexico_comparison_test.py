#!/usr/bin/env python3

"""
Turkey vs Mexico A+ Content Comparison Test
Verify Turkey now generates pure Turkish content like Mexico generates pure Spanish
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

def test_turkey_vs_mexico():
    """Compare Turkey vs Mexico A+ content to ensure language consistency"""
    print("🇹🇷 vs 🇲🇽 TURKEY vs MEXICO A+ CONTENT COMPARISON")
    print("=" * 70)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='turkey_mexico_comparison')
    
    results = {}
    
    # Test markets
    markets = [
        {
            'code': 'tr',
            'name': 'Turkey',
            'flag': '🇹🇷',
            'product_name': 'Sensei AI Çeviri Kulaklık',
            'expected_language': 'Turkish',
            'expected_keywords': ['kaliteli', 'güvenilir marka', 'müşteri memnuniyeti'],
            'unwanted_keywords': ['premium quality', 'trusted brand', 'Audífonos', 'México']
        },
        {
            'code': 'mx',
            'name': 'Mexico',
            'flag': '🇲🇽',
            'product_name': 'Audífonos Traductores Sensei',
            'expected_language': 'Spanish',
            'expected_keywords': ['calidad premium', 'marca confiable', 'satisfacción cliente'],
            'unwanted_keywords': ['premium quality', 'trusted brand', 'kaliteli', 'Türk']
        }
    ]
    
    for market in markets:
        print(f"\n{market['flag']} TESTING {market['name'].upper()} MARKET")
        print("-" * 50)
        
        # Create product for this market
        product = Product.objects.create(
            user=test_user,
            name=market['product_name'],
            brand_name="Sensei Tech",
            description=f"""Advanced AI translation technology with 40 languages. 
            Designed for {market['name']} families with premium sound quality.""",
            price=299.99,
            marketplace=market['code'],
            marketplace_language=market['code'],
            categories="Electronics/Audio/Headphones",
            occasion="general"
        )
        
        try:
            result = service.generate_listing(product_id=product.id, platform='amazon')
            
            if result and result.amazon_aplus_content:
                aplus_content = result.amazon_aplus_content
                
                # Analyze content
                analysis = {
                    'length': len(aplus_content),
                    'expected_found': [],
                    'unwanted_found': [],
                    'language_score': 0
                }
                
                # Check for expected keywords
                for keyword in market['expected_keywords']:
                    if keyword.lower() in aplus_content.lower():
                        analysis['expected_found'].append(keyword)
                
                # Check for unwanted keywords (other languages)
                for keyword in market['unwanted_keywords']:
                    if keyword.lower() in aplus_content.lower():
                        analysis['unwanted_found'].append(keyword)
                
                # Calculate language purity score
                expected_score = len(analysis['expected_found']) * 10
                unwanted_penalty = len(analysis['unwanted_found']) * -20
                analysis['language_score'] = max(0, expected_score + unwanted_penalty)
                
                # Store results
                results[market['code']] = analysis
                
                print(f"✅ Generated A+ content: {analysis['length']} characters")
                print(f"✅ Expected {market['expected_language']} keywords found: {len(analysis['expected_found'])}")
                for keyword in analysis['expected_found']:
                    print(f"   - '{keyword}'")
                
                if analysis['unwanted_found']:
                    print(f"❌ Unwanted foreign keywords found: {len(analysis['unwanted_found'])}")
                    for keyword in analysis['unwanted_found']:
                        print(f"   - '{keyword}' (should not be here!)")
                else:
                    print(f"✅ No foreign language contamination detected")
                
                print(f"📊 Language Purity Score: {analysis['language_score']}/100")
                
                # Show a sample of keywords for verification
                import re
                keyword_sections = re.findall(r'Keywords</strong>.*?<p class="text-gray-600">(.*?)</p>', aplus_content, re.DOTALL)
                if keyword_sections:
                    print(f"\n🔑 KEYWORD SAMPLE:")
                    print(f"   {keyword_sections[0][:100]}...")
                
            else:
                print(f"❌ Failed to generate A+ content")
                results[market['code']] = {'error': 'No content generated'}
                
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results[market['code']] = {'error': str(e)}
        
        # Cleanup
        product.delete()
    
    # Final comparison
    print(f"\n🏆 FINAL COMPARISON RESULTS")
    print("=" * 70)
    
    if 'tr' in results and 'mx' in results:
        tr_score = results['tr'].get('language_score', 0)
        mx_score = results['mx'].get('language_score', 0)
        
        print(f"🇹🇷 Turkey Language Purity: {tr_score}/100")
        print(f"🇲🇽 Mexico Language Purity: {mx_score}/100")
        
        if tr_score >= 80 and mx_score >= 80:
            print(f"✅ SUCCESS: Both markets generate pure language content!")
        elif tr_score < mx_score:
            print(f"⚠️ Turkey needs improvement (scoring {tr_score} vs Mexico's {mx_score})")
        else:
            print(f"⚠️ Mexico needs improvement (scoring {mx_score} vs Turkey's {tr_score})")
        
        # Check for cross-contamination
        tr_unwanted = len(results['tr'].get('unwanted_found', []))
        mx_unwanted = len(results['mx'].get('unwanted_found', []))
        
        if tr_unwanted == 0 and mx_unwanted == 0:
            print(f"✅ No cross-language contamination detected")
        else:
            print(f"❌ Language contamination detected:")
            if tr_unwanted > 0:
                print(f"   Turkey has {tr_unwanted} foreign keywords")
            if mx_unwanted > 0:
                print(f"   Mexico has {mx_unwanted} foreign keywords")

if __name__ == "__main__":
    test_turkey_vs_mexico()