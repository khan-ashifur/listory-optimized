"""
Debug Missing A+ Content Strategy
"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def debug_aplus_content():
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='debug_aplus')
    
    print("🔍 DEBUGGING A+ CONTENT STRATEGY")
    print("="*60)
    
    # Create product for Turkey market
    product = Product.objects.create(
        user=test_user,
        name="Premium Wireless Headphones",
        description="High-quality wireless headphones",
        brand_name="SoundMaster",
        brand_tone="premium",
        target_platform="amazon",
        marketplace="tr",
        marketplace_language="tr",
        categories="Electronics/Audio/Headphones",
        features="Active Noise Cancellation, 40H Battery",
        target_audience="Turkish professionals",
        occasion="kurban_bayrami"
    )
    
    try:
        print("🔄 Generating listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            print("✅ Listing generated successfully!")
            
            # Check all A+ content related fields
            aplus_fields = [
                ('amazon_aplus_content', 'Full A+ Content HTML'),
                ('hero_title', 'Hero Title'),
                ('hero_content', 'Hero Content'),
                ('features', 'Features'),
                ('trust_builders', 'Trust Builders'),
                ('faqs', 'FAQs')
            ]
            
            print(f"\n📊 A+ CONTENT FIELDS STATUS:")
            for field_name, description in aplus_fields:
                if hasattr(listing, field_name):
                    field_value = getattr(listing, field_name)
                    if field_value:
                        print(f"✅ {description}: {len(str(field_value))} characters")
                        if field_name == 'amazon_aplus_content':
                            # Show preview of A+ content
                            preview = str(field_value)[:200]
                            print(f"   Preview: {preview}...")
                    else:
                        print(f"❌ {description}: Empty/None")
                else:
                    print(f"❌ {description}: Field not found")
            
            # Check if A+ content has the strategy section
            if listing.amazon_aplus_content:
                aplus_html = listing.amazon_aplus_content
                
                # Look for strategy-related content
                strategy_indicators = [
                    'Complete A+ Content Strategy',
                    'A+ Content Suggestions', 
                    'Professional Amazon A+ content',
                    'AI-Generated Briefs',
                    'Design Guidelines',
                    'Ready for Production'
                ]
                
                print(f"\n🎯 A+ STRATEGY SECTION CHECK:")
                strategy_found = []
                for indicator in strategy_indicators:
                    if indicator in aplus_html:
                        strategy_found.append(indicator)
                        print(f"✅ Found: {indicator}")
                
                if not strategy_found:
                    print("❌ No strategy section indicators found!")
                    print("🔍 Looking for any strategy-like content...")
                    
                    # Look for broader patterns
                    broad_patterns = ['strategy', 'Strategy', 'suggestions', 'Suggestions', 'briefs', 'Briefs']
                    for pattern in broad_patterns:
                        if pattern in aplus_html:
                            print(f"🔍 Found pattern: {pattern}")
                
                # Check HTML structure
                if '<div class="aplus-section' in aplus_html:
                    import re
                    sections = re.findall(r'<div class="aplus-section[^>]*>', aplus_html)
                    print(f"\n📋 A+ SECTIONS FOUND: {len(sections)}")
                else:
                    print(f"\n❌ No A+ sections found in HTML structure")
                    
        else:
            print("❌ No listing generated")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        product.delete()

if __name__ == "__main__":
    debug_aplus_content()