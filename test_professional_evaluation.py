import os
import sys
import django
import json

# Set up Django environment
sys.path.insert(0, 'backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product, User

class KevinKingEvaluator:
    """
    PhD-level e-commerce evaluation framework based on Kevin King's 
    methodologies for Amazon listing optimization
    """
    
    def __init__(self):
        self.evaluation_criteria = {
            "title_optimization": {
                "max_score": 20,
                "factors": {
                    "keyword_placement": 5,  # Primary keywords in first 80 chars
                    "character_efficiency": 3,  # 115-150 char sweet spot
                    "benefit_clarity": 4,  # Clear value prop
                    "brand_positioning": 3,  # Brand placement strategy
                    "mobile_readability": 3,  # Readable on mobile
                    "search_volume_targeting": 2  # High-volume terms included
                }
            },
            "bullet_points": {
                "max_score": 25,
                "factors": {
                    "benefit_focused": 5,  # Benefits not features
                    "emotional_triggers": 5,  # Emotional buying motivations
                    "objection_handling": 4,  # Addresses common concerns
                    "keyword_integration": 4,  # Natural keyword placement
                    "scannability": 3,  # Easy to skim read
                    "differentiation": 4  # Unique value props
                }
            },
            "description_quality": {
                "max_score": 20,
                "factors": {
                    "story_structure": 5,  # Problem-solution narrative
                    "customer_psychology": 5,  # Buyer psychology triggers
                    "keyword_density": 3,  # Optimal keyword usage
                    "call_to_action": 3,  # Clear next steps
                    "trust_building": 4  # Credibility elements
                }
            },
            "keyword_strategy": {
                "max_score": 15,
                "factors": {
                    "primary_focus": 4,  # 3-5 primary keywords
                    "long_tail_coverage": 4,  # Long-tail opportunities
                    "search_intent_match": 4,  # Matches buyer intent
                    "competition_analysis": 3  # Competitive keyword gaps
                }
            },
            "aplus_content": {
                "max_score": 20,
                "factors": {
                    "visual_storytelling": 5,  # Image concepts and flow
                    "conversion_funnel": 5,  # Awareness to purchase journey
                    "unique_selling_prop": 4,  # Clear differentiation
                    "technical_specs": 3,  # Proper spec presentation
                    "social_proof": 3  # Trust and credibility elements
                }
            }
        }
        
    def evaluate_listing(self, listing, product):
        """
        Comprehensive Kevin King-style listing evaluation
        """
        scores = {}
        total_score = 0
        max_total = 100
        
        # 1. TITLE EVALUATION
        title_score = self._evaluate_title(listing.title, product)
        scores['title'] = title_score
        total_score += title_score
        
        # 2. BULLET POINTS EVALUATION  
        bullet_score = self._evaluate_bullets(listing.bullet_points, product)
        scores['bullets'] = bullet_score
        total_score += bullet_score
        
        # 3. DESCRIPTION EVALUATION
        desc_score = self._evaluate_description(listing.long_description, product)
        scores['description'] = desc_score
        total_score += desc_score
        
        # 4. KEYWORD STRATEGY EVALUATION
        keyword_score = self._evaluate_keywords(listing.keywords, listing.amazon_backend_keywords, product)
        scores['keywords'] = keyword_score
        total_score += keyword_score
        
        # 5. A+ CONTENT EVALUATION
        aplus_score = self._evaluate_aplus(listing.amazon_aplus_content, product)
        scores['aplus'] = aplus_score
        total_score += aplus_score
        
        # Calculate final grade
        percentage = (total_score / max_total) * 100
        grade = self._get_grade(percentage)
        
        return {
            'total_score': total_score,
            'max_score': max_total,
            'percentage': percentage,
            'grade': grade,
            'scores': scores,
            'detailed_feedback': self._generate_feedback(scores, product)
        }
    
    def _evaluate_title(self, title, product):
        score = 0
        feedback = []
        
        if not title:
            return 0
            
        # Keyword placement (5 points)
        if len(title) > 0:
            first_80 = title[:80].lower()
            if product.name.lower() in first_80:
                score += 3
            if product.brand_name.lower() in first_80:
                score += 2
        
        # Character efficiency (3 points)
        if 115 <= len(title) <= 150:
            score += 3
        elif 100 <= len(title) <= 170:
            score += 2
        elif len(title) > 0:
            score += 1
            
        # Benefit clarity (4 points)
        benefit_words = ['perfect', 'premium', 'professional', 'ultimate', 'best', 'advanced', 'superior']
        if any(word in title.lower() for word in benefit_words):
            score += 2
        if 'for' in title.lower():  # Use case targeting
            score += 2
            
        # Brand positioning (3 points)
        if product.brand_name in title:
            brand_pos = title.find(product.brand_name)
            if brand_pos < len(title) * 0.3:  # Brand in first 30%
                score += 3
            elif brand_pos < len(title) * 0.6:  # Brand in first 60%
                score += 2
            else:
                score += 1
                
        # Mobile readability (3 points)
        words = title.split()
        if len(words) <= 12:  # Mobile-friendly word count
            score += 2
        if not any(len(word) > 15 for word in words):  # No super long words
            score += 1
            
        return min(score, 20)  # Cap at max score
    
    def _evaluate_bullets(self, bullets, product):
        score = 0
        
        if not bullets:
            return 0
            
        bullet_list = bullets.split('\n') if bullets else []
        bullet_list = [b.strip() for b in bullet_list if b.strip()]
        
        # Benefit focused (5 points)
        benefit_count = 0
        for bullet in bullet_list:
            if any(word in bullet.lower() for word in ['you', 'your', 'experience', 'enjoy', 'feel', 'get']):
                benefit_count += 1
        score += min(benefit_count, 5)
        
        # Emotional triggers (5 points)
        emotion_words = ['love', 'amazing', 'perfect', 'incredible', 'outstanding', 'exceptional', 'worry-free', 'confidence', 'peace of mind']
        emotion_count = sum(1 for bullet in bullet_list for word in emotion_words if word in bullet.lower())
        score += min(emotion_count, 5)
        
        # Objection handling (4 points)
        objection_phrases = ['no', 'never', 'without', 'eliminate', 'solve', 'prevent', 'avoid', 'ensure']
        objection_count = sum(1 for bullet in bullet_list for phrase in objection_phrases if phrase in bullet.lower())
        score += min(objection_count, 4)
        
        # Keyword integration (4 points)
        if product.categories:
            categories = [cat.strip().lower() for cat in product.categories.split(',')]
            keyword_integration = sum(1 for bullet in bullet_list for cat in categories if cat in bullet.lower())
            score += min(keyword_integration, 4)
        
        # Scannability (3 points)
        if len(bullet_list) == 5:  # Optimal bullet count
            score += 2
        if all(100 <= len(bullet) <= 250 for bullet in bullet_list):  # Good length
            score += 1
            
        # Differentiation (4 points)
        unique_words = ['only', 'exclusive', 'unique', 'unlike', 'first', 'patented', 'proprietary']
        diff_count = sum(1 for bullet in bullet_list for word in unique_words if word in bullet.lower())
        score += min(diff_count, 4)
        
        return min(score, 25)
    
    def _evaluate_description(self, description, product):
        score = 0
        
        if not description:
            return 0
            
        # Story structure (5 points)
        if 'experience' in description.lower() or 'imagine' in description.lower():
            score += 2
        if len(description) >= 1000:  # Comprehensive description
            score += 3
            
        # Customer psychology (5 points)
        psych_words = ['you', 'your', 'feel', 'enjoy', 'discover', 'transform', 'achieve']
        psych_count = sum(1 for word in psych_words if word in description.lower())
        score += min(psych_count, 5)
        
        # Keyword density (3 points)
        if product.name.lower() in description.lower():
            score += 2
        if product.brand_name.lower() in description.lower():
            score += 1
            
        # Call to action (3 points)
        cta_phrases = ['order', 'buy', 'get', 'choose', 'select', 'add to cart']
        if any(phrase in description.lower() for phrase in cta_phrases):
            score += 3
            
        # Trust building (4 points)
        trust_words = ['guarantee', 'warranty', 'quality', 'certified', 'tested', 'proven']
        trust_count = sum(1 for word in trust_words if word in description.lower())
        score += min(trust_count, 4)
        
        return min(score, 20)
    
    def _evaluate_keywords(self, keywords, backend_keywords, product):
        score = 0
        
        # Primary focus (4 points)
        if keywords:
            keyword_list = [k.strip() for k in keywords.split(',')]
            if len(keyword_list) >= 5:
                score += 4
            elif len(keyword_list) >= 3:
                score += 2
                
        # Backend keyword optimization (4 points)
        if backend_keywords:
            if len(backend_keywords) >= 200:  # Good utilization
                score += 4
            elif len(backend_keywords) >= 150:
                score += 2
                
        # Search intent match (4 points)
        intent_words = ['best', 'top', 'review', 'buy', 'cheap', 'quality']
        if keywords:
            intent_matches = sum(1 for word in intent_words if word in keywords.lower())
            score += min(intent_matches, 4)
            
        # Competition analysis (3 points)
        if product.brand_name.lower() in (keywords or '').lower():
            score += 2
        if len((keywords or '').split(',')) > 10:  # Comprehensive coverage
            score += 1
            
        return min(score, 15)
    
    def _evaluate_aplus(self, aplus_content, product):
        score = 0
        
        if not aplus_content:
            return 0
            
        # Visual storytelling (5 points)
        if 'image' in aplus_content.lower() or 'visual' in aplus_content.lower():
            score += 3
        if len(aplus_content) >= 2000:  # Comprehensive A+ content
            score += 2
            
        # Conversion funnel (5 points)
        if 'section' in aplus_content.lower():
            section_count = aplus_content.lower().count('section')
            score += min(section_count, 5)
            
        # Unique selling proposition (4 points)
        usp_words = ['unique', 'only', 'exclusive', 'different', 'unlike', 'special']
        usp_count = sum(1 for word in usp_words if word in aplus_content.lower())
        score += min(usp_count, 4)
        
        # Technical specs (3 points)
        if 'specifications' in aplus_content.lower() or 'features' in aplus_content.lower():
            score += 3
            
        # Social proof (3 points)
        proof_words = ['customers', 'reviews', 'satisfaction', 'testimonial', 'rated']
        proof_count = sum(1 for word in proof_words if word in aplus_content.lower())
        score += min(proof_count, 3)
        
        return min(score, 20)
    
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
        elif percentage >= 65:
            return 'B-'
        elif percentage >= 60:
            return 'C+'
        elif percentage >= 55:
            return 'C'
        else:
            return 'F'
    
    def _generate_feedback(self, scores, product):
        feedback = []
        
        if scores.get('title', 0) < 15:
            feedback.append("❌ TITLE: Needs stronger keyword placement and benefit clarity")
        if scores.get('bullets', 0) < 20:
            feedback.append("❌ BULLETS: Need more emotional triggers and objection handling")
        if scores.get('description', 0) < 15:
            feedback.append("❌ DESCRIPTION: Missing story structure and customer psychology")
        if scores.get('keywords', 0) < 12:
            feedback.append("❌ KEYWORDS: Insufficient coverage and search intent matching")
        if scores.get('aplus', 0) < 15:
            feedback.append("❌ A+ CONTENT: Needs better visual storytelling and USP clarity")
            
        return feedback

def run_kevin_king_evaluation():
    """
    Run comprehensive Kevin King-style evaluation on regular listings
    """
    print("🎯 KEVIN KING E-COMMERCE EVALUATION FRAMEWORK")
    print("=" * 60)
    print("Testing regular listings (no occasion) for consistent 10/10 performance")
    
    evaluator = KevinKingEvaluator()
    service = ListingGeneratorService()
    
    # Test categories for comprehensive evaluation
    test_scenarios = [
        {
            'category': 'Electronics',
            'name': 'Wireless Bluetooth Headphones',
            'description': 'Premium noise-cancelling headphones with 30-hour battery',
            'brand': 'AudioMax',
            'tone': 'professional',
            'features': 'Noise cancelling, 30-hour battery, Bluetooth 5.3',
            'price': 149.99
        },
        {
            'category': 'Home & Kitchen', 
            'name': 'Stainless Steel Coffee Mug',
            'description': 'Insulated travel mug that keeps drinks hot for 8 hours',
            'brand': 'ThermoGrip',
            'tone': 'casual',
            'features': '16oz capacity, Double-wall insulation, Leak-proof lid',
            'price': 24.99
        },
        {
            'category': 'Health & Personal Care',
            'name': 'Ergonomic Lumbar Support Pillow',
            'description': 'Memory foam pillow designed to relieve back pain',
            'brand': 'ComfortCore',
            'tone': 'professional',
            'features': 'Memory foam, Ergonomic design, Washable cover',
            'price': 39.99
        }
    ]
    
    results = []
    
    if not service.client:
        print("❌ OpenAI client not available - check API key")
        return
    
    user = User.objects.first()
    if not user:
        print("❌ No user found")
        return
        
    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n{'='*20} TEST {i}: {scenario['category']} {'='*20}")
        print(f"📦 Product: {scenario['name']}")
        print(f"🎨 Tone: {scenario['tone']}")
        print(f"💰 Price: ${scenario['price']}")
        
        try:
            # Create test product
            product = Product.objects.create(
                name=scenario['name'],
                description=scenario['description'],
                brand_name=scenario['brand'],
                brand_tone=scenario['tone'],
                occasion='',  # NO OCCASION - Regular listing
                categories=scenario['category'],
                features=scenario['features'],
                price=scenario['price'],
                user=user
            )
            
            print(f"🤖 Generating listing with GPT-5...")
            
            # Generate listing
            listing = service.generate_listing(product.id, 'amazon')
            
            # Evaluate with Kevin King framework
            evaluation = evaluator.evaluate_listing(listing, product)
            results.append({
                'scenario': scenario,
                'evaluation': evaluation,
                'product_id': product.id
            })
            
            # Display results
            print(f"\n📊 KEVIN KING EVALUATION RESULTS:")
            print(f"🎯 OVERALL SCORE: {evaluation['total_score']}/{evaluation['max_score']} ({evaluation['percentage']:.1f}%)")
            print(f"📈 GRADE: {evaluation['grade']}")
            
            print(f"\n📋 DETAILED SCORES:")
            print(f"   Title: {evaluation['scores']['title']}/20")
            print(f"   Bullets: {evaluation['scores']['bullets']}/25") 
            print(f"   Description: {evaluation['scores']['description']}/20")
            print(f"   Keywords: {evaluation['scores']['keywords']}/15")
            print(f"   A+ Content: {evaluation['scores']['aplus']}/20")
            
            if evaluation['detailed_feedback']:
                print(f"\n🔧 IMPROVEMENT AREAS:")
                for feedback in evaluation['detailed_feedback']:
                    print(f"   {feedback}")
            else:
                print(f"\n✅ EXCELLENT: No major weaknesses detected!")
                
            # Clean up
            product.delete()
            
        except Exception as e:
            print(f"❌ Error: {e}")
            if 'product' in locals():
                product.delete()
    
    # Summary analysis
    print(f"\n" + "="*60)
    print(f"📈 OVERALL PERFORMANCE ANALYSIS")
    
    if results:
        avg_score = sum(r['evaluation']['percentage'] for r in results) / len(results)
        grades = [r['evaluation']['grade'] for r in results]
        
        print(f"🎯 Average Score: {avg_score:.1f}%")
        print(f"📊 Grade Distribution: {', '.join(grades)}")
        
        # Identify patterns
        weak_areas = {}
        for result in results:
            scores = result['evaluation']['scores']
            for area, score in scores.items():
                max_scores = {'title': 20, 'bullets': 25, 'description': 20, 'keywords': 15, 'aplus': 20}
                percentage = (score / max_scores[area]) * 100
                if percentage < 75:  # Below B grade
                    weak_areas[area] = weak_areas.get(area, 0) + 1
        
        if weak_areas:
            print(f"\n⚠️ CONSISTENT WEAKNESS PATTERNS:")
            for area, count in weak_areas.items():
                print(f"   {area.upper()}: {count}/{len(results)} tests below 75%")
        else:
            print(f"\n✅ CONSISTENT HIGH PERFORMANCE ACROSS ALL AREAS!")
            
        # Determine if fine-tuning needed
        if avg_score < 85:
            print(f"\n🔧 FINE-TUNING REQUIRED: Average below A- grade")
            print(f"🎯 TARGET: Achieve consistent 85%+ performance")
        else:
            print(f"\n🏆 SYSTEM PERFORMING AT KEVIN KING STANDARDS!")

if __name__ == "__main__":
    run_kevin_king_evaluation()