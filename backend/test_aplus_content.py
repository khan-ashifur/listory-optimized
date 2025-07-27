#!/usr/bin/env python3
"""
Test script to examine the A+ content and image descriptions.
"""
import os
import sys
import django
import json

# Add the backend directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def check_aplus_content():
    """Check the latest A+ content generation."""
    print("🔍 Checking A+ Content Generation...")
    
    # Get the most recent listing
    listing = GeneratedListing.objects.filter(platform='amazon').order_by('-created_at').first()
    
    if not listing:
        print("❌ No Amazon listings found")
        return
    
    print(f"📄 Latest Listing: {listing.product.name}")
    print(f"📅 Created: {listing.created_at}")
    
    # Check A+ content
    if listing.amazon_aplus_content:
        try:
            aplus_data = json.loads(listing.amazon_aplus_content)
            print(f"\n🎨 A+ Content Structure:")
            print("=" * 50)
            
            aplus_plan = aplus_data.get('aPlusContentPlan', {})
            if aplus_plan:
                print("📋 A+ Content Sections:")
                for section_key, section_data in aplus_plan.items():
                    if isinstance(section_data, dict):
                        title = section_data.get('title', 'No title')
                        content = section_data.get('content', 'No content')
                        image_req = section_data.get('image_requirements', section_data.get('image_suggestion', 'No image description'))
                        
                        print(f"\n🏷️  {section_key.upper()}:")
                        print(f"   Title: {title[:60]}{'...' if len(title) > 60 else ''}")
                        print(f"   Content: {content[:80]}{'...' if len(content) > 80 else ''}")
                        print(f"   Image: {image_req[:80]}{'...' if len(image_req) > 80 else ''}")
            
            # Check PPC Strategy
            ppc_strategy = aplus_data.get('ppcStrategy', {})
            if ppc_strategy:
                print(f"\n💰 PPC Strategy:")
                print(f"   Budget: {ppc_strategy.get('dailyBudget', 'Not specified')}")
                print(f"   Target ACOS: {ppc_strategy.get('targetAcos', 'Not specified')}")
            
            # Check Brand Summary
            brand_summary = aplus_data.get('brandSummary', '')
            if brand_summary:
                print(f"\n🏢 Brand Summary:")
                print(f"   {brand_summary[:100]}{'...' if len(brand_summary) > 100 else ''}")
                
        except json.JSONDecodeError:
            print("❌ A+ content is not valid JSON")
            print(f"Raw content preview: {listing.amazon_aplus_content[:200]}...")
    else:
        print("❌ No A+ content found")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    check_aplus_content()