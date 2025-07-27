#!/usr/bin/env python
"""
Test the optimized Amazon listing generation with brand tone integration
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

def test_optimized_listing():
    print("🚀 TESTING OPTIMIZED AMAZON LISTING GENERATION")
    print("=" * 60)
    
    # Get the first user
    user = User.objects.first()
    if not user:
        print("❌ No users found. Please create a user first.")
        return
    
    print(f"✅ Using user: {user.username}")
    
    # Test different brand tones
    test_cases = [
        {
            'name': 'Premium Translation Earbuds',
            'brand_name': 'TIMEKETTLE',
            'description': 'Real-time translation earbuds that break down language barriers',
            'features': 'Real-time translation, 40+ languages, 95% accuracy, 12-hour battery, noise cancellation',
            'categories': 'Electronics, Audio, Translation Devices',
            'price': 249.99,
            'brand_tone': 'professional'
        },
        {
            'name': 'Cozy Weighted Blanket',
            'brand_name': 'DreamChill',
            'description': 'Ultra-soft weighted blanket for better sleep and anxiety relief',
            'features': '15lb weight, breathable fabric, machine washable, anxiety relief, sleep improvement',
            'categories': 'Home & Garden, Bedding, Weighted Blankets',
            'price': 89.99,
            'brand_tone': 'casual'
        },
        {
            'name': 'Diamond Luxury Watch',
            'brand_name': 'PRESTIGE',
            'description': 'Swiss-made luxury timepiece with genuine diamonds',
            'features': 'Swiss movement, genuine diamonds, sapphire crystal, water resistant, leather strap',
            'categories': 'Jewelry & Watches, Luxury Watches, Swiss Watches',
            'price': 2499.99,
            'brand_tone': 'luxury'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🎯 TEST CASE {i}: {test_case['brand_tone'].upper()} BRAND TONE")
        print("-" * 40)
        
        # Create test product
        product = Product.objects.create(
            user=user,
            name=test_case['name'],
            brand_name=test_case['brand_name'],
            description=test_case['description'],
            features=test_case['features'],
            categories=test_case['categories'],
            price=test_case['price'],
            brand_tone=test_case['brand_tone']
        )
        
        print(f"✅ Created product: {product.name}")
        print(f"📊 Brand Tone: {product.brand_tone}")
        print(f"💰 Price: ${product.price}")
        
        try:
            # Generate Amazon listing
            service = ListingGeneratorService()
            print("🤖 Generating optimized Amazon listing...")
            
            start_time = time.time()
            listing = service.generate_listing(product.id, 'amazon')
            generation_time = time.time() - start_time
            
            print(f"⏱️  Generation completed in {generation_time:.2f} seconds")
            print(f"📝 Listing ID: {listing.id}")
            
            # Display results
            print(f"\n📋 GENERATED LISTING ANALYSIS:")
            print(f"Title Length: {len(listing.title)} chars")
            print(f"Title: {listing.title[:100]}...")
            
            # Count bullet points
            bullet_count = len(listing.bullet_points.split('\n')) if listing.bullet_points else 0
            print(f"Bullet Points: {bullet_count}")
            
            # Check for brand tone indicators
            content = f"{listing.title} {listing.bullet_points} {listing.long_description}".lower()
            
            tone_indicators = {
                'professional': ['professional', 'reliable', 'proven', 'certified', 'industry-leading'],
                'casual': ['awesome', 'super', 'totally', 'perfect', 'amazing'],
                'luxury': ['premium', 'luxury', 'exclusive', 'elite', 'sophisticated'],
                'playful': ['fun', 'playful', 'exciting', 'vibrant', 'energetic'],
                'minimal': ['simple', 'clean', 'minimalist', 'essential', 'streamlined'],
                'bold': ['breakthrough', 'revolutionary', 'game-changing', 'powerful', 'bold']
            }
            
            detected_tone_words = []
            for word in tone_indicators.get(product.brand_tone, []):
                if word in content:
                    detected_tone_words.append(word)
            
            print(f"🎨 Brand Tone Alignment: {len(detected_tone_words)}/5 tone words detected: {detected_tone_words}")
            
            # Check for quality indicators
            quality_indicators = ['finally', 'breakthrough', 'transform', 'never again', 'instant']
            quality_score = sum(1 for word in quality_indicators if word in content)
            print(f"⭐ Quality Score: {quality_score}/5 emotional triggers found")
            
            # Check FAQ quality
            if listing.faqs:
                faq_count = listing.faqs.count('Q:')
                print(f"❓ FAQs Generated: {faq_count} questions")
            
            # Store quality metrics if available
            if hasattr(listing, 'quality_score'):
                print(f"🎯 AI Quality Score: {listing.quality_score}/10")
            
            print(f"✅ Test case {i} completed successfully!")
            
        except Exception as e:
            print(f"❌ Error generating listing: {str(e)}")
            import traceback
            traceback.print_exc()
        
        print()
    
    print("🎉 ALL TESTS COMPLETED!")
    print("\n📊 SUMMARY:")
    print("- Testing optimized AI prompts with brand tone integration")
    print("- All brand tones should produce distinct writing styles")
    print("- Quality should be 8-10/10 with emotional engagement")
    print("- Listings should be conversion-focused with proper keywords")

if __name__ == "__main__":
    test_optimized_listing()