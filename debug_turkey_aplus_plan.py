"""
Debug Turkey A+ Plan Detection
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

def debug_turkey_aplus_plan():
    """Debug Turkey A+ plan creation"""
    try:
        print("🇹🇷 Debugging Turkey A+ Plan Creation...")
        
        # Get Turkey product
        product = Product.objects.filter(marketplace='tr').first()
        if not product:
            print("❌ No Turkey products found")
            return
        
        print(f"✅ Turkey Product: {product.name} (ID: {product.id})")
        
        # Check marketplace code
        marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
        print(f"📍 Marketplace code: '{marketplace_code}'")
        print(f"📍 Is Turkey? {marketplace_code == 'tr'}")
        
        # Initialize service and test the AI call
        service = ListingGeneratorService()
        
        # Test the AI prompt specifically for Turkey
        print("\n🤖 Testing AI prompt for Turkey...")
        
        # Create the prompt manually to see if it includes the Turkey A+ instructions
        prompt = service._create_listing_prompt(product, 'amazon')
        
        # Check if Turkey A+ instructions are in the prompt
        if "🚨🚨🚨 KRİTİK 8 BÖLÜM A+ İÇERİK KURALI" in prompt:
            print("✅ Turkey A+ instructions found in prompt!")
        else:
            print("❌ Turkey A+ instructions NOT found in prompt!")
            
        # Check for specific Turkey instruction parts
        if "TURKEY için MUTLAKA 8 comprehensive bölüm oluştur" in prompt:
            print("✅ Turkey 8-section requirement found!")
        else:
            print("❌ Turkey 8-section requirement NOT found!")
            
        # Test AI call directly
        print("\n🧠 Making AI call to test response...")
        try:
            response = service.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are an expert Amazon listing creator."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=16000,
                temperature=0.7
            )
            
            ai_content = response.choices[0].message.content
            print(f"📝 AI Response length: {len(ai_content)} characters")
            
            # Check if response contains A+ plan
            if "aPlusContentPlan" in ai_content:
                print("✅ A+ Content Plan found in AI response!")
                
                # Try to extract the plan
                import json
                try:
                    # Look for JSON in the response
                    start = ai_content.find('{')
                    end = ai_content.rfind('}') + 1
                    if start != -1 and end != -1:
                        json_str = ai_content[start:end]
                        parsed = json.loads(json_str)
                        
                        aplus_plan = parsed.get('aPlusContentPlan', {})
                        if aplus_plan:
                            print(f"🎯 A+ Plan sections: {len(aplus_plan)} found")
                            for section_key in aplus_plan.keys():
                                print(f"   - {section_key}")
                        else:
                            print("❌ A+ Plan is empty!")
                            
                except Exception as parse_error:
                    print(f"❌ JSON parsing failed: {parse_error}")
                    
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
    debug_turkey_aplus_plan()