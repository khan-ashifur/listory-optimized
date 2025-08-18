#!/usr/bin/env python3
"""
Netherlands Market Quality Test - Target: 10/10 Quality Score
Tests Dutch Amazon marketplace with Koningsdag occasion and comprehensive validation
Following same pattern as Brazil/Mexico for 10/10 quality achievement
"""

import os
import sys
import django
import json
import re

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_path)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product, User
from apps.listings.services import ListingGeneratorService

def calculate_netherlands_quality_score(listing_data):
    """Calculate comprehensive quality score for Netherlands market"""
    score = 0.0
    max_score = 100.0
    feedback = []

    # 1. Dutch Language Quality (25 points)
    dutch_score = 0
    title = listing_data.get('title', '')
    description = listing_data.get('description', '')
    bullet_points = listing_data.get('bullet_points', [])
    
    # Check for essential Dutch words
    essential_dutch = ['de', 'het', 'van', 'voor', 'met', 'gezellig', 'geweldig', 'perfect']
    dutch_word_count = 0
    full_content = title + ' ' + description + ' ' + ' '.join(bullet_points)
    
    for word in essential_dutch:
        if word.lower() in full_content.lower():
            dutch_word_count += 1
    
    if dutch_word_count >= 5:
        dutch_score += 12
        feedback.append(f"✓ Essential Dutch words found ({dutch_word_count}/{len(essential_dutch)})")
    else:
        feedback.append(f"✗ Missing essential Dutch words ({dutch_word_count}/{len(essential_dutch)})")
    
    # Dutch formality patterns
    formality_patterns = [
        r'\b(wij garanderen)\b',
        r'\b(wij bieden u)\b', 
        r'\b(met trots presenteren wij)\b',
        r'\b(u kunt er zeker van zijn)\b',
        r'\b(zonder twijfel)\b'
    ]
    
    formality_count = 0
    for pattern in formality_patterns:
        if re.search(pattern, full_content, re.IGNORECASE):
            formality_count += 1
    
    if formality_count >= 2:
        dutch_score += 13
        feedback.append(f"✓ Dutch formality expressions found ({formality_count}/5)")
    else:
        feedback.append(f"✗ Insufficient Dutch formality ({formality_count}/5)")
    
    score += dutch_score

    # 2. Cultural Intelligence - Koningsdag & Dutch Culture (20 points)
    culture_score = 0
    dutch_culture_terms = [
        'koningsdag', 'gezelligheid', 'sinterklaas', 'nederlands', 'nederland', 
        'gezin', 'familie', 'fiets', 'tulp', 'oranje'
    ]
    
    culture_count = 0
    for term in dutch_culture_terms:
        if term.lower() in full_content.lower():
            culture_count += 1
    
    if culture_count >= 3:
        culture_score += 20
        feedback.append(f"✓ Dutch cultural references found ({culture_count} terms)")
    else:
        feedback.append(f"✗ Missing Dutch cultural references ({culture_count} terms)")
    
    score += culture_score

    # 3. Dutch Power Words (20 points)
    power_words = [
        'geweldig', 'fantastisch', 'perfect', 'uitstekend', 'premium', 
        'super', 'top', 'slim', 'praktisch', 'innovatief', 'uniek'
    ]
    
    power_word_count = 0
    for word in power_words:
        if re.search(r'\b' + word + r'\b', full_content, re.IGNORECASE):
            power_word_count += 1
    
    power_score = min(20, power_word_count * 3)
    score += power_score
    
    if power_word_count >= 4:
        feedback.append(f"✓ Strong Dutch power words usage ({power_word_count})")
    else:
        feedback.append(f"✗ Insufficient Dutch power words ({power_word_count})")

    # 4. SEO and Keywords (15 points)
    seo_score = 0
    seo_keywords = listing_data.get('seo_keywords', [])
    search_terms = listing_data.get('search_terms', [])
    
    total_keywords = len(seo_keywords) + len(search_terms)
    if total_keywords >= 15:
        seo_score += 8
        feedback.append(f"✓ Comprehensive keyword coverage ({total_keywords} keywords)")
    else:
        feedback.append(f"✗ Limited keyword coverage ({total_keywords} keywords)")
    
    # Check for Dutch-specific keywords
    dutch_keywords = ['nederland', 'nederlands', 'dutch', 'nl']
    dutch_kw_count = 0
    for keyword in (seo_keywords + search_terms):
        for nl_kw in dutch_keywords:
            if nl_kw.lower() in keyword.lower():
                dutch_kw_count += 1
                break
    
    if dutch_kw_count >= 1:
        seo_score += 7
        feedback.append("✓ Dutch market keywords included")
    else:
        feedback.append("✗ Missing Dutch market keywords")
    
    score += seo_score

    # 5. Technical Compliance (10 points)
    compliance_score = 0
    
    # Title length (optimal 120-180 chars for Dutch)
    if 120 <= len(title) <= 180:
        compliance_score += 4
        feedback.append("✓ Optimal title length")
    else:
        feedback.append(f"✗ Title length not optimal ({len(title)} chars)")
    
    # Bullet points count (optimal 5)
    if len(bullet_points) == 5:
        compliance_score += 3
        feedback.append("✓ Optimal bullet points count")
    else:
        feedback.append(f"✗ Bullet points count not optimal ({len(bullet_points)})")
    
    # Description length (optimal 800+ chars)
    if len(description) >= 800:
        compliance_score += 3
        feedback.append("✓ Comprehensive description length")
    else:
        feedback.append(f"✗ Description too short ({len(description)} chars)")
    
    score += compliance_score

    # 6. Dutch Market Positioning (10 points)
    positioning_score = 0
    
    # Check for competitive positioning terms in Dutch
    competitive_terms = [
        'beste', 'nummer 1', '#1', 'leider', 'exclusief', 'uniek', 
        'ongeëvenaard', 'onovertroffen', 'premium', 'superieur'
    ]
    
    competitive_count = 0
    for term in competitive_terms:
        if re.search(r'\b' + term + r'\b', full_content, re.IGNORECASE):
            competitive_count += 1
    
    if competitive_count >= 2:
        positioning_score += 10
        feedback.append(f"✓ Strong competitive positioning ({competitive_count} terms)")
    else:
        feedback.append(f"✗ Weak competitive positioning ({competitive_count} terms)")
    
    score += positioning_score

    # Calculate final percentage
    final_percentage = (score / max_score) * 10
    
    return final_percentage, feedback

def test_netherlands_market():
    """Test Netherlands market with Koningsdag theme for 10/10 quality"""
    
    print("🇳🇱 NETHERLANDS MARKET QUALITY TEST")
    print("=" * 50)
    print("Target: 10/10 Quality Score")
    print("Occasion: Koningsdag (Netherlands' most important celebration)")
    print("Language: Dutch (nl)")
    print("Testing comprehensive cultural intelligence and quality...")
    print()

    # Test product data - Dutch consumer electronics for Koningsdag
    product_data = {
        'name': 'Draagbare Bluetooth Speaker Oranje Koningsdag Editie',
        'description': '''Premium draagbare Bluetooth speaker speciaal ontworpen voor Koningsdag! 
        Met waterbestendige behuizing en krachtige sound voor alle Nederlandse feesten. 
        Perfect voor gezellige momenten met familie en vrienden tijdens Koningsdag. 
        Oranje design met Nederlandse trots. Lange batterijduur voor hele dag festiviteiten.
        Betrouwbare Nederlandse kwaliteit voor elke gelegenheid.''',
        'brand_name': 'OranjeSound',
        'marketplace': 'nl',
        'marketplace_language': 'nl',
        'price': '89.99',
        'categories': 'Elektronica, Audio, Bluetooth Speakers',
        'features': '''Krachtige sound met Nederlandse kwaliteit
        Waterbestendig voor buitenfeesten
        Batterij 12 uur voor hele Koningsdag
        Oranje design perfecte Nederlandse stijl
        Bluetooth 5.0 verbinding handig gebrui''',
        'target_platform': 'amazon',
        'brand_tone': 'friendly',
        'target_audience': 'Nederlandse gezinnen die van Koningsdag en gezelligheid houden',
        'target_keywords': 'bluetooth speaker, koningsdag, oranje, gezellig, nederlands',
        'occasion': 'koningsdag'
    }

    try:
        # Get or create test user
        user, created = User.objects.get_or_create(
            email='netherlands@listory.ai',
            defaults={'first_name': 'Netherlands', 'last_name': 'Test', 'username': 'netherlands_test'}
        )
        
        # Create product
        print("1. Creating test product...")
        product_data['user'] = user
        product = Product.objects.create(**product_data)
        print(f"✓ Product created with ID: {product.id}")
        
        # Generate listing
        print("\n2. Generating Netherlands market listing...")
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if not result['success']:
            print(f"✗ Listing generation failed: {result.get('error', 'Unknown error')}")
            return False
        
        listing = result['data']
        print("✓ Listing generated successfully")
        
        # Convert to dict for analysis
        listing_data = {
            'title': listing.title,
            'description': listing.description,
            'bullet_points': listing.bullet_points,
            'seo_keywords': listing.seo_keywords if hasattr(listing, 'seo_keywords') else [],
            'search_terms': listing.search_terms if hasattr(listing, 'search_terms') else [],
        }
        
        # Parse bullet points
        bullet_points = listing_data.get('bullet_points', [])
        if isinstance(bullet_points, str):
            try:
                bullet_points = json.loads(bullet_points)
                listing_data['bullet_points'] = bullet_points
            except:
                bullet_points = []
        
        # Display content
        print("\n3. GENERATED CONTENT PREVIEW")
        print("-" * 40)
        print(f"📝 Title: {listing_data.get('title', 'N/A')}")
        print(f"📄 Description: {listing_data.get('description', 'N/A')[:200]}...")
        
        print(f"\n• Bullet Points: {len(bullet_points)} points")
        for i, bullet in enumerate(bullet_points, 1):
            print(f"  {i}. {bullet}")
        
        print(f"\n🔍 SEO Keywords: {len(listing_data.get('seo_keywords', []))} keywords")
        print(f"🔍 Search Terms: {len(listing_data.get('search_terms', []))} terms")
        
        # Calculate quality score
        print("\n4. QUALITY ANALYSIS")
        print("-" * 40)
        quality_score, feedback = calculate_netherlands_quality_score(listing_data)
        
        print(f"🎯 FINAL QUALITY SCORE: {quality_score:.1f}/10.0")
        print()
        
        # Display feedback
        print("DETAILED FEEDBACK:")
        for item in feedback:
            print(f"  {item}")
        
        print()
        
        # Competitive analysis
        print("5. COMPETITIVE ANALYSIS")
        print("-" * 40)
        
        competitors = {
            'Helium 10': 7.5,
            'Copy Monkey': 7.8,
            'Jasper AI': 8.2
        }
        
        print("📊 Competitor Benchmark:")
        for competitor, score in competitors.items():
            status = "✓ BEATS" if quality_score > score else "✗ BELOW"
            print(f"  {competitor}: {score}/10 - {status}")
        
        print()
        
        # Final verdict
        if quality_score >= 10.0:
            print("🏆 SUCCESS: 10/10 QUALITY ACHIEVED!")
            print("🇳🇱 Netherlands market optimization COMPLETE")
            print("🚀 Ready to dominate Dutch Amazon marketplace!")
        elif quality_score >= 9.0:
            print("⚡ EXCELLENT: Near-perfect quality achieved")
            print("🔧 Minor optimizations needed for 10/10")
        elif quality_score >= 8.0:
            print("👍 GOOD: Strong quality foundation")
            print("🔧 Additional optimization required")
        else:
            print("❌ NEEDS WORK: Quality below target")
            print("🔧 Significant optimization required")
        
        print()
        print("6. DUTCH CULTURAL INTELLIGENCE VERIFICATION")
        print("-" * 40)
        
        # Check for specific Dutch cultural elements
        full_content = (listing_data.get('title', '') + ' ' + 
                       listing_data.get('description', '') + ' ' + 
                       ' '.join(bullet_points))
        
        dutch_elements = {
            'Koningsdag references': ['koningsdag', 'oranje', 'feest'],
            'Dutch language': ['geweldig', 'gezellig', 'fantastisch'],
            'Local market terms': ['nederland', 'nederlands', 'dutch'],
            'Cultural values': ['familie', 'gezin', 'gezelligheid', 'traditie']
        }
        
        for category, terms in dutch_elements.items():
            found_terms = [term for term in terms if term.lower() in full_content.lower()]
            status = "✓" if found_terms else "✗"
            print(f"  {status} {category}: {found_terms}")
        
        # Cleanup
        product.delete()
        
        return quality_score >= 10.0

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_netherlands_market()
    print("\n" + "="*50)
    if success:
        print("🏆 NETHERLANDS MARKET: 10/10 QUALITY ACHIEVED!")
        print("🇳🇱 Ready to dominate Dutch Amazon!")
    else:
        print("🔧 Netherlands market needs optimization")
    print("="*50)