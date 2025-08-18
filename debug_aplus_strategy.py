import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory_backend.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product

# Create test product
product = Product.objects.create(
    name="Test Headphones",
    description="Test description",
    brand_name="TestBrand",
    marketplace="tr",
    marketplace_language="tr", 
    categories="electronics",
    price=40.00
)

# Generate listing
service = ListingGeneratorService()
result = service.generate_comprehensive_listing(product)

# Debug A+ content plan
print("🔍 DEBUGGING A+ CONTENT PLAN")
print("="*50)

if hasattr(result, 'amazon_aplus_content'):
    print(f"✅ A+ content exists: {len(result.amazon_aplus_content)} chars")
    
    # Check if strategy section is in the HTML
    if 'Overall A+ Strategy' in result.amazon_aplus_content:
        print("✅ Strategy section found in HTML")
        
        # Extract strategy content
        import re
        strategy_match = re.search(r'<h3[^>]*>Overall A\+ Strategy</h3>\s*<p[^>]*>(.*?)</p>', result.amazon_aplus_content, re.DOTALL)
        if strategy_match:
            strategy_content = strategy_match.group(1).strip()
            print(f"📝 Strategy content: {strategy_content}")
        else:
            print("❌ Strategy section HTML found but no content extracted")
    else:
        print("❌ Strategy section NOT found in HTML")
        
    # Check for strategy section in HTML more broadly
    if 'aplus-strategy-summary' in result.amazon_aplus_content:
        print("✅ Strategy CSS class found")
    else:
        print("❌ Strategy CSS class NOT found")
        
else:
    print("❌ No A+ content generated")

# Clean up
product.delete()