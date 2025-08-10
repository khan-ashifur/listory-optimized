"""
Comprehensive Occasion Testing Script for Amazon Listings
Tests every occasion and evaluates quality with Amazon best practices
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

class OccasionTester:
    def __init__(self):
        self.service = ListingGeneratorService()
        self.occasions = [
            "Valentine's Day",
            "Mother's Day", 
            "Christmas",
            "Birthday",
            "Wedding",
            "Anniversary",
            "Father's Day",
            "Easter",
            "Halloween",
            "Thanksgiving",
            "New Year",
            "Graduation",
            "Baby Shower",
            "Housewarming"
        ]
        self.test_results = []
        
    def evaluate_listing_quality(self, listing_data, occasion):
        """Evaluate listing quality based on Amazon best practices"""
        score = 0
        max_score = 100
        feedback = []
        
        # Parse the listing data
        try:
            if isinstance(listing_data, str):
                data = json.loads(listing_data)
            else:
                data = listing_data
        except:
            return 0, ["Failed to parse listing data"]
            
        # 1. Title Quality (20 points)
        title = data.get('productTitle', '') or data.get('amazonTitle', '')
        if title:
            # Check occasion mention
            if occasion.lower() in title.lower():
                score += 5
                feedback.append(f"✅ Title includes occasion: {occasion}")
            else:
                feedback.append(f"❌ Title missing occasion: {occasion}")
                
            # Check title length (optimal 150-200 chars)
            if 150 <= len(title) <= 200:
                score += 5
                feedback.append(f"✅ Title length optimal: {len(title)} chars")
            else:
                feedback.append(f"⚠️ Title length: {len(title)} chars (optimal: 150-200)")
                
            # Check for power words
            power_words = ['perfect', 'ideal', 'best', 'premium', 'quality', 'gift']
            if any(word in title.lower() for word in power_words):
                score += 5
                feedback.append("✅ Title contains power words")
            
            # Check brand presence
            if 'kzen' in title.lower():
                score += 5
                feedback.append("✅ Brand present in title")
        
        # 2. Bullet Points Quality (25 points)
        bullets = data.get('bulletPoints', [])
        if bullets:
            # Check occasion integration
            occasion_bullets = sum(1 for b in bullets if occasion.lower() in b.lower())
            if occasion_bullets >= 2:
                score += 10
                feedback.append(f"✅ {occasion_bullets} bullets mention {occasion}")
            elif occasion_bullets == 1:
                score += 5
                feedback.append(f"⚠️ Only 1 bullet mentions {occasion}")
            else:
                feedback.append(f"❌ No bullets mention {occasion}")
                
            # Check bullet structure
            if all(len(b) <= 500 for b in bullets):
                score += 5
                feedback.append("✅ All bullets within length limit")
                
            # Check for benefit-focused language
            benefit_keywords = ['perfect for', 'ideal for', 'great for', 'makes', 'helps', 'ensures']
            benefit_bullets = sum(1 for b in bullets if any(k in b.lower() for k in benefit_keywords))
            if benefit_bullets >= 3:
                score += 10
                feedback.append(f"✅ {benefit_bullets} benefit-focused bullets")
        
        # 3. Description Quality (20 points)
        description = data.get('productDescription', '')
        if description:
            # Check occasion context
            if occasion.lower() in description.lower():
                occasion_count = description.lower().count(occasion.lower())
                if occasion_count >= 2:
                    score += 10
                    feedback.append(f"✅ Description mentions {occasion} {occasion_count} times")
                else:
                    score += 5
                    feedback.append(f"⚠️ Description mentions {occasion} only once")
            else:
                feedback.append(f"❌ Description doesn't mention {occasion}")
                
            # Check for gift/occasion language
            gift_terms = ['gift', 'present', 'surprise', 'special', 'celebrate', 'perfect for']
            gift_count = sum(1 for term in gift_terms if term in description.lower())
            if gift_count >= 3:
                score += 10
                feedback.append(f"✅ Strong gift language ({gift_count} terms)")
        
        # 4. Keywords Quality (20 points)
        keywords = data.get('seoKeywords', []) or data.get('keywords', [])
        backend_keywords = data.get('backendKeywords', '')
        
        if keywords or backend_keywords:
            # Check occasion-specific keywords
            all_keywords = ' '.join(keywords) + ' ' + backend_keywords
            occasion_keywords = [
                f"{occasion.lower()} gift",
                f"{occasion.lower()} present", 
                f"best {occasion.lower()}",
                f"{occasion.lower()} ideas",
                f"perfect for {occasion.lower()}"
            ]
            
            found_occasion_keywords = sum(1 for k in occasion_keywords if k in all_keywords.lower())
            if found_occasion_keywords >= 3:
                score += 15
                feedback.append(f"✅ {found_occasion_keywords} occasion-specific keywords")
            elif found_occasion_keywords >= 1:
                score += 8
                feedback.append(f"⚠️ Only {found_occasion_keywords} occasion keywords")
            else:
                feedback.append(f"❌ No occasion-specific keywords")
                
            # Check keyword diversity
            if len(keywords) >= 15:
                score += 5
                feedback.append(f"✅ Good keyword diversity: {len(keywords)} keywords")
        
        # 5. A+ Content (15 points)
        aplus = data.get('aPlusContentPlan', {})
        if aplus:
            # Check if occasion is integrated in A+ content
            aplus_str = json.dumps(aplus).lower()
            if occasion.lower() in aplus_str:
                score += 10
                feedback.append(f"✅ A+ Content includes {occasion} theme")
            else:
                feedback.append(f"❌ A+ Content missing {occasion} theme")
                
            # Check for trust builders
            if 'trustBuilders' in data:
                score += 5
                feedback.append("✅ Trust builders present")
        
        # Calculate percentage score
        percentage = (score / max_score) * 100
        
        # Determine grade
        if percentage >= 90:
            grade = "A+ (Excellent)"
        elif percentage >= 80:
            grade = "A (Very Good)"
        elif percentage >= 70:
            grade = "B (Good)"
        elif percentage >= 60:
            grade = "C (Needs Improvement)"
        else:
            grade = "D (Poor)"
            
        return percentage, grade, feedback
    
    def test_occasion(self, occasion, product_id=None):
        """Test a single occasion"""
        print(f"\n{'='*60}")
        print(f"Testing: {occasion}")
        print(f"{'='*60}")
        
        try:
            # Use existing product or create test product
            if product_id:
                product = Product.objects.get(id=product_id)
            else:
                # Find or create test product
                product = Product.objects.filter(name__icontains="misting fan").first()
                if not product:
                    print("❌ No test product found")
                    return None
                    
            # Set the occasion
            product.occasion = occasion
            product.save()
            
            print(f"Product: {product.name}")
            print(f"Setting occasion: {occasion}")
            
            # Generate listing
            print("Generating listing...")
            listing = self.service.generate_listing(product.id, 'amazon')
            
            # Wait for generation
            time.sleep(2)
            
            # Retrieve the listing
            listing = GeneratedListing.objects.get(id=listing.id)
            
            # Access the actual content from the listing object
            content_field = None
            if hasattr(listing, 'listing_content'):
                content_field = listing.listing_content
            elif hasattr(listing, 'content'):
                content_field = listing.content
            else:
                # Try to get the content from other fields
                for field in ['ai_content', 'generated_content', 'data']:
                    if hasattr(listing, field):
                        content_field = getattr(listing, field)
                        break
            
            if listing.status == 'completed' and content_field:
                # Evaluate quality
                score, grade, feedback = self.evaluate_listing_quality(content_field, occasion)
                
                # Parse and display key elements
                try:
                    content = json.loads(content_field) if isinstance(content_field, str) else content_field
                    
                    print(f"\n📊 Quality Score: {score:.1f}% - {grade}")
                    print("\n📝 Title Preview:")
                    title = content.get('productTitle', '') or content.get('amazonTitle', '')
                    print(f"  {title[:100]}...")
                    
                    print("\n🎯 First Bullet:")
                    bullets = content.get('bulletPoints', [])
                    if bullets:
                        print(f"  {bullets[0][:150]}...")
                    
                    print("\n💡 Occasion Integration:")
                    for fb in feedback[:5]:  # Show top 5 feedback items
                        print(f"  {fb}")
                    
                    # Store result
                    self.test_results.append({
                        'occasion': occasion,
                        'score': score,
                        'grade': grade,
                        'feedback': feedback,
                        'title': title,
                        'success': True
                    })
                    
                except Exception as e:
                    print(f"❌ Error parsing content: {e}")
                    self.test_results.append({
                        'occasion': occasion,
                        'score': 0,
                        'grade': 'F',
                        'feedback': [f"Parse error: {e}"],
                        'success': False
                    })
            else:
                print(f"❌ Listing generation failed: {listing.status}")
                self.test_results.append({
                    'occasion': occasion,
                    'score': 0,
                    'grade': 'F',
                    'feedback': ["Generation failed"],
                    'success': False
                })
                
        except Exception as e:
            print(f"❌ Error testing {occasion}: {e}")
            self.test_results.append({
                'occasion': occasion,
                'score': 0,
                'grade': 'F',
                'feedback': [f"Test error: {e}"],
                'success': False
            })
            
        return self.test_results[-1] if self.test_results else None
    
    def run_all_tests(self, product_id=None):
        """Run tests for all occasions"""
        print("\n" + "="*60)
        print("COMPREHENSIVE OCCASION TESTING")
        print("="*60)
        
        for occasion in self.occasions:
            result = self.test_occasion(occasion, product_id)
            time.sleep(3)  # Delay between tests to avoid rate limiting
            
        # Generate summary report
        self.generate_report()
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("FINAL TEST REPORT")
        print("="*60)
        
        # Calculate averages
        successful_tests = [r for r in self.test_results if r['success']]
        if successful_tests:
            avg_score = sum(r['score'] for r in successful_tests) / len(successful_tests)
            
            print(f"\n📊 Overall Statistics:")
            print(f"  Tests Run: {len(self.test_results)}")
            print(f"  Successful: {len(successful_tests)}")
            print(f"  Failed: {len(self.test_results) - len(successful_tests)}")
            print(f"  Average Score: {avg_score:.1f}%")
            
            print(f"\n🏆 Individual Scores:")
            for result in self.test_results:
                status = "✅" if result['success'] else "❌"
                print(f"  {status} {result['occasion']:20} - {result['score']:.1f}% ({result['grade']})")
            
            # Identify best and worst
            if successful_tests:
                best = max(successful_tests, key=lambda x: x['score'])
                worst = min(successful_tests, key=lambda x: x['score'])
                
                print(f"\n⭐ Best Performance:")
                print(f"  {best['occasion']}: {best['score']:.1f}% - {best['grade']}")
                
                print(f"\n⚠️ Needs Most Improvement:")
                print(f"  {worst['occasion']}: {worst['score']:.1f}% - {worst['grade']}")
                
            # Common issues
            print(f"\n🔍 Common Issues Found:")
            all_feedback = []
            for result in self.test_results:
                all_feedback.extend([f for f in result['feedback'] if '❌' in f])
            
            from collections import Counter
            issue_types = Counter([f.split(':')[0] for f in all_feedback if ':' in f])
            for issue, count in issue_types.most_common(5):
                print(f"  • {issue}: {count} occurrences")
                
        else:
            print("❌ No successful tests to report")
            
        # Save report to file
        report_file = f"occasion_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n💾 Detailed report saved to: {report_file}")

if __name__ == "__main__":
    print("Starting Occasion Testing System...")
    
    # Check for specific product ID
    product_id = None
    if len(sys.argv) > 1:
        try:
            product_id = int(sys.argv[1])
            print(f"Using product ID: {product_id}")
        except:
            print("Invalid product ID, will use default product")
    
    tester = OccasionTester()
    
    # Option to test single occasion or all
    if len(sys.argv) > 2:
        occasion = sys.argv[2]
        if occasion in tester.occasions:
            tester.test_occasion(occasion, product_id)
        else:
            print(f"Invalid occasion. Choose from: {', '.join(tester.occasions)}")
    else:
        # Test all occasions
        tester.run_all_tests(product_id)