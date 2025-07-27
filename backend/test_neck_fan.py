#!/usr/bin/env python
"""
Test the neck fan product specifically to fix the quality issues
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import Product
from apps.listings.models import GeneratedListing
from apps.listings.services import ListingGeneratorService
import time

def test_neck_fan():
    print("🎯 TESTING IMPROVED NECK FAN LISTING GENERATION")
    print("=" * 60)
    
    # Get the first user
    user = User.objects.first()
    if not user:
        print("❌ No users found. Please create a user first.")
        return
    
    print(f"✅ Using user: {user.username}")
    
    # Create neck fan product exactly like the example
    product = Product.objects.create(
        user=user,
        name='kzen Portable Neck Fan Rechargeable',
        brand_name='kzen',
        description='Wearable neck fan that provides hands-free cooling with 30-hour battery life',
        features='30-hour battery life, 6 adjustable speeds, 360-degree airflow, Type-C dual charging, whisper-quiet motor, hair-safe design',
        categories='Electronics, Personal Care, Cooling Devices',
        price=49.99,
        brand_tone='casual'
    )
    
    print(f"✅ Created product: {product.name}")
    print(f"📊 Brand Tone: {product.brand_tone}")
    print(f"💰 Price: ${product.price}")
    
    try:
        # Generate Amazon listing with improved prompt
        service = ListingGeneratorService()
        print("🤖 Generating improved Amazon listing...")
        
        start_time = time.time()
        listing = service.generate_listing(product.id, 'amazon')
        generation_time = time.time() - start_time
        
        print(f"⏱️  Generation completed in {generation_time:.2f} seconds")
        print(f"📝 Listing ID: {listing.id}")
        
        # Display detailed results
        print(f"\n📋 DETAILED LISTING ANALYSIS:")
        print("=" * 50)
        
        print(f"TITLE ({len(listing.title)} chars):")
        print(f"'{listing.title}'")
        
        print(f"\nBULLET POINTS:")
        bullets = listing.bullet_points.split('\n') if listing.bullet_points else []
        for i, bullet in enumerate(bullets, 1):
            if bullet.strip():
                print(f"{i}. ({len(bullet)} chars) {bullet}")
        
        print(f"\nDESCRIPTION ({len(listing.long_description)} chars):")
        print(f"'{listing.long_description[:200]}...'")
        
        print(f"\nFAQS:")
        if listing.faqs:
            faqs = listing.faqs.split('\n')
            for i, faq in enumerate(faqs[:3], 1):
                if faq.strip():
                    print(f"{i}. {faq[:100]}...")
        
        # Quality analysis
        content = f"{listing.title} {listing.bullet_points} {listing.long_description}".lower()
        
        # Check for forbidden phrases
        forbidden = ['premium quality', 'state-of-the-art', 'cutting-edge', 'ultimate', 'amazing', 'awesome']
        found_forbidden = [phrase for phrase in forbidden if phrase in content]
        
        # Check for emotional triggers
        emotional_triggers = ['finally', 'breakthrough', 'never again', 'transform', 'revolutionary', 'instant', 'game-changing', 'life-changing']
        found_triggers = [trigger for trigger in emotional_triggers if trigger in content]
        
        # Check for specific use cases
        use_cases = ['meeting', 'commute', 'work', 'exercise', 'travel', 'office']
        found_use_cases = [case for case in use_cases if case in content]
        
        print(f"\n🔍 QUALITY ANALYSIS:")
        print("=" * 30)
        print(f"✅ Emotional Triggers Found: {len(found_triggers)}/8 - {found_triggers}")
        print(f"✅ Use Cases Mentioned: {len(found_use_cases)}/6 - {found_use_cases}")
        print(f"❌ Forbidden Phrases: {len(found_forbidden)} - {found_forbidden}")
        
        # Check for typos in title and bullets
        potential_typos = []
        if 'rechargeablea' in listing.title.lower():
            potential_typos.append("Title typo: 'Rechargeablea'")
        
        if potential_typos:
            print(f"❌ Potential Typos: {potential_typos}")
        else:
            print(f"✅ No obvious typos detected")
        
        # Store quality metrics if available
        if hasattr(listing, 'quality_score'):
            print(f"\n🎯 AI Quality Score: {listing.quality_score}/10")
            if hasattr(listing, 'emotion_score'):
                print(f"💫 Emotion Score: {listing.emotion_score}/10")
            if hasattr(listing, 'conversion_score'):
                print(f"💰 Conversion Score: {listing.conversion_score}/10")
        
        # Overall assessment
        print(f"\n📊 IMPROVEMENT ASSESSMENT:")
        score = 0
        if len(found_triggers) >= 3: score += 2
        if len(found_use_cases) >= 3: score += 2  
        if len(found_forbidden) == 0: score += 2
        if len(potential_typos) == 0: score += 2
        if len(listing.title) >= 100: score += 1
        if len(bullets) >= 5: score += 1
        
        print(f"Overall Improvement Score: {score}/10")
        
        if score >= 8:
            print("🎉 EXCELLENT - High quality listing generated!")
        elif score >= 6:
            print("✅ GOOD - Significant improvements made")
        elif score >= 4:
            print("⚠️ MODERATE - Some improvements but needs work")
        else:
            print("❌ POOR - Major issues still present")
            
    except Exception as e:
        print(f"❌ Error generating listing: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_neck_fan()