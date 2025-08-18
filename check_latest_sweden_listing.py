#!/usr/bin/env python
"""
Check the latest Sweden listing content
"""
import os
import sys
import django
import json

# Add backend directory to path
sys.path.insert(0, 'C:/Users/khana/Desktop/listory-ai/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def check_latest_sweden_listing():
    """Check the latest Sweden listing content"""
    
    # Get latest Sweden listing
    sweden_listings = GeneratedListing.objects.filter(product__marketplace='se').order_by('-created_at')
    
    if not sweden_listings.exists():
        print("No Sweden listings found!")
        return
    
    latest = sweden_listings.first()
    print(f"Latest Sweden listing ID: {latest.id}")
    print(f"Product: {latest.product.name}")
    print(f"Created: {latest.created_at}")
    print(f"Quality Score: {latest.quality_score}")
    
    print(f"\n=== FIELD ANALYSIS ===")
    print(f"Title: {'✅' if latest.title else '❌'} ({len(latest.title)} chars)")
    print(f"Bullet Points: {'✅' if latest.bullet_points else '❌'} ({len(latest.bullet_points)} chars)")
    print(f"Long Description: {'✅' if latest.long_description else '❌'} ({len(latest.long_description)} chars)")
    print(f"Short Description: {'✅' if latest.short_description else '❌'} ({len(latest.short_description)} chars)")
    print(f"Amazon Keywords: {'✅' if latest.amazon_keywords else '❌'} ({len(latest.amazon_keywords)} chars)")
    print(f"Amazon Backend Keywords: {'✅' if latest.amazon_backend_keywords else '❌'} ({len(latest.amazon_backend_keywords)} chars)")
    print(f"Amazon A+ Content: {'✅' if latest.amazon_aplus_content else '❌'} ({len(latest.amazon_aplus_content)} chars)")
    
    if latest.title:
        print(f"\n=== TITLE ===")
        print(f"{latest.title}")
    
    if latest.bullet_points:
        print(f"\n=== BULLET POINTS ===")
        bullets = latest.bullet_points.split('\n')
        for i, bullet in enumerate(bullets[:3], 1):
            print(f"{i}. {bullet[:100]}...")
    
    if latest.amazon_aplus_content:
        print(f"\n=== A+ CONTENT ===")
        # Try to parse as JSON first
        try:
            if latest.amazon_aplus_content.strip().startswith('{'):
                aplus_data = json.loads(latest.amazon_aplus_content)
                print("A+ Content format: JSON")
                if 'aPlusContentPlan' in aplus_data:
                    plan = aplus_data['aPlusContentPlan']
                    print(f"Sections: {list(plan.keys())}")
                    for section_name, section_data in plan.items():
                        if 'title' in section_data:
                            print(f"  {section_name}: {section_data['title'][:50]}...")
            else:
                print("A+ Content format: HTML")
                print(f"Content preview: {latest.amazon_aplus_content[:200]}...")
        except Exception as e:
            print(f"A+ Content parsing error: {e}")
    
    return latest

if __name__ == "__main__":
    check_latest_sweden_listing()