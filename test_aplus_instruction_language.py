"""
Test A+ Content Instruction Language Consistency
Check if instructions are in English but content is in local language
"""

import os
import sys
import json
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def test_aplus_instruction_consistency():
    print("\n🔍 TESTING A+ CONTENT INSTRUCTION LANGUAGE CONSISTENCY")
    print("=" * 70)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='aplus_instruction_test')
    
    # Test different markets
    markets = [
        {'marketplace': 'de', 'language': 'de', 'name': 'Germany'},
        {'marketplace': 'fr', 'language': 'fr', 'name': 'France'},
        {'marketplace': 'jp', 'language': 'ja', 'name': 'Japan'},
        {'marketplace': 'us', 'language': 'en', 'name': 'USA'}
    ]
    
    results = {}
    
    for market in markets:
        print(f"\n📍 TESTING MARKET: {market['name']} ({market['marketplace']})")
        print("-" * 50)
        
        # Create test product for this market
        product = Product.objects.create(
            user=test_user,
            name="Test Premium Headphones",
            description="High-quality wireless headphones",
            brand_name="TestBrand",
            brand_tone="professional",
            target_platform="amazon",
            marketplace=market['marketplace'],
            marketplace_language=market['language'],
            categories="Electronics/Audio",
            features="Wireless, Noise Cancelling",
            target_audience="Professionals",
            occasion="general"
        )
        
        try:
            # Generate listing
            listing = service.generate_listing(product_id=product.id, platform='amazon')
            
            if listing and listing.amazon_aplus_content:
                aplus_content = listing.amazon_aplus_content
                
                # Check if instructions/structure are in English vs content in local language
                has_english_instructions = any(word in aplus_content.lower() for word in [
                    'image description', 'strategy', 'keywords', 'seo optimization', 
                    'title', 'content', 'section'
                ])
                
                # Check if content has local language
                if market['language'] == 'de':
                    has_local_content = any(word in aplus_content for word in ['ä', 'ö', 'ü', 'ß', 'Qualität'])
                elif market['language'] == 'fr':
                    has_local_content = any(word in aplus_content for word in ['é', 'è', 'à', 'ç', 'qualité'])
                elif market['language'] == 'ja':
                    has_local_content = any('\u3040' <= char <= '\u309F' or '\u30A0' <= char <= '\u30FF' or '\u4E00' <= char <= '\u9FFF' for char in aplus_content)
                else:  # English
                    has_local_content = True  # English is expected
                
                # Analyze structure vs content
                print(f"  📋 A+ Content Analysis:")
                print(f"    • Has English Instructions: {'✅ YES' if has_english_instructions else '❌ NO'}")
                print(f"    • Has Local Content: {'✅ YES' if has_local_content else '❌ NO'}")
                print(f"    • Content Length: {len(aplus_content)} characters")
                
                # Show first 200 chars to examine
                preview = aplus_content[:200].replace('\n', ' ')
                print(f"    • Preview: {preview}...")
                
                results[market['name']] = {
                    'has_english_instructions': has_english_instructions,
                    'has_local_content': has_local_content,
                    'content_length': len(aplus_content),
                    'preview': preview,
                    'correct_format': has_english_instructions and has_local_content
                }
                
            else:
                print(f"  ❌ No A+ content generated")
                results[market['name']] = {'error': 'No A+ content generated'}
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results[market['name']] = {'error': str(e)}
            
        finally:
            product.delete()
    
    # Final analysis
    print(f"\n\n🎯 FINAL ANALYSIS:")
    print("=" * 50)
    
    for market_name, result in results.items():
        if 'error' not in result:
            status = "✅ CORRECT" if result['correct_format'] else "❌ ISSUE"
            print(f"{market_name}: {status}")
            if not result['correct_format']:
                print(f"  └─ Instructions in English: {result['has_english_instructions']}")
                print(f"  └─ Content in Local Language: {result['has_local_content']}")
        else:
            print(f"{market_name}: ❌ ERROR - {result['error']}")
    
    # Save detailed results
    with open('aplus_instruction_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n📁 Detailed results saved to aplus_instruction_analysis.json")

if __name__ == "__main__":
    test_aplus_instruction_consistency()