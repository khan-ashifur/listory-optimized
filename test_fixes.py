import os, sys, django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from openai import OpenAI
from django.conf import settings
import json

print('🔧 TESTING LABELED BULLET POINTS AND KEYWORDS FIXES')
print('=' * 60)

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# Simple test prompt with new format
prompt = '''Generate a Walmart listing for Gaming Headset Pro. Return ONLY valid JSON:

{
  "product_title": "Gaming Headset Pro - Premium Audio Experience",
  "key_features": [
    "MANDATORY FORMAT: 'Feature Label - Description explanation' (exactly this format with space-hyphen-space)",
    "Example: 'Sound Quality - Crystal clear 7.1 surround sound technology'",
    "Example: 'Battery Life - Extended 30-hour playtime on single charge'",
    "Write exactly 5-7 COMPLETE bullet points in this labeled format"
  ],
  "seo_keywords": "Generate 75-100 RELEVANT search keywords that real shoppers would use. WALMART NEEDS EXTENSIVE KEYWORDS. Include: 1) Core product terms (15-20 keywords) 2) Function keywords (15-20 keywords) 3) Problem-solving terms (10-15 keywords) 4) Price-related terms (5-10 keywords) 5) Brand + product combinations (10-15 keywords) 6) Shopper intent keywords like 'best [product]', 'buy [product]', '[product] for sale' (10-15 keywords) 7) Alternative names and synonyms (10-15 keywords). Return comma-separated list of 75-100+ keywords ONLY."
}'''

try:
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        temperature=0.3,
        max_tokens=3000
    )
    
    content = response.choices[0].message.content.strip()
    
    # Clean markdown if present
    if content.startswith('```'):
        if content.startswith('```json'):
            content = content[7:]
        else:
            content = content[3:]
        if content.endswith('```'):
            content = content[:-3]
        content = content.strip()
    
    print('🔍 AI RESPONSE LENGTH:', len(content), 'characters')
    
    result = json.loads(content)
    
    print('✅ JSON PARSED SUCCESSFULLY')
    print()
    
    # Test bullet points labeling
    print('🔘 BULLET POINTS TEST:')
    features = result.get('key_features', [])
    labeled_count = 0
    for i, feature in enumerate(features):
        has_label = ' - ' in feature and not feature.startswith('MANDATORY') and not feature.startswith('Example')
        if has_label:
            labeled_count += 1
        print(f'  {i+1}. {feature}')
        if has_label:
            print('     ✅ HAS LABEL FORMAT')
        elif feature.startswith('MANDATORY') or feature.startswith('Example'):
            print('     ⚠️ INSTRUCTION (ignore)')
        else:
            print('     ❌ NO LABEL FORMAT')
    
    print(f'\\nLabeled bullets: {labeled_count} (excluding instructions)')
    
    # Test keywords count
    print()
    print('🔍 KEYWORDS TEST:')
    keywords = result.get('seo_keywords', '')
    if isinstance(keywords, str):
        keywords_list = [k.strip() for k in keywords.split(',')]
        keyword_count = len(keywords_list)
        print(f'  Keyword count: {keyword_count}')
        print(f'  Target: 75-100 keywords')
        if keyword_count >= 75:
            print('  ✅ KEYWORDS: FIXED!')
        elif keyword_count >= 50:
            print('  ⚠️ KEYWORDS: Good progress')
        else:
            print('  ❌ KEYWORDS: Still too few')
        
        print(f'  Sample: {keywords_list[:10]}')
    else:
        print('  ❌ Keywords not in string format')
    
    print()
    print('🎯 FIXES SUMMARY:')
    bullet_fix = labeled_count >= 3
    keyword_fix = keyword_count >= 75 if isinstance(keywords, str) else False
    
    print(f'  Bullet points fix: {"✅ WORKING" if bullet_fix else "❌ NEEDS WORK"}')
    print(f'  Keywords fix: {"✅ WORKING" if keyword_fix else "❌ NEEDS WORK"}')
    
    if bullet_fix and keyword_fix:
        print('  🎉 BOTH FIXES SUCCESSFUL!')
    else:
        print('  ⚠️ Some fixes need refinement')

except json.JSONDecodeError as e:
    print(f'❌ JSON ERROR: {e}')
    print('Raw response preview:', content[:500] if 'content' in locals() else 'No content')
except Exception as e:
    print(f'❌ OTHER ERROR: {e}')