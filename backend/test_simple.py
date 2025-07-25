#!/usr/bin/env python
"""
Simple test of the updated listing generation
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from django.conf import settings
from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

print("Testing updated Listory Amazon listing generation...")
print("=" * 50)

print(f"Django settings loaded: OK")
print(f"OpenAI API Key configured: {'OK' if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != 'your-openai-api-key-here' else 'NO'}") 

if settings.OPENAI_API_KEY:
    print(f"API Key preview: {settings.OPENAI_API_KEY[:15]}...")

# Test the service
print("\nTesting ListingGeneratorService...")
try:
    service = ListingGeneratorService()
    if service.client:
        print("OpenAI service initialized successfully!")
        
        # Create a test product
        test_product = Product.objects.create(
            name="Premium Wireless Earbuds",
            brand_name="AudioTech",
            description="High-quality wireless earbuds with noise cancellation and long battery life",
            features="Noise cancellation, 24-hour battery, waterproof design",
            categories="Electronics, Audio, Headphones",
            price=79.99,
            brand_tone="Professional yet friendly"
        )
        
        print(f"\nTest product created: {test_product.name}")
        print("Generating Amazon listing with new emotional conversion format...")
        
        # Generate listing
        listing = service.generate_listing(test_product.id, 'amazon')
        
        print("\n" + "=" * 50)
        print("RESULTS:")
        print("=" * 50)
        print(f"Title ({len(listing.title)} chars): {listing.title}")
        print(f"\nBullet Points:\n{listing.bullet_points}")
        print(f"\nConversion Boosters:\n{listing.short_description[:200]}...")
        print(f"\nKeywords: {listing.keywords[:100]}...")
        
        # Cleanup
        test_product.delete()
        listing.delete()
        
        print("\nTest completed successfully!")
        
    else:
        print("OpenAI service failed to initialize")
        
except Exception as e:
    print(f"Error during test: {e}")

print("\n" + "=" * 50)
print("Test completed!")