#!/usr/bin/env python3
"""
Test script to view the structured HTML A+ content.
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

def view_aplus_html():
    """View the structured HTML A+ content."""
    print("🎨 Viewing Structured A+ Content...")
    
    # Get the most recent listing
    listing = GeneratedListing.objects.filter(platform='amazon').order_by('-created_at').first()
    
    if not listing:
        print("❌ No Amazon listings found")
        return
    
    print(f"📄 Latest Listing: {listing.product.name}")
    print(f"📅 Created: {listing.created_at}")
    
    if listing.amazon_aplus_content:
        print(f"\n🎨 A+ Content Length: {len(listing.amazon_aplus_content)} characters")
        
        # Check if it's HTML or JSON
        if listing.amazon_aplus_content.strip().startswith('<'):
            print("✅ Content is structured HTML")
            
            # Save to file for viewing
            with open('aplus_preview.html', 'w', encoding='utf-8') as f:
                f.write(listing.amazon_aplus_content)
            print("💾 A+ content saved to 'aplus_preview.html' for viewing")
            
            # Show preview of sections
            if '🎯 Hero Section' in listing.amazon_aplus_content:
                print("✅ Contains Hero Section")
            if '⭐ Key Features' in listing.amazon_aplus_content:
                print("✅ Contains Features Section")
            if '📸 Image Requirements' in listing.amazon_aplus_content:
                print("✅ Contains Image Requirements")
            if '💰 PPC Strategy' in listing.amazon_aplus_content:
                print("✅ Contains PPC Strategy")
            if '🏢 Brand Summary' in listing.amazon_aplus_content:
                print("✅ Contains Brand Summary")
                
        elif listing.amazon_aplus_content.strip().startswith('{'):
            print("⚠️ Content is JSON format")
            print("Preview:", listing.amazon_aplus_content[:200], "...")
        else:
            print("❓ Unknown content format")
            print("Preview:", listing.amazon_aplus_content[:200], "...")
    else:
        print("❌ No A+ content found")

if __name__ == "__main__":
    view_aplus_html()