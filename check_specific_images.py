#!/usr/bin/env python3
"""
Check Turkey A+ Content for Specific Image Descriptions
"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.models import GeneratedListing

def check_specific_images():
    print("🖼️ CHECKING TURKEY IMAGE DESCRIPTIONS")
    print("=" * 60)
    
    # Get the latest Turkey listing
    try:
        listing = GeneratedListing.objects.order_by('-id').first()
        
        if not listing:
            print("❌ No Turkey listing found")
            return
            
        print(f"✅ Found listing ID: {listing.id}")
        
        aplus = listing.amazon_aplus_content
        if not aplus:
            print("❌ No A+ content found")
            return
            
        # Extract ENGLISH: prefixed descriptions
        english_descriptions = []
        lines = aplus.split('\n')
        
        for line in lines:
            if 'ENGLISH:' in line:
                # Extract the description after ENGLISH:
                desc = line.split('ENGLISH:')[1].strip()
                if desc and len(desc) > 50:  # Only meaningful descriptions
                    english_descriptions.append(desc)
        
        print(f"🖼️ Found {len(english_descriptions)} detailed image descriptions:")
        print()
        
        for i, desc in enumerate(english_descriptions, 1):
            print(f"📸 IMAGE {i}:")
            print(f"   {desc}")
            print()
            
        # Check for generic vs specific terms
        generic_terms = ['Collage', 'Grid', 'professional setup', 'Feature grid', 'Split-screen']
        specific_terms = ['Turkish', 'Istanbul', 'Ankara', 'video conference', 'family members', 'preparing', 'background']
        
        generic_count = sum(1 for desc in english_descriptions for term in generic_terms if term.lower() in desc.lower())
        specific_count = sum(1 for desc in english_descriptions for term in specific_terms if term.lower() in desc.lower())
        
        print(f"📊 ANALYSIS:")
        print(f"   Generic terms found: {generic_count}")
        print(f"   Specific terms found: {specific_count}")
        print(f"   Mexico-level specificity: {'YES' if specific_count > generic_count else 'NO'}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_specific_images()