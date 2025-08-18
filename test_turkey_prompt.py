"""
Test Turkey Prompt Generation
"""
import os
import sys
import django

# Set up Django
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService

def test_turkey_prompt():
    """Test if Turkey prompt contains A+ instructions"""
    try:
        # Get Turkey product
        product = Product.objects.filter(marketplace='tr').first()
        if not product:
            print("❌ No Turkey products found")
            return
        
        print(f"✅ Turkey Product: {product.name} (ID: {product.id})")
        print(f"   Marketplace: {product.marketplace}")
        
        # Check marketplace code logic
        marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
        print(f"   Marketplace code: '{marketplace_code}'")
        
        # Initialize service
        service = ListingGeneratorService()
        
        # Build the full prompt by looking at the generate_listing method structure
        marketplace_title_template = service.get_marketplace_title_format(product.marketplace, product.brand_name)
        
        # Check if Turkey title template exists
        if 'AMAZON TURKEY' in marketplace_title_template:
            print("✅ Turkey title template found!")
        else:
            print("❌ Turkey title template missing!")
            
        # Build a basic prompt to test A+ content inclusion
        test_prompt = f"""
You are an expert Amazon listing creator.

PRODUCT INFO:
- Name: {product.name}
- Brand: {product.brand_name}
- Description: {product.description}
- Marketplace: {product.marketplace}

{marketplace_title_template}

Please create a comprehensive listing including A+ content sections.
"""
        
        # Check for Turkey A+ instructions
        if "KRİTİK 8 BÖLÜM A+ İÇERİK KURALI" in test_prompt:
            print("✅ Turkey A+ instructions found in prompt!")
        else:
            print("❌ Turkey A+ instructions NOT in base prompt")
            print("🔍 Checking if they should be added later...")
            
        # Now check the actual generate method to see where A+ instructions are added
        print("\n🔍 Turkey prompt debugging complete.")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_turkey_prompt()