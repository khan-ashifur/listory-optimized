"""
Test Mobile Scan-ability Optimization
Test that bullets are 2-3 sentences, substantial but digestible
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

def analyze_mobile_scan_ability(bullet_text):
    """Analyze bullet scan-ability for mobile optimization"""
    if not bullet_text:
        return {"quality": "empty", "sentences": 0, "avg_words": 0}
    
    # Split into sentences
    import re
    sentences = re.split(r'[.!?–—]\s+', bullet_text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    word_counts = [len(s.split()) for s in sentences]
    avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
    
    # Quality assessment
    if len(sentences) == 1 and avg_words > 40:
        quality = "too_long_single"
    elif len(sentences) == 1 and avg_words < 10:
        quality = "too_short"
    elif 2 <= len(sentences) <= 3 and 10 <= avg_words <= 20:
        quality = "perfect_scan"
    elif 2 <= len(sentences) <= 3:
        quality = "good_structure"
    elif len(sentences) > 3:
        quality = "too_fragmented"
    else:
        quality = "needs_work"
    
    return {
        "quality": quality,
        "sentences": len(sentences),
        "avg_words": avg_words,
        "word_counts": word_counts,
        "scannable": quality in ["perfect_scan", "good_structure"]
    }

def test_mobile_scan_optimization():
    """Test mobile scan-ability optimization"""
    print("📱 MOBILE SCAN-ABILITY OPTIMIZATION TEST")
    print("🎯 Testing: 2-3 sentences, substantial but digestible")
    print("=" * 70)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for German market
        product.marketplace = "de"
        product.marketplace_language = "de" 
        product.brand_tone = "casual"
        product.occasion = "none"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany")
        print(f"📱 Focus: Mobile scan-ability optimization")
        
        print("\n🔄 Generating mobile-optimized German copy...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(10)
        
        # Get the latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ Generation completed!")
            
            # Analyze bullet structure
            bullets = listing.bullet_points or ""
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            print(f"\n📱 MOBILE SCAN-ABILITY ANALYSIS:")
            print("=" * 50)
            
            scan_scores = []
            for i, bullet in enumerate(bullet_list[:5], 1):
                analysis = analyze_mobile_scan_ability(bullet)
                scan_scores.append(analysis['scannable'])
                
                print(f"\n📍 BULLET {i}:")
                print(f"   {bullet}")
                print(f"   Sentences: {analysis['sentences']} ({'✅' if 2 <= analysis['sentences'] <= 3 else '⚠️'})")
                print(f"   Avg words/sentence: {analysis['avg_words']:.1f} ({'✅' if 10 <= analysis['avg_words'] <= 20 else '⚠️'})")
                print(f"   Quality: {analysis['quality']}")
                print(f"   Mobile scannable: {'✅' if analysis['scannable'] else '❌'}")
                
                if analysis['quality'] == 'too_long_single':
                    print(f"   📱 Improvement: Split into 2-3 sentences")
                elif analysis['quality'] == 'too_short':
                    print(f"   📱 Improvement: Add more substantial content")
                elif analysis['quality'] == 'too_fragmented':
                    print(f"   📱 Improvement: Combine into fewer sentences")
                elif analysis['quality'] == 'perfect_scan':
                    print(f"   🎯 Perfect mobile scan-ability!")
            
            # Overall assessment
            scan_percentage = (sum(scan_scores) / len(scan_scores) * 100) if scan_scores else 0
            
            print(f"\n🏆 OVERALL MOBILE SCAN-ABILITY:")
            print(f"   Scannable bullets: {sum(scan_scores)}/{len(scan_scores)}")
            print(f"   Scan-ability score: {scan_percentage:.1f}%")
            
            if scan_percentage >= 80:
                print(f"   📱 EXCELLENT: Mobile-optimized for easy scanning!")
            elif scan_percentage >= 60:
                print(f"   📱 GOOD: Most bullets are mobile-friendly")
            else:
                print(f"   📱 NEEDS WORK: Improve bullet structure for mobile")
            
            # Check umlauts are still preserved
            german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
            total_umlauts = sum(bullets.count(char) for char in german_chars)
            print(f"\n🔤 UMLAUT PRESERVATION: {total_umlauts} umlauts ({'✅' if total_umlauts >= 10 else '❌'})")
            
            return scan_percentage >= 60
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_mobile_scan_optimization()
    print(f"\n🎯 RESULT: {'SUCCESS - Mobile scan-ability optimized!' if success else 'NEEDS MORE WORK'}")