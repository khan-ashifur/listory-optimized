"""
Debug Turkey A+ Plan Extraction
"""
import os
import sys
import django

# Set up Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService

def test_aplus_plan_extraction():
    """Test what A+ plan gets extracted for Turkey"""
    try:
        print("🇹🇷 Testing Turkey A+ Plan Extraction...")
        
        # Get Turkey product
        product = Product.objects.filter(marketplace='tr').first()
        if not product:
            print("❌ No Turkey products found")
            return
        
        print(f"✅ Turkey Product: {product.name} (ID: {product.id})")
        
        # Initialize service and make a direct AI call to see the response
        service = ListingGeneratorService()
        
        # Test with manual AI call to capture the actual A+ plan
        print("\n🤖 Making AI call to see A+ plan structure...")
        
        # Create a minimal test prompt
        test_prompt = f"""
Create a comprehensive listing for this product in Turkish with 8-section A+ content:

Product: {product.name}
Brand: {product.brand_name}
Description: {product.description}

🚨🚨🚨 KRİTİK 8 BÖLÜM A+ İÇERİK KURALI - MEKSİKA SEVİYESİNDE ZORUNLU! 🚨🚨🚨
TURKEY için MUTLAKA 8 comprehensive bölüm oluştur:

"aPlusContentPlan": {{
  "section1_hero": {{
    "title": "Türkçe ana başlık",
    "content": "Detaylı Türkçe hikaye (min 200 karakter)",
    "keywords": ["türkçe", "anahtar", "kelimeler"],
    "imageDescription": "ENGLISH: EXTREMELY detailed description...",
    "seoOptimization": "ENGLISH: SEO strategy note"
  }},
  "section2_features": {{ ... }},
  "section3_usage": {{ ... }},
  "section4_quality": {{ ... }},
  "section5_social_proof": {{ ... }},
  "section6_comparison": {{ ... }},
  "section7_warranty": {{ ... }},
  "section8_package": {{ ... }}
}}

ZORUNLU: Tüm 8 bölümü eksiksiz oluştur!

Return ONLY valid JSON.
"""
        
        try:
            response = service.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert Amazon listing creator."},
                    {"role": "user", "content": test_prompt}
                ],
                max_tokens=16000,
                temperature=0.7
            )
            
            ai_content = response.choices[0].message.content
            print(f"📝 AI Response length: {len(ai_content)} characters")
            
            # Check if response contains A+ plan
            if "aPlusContentPlan" in ai_content:
                print("✅ A+ Content Plan found in AI response!")
                
                # Try to extract A+ plan manually
                import re
                import json
                
                # Look for the A+ plan specifically
                aplus_pattern = r'"aPlusContentPlan":\s*({.*?}(?=,\s*"[^"]*":|\s*}$))'
                match = re.search(aplus_pattern, ai_content, re.DOTALL)
                
                if match:
                    aplus_json = match.group(1)
                    try:
                        aplus_plan = json.loads(aplus_json)
                        print(f"🎯 A+ Plan extracted successfully: {len(aplus_plan)} sections")
                        for section_key in aplus_plan.keys():
                            print(f"   - {section_key}")
                            
                        # Test if this would trigger Turkey logic
                        if aplus_plan:
                            print("✅ This A+ plan would trigger Turkey comprehensive sections!")
                        else:
                            print("❌ Empty A+ plan - Turkey logic would NOT trigger")
                            
                    except json.JSONDecodeError as e:
                        print(f"❌ A+ plan JSON parsing failed: {e}")
                        print(f"📄 A+ plan JSON: {aplus_json[:500]}...")
                else:
                    print("❌ Could not extract A+ plan from response")
                    
            else:
                print("❌ No A+ Content Plan in AI response!")
                print(f"📄 Response preview: {ai_content[:500]}...")
                
        except Exception as ai_error:
            print(f"❌ AI call failed: {ai_error}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_aplus_plan_extraction()