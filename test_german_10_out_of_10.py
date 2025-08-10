"""
German 10/10 Quality Test - Comprehensive Assessment
Tests all three critical areas:
1. Complete umlaut accuracy 
2. Mobile-optimized bullet structure
3. Emotional hooks in first bullet
"""

import os
import sys
import django
import time
import re

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

def analyze_bullet_structure(bullet_text):
    """Analyze bullet point structure for mobile optimization"""
    if not bullet_text:
        return {"sentences": 0, "mobile_optimized": False, "word_count": 0}
    
    # Count sentences (split by . or – or ; or !)
    sentences = re.split(r'[.!;–—]\s+', bullet_text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    # Count words
    words = len(bullet_text.split())
    
    # Mobile optimized = 1-2 sentences, max 50 words
    mobile_optimized = 1 <= len(sentences) <= 2 and words <= 50
    
    return {
        "sentences": len(sentences),
        "mobile_optimized": mobile_optimized,
        "word_count": words,
        "sentence_lengths": [len(s.split()) for s in sentences]
    }

def check_emotional_hook(first_bullet):
    """Check if first bullet follows emotional hook formula"""
    if not first_bullet:
        return {"has_hook": False, "pattern_matched": "none"}
    
    # Check for "wie ein Profi" pattern
    if "wie ein profi" in first_bullet.lower():
        if "ganz ohne" in first_bullet.lower():
            return {"has_hook": True, "pattern_matched": "perfect_formula"}
        else:
            return {"has_hook": True, "pattern_matched": "partial_formula"}
    
    # Check for other emotional hooks
    emotional_starters = [
        "endlich", "nie wieder", "schluss mit", "verwandeln sie", 
        "genießen sie", "erleben sie", "entdecken sie"
    ]
    
    for starter in emotional_starters:
        if starter in first_bullet.lower():
            return {"has_hook": True, "pattern_matched": "emotional_starter"}
    
    return {"has_hook": False, "pattern_matched": "none"}

def comprehensive_umlaut_check(text):
    """Comprehensive umlaut accuracy check"""
    if not text:
        return {"missing_umlauts": [], "total_umlauts": 0, "accuracy": 100}
    
    text_lower = text.lower()
    
    # Common words that need umlauts
    umlaut_words = {
        'fur ': 'für ',
        'gr ': 'grö', # part of größer, größe, etc
        'grosser': 'größer',
        'grosse': 'große',
        'grosse ': 'große ',
        'kuhl': 'kühl',
        'kuhle': 'kühle',
        'kuhlung': 'kühlung',
        'qualitat': 'qualität',
        'naturlich': 'natürlich',
        'muhelos': 'mühelos',
        'oberflache': 'oberfläche',
        'warme': 'wärme',
        'warmer': 'wärmer',
        'kalter': 'kälter',
        'schon ': 'schön ',
        'horen': 'hören',
        'fuhlen': 'fühlen',
        'zuverlas': 'zuverläs', # part of zuverlässig
        'heiss': 'heiß',
        'abkuhl': 'abkühl' # part of abkühlung
    }
    
    missing_umlauts = []
    for wrong, correct in umlaut_words.items():
        if wrong in text_lower:
            missing_umlauts.append(f"'{wrong.strip()}' should be '{correct.strip()}'")
    
    # Count existing umlauts
    german_chars = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
    total_umlauts = sum(text.count(char) for char in german_chars)
    
    # Calculate accuracy (fewer missing = higher accuracy)
    accuracy = max(0, 100 - (len(missing_umlauts) * 10))
    
    return {
        "missing_umlauts": missing_umlauts,
        "total_umlauts": total_umlauts,
        "accuracy": accuracy
    }

def test_german_10_out_of_10():
    """Comprehensive 10/10 German quality test"""
    print("🇩🇪 GERMAN 10/10 QUALITY OPTIMIZATION TEST")
    print("🎯 Testing: Umlauts + Mobile Bullets + Emotional Hooks")
    print("=" * 80)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return 0, 10
        
        # Configure for German market with different tone/occasion for variety
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "professional"  # Changed from luxury
        product.occasion = "none"  # Changed from Valentine's Day
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇩🇪 Market: Germany")
        print(f"🎨 Brand Tone: Professional")
        print(f"🎯 Focus: 10/10 Native German Quality")
        
        print("\n🔄 Generating optimized German copy...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for generation...")
        time.sleep(12)
        
        # Get the latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ Generation completed!")
            
            # Get content
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            description = listing.long_description or ""
            
            print(f"\n🏆 COMPREHENSIVE 10/10 QUALITY ASSESSMENT:")
            print("=" * 60)
            
            # 1. UMLAUT ACCURACY CHECK
            print(f"\n1️⃣ UMLAUT ACCURACY CHECK")
            total_text = title + bullets + description
            umlaut_results = comprehensive_umlaut_check(total_text)
            
            print(f"📌 TITLE: {title}")
            title_umlaut = comprehensive_umlaut_check(title)
            print(f"   Title umlauts: {title_umlaut['total_umlauts']} ({'✅' if title_umlaut['total_umlauts'] > 0 else '❌'})")
            print(f"   Title accuracy: {title_umlaut['accuracy']}% ({'✅' if title_umlaut['accuracy'] >= 90 else '❌'})")
            
            if title_umlaut['missing_umlauts']:
                print(f"   ⚠️ Title issues: {', '.join(title_umlaut['missing_umlauts'][:3])}")
            
            print(f"\n📍 BULLETS UMLAUT CHECK:")
            print(f"   Total umlauts: {umlaut_results['total_umlauts']} ({'✅' if umlaut_results['total_umlauts'] >= 10 else '❌'})")
            print(f"   Overall accuracy: {umlaut_results['accuracy']}% ({'✅' if umlaut_results['accuracy'] >= 90 else '❌'})")
            
            if umlaut_results['missing_umlauts']:
                print(f"   ⚠️ Missing umlauts found: {len(umlaut_results['missing_umlauts'])} issues")
                for issue in umlaut_results['missing_umlauts'][:3]:
                    print(f"      - {issue}")
            
            # 2. BULLET STRUCTURE ANALYSIS
            print(f"\n2️⃣ MOBILE-OPTIMIZED BULLET STRUCTURE")
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            mobile_scores = []
            for i, bullet in enumerate(bullet_list[:5], 1):
                structure = analyze_bullet_structure(bullet)
                mobile_optimized = structure['mobile_optimized']
                mobile_scores.append(mobile_optimized)
                
                print(f"   Bullet {i}: {bullet[:50]}...")
                print(f"      Sentences: {structure['sentences']} ({'✅' if structure['sentences'] <= 2 else '❌'})")
                print(f"      Words: {structure['word_count']} ({'✅' if structure['word_count'] <= 50 else '❌'})")
                print(f"      Mobile optimized: {'✅' if mobile_optimized else '❌'}")
                
                if structure['sentences'] > 2:
                    print(f"      📱 Split needed: Too many sentences for mobile")
                if structure['word_count'] > 50:
                    print(f"      📱 Too long: Reduce word count for mobile")
            
            mobile_score = sum(mobile_scores) / len(mobile_scores) * 100 if mobile_scores else 0
            
            # 3. EMOTIONAL HOOK CHECK
            print(f"\n3️⃣ EMOTIONAL HOOK ANALYSIS")
            if bullet_list:
                first_bullet = bullet_list[0]
                hook_results = check_emotional_hook(first_bullet)
                
                print(f"   First bullet: {first_bullet}")
                print(f"   Has emotional hook: {'✅' if hook_results['has_hook'] else '❌'}")
                print(f"   Pattern matched: {hook_results['pattern_matched']}")
                
                if hook_results['pattern_matched'] == 'perfect_formula':
                    print(f"   🎯 Perfect: Uses 'wie ein Profi – ganz ohne' formula")
                elif hook_results['pattern_matched'] == 'partial_formula':
                    print(f"   ⚠️ Good: Uses 'wie ein Profi' but missing 'ganz ohne'")
                elif hook_results['pattern_matched'] == 'emotional_starter':
                    print(f"   ✅ Good: Uses emotional starter words")
                else:
                    print(f"   ❌ Needs improvement: No emotional hook detected")
            else:
                hook_results = {"has_hook": False, "pattern_matched": "none"}
                print(f"   ❌ No bullets found")
            
            # FINAL SCORING
            print(f"\n📊 FINAL 10/10 QUALITY ASSESSMENT:")
            print("=" * 50)
            
            # Calculate individual scores
            umlaut_score = 1 if umlaut_results['accuracy'] >= 90 and umlaut_results['total_umlauts'] >= 10 else 0
            mobile_structure_score = 1 if mobile_score >= 80 else 0
            emotional_hook_score = 1 if hook_results['has_hook'] and hook_results['pattern_matched'] in ['perfect_formula', 'partial_formula'] else 0
            title_umlaut_score = 1 if title_umlaut['accuracy'] >= 90 and title_umlaut['total_umlauts'] > 0 else 0
            
            # Additional quality checks
            gift_words = ['geschenk', 'valentinstag', 'weihnachten', 'geburtstag']
            has_gift_angle = any(word in total_text.lower() for word in gift_words)
            gift_score = 1 if has_gift_angle else 0
            
            description_quality = 1 if len(description) > 800 and umlaut_results['total_umlauts'] > 0 else 0
            
            criteria = {
                "Umlaut accuracy (90%+)": umlaut_score,
                "Title has proper umlauts": title_umlaut_score,
                "Mobile-optimized bullets (80%+)": mobile_structure_score,
                "Emotional hook in bullet 1": emotional_hook_score,
                "Gift/seasonal angle": gift_score,
                "Rich description quality": description_quality
            }
            
            total_score = sum(criteria.values())
            max_score = len(criteria)
            
            print(f"📋 QUALITY CRITERIA:")
            for criterion, passed in criteria.items():
                print(f"   {criterion}: {'✅ PASS' if passed else '❌ FAIL'}")
            
            print(f"\n🏆 FINAL SCORE: {total_score}/{max_score}")
            percentage = (total_score / max_score) * 100
            
            if total_score == max_score:
                print("🎉 PERFECT: 10/10 Native German Quality Achieved!")
                grade = "A+"
            elif total_score >= max_score - 1:
                print("🥇 EXCELLENT: 9/10 High-quality German copy!")
                grade = "A"
            elif total_score >= max_score - 2:
                print("🥈 VERY GOOD: 8/10 Good German copy with minor improvements needed")
                grade = "B+"
            elif total_score >= max_score - 3:
                print("🥉 GOOD: 7/10 Solid German copy, several areas need work")
                grade = "B"
            else:
                print("⚠️ NEEDS SIGNIFICANT IMPROVEMENT: Major quality issues")
                grade = "C"
            
            print(f"📈 Quality Grade: {grade} ({percentage:.1f}%)")
            
            # Specific improvement recommendations
            if total_score < max_score:
                print(f"\n🔧 IMPROVEMENT RECOMMENDATIONS:")
                if not umlaut_score:
                    print(f"   • Fix umlaut accuracy: Currently {umlaut_results['accuracy']}%, need 90%+")
                if not title_umlaut_score:
                    print(f"   • Add umlauts to title: Currently {title_umlaut['total_umlauts']} umlauts")
                if not mobile_structure_score:
                    print(f"   • Optimize bullet structure: Currently {mobile_score:.1f}% mobile-friendly")
                if not emotional_hook_score:
                    print(f"   • Add emotional hook: Use 'wie ein Profi – ganz ohne' formula")
                if not gift_score:
                    print(f"   • Add gift angle: Include seasonal or gift messaging")
                if not description_quality:
                    print(f"   • Improve description: Need 800+ chars with proper umlauts")
            
            return total_score, max_score
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            return 0, 6
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 0, 6

if __name__ == "__main__":
    score, total = test_german_10_out_of_10()
    print(f"\n🎯 FINAL RESULT: {score}/{total} ({'READY FOR PRODUCTION' if score >= total - 1 else 'NEEDS MORE OPTIMIZATION'})")