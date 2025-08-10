import os
import sys
import django

# Set up Django environment
sys.path.insert(0, 'backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product, User

print("🚀 E-COMMERCE PROFESSIONAL EVALUATION - TARGET: 85%+ CONSISTENCY")
print("=" * 60)

class FinalEcommerceEvaluator:
    """Final evaluation with strict e-commerce professional standards"""
    
    def evaluate_final(self, listing, product):
        score = 0
        breakdown = {}
        
        # TITLE (30 points) - Stricter evaluation
        title_score = self._evaluate_title_strict(listing.title, product)
        breakdown['title'] = f"{title_score}/30"
        score += title_score
        
        # BULLETS (40 points) - Most important for conversion
        bullet_score = self._evaluate_bullets_strict(listing.bullet_points)
        breakdown['bullets'] = f"{bullet_score}/40"
        score += bullet_score
        
        # DESCRIPTION (20 points) - Story and psychology
        desc_score = self._evaluate_description_strict(listing.long_description)
        breakdown['description'] = f"{desc_score}/20"
        score += desc_score
        
        # OVERALL CONVERSION PSYCHOLOGY (10 points)
        psychology_score = self._evaluate_psychology(listing)
        breakdown['psychology'] = f"{psychology_score}/10"
        score += psychology_score
        
        percentage = score
        grade = self._get_grade(percentage)
        
        return {
            'score': score,
            'percentage': percentage,
            'grade': grade,
            'breakdown': breakdown,
            'professional_ready': percentage >= 85
        }
    
    def _evaluate_title_strict(self, title, product):
        if not title:
            return 0
            
        score = 0
        
        # Mandatory format compliance (15 points)
        has_brand = product.brand_name.lower() in title.lower()
        has_benefit = any(word in title.lower() for word in ['professional', 'premium', 'best', 'ultimate', 'perfect'])
        has_use_case = 'for' in title.lower() or 'perfect' in title.lower()
        
        if has_brand and has_benefit and has_use_case:
            score += 15
        elif has_brand and has_benefit:
            score += 10
        elif has_brand:
            score += 5
            
        # Length optimization (8 points)
        if 115 <= len(title) <= 145:
            score += 8
        elif 100 <= len(title) <= 160:
            score += 5
            
        # Mobile-first (7 points) 
        first_80 = title[:80]
        if product.brand_name in first_80 and any(word in first_80.lower() for word in ['professional', 'premium', 'best']):
            score += 7
        elif product.brand_name in first_80:
            score += 4
            
        return min(score, 30)
    
    def _evaluate_bullets_strict(self, bullets):
        if not bullets:
            return 0
            
        bullet_list = [b.strip() for b in bullets.split('\n') if b.strip()]
        score = 0
        
        # Kevin King structure compliance (20 points)
        structure_phrases = ['tired of', 'worried about', 'while other', 'imagine', 'join']
        structure_bullets = sum(1 for bullet in bullet_list for phrase in structure_phrases if phrase.lower() in bullet.lower())
        score += min(structure_bullets * 4, 20)
        
        # Emotional triggers (10 points) 
        emotion_words = ['finally', 'eliminate', 'never', 'stop', 'discover', 'experience', 'feel']
        emotion_count = sum(1 for bullet in bullet_list for word in emotion_words if word.lower() in bullet.lower())
        score += min(emotion_count * 2, 10)
        
        # Problem-solution pairs (10 points)
        problem_solutions = 0
        for bullet in bullet_list:
            if ('tired of' in bullet.lower() or 'worried about' in bullet.lower()) and ('finally' in bullet.lower() or 'eliminate' in bullet.lower()):
                problem_solutions += 1
        score += min(problem_solutions * 2, 10)
        
        return min(score, 40)
    
    def _evaluate_description_strict(self, description):
        if not description:
            return 0
            
        score = 0
        
        # High-impact opening (8 points)
        strong_openers = ['you know that sinking feeling', 'it\'s 2 am', 'picture this', 'every day thousands', 'you know that feeling']
        has_strong_opener = any(opener in description.lower() for opener in strong_openers)
        if has_strong_opener:
            score += 8
        elif any(opener in description.lower() for opener in ['you know', 'picture', 'imagine']):
            score += 5
            
        # Problem agitation (6 points)
        agitation_words = ['frustration', 'struggle', 'builds', 'annoying', 'sinking feeling', 'tired']
        agitation_count = sum(1 for word in agitation_words if word in description.lower())
        score += min(agitation_count, 6)
        
        # Solution positioning (6 points)
        solution_phrases = ['that\'s exactly why', 'engineered this', 'created this', 'designed to']
        if any(phrase in description.lower() for phrase in solution_phrases):
            score += 6
            
        return min(score, 20)
    
    def _evaluate_psychology(self, listing):
        score = 0
        
        # Overall emotional flow (5 points)
        total_text = f"{listing.title} {listing.bullet_points} {listing.long_description}".lower()
        
        # Pain points addressed
        if any(word in total_text for word in ['tired', 'frustrated', 'struggle', 'problem']):
            score += 2
            
        # Relief provided  
        if any(word in total_text for word in ['finally', 'eliminate', 'solve', 'discover']):
            score += 2
            
        # Future state painting
        if any(word in total_text for word in ['imagine', 'experience', 'transform', 'enjoy']):
            score += 1
            
        # Customer language (5 points)
        customer_phrases = ['you know', 'picture this', 'thousands of people', 'join', 'discover']
        customer_usage = sum(1 for phrase in customer_phrases if phrase in total_text)
        score += min(customer_usage, 5)
        
        return score
    
    def _get_grade(self, percentage):
        if percentage >= 95:
            return 'A+ (E-commerce Mastery)'
        elif percentage >= 90:
            return 'A (E-commerce Professional)'
        elif percentage >= 85:
            return 'A- (Professional Standard)'
        elif percentage >= 80:
            return 'B+ (Close to Professional)'
        elif percentage >= 75:
            return 'B (Good but needs work)'
        else:
            return 'C or below (Major improvements needed)'

def run_final_test():
    evaluator = FinalEcommerceEvaluator()
    service = ListingGeneratorService()
    
    if not service.client:
        print("❌ OpenAI client not available")
        return
        
    user = User.objects.first()
    if not user:
        print("❌ No user found")
        return
    
    # Final test scenarios - diverse categories
    final_scenarios = [
        {
            'name': 'Wireless Phone Charger',
            'description': 'Fast wireless charging pad with LED indicator',
            'brand': 'ChargeFast',
            'tone': 'professional',
            'category': 'Electronics',
            'features': 'Fast charging, LED indicator, Universal compatibility',
            'price': 29.99
        },
        {
            'name': 'Memory Foam Pillow',
            'description': 'Ergonomic memory foam pillow for neck support',
            'brand': 'DreamComfort',
            'tone': 'casual',
            'category': 'Home & Garden',
            'features': 'Memory foam, Ergonomic design, Hypoallergenic',
            'price': 59.99
        },
        {
            'name': 'Protein Powder Chocolate',
            'description': 'Whey protein powder with natural chocolate flavor',
            'brand': 'FitNutrition',
            'tone': 'bold',
            'category': 'Health & Personal Care',
            'features': '25g protein, Natural flavor, Easy mixing',
            'price': 39.99
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(final_scenarios, 1):
        print(f"\n{'='*10} FINAL TEST {i}: {scenario['name']} {'='*10}")
        
        try:
            # Create product
            product = Product.objects.create(
                name=scenario['name'],
                description=scenario['description'],
                brand_name=scenario['brand'],
                brand_tone=scenario['tone'],
                occasion='',  # Regular listing
                categories=scenario['category'],
                features=scenario['features'],
                price=scenario['price'],
                user=user
            )
            
            print(f"🎯 Generating with final professional optimization...")
            
            # Generate listing
            listing = service.generate_listing(product.id, 'amazon')
            
            # Final evaluation
            evaluation = evaluator.evaluate_final(listing, product)
            results.append(evaluation)
            
            print(f"\n🏆 FINAL PROFESSIONAL EVALUATION:")
            print(f"Score: {evaluation['score']}/100 ({evaluation['percentage']}%)")
            print(f"Grade: {evaluation['grade']}")
            print(f"Professional Ready: {'✅ YES' if evaluation['professional_ready'] else '❌ NO'}")
            
            print(f"\n📊 BREAKDOWN:")
            for component, score in evaluation['breakdown'].items():
                print(f"   {component.title()}: {score}")
            
            # Show sample content
            if evaluation['percentage'] >= 85:
                print(f"\n🎉 ACHIEVED PROFESSIONAL STANDARD!")
                if listing.bullet_points:
                    first_bullet = listing.bullet_points.split('\n')[0]
                    print(f"📝 Perfect Bullet Example: {first_bullet}")
            else:
                print(f"\n🔧 NEEDS IMPROVEMENT:")
                print(f"   Target: 85%+ | Current: {evaluation['percentage']}%")
            
            product.delete()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            if 'product' in locals():
                product.delete()
    
    # FINAL ANALYSIS
    if results:
        avg_score = sum(r['percentage'] for r in results) / len(results)
        professional_ready_count = sum(1 for r in results if r['professional_ready'])
        
        print(f"\n{'='*60}")
        print(f"🎯 FINAL E-COMMERCE SYSTEM EVALUATION")
        print(f"Average Score: {avg_score:.1f}%")
        print(f"Professional Ready: {professional_ready_count}/{len(results)} tests")
        
        if avg_score >= 85 and professional_ready_count >= len(results) * 0.8:
            print(f"\n🏆 SUCCESS: PROFESSIONAL STANDARD ACHIEVED!")
            print(f"✅ System consistently performs at 85%+ professional level")
            print(f"🚀 Ready for production deployment")
            print(f"📈 Conversion optimization: PhD e-commerce level")
        elif avg_score >= 80:
            print(f"\n🔄 CLOSE: Almost at professional standard")
            print(f"🎯 Need minor fine-tuning for full consistency")
            print(f"💪 Strong foundation established")
        else:
            print(f"\n❌ MORE WORK NEEDED")
            print(f"🔧 Significant improvements still required")
            
        # Final recommendations
        print(f"\n📋 FINAL RECOMMENDATIONS:")
        if avg_score >= 85:
            print(f"   • System ready for high-conversion listings")
            print(f"   • Can compete with top Amazon agencies") 
            print(f"   • Implement for all client listings")
        else:
            print(f"   • Continue prompt refinement")
            print(f"   • Focus on weakest components")
            print(f"   • Test additional scenarios")

if __name__ == "__main__":
    run_final_test()