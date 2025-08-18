"""
Quick Market Check - Test one product per market
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

def quick_test():
    """Quick test for all markets"""
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='test_user')
    
    markets = ['us', 'de', 'fr', 'it', 'es']
    
    print("\n" + "="*80)
    print("QUICK MARKET CHECK - LISTORY AI")
    print("="*80)
    
    results = {}
    
    for market in markets:
        print(f"\n Testing {market.upper()}...")
        
        # Create test product
        product = Product.objects.create(
            user=test_user,
            name="Premium Bluetooth Headphones",
            description="High-quality wireless headphones with noise cancellation",
            brand_name="TestBrand",
            brand_tone="professional",
            target_platform="amazon",
            marketplace=market,
            categories="Electronics/Audio",
            features="Noise Cancellation, 30 Hour Battery, Bluetooth 5.3",
            target_audience="Professionals and travelers",
            occasion="christmas" if market == 'us' else 'general'
        )
        
        try:
            # Generate listing
            listing = service.generate_listing(product_id=product.id, platform='amazon')
            
            if listing:
                # Parse results
                title = listing.title or ''
                bullets = json.loads(listing.bullet_points) if listing.bullet_points else []
                description = listing.description or ''
                aplus_content = json.loads(listing.aplus_content) if listing.aplus_content else {}
                
                # Check quality markers
                full_text = f"{title} {' '.join(bullets)} {description}"
                
                quality_checks = {
                    'has_title': bool(title),
                    'title_length': len(title),
                    'bullet_count': len(bullets),
                    'has_description': bool(description),
                    'aplus_sections': len(aplus_content),
                    'total_length': len(full_text)
                }
                
                # Language-specific checks
                if market == 'de':
                    quality_checks['has_umlauts'] = any(c in full_text for c in ['ä', 'ö', 'ü', 'ß'])
                elif market == 'fr':
                    quality_checks['has_accents'] = any(c in full_text for c in ['é', 'è', 'à', 'ç'])
                elif market == 'it':
                    quality_checks['has_accents'] = any(c in full_text for c in ['à', 'è', 'ù', 'ò'])
                elif market == 'es':
                    quality_checks['has_accents'] = any(c in full_text for c in ['á', 'é', 'í', 'ó', 'ú', 'ñ'])
                
                results[market] = quality_checks
                
                # Print summary
                print(f"  ✓ Title: {quality_checks['title_length']} chars")
                print(f"  ✓ Bullets: {quality_checks['bullet_count']} points")
                print(f"  ✓ A+ Content: {quality_checks['aplus_sections']} sections")
                
                if market != 'us':
                    accent_check = quality_checks.get('has_umlauts') or quality_checks.get('has_accents')
                    print(f"  ✓ Native Characters: {'✅ YES' if accent_check else '❌ NO'}")
                
                # Save sample
                with open(f'quick_{market}_sample.json', 'w', encoding='utf-8') as f:
                    json.dump({
                        'title': title[:200],
                        'first_bullet': bullets[0] if bullets else '',
                        'aplus_sections': list(aplus_content.keys())
                    }, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)[:100]}")
            results[market] = {'error': str(e)[:100]}
        
        finally:
            product.delete()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for market, checks in results.items():
        if 'error' in checks:
            print(f"{market.upper()}: ❌ Failed - {checks['error']}")
        else:
            score = sum([
                checks.get('has_title', False),
                checks.get('bullet_count', 0) >= 5,
                checks.get('has_description', False),
                checks.get('aplus_sections', 0) >= 6,
                checks.get('has_umlauts', True) if market == 'de' else True,
                checks.get('has_accents', True) if market in ['fr', 'it', 'es'] else True
            ])
            status = "✅ GOOD" if score >= 5 else "⚠️ NEEDS WORK" if score >= 3 else "❌ POOR"
            print(f"{market.upper()}: {status} ({score}/6 checks passed)")

if __name__ == "__main__":
    quick_test()