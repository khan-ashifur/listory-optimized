#!/usr/bin/env python3
"""
ETSY LISTING QUALITY EVALUATION SYSTEM
Comprehensive testing and optimization for 10/10 Etsy listing quality
Designed to beat Helium 10, Jasper AI, and CopyMonkey
"""

import os
import sys
import django
import json
import re
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from django.contrib.auth.models import User
from apps.core.models import Product
from apps.listings.models import GeneratedListing
from apps.listings.services import ListingGeneratorService

class EtsyQualityEvaluator:
    def __init__(self):
        self.service = ListingGeneratorService()
        self.test_products = []
        self.results = []
        
    def create_test_products(self):
        """Create diverse test products for comprehensive evaluation"""
        # Get or create test user
        test_user, created = User.objects.get_or_create(
            username='etsy_test_user',
            defaults={'email': 'test@example.com', 'first_name': 'Test', 'last_name': 'User'}
        )
        test_products_data = [
            {
                'name': 'Custom Wedding Ring Holder',
                'brand_name': 'ArtisanCraft Studio',
                'description': 'Beautiful handcrafted wooden ring holder with personalized engraving',
                'brand_tone': 'handmade',
                'features': 'Personalized engraving, natural wood finish, velvet lining',
                'price': 45.00,
                'categories': 'Home & Living, Wedding, Jewelry Storage',
                'target_keywords': 'wedding ring holder, personalized gift, wooden jewelry box',
                'marketplace': 'etsy_us',
                'occasion': 'wedding',
                'brand_persona': 'Skilled artisan who creates heirloom-quality pieces',
                'target_audience': 'Engaged couples and wedding planners seeking unique keepsakes'
            },
            {
                'name': 'Bohemian Macrame Wall Hanging',
                'brand_name': 'Luna Fiber Arts',
                'description': 'Intricate macrame wall art piece made with natural cotton cord',
                'brand_tone': 'bohemian',
                'features': 'Natural cotton cord, driftwood accent, ready to hang',
                'price': 78.00,
                'categories': 'Home & Living, Wall Decor, Macrame',
                'target_keywords': 'macrame wall hanging, boho decor, fiber art',
                'marketplace': 'etsy_us',
                'occasion': 'housewarming',
                'brand_persona': 'Free-spirited artist inspired by nature and ancient crafts',
                'target_audience': 'Bohemian lifestyle enthusiasts and modern hippies'
            },
            {
                'name': 'Vintage Art Deco Brooch',
                'brand_name': 'Timeless Treasures Co',
                'description': 'Authentic 1920s art deco brooch with rhinestone accents',
                'brand_tone': 'vintage',
                'features': 'Authentic 1920s piece, rhinestone details, original clasp',
                'price': 125.00,
                'categories': 'Jewelry, Vintage, Brooches & Pins',
                'target_keywords': 'art deco brooch, vintage jewelry, 1920s fashion',
                'marketplace': 'etsy_us',
                'occasion': 'christmas',
                'brand_persona': 'Vintage collector with expertise in historical fashion',
                'target_audience': 'Vintage fashion collectors and history enthusiasts'
            },
            {
                'name': 'Minimalist Ceramic Vase Set',
                'brand_name': 'Modern Clay Studio',
                'description': 'Set of three geometric ceramic vases in neutral tones',
                'brand_tone': 'minimalist',
                'features': 'Food-safe glaze, modern geometric design, set of three',
                'price': 89.00,
                'categories': 'Home & Living, Vases, Ceramics & Pottery',
                'target_keywords': 'ceramic vase set, minimalist home decor, modern pottery',
                'marketplace': 'etsy_us',
                'occasion': 'housewarming',
                'brand_persona': 'Contemporary ceramic artist focused on clean lines',
                'target_audience': 'Design-conscious homeowners and minimalist enthusiasts'
            },
            {
                'name': 'Whimsical Fairy Garden Kit',
                'brand_name': 'Enchanted Miniatures',
                'description': 'Complete fairy garden starter kit with hand-painted accessories',
                'brand_tone': 'whimsical',
                'features': 'Hand-painted miniatures, planting guide, weatherproof materials',
                'price': 52.00,
                'categories': 'Craft Supplies & Tools, Miniatures, Garden Decor',
                'target_keywords': 'fairy garden kit, miniature garden, kids craft project',
                'marketplace': 'etsy_us',
                'occasion': 'birthday',
                'brand_persona': 'Imaginative crafter who believes in magic and wonder',
                'target_audience': 'Parents, grandparents, and fairy tale enthusiasts'
            }
        ]
        
        for product_data in test_products_data:
            # Add user to product data
            product_data['user'] = test_user
            
            # Create or get product
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                user=test_user,
                defaults=product_data
            )
            if not created:
                # Update existing product with new data
                for field, value in product_data.items():
                    setattr(product, field, value)
                product.save()
            
            self.test_products.append(product)
            print(f"Created/Updated product: {product.name} (ID: {product.id})")
        
        return self.test_products

    def generate_listings(self):
        """Generate Etsy listings for all test products"""
        print("\n" + "="*50)
        print("GENERATING ETSY LISTINGS")
        print("="*50)
        
        for product in self.test_products:
            try:
                print(f"\nGenerating listing for: {product.name}")
                listing = self.service.generate_listing(product.id, 'etsy')
                if listing:
                    print(f"✅ Successfully generated listing ID: {listing.id}")
                    self.results.append({
                        'product': product,
                        'listing': listing,
                        'status': 'success'
                    })
                else:
                    print(f"❌ Failed to generate listing for {product.name}")
                    self.results.append({
                        'product': product,
                        'listing': None,
                        'status': 'failed'
                    })
            except Exception as e:
                print(f"❌ Error generating listing for {product.name}: {str(e)}")
                self.results.append({
                    'product': product,
                    'listing': None,
                    'status': 'error',
                    'error': str(e)
                })

    def evaluate_listing_quality(self, listing):
        """Comprehensive quality evaluation with 10 criteria (10 points each)"""
        scores = {}
        
        # 1. Title SEO (keyword placement, character usage, readability)
        title_score = 0
        if listing.etsy_title:
            title_length = len(listing.etsy_title)
            if 40 <= title_length <= 140:
                title_score += 3
            if any(keyword in listing.etsy_title.lower() for keyword in ['handmade', 'custom', 'personalized', 'vintage', 'unique']):
                title_score += 2
            if listing.etsy_title.count('|') <= 2:  # Good structure
                title_score += 2
            if not re.search(r'[!@#$%^&*()_+=\[\]{}";\'\\:<>?,.\/]', listing.etsy_title):
                title_score += 1
            if listing.product.brand_tone in listing.etsy_title.lower():
                title_score += 2
        scores['title_seo'] = min(10, title_score)
        
        # 2. Tags Strategy (13 tags usage, multi-word phrases, relevance)
        tags_score = 0
        try:
            tags = json.loads(listing.etsy_tags) if listing.etsy_tags else []
            if len(tags) == 13:
                tags_score += 3
            if len(tags) >= 10:
                tags_score += 2
            
            # Check for multi-word phrases
            multi_word_count = sum(1 for tag in tags if len(tag.split()) > 1)
            if multi_word_count >= 5:
                tags_score += 2
            
            # Check for gift-giving tags
            gift_tags = ['gift for', 'wedding gift', 'birthday gift', 'mothers day', 'christmas']
            if any(gift_tag in ' '.join(tags).lower() for gift_tag in gift_tags):
                tags_score += 2
            
            # Check for brand tone relevance
            if any(listing.product.brand_tone in tag.lower() for tag in tags):
                tags_score += 1
                
        except (json.JSONDecodeError, AttributeError):
            pass
        scores['tags_strategy'] = min(10, tags_score)
        
        # 3. Description Storytelling (emotional connection, materials, process)
        description_score = 0
        if listing.etsy_description:
            desc_lower = listing.etsy_description.lower()
            
            # Emotional indicators
            emotional_words = ['love', 'passion', 'inspiration', 'joy', 'beautiful', 'special', 'unique', 'heart']
            emotion_count = sum(1 for word in emotional_words if word in desc_lower)
            description_score += min(3, emotion_count)
            
            # Process/crafting mentions
            craft_words = ['handmade', 'crafted', 'created', 'designed', 'made with', 'carefully']
            craft_count = sum(1 for word in craft_words if word in desc_lower)
            description_score += min(2, craft_count)
            
            # Materials mentioned
            if listing.etsy_materials or any(material in desc_lower for material in ['wood', 'metal', 'fabric', 'cotton', 'silk', 'leather']):
                description_score += 2
            
            # Length check (should be substantial)
            if len(listing.etsy_description) > 200:
                description_score += 2
            
            # Story/personal touch
            story_words = ['story', 'inspiration', 'journey', 'experience', 'personal']
            if any(word in desc_lower for word in story_words):
                description_score += 1
                
        scores['description_storytelling'] = min(10, description_score)
        
        # 4. Search Visibility (Etsy algorithm optimization)
        visibility_score = 0
        if listing.etsy_title and listing.etsy_tags:
            # Title-tag keyword alignment
            title_words = set(listing.etsy_title.lower().split())
            try:
                tags = json.loads(listing.etsy_tags)
                tag_words = set(' '.join(tags).lower().split())
                overlap = len(title_words.intersection(tag_words))
                visibility_score += min(3, overlap // 2)
            except:
                pass
            
            # Long-tail keyword usage
            if any(len(word) > 8 for word in title_words):
                visibility_score += 2
            
            # Category-relevant keywords
            if listing.product.categories:
                cat_words = set(listing.product.categories.lower().split())
                if title_words.intersection(cat_words):
                    visibility_score += 2
            
            # Seasonal/occasion optimization
            if listing.product.occasion:
                if listing.product.occasion.lower() in listing.etsy_title.lower():
                    visibility_score += 2
            
            # Brand tone integration
            if listing.product.brand_tone in listing.etsy_title.lower():
                visibility_score += 1
                
        scores['search_visibility'] = min(10, visibility_score)
        
        # 5. Conversion Elements (trust signals, social proof, urgency)
        conversion_score = 0
        full_text = f"{listing.etsy_title} {listing.etsy_description}".lower()
        
        # Trust signals
        trust_signals = ['handmade', 'quality', 'satisfaction', 'guarantee', 'carefully', 'professional']
        trust_count = sum(1 for signal in trust_signals if signal in full_text)
        conversion_score += min(3, trust_count)
        
        # Processing time clarity
        if listing.etsy_processing_time:
            conversion_score += 2
        
        # Care instructions (builds trust)
        if listing.etsy_care_instructions:
            conversion_score += 2
        
        # Materials transparency
        if listing.etsy_materials:
            conversion_score += 2
        
        # Gift positioning
        gift_words = ['gift', 'perfect for', 'ideal for', 'special occasion']
        if any(word in full_text for word in gift_words):
            conversion_score += 1
            
        scores['conversion_elements'] = min(10, conversion_score)
        
        # 6. Brand Voice (authenticity, artisan story, uniqueness)
        brand_voice_score = 0
        
        # Brand tone consistency
        if listing.product.brand_tone:
            tone_indicators = {
                'handmade': ['handmade', 'crafted', 'artisan', 'handcrafted'],
                'artistic': ['artistic', 'creative', 'design', 'inspired'],
                'vintage': ['vintage', 'classic', 'timeless', 'retro'],
                'bohemian': ['bohemian', 'boho', 'free-spirited', 'natural'],
                'minimalist': ['minimalist', 'clean', 'simple', 'modern'],
                'whimsical': ['whimsical', 'magical', 'enchanting', 'playful'],
                'luxury_craft': ['luxury', 'premium', 'elegant', 'sophisticated'],
                'eco_friendly': ['eco', 'sustainable', 'natural', 'organic'],
                'rustic': ['rustic', 'farmhouse', 'country', 'cozy'],
                'modern_craft': ['modern', 'contemporary', 'sleek', 'innovative']
            }
            
            relevant_words = tone_indicators.get(listing.product.brand_tone, [])
            if any(word in full_text for word in relevant_words):
                brand_voice_score += 3
        
        # Artisan story
        if listing.etsy_story_behind:
            brand_voice_score += 3
        
        # Personal touch in description
        personal_words = ['i', 'my', 'our', 'we', 'personally', 'passion']
        personal_count = sum(1 for word in personal_words if word in full_text)
        brand_voice_score += min(2, personal_count)
        
        # Uniqueness claims
        unique_words = ['unique', 'one-of-a-kind', 'exclusive', 'special', 'original']
        if any(word in full_text for word in unique_words):
            brand_voice_score += 2
            
        scores['brand_voice'] = min(10, brand_voice_score)
        
        # 7. Visual Recommendations (photo suggestions, styling tips)
        visual_score = 2  # Lower base score
        
        # Check for dedicated visual suggestions field
        if hasattr(listing, 'etsy_visual_suggestions') and listing.etsy_visual_suggestions:
            visual_score += 5  # Major boost for dedicated field
        
        # Check if description mentions visual elements
        visual_words = ['photo', 'image', 'color', 'lighting', 'angle', 'styling', 'display', 'texture', 'finish']
        visual_mentions = sum(1 for word in visual_words if word in full_text)
        visual_score += min(3, visual_mentions)
        
        # Size information (helps visualization)
        if listing.etsy_size_guide or any(size_word in full_text for size_word in ['size', 'dimensions', 'inches', 'cm']):
            visual_score += 2
            
        scores['visual_recommendations'] = min(10, visual_score)
        
        # 8. Personalization Options (customization offerings)
        personalization_score = 0
        
        if listing.etsy_personalization:
            personalization_score += 5
        
        # Check for customization mentions
        custom_words = ['custom', 'personalized', 'engraved', 'monogram', 'bespoke', 'made to order']
        custom_count = sum(1 for word in custom_words if word in full_text)
        personalization_score += min(3, custom_count)
        
        # Options variety
        if 'options' in full_text or 'choose' in full_text:
            personalization_score += 2
            
        scores['personalization_options'] = min(10, personalization_score)
        
        # 9. Pricing Psychology (perceived value, gift-ability)
        pricing_score = 0
        
        # Check for dedicated value proposition field
        if hasattr(listing, 'etsy_value_proposition') and listing.etsy_value_proposition:
            pricing_score += 4  # Major boost for dedicated field
        
        # Price positioning language
        value_words = ['value', 'quality', 'investment', 'worth', 'affordable', 'reasonable', 'heirloom']
        value_mentions = sum(1 for word in value_words if word in full_text)
        pricing_score += min(2, value_mentions)
        
        # Gift positioning
        if listing.etsy_gift_suggestions:
            pricing_score += 3
        
        # Quality justification
        quality_words = ['premium', 'high-quality', 'durable', 'lasting', 'finest']
        if any(word in full_text for word in quality_words):
            pricing_score += 2
        
        # Bundle/set value
        bundle_words = ['set', 'collection', 'bundle', 'package']
        if any(word in full_text for word in bundle_words):
            pricing_score += 2
        
        # Comparison to alternatives
        comparison_words = ['unlike', 'better than', 'superior', 'compared to']
        if any(word in full_text for word in comparison_words):
            pricing_score += 1
            
        scores['pricing_psychology'] = min(10, pricing_score)
        
        # 10. Competitive Advantage (vs mass-produced items)
        competitive_score = 0
        
        # Handmade emphasis
        if 'handmade' in full_text or 'hand-crafted' in full_text:
            competitive_score += 3
        
        # Unique selling proposition
        usp_words = ['exclusive', 'limited', 'rare', 'one-of-a-kind', 'original design']
        if any(word in full_text for word in usp_words):
            competitive_score += 2
        
        # Artisan credentials
        if listing.etsy_story_behind or 'years of experience' in full_text:
            competitive_score += 2
        
        # Sustainability advantage
        if listing.etsy_sustainability_info:
            competitive_score += 2
        
        # Made-to-order emphasis
        if 'made to order' in full_text or listing.etsy_when_made == 'made_to_order':
            competitive_score += 1
            
        scores['competitive_advantage'] = min(10, competitive_score)
        
        # Calculate overall score
        total_score = sum(scores.values())
        scores['total_score'] = total_score
        scores['percentage'] = (total_score / 100) * 100
        
        return scores

    def analyze_results(self):
        """Analyze all generated listings and provide comprehensive evaluation"""
        print("\n" + "="*70)
        print("COMPREHENSIVE ETSY LISTING QUALITY EVALUATION")
        print("="*70)
        
        total_listings = len([r for r in self.results if r['status'] == 'success'])
        
        if total_listings == 0:
            print("❌ No successful listings generated for evaluation")
            return
        
        all_scores = []
        detailed_results = []
        
        for result in self.results:
            if result['status'] != 'success':
                continue
                
            listing = result['listing']
            product = result['product']
            
            print(f"\n{'='*50}")
            print(f"EVALUATING: {product.name}")
            print(f"Brand Tone: {product.brand_tone}")
            print(f"Occasion: {product.occasion}")
            print(f"{'='*50}")
            
            # Evaluate quality
            scores = self.evaluate_listing_quality(listing)
            all_scores.append(scores)
            
            # Display detailed scores
            print(f"\n📊 QUALITY SCORES (Target: 90+/100)")
            print(f"1. Title SEO: {scores['title_seo']}/10")
            print(f"2. Tags Strategy: {scores['tags_strategy']}/10")
            print(f"3. Description Storytelling: {scores['description_storytelling']}/10")
            print(f"4. Search Visibility: {scores['search_visibility']}/10")
            print(f"5. Conversion Elements: {scores['conversion_elements']}/10")
            print(f"6. Brand Voice: {scores['brand_voice']}/10")
            print(f"7. Visual Recommendations: {scores['visual_recommendations']}/10")
            print(f"8. Personalization Options: {scores['personalization_options']}/10")
            print(f"9. Pricing Psychology: {scores['pricing_psychology']}/10")
            print(f"10. Competitive Advantage: {scores['competitive_advantage']}/10")
            print(f"\n🎯 TOTAL SCORE: {scores['total_score']}/100 ({scores['percentage']:.1f}%)")
            
            # Quality assessment
            if scores['total_score'] >= 90:
                quality_status = "🏆 EXCELLENT - Beats competitors!"
            elif scores['total_score'] >= 80:
                quality_status = "✅ GOOD - Competitive quality"
            elif scores['total_score'] >= 70:
                quality_status = "⚠️ FAIR - Needs improvement"
            else:
                quality_status = "❌ POOR - Major optimization needed"
            
            print(f"📈 QUALITY ASSESSMENT: {quality_status}")
            
            # Show actual content samples
            print(f"\n📝 GENERATED CONTENT SAMPLES:")
            print(f"Title: {listing.etsy_title}")
            if listing.etsy_tags:
                try:
                    tags = json.loads(listing.etsy_tags)
                    print(f"Tags: {', '.join(tags[:5])}...")
                except:
                    print(f"Tags: {listing.etsy_tags[:100]}...")
            if listing.etsy_description:
                print(f"Description (first 200 chars): {listing.etsy_description[:200]}...")
            
            detailed_results.append({
                'product_name': product.name,
                'brand_tone': product.brand_tone,
                'scores': scores,
                'listing': listing
            })
        
        # Overall analysis
        print(f"\n{'='*70}")
        print("OVERALL ANALYSIS & COMPETITOR COMPARISON")
        print(f"{'='*70}")
        
        avg_total = sum(s['total_score'] for s in all_scores) / len(all_scores)
        avg_by_category = {}
        for category in ['title_seo', 'tags_strategy', 'description_storytelling', 'search_visibility', 
                        'conversion_elements', 'brand_voice', 'visual_recommendations', 
                        'personalization_options', 'pricing_psychology', 'competitive_advantage']:
            avg_by_category[category] = sum(s[category] for s in all_scores) / len(all_scores)
        
        print(f"📊 AVERAGE SCORES ACROSS ALL LISTINGS:")
        for category, avg_score in avg_by_category.items():
            category_name = category.replace('_', ' ').title()
            print(f"  {category_name}: {avg_score:.1f}/10")
        
        print(f"\n🎯 OVERALL AVERAGE: {avg_total:.1f}/100 ({(avg_total/100)*100:.1f}%)")
        
        # Competitor comparison
        print(f"\n🔥 COMPETITOR COMPARISON:")
        if avg_total >= 90:
            print("✅ SUPERIOR to Helium 10, Jasper AI, and CopyMonkey")
            print("  - Storytelling exceeds competitor emotional engagement")
            print("  - SEO strategy more Etsy-specific than generic tools")
            print("  - Personalization options more comprehensive")
        elif avg_total >= 80:
            print("⚖️ COMPETITIVE with major tools, some advantages")
            print("  - Strong in artisan storytelling")
            print("  - Good Etsy-specific optimization")
            print("  - Room for improvement in conversion elements")
        else:
            print("⚠️ BELOW competitor standards - optimization needed")
            print("  - Improve emotional storytelling")
            print("  - Enhance SEO keyword strategy")
            print("  - Strengthen conversion elements")
        
        # Specific recommendations
        print(f"\n🎯 PRIORITY IMPROVEMENTS:")
        lowest_scores = sorted(avg_by_category.items(), key=lambda x: x[1])[:3]
        for i, (category, score) in enumerate(lowest_scores, 1):
            category_name = category.replace('_', ' ').title()
            print(f"{i}. {category_name} (Current: {score:.1f}/10)")
            self._get_improvement_suggestions(category)
        
        return detailed_results, avg_total
    
    def _get_improvement_suggestions(self, category):
        """Provide specific improvement suggestions for each category"""
        suggestions = {
            'title_seo': [
                "  • Front-load primary keywords in first 50 characters",
                "  • Include brand tone keywords (handmade, vintage, etc.)",
                "  • Use buyer intent keywords (gift, custom, personalized)",
                "  • Optimize character count (80-120 chars for best results)"
            ],
            'tags_strategy': [
                "  • Use all 13 tags available",
                "  • Mix broad and long-tail keywords",
                "  • Include gift-giving occasion tags",
                "  • Add material and technique tags"
            ],
            'description_storytelling': [
                "  • Lead with emotional hook in first line",
                "  • Include creation story and inspiration",
                "  • Detail materials and crafting process",
                "  • Add care instructions and gift appeal"
            ],
            'search_visibility': [
                "  • Align title keywords with tag keywords",
                "  • Use Etsy-specific search terms",
                "  • Include seasonal/occasion keywords",
                "  • Optimize for mobile search behavior"
            ],
            'conversion_elements': [
                "  • Add clear processing/shipping timeframes",
                "  • Include trust signals and guarantees",
                "  • Mention materials and quality features",
                "  • Position as perfect gift option"
            ],
            'brand_voice': [
                "  • Strengthen artisan story and personal touch",
                "  • Maintain consistent brand tone throughout",
                "  • Emphasize unique selling proposition",
                "  • Share inspiration and creative process"
            ],
            'visual_recommendations': [
                "  • Suggest specific photo angles and styling",
                "  • Mention color variations and options",
                "  • Include size and scale references",
                "  • Recommend lifestyle context photos"
            ],
            'personalization_options': [
                "  • Clearly state customization available",
                "  • Detail personalization process",
                "  • Show example customizations",
                "  • Mention made-to-order benefits"
            ],
            'pricing_psychology': [
                "  • Justify price with quality and uniqueness",
                "  • Position as investment/heirloom piece",
                "  • Compare to mass-produced alternatives",
                "  • Emphasize gift value proposition"
            ],
            'competitive_advantage': [
                "  • Emphasize handmade vs mass-produced",
                "  • Highlight artisan expertise and experience",
                "  • Mention sustainable/ethical practices",
                "  • Show unique design elements"
            ]
        }
        
        for suggestion in suggestions.get(category, ["  • Review and optimize this category"]):
            print(suggestion)

    def generate_improvement_recommendations(self):
        """Generate specific recommendations to achieve 10/10 quality"""
        print(f"\n{'='*70}")
        print("OPTIMIZATION RECOMMENDATIONS FOR 10/10 QUALITY")
        print(f"{'='*70}")
        
        print("""
🎯 PROMPT OPTIMIZATION STRATEGY:

1. ENHANCE EMOTIONAL STORYTELLING:
   - Add requirement for personal creation story
   - Include inspiration source and artistic journey
   - Emphasize emotional connection with buyer
   - Require mention of care and love in crafting

2. IMPROVE SEO KEYWORD STRATEGY:
   - Front-load titles with highest-traffic keywords
   - Require 3+ long-tail keyword phrases
   - Include gift-giving scenarios in every listing
   - Add seasonal/occasion optimization

3. STRENGTHEN CONVERSION ELEMENTS:
   - Mandate processing time clarity
   - Require materials transparency
   - Add quality guarantees and care instructions
   - Include gift positioning statements

4. ENHANCE BRAND VOICE AUTHENTICITY:
   - Require first-person storytelling elements
   - Add artisan credentials and experience
   - Include unique selling proposition
   - Emphasize handmade vs mass-produced advantages

5. OPTIMIZE TAGS STRATEGY:
   - Ensure all 13 tags are used
   - Mix broad terms with specific long-tail phrases
   - Include buyer intent keywords (gift for, custom, etc.)
   - Add material and technique tags

🔧 TECHNICAL IMPROVEMENTS:
   - Fix JSON parsing error handling
   - Enhance fallback content quality
   - Add retry mechanism for failed generations
   - Implement quality validation before saving

🏆 QUALITY VALIDATION:
   - Implement pre-save quality scoring
   - Reject listings below 85/100 score
   - Auto-regenerate until quality threshold met
   - Track quality improvements over time
        """)

def main():
    """Main execution function"""
    print("🎨 ETSY LISTING QUALITY EVALUATION SYSTEM")
    print("Comprehensive testing to achieve 10/10 quality vs competitors")
    print("="*70)
    
    evaluator = EtsyQualityEvaluator()
    
    # Step 1: Create test products
    print("\n1️⃣ Creating diverse test products...")
    evaluator.create_test_products()
    
    # Step 2: Generate listings
    print("\n2️⃣ Generating Etsy listings...")
    evaluator.generate_listings()
    
    # Step 3: Evaluate quality
    print("\n3️⃣ Evaluating listing quality...")
    results, avg_score = evaluator.analyze_results()
    
    # Step 4: Generate recommendations
    print("\n4️⃣ Generating improvement recommendations...")
    evaluator.generate_improvement_recommendations()
    
    # Final summary
    print(f"\n{'='*70}")
    print("EVALUATION COMPLETE")
    print(f"{'='*70}")
    print(f"📊 Final Average Score: {avg_score:.1f}/100")
    if avg_score >= 90:
        print("🏆 ACHIEVEMENT UNLOCKED: 10/10 Quality - Superior to competitors!")
    else:
        print(f"🎯 Target: 90+/100 (Current gap: {90-avg_score:.1f} points)")
    
    print(f"\n💡 Next Steps:")
    print(f"1. Implement recommended prompt optimizations")
    print(f"2. Fix technical issues (JSON parsing, fallbacks)")
    print(f"3. Re-test with improved implementation")
    print(f"4. Validate 90+ average score achievement")

if __name__ == "__main__":
    main()