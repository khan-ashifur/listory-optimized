#!/usr/bin/env python3
"""
Test script to generate a Swedish Amazon listing
Tests all Swedish language implementation features:
- Title optimization with Swedish formatting
- Bullet points with Swedish formatting 
- A+ content with Swedish UI labels but English image descriptions
- Swedish occasions integration (Jul, Lucia, Midsommar, etc.)
- Swedish industry keywords
"""

import os
import sys
import django
import json
from datetime import datetime

# Add the backend directory to Python path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_path)

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

def create_test_product():
    """Create a test product for Swedish marketplace"""
    
    from django.contrib.auth.models import User
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com'}
    )
    
    # Delete existing test products to avoid duplicates
    Product.objects.filter(name__icontains="Swedish Test").delete()
    
    product_data = {
        'user': user,
        'name': 'Swedish Test Premium Bluetooth Headphones',
        'description': 'High-quality wireless headphones perfect for Swedish lifestyle. Features noise cancellation, 30-hour battery, and sustainable design.',
        'brand_name': 'SwedishAudio',
        'brand_tone': 'professional',
        'target_platform': 'amazon',
        'price': 899.00,  # Swedish krona pricing
        'categories': 'Electronics, Audio, Headphones',
        'target_keywords': 'bluetooth hörlurar, trådlösa hörlurar, noise cancelling, premium ljudkvalitet, lång batteritid',
        'marketplace': 'se',  # Sweden marketplace
        'marketplace_language': 'sv',  # Swedish language
        'occasion': 'jul',  # Christmas in Swedish
        'target_audience': 'Swedish families, professionals, music lovers',
        'features': 'Noise cancellation, 30-hour battery, Bluetooth 5.3, comfortable design, sustainable materials'
    }
    
    product = Product.objects.create(**product_data)
    print(f"✅ Created test product: {product.name} (ID: {product.id})")
    print(f"   Marketplace: {product.marketplace}")
    print(f"   Language: {product.marketplace_language}")
    print(f"   Occasion: {product.occasion}")
    print(f"   Brand Tone: {product.brand_tone}")
    
    return product

def test_swedish_listing_generation():
    """Test the complete Swedish listing generation"""
    print("🇸🇪 TESTING SWEDISH LISTING GENERATION")
    print("=" * 50)
    
    # Create test product
    product = create_test_product()
    
    # Initialize the listing generator service
    service = ListingGeneratorService()
    
    print(f"\n📋 Generating Swedish listing for: {product.name}")
    print(f"   Target keywords: {product.target_keywords}")
    print(f"   Occasion: {product.occasion} (Swedish Christmas)")
    
    try:
        # Generate the listing
        listing = service.generate_listing(product.id, 'amazon')
        
        print(f"\n✅ LISTING GENERATION SUCCESSFUL!")
        print(f"   Listing ID: {listing.id}")
        print(f"   Status: {listing.status}")
        
        # Display the generated content
        print(f"\n🇸🇪 SWEDISH LISTING RESULTS:")
        print("=" * 60)
        
        # Title
        print(f"\n📝 TITLE ({len(listing.title)} chars):")
        print(f"   {listing.title}")
        
        # Check for Swedish title formatting
        swedish_indicators = ['Bäst i Test', 'Premium', 'Kvalitet', 'Sverige', 'CE-märkt']
        title_has_swedish = any(indicator in listing.title for indicator in swedish_indicators)
        print(f"   ✅ Swedish formatting detected: {title_has_swedish}")
        
        # Bullet Points
        print(f"\n🔸 BULLET POINTS:")
        if hasattr(listing, 'bullet_points') and listing.bullet_points:
            try:
                bullets = json.loads(listing.bullet_points) if isinstance(listing.bullet_points, str) else listing.bullet_points
                for i, bullet in enumerate(bullets, 1):
                    print(f"   {i}. {bullet}")
            except:
                print(f"   {listing.bullet_points}")
        
        # Check for Swedish bullet formatting
        bullet_text = str(listing.bullet_points)
        swedish_bullet_phrases = ['BÄST I TEST', 'svenska familjer', 'CE-märkt', 'års garanti', 'miljövänlig']
        bullet_has_swedish = any(phrase in bullet_text for phrase in swedish_bullet_phrases)
        print(f"   ✅ Swedish bullet formatting detected: {bullet_has_swedish}")
        
        # Product Description
        print(f"\n📄 DESCRIPTION ({len(listing.long_description)} chars):")
        desc_preview = listing.long_description[:200] + "..." if len(listing.long_description) > 200 else listing.long_description
        print(f"   {desc_preview}")
        
        # Check for Swedish content in description
        swedish_desc_phrases = ['svenska', 'kvalitet', 'garanti', 'hållbar']
        desc_has_swedish = any(phrase in listing.long_description.lower() for phrase in swedish_desc_phrases)
        print(f"   ✅ Swedish content detected: {desc_has_swedish}")
        
        # Keywords
        print(f"\n🔍 SEO KEYWORDS:")
        if hasattr(listing, 'amazon_keywords') and listing.amazon_keywords:
            try:
                keywords = json.loads(listing.amazon_keywords) if isinstance(listing.amazon_keywords, str) else listing.amazon_keywords
                for keyword in keywords[:10]:  # Show first 10
                    print(f"   - {keyword}")
                if len(keywords) > 10:
                    print(f"   ... and {len(keywords) - 10} more keywords")
            except:
                print(f"   {listing.amazon_keywords}")
        
        # Backend Keywords
        print(f"\n🔧 BACKEND KEYWORDS:")
        if hasattr(listing, 'amazon_backend_keywords') and listing.amazon_backend_keywords:
            print(f"   {listing.amazon_backend_keywords}")
        
        # Check for Swedish industry keywords
        all_keywords = str(listing.amazon_keywords) + " " + str(listing.amazon_backend_keywords)
        swedish_keywords = ['hörlurar', 'trådlösa', 'ljudkvalitet', 'batteritid', 'brusreducering']
        keywords_have_swedish = any(keyword in all_keywords.lower() for keyword in swedish_keywords)
        print(f"   ✅ Swedish industry keywords detected: {keywords_have_swedish}")
        
        # A+ Content
        print(f"\n🎨 A+ CONTENT ANALYSIS:")
        if hasattr(listing, 'amazon_aplus_content') and listing.amazon_aplus_content:
            try:
                aplus = json.loads(listing.amazon_aplus_content) if isinstance(listing.amazon_aplus_content, str) else listing.amazon_aplus_content
                
                print(f"   📊 A+ Content Structure:")
                for section_key, section_data in aplus.items():
                    if isinstance(section_data, dict):
                        print(f"     - {section_key}: {section_data.get('title', 'N/A')}")
                        
                        # Check for Swedish UI labels
                        content_text = str(section_data)
                        if 'Nyckelord' in content_text or 'Bildstrategi' in content_text or 'SEO Fokus' in content_text:
                            print(f"       ✅ Swedish UI labels detected")
                        
                        # Check for English image descriptions
                        if 'ENGLISH:' in content_text:
                            print(f"       ✅ English image descriptions detected")
                
            except Exception as e:
                print(f"   Error parsing A+ content: {e}")
        
        # Occasions Integration
        print(f"\n🎄 OCCASIONS ANALYSIS:")
        content_text = listing.title + " " + listing.long_description + " " + str(listing.bullet_points)
        
        # Check for Swedish occasions
        swedish_occasions = ['Jul', 'Lucia', 'Midsommar', 'Valborg', 'svenska familjer']
        found_occasions = [occ for occ in swedish_occasions if occ.lower() in content_text.lower()]
        
        if found_occasions:
            print(f"   ✅ Swedish occasions found: {', '.join(found_occasions)}")
        else:
            print(f"   ⚠️  No specific Swedish occasions detected (may be generic)")
        
        # Quality Score
        if hasattr(listing, 'quality_score') and listing.quality_score:
            print(f"\n📊 QUALITY SCORE: {listing.quality_score}")
        
        # Summary
        print(f"\n🇸🇪 SWEDISH IMPLEMENTATION SUMMARY:")
        print(f"   ✅ Title formatting: {title_has_swedish}")
        print(f"   ✅ Bullet formatting: {bullet_has_swedish}")
        print(f"   ✅ Swedish content: {desc_has_swedish}")
        print(f"   ✅ Swedish keywords: {keywords_have_swedish}")
        print(f"   ✅ Occasions: {len(found_occasions) > 0}")
        
        overall_swedish_score = sum([
            title_has_swedish, bullet_has_swedish, desc_has_swedish, 
            keywords_have_swedish, len(found_occasions) > 0
        ])
        
        print(f"\n🎯 OVERALL SWEDISH IMPLEMENTATION: {overall_swedish_score}/5")
        
        if overall_swedish_score >= 4:
            print("   🏆 EXCELLENT - Sweden implementation working well!")
        elif overall_swedish_score >= 3:
            print("   ✅ GOOD - Most Swedish features working")
        elif overall_swedish_score >= 2:
            print("   ⚠️  PARTIAL - Some Swedish features missing")
        else:
            print("   ❌ NEEDS WORK - Swedish implementation incomplete")
        
        return listing
        
    except Exception as e:
        print(f"❌ Error generating listing: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None

def main():
    """Main test function"""
    print("🧪 SWEDEN MARKET TESTING SUITE")
    print("Testing Swedish language implementation in Listory AI")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Test listing generation
    listing = test_swedish_listing_generation()
    
    if listing:
        print(f"\n✅ SWEDEN MARKET TEST COMPLETED SUCCESSFULLY!")
        print(f"Generated listing ID: {listing.id}")
        print(f"Review the output above to evaluate Swedish implementation quality.")
    else:
        print(f"\n❌ SWEDEN MARKET TEST FAILED!")
        print(f"Check the error messages above for troubleshooting.")

if __name__ == "__main__":
    main()