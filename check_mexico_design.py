"""
Check Mexico A+ Design Structure
"""
import os, sys, django

# Set up Django
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)
os.chdir(backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing
from apps.core.models import Product

def check_mexico_design():
    try:
        print("🇲🇽 CHECKING MEXICO A+ DESIGN STRUCTURE")
        print("=" * 60)
        
        # Find a Mexico product
        mexico_product = Product.objects.filter(marketplace='mx').first()
        if not mexico_product:
            print("❌ No Mexico products found")
            return
            
        print(f"✅ Found Mexico product: {mexico_product.id} - {mexico_product.name}")
        
        # Find Mexico listing
        mexico_listing = GeneratedListing.objects.filter(product=mexico_product).order_by('-created_at').first()
        if not mexico_listing:
            print("❌ No Mexico listings found")
            return
            
        print(f"✅ Found Mexico listing: {mexico_listing.id}")
        
        aplus_content = mexico_listing.amazon_aplus_content
        print(f"📏 Mexico A+ Length: {len(aplus_content)} characters")
        
        print(f"\n📋 MEXICO A+ DESIGN STRUCTURE:")
        print("=" * 60)
        
        # Show first 2000 characters to see structure
        print(aplus_content[:2000])
        print("...")
        
        # Check for specific patterns
        print(f"\n🔍 DESIGN PATTERN ANALYSIS:")
        print(f"   - Contains 'aplus-section': {'aplus-section' in aplus_content}")
        print(f"   - Contains section cards: {'section-card' in aplus_content}")
        print(f"   - Contains grid layout: {'grid' in aplus_content.lower()}")
        print(f"   - Contains hero section: {'hero' in aplus_content.lower()}")
        print(f"   - Contains feature cards: {'feature' in aplus_content.lower()}")
        
        return aplus_content
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    check_mexico_design()