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

def test_walmart_canada():
    print('🇨🇦 TESTING WALMART CANADA LISTING GENERATION')
    print('=' * 55)

    user, created = User.objects.get_or_create(username='test_walmart_canada')

    # Create Canadian product with Boxing Day occasion
    product = Product.objects.create(
        user=user,
        name='Premium Noise Cancelling Headphones',
        brand_name='AudioPro',
        target_platform='walmart',
        marketplace='walmart_canada',
        marketplace_language='en-ca',
        price=149.99,
        occasion='boxing_day',
        brand_tone='luxury',
        categories='Electronics > Audio > Headphones',
        description='Professional-grade wireless headphones with active noise cancellation',
        features='Active Noise Cancellation\nWireless Bluetooth 5.3\n35H Battery Life\nQuick Charge Technology\nPremium Leather Headband\nCSA Certified for Canada'
    )

    print(f'✅ Created Walmart Canada product:')
    print(f'   Name: {product.name}')
    print(f'   Marketplace: {product.marketplace}')
    print(f'   Occasion: {product.occasion}')
    print(f'   Brand Tone: {product.brand_tone}')
    print(f'   Price: ${product.price}')

    try:
        service = ListingGeneratorService()
        listing = service.generate_listing(product.id, 'walmart')

        print(f'\n📊 WALMART CANADA LISTING RESULTS:')
        print(f'   Status: {listing.status}')
        print(f'   Title: {listing.walmart_product_title}')
        print(f'   Title Length: {len(listing.walmart_product_title)} chars')

        # Check for Canadian elements
        canadian_elements = []
        title_lower = listing.walmart_product_title.lower()
        if 'canada' in title_lower: 
            canadian_elements.append('Canada in title')
        if 'boxing day' in title_lower: 
            canadian_elements.append('Boxing Day in title')
        if 'rollback' in title_lower: 
            canadian_elements.append('Rollback pricing')

        print(f'   Canadian Elements: {len(canadian_elements)} - {canadian_elements}')

        # Check features for Canadian elements
        features_text = ' '.join(listing.walmart_key_features.split('\n'))
        feature_elements = []
        features_lower = features_text.lower()
        if 'canadian' in features_lower:
            feature_elements.append('Canadian references')
        if 'csa' in features_lower:
            feature_elements.append('CSA certification')
        if 'health canada' in features_lower:
            feature_elements.append('Health Canada approval')

        print(f'   Feature Canadian Elements: {len(feature_elements)} - {feature_elements}')

        # Show key features
        print(f'\n🔘 KEY FEATURES:')
        features = listing.walmart_key_features.split('\n')
        for i, feature in enumerate(features[:3], 1):
            print(f'   {i}. {feature}')

        print(f'\n✅ Walmart Canada listing generated successfully!')
        
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
    test_walmart_canada()