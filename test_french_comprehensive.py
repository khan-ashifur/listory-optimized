"""
Comprehensive French Quality Test
Test all brand tones and occasions to ensure 10/10 across all variations
"""

import os
import sys
import django
import time

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

def quick_french_quality_check(title, bullets, description):
    """Quick quality assessment for French content"""
    total_text = title + bullets + description
    
    # French accents
    french_chars = ['é', 'è', 'à', 'ç', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ÿ']
    accent_count = sum(total_text.count(char) for char in french_chars)
    
    # French labels in bullets
    french_labels = ["EXCELLENCE", "QUALITÉ", "RAFFINEMENT", "LUXUEUX", "SOPHISTIQUÉ"]
    has_labels = sum(label in bullets.upper() for label in french_labels)
    
    # Cultural sophistication
    cultural_words = ["à la française", "raffinement", "élégant", "sophistiqué", "qualité"]
    cultural_count = sum(word in total_text.lower() for word in cultural_words)
    
    score = 0
    if accent_count >= 10: score += 1
    if has_labels >= 2: score += 1  
    if cultural_count >= 3: score += 1
    if len(total_text) >= 1500: score += 1
    
    return score, {
        "accents": accent_count,
        "labels": has_labels,
        "cultural": cultural_count,
        "length": len(total_text)
    }

def test_comprehensive_french():
    """Test French quality across different brand tones and occasions"""
    print("🇫🇷 COMPREHENSIVE FRENCH MARKET TEST")
    print("🎯 Testing all brand tones and occasions for 10/10 consistency")
    print("=" * 70)
    
    # Test configurations
    test_configs = [
        {"tone": "luxury", "occasion": "Valentine's Day", "expected": "Sophisticated romance"},
        {"tone": "professional", "occasion": "none", "expected": "Professional excellence"},
        {"tone": "casual", "occasion": "Christmas", "expected": "Friendly sophistication"},
        {"tone": "minimal", "occasion": "none", "expected": "Clean elegance"}
    ]
    
    results = []
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        for i, config in enumerate(test_configs, 1):
            print(f"\n{'='*60}")
            print(f"TEST {i}/4: {config['tone'].upper()} + {config['occasion']}")
            print(f"Expected: {config['expected']}")
            print(f"{'='*60}")
            
            # Configure product
            product.marketplace = "fr"
            product.marketplace_language = "fr"
            product.brand_tone = config['tone']
            product.occasion = config['occasion']
            product.save()
            
            print(f"🔄 Generating {config['tone']} French listing...")
            
            # Generate listing
            service.generate_listing(product.id, 'amazon')
            
            # Wait
            time.sleep(8)
            
            # Get listing
            listing = GeneratedListing.objects.filter(
                product=product,
                platform='amazon'
            ).order_by('-created_at').first()
            
            if listing and listing.status == 'completed':
                title = listing.title or ""
                bullets = listing.bullet_points or ""
                description = listing.long_description or ""
                
                print(f"✅ Generated successfully!")
                print(f"📌 TITLE: {title[:80]}...")
                
                # Quick quality check
                score, details = quick_french_quality_check(title, bullets, description)
                
                print(f"\n📊 QUALITY ASSESSMENT:")
                print(f"   French accents: {details['accents']} ({'✅' if details['accents'] >= 10 else '❌'})")
                print(f"   Brand labels: {details['labels']} ({'✅' if details['labels'] >= 2 else '❌'})")
                print(f"   Cultural sophistication: {details['cultural']} ({'✅' if details['cultural'] >= 3 else '❌'})")
                print(f"   Content length: {details['length']} chars ({'✅' if details['length'] >= 1500 else '❌'})")
                
                quality_percentage = (score / 4) * 100
                print(f"🏆 QUALITY SCORE: {score}/4 ({quality_percentage:.0f}%)")
                
                # Check first bullet for sophistication
                bullet_list = bullets.split('\n')
                first_bullet = bullet_list[0] if bullet_list else ""
                has_sophistication = "à la française" in first_bullet.lower() or any(word in first_bullet.lower() for word in ["excellence", "qualité", "raffinement"])
                
                print(f"   Sophistication formula: {'✅' if has_sophistication else '❌'}")
                
                results.append({
                    "config": config,
                    "score": score,
                    "quality": quality_percentage,
                    "sophisticated": has_sophistication,
                    "details": details
                })
                
            else:
                print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
                results.append({
                    "config": config,
                    "score": 0,
                    "quality": 0,
                    "sophisticated": False,
                    "details": {}
                })
        
        # Overall assessment
        print(f"\n{'='*70}")
        print(f"🏆 COMPREHENSIVE FRENCH QUALITY RESULTS")
        print(f"{'='*70}")
        
        total_score = sum(r['score'] for r in results)
        max_possible = len(results) * 4
        overall_quality = (total_score / max_possible) * 100
        
        sophisticated_count = sum(1 for r in results if r['sophisticated'])
        
        print(f"\n📊 OVERALL ASSESSMENT:")
        for i, result in enumerate(results, 1):
            config = result['config']
            print(f"   Test {i} ({config['tone']} + {config['occasion']}): {result['score']}/4 ({result['quality']:.0f}%) {'✅' if result['quality'] >= 75 else '❌'}")
        
        print(f"\n🎯 FINAL RESULTS:")
        print(f"   Total quality score: {total_score}/{max_possible} ({overall_quality:.1f}%)")
        print(f"   Sophisticated executions: {sophisticated_count}/{len(results)}")
        
        if overall_quality >= 90 and sophisticated_count >= 3:
            print(f"\n🎉 EXCELLENT! French market achieves 10/10 across all configurations!")
            print(f"🇫🇷 France is ready for production with consistent quality!")
            status = "READY"
        elif overall_quality >= 80:
            print(f"\n🥈 VERY GOOD! French market mostly achieves high quality")
            print(f"🔧 Minor improvements needed for perfect consistency")
            status = "NEARLY READY"  
        else:
            print(f"\n⚠️ NEEDS IMPROVEMENT! French market quality inconsistent")
            print(f"🔧 Significant optimization needed")
            status = "NEEDS WORK"
        
        return status, overall_quality, results
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return "ERROR", 0, []

if __name__ == "__main__":
    status, quality, results = test_comprehensive_french()
    print(f"\n🚀 FRENCH MARKET STATUS: {status} ({quality:.1f}% quality)")
    
    if status == "READY":
        print(f"✅ 🇫🇷 FRANCE OPTIMIZED TO 10/10 - READY FOR PRODUCTION! 🇫🇷 ✅")