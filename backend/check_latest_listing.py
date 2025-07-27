#!/usr/bin/env python3
"""
Check the latest listing to see all field values.
"""
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def check_latest_listing():
    """Check the latest listing to see all field values."""
    print("🔍 CHECKING LATEST LISTING - ALL FIELDS")
    print("=" * 60)
    
    # Get the most recent listing
    listing = GeneratedListing.objects.filter(platform='amazon').order_by('-created_at').first()
    
    if not listing:
        print("❌ No Amazon listings found")
        return
    
    print(f"📄 Latest Listing: {listing.product.name}")
    print(f"📅 Created: {listing.created_at}")
    print(f"🏷️  Platform: {listing.platform}")
    print(f"📊 Status: {listing.status}")
    
    print(f"\n📝 FIELD VALUES:")
    print("-" * 40)
    
    # Check all important fields
    fields_to_check = [
        ('title', 'Title'),
        ('short_description', 'Short Description'),
        ('long_description', 'Long Description'),
        ('bullet_points', 'Bullet Points'),
        ('keywords', 'Keywords (Short Tail)'),
        ('amazon_backend_keywords', 'Backend Keywords'),
        ('amazon_aplus_content', 'A+ Content'),
        ('hero_title', 'Hero Title'),
        ('hero_content', 'Hero Content'),
        ('features', 'Features'),
        ('whats_in_box', "What's in Box"),
        ('trust_builders', 'Trust Builders'),
        ('faqs', 'FAQs'),
        ('social_proof', 'Social Proof'),
        ('guarantee', 'Guarantee'),
    ]
    
    for field_name, display_name in fields_to_check:
        field_value = getattr(listing, field_name, '')
        if field_value and len(str(field_value).strip()) > 0:
            char_count = len(str(field_value))
            print(f"✅ {display_name}: {char_count} characters")
            # Show preview for text fields
            if char_count > 100:
                preview = str(field_value)[:100] + "..."
            else:
                preview = str(field_value)
            print(f"   Preview: {preview}")
        else:
            print(f"❌ {display_name}: Empty or missing")
    
    # Special analysis for keywords
    print(f"\n🔑 KEYWORD ANALYSIS:")
    print("-" * 30)
    
    if listing.keywords:
        keywords_list = [k.strip() for k in listing.keywords.split(',') if k.strip()]
        print(f"📌 Short Tail Keywords: {len(keywords_list)} found")
        print(f"   Total characters: {len(listing.keywords)}")
        print(f"   Keywords: {', '.join(keywords_list[:5])}{'...' if len(keywords_list) > 5 else ''}")
    else:
        print(f"❌ Short Tail Keywords: EMPTY")
    
    if listing.amazon_backend_keywords:
        backend_char_count = len(listing.amazon_backend_keywords)
        print(f"🔧 Backend Keywords: {backend_char_count} characters")
        print(f"   Content: {listing.amazon_backend_keywords[:100]}{'...' if backend_char_count > 100 else ''}")
    else:
        print(f"❌ Backend Keywords: EMPTY")
    
    # Quality scores
    print(f"\n⭐ QUALITY SCORES:")
    print("-" * 30)
    print(f"Overall Quality: {listing.quality_score if listing.quality_score else 'Not set'}")
    print(f"Emotion Score: {listing.emotion_score if listing.emotion_score else 'Not set'}")
    print(f"Conversion Score: {listing.conversion_score if listing.conversion_score else 'Not set'}")
    print(f"Trust Score: {listing.trust_score if listing.trust_score else 'Not set'}")

if __name__ == "__main__":
    check_latest_listing()