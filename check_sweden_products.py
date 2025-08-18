#!/usr/bin/env python
"""
Check Sweden products in database
"""
import os
import sys
import django

# Add backend directory to path
sys.path.insert(0, 'C:/Users/khana/Desktop/listory-ai/backend')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product

def check_sweden_products():
    # Check Sweden products
    sweden_products = Product.objects.filter(marketplace='se')
    print(f"Sweden products count: {sweden_products.count()}")
    
    if sweden_products.exists():
        for p in sweden_products[:3]:
            print(f"ID: {p.id}, Name: {p.name}, Categories: {p.categories}")
    else:
        print("No Sweden products found")
    
    # Check if any listings exist for Sweden
    from apps.listings.models import GeneratedListing
    sweden_listings = GeneratedListing.objects.filter(product__marketplace='se')
    print(f"\nSweden listings count: {sweden_listings.count()}")
    
    if sweden_listings.exists():
        latest = sweden_listings.order_by('-created_at').first()
        print(f"Latest listing: {latest.product.name} (Quality: {latest.quality_score})")
    
    return sweden_products.first() if sweden_products.exists() else None

if __name__ == "__main__":
    check_sweden_products()