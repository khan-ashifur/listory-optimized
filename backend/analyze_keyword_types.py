#!/usr/bin/env python3
"""
Analyze how keywords are being categorized by word count.
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

def analyze_keyword_types():
    """Analyze how keywords are being categorized by word count."""
    print("🔍 KEYWORD TYPE ANALYSIS")
    print("=" * 50)
    
    # Get the most recent listing
    listing = GeneratedListing.objects.filter(platform='amazon').order_by('-created_at').first()
    
    if not listing:
        print("❌ No Amazon listings found")
        return
    
    print(f"📄 Listing: {listing.product.name}")
    print(f"📅 Created: {listing.created_at}")
    
    if not listing.keywords:
        print("❌ No keywords found in listing")
        return
    
    print(f"\n🔑 KEYWORD ANALYSIS:")
    print("-" * 30)
    
    # Split keywords and analyze
    all_keywords = [k.strip() for k in listing.keywords.split(',') if k.strip()]
    
    short_tail = []  # <= 2 words
    long_tail = []   # > 2 words
    
    for keyword in all_keywords:
        word_count = len(keyword.split())
        if word_count <= 2:
            short_tail.append(keyword)
        else:
            long_tail.append(keyword)
    
    print(f"📊 TOTAL KEYWORDS: {len(all_keywords)}")
    print(f"📌 SHORT-TAIL (≤2 words): {len(short_tail)}")
    print(f"📍 LONG-TAIL (>2 words): {len(long_tail)}")
    
    print(f"\n📌 SHORT-TAIL KEYWORDS ({len(short_tail)}):")
    print("-" * 25)
    if short_tail:
        for i, keyword in enumerate(short_tail, 1):
            word_count = len(keyword.split())
            print(f"{i:2d}. {keyword} ({word_count} words)")
    else:
        print("❌ NO SHORT-TAIL KEYWORDS FOUND!")
        print("🔧 This explains why frontend shows 0 or 1 short-tail keyword")
    
    print(f"\n📍 LONG-TAIL KEYWORDS ({len(long_tail)}):")
    print("-" * 25)
    for i, keyword in enumerate(long_tail[:10], 1):  # Show first 10
        word_count = len(keyword.split())
        print(f"{i:2d}. {keyword} ({word_count} words)")
    if len(long_tail) > 10:
        print(f"    ... and {len(long_tail) - 10} more")
    
    print(f"\n🎯 FRONTEND DISPLAY LOGIC:")
    print("-" * 30)
    print(f"Short-tail display: .filter(k => k.split(' ').length <= 2)")
    print(f"Long-tail display:  .filter(k => k.split(' ').length > 2)")
    print(f"")
    print(f"Result in frontend:")
    print(f"• Short-tail counter: {len(short_tail)}")
    print(f"• Long-tail counter: {len(long_tail)}")
    
    if len(short_tail) <= 1:
        print(f"\n🔧 ISSUE IDENTIFIED:")
        print(f"The AI is generating mostly 3+ word keywords, which are")
        print(f"classified as 'long-tail' by the frontend filter.")
        print(f"Need to adjust AI prompt to generate more 1-2 word keywords.")
    
    return short_tail, long_tail

if __name__ == "__main__":
    analyze_keyword_types()