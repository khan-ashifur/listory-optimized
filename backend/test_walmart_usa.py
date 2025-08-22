#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to the Python path
backend_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

def test_walmart_usa():
    print('🇺🇸 TESTING WALMART USA LISTING GENERATION')
    print('=' * 55)

    user, created = User.objects.get_or_create(username='test_walmart_usa')

    # Create USA product with Independence Day occasion
    product = Product.objects.create(
        user=user,
        name='Patriotic LED Flag Display',
        brand_name='AmericaPride',
        target_platform='walmart',
        marketplace='walmart_usa',
        marketplace_language='en-us',
        price=89.99,
        occasion='independence_day',
        brand_tone='luxury',
        categories='Home & Garden > Outdoor Decor > Flags',
        description='Premium LED-illuminated American flag display for patriotic home decoration',
        features='LED Illumination System\nWeatherproof Construction\nRemote Control Operation\nTimer Function\nUL Listed for Safety\nMade in USA'
    )

    print(f'✅ Created Walmart USA product:')
    print(f'   Name: {product.name}')
    print(f'   Marketplace: {product.marketplace}')
    print(f'   Occasion: {product.occasion}')
    print(f'   Brand Tone: {product.brand_tone}')
    print(f'   Price: ${product.price}')

    try:
        service = ListingGeneratorService()
        listing = service.generate_listing(product.id, 'walmart')

        print(f'\n📊 WALMART USA LISTING RESULTS:')
        print(f'   Status: {listing.status}')
        print(f'   Title: {listing.walmart_product_title}')
        print(f'   Title Length: {len(listing.walmart_product_title)} chars')

        # Check for American elements
        american_elements = []
        title_lower = listing.walmart_product_title.lower()
        if 'america' in title_lower or 'usa' in title_lower: 
            american_elements.append('American reference')
        if 'july' in title_lower or 'independence' in title_lower: 
            american_elements.append('Independence Day')
        if 'patriotic' in title_lower or 'flag' in title_lower: 
            american_elements.append('Patriotic theme')

        print(f'   American Elements: {len(american_elements)} - {american_elements}')

        # Check features for American elements
        features_text = ' '.join(listing.walmart_key_features.split('\n'))
        feature_elements = []
        features_lower = features_text.lower()
        if 'american' in features_lower or 'usa' in features_lower:
            feature_elements.append('American manufacturing')
        if 'ul' in features_lower:
            feature_elements.append('UL certification')
        if 'patriotic' in features_lower:
            feature_elements.append('Patriotic theme')

        print(f'   Feature American Elements: {len(feature_elements)} - {feature_elements}')

        # Show key features
        print(f'\n🔘 KEY FEATURES:')
        features = listing.walmart_key_features.split('\n')
        for i, feature in enumerate(features[:3], 1):
            print(f'   {i}. {feature}')

        print(f'\n✅ Walmart USA listing generated successfully!')
        
        # Save listing ID for frontend testing
        print(f'\n🌐 Test URL: http://localhost:3000/results/{listing.id}')

    except Exception as e:
        print(f'❌ Error generating listing: {e}')
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        product.delete()
        print(f'\n🧹 Test completed!')

if __name__ == '__main__':
    test_walmart_usa()