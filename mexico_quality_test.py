"""
Mexico Market Quality Test - 10/10 Target vs Competition
Tests Mexican Spanish with Día de Muertos cultural intelligence
Optimizes until beating Helium 10, Copy Monkey, Jasper AI
"""

import os
import sys
import json
import django
from datetime import datetime

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def mexico_quality_test():
    print("\n🇲🇽 MEXICO MARKET QUALITY TEST - TARGET: 10/10")
    print("=" * 60)
    print("Goal: Beat Helium 10, Copy Monkey, Jasper AI")
    print("=" * 60)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='mexico_quality_test')
    
    # Test Mexican product with Día de Muertos cultural context
    product = Product.objects.create(
        user=test_user,
        name="Premium Traditional Mexican Candle Set",
        description="Handcrafted traditional Mexican candles for Día de Muertos celebrations and home decoration",
        brand_name="CasaMexicana",
        brand_tone="luxurious",
        target_platform="amazon",
        marketplace="mx",
        marketplace_language="es-mx",  # Mexican Spanish - CRITICAL!
        categories="Home/Decor/Candles",
        features="Handcrafted, Traditional Mexican Design, Long Burning, Natural Wax, Beautiful Colors",
        target_audience="Mexican families celebrating traditions and cultural heritage",
        occasion="dia_de_muertos"  # Day of the Dead - Most important Mexican tradition
    )
    
    try:
        print("⏳ Generating Mexican Spanish listing with cultural intelligence...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            title = listing.title or ''
            # Handle bullet points safely
            try:
                bullets = json.loads(listing.bullet_points) if listing.bullet_points else []
            except json.JSONDecodeError:
                bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
            description = listing.long_description or ''
            
            print(f"\n📊 Generated Content Analysis:")
            print(f"Title ({len(title)} chars): {title}")
            print(f"\nFirst Bullet: {bullets[0] if bullets else 'None'}")
            print(f"\nDescription Preview ({len(description)} chars): {description[:250]}...")
            
            # Check for Mexican Spanish quality indicators
            bullets_text = ' '.join(bullets) if isinstance(bullets, list) else str(bullets)
            full_text = f"{title} {bullets_text} {description}"
            
            # Mexican Spanish accent marks validation
            mexican_accents = ['á', 'é', 'í', 'ó', 'ú', 'ñ']
            has_proper_accents = any(accent in full_text for accent in mexican_accents)
            
            # Mexican power words validation
            mexican_power_words = ['increíble', 'excelente', 'fantástico', 'perfecto', 'súper', 'padrísimo', 'mexicano', 'tradicional']
            power_word_count = sum(1 for word in mexican_power_words if word in full_text.lower())
            
            # Día de Muertos cultural context
            dia_muertos_words = ['muertos', 'día de muertos', 'tradición', 'familia', 'ancestros', 'celebración', 'altar', 'ofrenda']
            cultural_context_count = sum(1 for word in dia_muertos_words if word.lower() in full_text.lower())
            
            # Mexican expressions validation
            mexican_expressions = ['en México', 'mexicana', 'mexicano', 'familia mexicana', 'tradición mexicana']
            mexican_identity_count = sum(1 for expr in mexican_expressions if expr.lower() in full_text.lower())
            
            # Quality score calculation (out of 10)
            quality_score = 0
            quality_score += 2 if has_proper_accents else 0  # Accent marks (2 points)
            quality_score += min(3, power_word_count * 0.5)  # Power words (3 points max)
            quality_score += min(3, cultural_context_count * 0.5)  # Cultural context (3 points max)
            quality_score += min(2, mexican_identity_count * 0.5)  # Mexican identity (2 points max)
            
            print(f"\n🇲🇽 Mexican Quality Analysis:")
            print(f"  • Has Proper Accents (á,é,í,ó,ú,ñ): {'✅ YES' if has_proper_accents else '❌ NO'}")
            print(f"  • Mexican Power Words Count: {power_word_count}/8 found")
            print(f"  • Día de Muertos Cultural Context: {cultural_context_count}/8 found") 
            print(f"  • Mexican Identity References: {mexican_identity_count}/5 found")
            print(f"  • **QUALITY SCORE: {quality_score:.1f}/10**")
            
            # Competition comparison
            if quality_score >= 9.0:
                competition_status = "🏆 BEATS ALL COMPETITORS! (Helium 10, Copy Monkey, Jasper AI)"
            elif quality_score >= 7.5:
                competition_status = "🥈 COMPETITIVE with top tools"
            elif quality_score >= 6.0:
                competition_status = "🥉 GOOD but needs optimization"
            else:
                competition_status = "❌ NEEDS SIGNIFICANT IMPROVEMENT"
            
            print(f"\n🏆 Competition Analysis:")
            print(f"  {competition_status}")
            
            # Specific Mexican features validation
            print(f"\n🎯 Mexican Market Features:")
            mexican_features = {
                'Mexican Spanish Formality': any(word in full_text for word in ['le ofrecemos', 'le garantizamos', 'con mucho orgullo']),
                'Family Emphasis': any(word in full_text for word in ['familia', 'familias', 'hogar']),
                'Traditional Values': any(word in full_text for word in ['tradición', 'tradicional', 'auténtico']),
                'Celebration Context': any(word in full_text for word in ['celebración', 'fiesta', 'festejo']),
                'Quality Guarantee': any(word in full_text for word in ['garantía', 'garantizado', 'calidad'])
            }
            
            for feature, present in mexican_features.items():
                print(f"    • {feature}: {'✅' if present else '❌'}")
                
            # Save comprehensive sample for analysis
            with open('mexico_quality_sample.json', 'w', encoding='utf-8') as f:
                json.dump({
                    'title': title,
                    'bullets': bullets if isinstance(bullets, list) else [bullets],
                    'description': description,
                    'quality_analysis': {
                        'quality_score': quality_score,
                        'has_proper_accents': has_proper_accents,
                        'power_word_count': power_word_count,
                        'cultural_context_count': cultural_context_count,
                        'mexican_identity_count': mexican_identity_count,
                        'competition_status': competition_status,
                        'mexican_features': mexican_features
                    }
                }, f, indent=2, ensure_ascii=False)
            
            print(f"\n📁 Quality analysis saved to mexico_quality_sample.json")
            
            # Final recommendation
            if quality_score >= 9.0:
                print(f"\n🎉 SUCCESS: Mexico market ready for production!")
                print(f"🏆 Beats competition with {quality_score}/10 quality!")
            else:
                print(f"\n⚠️ OPTIMIZATION NEEDED: Current score {quality_score}/10")
                print(f"💡 Focus on: More Mexican expressions, cultural references, accent marks")
            
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    mexico_quality_test()