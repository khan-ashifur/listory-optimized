"""
Comprehensive Field Verification Test
Checks EVERY single field is being generated properly
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
from django.contrib.auth.models import User

def verify_all_fields():
    """Verify every single field is generated"""
    
    print("\n" + "="*80)
    print("COMPREHENSIVE FIELD VERIFICATION TEST")
    print("="*80)
    
    service = ListingGeneratorService()
    test_user, _ = User.objects.get_or_create(username='field_tester')
    
    # Create test product
    product = Product.objects.create(
        user=test_user,
        name="Professional Wireless Headphones",
        description="Premium audio device for professionals",
        brand_name="TestBrand",
        brand_tone="professional",
        target_platform="amazon",
        marketplace="us",
        categories="Electronics/Audio",
        features="Noise Cancellation, 30hr Battery",
        target_audience="Professionals",
        occasion="christmas"
    )
    
    try:
        # Generate listing
        print("\n⏳ Generating listing...")
        listing = service.generate_listing(product_id=product.id, platform='amazon')
        
        if listing:
            # Define all expected fields (using correct model field names)
            expected_fields = {
                'title': 'Product Title',
                'bullet_points': 'Bullet Points (5)',
                'long_description': 'Product Description',
                'amazon_backend_keywords': 'Backend Search Terms',
                'amazon_keywords': 'SEO Keywords',
                'amazon_aplus_content': 'A+ Content Sections',
                'hero_title': 'Hero Title',
                'hero_content': 'Hero Content',
                'features': 'Features',
                'whats_in_box': "What's in the Box",
                'trust_builders': 'Trust Builders',
                'faqs': 'FAQs',
                'social_proof': 'Social Proof',
                'guarantee': 'Guarantee',
                'keywords': 'Keywords'
            }
            
            print("\n📋 FIELD VERIFICATION RESULTS:")
            print("-" * 60)
            
            missing_fields = []
            incomplete_fields = []
            
            # Check each field
            for field, display_name in expected_fields.items():
                value = getattr(listing, field, None)
                
                if value is None:
                    print(f"❌ {display_name}: MISSING")
                    missing_fields.append(field)
                elif value == "" or value == "[]" or value == "{}":
                    print(f"⚠️  {display_name}: EMPTY")
                    incomplete_fields.append(field)
                else:
                    # Parse JSON fields
                    if field in ['bullet_points', 'amazon_aplus_content', 'faqs']:
                        try:
                            if field == 'bullet_points':
                                parsed = json.loads(value) if value else None
                                count = len(parsed) if parsed else 0
                                status = "✅" if count >= 5 else "⚠️"
                                print(f"{status} {display_name}: {count} items")
                                if count < 5:
                                    incomplete_fields.append(field)
                            elif field == 'amazon_aplus_content':
                                # A+ content is HTML, not JSON
                                html_content = value
                                if html_content and len(html_content) > 100:
                                    # Count sections by counting div elements
                                    section_count = html_content.count('<div class=') + html_content.count('<div id=')
                                    print(f"{'✅' if section_count >= 4 else '⚠️'} {display_name}: {len(html_content)} chars, ~{section_count} sections")
                                    
                                    # Check for key A+ elements
                                    has_hero = 'hero' in html_content.lower()
                                    has_features = 'feature' in html_content.lower()
                                    has_quality = 'quality' in html_content.lower() or 'trust' in html_content.lower()
                                    has_warranty = 'warranty' in html_content.lower() or 'guarantee' in html_content.lower()
                                    
                                    print(f"     ✅ Hero Section: {'Yes' if has_hero else 'No'}")
                                    print(f"     ✅ Features: {'Yes' if has_features else 'No'}")
                                    print(f"     ✅ Quality/Trust: {'Yes' if has_quality else 'No'}")
                                    print(f"     ✅ Warranty/Guarantee: {'Yes' if has_warranty else 'No'}")
                                    
                                    if section_count < 4:
                                        incomplete_fields.append(field)
                                else:
                                    print(f"⚠️  {display_name}: Too short ({len(html_content)} chars)")
                                    incomplete_fields.append(field)
                            elif field == 'faqs':
                                parsed = json.loads(value) if value else None
                                count = len(parsed) if parsed else 0
                                print(f"{'✅' if count >= 3 else '⚠️'} {display_name}: {count} Q&As")
                                if count < 3:
                                    incomplete_fields.append(field)
                        except json.JSONDecodeError:
                            print(f"⚠️  {display_name}: Invalid JSON")
                            incomplete_fields.append(field)
                    else:
                        # Text fields
                        length = len(value)
                        if field == 'title':
                            status = "✅" if 80 <= length <= 200 else "⚠️"
                            print(f"{status} {display_name}: {length} chars")
                            if length < 80:
                                incomplete_fields.append(field)
                        elif field == 'description':
                            status = "✅" if length >= 500 else "⚠️"
                            print(f"{status} {display_name}: {length} chars")
                            if length < 500:
                                incomplete_fields.append(field)
                        elif field == 'backend_keywords':
                            status = "✅" if length >= 200 else "⚠️"
                            print(f"{status} {display_name}: {length} chars")
                            if length < 200:
                                incomplete_fields.append(field)
                        else:
                            print(f"✅ {display_name}: {length} chars")
            
            # Additional checks
            print("\n📊 ADDITIONAL VERIFICATION:")
            print("-" * 60)
            
            # Check if keywords are properly separated
            if hasattr(listing, 'amazon_backend_keywords') and listing.amazon_backend_keywords:
                keyword_count = len(listing.amazon_backend_keywords.split(','))
                print(f"{'✅' if keyword_count >= 15 else '⚠️'} Backend Keywords: {keyword_count} terms")
            
            # Check SEO keywords
            if hasattr(listing, 'amazon_keywords') and listing.amazon_keywords:
                seo_count = len(listing.amazon_keywords.split(','))
                print(f"{'✅' if seo_count >= 5 else '⚠️'} SEO Keywords: {seo_count} terms")
            else:
                print(f"❌ SEO Keywords: NOT FOUND")
                missing_fields.append('amazon_keywords')
            
            # Summary
            print("\n" + "="*60)
            print("SUMMARY")
            print("="*60)
            
            if missing_fields:
                print(f"\n❌ CRITICAL: {len(missing_fields)} fields are MISSING:")
                for field in missing_fields:
                    print(f"   • {field}")
            
            if incomplete_fields:
                print(f"\n⚠️  WARNING: {len(incomplete_fields)} fields are INCOMPLETE:")
                for field in incomplete_fields:
                    print(f"   • {field}")
            
            if not missing_fields and not incomplete_fields:
                print("\n✅ SUCCESS: All fields are properly generated!")
            
            # Save detailed output
            output = {
                'title': listing.title,
                'bullet_points': json.loads(listing.bullet_points) if listing.bullet_points else [],
                'description': listing.description[:500] + '...' if listing.description else '',
                'backend_keywords': listing.backend_keywords,
                'seo_keywords': listing.seo_keywords,
                'aplus_content': json.loads(listing.aplus_content) if listing.aplus_content else {},
                'brand_summary': listing.brand_summary if hasattr(listing, 'brand_summary') else 'N/A',
                'faqs': json.loads(listing.faqs) if hasattr(listing, 'faqs') and listing.faqs else [],
                'missing_fields': missing_fields,
                'incomplete_fields': incomplete_fields
            }
            
            with open('field_verification_output.json', 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            
            print("\n📁 Detailed output saved to: field_verification_output.json")
            
            return not missing_fields  # Return True if no missing fields
            
    except Exception as e:
        print(f"\n❌ Error during generation: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        product.delete()

if __name__ == "__main__":
    success = verify_all_fields()
    
    if not success:
        print("\n🔧 RECOMMENDATION: Check the services.py file to ensure all fields are being generated and saved properly.")
        print("   Specifically check:")
        print("   1. A+ Content SEO optimization fields")
        print("   2. Keywords field in each A+ section")
        print("   3. Brand summary generation")
        print("   4. SEO keywords separate from backend keywords")