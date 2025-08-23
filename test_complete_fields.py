import os, sys, django
backend_path = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

print('🔧 TESTING COMPLETE HYBRID APPROACH WITH ALL MISSING FIELDS')
print('=' * 65)

user, created = User.objects.get_or_create(username='complete_test_user')

# Clean up any existing test products
Product.objects.filter(user=user, name__icontains='Complete Test').delete()

# Create test product
product = Product.objects.create(
    user=user,
    name='Complete Test Smart Air Fryer',
    brand_name='CookMaster',
    target_platform='walmart',
    marketplace='walmart_usa',
    marketplace_language='en-us',
    price=199.99,
    occasion='christmas',
    brand_tone='luxury',
    categories='Home & Kitchen > Small Appliances > Air Fryers',
    description='Smart WiFi-enabled air fryer with app control and multiple cooking presets',
    features='Digital touchscreen\n8 cooking presets\n6-quart capacity\nNon-stick basket\nAuto shut-off\n1400W power\nDishwasher safe parts'
)

print(f'✅ Created test product: {product.name}')
print(f'   Price: ${product.price}')
print(f'   Brand: {product.brand_name}')
print(f'   Category: {product.categories}')

# Generate with complete hybrid approach
service = ListingGeneratorService()
listing = service.generate_listing(product.id, 'walmart')

print()
print('📊 COMPLETE GENERATION RESULTS:')
print(f'   Status: {listing.status}')
print(f'   Listing ID: {listing.id}')

if listing.status == 'completed':
    print()
    print('🔍 COMPLETE FIELD VERIFICATION:')
    
    # Core fields
    print('CORE FIELDS:')
    print(f'   ✅ Title: {listing.walmart_product_title[:60]}...')
    print(f'   ✅ Description: {len(listing.walmart_description)} chars')
    print(f'   ✅ Key Features: {len(listing.walmart_key_features.split(chr(10)))} features')
    
    # Keywords count 
    if listing.keywords:
        keywords_list = [k.strip() for k in listing.keywords.split(',') if k.strip()]
        keyword_count = len(keywords_list)
        print(f'   ✅ Keywords: {keyword_count} (Target: 30+)')
        if keyword_count >= 30:
            print('      🎯 KEYWORD TARGET ACHIEVED!')
        else:
            print('      ⚠️ Still below 30 keyword target')
    
    # NEW FIELDS - Product Identifiers
    print()
    print('PRODUCT IDENTIFIERS (PREVIOUSLY MISSING):')
    print(f'   GTIN/UPC: {listing.walmart_gtin_upc or "Not generated"}')
    print(f'   Manufacturer Part: {listing.walmart_manufacturer_part or "Not generated"}')
    print(f'   SKU ID: {listing.walmart_sku_id or "Not generated"}')
    
    # NEW FIELDS - Shipping Information
    print()
    print('SHIPPING INFORMATION (PREVIOUSLY MISSING):')
    print(f'   Shipping Weight: {listing.walmart_shipping_weight or "Not specified"}')
    shipping_dims = listing.walmart_shipping_dimensions
    if shipping_dims and shipping_dims != '{}':
        print(f'   Package Dimensions: Available ({len(shipping_dims)} chars)')
    else:
        print(f'   Package Dimensions: Not specified')
    
    # NEW FIELDS - Rich Media Recommendations
    print()
    print('RICH MEDIA RECOMMENDATIONS (PREVIOUSLY MISSING):')
    rich_media = listing.walmart_rich_media
    if rich_media and rich_media != '{}':
        import json
        try:
            media_data = json.loads(rich_media)
            print(f'   Rich Media: Generated ({len(media_data)} sections)')
            if 'main_images' in media_data:
                print(f'      - Main Images: {len(media_data["main_images"])} recommendations')
            if 'video_content' in media_data:
                print(f'      - Video Content: {len(media_data["video_content"])} recommendations')
        except:
            print(f'   Rich Media: Generated but parsing error')
    else:
        print(f'   Rich Media: Not generated')
    
    # Enhanced Profit Maximizer
    print()
    print('PROFIT MAXIMIZER (ENHANCED):')
    profit_data = listing.walmart_profit_maximizer
    if profit_data:
        import json
        try:
            profit = json.loads(profit_data)
            print(f'   Revenue Projections: Available')
            if 'revenue_projections' in profit:
                rev_proj = profit['revenue_projections']
                if 'yearly_projections' in rev_proj:
                    yearly = rev_proj['yearly_projections']
                    print(f'      - Conservative: {yearly.get("conservative", "N/A")}')
                    print(f'      - Realistic: {yearly.get("realistic", "N/A")}')
                    print(f'      - Aggressive: {yearly.get("aggressive", "N/A")}')
                else:
                    print(f'      - Basic projections only')
        except:
            print(f'   Profit Maximizer: Generated but parsing error')
    else:
        print(f'   Profit Maximizer: Not generated')
    
    # Success Assessment
    print()
    print('🎯 COMPLETENESS ASSESSMENT:')
    identifiers_complete = bool(listing.walmart_gtin_upc and listing.walmart_manufacturer_part and listing.walmart_sku_id)
    shipping_complete = bool(listing.walmart_shipping_weight and listing.walmart_shipping_dimensions != '{}')
    rich_media_complete = bool(listing.walmart_rich_media and listing.walmart_rich_media != '{}')
    keyword_target = keyword_count >= 30 if 'keyword_count' in locals() else False
    
    print(f'   Product Identifiers: {"✅ COMPLETE" if identifiers_complete else "❌ INCOMPLETE"}')
    print(f'   Shipping Information: {"✅ COMPLETE" if shipping_complete else "❌ INCOMPLETE"}')
    print(f'   Rich Media Recommendations: {"✅ COMPLETE" if rich_media_complete else "❌ INCOMPLETE"}')
    print(f'   Keyword Target (30+): {"✅ ACHIEVED" if keyword_target else "❌ NEEDS WORK"}')
    
    overall_complete = identifiers_complete and shipping_complete and rich_media_complete and keyword_target
    
    if overall_complete:
        print()
        print('🎉 SUCCESS: ALL MISSING FIELDS NOW GENERATED!')
        print('   Hybrid approach is now COMPLETE with all required sections')
        print('   Ready for 10/10 quality evaluation')
    else:
        incomplete_sections = []
        if not identifiers_complete: incomplete_sections.append('Product Identifiers')
        if not shipping_complete: incomplete_sections.append('Shipping Information')
        if not rich_media_complete: incomplete_sections.append('Rich Media')
        if not keyword_target: incomplete_sections.append('Keywords')
        
        print()
        print('⚠️ SOME SECTIONS STILL INCOMPLETE:')
        for section in incomplete_sections:
            print(f'   - {section}')
    
    print()
    print('🌐 FRONTEND TEST URL:')
    print(f'   http://localhost:3000/results/{listing.id}')
    print('   Should now display ALL sections including previously missing fields')

else:
    print(f'   ❌ Generation failed: {getattr(listing, "error_message", "Unknown error")}')

print()
print('✅ Complete field generation test completed!')