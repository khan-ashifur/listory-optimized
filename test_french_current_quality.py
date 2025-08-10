"""
Test Current French Market Quality
Analyze existing French generation to identify optimization opportunities
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

def analyze_french_quality():
    """Analyze current French market generation quality"""
    print("🇫🇷 FRENCH MARKET QUALITY ANALYSIS")
    print("🎯 Current State Assessment for 10/10 Optimization")
    print("=" * 70)
    
    try:
        service = ListingGeneratorService()
        
        # Find test product
        product = Product.objects.filter(name__icontains="misting fan").first()
        if not product:
            print("❌ No test product found")
            return
        
        # Configure for French market
        product.marketplace = "fr"
        product.marketplace_language = "fr"
        product.brand_tone = "luxury"  # French market loves sophistication
        product.occasion = "Valentine's Day"
        product.save()
        
        print(f"📦 Product: {product.name}")
        print(f"🇫🇷 Market: France")
        print(f"🎨 Brand Tone: Luxury")
        print(f"💝 Occasion: Valentine's Day")
        
        print("\n🔄 Generating current French listing...")
        
        # Generate listing
        service.generate_listing(product.id, 'amazon')
        
        # Wait for generation
        print("⏳ Analyzing current quality...")
        time.sleep(12)
        
        # Get the latest listing
        listing = GeneratedListing.objects.filter(
            product=product,
            platform='amazon'
        ).order_by('-created_at').first()
        
        if listing and listing.status == 'completed':
            print("✅ Generation completed!")
            
            # Analyze content
            title = listing.title or ""
            bullets = listing.bullet_points or ""
            description = listing.long_description or ""
            total_text = title + bullets + description
            
            print(f"\n🔍 CURRENT FRENCH QUALITY ANALYSIS:")
            print("=" * 50)
            
            # 1. French Language Quality
            print(f"\n1️⃣ FRENCH LANGUAGE QUALITY:")
            french_chars = ['é', 'è', 'à', 'ç', 'ù', 'â', 'ê', 'î', 'ô', 'û', 'ë', 'ï', 'ÿ', 'É', 'È', 'À', 'Ç']
            french_accent_count = sum(total_text.count(char) for char in french_chars)
            print(f"   French accents found: {french_accent_count} ({'✅' if french_accent_count >= 10 else '❌'})")
            
            # Check for French words
            french_words = ['qualité', 'élégant', 'raffinement', 'sophistiqué', 'excellence', 'français', 'avec', 'très', 'être']
            french_words_found = sum(word in total_text.lower() for word in french_words)
            print(f"   French words detected: {french_words_found}/9 ({'✅' if french_words_found >= 6 else '❌'})")
            
            # 2. Title Analysis
            print(f"\n2️⃣ TITLE ANALYSIS:")
            print(f"   📌 TITLE: {title}")
            print(f"   Length: {len(title)} chars ({'✅' if 120 <= len(title) <= 200 else '❌'})")
            has_luxury_words = any(word in title.lower() for word in ['premium', 'luxury', 'élégant', 'raffinement', 'sophistiqué'])
            print(f"   Luxury tone: {'✅' if has_luxury_words else '❌'}")
            
            # 3. Bullet Structure Analysis
            print(f"\n3️⃣ BULLET STRUCTURE ANALYSIS:")
            bullet_list = bullets.split('\n')
            bullet_list = [b.strip() for b in bullet_list if b.strip()]
            
            has_labels = []
            for i, bullet in enumerate(bullet_list[:5], 1):
                if bullet:
                    print(f"   Bullet {i}: {bullet[:80]}...")
                    has_colon = ":" in bullet[:40]
                    has_labels.append(has_colon)
                    print(f"      Has label: {'✅' if has_colon else '❌'}")
            
            label_percentage = (sum(has_labels) / len(has_labels) * 100) if has_labels else 0
            print(f"   Label percentage: {label_percentage:.1f}%")
            
            # 4. French Cultural Elements
            print(f"\n4️⃣ FRENCH CULTURAL ELEMENTS:")
            cultural_words = ['français', 'élégance', 'raffinement', 'sophistication', 'qualité française', 'savoir-faire']
            cultural_found = sum(word in total_text.lower() for word in cultural_words)
            print(f"   Cultural elements: {cultural_found}/6 ({'✅' if cultural_found >= 3 else '❌'})")
            
            # 5. Valentine's Day Integration
            print(f"\n5️⃣ VALENTINE'S DAY INTEGRATION:")
            valentine_words = ['saint-valentin', 'valentin', 'amour', 'romantique', 'cadeau', 'offrir']
            valentine_found = sum(word in total_text.lower() for word in valentine_words)
            print(f"   Valentine elements: {valentine_found}/6 ({'✅' if valentine_found >= 2 else '❌'})")
            
            # 6. Overall Quality Score
            print(f"\n6️⃣ OVERALL QUALITY ASSESSMENT:")
            criteria = {
                "French language accuracy": french_accent_count >= 10 and french_words_found >= 6,
                "Title optimization": 120 <= len(title) <= 200 and has_luxury_words,
                "Bullet labels present": label_percentage >= 60,
                "Cultural adaptation": cultural_found >= 3,
                "Occasion integration": valentine_found >= 2,
                "Content length": len(total_text) >= 1500
            }
            
            score = sum(criteria.values())
            total_criteria = len(criteria)
            
            print(f"📋 QUALITY CRITERIA:")
            for criterion, passed in criteria.items():
                print(f"   {criterion}: {'✅ PASS' if passed else '❌ NEEDS WORK'}")
            
            current_score = (score / total_criteria) * 10
            print(f"\n🏆 CURRENT SCORE: {score}/{total_criteria} ({current_score:.1f}/10)")
            
            if current_score >= 9:
                print("🎉 EXCELLENT: French market nearly perfect!")
            elif current_score >= 7:
                print("🥈 GOOD: French market needs minor improvements")
            elif current_score >= 5:
                print("🥉 MODERATE: French market needs significant optimization")
            else:
                print("⚠️ CRITICAL: French market needs complete overhaul")
            
            print(f"\n🎯 OPTIMIZATION PRIORITIES:")
            if not criteria["French language accuracy"]:
                print(f"   🔧 HIGH: Fix French accent usage and vocabulary")
            if not criteria["Bullet labels present"]:
                print(f"   🔧 HIGH: Add French brand tone bullet labels")
            if not criteria["Cultural adaptation"]:
                print(f"   🔧 MEDIUM: Enhance French cultural elements")
            if not criteria["Occasion integration"]:
                print(f"   🔧 MEDIUM: Improve Valentine's Day messaging")
            
            return current_score, criteria
            
        else:
            print(f"❌ Generation failed: {listing.status if listing else 'Not found'}")
            return 0, {}
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 0, {}

if __name__ == "__main__":
    score, analysis = analyze_french_quality()
    print(f"\n🚀 READY TO OPTIMIZE FRANCE TO 10/10 QUALITY!")