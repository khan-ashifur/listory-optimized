#!/usr/bin/env python3
"""
DEBUG A+ CONTENT EXTRACTION
Find out what A+ content the AI is actually generating vs what's being saved
"""

import os
import sys
import django
import json
from datetime import datetime

# Add backend to Python path
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
import re

def debug_aplus_extraction():
    """Debug what A+ content the AI is generating"""
    
    print("🔍 DEBUGGING A+ CONTENT EXTRACTION")
    print("=" * 40)
    
    from django.contrib.auth.models import User
    user, created = User.objects.get_or_create(username='debug_aplus_extract')
    
    # Create a simple Turkey product
    product = Product.objects.create(
        user=user,
        name="Test Kulaklık",
        brand_name="TestBrand",
        marketplace="tr",
        marketplace_language="tr", 
        price=199.99,
        occasion="yeni_yil",
        brand_tone="luxury",
        categories="Electronics",
        description="Test ürün",
        features="Feature 1\nFeature 2"
    )
    
    print(f"✅ Test Product Created: {product.id}")
    
    # Monkey patch to capture the AI response
    original_method = None
    captured_response = None
    
    def capture_ai_response(self, response_text):
        nonlocal captured_response
        captured_response = response_text
        print(f"🤖 AI Response Captured: {len(response_text)} characters")
        
        # Try to extract aPlusContentPlan
        try:
            # Find JSON in response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                ai_data = json.loads(json_str)
                
                aplus_plan = ai_data.get('aPlusContentPlan', {})
                if aplus_plan:
                    print(f"📋 A+ Content Plan Found: {len(aplus_plan)} sections")
                    for key, value in aplus_plan.items():
                        if isinstance(value, dict):
                            title = value.get('title', 'No title')
                            content = value.get('content', 'No content')
                            print(f"   📄 {key}: {title[:50]}... (content: {len(content)} chars)")
                        else:
                            print(f"   📄 {key}: {str(value)[:100]}...")
                else:
                    print("❌ No aPlusContentPlan found in AI response")
            else:
                print("❌ No valid JSON found in AI response")
                
        except Exception as e:
            print(f"❌ Error parsing AI response: {e}")
        
        return response_text
    
    try:
        # Generate listing
        service = ListingGeneratorService()
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"\n📊 Generation Complete:")
        print(f"   Status: {listing.status}")
        print(f"   A+ Content Length: {len(listing.amazon_aplus_content)} characters")
        
        # Check what's in the A+ content
        aplus_content = listing.amazon_aplus_content
        
        # Count sections
        generic_indicators = [
            'Complete A+ Content Strategy',
            'AI-Generated Briefs',
            'Design Guidelines',
            'Ready for Production'
        ]
        
        turkish_indicators = [
            'türk', 'aile', 'kalite', 'garanti', 'ürün', 'müşteri'
        ]
        
        generic_count = sum(1 for indicator in generic_indicators if indicator in aplus_content)
        turkish_count = sum(1 for indicator in turkish_indicators if indicator.lower() in aplus_content.lower())
        
        print(f"\n🔍 A+ CONTENT ANALYSIS:")
        print(f"   Generic English elements: {generic_count}/{len(generic_indicators)}")
        print(f"   Turkish elements: {turkish_count}/{len(turkish_indicators)}")
        
        # Check for specific sections
        if 'aplus-section-card' in aplus_content:
            section_count = aplus_content.count('aplus-section-card')
            print(f"   A+ Section Cards: {section_count}")
        
        # Look for the actual Turkish content
        turkish_content_matches = re.findall(r'<h3[^>]*>([^<]*(?:türk|aile|kalite)[^<]*)</h3>', aplus_content, re.IGNORECASE)
        if turkish_content_matches:
            print(f"   Turkish Headers Found: {len(turkish_content_matches)}")
            for match in turkish_content_matches[:3]:
                print(f"     • {match}")
        
        # Save the A+ content for inspection
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f'debug_aplus_content_{timestamp}.html', 'w', encoding='utf-8') as f:
            f.write(aplus_content)
        
        print(f"\n💾 A+ content saved to debug_aplus_content_{timestamp}.html")
        
        # Summary assessment
        print(f"\n🎯 ASSESSMENT:")
        if generic_count > 2:
            print("❌ Using generic English template instead of AI-generated Turkish content")
            print("🔧 ROOT CAUSE: A+ content generation not using aPlusContentPlan from AI")
        elif turkish_count >= 4:
            print("✅ Turkish content properly integrated")
        else:
            print("⚠️ Mixed content - partial localization")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()
        print(f"\n🧹 Test product cleaned up")

if __name__ == "__main__":
    debug_aplus_extraction()