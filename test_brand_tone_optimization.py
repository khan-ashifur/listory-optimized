"""
Comprehensive Brand Tone Testing & Optimization System
Tests all 6 brand tones and evaluates quality to achieve 10/10
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

class BrandToneOptimizer:
    def __init__(self):
        self.service = ListingGeneratorService()
        self.brand_tones = [
            "professional",
            "casual", 
            "luxury",
            "playful",
            "minimal",
            "bold"
        ]
        self.results = {}
        
        # Brand tone quality criteria
        self.tone_criteria = {
            "professional": {
                "title_keywords": ["professional", "industry", "proven", "expert", "reliable", "advanced", "premium"],
                "avoid_words": ["revolutionary", "game-changing", "cutting-edge", "state-of-the-art"],
                "voice_style": "authoritative, credible, expertise-focused",
                "bullet_style": "varied formats, professional insights, specific details",
                "description_approach": "professional recommendation, colleague-to-colleague"
            },
            "casual": {
                "title_keywords": ["easy", "simple", "love", "perfect", "great", "awesome", "friendly"],
                "avoid_words": ["pretentious", "complex", "sophisticated", "elite"],
                "voice_style": "friendly, conversational, relatable",
                "bullet_style": "chatty, personal, everyday language",
                "description_approach": "friend recommendation, makes life easier"
            },
            "luxury": {
                "title_keywords": ["premium", "elegant", "sophisticated", "exclusive", "luxury", "elevated", "refined"],
                "avoid_words": ["cheap", "basic", "simple", "ordinary"],
                "voice_style": "sophisticated, aspirational, sensory",
                "bullet_style": "refined language, quality focus, transformational",
                "description_approach": "sophisticated connoisseur, quality appreciation"
            },
            "playful": {
                "title_keywords": ["fun", "innovative", "smart", "clever", "ready", "amazing", "cool"],
                "avoid_words": ["boring", "serious", "corporate", "stuffy"],
                "voice_style": "fun, confident, slightly cheeky",
                "bullet_style": "creative, energetic, balance innovation with accessibility",
                "description_approach": "tech-savvy friend, makes complex simple"
            },
            "minimal": {
                "title_keywords": ["simply", "pure", "clean", "essential", "clear", "focused", "quality"],
                "avoid_words": ["complicated", "flashy", "excessive", "over-the-top"],
                "voice_style": "clear, concise, purposeful",
                "bullet_style": "clean, minimal, purpose-focused",
                "description_approach": "thoughtful minimalist, values quality over quantity"
            },
            "bold": {
                "title_keywords": ["power", "dominate", "unleash", "transform", "strong", "confident", "leader"],
                "avoid_words": ["weak", "passive", "gentle", "subtle"],
                "voice_style": "strong, decisive, powerful",
                "bullet_style": "impactful, action-oriented, transformation-focused",
                "description_approach": "leader who inspires action, strength and transformation"
            }
        }
    
    def evaluate_brand_tone_quality(self, listing, brand_tone):
        """Comprehensive evaluation of brand tone adherence"""
        
        if not listing or listing.status != 'completed':
            return {
                'overall_score': 0,
                'title_score': 0,
                'bullets_score': 0,
                'description_score': 0,
                'voice_consistency': 0,
                'issues': ['Listing generation failed']
            }
        
        criteria = self.tone_criteria.get(brand_tone, self.tone_criteria['professional'])
        
        analysis = {
            'title_score': 0,
            'bullets_score': 0,
            'description_score': 0,
            'voice_consistency': 0,
            'issues': []
        }
        
        # Combine all text for analysis
        all_text = ' '.join([
            listing.title or '',
            listing.bullet_points or '',
            listing.long_description or ''
        ]).lower()
        
        # === TITLE ANALYSIS ===
        if listing.title:
            title_lower = listing.title.lower()
            
            # Check for appropriate keywords
            tone_keywords_found = sum(1 for kw in criteria['title_keywords'] if kw in title_lower)
            if tone_keywords_found >= 2:
                analysis['title_score'] += 40
            elif tone_keywords_found >= 1:
                analysis['title_score'] += 20
            else:
                analysis['issues'].append(f"❌ Title missing {brand_tone} tone keywords")
            
            # Check for avoided words
            avoid_words_found = sum(1 for word in criteria['avoid_words'] if word in title_lower)
            if avoid_words_found == 0:
                analysis['title_score'] += 30
            else:
                analysis['issues'].append(f"❌ Title contains inappropriate words for {brand_tone} tone")
            
            # Check title length and structure
            if 150 <= len(listing.title) <= 200:
                analysis['title_score'] += 30
            else:
                analysis['issues'].append(f"⚠️ Title length: {len(listing.title)} (optimal: 150-200)")
        else:
            analysis['issues'].append("❌ No title generated")
        
        # === BULLET POINTS ANALYSIS ===
        if listing.bullet_points:
            bullets_lower = listing.bullet_points.lower()
            
            # Check for tone-appropriate language
            tone_language = sum(1 for kw in criteria['title_keywords'] if kw in bullets_lower)
            if tone_language >= 3:
                analysis['bullets_score'] += 40
            elif tone_language >= 1:
                analysis['bullets_score'] += 20
            else:
                analysis['issues'].append(f"❌ Bullets missing {brand_tone} tone language")
            
            # Check bullet variety and structure
            bullets = listing.bullet_points.split('\n')
            if len(bullets) >= 5:
                analysis['bullets_score'] += 30
            
            # Check for appropriate formatting variety
            labels = [bullet.split(':')[0] for bullet in bullets if ':' in bullet]
            if len(set(labels)) == len(labels):  # All unique labels
                analysis['bullets_score'] += 30
            else:
                analysis['issues'].append("⚠️ Bullet labels not sufficiently varied")
        else:
            analysis['issues'].append("❌ No bullet points generated")
        
        # === DESCRIPTION ANALYSIS ===
        if listing.long_description:
            desc_lower = listing.long_description.lower()
            
            # Check for tone consistency
            tone_consistency = sum(1 for kw in criteria['title_keywords'] if kw in desc_lower)
            if tone_consistency >= 2:
                analysis['description_score'] += 40
            elif tone_consistency >= 1:
                analysis['description_score'] += 20
            else:
                analysis['issues'].append(f"❌ Description lacks {brand_tone} tone consistency")
            
            # Check description length and structure
            if 1200 <= len(listing.long_description) <= 2000:
                analysis['description_score'] += 30
            
            # Check for avoided clichés
            avoid_desc = sum(1 for word in criteria['avoid_words'] if word in desc_lower)
            if avoid_desc == 0:
                analysis['description_score'] += 30
            else:
                analysis['issues'].append(f"❌ Description contains inappropriate language")
        else:
            analysis['issues'].append("❌ No description generated")
        
        # === VOICE CONSISTENCY ANALYSIS ===
        # Check overall voice consistency across all elements
        if all([listing.title, listing.bullet_points, listing.long_description]):
            # Advanced analysis for voice consistency
            total_tone_keywords = sum(1 for kw in criteria['title_keywords'] if kw in all_text)
            total_avoid_words = sum(1 for word in criteria['avoid_words'] if word in all_text)
            
            if total_tone_keywords >= 5 and total_avoid_words == 0:
                analysis['voice_consistency'] = 100
            elif total_tone_keywords >= 3 and total_avoid_words <= 1:
                analysis['voice_consistency'] = 70
            elif total_tone_keywords >= 1:
                analysis['voice_consistency'] = 40
            else:
                analysis['voice_consistency'] = 0
                analysis['issues'].append(f"❌ Poor voice consistency for {brand_tone}")
        
        # Calculate overall score
        analysis['overall_score'] = (
            analysis['title_score'] + 
            analysis['bullets_score'] + 
            analysis['description_score'] + 
            analysis['voice_consistency']
        ) / 4
        
        return analysis
    
    def test_brand_tone(self, brand_tone):
        """Test a single brand tone comprehensively"""
        print(f"\n{'='*70}")
        print(f"🎨 TESTING BRAND TONE: {brand_tone.upper()}")
        print(f"{'='*70}")
        
        criteria = self.tone_criteria.get(brand_tone)
        print(f"Expected Voice: {criteria['voice_style']}")
        print(f"Key Words: {', '.join(criteria['title_keywords'][:5])}")
        print(f"Avoid: {', '.join(criteria['avoid_words'][:3])}")
        
        try:
            # Find test product
            product = Product.objects.filter(name__icontains="misting fan").first()
            if not product:
                print("❌ No test product found")
                return None
                
            # Set the brand tone
            product.brand_tone = brand_tone
            if hasattr(product, 'occasion'):
                product.occasion = 'None'  # Test regular (non-occasion) listing
            product.save()
            
            print(f"\nProduct: {product.name}")
            print(f"Brand Tone: {brand_tone}")
            print("Generating listing...")
            
            # Generate listing
            self.service.generate_listing(product.id, 'amazon')
            
            # Wait for generation
            time.sleep(6)
            
            # Get the listing
            listing = GeneratedListing.objects.filter(
                product=product,
                platform='amazon'
            ).order_by('-created_at').first()
            
            if listing and listing.status == 'completed':
                # Evaluate brand tone adherence
                analysis = self.evaluate_brand_tone_quality(listing, brand_tone)
                
                # Display results
                print(f"\n📊 BRAND TONE QUALITY ANALYSIS:")
                print(f"  📝 Title: {analysis['title_score']:.1f}/100 {'✅' if analysis['title_score'] >= 80 else '⚠️' if analysis['title_score'] >= 60 else '❌'}")
                print(f"  🎯 Bullets: {analysis['bullets_score']:.1f}/100 {'✅' if analysis['bullets_score'] >= 80 else '⚠️' if analysis['bullets_score'] >= 60 else '❌'}")
                print(f"  📄 Description: {analysis['description_score']:.1f}/100 {'✅' if analysis['description_score'] >= 80 else '⚠️' if analysis['description_score'] >= 60 else '❌'}")
                print(f"  🎭 Voice Consistency: {analysis['voice_consistency']:.1f}/100 {'✅' if analysis['voice_consistency'] >= 80 else '⚠️' if analysis['voice_consistency'] >= 60 else '❌'}")
                print(f"  🏆 Overall Score: {analysis['overall_score']:.1f}/100 {'✅' if analysis['overall_score'] >= 80 else '⚠️' if analysis['overall_score'] >= 60 else '❌'}")
                
                # Show sample content
                if listing.title:
                    print(f"\n📝 TITLE: {listing.title}")
                
                if listing.bullet_points:
                    bullets = listing.bullet_points.split('\n')[:2]
                    print(f"\n🎯 SAMPLE BULLETS:")
                    for i, bullet in enumerate(bullets):
                        print(f"   {i+1}. {bullet[:100]}...")
                
                if listing.long_description:
                    print(f"\n📄 DESCRIPTION PREVIEW: {listing.long_description[:200]}...")
                
                # Show issues
                if analysis['issues']:
                    print(f"\n⚠️ ISSUES FOUND:")
                    for issue in analysis['issues'][:5]:
                        print(f"   {issue}")
                
                self.results[brand_tone] = analysis
                return analysis
                
            else:
                print(f"❌ Listing generation failed: {listing.status if listing else 'Not found'}")
                self.results[brand_tone] = {'overall_score': 0, 'issues': ['Generation failed']}
                return None
                
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            self.results[brand_tone] = {'overall_score': 0, 'issues': [f'Error: {e}']}
            return None
    
    def run_all_tests(self):
        """Test all brand tones comprehensively"""
        print("🚀 COMPREHENSIVE BRAND TONE QUALITY TESTING")
        print("="*70)
        print("Testing all 6 brand tones for 10/10 quality optimization")
        
        for brand_tone in self.brand_tones:
            result = self.test_brand_tone(brand_tone)
            time.sleep(4)  # Delay between tests
            
        # Generate comprehensive report
        self.generate_optimization_report()
    
    def generate_optimization_report(self):
        """Generate detailed optimization report"""
        print(f"\n{'='*70}")
        print("📊 BRAND TONE OPTIMIZATION REPORT")
        print(f"{'='*70}")
        
        if not self.results:
            print("❌ No results to analyze")
            return
        
        # Overall statistics
        scores = []
        perfect_tones = 0
        good_tones = 0
        poor_tones = 0
        
        print(f"\n🎨 INDIVIDUAL BRAND TONE SCORES:")
        print("-" * 70)
        
        for tone, analysis in self.results.items():
            score = analysis.get('overall_score', 0)
            scores.append(score)
            
            if score >= 90:
                grade = "A+"
                status = "✅"
                perfect_tones += 1
            elif score >= 80:
                grade = "A"
                status = "✅" 
                good_tones += 1
            elif score >= 70:
                grade = "B"
                status = "⚠️"
                good_tones += 1
            elif score >= 60:
                grade = "C"
                status = "⚠️"
            else:
                grade = "D"
                status = "❌"
                poor_tones += 1
            
            print(f"{status} {tone.capitalize():12} - {score:5.1f}/100 (Grade: {grade})")
        
        # Summary statistics
        avg_score = sum(scores) / len(scores) if scores else 0
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"  Average Score: {avg_score:.1f}/100")
        print(f"  Perfect (90+): {perfect_tones}")
        print(f"  Good (70-89):  {good_tones}")
        print(f"  Poor (<70):    {poor_tones}")
        
        # Category analysis
        categories = ['title_score', 'bullets_score', 'description_score', 'voice_consistency']
        category_names = ['Title', 'Bullets', 'Description', 'Voice Consistency']
        
        print(f"\n🔍 CATEGORY BREAKDOWN:")
        for i, category in enumerate(categories):
            cat_scores = [result.get(category, 0) for result in self.results.values() if isinstance(result, dict)]
            cat_avg = sum(cat_scores) / len(cat_scores) if cat_scores else 0
            print(f"  {category_names[i]:18}: {cat_avg:5.1f}/100")
        
        # Identify issues
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
        
        # Recommendations
        print(f"\n🎯 OPTIMIZATION RECOMMENDATIONS:")
        if avg_score >= 85:
            print("✅ EXCELLENT: Brand tone system working at professional level")
        elif avg_score >= 75:
            print("⚠️ GOOD: Minor improvements needed for 10/10 quality")
            print("  - Enhance voice consistency across all elements")
            print("  - Strengthen tone-specific vocabulary")
        elif avg_score >= 60:
            print("⚠️ NEEDS IMPROVEMENT: Several areas require attention")
            print("  - Improve brand tone prompt specificity")
            print("  - Add stronger tone validation")
            print("  - Enhance vocabulary differentiation")
        else:
            print("❌ CRITICAL: Major brand tone system overhaul needed")
            print("  - Redesign tone-specific prompts")
            print("  - Add comprehensive tone guidelines")
            print("  - Implement better tone enforcement")
        
        # Save detailed report
        report_file = f"brand_tone_optimization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n💾 Detailed report saved: {report_file}")
        
        return avg_score

if __name__ == "__main__":
    print("Starting Brand Tone Optimization System...")
    optimizer = BrandToneOptimizer()
    
    # Option to test single tone or all
    if len(sys.argv) > 1:
        tone = sys.argv[1].lower()
        if tone in optimizer.brand_tones:
            optimizer.test_brand_tone(tone)
        else:
            print(f"Invalid tone. Choose from: {', '.join(optimizer.brand_tones)}")
    else:
        # Test all brand tones
        final_score = optimizer.run_all_tests()
        if final_score and final_score >= 80:
            print(f"\n🎉 SUCCESS: Brand tone system optimized to {final_score:.1f}/100!")
        else:
            print(f"\n⚠️ Additional optimization needed.")