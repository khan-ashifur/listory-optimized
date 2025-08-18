"""
Simple Turkey JSON Fix - No Emojis
"""

import re
import json

def fix_turkey_json(raw_response):
    """Fix Turkey JSON structure issues"""
    print("Fixing Turkey JSON structure...")
    
    # Extract JSON
    start_idx = raw_response.find('{')
    end_idx = raw_response.rfind('}')
    
    if start_idx < 0 or end_idx < 0:
        print("No JSON found")
        return None
    
    json_content = raw_response[start_idx:end_idx + 1]
    print(f"JSON length: {len(json_content)} characters")
    
    # Fix common issues
    fixed = json_content
    
    # Remove trailing commas
    fixed = re.sub(r',(\s*[}\]])', r'\\1', fixed)
    
    # Balance braces
    open_braces = fixed.count('{')
    close_braces = fixed.count('}')
    
    if open_braces > close_braces:
        missing = open_braces - close_braces
        fixed += '}' * missing
        print(f"Added {missing} missing braces")
    
    try:
        parsed = json.loads(fixed)
        print("SUCCESS: JSON parsed!")
        return parsed
    except Exception as e:
        print(f"Still failed: {e}")
        return None

def test_fix():
    """Test the fix"""
    try:
        with open('turkey_raw_ai_response.json', 'r', encoding='utf-8') as f:
            raw = f.read()
        
        result = fix_turkey_json(raw)
        
        if result and 'aPlusContentPlan' in result:
            aplus = result['aPlusContentPlan']
            sections = [k for k in aplus.keys() if k.startswith('section')]
            print(f"A+ sections found: {len(sections)}")
            
            english_count = 0
            for section_data in aplus.values():
                if isinstance(section_data, dict) and 'imageDescription' in section_data:
                    if 'ENGLISH:' in section_data['imageDescription']:
                        english_count += 1
            
            print(f"English descriptions: {english_count}")
            
            if len(sections) >= 8 and english_count >= 6:
                print("SUCCESS: Perfect A+ content structure!")
                return True
        
        print("Failed to extract A+ content properly")
        return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_fix()
    if success:
        print("Turkey JSON fix is ready for implementation!")
    else:
        print("Need more debugging")