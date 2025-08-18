#!/usr/bin/env python3
"""
DEBUG TURKEY JSON PARSING FAILURES
Find exactly what's causing Turkey JSON to fail while Mexico succeeds
"""

import os
import sys
import django
import json
import re
from datetime import datetime

# Add backend to Python path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_turkey_json_parsing():
    """Debug Turkey JSON parsing failures"""
    
    print("🔍 DEBUGGING TURKEY JSON PARSING FAILURES")
    print("=" * 45)
    
    # Let's monkey patch the JSON parsing to capture the raw response
    from apps.listings.services import ListingGeneratorService
    from apps.core.models import Product
    
    captured_responses = {}
    
    # Monkey patch to capture responses
    original_generate = ListingGeneratorService._generate_amazon_listing
    
    def capture_response(self, product, listing):
        # Call original method but capture any JSON parsing attempts
        try:
            return original_generate(self, product, listing)
        except Exception as e:
            print(f"❌ Generation failed: {e}")
            raise
    
    ListingGeneratorService._generate_amazon_listing = capture_response
    
    try:
        from django.contrib.auth.models import User
        user, created = User.objects.get_or_create(username='json_debug')
        
        # Test Mexico first (working case)
        print("🇲🇽 TESTING MEXICO (BASELINE):")
        print("-" * 30)
        
        product_mx = Product.objects.create(
            user=user,
            name="JSON Test Product",
            brand_name="JSONTest",
            marketplace="mx",
            marketplace_language="es-mx", 
            price=199.99,
            occasion="navidad",
            brand_tone="luxury",
            categories="Electronics",
            description="JSON test",
            features="Feature 1\nFeature 2"
        )
        
        service = ListingGeneratorService()
        
        # Temporarily capture the OpenAI response for Mexico
        print("🤖 Generating Mexico listing to capture JSON...")
        
        try:
            listing_mx = service.generate_listing(product_mx.id, 'amazon')
            print(f"✅ Mexico JSON parsing: SUCCESS")
            print(f"📊 Mexico result: {listing_mx.status}")
        except Exception as e:
            print(f"❌ Mexico JSON parsing: FAILED - {e}")
        
        product_mx.delete()
        
        print("\n🇹🇷 TESTING TURKEY (PROBLEM CASE):")
        print("-" * 35)
        
        product_tr = Product.objects.create(
            user=user,
            name="JSON Test Product", 
            brand_name="JSONTest",
            marketplace="tr",
            marketplace_language="tr",
            price=199.99,
            occasion="yeni_yil",
            brand_tone="luxury",
            categories="Electronics",
            description="JSON test",
            features="Feature 1\nFeature 2"
        )
        
        print("🤖 Generating Turkey listing to capture JSON...")
        
        try:
            listing_tr = service.generate_listing(product_tr.id, 'amazon')
            print(f"✅ Turkey JSON parsing: SUCCESS")
            print(f"📊 Turkey result: {listing_tr.status}")
        except Exception as e:
            print(f"❌ Turkey JSON parsing: FAILED - {e}")
        
        product_tr.delete()
        
        print("\n🔍 ROOT CAUSE ANALYSIS:")
        print("=" * 25)
        
        # The issue is likely in the Turkish language characters or prompt differences
        # Let's check what might be different in the prompts
        
        from apps.listings.international_localization_optimizer import InternationalLocalizationOptimizer
        optimizer = InternationalLocalizationOptimizer()
        
        try:
            mx_enhancement = optimizer.get_localization_enhancement("mx", "es-mx")
            tr_enhancement = optimizer.get_localization_enhancement("tr", "tr")
            
            print(f"🇲🇽 Mexico enhancement length: {len(mx_enhancement) if mx_enhancement else 0}")
            print(f"🇹🇷 Turkey enhancement length: {len(tr_enhancement) if tr_enhancement else 0}")
            
            if tr_enhancement:
                # Check for problematic characters
                problematic_chars = []
                special_chars = set()
                
                for char in tr_enhancement:
                    if ord(char) > 127:  # Non-ASCII
                        special_chars.add(char)
                    # Check for JSON-breaking characters
                    if char in ['"', "'", '\\', '{', '}', '[', ']']:
                        if char not in ['"', "'", '\\']:  # Allow some special chars
                            problematic_chars.append(char)
                
                print(f"🇹🇷 Special Turkish characters: {len(special_chars)}")
                print(f"🇹🇷 Sample special chars: {list(special_chars)[:10]}")
                
                if problematic_chars:
                    print(f"⚠️ Potentially problematic chars: {problematic_chars}")
                
                # Look for specific patterns that might break JSON
                json_breaking_patterns = [
                    r'[^\\]"[^:]',  # Unescaped quotes
                    r'\\n\\n',      # Double newlines
                    r'\t',          # Tab characters
                    r'[{}]',        # Unmatched braces
                ]
                
                for pattern in json_breaking_patterns:
                    matches = re.findall(pattern, tr_enhancement)
                    if matches:
                        print(f"⚠️ Pattern '{pattern}' found {len(matches)} times")
                
        except Exception as e:
            print(f"❌ Error analyzing enhancements: {e}")
        
        print("\n💡 LIKELY CAUSES:")
        print("-" * 15)
        print("1. Turkish characters (ü, ğ, ı, ö, ş, ç) in JSON strings")
        print("2. Unescaped quotes in Turkish prompt text")
        print("3. Different prompt length causing JSON structure issues")
        print("4. Special formatting in Turkish enforcement rules")
        print("5. Character encoding issues during JSON generation")
        
        print("\n🔧 RECOMMENDED FIXES:")
        print("-" * 20)
        print("1. Ensure proper JSON escaping for Turkish characters")
        print("2. Review Turkish prompt for quote escaping")
        print("3. Add specific Turkish JSON parsing fallback")
        print("4. Improve character encoding handling")
        print("5. Add debug logging for Turkish JSON parsing")
        
    except Exception as e:
        print(f"❌ Debug error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_turkey_json_parsing()