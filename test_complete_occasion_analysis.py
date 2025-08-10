"""
Complete Occasion Integration Test - ALL 15 Occasions
Tests title, bullets, description, A+ content, and keywords for each occasion
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

class CompleteOccasionTester:
    def __init__(self):
        self.service = ListingGeneratorService()
        self.all_occasions = [
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
            "Housewarming",
            "General" # Control test
        ]
        self.results = {}
        
    def deep_analyze_listing(self, listing, occasion):
        """Comprehensive analysis of all listing elements"""
        
        if not listing or listing.status != 'completed':
            return {
                'overall_score': 0,
                'title_score': 0,
                'bullets_score': 0,
                'description_score': 0,
                'aplus_score': 0,
                'keywords_score': 0,
                'issues': ['Listing generation failed']
            }
        
        occasion_lower = occasion.lower().replace("'s", "").replace("'", "")
        gift_terms = ['gift', 'present', 'perfect for', 'ideal for', 'great for']
        
        analysis = {
            'title_score': 0,
            'bullets_score': 0,
            'description_score': 0,
            'aplus_score': 0,
            'keywords_score': 0,
            'issues': []
        }
        
        # === TITLE ANALYSIS ===
        if listing.title:
            title_lower = listing.title.lower()
            
            # Check occasion mention in title
            if occasion_lower in title_lower:
                analysis['title_score'] += 40
            else:
                analysis['issues'].append(f"❌ Title missing '{occasion}' mention")
            
            # Check gift terms in title
            gift_count = sum(1 for term in gift_terms if term in title_lower)
            if gift_count > 0:
                analysis['title_score'] += 30
            else:
                analysis['issues'].append("❌ Title missing gift language")
            
            # Check title length optimization
            if 150 <= len(listing.title) <= 200:
                analysis['title_score'] += 30
            else:
                analysis['issues'].append(f"⚠️ Title length: {len(listing.title)} (optimal: 150-200)")
        else:
            analysis['issues'].append("❌ No title generated")
        
        # === BULLET POINTS ANALYSIS ===
        if listing.bullet_points:
            bullets_lower = listing.bullet_points.lower()
            
            # Check occasion mentions in bullets
            occasion_mentions = bullets_lower.count(occasion_lower)
            if occasion_mentions >= 2:
                analysis['bullets_score'] += 40
            elif occasion_mentions == 1:
                analysis['bullets_score'] += 20
            else:
                analysis['issues'].append(f"❌ Bullets missing '{occasion}' mentions")
            
            # Check gift language in bullets
            gift_mentions = sum(1 for term in gift_terms if term in bullets_lower)
            if gift_mentions >= 3:
                analysis['bullets_score'] += 40
            elif gift_mentions >= 1:
                analysis['bullets_score'] += 20
            else:
                analysis['issues'].append("❌ Bullets missing gift language")
            
            # Check for occasion-specific benefits
            bullets = listing.bullet_points.split('\n')
            if len(bullets) >= 5:
                analysis['bullets_score'] += 20
            else:
                analysis['issues'].append(f"⚠️ Only {len(bullets)} bullet points")
        else:
            analysis['issues'].append("❌ No bullet points generated")
        
        # === DESCRIPTION ANALYSIS ===
        if listing.long_description:
            desc_lower = listing.long_description.lower()
            
            # Check occasion mentions in description
            occasion_desc_mentions = desc_lower.count(occasion_lower)
            if occasion_desc_mentions >= 3:
                analysis['description_score'] += 40
            elif occasion_desc_mentions >= 1:
                analysis['description_score'] += 20
            else:
                analysis['issues'].append(f"❌ Description missing '{occasion}' mentions")
            
            # Check gift context in description
            gift_desc_mentions = sum(1 for term in gift_terms if term in desc_lower)
            if gift_desc_mentions >= 3:
                analysis['description_score'] += 40
            elif gift_desc_mentions >= 1:
                analysis['description_score'] += 20
            else:
                analysis['issues'].append("❌ Description missing gift context")
            
            # Check description length
            if 200 <= len(listing.long_description) <= 2000:
                analysis['description_score'] += 20
            else:
                analysis['issues'].append(f"⚠️ Description length: {len(listing.long_description)}")
        else:
            analysis['issues'].append("❌ No description generated")
        
        # === A+ CONTENT ANALYSIS ===
        aplus_fields = [listing.hero_title, listing.hero_content, listing.features, 
                       listing.trust_builders, listing.faqs]
        aplus_text = ' '.join([field for field in aplus_fields if field]).lower()
        
        if aplus_text:
            # Check occasion integration in A+ content
            aplus_occasion_mentions = aplus_text.count(occasion_lower)
            if aplus_occasion_mentions >= 3:
                analysis['aplus_score'] += 50
            elif aplus_occasion_mentions >= 1:
                analysis['aplus_score'] += 25
            else:
                analysis['issues'].append(f"❌ A+ Content missing '{occasion}' integration")
            
            # Check gift scenarios in A+ content
            aplus_gift_mentions = sum(1 for term in gift_terms if term in aplus_text)
            if aplus_gift_mentions >= 2:
                analysis['aplus_score'] += 50
            elif aplus_gift_mentions >= 1:
                analysis['aplus_score'] += 25
            else:
                analysis['issues'].append("❌ A+ Content missing gift scenarios")
        else:
            analysis['issues'].append("❌ No A+ Content generated")
        
        # === KEYWORDS ANALYSIS ===
        if listing.keywords:
            keywords_lower = listing.keywords.lower()
            
            # Check occasion-specific keywords
            occasion_keywords = keywords_lower.count(occasion_lower)
            if occasion_keywords >= 5:
                analysis['keywords_score'] += 50
            elif occasion_keywords >= 2:
                analysis['keywords_score'] += 30
            elif occasion_keywords >= 1:
                analysis['keywords_score'] += 15
            else:
                analysis['issues'].append(f"❌ Keywords missing '{occasion}' terms")
            
            # Check gift-related keywords
            gift_keywords = sum(1 for term in gift_terms if term in keywords_lower)
            if gift_keywords >= 3:
                analysis['keywords_score'] += 50
            elif gift_keywords >= 1:
                analysis['keywords_score'] += 25
            else:
                analysis['issues'].append("❌ Keywords missing gift terms")
        else:
            analysis['issues'].append("❌ No keywords generated")
        
        # Calculate overall score
        analysis['overall_score'] = (
            analysis['title_score'] + 
            analysis['bullets_score'] + 
            analysis['description_score'] + 
            analysis['aplus_score'] + 
            analysis['keywords_score']
        ) / 5
        
        return analysis
    
    def test_single_occasion(self, occasion):
        """Test a single occasion comprehensively"""
        print(f"\n{'='*80}")
        print(f"🎁 TESTING: {occasion.upper()}")
        print(f"{'='*80}")
        
        try:
            # Find test product
            product = Product.objects.filter(name__icontains="misting fan").first()
            if not product:
                print("❌ No test product found")
                return None
                
            # Set the occasion
            if occasion == "General":
                product.occasion = None
            else:
                product.occasion = occasion
            product.save()
            
            print(f"Product: {product.name}")
            print(f"Occasion: {occasion}")
            print("Generating listing...")
            
            # Generate listing
            self.service.generate_listing(product.id, 'amazon')
            
            # Wait for generation
            time.sleep(5)
            
            # Get the listing
            listing = GeneratedListing.objects.filter(
                product=product,
                platform='amazon'
            ).order_by('-created_at').first()
            
            # Analyze the listing
            analysis = self.deep_analyze_listing(listing, occasion)
            
            # Display results
            print(f"\n📊 ANALYSIS RESULTS:")
            print(f"  Overall Score: {analysis['overall_score']:.1f}/100")
            print(f"  📝 Title Score: {analysis['title_score']:.1f}/100")
            print(f"  🎯 Bullets Score: {analysis['bullets_score']:.1f}/100") 
            print(f"  📄 Description Score: {analysis['description_score']:.1f}/100")
            print(f"  ⭐ A+ Content Score: {analysis['aplus_score']:.1f}/100")
            print(f"  🔍 Keywords Score: {analysis['keywords_score']:.1f}/100")
            
            if listing and listing.status == 'completed':
                # Show sample content
                if listing.title:
                    print(f"\n📝 TITLE: {listing.title[:120]}...")
                
                if listing.bullet_points:
                    bullets = listing.bullet_points.split('\n')[:2]
                    print(f"\n🎯 BULLETS:")
                    for i, bullet in enumerate(bullets):
                        print(f"   {i+1}. {bullet[:100]}...")
                
                if listing.hero_title:
                    print(f"\n⭐ A+ HERO: {listing.hero_title[:80]}...")
                
                if listing.keywords:
                    keywords = listing.keywords.split(',')[:10]
                    print(f"\n🔍 KEYWORDS: {', '.join(k.strip() for k in keywords)}...")
            
            # Show issues
            if analysis['issues']:
                print(f"\n⚠️ ISSUES FOUND:")
                for issue in analysis['issues'][:5]:  # Show top 5 issues
                    print(f"   {issue}")
            
            self.results[occasion] = analysis
            return analysis
            
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            self.results[occasion] = {'overall_score': 0, 'issues': [f'Error: {e}']}
            return None
    
    def run_complete_test(self):
        """Run complete test for all occasions"""
        print("🚀 STARTING COMPLETE OCCASION INTEGRATION TEST")
        print("Testing all 15 occasions for:")
        print("- Title occasion integration")
        print("- Bullet points occasion mentions")
        print("- Description occasion context")
        print("- A+ Content occasion blending")
        print("- Keywords occasion optimization")
        
        for occasion in self.all_occasions:
            result = self.test_single_occasion(occasion)
            time.sleep(3)  # Brief pause between tests
        
        # Generate comprehensive report
        self.generate_final_report()
    
    def generate_final_report(self):
        """Generate comprehensive final report"""
        print(f"\n{'='*80}")
        print("🏆 COMPLETE OCCASION INTEGRATION REPORT")
        print(f"{'='*80}")
        
        if not self.results:
            print("❌ No results to report")
            return
        
        # Calculate statistics
        scores = []
        perfect_scores = 0
        good_scores = 0
        poor_scores = 0
        
        print(f"\n📊 INDIVIDUAL RESULTS:")
        print("-" * 80)
        
        for occasion, analysis in self.results.items():
            score = analysis.get('overall_score', 0)
            scores.append(score)
            
            # Grade calculation
            if score >= 90:
                grade = "A+"
                status = "✅"
                perfect_scores += 1
            elif score >= 80:
                grade = "A"
                status = "✅"
                good_scores += 1
            elif score >= 70:
                grade = "B"
                status = "⚠️"
                good_scores += 1
            elif score >= 60:
                grade = "C"
                status = "⚠️"
            else:
                grade = "D"
                status = "❌"
                poor_scores += 1
            
            print(f"{status} {occasion:20} - {score:5.1f}/100 (Grade: {grade})")
        
        # Overall statistics
        avg_score = sum(scores) / len(scores) if scores else 0
        print(f"\n📈 OVERALL STATISTICS:")
        print(f"  Average Score: {avg_score:.1f}/100")
        print(f"  Perfect (90+): {perfect_scores}")
        print(f"  Good (70-89):  {good_scores}")
        print(f"  Poor (<70):    {poor_scores}")
        
        # Detailed breakdown by category
        categories = ['title_score', 'bullets_score', 'description_score', 'aplus_score', 'keywords_score']
        category_names = ['Title', 'Bullets', 'Description', 'A+ Content', 'Keywords']
        
        print(f"\n🔍 CATEGORY BREAKDOWN:")
        for i, category in enumerate(categories):
            cat_scores = [result.get(category, 0) for result in self.results.values() if isinstance(result, dict)]
            cat_avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
            print(f"  {category_names[i]:12}: {cat_avg:5.1f}/100")
        
        # Common issues
        all_issues = []
        for result in self.results.values():
            if isinstance(result, dict) and 'issues' in result:
                all_issues.extend(result['issues'])
        
        if all_issues:
            from collections import Counter
            issue_counts = Counter(all_issues)
            print(f"\n⚠️ MOST COMMON ISSUES:")
            for issue, count in issue_counts.most_common(5):
                print(f"  {count}x - {issue}")
        
        # Final recommendation
        print(f"\n🎯 RECOMMENDATION:")
        if avg_score >= 85:
            print("✅ EXCELLENT: Occasion integration is working perfectly!")
        elif avg_score >= 75:
            print("⚠️ GOOD: Occasion integration is solid but has room for improvement")
        elif avg_score >= 60:
            print("⚠️ NEEDS IMPROVEMENT: Several issues need to be addressed")
        else:
            print("❌ CRITICAL: Major fixes needed for proper occasion integration")
        
        # Save detailed report
        report_file = f"complete_occasion_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n💾 Detailed report saved: {report_file}")
        
        return avg_score

if __name__ == "__main__":
    print("Starting Complete Occasion Integration Test...")
    tester = CompleteOccasionTester()
    
    # Option to test single occasion or all
    if len(sys.argv) > 1:
        occasion = sys.argv[1]
        if occasion in tester.all_occasions:
            tester.test_single_occasion(occasion)
        else:
            print(f"Invalid occasion. Choose from: {', '.join(tester.all_occasions)}")
    else:
        # Test all occasions
        final_score = tester.run_complete_test()
        print(f"\nFinal Average Score: {final_score:.1f}/100")