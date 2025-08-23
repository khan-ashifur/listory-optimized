import os, sys, django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User
import json
from openai import OpenAI

print('🔍 DEBUG: CHECKING WHAT AI ACTUALLY RETURNS FOR WALMART')
print('=' * 60)

# Create a test product
user, created = User.objects.get_or_create(username='walmart_ai_debug')

product = Product.objects.create(
    user=user,
    name='Gaming Headset Pro',
    brand_name='AudioTech',
    target_platform='walmart',
    marketplace='walmart_usa',
    marketplace_language='en-us',
    price=149.99,
    occasion='christmas',
    brand_tone='luxury',
    categories='Electronics > Gaming > Audio',
    description='Premium gaming headset with surround sound',
    features='7.1 Surround Sound\nNoise Cancellation\n50mm Drivers'
)

# Get OpenAI client
api_key = os.environ.get('OPENAI_API_KEY')
if not api_key:
    from django.conf import settings
    api_key = settings.OPENAI_API_KEY

client = OpenAI(api_key=api_key)

# Build the EXACT prompt that services.py uses
prompt = f"""Create a professional Walmart listing for this product. Return ONLY valid JSON with no extra text.


PRODUCT: {product.name}
BRAND: {product.brand_name}
DESCRIPTION: {product.description}  
FEATURES: {product.features}
PRICE: ${product.price}
SPECIAL OCCASION: christmas

Requirements:
- Title: Under 100 characters with brand and key benefit
- Features: Exactly 5-7 bullet points, max 80 characters each
- Description: 200-250 words, professional tone, no generic templates
- Keywords: 20 diverse SEO terms covering primary, long-tail, technical, brand, competitive, and demographic terms
- Include specific measurements and technical details

{{
  "product_title": "Professional title under 100 chars with brand and benefit",
  "key_features": [
    "Technical detail with measurement (under 80 chars)",
    "Certification or safety standard included",
    "Performance metric with specific numbers",
    "Material advantage or technology feature",
    "Compatibility or capacity specification",
    "Design or convenience benefit",
    "Warranty or reliability information"
  ],
  "description": "Write 200-250 word professional description focusing on technical advantages, performance benefits, and product superiority. Include specific details about materials, certifications, and real-world performance. Avoid generic templates.",
  "product_type": "Specific product category (e.g., Gaming Headset, Kitchen Knife, Bluetooth Speaker)",
  "attributes": {{
    "color": "Primary color",
    "size": "Dimensions or size",
    "material": "Primary material",
    "brand": "{product.brand_name}",
    "model": "Model name or number",
    "price": "{product.price}"
  }},
  "specifications": {{
    "weight": "Product weight",
    "dimensions": "L x W x H measurements",
    "power": "Power requirements if applicable",
    "compatibility": "Compatible devices/systems",
    "warranty": "Warranty period",
    "certification": "Safety certifications"
  }},
  "seo_keywords": [
    "primary keyword 1",
    "primary keyword 2",
    "primary keyword 3", 
    "long tail benefit phrase 1",
    "long tail benefit phrase 2",
    "problem solving phrase 1",
    "problem solving phrase 2",
    "technical specification term 1",
    "technical specification term 2",
    "brand specific term 1",
    "brand specific term 2",
    "category keyword 1",
    "category keyword 2",
    "comparison vs competitor keyword",
    "use case specific keyword",
    "feature specific keyword",
    "price range keyword",
    "quality indicator keyword",
    "seasonal/trending keyword",
    "demographic target keyword"
  ],
  "category_path": "Category > Subcategory > Product Type",
  "identifiers": {{
    "gtin_upc": "12-digit UPC code",
    "manufacturer_part": "Manufacturer part number",
    "sku_id": "SKU identifier"
  }},
  "shipping": {{
    "weight": "Weight with unit (e.g., 2.5 lbs)",
    "dimensions": "L x W x H in inches (e.g., 12 x 8 x 4 inches)"
  }},
  "warranty": {{
    "type": "Warranty type (manufacturer, extended)",
    "duration": "Warranty period (e.g., 1 year, lifetime)",
    "coverage": "What is covered"
  }},
  "compliance": {{
    "certifications": ["UL Listed", "FDA Approved", "CE Marked", "relevant safety certifications"]
  }},
  "assembly": {{
    "required": false,
    "time": "Assembly time if required",
    "difficulty": "Easy/Medium/Hard"
  }},
  "rich_media": {{
    "videos": ["video URL if available"],
    "additional_images": ["additional product images"]
  }}
}}"""

print('📝 PROMPT LENGTH:', len(prompt))
print('📝 CHECKING PROMPT HAS ALL FIELDS:')
print('   - category_path:', 'category_path' in prompt)
print('   - identifiers:', 'identifiers' in prompt)
print('   - shipping:', 'shipping' in prompt)
print('   - warranty:', 'warranty' in prompt)
print('   - compliance:', 'compliance' in prompt)

print('\n🚀 Calling OpenAI API...')
response = client.chat.completions.create(
    model='gpt-4o-mini',
    messages=[{'role': 'user', 'content': prompt}],
    temperature=1,
    max_tokens=3000
)

response_content = response.choices[0].message.content

print('\n📥 RAW AI RESPONSE:')
print('=' * 60)
print(response_content)
print('=' * 60)

# Try to parse the response
try:
    # Clean markdown if present
    if response_content.strip().startswith('```'):
        response_content = response_content.strip()
        if response_content.startswith('```json'):
            response_content = response_content[7:]
        elif response_content.startswith('```'):
            response_content = response_content[3:]
        if response_content.endswith('```'):
            response_content = response_content[:-3]
        response_content = response_content.strip()
    
    result = json.loads(response_content)
    
    print('\n✅ JSON PARSED SUCCESSFULLY')
    print('\n📊 FIELDS IN AI RESPONSE:')
    for key in sorted(result.keys()):
        value = result[key]
        if isinstance(value, dict):
            print(f'   ✅ {key}: dict with {len(value)} keys - {list(value.keys())[:3]}...')
        elif isinstance(value, list):
            print(f'   ✅ {key}: list with {len(value)} items')
        else:
            print(f'   ✅ {key}: {str(value)[:60]}...')
    
    # Check for missing fields
    expected_fields = [
        'product_title', 'description', 'key_features', 'product_type',
        'category_path', 'attributes', 'specifications', 'identifiers',
        'shipping', 'warranty', 'compliance', 'assembly', 'rich_media',
        'seo_keywords'
    ]
    
    missing = []
    for field in expected_fields:
        if field not in result:
            missing.append(field)
            print(f'   ❌ {field}: MISSING')
    
    if missing:
        print(f'\n❌ AI DID NOT RETURN THESE FIELDS: {missing}')
    else:
        print('\n✅ AI RETURNED ALL EXPECTED FIELDS!')
        
except json.JSONDecodeError as e:
    print(f'\n❌ JSON PARSE ERROR: {e}')
    print('Response was not valid JSON')

# Clean up
product.delete()
print('\n🧹 Debug completed')