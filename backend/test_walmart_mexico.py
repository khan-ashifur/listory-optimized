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

def test_walmart_mexico():
    print('🇲🇽 TESTING WALMART MEXICO LISTING GENERATION')
    print('=' * 55)

    user, created = User.objects.get_or_create(username='test_walmart_mexico')

    # Create Mexican product with Día de los Muertos occasion
    product = Product.objects.create(
        user=user,
        name='Decoración Altar Muertos LED',
        brand_name='MexicanTraditions',
        target_platform='walmart',
        marketplace='walmart_mexico',
        marketplace_language='es-mx',
        price=199.99,
        occasion='dia_de_los_muertos',
        brand_tone='luxury',
        categories='Hogar > Decoración > Festivales',
        description='Decoración LED premium para altar de Día de los Muertos con iluminación personalizable',
        features='Luces LED Multicolor\nControl Remoto Incluido\nResistente al Agua\nMateriales Mexicanos\nDiseño Tradicional\nNOM Certificado'
    )

    print(f'✅ Created Walmart Mexico product:')
    print(f'   Name: {product.name}')
    print(f'   Marketplace: {product.marketplace}')
    print(f'   Occasion: {product.occasion}')
    print(f'   Brand Tone: {product.brand_tone}')
    print(f'   Price: ${product.price}')

    try:
        service = ListingGeneratorService()
        listing = service.generate_listing(product.id, 'walmart')

        print(f'\n📊 WALMART MEXICO LISTING RESULTS:')
        print(f'   Status: {listing.status}')
        print(f'   Title: {listing.walmart_product_title}')
        print(f'   Title Length: {len(listing.walmart_product_title)} chars')

        # Check for Mexican elements
        mexican_elements = []
        title_lower = listing.walmart_product_title.lower()
        if 'mexico' in title_lower or 'méxico' in title_lower: 
            mexican_elements.append('Mexico reference')
        if 'dia' in title_lower and 'muertos' in title_lower: 
            mexican_elements.append('Día de los Muertos')
        if 'especial' in title_lower or 'walmart' in title_lower: 
            mexican_elements.append('Walmart México branding')

        print(f'   Mexican Elements: {len(mexican_elements)} - {mexican_elements}')

        # Check features for Mexican elements
        features_text = ' '.join(listing.walmart_key_features.split('\n'))
        feature_elements = []
        features_lower = features_text.lower()
        if 'mexicano' in features_lower or 'méxico' in features_lower:
            feature_elements.append('Mexican cultural references')
        if 'nom' in features_lower:
            feature_elements.append('NOM certification')
        if 'tradición' in features_lower or 'tradicion' in features_lower:
            feature_elements.append('Mexican tradition')

        print(f'   Feature Mexican Elements: {len(feature_elements)} - {feature_elements}')

        # Show key features
        print(f'\n🔘 KEY FEATURES:')
        features = listing.walmart_key_features.split('\n')
        for i, feature in enumerate(features[:3], 1):
            print(f'   {i}. {feature}')

        # Check for proper compliance guidance (not fake data)
        compliance_data = listing.walmart_compliance_certifications
        if '[SELLER TO PROVIDE]' in compliance_data:
            print(f'\n✅ Compliance contains proper guidance (not fake data)')
        else:
            print(f'\n⚠️ Compliance may contain generated data')

        print(f'\n✅ Walmart Mexico listing generated successfully!')
        
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
    test_walmart_mexico()