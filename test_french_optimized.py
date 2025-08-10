"""
Test Optimized French Market Quality
Verify 10/10 French quality improvements with all enhancements
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

def analyze_french_accent_accuracy(text):
    """Analyze French accent accuracy"""
    if not text:
        return {"missing_accents": [], "total_accents": 0, "accuracy": 100}
    
    text_lower = text.lower()
    
    # Common words that need French accents
    accent_words = {
        'qualite': 'qualité',
        'elegant': 'élégant',
        'francais': 'français', 
        'tres': 'très',
        'etre': 'être',
        'premiere': 'première',
        'cree': 'créé',
        'developpe': 'développé',
        'integre': 'intégré',
        'securite': 'sécurité',
        'concu': 'conçu',
        'precision': 'précision',
        'efficacite': 'efficacité'
    }
    
    missing_accents = []
    for wrong, correct in accent_words.items():
        if wrong in text_lower and correct not in text_lower:
            missing_accents.append(f"'{wrong}' should be '{correct}'")
    
    # Count existing French accents
    french_chars = ['é', 'è', 'à', 'ç', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ÿ', 'É', 'È', 'À', 'Ç']
    total_accents = sum(text.count(char) for char in french_chars)
    
    # Calculate accuracy
    accuracy = max(0, 100 - (len(missing_accents) * 5))
    
    return {
        "missing_accents": missing_accents,
        "total_accents": total_accents,
        "accuracy": accuracy
    }

def analyze_french_sophistication(bullet_text):
    """Analyze French sophistication and structure"""
    if not bullet_text:
        return {"sophisticated": False, "has_formula": False, "mobile_optimized": False}
    
    # Check for sophistication formula "à la française – sans"
    has_formula = "à la française" in bullet_text.lower() and "sans" in bullet_text.lower()
    
    # Check for sophisticated vocabulary
    sophisticated_words = ["raffinement", "élégant", "sophistiqué", "excellence", "qualité", "français", "authentique"]
    has_sophisticated = any(word in bullet_text.lower() for word in sophisticated_words)
    
    # Check mobile structure
    sentences = re.split(r'[.!?–—]\s+', bullet_text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    mobile_optimized = 2 <= len(sentences) <= 3
    
    return {
        "sophisticated": has_sophisticated,
        "has_formula": has_formula,
        "mobile_optimized": mobile_optimized,
        "sentences": len(sentences)
    }

def test_french_10_out_of_10():
    """Test optimized French market for 10/10 quality"""
    print("🇫🇷 FRENCH 10/10 QUALITY OPTIMIZATION TEST")
    print("🎯 Testing: Accents + Sophistication + Brand Labels + Cultural Elements")
    print("=" * 80)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return 0, 10
        
        # Configure for French market with luxury tone
        product.marketplace = "fr"
        product.marketplace_language = "fr"
        product.brand_tone = "luxury"  # Perfect for French sophistication
        product.occasion = "Christmas"  # Test seasonal integration
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇫🇷 Market: France")
        print(f"🎨 Brand Tone: Luxury (French sophistication)")
        print(f"🎄 Occasion: Christmas")
        
        print("\n🔄 Generating optimized French listing...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Waiting for French optimization...")
        time.sleep(15)
        
        # Get the latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ French generation completed!")
            
            # Get content
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            description = listing.long_description or ""
            total_text = title + bullets + description
            
            print(f"\n🏆 COMPREHENSIVE FRENCH 10/10 QUALITY ASSESSMENT:")
            print("=" * 60)
            
            # 1. FRENCH ACCENT ACCURACY
            print(f"\n1️⃣ FRENCH ACCENT ACCURACY CHECK")
            accent_results = analyze_french_accent_accuracy(total_text)
            
            print(f"📌 TITLE: {title}")
            title_accent = analyze_french_accent_accuracy(title)
            print(f"   Title accents: {title_accent['total_accents']} ({'✅' if title_accent['total_accents'] > 0 else '❌'})")
            print(f"   Title accuracy: {title_accent['accuracy']}% ({'✅' if title_accent['accuracy'] >= 95 else '❌'})")
            
            print(f"\n📍 FRENCH ACCENT RESULTS:")
            print(f"   Total accents: {accent_results['total_accents']} ({'✅' if accent_results['total_accents'] >= 15 else '❌'})")
            print(f"   Overall accuracy: {accent_results['accuracy']}% ({'✅' if accent_results['accuracy'] >= 95 else '❌'})")
            
            if accent_results['missing_accents']:
                print(f"   ⚠️ Missing accents: {len(accent_results['missing_accents'])} issues")
                for issue in accent_results['missing_accents'][:3]:
                    print(f"      - {issue}")
            
            # 2. FRENCH BULLET LABEL ANALYSIS
            print(f"\n2️⃣ FRENCH BULLET LABELS & SOPHISTICATION")
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            french_labels = ["EXCELLENCE", "QUALITÉ", "RAFFINEMENT", "LUXUEUX", "SOPHISTIQUÉ", "FRANÇAIS", "PREMIUM"]
            sophistication_scores = []
            
            for i, bullet in enumerate(bullet_list[:5], 1):
                if bullet:
                    print(f"\n   BULLET {i}: {bullet[:80]}...")
                    
                    # Check for French labels
                    has_french_label = any(label in bullet.upper() for label in french_labels)
                    has_colon = ":" in bullet[:50]
                    
                    # Analyze sophistication
                    soph_analysis = analyze_french_sophistication(bullet)
                    sophistication_scores.append(soph_analysis['sophisticated'] and soph_analysis['mobile_optimized'])
                    
                    print(f"      French label: {'✅' if has_french_label and has_colon else '❌'}")
                    print(f"      Sophistication: {'✅' if soph_analysis['sophisticated'] else '❌'}")
                    print(f"      French formula: {'✅' if soph_analysis['has_formula'] else '❌'}")
                    print(f"      Mobile structure: {'✅' if soph_analysis['mobile_optimized'] else '❌'} ({soph_analysis['sentences']} sentences)")
            
            sophistication_percentage = (sum(sophistication_scores) / len(sophistication_scores) * 100) if sophistication_scores else 0
            
            # 3. FRENCH CULTURAL ELEMENTS
            print(f"\n3️⃣ FRENCH CULTURAL ELEMENTS")
            cultural_phrases = ["à la française", "art de vivre", "raffinement", "sophistication", "qualité française", "élégance", "savoir-faire"]
            cultural_found = sum(phrase in total_text.lower() for phrase in cultural_phrases)
            print(f"   Cultural phrases found: {cultural_found}/7 ({'✅' if cultural_found >= 4 else '❌'})")
            
            # 4. CHRISTMAS/SEASONAL INTEGRATION
            print(f"\n4️⃣ SEASONAL INTEGRATION (Christmas)")
            christmas_words = ["noël", "cadeau", "offrir", "fêtes", "saison", "hiver"]
            christmas_found = sum(word in total_text.lower() for word in christmas_words)
            print(f"   Christmas elements: {christmas_found}/6 ({'✅' if christmas_found >= 2 else '❌'})")
            
            # 5. OVERALL QUALITY SCORING
            print(f"\n5️⃣ FINAL 10/10 QUALITY ASSESSMENT")
            
            criteria = {
                "French accent accuracy (95%+)": accent_results['accuracy'] >= 95,
                "High accent count (15+)": accent_results['total_accents'] >= 15,
                "Sophisticated bullets (80%+)": sophistication_percentage >= 80,
                "French cultural elements (4+)": cultural_found >= 4,
                "Seasonal integration": christmas_found >= 2,
                "Rich content length": len(total_text) >= 1800
            }
            
            score = sum(criteria.values())
            total_criteria = len(criteria)
            
            print(f"📋 FRENCH QUALITY CRITERIA:")
            for criterion, passed in criteria.items():
                print(f"   {criterion}: {'✅ PASS' if passed else '❌ NEEDS WORK'}")
            
            final_score = (score / total_criteria) * 10
            
            print(f"\n🏆 FINAL FRENCH SCORE: {score}/{total_criteria} ({final_score:.1f}/10)")
            
            if final_score >= 9:
                print("🎉 PARFAIT! 10/10 French quality achieved!")
                grade = "A+"
            elif final_score >= 8:
                print("🥇 EXCELLENT! 9/10 High-quality French sophistication!")
                grade = "A"
            elif final_score >= 7:
                print("🥈 TRÈS BIEN! 8/10 Good French quality, minor improvements needed")
                grade = "B+"
            elif final_score >= 6:
                print("🥉 BIEN! 7/10 Decent French copy, several areas need work")
                grade = "B"
            else:
                print("⚠️ À AMÉLIORER! Significant French quality improvements needed")
                grade = "C"
            
            print(f"📈 French Quality Grade: {grade} ({final_score:.1f}/10)")
            
            # Improvement recommendations
            if final_score < 10:
                print(f"\n🔧 FRENCH IMPROVEMENT RECOMMENDATIONS:")
                if not criteria["French accent accuracy (95%+"]:
                    print(f"   • Fix accent accuracy: Currently {accent_results['accuracy']}%, need 95%+")
                if not criteria["High accent count (15+)"]:
                    print(f"   • Add more French accents: Currently {accent_results['total_accents']}, need 15+")
                if not criteria["Sophisticated bullets (80%+)"]:
                    print(f"   • Enhance sophistication: Currently {sophistication_percentage:.1f}%, need 80%+")
                if not criteria["French cultural elements (4+)"]:
                    print(f"   • Add cultural elements: Currently {cultural_found}, need 4+")
                if not criteria["Seasonal integration"]:
                    print(f"   • Improve Christmas messaging: Currently {christmas_found}, need 2+")
            
            return final_score, total_criteria
            
        else:
            print(f"❌ French generation failed: {listing.status if listing else 'Not found'}")
            return 0, 6
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 0, 6

if __name__ == "__main__":
    score, total = test_french_10_out_of_10()
    if score >= 9:
        print(f"\n🎉 FRANCE READY! 10/10 quality achieved! 🇫🇷")
    else:
        print(f"\n🔧 FRANCE NEEDS MORE OPTIMIZATION: {score:.1f}/10")