#!/usr/bin/env python3
"""
Test script to verify the Amazon listing generation integration works correctly.
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import Product
from apps.listings.services import ListingGeneratorService

def test_amazon_listing_generation():
    """Test the Amazon listing generation with the new prompt structure."""
    print("🧪 Testing Amazon listing generation...")
    
    # Create a test user if it doesn't exist
    test_user, created = User.objects.get_or_create(
        username="testuser",
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print(f"✅ Created test user: {test_user.username}")
    else:
        print(f"✅ Using existing test user: {test_user.username}")
    
    # Create a test product if it doesn't exist
    test_product, created = Product.objects.get_or_create(
        name="Test Air Fryer",
        user=test_user,
        defaults={
            'brand_name': 'TestBrand',
            'description': 'A compact digital air fryer for healthy cooking',
            'features': 'Digital controls, 4-quart capacity, dishwasher safe basket, 12 preset programs',
            'categories': 'Kitchen Appliances, Air Fryers',
            'brand_tone': 'casual',
            'target_platform': 'amazon',
            'price': 89.99
        }
    )
    
    if created:
        print(f"✅ Created test product: {test_product.name}")
    else:
        print(f"✅ Using existing test product: {test_product.name}")
    
    # Initialize the service
    service = ListingGeneratorService()
    
    # Check OpenAI client status
    if not service.client:
        print("❌ OpenAI client not configured. Please set OPENAI_API_KEY in .env file.")
        return False
    
    print("✅ OpenAI client configured successfully")
    
    try:
        # Generate the listing
        print("🔄 Generating Amazon listing...")
        listing = service.generate_listing(test_product.id, 'amazon')
        print(f"✅ Listing generated successfully with ID: {listing.id}")
        
        # Verify the listing has the expected structure
        print("\n📋 Listing verification:")
        print(f"  Title: {listing.title[:50]}...")
        print(f"  Bullet points: {len(listing.bullet_points.split('\\n\\n')) if listing.bullet_points else 0} bullets")
        print(f"  Description length: {len(listing.long_description)} characters")
        print(f"  Keywords: {len(listing.keywords.split(', ')) if listing.keywords else 0} keywords")
        print(f"  Backend keywords: {len(listing.amazon_backend_keywords)} characters")
        print(f"  A+ Content: {len(listing.amazon_aplus_content)} characters")
        print(f"  Hero title: {listing.hero_title[:30]}..." if listing.hero_title else "  Hero title: Not set")
        print(f"  Features: {len(listing.features.split('\\n')) if listing.features else 0} features")
        print(f"  FAQs: {len(listing.faqs.split('\\n')) if listing.faqs else 0} FAQs")
        print(f"  Status: {listing.status}")
        
        # Verify A+ content structure
        if listing.amazon_aplus_content:
            try:
                import json
                aplus_data = json.loads(listing.amazon_aplus_content)
                print("\\n🎨 A+ Content verification:")
                print(f"  A+ Plan sections: {len([k for k in aplus_data.get('aPlusContentPlan', {}).keys() if k.startswith('section')])}")
                print(f"  PPC strategy present: {'✅' if aplus_data.get('ppcStrategy') else '❌'}")
                print(f"  Keyword strategy: {'✅' if aplus_data.get('keywordStrategy') else '❌'}")
                print(f"  Brand summary: {'✅' if aplus_data.get('brandSummary') else '❌'}")
            except Exception as e:
                print(f"  ❌ A+ Content parsing error: {e}")
        
        if listing.status == 'completed':
            print("✅ All tests passed! Amazon listing generation is working correctly.")
            return True
        else:
            print(f"❌ Listing generation failed with status: {listing.status}")
            return False
            
    except Exception as e:
        print(f"❌ Error during listing generation: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("🚀 Starting Amazon listing generation integration test...")
    success = test_amazon_listing_generation()
    
    if success:
        print("\n🎉 Integration test completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Integration test failed!")
        sys.exit(1)