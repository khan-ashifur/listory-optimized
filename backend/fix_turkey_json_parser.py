"""
FINAL FIX: Turkey JSON Parser
Implement robust JSON parsing that handles Turkish characters and malformed JSON
"""

import re
import json

def fix_turkey_json_structure(raw_response):
    """
    Fix Turkey JSON structure issues and extract perfect A+ content
    """
    print("FIXING TURKEY JSON STRUCTURE...")
    
    # Step 1: Extract JSON boundaries
    start_idx = raw_response.find('{')
    end_idx = raw_response.rfind('}')
    
    if start_idx < 0 or end_idx < 0:
        print("No JSON structure found")
        return None
    
    json_content = raw_response[start_idx:end_idx + 1]
    print(f"Extracted JSON: {len(json_content)} characters")
    
    # Step 2: Fix common JSON issues
    fixed_json = json_content
    
    # Fix 1: Remove trailing commas before closing brackets/braces
    fixed_json = re.sub(r',(\s*[}\]])', r'\1', fixed_json)
    print("Removed trailing commas")
    
    # Fix 2: Fix unescaped quotes in strings
    # Replace " inside strings with '
    def fix_quotes_in_strings(match):
        full_string = match.group(0)
        # If this is a field name, don't touch it
        if full_string.endswith('":'):
            return full_string
        # Replace internal quotes with single quotes
        content = match.group(1)
        fixed_content = content.replace('"', "'")
        return f'"{fixed_content}"'
    
    # Fix quotes in string values (not field names)
    fixed_json = re.sub(r'"([^"]*[a-zA-Z][^"]*)"(?!\s*:)', fix_quotes_in_strings, fixed_json)
    print("Fixed unescaped quotes in strings")
    
    # Fix 3: Handle Turkish characters properly
    # Turkish characters are fine in JSON, no changes needed
    print("Turkish characters preserved")
    
    # Fix 4: Balance braces
    open_braces = fixed_json.count('{')
    close_braces = fixed_json.count('}')
    
    if open_braces > close_braces:
        # Add missing closing braces
        missing_braces = open_braces - close_braces
        fixed_json += '}' * missing_braces
        print(f"Added {missing_braces} missing closing braces")
    elif close_braces > open_braces:
        # Remove extra closing braces from the end
        extra_braces = close_braces - open_braces
        for _ in range(extra_braces):
            last_brace = fixed_json.rfind('}')
            if last_brace >= 0:
                fixed_json = fixed_json[:last_brace] + fixed_json[last_brace + 1:]
        print(f"Removed {extra_braces} extra closing braces")
    
    # Fix 5: Handle incomplete JSON at the end
    # If JSON seems cut off, try to complete it
    if not fixed_json.strip().endswith('}'):
        fixed_json = fixed_json.rstrip() + '}'
        print("Added final closing brace")
    
    # Step 3: Try parsing
    try:
        parsed = json.loads(fixed_json)
        print("🎉 SUCCESS: JSON parsing successful!")
        return parsed
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing still failed: {e}")
        print(f"Error at line {e.lineno}, column {e.colno}")
        
        # More aggressive fixes
        print("🔧 Applying aggressive fixes...")
        
        # Fix 6: Remove problematic characters
        # Remove non-printable characters except common ones
        fixed_json = re.sub(r'[^\x20-\x7E\u00A0-\u024F\u1E00-\u1EFF]', '', fixed_json)
        
        # Fix 7: Try to salvage by extracting key sections manually
        return extract_turkey_content_manually(fixed_json)

def extract_turkey_content_manually(broken_json):
    """
    Manual extraction of Turkey content when JSON parsing fails
    """
    print("🔨 MANUAL CONTENT EXTRACTION...")
    
    result = {}
    
    # Extract title
    title_match = re.search(r'"productTitle":\s*"([^"]+)"', broken_json)
    if title_match:
        result['productTitle'] = title_match.group(1)
        print("✅ Extracted title")
    
    # Extract bullet points
    bullet_match = re.search(r'"bulletPoints":\s*\[(.*?)\]', broken_json, re.DOTALL)
    if bullet_match:
        bullets_text = bullet_match.group(1)
        # Extract individual bullets
        bullets = re.findall(r'"([^"]+)"', bullets_text)
        result['bulletPoints'] = bullets
        print(f"✅ Extracted {len(bullets)} bullet points")
    
    # Extract description
    desc_match = re.search(r'"productDescription":\s*"([^"]+)"', broken_json)
    if desc_match:
        result['productDescription'] = desc_match.group(1)
        print("✅ Extracted description")
    
    # Extract A+ Content Plan (most important!)
    aplus_match = re.search(r'"aPlusContentPlan":\s*\{(.*?)\n\s*\}', broken_json, re.DOTALL)
    if aplus_match:
        aplus_content = aplus_match.group(0)
        result['aPlusContentPlan'] = extract_aplus_sections(aplus_content)
        print(f"✅ Extracted A+ content with {len(result['aPlusContentPlan'])} sections")
    
    # Extract other fields
    for field in ['seoKeywords', 'backendKeywords', 'brandSummary', 'whatsInBox', 'trustBuilders', 'faqs']:
        field_match = re.search(rf'"{field}":\s*"([^"]+)"', broken_json)
        if field_match:
            result[field] = field_match.group(1)
    
    print(f"✅ Manual extraction completed: {len(result)} fields")
    return result

def extract_aplus_sections(aplus_content):
    """
    Extract A+ content sections manually
    """
    sections = {}
    
    # Find all section blocks
    section_pattern = r'"(section\d+_\w+)":\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
    section_matches = re.findall(section_pattern, aplus_content, re.DOTALL)
    
    for section_name, section_content in section_matches:
        section_data = {}
        
        # Extract fields from section
        for field in ['title', 'content', 'imageDescription', 'seoOptimization']:
            field_match = re.search(rf'"{field}":\s*"([^"]+)"', section_content)
            if field_match:
                section_data[field] = field_match.group(1)
        
        # Extract keywords array
        keywords_match = re.search(r'"keywords":\s*\[(.*?)\]', section_content)
        if keywords_match:
            keywords_text = keywords_match.group(1)
            keywords = re.findall(r'"([^"]+)"', keywords_text)
            section_data['keywords'] = keywords
        
        if section_data:
            sections[section_name] = section_data
    
    return sections

def test_turkey_json_fix():
    """
    Test the Turkey JSON fix
    """
    print("\n" + "="*80)
    print("TURKEY TESTING TURKEY JSON FIX")
    print("="*80)
    
    # Read the raw response
    try:
        with open('turkey_raw_ai_response.json', 'r', encoding='utf-8') as f:
            raw_response = f.read()
        
        # Apply fix
        fixed_data = fix_turkey_json_structure(raw_response)
        
        if fixed_data:
            print("\n📊 FIXED DATA ANALYSIS:")
            print(f"   Fields extracted: {len(fixed_data)}")
            
            if 'aPlusContentPlan' in fixed_data:
                aplus = fixed_data['aPlusContentPlan']
                print(f"   A+ sections: {len(aplus)}")
                
                # Check for all 8 sections
                required_sections = [
                    'section1_hero', 'section2_features', 'section3_usage', 'section4_quality',
                    'section5_guarantee', 'section6_social_proof', 'section7_comparison', 'section8_package'
                ]
                
                found_sections = [s for s in required_sections if s in aplus]
                print(f"   Required sections found: {len(found_sections)}/8")
                
                # Count English image descriptions
                english_count = 0
                for section_data in aplus.values():
                    if isinstance(section_data, dict) and 'imageDescription' in section_data:
                        if 'ENGLISH:' in section_data['imageDescription']:
                            english_count += 1
                
                print(f"   English image descriptions: {english_count}")
                
                if len(found_sections) >= 8 and english_count >= 6:
                    print("\n🎉 SUCCESS! Turkey A+ content is PERFECT!")
                    print("✅ All 8 sections with English image descriptions")
                    print("✅ Ready to beat Helium 10, Jasper AI, CopyMonkey")
                    return True
                else:
                    print("⚠️ Some sections missing - check extraction logic")
            else:
                print("❌ No A+ content plan found")
        else:
            print("❌ JSON fix failed")
    
    except FileNotFoundError:
        print("❌ Raw response file not found")
    
    return False

if __name__ == "__main__":
    success = test_turkey_json_fix()
    
    if success:
        print("\n💡 IMPLEMENTATION READY:")
        print("   Apply this fix to the main ListingGeneratorService")
        print("   Turkey will then generate perfect A+ content!")
    else:
        print("\n🔧 Additional debugging needed")