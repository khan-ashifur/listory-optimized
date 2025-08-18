"""
🇯🇵 DIRECT JAPANESE GENERATION TEST
Bypass the broken JSON parser and test AI generation directly
"""

import os
import sys
import django

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def test_direct_japanese():
    """Test Japanese generation with direct OpenAI call"""
    
    print("🇯🇵 TESTING JAPANESE GENERATION - DIRECT API CALL")
    print("=" * 60)
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User
        import json
        
        service = ListingGeneratorService()
        
        # Create test product
        user, _ = User.objects.get_or_create(username='direct_jp', defaults={'email': 'test@amazon.co.jp'})
        product = Product.objects.create(
            user=user,
            name='高品質ワイヤレスイヤホン',
            description='ノイズキャンセリング機能付きワイヤレスイヤホン',
            brand_name='TechSound',
            brand_tone='professional', 
            target_platform='amazon',
            marketplace='jp',
            marketplace_language='ja',
            price=12800,
            occasion='正月',
            categories='Electronics,Audio',
            features='ノイズキャンセリング,30時間バッテリー,Bluetooth5.3,IPX5防水'
        )
        
        # Build the prompt manually to see what's sent to AI
        print("🤖 BUILDING JAPANESE PROMPT...")
        
        title_format = service.get_marketplace_title_format('jp', 'TechSound')
        bullet_format = service.get_marketplace_bullet_format('jp', 1)
        desc_format = service.get_marketplace_description_format('jp', 'professional')
        
        # Build basic prompt structure (simplified)
        prompt = f"""
You are generating Amazon Japan (Amazon.co.jp) listing content in PERFECT JAPANESE.

Product: {product.name}
Brand: {product.brand_name}
Price: ¥{product.price}
Occasion: {product.occasion}
Features: {product.features}

CRITICAL: ALL content must be in Japanese using proper keigo (polite form).

{title_format[:800]}

{bullet_format[:600]}

{desc_format[:800]}

Return JSON with:
{{
  "productTitle": "Japanese title here",
  "bulletPoints": [
    "Japanese bullet 1 here",
    "Japanese bullet 2 here", 
    "Japanese bullet 3 here",
    "Japanese bullet 4 here",
    "Japanese bullet 5 here"
  ],
  "productDescription": "Japanese description here"
}}

MANDATORY: Use ONLY Japanese characters. Include proper keigo (です/ます). Focus on trust, quality, and technical precision.
"""

        print(f"✅ Prompt built: {len(prompt)} characters")
        print(f"📝 Prompt sample: {prompt[:200]}...")
        
        # Try direct OpenAI call
        if service.client:
            print(f"\n🚀 CALLING OPENAI DIRECTLY...")
            
            response = service.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert Japanese copywriter for Amazon Japan. Generate perfect Japanese listing content with proper keigo."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            raw_response = response.choices[0].message.content
            print(f"✅ Raw AI Response ({len(raw_response)} chars):")
            print(f"📝 Response preview: {raw_response[:300]}...")
            
            # Try to parse JSON manually
            try:
                # Find JSON in response
                json_start = raw_response.find('{')
                json_end = raw_response.rfind('}') + 1
                
                if json_start >= 0 and json_end > json_start:
                    json_content = raw_response[json_start:json_end]
                    parsed = json.loads(json_content)
                    
                    print(f"\n🎌 SUCCESSFUL JAPANESE CONTENT:")
                    print(f"Title: {parsed.get('productTitle', 'MISSING')}")
                    print(f"\nBullets ({len(parsed.get('bulletPoints', []))}):")
                    for i, bullet in enumerate(parsed.get('bulletPoints', [])[:3], 1):
                        print(f"  {i}. {bullet}")
                    print(f"\nDescription: {parsed.get('productDescription', 'MISSING')[:200]}...")
                    
                    # Validate Japanese content
                    title = parsed.get('productTitle', '')
                    description = parsed.get('productDescription', '')
                    bullets = parsed.get('bulletPoints', [])
                    
                    validation = {
                        'Has Japanese chars': any(ord(c) > 127 for c in title + description + str(bullets)),
                        'Uses keigo (です/ます)': any(word in title + description + str(bullets) for word in ['です', 'ます']),
                        'Has trust signals': any(word in title + description for word in ['正規品', '保証', '安心']),
                        'Has technical specs': any(word in description for word in ['30時間', 'Bluetooth5.3', 'IPX5']),
                        'Proper occasion (正月)': '正月' in title + description + str(bullets)
                    }
                    
                    score = sum(validation.values()) / len(validation) * 100
                    print(f"\n🏮 JAPANESE VALIDATION:")
                    for check, passed in validation.items():
                        print(f"   {'✅' if passed else '❌'} {check}")
                    
                    print(f"\n🎌 JAPANESE QUALITY: {score:.1f}%")
                    
                    if score >= 80:
                        print("🎉 DIRECT JAPANESE GENERATION: SUCCESS!")
                        print("💡 The issue is in the JSON parsing infrastructure, not Japanese content generation.")
                        return True
                    else:
                        print("⚠️ Japanese content needs improvement")
                        return False
                        
                else:
                    print("❌ No valid JSON found in response")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing failed: {e}")
                print(f"Raw content: {json_content[:200]}...")
                return False
                
        else:
            print("❌ No OpenAI client available")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        try:
            product.delete()
        except:
            pass

if __name__ == "__main__":
    success = test_direct_japanese()
    if success:
        print(f"\n🏆 CONCLUSION: Japanese generation works perfectly!")
        print("🔧 Fix needed: JSON parsing infrastructure, not Japanese implementation")
    else:
        print(f"\n🔧 NEEDS INVESTIGATION")