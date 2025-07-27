#!/usr/bin/env python3
"""
Debug script to see the raw AI response and identify JSON parsing issues.
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

def debug_ai_response():
    """Debug the raw AI response to fix JSON parsing."""
    print("🔍 DEBUG: Testing AI Response Raw Output")
    print("=" * 50)
    
    # Get or create user
    user, _ = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
    
    # Create simple product for testing
    product = Product.objects.create(
        name='Simple Test Neck Massager',
        user=user,
        description='Electric neck massager with heat therapy for pain relief.',
        brand_name='TestBrand',
        brand_tone='friendly',
        target_platform='amazon',
        price=99.99,
        categories='Health & Personal Care, Massagers',
        features='Heat therapy, ergonomic design, auto shut-off',
        target_keywords='neck massager, pain relief, heat therapy',
        seo_keywords='electric neck massager, heated neck massager',
        long_tail_keywords='best neck massager for office workers',
        faqs='Q: Is it safe? A: Yes, with auto shut-off.',
        whats_in_box='Massager, power cord, manual',
        competitor_urls='https://example.com/competitor'
    )
    
    print(f"✅ Created test product: {product.name}")
    
    # Generate listing and capture raw response
    generator = ListingGeneratorService()
    
    # Override the generate_ai_content method to capture raw response
    import types
    
    def debug_generate_ai_content(self, product):
        """Debug version that saves raw response."""
        print("\n🚀 Generating AI content (debug mode)...")
        
        # Use the existing prompt generation logic
        original_method = ListingGeneratorService._generate_ai_content
        try:
            # Call original method but capture the response
            result = original_method(self, product)
            return result
        except Exception as e:
            print(f"❌ Error in AI generation: {str(e)}")
            # Let's manually call OpenAI to see the raw response
            return self._debug_manual_ai_call(product)
    
    def debug_manual_ai_call(self, product):
        """Manual AI call to debug response."""
        import openai
        import time
        
        # Get prompt (simplified version)
        prompt = f"""
Generate a valid JSON response for an Amazon listing for:
Product: {product.name}
Description: {product.description}

Return JSON with these fields:
{{
  "productTitle": "Write a 160-200 character title for {product.name}",
  "bulletPoints": [
    "Write bullet 1 with 150+ characters about the main benefit",
    "Write bullet 2 with 150+ characters about features",
    "Write bullet 3 with 150+ characters about usage",
    "Write bullet 4 with 150+ characters about quality",
    "Write bullet 5 with 150+ characters about guarantee"
  ],
  "productDescription": "Write 1500+ characters describing this product in detail",
  "brandSummary": "Write 200+ characters about the brand",
  "backendKeywords": "Write 240+ characters of search terms"
}}

CRITICAL: Ensure all text fields meet the minimum character requirements specified.
"""
        
        try:
            client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000,
                temperature=0.7,
            )
            
            raw_content = response.choices[0].message.content
            print(f"\n📄 RAW AI RESPONSE ({len(raw_content)} chars):")
            print("=" * 50)
            print(raw_content[:1000])
            print("..." if len(raw_content) > 1000 else "")
            print("=" * 50)
            
            # Save to file for inspection
            with open('debug_raw_response.txt', 'w', encoding='utf-8') as f:
                f.write(raw_content)
            print("💾 Raw response saved to 'debug_raw_response.txt'")
            
            # Try to parse JSON
            print("\n🔍 JSON PARSING ATTEMPTS:")
            
            # Attempt 1: Direct parse
            try:
                cleaned = raw_content.strip()
                if cleaned.startswith('```json'):
                    cleaned = cleaned[7:]
                if cleaned.endswith('```'):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                result = json.loads(cleaned)
                print("✅ SUCCESS: Direct JSON parsing worked!")
                
                # Check lengths
                title_len = len(result.get('productTitle', ''))
                desc_len = len(result.get('productDescription', ''))
                print(f"📏 Title length: {title_len} chars")
                print(f"📏 Description length: {desc_len} chars")
                
                if 'bulletPoints' in result:
                    bullets = result['bulletPoints']
                    print(f"📏 Number of bullets: {len(bullets)}")
                    for i, bullet in enumerate(bullets, 1):
                        print(f"📏 Bullet {i} length: {len(bullet)} chars")
                
                return result
                
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {str(e)}")
                print(f"Error at position {e.pos}")
                if e.pos < len(cleaned):
                    print(f"Content around error: '{cleaned[max(0, e.pos-20):e.pos+20]}'")
                
                return None
            
        except Exception as e:
            print(f"❌ OpenAI API error: {str(e)}")
            return None
    
    # Patch the methods
    generator._debug_manual_ai_call = types.MethodType(debug_manual_ai_call, generator)
    generator._generate_ai_content = types.MethodType(debug_generate_ai_content, generator)
    
    try:
        result = generator._debug_manual_ai_call(product)
        return result
    finally:
        # Clean up test product
        product.delete()
        print(f"\n🧹 Cleaned up test product")

if __name__ == "__main__":
    debug_ai_response()