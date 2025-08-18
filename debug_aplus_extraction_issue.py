"""
Debug A+ content extraction issue - why are we getting 0 sections?
"""

import os
import sys
import django
import json

# Add the project path and configure Django
project_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(project_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

def debug_aplus_extraction_issue():
    """Debug why A+ content shows 0 sections instead of 8"""
    
    try:
        from apps.listings.services import ListingGeneratorService
        from apps.core.models import Product
        from django.contrib.auth.models import User

        print("🔍 DEBUGGING A+ CONTENT EXTRACTION ISSUE")
        print("=" * 60)
        
        user, _ = User.objects.get_or_create(
            username='debug_aplus_issue', 
            defaults={'email': 'test@test.com'}
        )
        
        product = Product.objects.create(
            user=user,
            name='テストイヤホン',
            description='高品質テスト',
            brand_name='TestBrand',
            marketplace='jp',
            marketplace_language='ja'
        )
        
        service = ListingGeneratorService()
        
        # Capture the OpenAI response to see what's actually being generated
        original_call_openai = service.client.chat.completions.create if hasattr(service, 'client') else None
        captured_response = None
        
        def capture_openai_response(*args, **kwargs):
            nonlocal captured_response
            response = original_call_openai(*args, **kwargs)
            if hasattr(response, 'choices') and response.choices:
                captured_response = response.choices[0].message.content
            return response
        
        if original_call_openai:
            service.client.chat.completions.create = capture_openai_response
        
        result = service.generate_listing(product.id, 'amazon')
        
        if captured_response:
            print(f"📤 RAW OPENAI RESPONSE ({len(captured_response)} chars):")
            print(f"   Preview: {captured_response[:200]}...")
            
            # Check if aPlusContentPlan exists in raw response
            if '"aPlusContentPlan"' in captured_response:
                print("✅ aPlusContentPlan found in raw response")
                
                # Try to extract it manually
                try:
                    # Find the start and end of aPlusContentPlan
                    start = captured_response.find('"aPlusContentPlan":')
                    if start != -1:
                        # Find the opening brace
                        brace_start = captured_response.find('{', start)
                        if brace_start != -1:
                            # Count braces to find the end
                            brace_count = 1
                            pos = brace_start + 1
                            while pos < len(captured_response) and brace_count > 0:
                                if captured_response[pos] == '{':
                                    brace_count += 1
                                elif captured_response[pos] == '}':
                                    brace_count -= 1
                                pos += 1
                            
                            if brace_count == 0:
                                aplus_json = captured_response[brace_start:pos]
                                print(f"📋 Extracted aPlusContentPlan ({len(aplus_json)} chars):")
                                print(f"   {aplus_json[:300]}...")
                                
                                # Try to parse it
                                try:
                                    aplus_data = json.loads(aplus_json)
                                    section_count = len([k for k in aplus_data.keys() if k.startswith('section')])
                                    print(f"✅ Successfully parsed! Found {section_count} sections:")
                                    for key in sorted(aplus_data.keys()):
                                        if key.startswith('section'):
                                            section = aplus_data[key]
                                            title = section.get('title', 'No title')
                                            content_len = len(section.get('content', ''))
                                            print(f"   {key}: {title[:50]}... ({content_len} chars)")
                                except json.JSONDecodeError as e:
                                    print(f"❌ JSON parse error: {e}")
                            else:
                                print("❌ Could not find complete aPlusContentPlan structure")
                        else:
                            print("❌ Could not find opening brace for aPlusContentPlan")
                    else:
                        print("❌ Could not find aPlusContentPlan start")
                        
                except Exception as e:
                    print(f"❌ Manual extraction failed: {e}")
            else:
                print("❌ aPlusContentPlan not found in raw response")
        
        if result:
            aplus_content = getattr(result, 'amazon_aplus_content', '')
            print(f"\\n📊 FINAL A+ CONTENT ANALYSIS:")
            print(f"   Length: {len(aplus_content)} characters")
            
            if '<h3>' in aplus_content:
                sections = aplus_content.split('<h3>')[1:]
                print(f"   Sections found: {len(sections)}")
                for i, section in enumerate(sections[:3], 1):
                    title = section.split('</h3>')[0] if '</h3>' in section else section[:30]
                    print(f"   Section {i}: {title}...")
            else:
                print("   ❌ No <h3> sections found")
                print(f"   Content type: {'HTML template' if '<div class=' in aplus_content else 'Plain text'}")
                print(f"   Preview: {aplus_content[:200]}...")
        
        product.delete()
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    debug_aplus_extraction_issue()