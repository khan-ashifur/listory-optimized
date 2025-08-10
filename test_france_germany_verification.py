"""
Verify France and Germany Language Generation
Test that France generates French and Germany generates German separately
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

def test_language_verification():
    """Test that France generates French and Germany generates German"""
    print("🌍 LANGUAGE VERIFICATION TEST")
    print("🎯 Verify France = French, Germany = German (no cross-contamination)")
    print("=" * 70)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        results = []
        
        # Test 1: France should generate French
        print(f"\n🇫🇷 TESTING FRANCE - SHOULD BE FRENCH")
        print("=" * 50)
        
        product.marketplace = "fr"
        product.marketplace_language = "fr"
        product.brand_tone = "luxury"
        product.occasion = "none"
        product.save()
        
        print("🔄 Generating France listing...")
        service.generate_listing(product.id, 'amazon')
        time.sleep(10)
        
        listing_fr = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing_fr and listing_fr.status == 'completed':
            title_fr = listing_fr.title or ""
            bullets_fr = listing_fr.bullet_points or ""
            
            print(f"✅ France generated successfully!")
            print(f"📌 FRENCH TITLE: {title_fr[:80]}...")
            print(f"📍 FIRST BULLET: {bullets_fr.split(chr(10))[0][:80]}..." if bullets_fr else "No bullets")
            
            # Check if it's actually French
            french_indicators = ['français', 'qualité', 'élégant', 'avec', 'pour', 'raffinement', 'excellence']
            french_accents = ['é', 'è', 'à', 'ç', 'ù', 'â', 'ê', 'î', 'ô', 'û']
            
            total_text_fr = title_fr + bullets_fr
            french_words_found = sum(word in total_text_fr.lower() for word in french_indicators)
            french_accents_found = sum(total_text_fr.count(char) for char in french_accents)
            
            print(f"\n🔍 FRENCH VERIFICATION:")
            print(f"   French words found: {french_words_found}/7 ({'✅' if french_words_found >= 3 else '❌'})")
            print(f"   French accents found: {french_accents_found} ({'✅' if french_accents_found >= 5 else '❌'})")
            
            is_french = french_words_found >= 3 and french_accents_found >= 5
            print(f"   Language confirmed: {'✅ FRENCH' if is_french else '❌ NOT FRENCH'}")
            
            results.append({
                "market": "France",
                "expected": "French", 
                "is_correct": is_french,
                "words": french_words_found,
                "accents": french_accents_found
            })
        else:
            print("❌ France generation failed")
            results.append({
                "market": "France",
                "expected": "French",
                "is_correct": False,
                "words": 0,
                "accents": 0
            })
        
        # Test 2: Germany should generate German 
        print(f"\n🇩🇪 TESTING GERMANY - SHOULD BE GERMAN")
        print("=" * 50)
        
        product.marketplace = "de"
        product.marketplace_language = "de"
        product.brand_tone = "professional"
        product.occasion = "none"
        product.save()
        
        print("🔄 Generating Germany listing...")
        service.generate_listing(product.id, 'amazon')
        time.sleep(10)
        
        listing_de = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing_de and listing_de.status == 'completed':
            title_de = listing_de.title or ""
            bullets_de = listing_de.bullet_points or ""
            
            print(f"✅ Germany generated successfully!")
            print(f"📌 GERMAN TITLE: {title_de[:80]}...")
            print(f"📍 FIRST BULLET: {bullets_de.split(chr(10))[0][:80]}..." if bullets_de else "No bullets")
            
            # Check if it's actually German
            german_indicators = ['für', 'mit', 'und', 'der', 'die', 'das', 'wie', 'ein', 'profi']
            german_umlauts = ['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü']
            
            total_text_de = title_de + bullets_de
            german_words_found = sum(word in total_text_de.lower() for word in german_indicators)
            german_umlauts_found = sum(total_text_de.count(char) for char in german_umlauts)
            
            print(f"\n🔍 GERMAN VERIFICATION:")
            print(f"   German words found: {german_words_found}/9 ({'✅' if german_words_found >= 4 else '❌'})")
            print(f"   German umlauts found: {german_umlauts_found} ({'✅' if german_umlauts_found >= 5 else '❌'})")
            
            is_german = german_words_found >= 4 and german_umlauts_found >= 5
            print(f"   Language confirmed: {'✅ GERMAN' if is_german else '❌ NOT GERMAN'}")
            
            results.append({
                "market": "Germany",
                "expected": "German",
                "is_correct": is_german,
                "words": german_words_found,
                "umlauts": german_umlauts_found
            })
        else:
            print("❌ Germany generation failed")
            results.append({
                "market": "Germany", 
                "expected": "German",
                "is_correct": False,
                "words": 0,
                "umlauts": 0
            })
        
        # Final verification
        print(f"\n🏆 LANGUAGE VERIFICATION RESULTS")
        print("=" * 50)
        
        all_correct = True
        for result in results:
            market = result["market"]
            expected = result["expected"]
            correct = result["is_correct"]
            
            print(f"   {market}: {'✅ CORRECT' if correct else '❌ INCORRECT'} ({expected} language)")
            if not correct:
                all_correct = False
        
        print(f"\n🎯 FINAL VERIFICATION:")
        if all_correct and len(results) == 2:
            print(f"✅ SUCCESS: Both markets generate correct languages!")
            print(f"🇫🇷 France generates French ✅")
            print(f"🇩🇪 Germany generates German ✅") 
            print(f"🚀 No cross-contamination - languages work independently!")
        else:
            print(f"❌ ISSUE: Language generation has problems!")
            print(f"🔧 Need to fix language separation")
        
        return all_correct, results
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False, []

if __name__ == "__main__":
    success, results = test_language_verification()
    if success:
        print(f"\n🎉 VERIFICATION PASSED: Both France and Germany work correctly!")
    else:
        print(f"\n⚠️ VERIFICATION FAILED: Language issues detected!")