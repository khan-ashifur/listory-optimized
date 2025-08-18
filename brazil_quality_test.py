#!/usr/bin/env python3
"""
Brazil Market Quality Test - Target: 10/10 Quality Score
Tests Brazilian Amazon marketplace with Carnaval occasion and comprehensive validation
Following exact same pattern as Mexico test for consistency
"""

import os
import sys
import django
import json
import re
from datetime import datetime

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_path)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product, User
from apps.listings.services import ListingGeneratorService

def calculate_quality_score(listing_data):
    """Calculate comprehensive quality score for Brazil market"""
    score = 0.0
    max_score = 100.0
    feedback = []

    # 1. Portuguese Language Quality (20 points)
    portuguese_score = 0
    title = listing_data.get('title', '')
    description = listing_data.get('description', '')
    bullet_points = listing_data.get('bullet_points', [])
    
    # Check for Brazilian Portuguese accent marks (á, â, ã, é, ê, í, ó, ô, õ, ú, ç)
    portuguese_chars = re.findall(r'[áâãéêíóôõúç]', title + ' ' + description + ' ' + ' '.join(bullet_points))
    if len(portuguese_chars) >= 3:
        portuguese_score += 8
        feedback.append("✓ Proper Brazilian Portuguese characters found")
    else:
        feedback.append("✗ Missing Brazilian Portuguese accent marks")
    
    # Brazilian Portuguese formality patterns
    formal_patterns = [
        r'\b(nosso|nossa)\b',  # "our" in Brazilian Portuguese
        r'\b(você|vocês)\b',   # "you" (Brazilian style vs European tu)
        r'\b(garantimos|oferecemos)\b',  # "we guarantee/offer"
        r'\b(perfeito|incrível|extraordinário)\b',  # quality adjectives
        r'\b(Brazilian|brasileiro|brasileira)\b'  # Brazilian references
    ]
    
    formal_count = 0
    for pattern in formal_patterns:
        if re.search(pattern, title + ' ' + description + ' ' + ' '.join(bullet_points), re.IGNORECASE):
            formal_count += 1
    
    if formal_count >= 3:
        portuguese_score += 12
        feedback.append(f"✓ Brazilian Portuguese formality patterns found ({formal_count}/5)")
    else:
        feedback.append(f"✗ Insufficient Brazilian formality patterns ({formal_count}/5)")
    
    score += portuguese_score

    # 2. Cultural Intelligence - Carnaval (15 points)
    carnaval_score = 0
    carnaval_terms = ['carnaval', 'festa', 'celebração', 'alegria', 'diversão', 'bloco', 'fantasia']
    
    carnaval_count = 0
    for term in carnaval_terms:
        if re.search(term, title + ' ' + description + ' ' + ' '.join(bullet_points), re.IGNORECASE):
            carnaval_count += 1
    
    if carnaval_count >= 2:
        carnaval_score += 15
        feedback.append(f"✓ Carnaval cultural references found ({carnaval_count} terms)")
    else:
        feedback.append(f"✗ Missing Carnaval cultural references ({carnaval_count} terms)")
    
    score += carnaval_score

    # 3. Brazilian Power Words (15 points)
    power_words = [
        'incrível', 'fantástico', 'extraordinário', 'revolucionário', 'perfeito',
        'premium', 'exclusivo', 'garantido', 'demais', 'top', 'super'
    ]
    
    power_word_count = 0
    for word in power_words:
        if re.search(r'\b' + word + r'\b', title + ' ' + description + ' ' + ' '.join(bullet_points), re.IGNORECASE):
            power_word_count += 1
    
    power_score = min(15, power_word_count * 2)
    score += power_score
    
    if power_word_count >= 5:
        feedback.append(f"✓ Strong Brazilian power words usage ({power_word_count})")
    else:
        feedback.append(f"✗ Insufficient Brazilian power words ({power_word_count})")

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
    
    # Check for Brazilian-specific keywords
    brazilian_keywords = ['brasil', 'brasileiro', 'brasileira', 'BR']
    brazilian_kw_count = 0
    for keyword in (seo_keywords + search_terms):
        for br_kw in brazilian_keywords:
            if br_kw.lower() in keyword.lower():
                brazilian_kw_count += 1
                break
    
    if brazilian_kw_count >= 2:
        seo_score += 7
        feedback.append("✓ Brazilian market keywords included")
    else:
        feedback.append("✗ Missing Brazilian market keywords")
    
    score += seo_score

    # 5. A+ Content Quality (15 points)
    aplus_score = 0
    aplus_sections = [
        'aplus_headline', 'aplus_key_features', 'aplus_about_brand',
        'aplus_ingredients', 'aplus_directions', 'aplus_safety_warning',
        'aplus_comparison_chart', 'aplus_qa_section'
    ]
    
    filled_sections = 0
    for section in aplus_sections:
        content = listing_data.get(section, '')
        if content and len(content.strip()) > 20:
            filled_sections += 1
    
    aplus_score = min(15, filled_sections * 2)
    score += aplus_score
    
    if filled_sections >= 6:
        feedback.append(f"✓ Comprehensive A+ content ({filled_sections}/8 sections)")
    else:
        feedback.append(f"✗ Limited A+ content ({filled_sections}/8 sections)")

    # 6. Market Positioning vs Competitors (10 points)
    positioning_score = 0
    
    # Check for competitive positioning terms
    competitive_terms = [
        'melhor que', 'superior', 'número 1', '#1', 'líder', 'exclusivo',
        'único', 'incomparável', 'imbatível', 'premium'
    ]
    
    competitive_count = 0
    for term in competitive_terms:
        if re.search(term, title + ' ' + description + ' ' + ' '.join(bullet_points), re.IGNORECASE):
            competitive_count += 1
    
    if competitive_count >= 3:
        positioning_score += 10
        feedback.append(f"✓ Strong competitive positioning ({competitive_count} terms)")
    else:
        feedback.append(f"✗ Weak competitive positioning ({competitive_count} terms)")
    
    score += positioning_score

    # 7. Technical Compliance (10 points)
    compliance_score = 0
    
    # Title length (optimal 150-200 chars for Brazil)
    if 150 <= len(title) <= 200:
        compliance_score += 3
        feedback.append("✓ Optimal title length")
    else:
        feedback.append(f"✗ Title length not optimal ({len(title)} chars)")
    
    # Bullet points count (optimal 5)
    if len(bullet_points) == 5:
        compliance_score += 3
        feedback.append("✓ Optimal bullet points count")
    else:
        feedback.append(f"✗ Bullet points count not optimal ({len(bullet_points)})")
    
    # Description length (optimal 1000+ chars)
    if len(description) >= 1000:
        compliance_score += 4
        feedback.append("✓ Comprehensive description length")
    else:
        feedback.append(f"✗ Description too short ({len(description)} chars)")
    
    score += compliance_score

    # Calculate final percentage
    final_percentage = (score / max_score) * 10
    
    return final_percentage, feedback

def test_brazil_market():
    """Test Brazil market with Carnaval theme for 10/10 quality"""
    
    print("🇧🇷 BRAZIL MARKET QUALITY TEST")
    print("=" * 50)
    print("Target: 10/10 Quality Score")
    print("Occasion: Carnaval (Brazil's most important celebration)")
    print("Language: Brazilian Portuguese (pt-br)")
    print("Testing comprehensive cultural intelligence and quality...")
    print()

    # Test product data - Brazilian consumer electronics for Carnaval
    product_data = {
        'name': 'Alto-falante Bluetooth Portátil Resistente à Água Premium',
        'description': '''Alto-falante Bluetooth portátil de alta qualidade, perfeito para suas festas de Carnaval! 
        Com design resistente à água IPX7 e som cristalino de 360°, este incrível alto-falante vai transformar 
        qualquer bloco de Carnaval em uma experiência inesquecível. Som potente de 20W com graves profundos 
        e agudos nítidos. Bateria de longa duração para até 12 horas de música contínua. Conectividade Bluetooth 5.0 
        com alcance de até 30 metros. Design moderno e cores vibrantes perfeitas para o Carnaval brasileiro.''',
        'brand_name': 'SomBrasil',
        'marketplace': 'br',
        'marketplace_language': 'pt-br',
        'price': '149.99',
        'categories': 'Eletrônicos, Áudio, Alto-falantes Bluetooth',
        'features': '''Som cristalino 360° com tecnologia premium
        Resistente à água IPX7 - perfeito para Carnaval
        Bateria 12 horas de duração contínua
        Bluetooth 5.0 com alcance 30 metros
        Design brasileiro com cores vibrantes''',
        'target_platform': 'amazon',
        'brand_tone': 'festive',
        'target_audience': 'Brasileiros que amam festas e Carnaval, jovens adultos 18-35 anos',
        'target_keywords': 'alto-falante bluetooth, som carnaval, resistente água, música festa',
        'occasion': 'carnaval'
    }

    try:
        # Get or create test user
        user, created = User.objects.get_or_create(
            email='test@listory.ai',
            defaults={'first_name': 'Test', 'last_name': 'User'}
        )
        
        # Create product
        print("1. Creating test product...")
        product_data['user'] = user
        product = Product.objects.create(**product_data)
        print(f"✓ Product created with ID: {product.id}")
        
        # Generate listing
        print("\n2. Generating Brazil market listing...")
        service = ListingGeneratorService()
        result = service.generate_listing(product.id, 'amazon')
        
        if not result['success']:
            print(f"✗ Listing generation failed: {result.get('error', 'Unknown error')}")
            return False
        
        listing_obj = result['data']
        print("✓ Listing generated successfully")
        
        # Convert to dict for analysis
        listing_data = {
            'title': listing_obj.title,
            'description': listing_obj.description,
            'bullet_points': listing_obj.bullet_points,
            'seo_keywords': listing_obj.seo_keywords if hasattr(listing_obj, 'seo_keywords') else [],
            'search_terms': listing_obj.search_terms if hasattr(listing_obj, 'search_terms') else [],
            'aplus_headline': listing_obj.aplus_headline if hasattr(listing_obj, 'aplus_headline') else '',
            'aplus_key_features': listing_obj.aplus_key_features if hasattr(listing_obj, 'aplus_key_features') else '',
            'aplus_about_brand': listing_obj.aplus_about_brand if hasattr(listing_obj, 'aplus_about_brand') else '',
            'aplus_ingredients': listing_obj.aplus_ingredients if hasattr(listing_obj, 'aplus_ingredients') else '',
            'aplus_directions': listing_obj.aplus_directions if hasattr(listing_obj, 'aplus_directions') else '',
            'aplus_safety_warning': listing_obj.aplus_safety_warning if hasattr(listing_obj, 'aplus_safety_warning') else '',
            'aplus_comparison_chart': listing_obj.aplus_comparison_chart if hasattr(listing_obj, 'aplus_comparison_chart') else '',
            'aplus_qa_section': listing_obj.aplus_qa_section if hasattr(listing_obj, 'aplus_qa_section') else '',
        }
        
        # Display key content
        print("\n3. GENERATED CONTENT PREVIEW")
        print("-" * 40)
        print(f"📝 Title: {listing_data.get('title', 'N/A')}")
        print(f"📄 Description: {listing_data.get('description', 'N/A')[:300]}...")
        
        bullet_points = listing_data.get('bullet_points', [])
        if isinstance(bullet_points, str):
            try:
                bullet_points = json.loads(bullet_points)
            except:
                bullet_points = []
        
        print(f"\n• Bullet Points: {len(bullet_points)} points")
        for i, bullet in enumerate(bullet_points, 1):
            print(f"  {i}. {bullet}")
        
        print(f"\n🔍 SEO Keywords: {len(listing_data.get('seo_keywords', []))} keywords")
        print(f"🔍 Search Terms: {len(listing_data.get('search_terms', []))} terms")
        
        # Calculate quality score
        print("\n4. QUALITY ANALYSIS")
        print("-" * 40)
        quality_score, feedback = calculate_quality_score(listing_data)
        
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
            print("🎉 Brazil market optimization COMPLETE")
            print("🚀 Ready to dominate Brazilian Amazon marketplace!")
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
        print("6. CULTURAL INTELLIGENCE VERIFICATION")
        print("-" * 40)
        
        # Check for specific Brazilian cultural elements
        full_content = (listing_data.get('title', '') + ' ' + 
                       listing_data.get('description', '') + ' ' + 
                       ' '.join(bullet_points))
        
        brazilian_elements = {
            'Carnaval references': ['carnaval', 'festa', 'bloco'],
            'Brazilian Portuguese': ['você', 'nosso', 'demais'],
            'Local market terms': ['brasil', 'brasileiro'],
            'Cultural values': ['alegria', 'diversão', 'família']
        }
        
        for category, terms in brazilian_elements.items():
            found_terms = [term for term in terms if term in full_content.lower()]
            status = "✓" if found_terms else "✗"
            print(f"  {status} {category}: {found_terms}")
        
        # Cleanup
        product.delete()
        
        return quality_score >= 10.0

    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_brazil_market()
    print("\n" + "="*50)
    if success:
        print("🏆 BRAZIL MARKET: 10/10 QUALITY ACHIEVED!")
        print("🇧🇷 Ready to dominate Brazilian Amazon!")
    else:
        print("🔧 Brazil market needs optimization")
    print("="*50)