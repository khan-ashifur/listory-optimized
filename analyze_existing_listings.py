#!/usr/bin/env python3
"""
Analyze existing listings to understand current system quality
"""

import os
import sys
import django
import json

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.models import GeneratedListing

def analyze_existing_listings():
    """Analyze existing listings in the database"""
    
    print("ANALYZING EXISTING LISTINGS")
    print("=" * 50)
    
    # Get all products
    products = Product.objects.all()
    print(f"Total products in database: {products.count()}")
    
    # Get all listings
    listings = GeneratedListing.objects.all()
    print(f"Total listings in database: {listings.count()}")
    
    # Find Sweden products
    sweden_products = Product.objects.filter(marketplace='se')
    print(f"Sweden products: {sweden_products.count()}")
    
    # Find international products
    international_products = Product.objects.exclude(marketplace='us')
    print(f"International products: {international_products.count()}")
    
    print("\nINTERNATIONAL PRODUCTS BREAKDOWN:")
    marketplaces = international_products.values_list('marketplace', flat=True).distinct()
    for marketplace in marketplaces:
        count = international_products.filter(marketplace=marketplace).count()
        print(f"  {marketplace}: {count} products")
    
    # Analyze recent listings
    recent_listings = GeneratedListing.objects.order_by('-created_at')[:10]
    
    print(f"\nRECENT LISTINGS ANALYSIS:")
    print("-" * 30)
    
    for i, listing in enumerate(recent_listings, 1):
        print(f"\n{i}. Listing ID: {listing.id}")
        print(f"   Product: {listing.product.name}")
        print(f"   Marketplace: {listing.product.marketplace}")
        print(f"   Language: {listing.product.marketplace_language}")
        print(f"   Platform: {listing.platform}")
        print(f"   Created: {listing.created_at}")
        
        # Check if has title
        if hasattr(listing, 'product_title') and listing.product_title:
            title_preview = listing.product_title[:100] + "..." if len(listing.product_title) > 100 else listing.product_title
            print(f"   Title: {title_preview}")
        
        # Check for international content
        content_to_check = ""
        if hasattr(listing, 'product_title'):
            content_to_check += str(listing.product_title or "")
        if hasattr(listing, 'bullet_points') and listing.bullet_points:
            content_to_check += str(listing.bullet_points)
        
        # Check language
        english_indicators = ['kitchen', 'knife', 'professional', 'quality', 'stainless', 'steel', 'the', 'and', 'with']
        international_indicators = {
            'se': ['kök', 'kniv', 'professionell', 'kvalitet', 'rostfritt', 'stål'],
            'de': ['küche', 'messer', 'professionell', 'qualität', 'edelstahl'],
            'fr': ['cuisine', 'couteau', 'professionnel', 'qualité', 'acier'],
            'mx': ['cocina', 'cuchillo', 'profesional', 'calidad', 'acero'],
            'tr': ['mutfak', 'bıçak', 'profesyonel', 'kalite', 'çelik'],
            'nl': ['keuken', 'mes', 'professioneel', 'kwaliteit', 'staal'],
            'br': ['cozinha', 'faca', 'profissional', 'qualidade', 'aço'],
            'ae': ['مطبخ', 'سكين', 'مهني', 'جودة', 'فولاذ'],
            'jp': ['キッチン', 'ナイフ', 'プロ', '品質', '鋼'],
        }
        
        marketplace = listing.product.marketplace
        english_found = sum(1 for word in english_indicators if word.lower() in content_to_check.lower())
        international_found = 0
        
        if marketplace in international_indicators:
            international_found = sum(1 for word in international_indicators[marketplace] if word.lower() in content_to_check.lower())
        
        if marketplace != 'us':
            if english_found > international_found:
                print(f"   ISSUE: More English ({english_found}) than {marketplace} ({international_found}) content detected")
            elif international_found > 0:
                print(f"   GOOD: International content detected ({international_found} words)")
            else:
                print(f"   WARNING: No clear language markers found")
    
    return {
        'total_products': products.count(),
        'total_listings': listings.count(),
        'sweden_products': sweden_products.count(),
        'international_products': international_products.count(),
        'recent_listings': list(recent_listings)
    }

def find_sweden_listing_sample():
    """Find a Sweden listing sample for analysis"""
    
    print("\nFINDING SWEDEN LISTING SAMPLE:")
    print("-" * 40)
    
    # Look for Sweden listings
    sweden_listings = GeneratedListing.objects.filter(product__marketplace='se').order_by('-created_at')
    
    if sweden_listings.exists():
        listing = sweden_listings.first()
        print(f"Found Sweden listing: {listing.id}")
        print(f"Product: {listing.product.name}")
        print(f"Created: {listing.created_at}")
        
        # Extract content for analysis
        content = {}
        
        # Get all attributes
        for field in ['product_title', 'bullet_points', 'product_description', 'keywords', 'aplus_content_plan']:
            if hasattr(listing, field):
                value = getattr(listing, field)
                if value:
                    content[field] = value
                    print(f"\n{field.upper()}:")
                    if isinstance(value, str):
                        preview = value[:200] + "..." if len(value) > 200 else value
                        print(f"  {preview}")
                    elif isinstance(value, list):
                        print(f"  Count: {len(value)}")
                        if len(value) > 0:
                            print(f"  Sample: {str(value[0])[:100]}...")
                    else:
                        print(f"  Type: {type(value)}")
        
        return listing, content
    else:
        print("No Sweden listings found")
        return None, None

def analyze_listing_content(listing, content):
    """Analyze listing content quality"""
    
    if not listing or not content:
        return {'quality': 'No data', 'issues': ['No listing found']}
    
    print(f"\nANALYZING LISTING QUALITY:")
    print("-" * 40)
    
    analysis = {
        'quality': 'Unknown',
        'issues': [],
        'successes': [],
        'language_analysis': {}
    }
    
    # Check each field
    for field, value in content.items():
        print(f"\n{field.upper()} ANALYSIS:")
        
        if not value:
            analysis['issues'].append(f"Empty {field}")
            continue
        
        # Convert to string for analysis
        text_content = str(value)
        
        # Language analysis for Sweden
        english_words = ['kitchen', 'knife', 'professional', 'quality', 'stainless', 'steel', 'the', 'and', 'with', 'for', 'is']
        swedish_words = ['kök', 'kniv', 'professionell', 'kvalitet', 'rostfritt', 'stål', 'och', 'med', 'för', 'är']
        
        english_count = sum(1 for word in english_words if word.lower() in text_content.lower())
        swedish_count = sum(1 for word in swedish_words if word.lower() in text_content.lower())
        
        print(f"  Length: {len(text_content)} characters")
        print(f"  English words detected: {english_count}")
        print(f"  Swedish words detected: {swedish_count}")
        
        if field == 'product_title':
            if len(text_content) < 50:
                analysis['issues'].append("Title too short")
            elif len(text_content) > 200:
                analysis['issues'].append("Title too long")
            else:
                analysis['successes'].append("Title length good")
        
        if english_count > swedish_count and field != 'aplus_content_plan':
            analysis['issues'].append(f"{field} has more English than Swedish content")
        elif swedish_count > 0:
            analysis['successes'].append(f"{field} has Swedish content")
        
        analysis['language_analysis'][field] = {
            'length': len(text_content),
            'english_words': english_count,
            'swedish_words': swedish_count
        }
    
    # Overall assessment
    total_issues = len(analysis['issues'])
    total_successes = len(analysis['successes'])
    
    if total_issues == 0:
        analysis['quality'] = 'Excellent'
    elif total_issues <= 2:
        analysis['quality'] = 'Good'
    elif total_issues <= 5:
        analysis['quality'] = 'Fair'
    else:
        analysis['quality'] = 'Poor'
    
    print(f"\nOVERALL QUALITY: {analysis['quality']}")
    print(f"Issues: {total_issues}, Successes: {total_successes}")
    
    return analysis

def main():
    """Main analysis function"""
    
    # Analyze existing listings
    overview = analyze_existing_listings()
    
    # Find Sweden sample
    listing, content = find_sweden_listing_sample()
    
    # Analyze content quality
    analysis = analyze_listing_content(listing, content)
    
    # Summary
    print(f"\nSUMMARY REPORT:")
    print("=" * 50)
    print(f"Total products: {overview['total_products']}")
    print(f"Total listings: {overview['total_listings']}")
    print(f"Sweden products: {overview['sweden_products']}")
    print(f"International products: {overview['international_products']}")
    
    if listing:
        print(f"\nSweden listing quality: {analysis['quality']}")
        print(f"Main issues: {analysis['issues'][:3]}")
        print(f"Main successes: {analysis['successes'][:3]}")
    else:
        print("No Sweden listings available for analysis")
    
    return overview, listing, content, analysis

if __name__ == "__main__":
    try:
        results = main()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()