#!/usr/bin/env python3
"""
Test script to generate a completely new listing with updated prompt.
"""
import os
import sys
import django
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def test_new_generation():
    """Test with a new product to get fresh AI generation."""
    print("🧪 Testing with New Product for Fresh Generation...")
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create a new product for testing
    product = Product.objects.create(
        name='Smart Wireless Earbuds Pro',
        user=user,
        description='Premium wireless earbuds with noise cancellation and long battery life. Perfect for music lovers and professionals.',
        brand_name='SoundMax',
        brand_tone='professional', 
        target_platform='amazon',
        price=89.99,
        categories='Electronics, Headphones, Wireless Earbuds',
        features='Noise cancellation, 24hr battery, waterproof, quick charge, premium sound',
        target_keywords='wireless earbuds, bluetooth headphones, noise cancelling',
        seo_keywords='wireless earbuds, bluetooth earbuds, noise cancelling headphones',
        long_tail_keywords='wireless earbuds with noise cancellation, best bluetooth earbuds for exercise',
        faqs='How long does battery last? Up to 24 hours with case. Are they waterproof? Yes, IPX5 rated.',
        whats_in_box='Earbuds, charging case, USB-C cable, ear tips (S/M/L), user manual',
        competitor_urls='https://www.amazon.com/competitor-earbuds'
    )
    
    print(f"✅ Created new product: {product.name}")
    
    # Generate listing
    generator = ListingGeneratorService()
    print("\n🚀 Generating Amazon listing with updated prompt...")
    
    try:
        listing = generator.generate_listing(product.id, 'amazon')
        
        print("\n📊 GENERATION RESULTS:")
        print("=" * 50)
        
        # Check A+ content with image requirements
        if listing.amazon_aplus_content:
            try:
                aplus_data = json.loads(listing.amazon_aplus_content)
                aplus_plan = aplus_data.get('aPlusContentPlan', {})
                
                print("🎨 A+ Content with Image Requirements:")
                for section_key, section_data in aplus_plan.items():
                    if isinstance(section_data, dict):
                        title = section_data.get('title', 'No title')
                        image_req = section_data.get('image_requirements', 'No image requirements')
                        
                        print(f"\n📸 {section_key.upper()}:")
                        print(f"   Title: {title}")
                        if len(image_req) > 50:
                            print(f"   ✅ Image Requirements: {len(image_req)} chars")
                            print(f"   Preview: {image_req[:100]}...")
                        else:
                            print(f"   ❌ Image Requirements: {image_req}")
                            
            except json.JSONDecodeError:
                print("❌ A+ content is not valid JSON")
        else:
            print("❌ No A+ content generated")
        
        # Clean up test product
        product.delete()
        print(f"\n🧹 Cleaned up test product")
        
        print("\n" + "=" * 50)
        return listing
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        product.delete()  # Clean up even on error
        return None

if __name__ == "__main__":
    test_new_generation()