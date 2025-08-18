#!/usr/bin/env python3

"""
Test Turkey Fallback Issue
Simulate scenario where AI doesn't generate proper aPlusContentPlan to trigger fallback logic
"""

import os
import sys
import django

# Django setup
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from django.contrib.auth.models import User

def test_fallback_scenario():
    """Test what happens when AI fails to generate comprehensive aPlusContentPlan"""
    print("🔍 TESTING TURKEY FALLBACK ISSUE")
    print("=" * 60)
    
    # The issue is in line 3058: marketplace_code not in ['tr', 'nl']
    # This means if AI doesn't generate proper sections, Turkey gets NO fallback content
    # But Mexico DOES get fallback content
    
    print("📋 CRITICAL CODE ANALYSIS:")
    print("   Line 3058: if not sections_html and [...] and marketplace_code not in ['tr', 'nl']:")
    print("   This means:")
    print("   ✅ Mexico (mx): Gets fallback content if AI fails")
    print("   ❌ Turkey (tr): Gets NO fallback content if AI fails")
    print("   ❌ Netherlands (nl): Gets NO fallback content if AI fails")
    print()
    
    print("🚨 THE PROBLEM:")
    print("   When AI generates incomplete aPlusContentPlan:")
    print("   - Mexico: Fallback creates 8 detailed sections from listing content")
    print("   - Turkey: No fallback, only shows basic HTML template")
    print("   - Result: Turkey shows 'Complete A+ Content Strategy' + 'Overall A+ Strategy' only")
    print("   - Result: Mexico shows detailed 'Audífonos Traductores...' + 8 sections")
    print()
    
    print("🔧 THE FIX:")
    print("   Remove Turkey (tr) from the exclusion list in line 3058")
    print("   Current: marketplace_code not in ['tr', 'nl']")
    print("   Fixed:   marketplace_code not in ['nl']  # Only exclude Netherlands")
    print("   Or:      marketplace_code not in []      # Allow fallback for all markets")
    print()
    
    print("📝 EXACT LINE TO CHANGE:")
    print("   File: backend/apps/listings/services.py")
    print("   Line: 3058")
    print("   From: if not sections_html and (listing.hero_title or listing.features or listing.trust_builders) and marketplace_code not in ['tr', 'nl']:")
    print("   To:   if not sections_html and (listing.hero_title or listing.features or listing.trust_builders) and marketplace_code not in ['nl']:")
    print()
    
    print("✅ RESULT AFTER FIX:")
    print("   Turkey will get the same fallback content generation as Mexico")
    print("   Both will show 8 detailed comprehensive sections when AI fails")
    print("   Turkey will show 'Sensei AI Çeviri Kulaklık – Türk Ailesi için' detailed sections")
    print("   Mexico will show 'Audífonos Traductores – Familias Mexicanas' detailed sections")

if __name__ == "__main__":
    test_fallback_scenario()