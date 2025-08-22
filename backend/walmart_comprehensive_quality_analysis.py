#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to the Python path
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User
import json

def comprehensive_walmart_analysis():
    print('🏪 COMPREHENSIVE WALMART QUALITY ANALYSIS - ALL MARKETS')
    print('=' * 70)
    print('Testing USA, Canada, and Mexico for 10/10 quality consistency\n')

    user, created = User.objects.get_or_create(username='walmart_quality_analysis')
    service = ListingGeneratorService()
    
    test_results = {}
    
    # Test cases for each market
    test_cases = [
        {
            'market': 'walmart_usa',
            'flag': '🇺🇸',
            'name': 'Premium Gaming Headset Pro',
            'brand': 'AudioTech',
            'occasion': 'black_friday',
            'price': 129.99,
            'features': 'Wireless Bluetooth 5.3\nActive Noise Cancellation\n50mm Drivers\n35H Battery\nRGB Lighting\nUL Listed Safety',
            'cultural_elements': ['america', 'usa', 'black friday', 'ul listed'],
            'language': 'en-us'
        },
        {
            'market': 'walmart_canada',
            'flag': '🇨🇦',
            'name': 'Premium Gaming Headset Pro',
            'brand': 'AudioTech',
            'occasion': 'boxing_day',
            'price': 149.99,
            'features': 'Wireless Bluetooth 5.3\nActive Noise Cancellation\n50mm Drivers\n35H Battery\nRGB Lighting\nCSA Certified',
            'cultural_elements': ['canada', 'boxing day', 'rollback', 'csa'],
            'language': 'en-ca'
        },
        {
            'market': 'walmart_mexico',
            'flag': '🇲🇽',
            'name': 'Audífonos Gaming Premium Pro',
            'brand': 'AudioTech',
            'occasion': 'dia_de_los_muertos',
            'price': 2499.99,
            'features': 'Bluetooth Inalámbrico 5.3\nCancelación Activa Ruido\nDrivers 50mm\nBatería 35H\nIluminación RGB\nCertificación NOM',
            'cultural_elements': ['méxico', 'muertos', 'nom', 'tradición'],
            'language': 'es-mx'
        }
    ]
    
    for case in test_cases:
        print(f"{case['flag']} TESTING {case['market'].upper().replace('_', ' ')}")
        print('-' * 50)
        
        # Create test product
        product = Product.objects.create(
            user=user,
            name=case['name'],
            brand_name=case['brand'],
            target_platform='walmart',
            marketplace=case['market'],
            marketplace_language=case['language'],
            price=case['price'],
            occasion=case['occasion'],
            brand_tone='trendy',
            categories='Electronics > Gaming > Audio',
            description='Professional gaming headset with advanced features',
            features=case['features']
        )
        
        try:
            # Generate listing
            listing = service.generate_listing(product.id, 'walmart')
            
            # Quality Analysis
            quality_score = 0
            max_score = 10
            issues = []
            
            # 1. Title Quality (2 points)
            title = listing.walmart_product_title
            if len(title) >= 50 and len(title) <= 100:
                quality_score += 2
            elif len(title) >= 40:
                quality_score += 1
                issues.append(f"Title could be longer ({len(title)} chars)")
            else:
                issues.append(f"Title too short ({len(title)} chars)")
            
            # 2. Cultural Integration (2 points)
            title_lower = title.lower()
            features_lower = listing.walmart_key_features.lower()
            cultural_found = sum(1 for element in case['cultural_elements'] 
                               if element in title_lower or element in features_lower)
            if cultural_found >= 3:
                quality_score += 2
            elif cultural_found >= 2:
                quality_score += 1
                issues.append(f"Could improve cultural integration ({cultural_found}/4 elements)")
            else:
                issues.append(f"Poor cultural integration ({cultural_found}/4 elements)")
            
            # 3. Features Quality (2 points)
            features = listing.walmart_key_features.split('\n')
            if len(features) >= 5 and all(len(f.strip()) > 30 for f in features[:5]):
                quality_score += 2
            elif len(features) >= 4:
                quality_score += 1
                issues.append("Features could be more detailed")
            else:
                issues.append("Insufficient feature detail")
            
            # 4. Compliance Guidance (1 point)
            compliance = listing.walmart_compliance_certifications
            if '[SELLER TO PROVIDE]' in compliance:
                quality_score += 1
            else:
                issues.append("Missing proper compliance guidance")
            
            # 5. Pricing Integration (1 point)
            specs = json.loads(listing.walmart_specifications)
            if str(case['price']) in specs.get('Price', ''):
                quality_score += 1
            else:
                issues.append("Price not properly integrated")
            
            # 6. Brand Tone Consistency (1 point)
            if 'trendy' in title_lower or 'modern' in title_lower or 'latest' in title_lower:
                quality_score += 1
            else:
                issues.append("Brand tone not reflected")
            
            # 7. Occasion Optimization (1 point)
            occasion_keywords = {
                'black_friday': ['black friday', 'deal', 'sale'],
                'boxing_day': ['boxing day', 'canada', 'sale'],
                'dia_de_los_muertos': ['muertos', 'día', 'tradición']
            }
            occasion_found = any(kw in title_lower or kw in features_lower 
                               for kw in occasion_keywords.get(case['occasion'], []))
            if occasion_found:
                quality_score += 1
            else:
                issues.append("Occasion not properly optimized")
            
            # 8. Technical Specifications (1 point)
            tech_specs = ['bluetooth', '5.3', '50mm', '35h', 'rgb']
            tech_found = sum(1 for spec in tech_specs if spec in features_lower)
            if tech_found >= 4:
                quality_score += 1
            else:
                issues.append(f"Technical specs incomplete ({tech_found}/5)")
            
            # Store results
            test_results[case['market']] = {
                'quality_score': quality_score,
                'max_score': max_score,
                'percentage': (quality_score / max_score) * 100,
                'title': title,
                'title_length': len(title),
                'cultural_elements': cultural_found,
                'feature_count': len(features),
                'issues': issues,
                'listing_id': listing.id
            }
            
            # Display results
            print(f"Quality Score: {quality_score}/{max_score} ({(quality_score/max_score)*100:.1f}%)")
            print(f"Title: {title}")
            print(f"Length: {len(title)} chars")
            print(f"Cultural Elements: {cultural_found}/{len(case['cultural_elements'])}")
            print(f"Features: {len(features)}")
            if issues:
                print(f"Issues: {', '.join(issues)}")
            else:
                print("✅ PERFECT QUALITY!")
            print(f"URL: http://localhost:3000/results/{listing.id}")
            print()
            
        except Exception as e:
            test_results[case['market']] = {
                'error': str(e),
                'quality_score': 0,
                'percentage': 0
            }
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            print()
        finally:
            product.delete()
    
    # Overall Analysis
    print('🎯 OVERALL WALMART MARKETPLACE ANALYSIS')
    print('=' * 50)
    
    total_score = 0
    total_possible = 0
    market_results = []
    
    for market, results in test_results.items():
        if 'error' not in results:
            total_score += results['quality_score']
            total_possible += results['max_score']
            market_results.append((market, results['percentage']))
            print(f"{market.replace('_', ' ').title()}: {results['quality_score']}/{results['max_score']} ({results['percentage']:.1f}%)")
    
    if total_possible > 0:
        overall_percentage = (total_score / total_possible) * 100
        print(f"\n🏆 OVERALL SCORE: {total_score}/{total_possible} ({overall_percentage:.1f}%)")
        
        if overall_percentage >= 90:
            print("✅ EXCELLENT! All Walmart markets achieve 9+ quality")
        elif overall_percentage >= 80:
            print("✅ GOOD! Most markets achieve high quality")
        else:
            print("⚠️ NEEDS IMPROVEMENT! Quality inconsistent across markets")
        
        # Consistency check
        if market_results:
            percentages = [p for _, p in market_results]
            consistency = 100 - (max(percentages) - min(percentages))
            print(f"🎯 CONSISTENCY SCORE: {consistency:.1f}%")
            
            if consistency >= 95:
                print("🎉 PERFECT CONSISTENCY across all markets!")
            elif consistency >= 85:
                print("✅ Good consistency across markets")
            else:
                print("⚠️ Quality varies significantly between markets")
    
    print(f"\n🧹 Analysis completed!")

if __name__ == '__main__':
    comprehensive_walmart_analysis()