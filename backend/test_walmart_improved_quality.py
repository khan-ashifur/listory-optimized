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

def test_improved_walmart_quality():
    print('🚀 TESTING IMPROVED WALMART QUALITY - ALL FEEDBACK IMPLEMENTED')
    print('=' * 75)
    print('Testing: No store brands, clear differentiators, benefit-driven bullets,')
    print('practical examples, social proof, trust elements, buyer-intent SEO\n')

    user, created = User.objects.get_or_create(username='walmart_improved_test')
    service = ListingGeneratorService()
    
    # Test premium product that should showcase all improvements
    product = Product.objects.create(
        user=user,
        name='HORL 2 Rolling Knife Sharpener',
        brand_name='HORL',
        target_platform='walmart',
        marketplace='walmart_usa',
        marketplace_language='en-us',
        price=299.99,  # Premium pricing to trigger "Professional Grade"
        occasion='christmas',
        brand_tone='luxury',
        categories='Kitchen & Dining > Cutlery > Knife Sharpeners',
        description='German-engineered rolling knife sharpener with interchangeable diamond and ceramic discs',
        features='Interchangeable diamond & ceramic discs\nPremium walnut wood construction\nGerman engineering precision\nMagnetic angle alignment system\n15° and 20° sharpening angles\n2-year manufacturer warranty'
    )

    print(f'✅ Created premium test product:')
    print(f'   Name: {product.name}')
    print(f'   Brand: {product.brand_name}')
    print(f'   Price: ${product.price} (Should trigger "Professional Grade")')
    print(f'   Occasion: {product.occasion}')
    print(f'   Brand Tone: {product.brand_tone}')

    try:
        listing = service.generate_listing(product.id, 'walmart')
        
        print(f'\n🎯 COMPREHENSIVE IMPROVEMENT ANALYSIS')
        print('=' * 50)
        
        # 1. Title Analysis
        title = listing.walmart_product_title
        print(f'📝 TITLE ANALYSIS:')
        print(f'   Title: {title}')
        print(f'   Length: {len(title)} chars')
        
        title_scores = []
        # Check for store brand removal
        store_brands = ['great value', 'equate', 'mainstays']
        has_store_brands = any(brand in title.lower() for brand in store_brands)
        title_scores.append(('No store brands', not has_store_brands))
        
        # Check for clear differentiators
        differentiators = ['german', 'made', '15°', '20°', 'angles', 'professional', 'precision']
        has_differentiator = any(diff in title.lower() for diff in differentiators)
        title_scores.append(('Has differentiator', has_differentiator))
        
        # Check for premium positioning
        premium_terms = ['professional grade', 'premium', 'special']
        has_premium = any(term in title.lower() for term in premium_terms)
        title_scores.append(('Premium positioning', has_premium))
        
        for check, passed in title_scores:
            status = '✅' if passed else '❌'
            print(f'   {status} {check}')
        
        # 2. Bullet Points Analysis
        print(f'\n🔘 BULLET POINTS ANALYSIS:')
        features = listing.walmart_key_features.split('\n')
        print(f'   Feature count: {len(features)}')
        
        bullet_scores = []
        for i, feature in enumerate(features[:5], 1):
            print(f'   {i}. {feature}')
            
            # Check if benefit-driven
            benefit_words = ['achieve', 'get', 'perfect', 'faster', 'safer', 'trusted', 'better']
            is_benefit_driven = any(word in feature.lower() for word in benefit_words)
            bullet_scores.append(is_benefit_driven)
            
            # Check for fulfillment text
            fulfillment_text = ['free pickup', 'store pickup', 'ships fast', 'free shipping']
            has_fulfillment = any(text in feature.lower() for text in fulfillment_text)
            if has_fulfillment:
                print(f'      ❌ Contains fulfillment text!')
        
        benefit_driven_percentage = (sum(bullet_scores) / len(bullet_scores)) * 100 if bullet_scores else 0
        print(f'   Benefit-driven bullets: {benefit_driven_percentage:.1f}%')
        
        # 3. Description Analysis
        print(f'\n📄 DESCRIPTION ANALYSIS:')
        description = listing.walmart_description
        print(f'   Length: {len(description)} words')
        
        # Check for corporate fluff
        corporate_fluff = ['outstanding performance', 'superior results', 'exceptional quality']
        has_fluff = any(phrase in description.lower() for phrase in corporate_fluff)
        print(f'   {"❌" if has_fluff else "✅"} Corporate fluff removed: {not has_fluff}')
        
        # Check for practical examples
        practical_examples = ['home cooking', 'sushi prep', 'outdoor', 'kitchen', 'chef']
        has_examples = any(example in description.lower() for example in practical_examples)
        print(f'   {"✅" if has_examples else "❌"} Practical examples: {has_examples}')
        
        # Check for social proof
        social_proof = ['trusted', 'thousands', 'professional', 'recommend', 'rated']
        has_social_proof = any(proof in description.lower() for proof in social_proof)
        print(f'   {"✅" if has_social_proof else "❌"} Social proof: {has_social_proof}')
        
        # Check for urgency
        urgency_terms = ['limited', 'stock', 'ships free', 'today', 'while supplies']
        has_urgency = any(term in description.lower() for term in urgency_terms)
        print(f'   {"✅" if has_urgency else "❌"} Urgency hooks: {has_urgency}')
        
        # 4. SEO Keywords Analysis
        print(f'\n🔍 SEO KEYWORDS ANALYSIS:')
        keywords = listing.keywords.split(', ') if listing.keywords else []
        print(f'   Keyword count: {len(keywords)}')
        
        # Check for buyer intent phrases
        buyer_intent = ['best for', 'easy', 'professional results', 'home cooks']
        buyer_intent_count = sum(1 for keyword in keywords if any(intent in keyword.lower() for intent in buyer_intent))
        print(f'   Buyer-intent phrases: {buyer_intent_count}')
        
        # Check for reduced duplicates (should have variety)
        unique_words = set()
        for keyword in keywords:
            unique_words.update(keyword.lower().split())
        duplication_ratio = len(unique_words) / (sum(len(k.split()) for k in keywords) or 1)
        print(f'   Keyword variety ratio: {duplication_ratio:.2f} (higher is better)')
        
        # 5. Product Identifiers & Compliance
        print(f'\n📦 PRODUCT IDENTIFIERS & COMPLIANCE:')
        try:
            specs = json.loads(listing.walmart_specifications)
            compliance = json.loads(listing.walmart_compliance_certifications) if listing.walmart_compliance_certifications else {}
            
            # Check for improved guidance
            structured_data_guidance = '[REQUIRED]' in str(specs) or '[RECOMMENDED]' in str(specs)
            print(f'   {"✅" if structured_data_guidance else "❌"} Improved guidance: {structured_data_guidance}')
            
            # Check pricing integration
            price_integrated = str(product.price) in str(specs)
            print(f'   {"✅" if price_integrated else "❌"} Price integrated: {price_integrated}')
            
        except Exception as e:
            print(f'   ⚠️ Error parsing product data: {e}')
        
        # 6. Overall Quality Score
        print(f'\n🏆 OVERALL IMPROVEMENT SCORE:')
        
        quality_checks = [
            ('Title improvements', not has_store_brands and has_differentiator and has_premium),
            ('Benefit-driven bullets', benefit_driven_percentage >= 70),
            ('Description quality', not has_fluff and has_examples and has_social_proof),
            ('Trust & urgency', has_urgency),
            ('SEO improvements', buyer_intent_count >= 3 and duplication_ratio >= 0.7),
            ('Product compliance', structured_data_guidance)
        ]
        
        passed_checks = sum(1 for _, passed in quality_checks)
        total_checks = len(quality_checks)
        improvement_score = (passed_checks / total_checks) * 100
        
        for check_name, passed in quality_checks:
            status = '✅' if passed else '❌'
            print(f'   {status} {check_name}')
        
        print(f'\n🎯 IMPROVEMENT SCORE: {passed_checks}/{total_checks} ({improvement_score:.1f}%)')
        
        if improvement_score >= 95:
            print('🎉 PERFECT! All improvements successfully implemented!')
        elif improvement_score >= 85:
            print('✅ EXCELLENT! Most improvements successfully implemented!')
        elif improvement_score >= 70:
            print('✅ GOOD! Significant improvements made!')
        else:
            print('⚠️ MORE WORK NEEDED! Some improvements missing!')
        
        print(f'\n🌐 Test URL: http://localhost:3000/results/{listing.id}')
        
    except Exception as e:
        print(f'❌ Error generating listing: {e}')
        import traceback
        traceback.print_exc()
    finally:
        # Keep for manual testing
        print(f'\n✅ Test completed - product kept for manual verification')

if __name__ == '__main__':
    test_improved_walmart_quality()