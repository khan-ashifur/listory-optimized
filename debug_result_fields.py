"""
Debug what fields are in the AI result for international markets
"""

import os
import sys
import django
import json

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

print("🔍 CHECKING AI RESULT STRUCTURE")
print("="*60)

# Test what the InternationalContentExtractor returns
from apps.listings.international_content_extractor import InternationalContentExtractor

# Sample AI response (from logs)
sample_response = '''
{
  "productTitle": "N-GEN Handventilator mit Wasserspray",
  "bulletPoints": ["Test bullet 1", "Test bullet 2"],
  "productDescription": "Test description",
  "seoKeywords": {"primary": ["test"], "secondary": ["test2"]},
  "backendKeywords": "test keywords",
  "aPlusContentPlan": {
    "section1_hero": {
      "title": "Hero Title Test",
      "content": "Hero Content Test",
      "keywords": ["hero", "test"],
      "imageDescription": "Hero image"
    },
    "section2_features": {
      "title": "Features Title",
      "content": "Features Content",
      "features": ["Feature 1", "Feature 2"]
    }
  },
  "brandSummary": "Brand summary test",
  "whatsInBox": ["Item 1", "Item 2"],
  "trustBuilders": ["Trust 1", "Trust 2"],
  "faqs": ["FAQ 1", "FAQ 2"],
  "socialProof": "Social proof test",
  "guarantee": "Guarantee test"
}
'''

extractor = InternationalContentExtractor()
result = extractor.extract_international_content(sample_response, "de")

if result:
    print("✅ Extraction successful!")
    print(f"\n📋 FIELDS IN RESULT:")
    for key in result.keys():
        value = result[key]
        if isinstance(value, dict):
            print(f"  {key}: dict with {len(value)} keys")
            for subkey in value.keys():
                print(f"    - {subkey}")
        elif isinstance(value, list):
            print(f"  {key}: list with {len(value)} items")
        elif isinstance(value, str):
            print(f"  {key}: string ({len(value)} chars)")
        else:
            print(f"  {key}: {type(value)}")
    
    # Check A+ content plan structure
    aplus_plan = result.get('aPlusContentPlan', {})
    print(f"\n🖼️ A+ CONTENT PLAN STRUCTURE:")
    if aplus_plan:
        print(f"  Keys in aPlusContentPlan: {list(aplus_plan.keys())}")
        
        # Check for section1_hero
        if 'section1_hero' in aplus_plan:
            hero = aplus_plan['section1_hero']
            print(f"\n  ✅ section1_hero found:")
            print(f"     title: {hero.get('title', 'NOT FOUND')}")
            print(f"     content: {hero.get('content', 'NOT FOUND')[:50]}...")
        else:
            print(f"\n  ❌ section1_hero NOT found")
            
        # Check for heroSection (alternative key)
        if 'heroSection' in aplus_plan:
            print(f"  ✅ heroSection found")
        else:
            print(f"  ❌ heroSection NOT found")
    else:
        print("  ❌ aPlusContentPlan is empty")
    
    # Check direct fields
    print(f"\n📦 DIRECT CONTENT FIELDS:")
    print(f"  whatsInBox: {result.get('whatsInBox', 'NOT FOUND')}")
    print(f"  trustBuilders: {result.get('trustBuilders', 'NOT FOUND')}")
    print(f"  faqs: {result.get('faqs', 'NOT FOUND')}")
    print(f"  brandSummary: {result.get('brandSummary', 'NOT FOUND')[:50] if result.get('brandSummary') else 'NOT FOUND'}...")
    
else:
    print("❌ Extraction failed!")