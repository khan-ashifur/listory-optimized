import os
import sys
import django

# Set up Django environment
sys.path.insert(0, 'backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product, User

print("🏆 KEVIN KING OPTIMIZATION V2 - POST-ENHANCEMENT TESTING")
print("=" * 65)
print("Testing improved system for consistent 85%+ performance")

class QuickKevinEvaluator:
    """Quick evaluation focusing on the key Kevin King criteria"""
    
    def evaluate_quick(self, listing, product):
        score = 0
        feedback = []
        
        # Title Evaluation (25 points)
        title_score = self._evaluate_title_v2(listing.title, product)
        score += title_score
        
        # Bullet Evaluation (35 points) 
        bullet_score = self._evaluate_bullets_v2(listing.bullet_points)
        score += bullet_score
        
        # Description Evaluation (25 points)
        desc_score = self._evaluate_description_v2(listing.long_description)
        score += desc_score
        
        # Keywords (15 points)
        keyword_score = min(15, len((listing.keywords or '').split(',')) if listing.keywords else 0)
        score += keyword_score
        
        percentage = score
        grade = self._get_grade(percentage)
        
        return {
            'score': score,
            'percentage': percentage,
            'grade': grade,
            'title_score': title_score,
            'bullet_score': bullet_score,
            'desc_score': desc_score,
            'keyword_score': keyword_score,
            'feedback': feedback
        }
    
    def _evaluate_title_v2(self, title, product):
        if not title:
            return 0
            
        score = 0
        
        # Brand placement (5 points)
        if product.brand_name.lower() in title.lower():
            score += 5
            
        # Benefit words (5 points)
        benefit_words = ['best', 'professional', 'premium', 'perfect', 'ultimate', 'advanced']
        if any(word in title.lower() for word in benefit_words):
            score += 5
            
        # Length optimization (5 points)
        if 115 <= len(title) <= 150:
            score += 5
        elif 100 <= len(title) <= 170:
            score += 3
            
        # Mobile readability (5 points)
        words = title.split()
        if len(words) <= 12:
            score += 5
            
        # Keyword presence (5 points)
        if product.name.lower() in title.lower():
            score += 5
            
        return min(score, 25)
    
    def _evaluate_bullets_v2(self, bullets):
        if not bullets:
            return 0
            
        bullet_list = [b.strip() for b in bullets.split('\n') if b.strip()]
        score = 0
        
        # Emotional triggers (10 points)
        emotion_phrases = ['tired of', 'worried about', 'finally', 'imagine', 'join', 'eliminate', 'never', 'no more']
        emotion_count = sum(1 for bullet in bullet_list for phrase in emotion_phrases if phrase.lower() in bullet.lower())
        score += min(emotion_count * 2, 10)
        
        # Problem-solution structure (10 points)
        problem_words = ['tired', 'worried', 'frustrated', 'annoyed', 'struggling', 'while other']
        problem_bullets = sum(1 for bullet in bullet_list for word in problem_words if word.lower() in bullet.lower())
        score += min(problem_bullets * 2, 10)
        
        # Customer language (10 points)
        customer_phrases = ['you know', 'picture this', 'imagine', 'finally', 'discover', 'experience']
        customer_count = sum(1 for bullet in bullet_list for phrase in customer_phrases if phrase.lower() in bullet.lower())
        score += min(customer_count * 2, 10)
        
        # Proper length (5 points)
        if all(150 <= len(bullet) <= 300 for bullet in bullet_list):
            score += 5
            
        return min(score, 35)
    
    def _evaluate_description_v2(self, description):
        if not description:
            return 0
            
        score = 0
        
        # Story opening (8 points)
        story_openers = ['picture this', 'imagine', 'it\'s', 'you know that feeling', 'ever notice']
        if any(opener in description.lower() for opener in story_openers):
            score += 8
            
        # Problem agitation (6 points)
        problem_words = ['frustrating', 'annoying', 'tired', 'struggle', 'problem', 'issue']
        problem_count = sum(1 for word in problem_words if word in description.lower())
        score += min(problem_count, 6)
        
        # Solution positioning (6 points)
        solution_phrases = ['that\'s why', 'exactly why', 'solution', 'answer', 'fix', 'solve']
        if any(phrase in description.lower() for phrase in solution_phrases):
            score += 6
            
        # Call to action (5 points)
        cta_words = ['order', 'get', 'choose', 'buy', 'experience', 'discover', 'transform']
        if any(word in description.lower() for word in cta_words):
            score += 5
            
        return min(score, 25)
    
    def _get_grade(self, percentage):
        if percentage >= 90:
            return 'A+'
        elif percentage >= 85:
            return 'A'
        elif percentage >= 80:
            return 'A-'
        elif percentage >= 75:
            return 'B+'
        elif percentage >= 70:
            return 'B'
        else:
            return 'C or below'

def test_enhanced_system():
    evaluator = QuickKevinEvaluator()
    service = ListingGeneratorService()
    
    if not service.client:
        print("❌ OpenAI client not available")
        return
        
    user = User.objects.first()
    if not user:
        print("❌ No user found")
        return
    
    # Enhanced test scenarios
    scenarios = [
        {
            'name': 'Gaming Mechanical Keyboard',
            'description': 'RGB backlit gaming keyboard with tactile switches',
            'brand': 'GamePro',
            'tone': 'bold',
            'category': 'Electronics',
            'features': 'Mechanical switches, RGB backlighting, Programmable keys',
            'price': 129.99,
            'expected_improvement': 'Emotion Score should jump from 0 to 8+'
        },
        {
            'name': 'Yoga Mat Premium',
            'description': 'Non-slip yoga mat with alignment guides',
            'brand': 'ZenFlow',
            'tone': 'casual',
            'category': 'Sports',
            'features': 'Non-slip surface, Alignment guides, 6mm thickness',
            'price': 49.99,
            'expected_improvement': 'Bullets should have problem-solution structure'
        }
    ]
    
    results = []
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*15} ENHANCED TEST {i}: {scenario['name']} {'='*15}")
        print(f"🎯 Expected: {scenario['expected_improvement']}")
        
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
            
            print(f"🤖 Generating with Kevin King V2 optimization...")
            
            # Generate listing
            listing = service.generate_listing(product.id, 'amazon')
            
            # Quick evaluation
            evaluation = evaluator.evaluate_quick(listing, product)
            results.append(evaluation)
            
            print(f"\n🎯 KEVIN KING V2 RESULTS:")
            print(f"Overall Score: {evaluation['score']}/100 ({evaluation['percentage']}%)")
            print(f"Grade: {evaluation['grade']}")
            print(f"   Title: {evaluation['title_score']}/25")
            print(f"   Bullets: {evaluation['bullet_score']}/35")
            print(f"   Description: {evaluation['desc_score']}/25")
            print(f"   Keywords: {evaluation['keyword_score']}/15")
            
            # Show specific improvements
            print(f"\n📊 IMPROVEMENT ANALYSIS:")
            if evaluation['bullet_score'] >= 25:
                print(f"   ✅ BULLETS: Strong emotional triggers detected")
            else:
                print(f"   ❌ BULLETS: Still need more emotion ({evaluation['bullet_score']}/35)")
                
            if evaluation['desc_score'] >= 20:
                print(f"   ✅ DESCRIPTION: Story structure implemented")
            else:
                print(f"   ❌ DESCRIPTION: Missing story elements ({evaluation['desc_score']}/25)")
                
            if evaluation['title_score'] >= 20:
                print(f"   ✅ TITLE: Well optimized")
            else:
                print(f"   ❌ TITLE: Needs improvement ({evaluation['title_score']}/25)")
            
            # Sample content analysis
            if listing.bullet_points:
                first_bullet = listing.bullet_points.split('\n')[0][:100]
                print(f"\n📝 First Bullet Sample: {first_bullet}...")
                
                # Check for Kevin King structure
                if any(phrase in first_bullet.lower() for phrase in ['tired of', 'finally', 'worried about']):
                    print(f"   ✅ Kevin King structure detected!")
                else:
                    print(f"   ❌ Missing Kevin King emotional framework")
            
            product.delete()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            if 'product' in locals():
                product.delete()
    
    # Final analysis
    if results:
        avg_score = sum(r['percentage'] for r in results) / len(results)
        print(f"\n{'='*65}")
        print(f"🏆 KEVIN KING V2 SYSTEM PERFORMANCE:")
        print(f"Average Score: {avg_score:.1f}%")
        
        if avg_score >= 85:
            print(f"✅ SUCCESS: Achieved Kevin King standards (85%+)")
            print(f"🚀 System ready for production use")
        elif avg_score >= 75:
            print(f"🔄 GOOD PROGRESS: Near Kevin King standards")
            print(f"🎯 Need slight fine-tuning for 85%+ consistency")
        else:
            print(f"❌ NEEDS MORE WORK: Below professional standards")
            print(f"🔧 Major prompt improvements still needed")
        
        # Grade distribution
        grades = [r['grade'] for r in results]
        print(f"Grade Distribution: {', '.join(grades)}")
        
        # Specific area analysis
        avg_title = sum(r['title_score'] for r in results) / len(results)
        avg_bullets = sum(r['bullet_score'] for r in results) / len(results)
        avg_desc = sum(r['desc_score'] for r in results) / len(results)
        
        print(f"\n📊 COMPONENT ANALYSIS:")
        print(f"Titles: {avg_title:.1f}/25 ({'✅' if avg_title >= 20 else '❌'})")
        print(f"Bullets: {avg_bullets:.1f}/35 ({'✅' if avg_bullets >= 25 else '❌'})")
        print(f"Descriptions: {avg_desc:.1f}/25 ({'✅' if avg_desc >= 20 else '❌'})")

if __name__ == "__main__":
    test_enhanced_system()