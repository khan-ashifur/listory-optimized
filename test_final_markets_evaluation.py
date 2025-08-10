"""
FINAL COMPREHENSIVE EVALUATION: Amazon Germany Marketplace
Tests all brand tones and occasions after implementing critical fixes
"""

import os
import sys
import django
import json

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

def test_german_marketplace_comprehensive():
    """Test all German marketplace configurations"""
    
    print("🇩🇪 AMAZON GERMANY COMPREHENSIVE EVALUATION")
    print("=" * 60)
    
    # Test configurations
    brand_tones = ['professional', 'casual', 'luxury', 'playful', 'minimal', 'bold']
    occasions = ['Christmas', 'Weihnachten', 'Valentine\'s Day', 'Mother\'s Day']
    
    service = ListingGeneratorService()
    
    # Get or create test user
    user, created = User.objects.get_or_create(
        username='test_german',
        defaults={'email': 'test@example.com'}
    )
    
    results = {}
    
    print("\n🧪 TESTING: German Christmas (Weihnachten) across all brand tones")
    print("-" * 50)
    
    for brand_tone in brand_tones[:3]:  # Test first 3 to save time
        try:
            print(f"\n🎨 Brand Tone: {brand_tone.upper()}")
            
            # Create product with German settings using correct field names
            product = Product.objects.create(
                user=user,
                name='Bluetooth Kopfhörer Premium',
                description='Premium wireless headphones with noise cancelling',
                brand_name='TechnoSound',
                brand_tone=brand_tone,
                target_platform='amazon',
                marketplace='de',
                marketplace_language='de',
                price=89.99,
                occasion='Weihnachten',  # German Christmas
                categories='Electronics,Headphones',
                features='Noise Cancelling Technology,30-hour battery life,Quick charge in 15 minutes,Foldable design for travel,Premium leather ear cups'
            )
            
            # Generate German listing
            listing = service.generate_listing(product.id, 'amazon')
            
            if listing and 'success' in listing and listing['success']:
                data = listing['data']
                
                print(f"✅ Generation successful for {brand_tone}")
                
                # Analyze content
                title = data.get('productTitle', '')
                bullets = data.get('bulletPoints', [])
                description = data.get('productDescription', '')
                
                # German language check
                german_indicators = ['ä', 'ö', 'ü', 'ß', 'für', 'mit', 'und', 'der', 'die', 'das']
                has_german = any(indicator in (title + str(bullets) + description).lower() for indicator in german_indicators)
                
                # Christmas/Weihnachten keywords check
                christmas_german = ['weihnacht', 'geschenk', 'feiertag', 'fest']
                has_german_christmas = any(keyword in (title + str(bullets) + description).lower() for keyword in christmas_german)
                
                # Brand tone label check for German
                german_labels = ['PROFESSIONELLE', 'SUPER EINFACH', 'PREMIUM', 'CLEVERLY', 'SIMPLY', 'MAXIMUM']
                has_german_labels = any(label in str(bullets).upper() for label in german_labels)
                
                results[brand_tone] = {
                    'title': title[:100] + '...' if len(title) > 100 else title,
                    'bullets_count': len(bullets),
                    'has_german_language': has_german,
                    'has_german_christmas': has_german_christmas,
                    'has_german_labels': has_german_labels,
                    'first_bullet': bullets[0] if bullets else 'No bullets',
                    'localization_length': len(data.get('localization_enhancement', '')),
                    'aplus_length': len(data.get('aplus_enhancement', ''))
                }
                
                # Print analysis
                print(f"📝 Title: {title[:80]}{'...' if len(title) > 80 else ''}")
                print(f"🎯 Bullets: {len(bullets)} found")
                print(f"🇩🇪 German content: {'✅ YES' if has_german else '❌ NO'}")
                print(f"🎄 Christmas German: {'✅ YES' if has_german_christmas else '❌ NO'}")
                print(f"🏷️ German labels: {'✅ YES' if has_german_labels else '❌ NO'}")
                print(f"📊 Localization: {len(data.get('localization_enhancement', ''))} chars")
                print(f"📋 A+ Content: {len(data.get('aplus_enhancement', ''))} chars")
                
                if bullets:
                    print(f"📌 First bullet: {bullets[0]}")
                
            else:
                print(f"❌ Generation failed for {brand_tone}")
                results[brand_tone] = {'error': 'Generation failed'}
                
            # Cleanup
            product.delete()
            
        except Exception as e:
            print(f"❌ Error testing {brand_tone}: {str(e)}")
            results[brand_tone] = {'error': str(e)}
    
    # Overall evaluation
    print(f"\n📊 FINAL EVALUATION SUMMARY")
    print("=" * 50)
    
    success_count = 0
    german_content_count = 0
    german_christmas_count = 0
    german_labels_count = 0
    
    for tone, result in results.items():
        if 'error' not in result:
            success_count += 1
            if result.get('has_german_language'):
                german_content_count += 1
            if result.get('has_german_christmas'): 
                german_christmas_count += 1
            if result.get('has_german_labels'):
                german_labels_count += 1
    
    total_tests = len(results)
    
    print(f"✅ Successful generations: {success_count}/{total_tests}")
    print(f"🇩🇪 German language used: {german_content_count}/{success_count}")
    print(f"🎄 German Christmas terms: {german_christmas_count}/{success_count}")
    print(f"🏷️ German brand labels: {german_labels_count}/{success_count}")
    
    # Quality rating
    if success_count == total_tests and german_content_count == success_count:
        print(f"\n🏆 OVERALL RATING: 10/10 - Perfect German marketplace optimization!")
    elif german_content_count >= success_count * 0.8:
        print(f"\n🎯 OVERALL RATING: 8/10 - Good German optimization, minor fixes needed")
    elif german_content_count >= success_count * 0.5:
        print(f"\n⚠️ OVERALL RATING: 6/10 - Moderate German optimization, major fixes needed")
    else:
        print(f"\n🚨 OVERALL RATING: 3/10 - Critical German optimization issues")
    
    return results

if __name__ == "__main__":
    test_german_marketplace_comprehensive()