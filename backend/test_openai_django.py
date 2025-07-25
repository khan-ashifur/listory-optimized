#!/usr/bin/env python
"""
Test OpenAI within Django environment
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from django.conf import settings
from apps.listings.services import ListingGeneratorService

print("🔍 Testing OpenAI in Django Environment...")
print("=" * 50)

print(f"Django settings loaded: ✅")
print(f"OpenAI API Key configured: {'✅' if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != 'your-openai-api-key-here' else '❌'}")

if settings.OPENAI_API_KEY:
    print(f"API Key preview: {settings.OPENAI_API_KEY[:15]}...")

# Test the service
print("\nTesting ListingGeneratorService...")
try:
    service = ListingGeneratorService()
    if service.client:
        print("✅ OpenAI service initialized successfully!")
    else:
        print("❌ OpenAI service failed to initialize")
        
except Exception as e:
    print(f"❌ Error initializing service: {e}")

print("\n" + "=" * 50)
print("🔍 Django OpenAI test completed!")