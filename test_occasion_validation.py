"""
Test Script to Validate Enhanced Occasion Integration
Tests each occasion and evaluates quality improvements
"""

import os
import sys
import django
import json
import time
from datetime import datetime

# Add the backend directory to the Python path
sys.path.insert(0, r'C:\Users\khana\Desktop\listory-ai\backend')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "listory.settings")
django.setup()

from apps.core.models import Product
from apps.listings.services import ListingGeneratorService
from apps.listings.models import GeneratedListing

class OccasionValidator:
    def __init__(self):
        self.service = ListingGeneratorService()
        # Test 3 key occasions for quick validation
        self.test_occasions = [
            "Valentine's Day",
            "Christmas",
            "Mother's Day"
        ]
        
    def test_occasion(self, occasion):
        """Test a single occasion with enhanced validation"""
        print(f"\n{'='*60}")
        print(f"🎁 Testing: {occasion}")
        print(f"{'='*60}")
        
        try:
            # Find test product
            product = Product.objects.filter(name__icontains="misting fan").first()
            if not product:
                print("❌ No test product found")
                return None
                
            # Set the occasion
            product.occasion = occasion
            product.save()
            
            print(f"Product: {product.name}")
            print(f"Occasion: {occasion}")
            print("Generating listing with enhanced occasion integration...")
            
            # Generate listing
            self.service.generate_listing(product.id, 'amazon')
            
            # Wait for generation
            time.sleep(5)
            
            # Get the listing
            listing = GeneratedListing.objects.filter(
                product=product,
                platform='amazon'
            ).order_by('-created_at').first()
            
            if listing and listing.status == 'completed':
                print("✅ Listing generated successfully")
                
                # Evaluate occasion integration
                occasion_lower = occasion.lower().replace("'s", "").replace("'", "")
                score = 0
                feedback = []
                
                # Check title
                if listing.title:
                    if occasion_lower in listing.title.lower():
                        score += 25
                        feedback.append(f"✅ Title includes {occasion}")
                        print(f"\n📝 Title: {listing.title[:100]}...")
                    else:
                        feedback.append(f"❌ Title missing {occasion}")
                
                # Check bullets
                if listing.bullet_points:
                    bullets_lower = listing.bullet_points.lower()
                    count = bullets_lower.count(occasion_lower)
                    if count >= 2:
                        score += 25
                        feedback.append(f"✅ Bullets mention {occasion} {count} times")
                    elif count == 1:
                        score += 15
                        feedback.append(f"⚠️ Bullets mention {occasion} only once")
                    else:
                        feedback.append(f"❌ Bullets missing {occasion}")
                    
                    # Show first bullet
                    bullets = listing.bullet_points.split('\n')
                    if bullets:
                        print(f"\n🎯 First Bullet: {bullets[0][:150]}...")
                
                # Check description
                if listing.long_description:
                    desc_lower = listing.long_description.lower()
                    count = desc_lower.count(occasion_lower)
                    if count >= 3:
                        score += 25
                        feedback.append(f"✅ Description mentions {occasion} {count} times")
                    elif count >= 1:
                        score += 15
                        feedback.append(f"⚠️ Description mentions {occasion} only {count} time(s)")
                    else:
                        feedback.append(f"❌ Description missing {occasion}")
                
                # Check keywords
                if listing.keywords:
                    keywords_lower = listing.keywords.lower()
                    gift_terms = ['gift', 'present', 'special', 'perfect for']
                    occasion_keywords = sum(1 for term in gift_terms if term in keywords_lower and occasion_lower in keywords_lower)
                    if occasion_keywords >= 3:
                        score += 25
                        feedback.append(f"✅ Strong occasion keywords ({occasion_keywords} gift terms)")
                    elif occasion_keywords >= 1:
                        score += 15
                        feedback.append(f"⚠️ Some occasion keywords ({occasion_keywords} gift terms)")
                    else:
                        feedback.append(f"❌ Weak occasion keywords")
                
                print(f"\n📊 Occasion Integration Score: {score}/100")
                print("\n💡 Detailed Evaluation:")
                for fb in feedback:
                    print(f"  {fb}")
                
                # Check quality scores
                if listing.quality_score:
                    print(f"\n📈 Quality Metrics:")
                    print(f"  Overall Quality: {listing.quality_score:.1f}/10")
                    if listing.emotion_score:
                        print(f"  Emotional Engagement: {listing.emotion_score:.1f}/10")
                    if listing.conversion_score:
                        print(f"  Conversion Optimization: {listing.conversion_score:.1f}/10")
                
                return score
                
            else:
                print(f"❌ Listing generation failed: {listing.status if listing else 'Not found'}")
                return 0
                
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return 0
    
    def run_validation(self):
        """Run validation for all test occasions"""
        print("\n" + "="*60)
        print("🎄 ENHANCED OCCASION INTEGRATION VALIDATION")
        print("="*60)
        print("\nTesting enhanced occasion-specific optimizations...")
        
        results = []
        for occasion in self.test_occasions:
            score = self.test_occasion(occasion)
            results.append((occasion, score))
            time.sleep(3)
        
        # Summary
        print("\n" + "="*60)
        print("📊 VALIDATION SUMMARY")
        print("="*60)
        
        total_score = 0
        for occasion, score in results:
            if score is not None:
                total_score += score
                grade = "A+" if score >= 90 else "A" if score >= 80 else "B" if score >= 70 else "C" if score >= 60 else "D"
                status = "✅" if score >= 80 else "⚠️" if score >= 60 else "❌"
                print(f"{status} {occasion:20} - {score}/100 (Grade: {grade})")
        
        avg_score = total_score / len(results) if results else 0
        print(f"\n🏆 Average Score: {avg_score:.1f}/100")
        
        if avg_score >= 80:
            print("✅ EXCELLENT: Occasion integration is working perfectly!")
        elif avg_score >= 60:
            print("⚠️ GOOD: Occasion integration is working but could be improved")
        else:
            print("❌ NEEDS WORK: Occasion integration needs significant improvement")
        
        return avg_score

if __name__ == "__main__":
    print("Starting Enhanced Occasion Validation...")
    validator = OccasionValidator()
    
    # Run the validation
    avg_score = validator.run_validation()
    
    if avg_score >= 80:
        print("\n🎉 SUCCESS: Amazon occasion integration is now optimized to 10/10!")
    else:
        print("\n⚠️ Additional optimization may be needed.")