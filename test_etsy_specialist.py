#!/usr/bin/env python3
"""
🎨 TOP E-COMMERCE SPECIALIST: ETSY LISTING QUALITY EVALUATION
Testing world-class Etsy generation system for emotional impact and conversion optimization
"""

import os, sys, django
import json

# Setup Django
sys.path.insert(0, 'backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

def main():
    print('🎨 TOP E-COMMERCE SPECIALIST: TESTING WORLD-CLASS ETSY GENERATION')
    print('=' * 70)

    user, created = User.objects.get_or_create(username='etsy_quality_specialist')

    # Test with high-emotional-potential product
    Product.objects.filter(user=user, name__icontains='Personalized Birth Flower').delete()

    product = Product.objects.create(
        user=user,
        name='Personalized Birth Flower Necklace',
        brand_name='SoulCrafted',
        target_platform='etsy',
        marketplace='etsy',
        marketplace_language='en',
        price=68.00,
        description='Delicate handmade necklace featuring your birth flower in sterling silver',
        categories='Jewelry > Necklaces > Pendant Necklaces',
        features='Sterling silver chain\nHand-engraved birth flower pendant\nPersonalized with birthdate\nGift box included\n18-inch adjustable chain\nHypoallergenic materials',
        brand_tone='handmade_artisan',
        occasion='mothers_day'
    )

    print('✅ Premium Test Product Created:')
    print(f'   Category: Personalized Jewelry (HIGH emotional potential)')
    print(f'   Price: ${product.price} (Premium handmade range)')
    print(f'   Brand Tone: {product.brand_tone}')
    print(f'   Occasion: {product.occasion}')

    print('\n🚀 GENERATING WORLD-CLASS ETSY LISTING...')
    service = ListingGeneratorService()
    listing = service.generate_listing(product.id, 'etsy')

    print('\n📊 GENERATION RESULTS:')
    print(f'   Status: {listing.status}')
    print(f'   ID: {listing.id}')

    if listing.status == 'completed':
        analyze_listing_quality(listing)
    else:
        print('❌ GENERATION FAILED')
        if hasattr(listing, 'error_message'):
            print(f'   Error: {listing.error_message}')

def analyze_listing_quality(listing):
    """Comprehensive quality analysis by top e-commerce specialist"""
    
    print('\n🎭 EMOTIONAL IMPACT ANALYSIS:')
    print('=' * 50)
    
    # Analyze title
    title = listing.etsy_title
    print(f'📝 TITLE ({len(title)}/140 chars):')
    print(f'   {title}')
    
    # Check emotional triggers in title
    emotional_triggers = [
        'personalized', 'custom', 'handmade', 'artisan', 'crafted', 'birth', 
        'flower', 'necklace', 'sterling', 'silver', 'gift', 'mom', 'mother'
    ]
    
    title_triggers = [word for word in emotional_triggers if word.lower() in title.lower()]
    print(f'   Emotional keywords found: {title_triggers} ({len(title_triggers)} total)')
    
    # Check if starts with primary keyword
    primary_keywords = ['birth flower', 'personalized', 'custom', 'handmade']
    starts_with_keyword = any(title.lower().startswith(kw) for kw in primary_keywords)
    print(f'   Starts with primary keyword: {"✅ YES" if starts_with_keyword else "❌ NO"}')
    
    # Analyze description 
    description = listing.etsy_description
    print(f'\n📄 DESCRIPTION ({len(description)} chars):')
    print(f'   Preview: {description[:300]}...')
    
    # Check for storytelling sections
    story_sections = ['story', 'inspiration', 'behind', 'created', 'crafted']
    story_count = sum(1 for section in story_sections if section.lower() in description.lower())
    print(f'   Storytelling elements: {story_count} found')
    
    # Check for sensory/emotional words
    sensory_words = ['delicate', 'shimmer', 'sparkle', 'glow', 'soft', 'smooth', 'elegant']
    emotion_words = ['love', 'heart', 'memory', 'meaningful', 'special', 'treasure', 'cherish']
    
    sensory_count = sum(1 for word in sensory_words if word.lower() in description.lower())
    emotion_count = sum(1 for word in emotion_words if word.lower() in description.lower())
    
    print(f'   Sensory words: {sensory_count} found')
    print(f'   Emotional words: {emotion_count} found')
    
    # Analyze tags
    if listing.etsy_tags:
        try:
            tags = json.loads(listing.etsy_tags)
            print(f'\n🏷️ TAGS ({len(tags)}/13):')
            print(f'   Tags: {tags}')
            
            # Check tag emotional impact
            emotional_tags = [tag for tag in tags if any(emo in tag.lower() for emo in ['personalized', 'custom', 'gift', 'mom', 'birth'])]
            print(f'   Emotional tags: {len(emotional_tags)} found')
        except:
            print(f'\n🏷️ TAGS: Format error')
    
    # Check quality scores
    print(f'\n📊 AI-CALCULATED QUALITY SCORES:')
    print(f'   Emotion Score: {listing.emotion_score:.1f}/10')
    print(f'   Conversion Score: {listing.conversion_score:.1f}/10')
    print(f'   Trust Score: {listing.trust_score:.1f}/10')
    print(f'   Overall Quality: {listing.quality_score:.1f}/10')
    
    # Check WOW features (premium business tools)
    wow_features = [
        ('Shop Setup Guide', listing.etsy_shop_setup_guide),
        ('Social Media Package', listing.etsy_social_media_package),
        ('Photography Guide', listing.etsy_photography_guide),
        ('Pricing Analysis', listing.etsy_pricing_analysis),
        ('SEO Report', listing.etsy_seo_report),
        ('Customer Service Templates', listing.etsy_customer_service_templates),
        ('Policies Templates', listing.etsy_policies_templates),
        ('Variations Guide', listing.etsy_variations_guide),
        ('Competitor Insights', listing.etsy_competitor_insights),
        ('Seasonal Calendar', listing.etsy_seasonal_calendar)
    ]
    
    print(f'\n💼 WOW FEATURES (Premium Business Tools):')
    generated_wow = 0
    total_wow_content = 0
    for name, content in wow_features:
        if content and len(content) > 100:
            print(f'   ✅ {name}: {len(content):,} chars')
            generated_wow += 1
            total_wow_content += len(content)
        else:
            print(f'   ❌ {name}: Missing/Short')
    
    print(f'   WOW Features Generated: {generated_wow}/10')
    print(f'   Total WOW Content: {total_wow_content:,} characters')
    
    # Calculate specialist scores
    title_score = calculate_title_score(title, starts_with_keyword, len(title_triggers))
    desc_score = calculate_description_score(description, story_count, sensory_count, emotion_count)
    wow_score = min(10.0, generated_wow)
    
    overall_specialist_score = (title_score + desc_score + wow_score) / 3
    
    print(f'\n🎯 TOP E-COMMERCE SPECIALIST EVALUATION:')
    print(f'   Title Optimization: {title_score:.1f}/10')
    print(f'   Description Storytelling: {desc_score:.1f}/10')
    print(f'   WOW Features Value: {wow_score:.1f}/10')
    print(f'   =====================')
    print(f'   SPECIALIST SCORE: {overall_specialist_score:.1f}/10')
    
    # Final assessment
    if overall_specialist_score >= 9.5:
        print('   🏆🏆 REVOLUTIONARY! Crushes all competition!')
        assessment = "REVOLUTIONARY"
    elif overall_specialist_score >= 9.0:
        print('   🏆 WORLD-CLASS! Beats top listing generators!')
        assessment = "WORLD-CLASS"
    elif overall_specialist_score >= 8.0:
        print('   ✅ EXCELLENT! Superior to most competitors!')
        assessment = "EXCELLENT"
    elif overall_specialist_score >= 7.0:
        print('   ⚠️ GOOD! Ready for fine-tuning to reach 10/10')
        assessment = "GOOD - NEEDS TUNING"
    else:
        print('   ❌ NEEDS MAJOR IMPROVEMENT')
        assessment = "NEEDS IMPROVEMENT"
    
    print(f'\n📋 COMPETITIVE ANALYSIS:')
    print(f'   vs Marmalead: {"✅ SUPERIOR" if overall_specialist_score >= 8.5 else "⚠️ COMPETITIVE"}')
    print(f'   vs eRank: {"✅ SUPERIOR" if overall_specialist_score >= 8.0 else "⚠️ COMPETITIVE"}')
    print(f'   vs Sale Samurai: {"✅ SUPERIOR" if overall_specialist_score >= 8.5 else "⚠️ COMPETITIVE"}')
    print(f'   vs Manual Creation: {"✅ VASTLY SUPERIOR" if overall_specialist_score >= 7.5 else "⚠️ COMPETITIVE"}')
    
    print(f'\n🌐 Frontend Test URL: http://localhost:3000/results/{listing.id}')
    
    return overall_specialist_score, assessment

def calculate_title_score(title, starts_with_keyword, trigger_count):
    """Calculate title optimization score"""
    score = 5.0  # Base score
    
    if starts_with_keyword:
        score += 2.0  # Primary keyword positioning
    
    if len(title) <= 140:
        score += 1.0  # Length compliance
    
    score += min(2.0, trigger_count * 0.4)  # Emotional triggers
    
    return min(10.0, score)

def calculate_description_score(description, story_count, sensory_count, emotion_count):
    """Calculate description storytelling score"""
    score = 5.0  # Base score
    
    if len(description) >= 800:
        score += 1.5  # Comprehensive length
    elif len(description) >= 500:
        score += 1.0
        
    score += min(2.0, story_count * 0.5)  # Storytelling elements
    score += min(1.0, sensory_count * 0.3)  # Sensory details
    score += min(1.5, emotion_count * 0.3)  # Emotional connection
    
    return min(10.0, score)

if __name__ == "__main__":
    main()