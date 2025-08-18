"""
Fix Turkey A+ Content Generation
Analyze the JSON parsing issue and ensure proper 8-section A+ content generation
"""

import os
import sys
import django
import json

# Add backend to path
backend_path = os.path.join(os.getcwd())
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def debug_turkey_json_parsing():
    """Debug the JSON parsing issue for Turkey"""
    print("\n" + "="*80)
    print("🔍 DEBUGGING TURKEY JSON PARSING ISSUE")
    print("="*80)
    
    # Create a test product for Turkey
    turkey_product = Product.objects.filter(marketplace='tr').first()
    if not turkey_product:
        print("Creating Turkey test product...")
        turkey_product = Product.objects.create(
            name="Premium Wireless Bluetooth Headphones",
            brand_name="TurkAudio",
            marketplace="tr",
            brand_tone="professional yet warm",
            categories="Electronics, Audio, Headphones",
            occasion="work, travel, family time",
            search_terms="bluetooth kulaklik kablosuz muzik ses"
        )
    
    print(f"✅ Turkey Product: {turkey_product.name} (ID: {turkey_product.id})")
    
    # Get the service and check what's happening in the AI call
    service = ListingGeneratorService()
    
    # Turkey marketplace should use Turkish (tr)
    print(f"🌍 Marketplace: {turkey_product.marketplace}")
    print(f"📝 Generating Turkey listing to check A+ content...")
    
    # Now let's try to generate and capture the raw AI response
    print("\n🤖 Generating Turkey listing to capture raw AI response...")
    
    try:
        # We'll patch the service to capture the raw response
        original_call = service._call_openai_api
        captured_response = None
        
        def capture_response(*args, **kwargs):
            nonlocal captured_response
            result = original_call(*args, **kwargs)
            captured_response = result
            return result
        
        service._call_openai_api = capture_response
        
        # Generate the listing
        listing = service.generate_listing(turkey_product.id, platform='amazon')
        
        # Restore original method
        service._call_openai_api = original_call
        
        print("\n✅ Listing generated successfully!")
        print(f"📊 A+ Content sections: {listing.amazon_aplus_content.count('aplus-section-card') if listing.amazon_aplus_content else 0}")
        
        # Now examine what went wrong with the JSON
        if captured_response:
            print("\n🔍 ANALYZING RAW AI RESPONSE:")
            response_text = captured_response.choices[0].message.content if captured_response.choices else ""
            
            # Look for JSON structure issues
            if '{' in response_text and '}' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                json_part = response_text[start:end]
                
                print(f"📏 JSON length: {len(json_part)} characters")
                
                # Check for common issues
                issues = []
                if '"aPlusContentPlan":' not in json_part:
                    issues.append("❌ Missing aPlusContentPlan")
                elif '"section8_package":' not in json_part:
                    issues.append("❌ Missing section8_package (not all 8 sections)")
                
                if 'ENGLISH:' not in json_part:
                    issues.append("❌ Missing ENGLISH: image descriptions")
                
                # Count sections
                section_count = 0
                for i in range(1, 9):
                    if f'"section{i}_' in json_part:
                        section_count += 1
                
                print(f"🔢 Sections found: {section_count}/8")
                
                if issues:
                    print("\n⚠️ ISSUES FOUND:")
                    for issue in issues:
                        print(f"   {issue}")
                else:
                    print("\n✅ JSON structure looks good")
                
                # Try to parse and see what fails
                try:
                    parsed = json.loads(json_part)
                    print("✅ JSON parsing successful!")
                    
                    if 'aPlusContentPlan' in parsed:
                        aplus = parsed['aPlusContentPlan']
                        sections = [k for k in aplus.keys() if k.startswith('section')]
                        print(f"✅ A+ sections in parsed JSON: {len(sections)}")
                        for section in sections:
                            print(f"   - {section}")
                    else:
                        print("❌ No aPlusContentPlan in parsed JSON")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing failed: {e}")
                    
                    # Find the problematic area
                    error_pos = getattr(e, 'pos', 0)
                    context_start = max(0, error_pos - 100)
                    context_end = min(len(json_part), error_pos + 100)
                    context = json_part[context_start:context_end]
                    
                    print(f"🔍 Error context around position {error_pos}:")
                    print(f"   ...{context}...")
                    
                    # Common fixes needed
                    fixes_needed = []
                    if '",\n    "' in json_part and '",\n    "' in json_part[error_pos-50:error_pos+50]:
                        fixes_needed.append("Fix trailing commas")
                    if '\\"' in json_part[error_pos-50:error_pos+50]:
                        fixes_needed.append("Fix escaped quotes in strings")
                    if '"keywords": [' in json_part and context.count('[') != context.count(']'):
                        fixes_needed.append("Fix unmatched brackets in keywords array")
                    
                    if fixes_needed:
                        print("🔧 Suggested fixes:")
                        for fix in fixes_needed:
                            print(f"   - {fix}")
            
            else:
                print("❌ No JSON structure found in AI response")
        
        return listing
        
    except Exception as e:
        print(f"❌ Error generating listing: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_turkey_aplus_fix():
    """Test the fixed Turkey A+ content generation"""
    print("\n" + "="*80)
    print("🔧 TESTING TURKEY A+ CONTENT FIX")
    print("="*80)
    
    listing = debug_turkey_json_parsing()
    
    if listing and listing.amazon_aplus_content:
        aplus = listing.amazon_aplus_content
        sections = aplus.count('aplus-section-card')
        english_descriptions = aplus.count('ENGLISH:')
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"   A+ Sections: {sections}")
        print(f"   English descriptions: {english_descriptions}")
        print(f"   Total content length: {len(aplus)} characters")
        
        # Check if we have the required structure
        if sections >= 8 and english_descriptions >= 6:
            print("\n✅ SUCCESS! Turkey A+ content matches Mexico quality!")
            print("✅ Ready to beat Helium 10, Jasper AI, CopyMonkey")
        else:
            print(f"\n⚠️ Still needs improvement:")
            if sections < 8:
                print(f"   - Need {8-sections} more A+ sections")
            if english_descriptions < 6:
                print(f"   - Need {6-english_descriptions} more English image descriptions")
    else:
        print("\n❌ A+ content generation still failing")
        print("🔧 Additional debugging needed")

if __name__ == "__main__":
    test_turkey_aplus_fix()