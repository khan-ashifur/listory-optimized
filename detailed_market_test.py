"""
Detailed Market Testing with Debug Information
"""

import os
import sys
import json
import django
from datetime import datetime

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService

def test_single_market(market_code):
    """Test a single market with detailed output"""
    
    print(f"\n{'='*60}")
    print(f"TESTING MARKET: {market_code.upper()}")
    print(f"{'='*60}")
    
    service = ListingGeneratorService()
    
    # Create test product
    from django.contrib.auth.models import User
    
    # Get or create a test user
    test_user, _ = User.objects.get_or_create(username='test_user')
    
    product = Product.objects.create(
        user=test_user,
        name="Premium Noise-Cancelling Bluetooth Headphones",
        description="Premium wireless headphones with active noise cancellation, 30-hour battery life, and superior sound quality. Perfect for travel, work, and daily commutes.",
        brand_name="AudioPro",
        brand_tone="professional",
        target_platform="amazon",
        marketplace=market_code,
        categories="Electronics/Audio/Headphones",
        features="Active Noise Cancellation, 30 Hour Battery, Bluetooth 5.3, Memory Foam Cushions, Foldable Design",
        target_audience="Professionals, Travelers, Music Enthusiasts",
        target_keywords="noise cancelling headphones, bluetooth headphones, wireless headphones, ANC headphones",
        seo_keywords="premium headphones, travel headphones, long battery headphones",
        long_tail_keywords="best noise cancelling headphones for travel, wireless headphones with 30 hour battery",
        faqs="Q: How long does the battery last? A: Up to 30 hours with ANC on.",
        whats_in_box="Headphones, USB-C cable, 3.5mm audio cable, Travel case, User manual"
    )
    
    try:
        # Define occasions to test based on market
        market_occasions = {
            'us': ['christmas', 'black_friday', 'general'],
            'fr': ['noel', 'black_friday', 'general'],
            'it': ['natale', 'black_friday', 'general'],
            'de': ['weihnachten', 'black_friday', 'general'],
            'es': ['navidad', 'black_friday', 'general']
        }
        
        # Test different brand tones
        brand_tones = ['professional', 'friendly', 'luxurious']
        
        for occasion in market_occasions.get(market_code, ['general']):
            for tone in brand_tones:
                print(f"\n Testing: {occasion.upper()} + {tone.upper()}")
                print("-" * 40)
                
                # Update product with occasion and save
                product.occasion = occasion
                product.brand_tone = tone
                product.marketplace = market_code
                product.save()
                
                # Generate listing
                result = service.generate_listing(
                    product_id=product.id,
                    platform='amazon'
                )
                
                # Check results
                if result:
                    # Parse the result (it's a GeneratedListing object)
                    title = result.title or ''
                    bullets = json.loads(result.bullet_points) if result.bullet_points else []
                    description = result.description or ''
                    backend_keywords = result.backend_keywords or ''
                    aplus_content = json.loads(result.aplus_content) if result.aplus_content else {}
                    
                    print(f"✅ Title: {len(title)} chars")
                    if title:
                        print(f"   Preview: {title[:100]}...")
                    
                    print(f"✅ Bullets: {len(bullets)} points")
                    if bullets:
                        print(f"   First bullet: {bullets[0][:100]}...")
                    
                    print(f"✅ Description: {len(description)} chars")
                    
                    print(f"✅ Backend Keywords: {len(backend_keywords.split(','))} keywords")
                    
                    print(f"✅ A+ Content: {len(aplus_content)} sections")
                    if aplus_content:
                        sections = list(aplus_content.keys())
                        print(f"   Sections: {', '.join(sections[:3])}...")
                    
                    # Check for local occasions in content
                    full_text = f"{title} {' '.join(bullets)} {description}"
                    
                    # Check for proper language markers
                    if market_code == 'de':
                        has_umlauts = any(char in full_text for char in ['ä', 'ö', 'ü', 'ß'])
                        print(f"🔤 German Umlauts: {'✅ YES' if has_umlauts else '❌ NO'}")
                        
                    elif market_code == 'fr':
                        has_accents = any(char in full_text for char in ['é', 'è', 'à', 'ç'])
                        print(f"🔤 French Accents: {'✅ YES' if has_accents else '❌ NO'}")
                        
                    elif market_code == 'it':
                        has_accents = any(char in full_text for char in ['à', 'è', 'ù', 'ò'])
                        print(f"🔤 Italian Accents: {'✅ YES' if has_accents else '❌ NO'}")
                        
                    elif market_code == 'es':
                        has_accents = any(char in full_text for char in ['á', 'é', 'í', 'ó', 'ú', 'ñ'])
                        print(f"🔤 Spanish Accents: {'✅ YES' if has_accents else '❌ NO'}")
                    
                    # Save sample for analysis
                    filename = f"sample_{market_code}_{occasion}_{tone}.json"
                    sample_data = {
                        'title': title,
                        'bullet_points': bullets,
                        'description': description,
                        'backend_keywords': backend_keywords,
                        'aplus_content': aplus_content
                    }
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(sample_data, f, indent=2, ensure_ascii=False)
                    print(f"📁 Saved to: {filename}")
                    
                else:
                    print("❌ No result generated")
                    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        product.delete()
    
    print(f"\n{'='*60}")
    print(f"MARKET {market_code.upper()} TEST COMPLETE")
    print(f"{'='*60}")

# Main execution
if __name__ == "__main__":
    markets = ['us', 'de', 'fr', 'it', 'es']
    
    print("\n" + "="*80)
    print("DETAILED MARKET TESTING - LISTORY AI")
    print("Testing all 5 markets with occasions and brand tones")
    print("="*80)
    
    for market in markets:
        test_single_market(market)
    
    print("\n\n✅ All market tests complete!")
    print("Check the generated sample_*.json files for detailed content analysis")