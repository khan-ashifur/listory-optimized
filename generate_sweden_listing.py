#!/usr/bin/env python
"""
Generate fresh Sweden listing and evaluate comprehensively
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

from apps.core.models import Product
from apps.listings.models import GeneratedListing
from apps.listings.services import ListingGeneratorService

def generate_fresh_sweden_listing():
    """Generate fresh Sweden listing for evaluation"""
    
    # Get a Sweden product
    sweden_products = Product.objects.filter(marketplace='se')
    if not sweden_products.exists():
        print("No Sweden products found!")
        return None
    
    # Use the first product
    product = sweden_products.first()
    print(f"Generating listing for: {product.name}")
    print(f"Marketplace: {product.marketplace}")
    print(f"Brand: {product.brand_name}")
    
    # Initialize service
    service = ListingGeneratorService()
    
    # Create new listing
    listing = GeneratedListing.objects.create(
        product=product,
        platform="amazon",
        title="",
        bullet_points="",
        long_description="",
        quality_score=0,
        emotion_score=0
    )
    
    print(f"Created listing with ID: {listing.id}")
    
    try:
        # Generate the listing
        service._generate_amazon_listing(product, listing)
        
        print(f"\n=== GENERATION RESULT ===")
        
        # Refresh from database
        listing.refresh_from_db()
        
        # Check if generation was successful by looking at content
        print(f"Title exists: {bool(listing.title)}")
        print(f"Bullet points exist: {bool(listing.bullet_points)}")
        
        if listing.title and listing.bullet_points and len(listing.title) > 10:
            
            print(f"\n=== LISTING QUALITY SCORES ===")
            print(f"Quality Score: {listing.quality_score}")
            print(f"Emotion Score: {listing.emotion_score}")
            
            print(f"\n=== GENERATED CONTENT ===")
            print(f"Title: {listing.title[:100]}...")
            print(f"Bullets: {listing.bullet_points[:200]}...")
            print(f"Description: {listing.long_description[:200]}...")
            
            # Check A+ content
            if listing.amazon_aplus_content:
                print(f"\n=== A+ CONTENT ===")
                try:
                    # A+ content might be HTML or JSON
                    if listing.amazon_aplus_content.strip().startswith('{'):
                        aplus_data = json.loads(listing.amazon_aplus_content)
                        if isinstance(aplus_data, dict) and 'aPlusContentPlan' in aplus_data:
                            plan = aplus_data['aPlusContentPlan']
                            print(f"A+ sections found: {len(plan)}")
                            for section_name in plan.keys():
                                print(f"  ✅ {section_name}")
                                if 'title' in plan[section_name]:
                                    title = plan[section_name]['title']
                                    print(f"     Title: {title[:80]}...")
                    else:
                        # HTML content
                        print(f"A+ HTML content: {len(listing.amazon_aplus_content)} characters")
                        print(f"Preview: {listing.amazon_aplus_content[:200]}...")
                except Exception as e:
                    print(f"A+ content parsing error: {e}")
                    print(f"Raw A+ content: {listing.amazon_aplus_content[:300]}...")
            else:
                print("❌ No A+ content generated")
                
            # Check keywords
            if listing.amazon_keywords:
                keywords = listing.amazon_keywords.split(',')
                print(f"\n=== KEYWORDS ===")
                print(f"Amazon Keywords count: {len(keywords)}")
                print(f"Sample keywords: {', '.join(keywords[:5])}")
            
            if listing.amazon_backend_keywords:
                backend_keywords = listing.amazon_backend_keywords.split(',')
                print(f"Backend Keywords count: {len(backend_keywords)}")
                print(f"Sample backend keywords: {', '.join(backend_keywords[:5])}")
            
            return listing
        else:
            print(f"Generation failed: No content generated")
            return None
            
    except Exception as e:
        print(f"Error during generation: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    generate_fresh_sweden_listing()