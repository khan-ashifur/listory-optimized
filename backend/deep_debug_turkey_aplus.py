"""
DEEP DEBUG: Turkey A+ Content Generation
Trace exact flow and find the root cause of JSON parsing failure
"""

import os
import sys
import django
import json
import re

# Add backend to path
backend_path = os.path.join(os.getcwd())
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

def capture_raw_ai_response():
    """Capture and analyze the raw AI response for Turkey"""
    print("\n" + "="*80)
    print("🔍 DEEP DEBUG: TURKEY A+ CONTENT GENERATION")
    print("="*80)
    
    # Get Turkey product
    turkey_product = Product.objects.filter(marketplace='tr').first()
    if not turkey_product:
        print("❌ No Turkey product found")
        return
    
    print(f"✅ Turkey Product: {turkey_product.name} (ID: {turkey_product.id})")
    
    # Monkey patch the service to capture raw response
    service = ListingGeneratorService()
    
    # Store original method
    original_method = None
    captured_response = None
    
    # Find the actual method that makes the OpenAI call
    import openai
    original_create = openai.ChatCompletion.create if hasattr(openai, 'ChatCompletion') else None
    
    if hasattr(openai, 'OpenAI'):
        # New OpenAI client
        original_client_create = None
        
        def capture_openai_response(*args, **kwargs):
            nonlocal captured_response
            try:
                # Try to capture from the new client
                if hasattr(service, 'client') and service.client:
                    original_chat_create = service.client.chat.completions.create
                    
                    def capture_chat(*chat_args, **chat_kwargs):
                        nonlocal captured_response
                        result = original_chat_create(*chat_args, **chat_kwargs)
                        captured_response = result.choices[0].message.content if result.choices else ""
                        return result
                    
                    service.client.chat.completions.create = capture_chat
                    
                return service.generate_listing(turkey_product.id, platform='amazon')
            except Exception as e:
                print(f"❌ Capture error: {e}")
                return None
    
    # Generate listing and capture response
    print("\n🤖 Generating Turkey listing and capturing raw AI response...")
    
    try:
        listing = capture_openai_response()
        
        if captured_response:
            print(f"\n📊 RAW AI RESPONSE CAPTURED:")
            print(f"   Length: {len(captured_response)} characters")
            
            # Save full response to file for analysis
            with open('turkey_raw_ai_response.json', 'w', encoding='utf-8') as f:
                f.write(captured_response)
            print("✅ Full response saved to: turkey_raw_ai_response.json")
            
            # Find JSON boundaries
            start_idx = captured_response.find('{')
            end_idx = captured_response.rfind('}')
            
            if start_idx >= 0 and end_idx >= 0:
                json_content = captured_response[start_idx:end_idx + 1]
                print(f"\n📋 JSON EXTRACTION:")
                print(f"   JSON start: character {start_idx}")
                print(f"   JSON end: character {end_idx}")
                print(f"   JSON length: {len(json_content)} characters")
                
                # Analyze JSON structure
                analyze_json_structure(json_content)
                
                # Check for aPlusContentPlan specifically
                if '"aPlusContentPlan":' in json_content:
                    print("\n✅ aPlusContentPlan found in JSON")
                    analyze_aplus_content_plan(json_content)
                else:
                    print("\n❌ aPlusContentPlan NOT found in JSON")
                
            else:
                print("\n❌ No valid JSON structure found")
        else:
            print("\n❌ Failed to capture AI response")
        
        return listing, captured_response
        
    except Exception as e:
        print(f"\n❌ Error in deep debug: {e}")
        import traceback
        traceback.print_exc()
        return None, None

def analyze_json_structure(json_content):
    """Analyze the JSON structure to find parsing issues"""
    print("\n🔍 JSON STRUCTURE ANALYSIS:")
    
    # Check for common JSON issues
    issues = []
    
    # 1. Unmatched braces
    open_braces = json_content.count('{')
    close_braces = json_content.count('}')
    if open_braces != close_braces:
        issues.append(f"Unmatched braces: {open_braces} open, {close_braces} close")
    
    # 2. Unmatched brackets
    open_brackets = json_content.count('[')
    close_brackets = json_content.count(']')
    if open_brackets != close_brackets:
        issues.append(f"Unmatched brackets: {open_brackets} open, {close_brackets} close")
    
    # 3. Check for trailing commas
    trailing_comma_pattern = r',\s*[}\]]'
    trailing_commas = re.findall(trailing_comma_pattern, json_content)
    if trailing_commas:
        issues.append(f"Trailing commas found: {len(trailing_commas)} instances")
    
    # 4. Check for unescaped quotes in strings
    # Look for patterns like "text "word" text" which should be "text 'word' text"
    quote_issues = re.findall(r'"[^"]*"[^"]*"[^"]*":', json_content)
    if quote_issues:
        issues.append(f"Potential quote issues: {len(quote_issues)} instances")
    
    # 5. Check for Turkish characters causing issues
    turkish_chars = ['ğ', 'ı', 'ş', 'ç', 'ü', 'ö', 'Ğ', 'I', 'Ş', 'Ç', 'Ü', 'Ö']
    turkish_count = sum(json_content.count(char) for char in turkish_chars)
    print(f"   Turkish characters: {turkish_count} found")
    
    if issues:
        print(f"   ❌ ISSUES FOUND:")
        for issue in issues:
            print(f"      - {issue}")
    else:
        print(f"   ✅ Basic structure looks good")
    
    # Try to parse and get specific error
    try:
        parsed = json.loads(json_content)
        print(f"   ✅ JSON parsing successful!")
        return parsed
    except json.JSONDecodeError as e:
        print(f"   ❌ JSON parsing failed: {e}")
        print(f"   Error at line {e.lineno}, column {e.colno}")
        
        # Show context around error
        lines = json_content.split('\n')
        if e.lineno <= len(lines):
            error_line = lines[e.lineno - 1] if e.lineno > 0 else ""
            print(f"   Error line: {error_line}")
            
            # Show context
            start_line = max(0, e.lineno - 3)
            end_line = min(len(lines), e.lineno + 2)
            print(f"   Context:")
            for i in range(start_line, end_line):
                marker = ">>> " if i == e.lineno - 1 else "    "
                print(f"   {marker}{i+1:3d}: {lines[i]}")
        
        return None

def analyze_aplus_content_plan(json_content):
    """Analyze the aPlusContentPlan section specifically"""
    print("\n🎨 A+ CONTENT PLAN ANALYSIS:")
    
    # Extract aPlusContentPlan section
    aplus_start = json_content.find('"aPlusContentPlan":')
    if aplus_start == -1:
        print("   ❌ aPlusContentPlan not found")
        return
    
    # Find the end of aPlusContentPlan
    # Look for the opening brace after aPlusContentPlan
    brace_start = json_content.find('{', aplus_start)
    if brace_start == -1:
        print("   ❌ No opening brace found for aPlusContentPlan")
        return
    
    # Count braces to find matching closing brace
    brace_count = 0
    aplus_end = brace_start
    for i, char in enumerate(json_content[brace_start:], brace_start):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                aplus_end = i + 1
                break
    
    aplus_section = json_content[aplus_start:aplus_end]
    print(f"   aPlusContentPlan length: {len(aplus_section)} characters")
    
    # Check for all 8 sections
    required_sections = [
        'section1_hero', 'section2_features', 'section3_usage', 'section4_quality',
        'section5_guarantee', 'section6_social_proof', 'section7_comparison', 'section8_package'
    ]
    
    found_sections = []
    for section in required_sections:
        if f'"{section}":' in aplus_section:
            found_sections.append(section)
    
    print(f"   Sections found: {len(found_sections)}/8")
    for section in found_sections:
        print(f"      ✅ {section}")
    
    missing_sections = [s for s in required_sections if s not in found_sections]
    if missing_sections:
        print(f"   Missing sections:")
        for section in missing_sections:
            print(f"      ❌ {section}")
    
    # Check for English image descriptions
    english_count = aplus_section.count('ENGLISH:')
    print(f"   English image descriptions: {english_count}")
    
    # Save aPlusContentPlan to separate file for analysis
    with open('turkey_aplus_content_plan.txt', 'w', encoding='utf-8') as f:
        f.write(aplus_section)
    print("   ✅ aPlusContentPlan saved to: turkey_aplus_content_plan.txt")

def test_json_fix():
    """Test a potential JSON fix"""
    print("\n🔧 TESTING JSON FIX:")
    
    # Read the captured response
    try:
        with open('turkey_raw_ai_response.json', 'r', encoding='utf-8') as f:
            raw_response = f.read()
        
        # Apply fixes
        fixed_json = fix_json_issues(raw_response)
        
        if fixed_json:
            try:
                parsed = json.loads(fixed_json)
                print("   ✅ Fixed JSON parses successfully!")
                
                if 'aPlusContentPlan' in parsed:
                    aplus = parsed['aPlusContentPlan']
                    sections = [k for k in aplus.keys() if k.startswith('section')]
                    print(f"   ✅ A+ sections in fixed JSON: {len(sections)}")
                    
                    # Count English image descriptions
                    english_count = 0
                    for section_data in aplus.values():
                        if isinstance(section_data, dict) and 'imageDescription' in section_data:
                            if section_data['imageDescription'].startswith('ENGLISH:'):
                                english_count += 1
                    
                    print(f"   ✅ English image descriptions: {english_count}")
                    
                    if len(sections) >= 8 and english_count >= 6:
                        print("   🎉 SUCCESS! Turkey A+ content structure is PERFECT!")
                        return True
                
            except json.JSONDecodeError as e:
                print(f"   ❌ Fixed JSON still fails: {e}")
        
    except FileNotFoundError:
        print("   ❌ Raw response file not found - run capture first")
    
    return False

def fix_json_issues(json_content):
    """Apply common JSON fixes"""
    print("   🔧 Applying JSON fixes...")
    
    # Extract JSON part
    start_idx = json_content.find('{')
    end_idx = json_content.rfind('}')
    
    if start_idx < 0 or end_idx < 0:
        return None
    
    fixed = json_content[start_idx:end_idx + 1]
    
    # Fix 1: Remove trailing commas
    fixed = re.sub(r',(\s*[}\]])', r'\1', fixed)
    
    # Fix 2: Fix unescaped quotes in strings
    # This is complex - for now, try to fix common patterns
    fixed = re.sub(r'": "([^"]*)"([^"]*)"([^"]*)"', r'": "\1\'\2\'\3"', fixed)
    
    # Fix 3: Ensure proper string termination
    # Look for unterminated strings and try to fix them
    
    print(f"   ✅ Applied fixes, new length: {len(fixed)}")
    return fixed

if __name__ == "__main__":
    print("🇹🇷 DEEP DEBUG: TURKEY A+ CONTENT GENERATION")
    print("="*80)
    
    # Step 1: Capture raw response
    listing, raw_response = capture_raw_ai_response()
    
    # Step 2: Test JSON fix
    if raw_response:
        success = test_json_fix()
        
        if success:
            print("\n🎉 SUCCESS! Turkey A+ content issue SOLVED!")
        else:
            print("\n🔧 Additional fixes needed - check debug files for details")
    
    print("\n📁 Debug files created:")
    print("   - turkey_raw_ai_response.json (full AI response)")
    print("   - turkey_aplus_content_plan.txt (A+ content section)")
    print("\n💡 Next: Implement the fixes in the main service")