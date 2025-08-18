"""
Debug Turkey Marketplace Detection
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

def test_marketplace_detection():
    """Test if Turkey marketplace is being detected correctly"""
    try:
        print("🔍 Testing Turkey marketplace detection...")
        
        # Get Turkey product
        product = Product.objects.filter(marketplace='tr').first()
        if not product:
            print("❌ No Turkey products found")
            return
            
        print(f"✅ Turkey Product: {product.name}")
        print(f"   - ID: {product.id}")
        print(f"   - Marketplace: '{product.marketplace}'")
        print(f"   - Marketplace type: {type(product.marketplace)}")
        
        # Test marketplace code detection
        service = ListingGeneratorService()
        marketplace_code = service._get_marketplace_code(product.marketplace)
        print(f"   - Detected marketplace_code: '{marketplace_code}'")
        print(f"   - Marketplace code type: {type(marketplace_code)}")
        print(f"   - marketplace_code == 'tr': {marketplace_code == 'tr'}")
        
        # Test condition directly
        is_turkey = marketplace_code == 'tr'
        print(f"   - Is Turkey condition: {is_turkey}")
        
        return marketplace_code
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_marketplace_detection()