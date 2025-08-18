import os
import sys
import django

# Set up the backend path correctly
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
import logging
import json

# Set up logging to see what's happening
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def debug_aplus_plan():
    try:
        # Find a Turkey product
        product = Product.objects.filter(marketplace='tr').first()
        if not product:
            # Update an existing product to Turkey marketplace
            product = Product.objects.first()
            product.marketplace = 'tr'
            product.save()
            print(f"✅ Updated product {product.id} to Turkey marketplace")

        print(f"🔍 Testing A+ plan generation for Turkey product: {product.id}")
        
        # Create service and test AI call
        service = ListingGeneratorService()
        
        # Make the AI call manually to inspect the response
        from apps.listings.market_occasions import get_occasions_data
        occasions_data = get_occasions_data('tr')
        
        # Build the prompt (simplified version)
        prompt = f"""Generate comprehensive Amazon listing content for:
Product: {product.name}
Brand: {product.brand_name}
Market: Turkey (tr)
Category: {getattr(product, 'product_category', 'general')}

CRITICAL: Include a comprehensive aPlusContentPlan with exactly 8 sections:
1. hero_section (or section1_hero)
2. features_section (or section2_features)  
3. usage_section (or section3_usage)
4. quality_section (or section4_quality)
5. guarantee_section (or section5_guarantee)
6. social_proof (or section6_social_proof)
7. comparison_section (or section7_comparison)
8. package_section (or section8_package)

Each section must have:
- title: Turkish title
- content: Detailed Turkish content (minimum 200 characters)
- keywords: Turkish keywords for this section
- imageStrategy: Detailed English image description

Return as valid JSON."""

        print(f"\n🔍 Making AI call...")
        response = service.client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=8000,
            temperature=0.7
        )
        
        raw_response = response.choices[0].message.content
        print(f"📊 AI Response length: {len(raw_response)} characters")
        
        # Try to parse JSON
        try:
            parsed = json.loads(raw_response)
            print(f"✅ JSON parsing successful!")
            
            # Check for A+ plan
            aplus_plan = parsed.get('aPlusContentPlan', {})
            if aplus_plan:
                print(f"✅ A+ Content Plan found with {len(aplus_plan)} sections:")
                for key, section in aplus_plan.items():
                    print(f"   - {key}: {section.get('title', 'No title')[:50]}...")
                    if 'content' in section:
                        print(f"     Content: {len(section['content'])} chars")
                    if 'imageStrategy' in section:
                        print(f"     Image: {section['imageStrategy'][:100]}...")
            else:
                print(f"❌ NO A+ Content Plan found in response!")
                print(f"Available keys: {list(parsed.keys())}")
                
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing failed: {e}")
            print(f"Raw response preview: {raw_response[:500]}...")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = debug_aplus_plan()