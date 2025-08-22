#!/usr/bin/env python
"""
TARGETED MARKETPLACE EVALUATOR
==============================

Focuses on key marketplaces to quickly assess quality and identify optimization opportunities.
"""

import os
import sys
import django
import json
from datetime import datetime
from typing import Dict, List, Tuple, Any

# Add the backend directory to the Python path
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_path)

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.services import ListingGeneratorService
from apps.core.models import Product
from django.contrib.auth.models import User

class TargetedQualityEvaluator:
    """Quick quality evaluation for key marketplaces."""
    
    def __init__(self):
        self.service = ListingGeneratorService()
        self.user, _ = User.objects.get_or_create(username='targeted_evaluator')
        
        # Single test product for speed
        self.test_product = {
            'name': 'Professional Gaming Headset',
            'brand_name': 'AudioPro',
            'description': 'Professional wireless gaming headset with active noise cancellation',
            'categories': 'Electronics > Audio > Headphones',
            'features': 'Wireless Connectivity\nActive Noise Cancellation\n50-hour Battery Life\nErgonomic Design\nPremium Sound Quality\nDetachable Microphone',
            'price': 129.99,
            'occasion': 'christmas',
            'brand_tone': 'professional'
        }

    def quick_evaluate_listing(self, listing: Any, marketplace: str) -> Dict[str, Any]:
        """Quick evaluation with key quality indicators."""
        results = {
            'marketplace': marketplace,
            'status': listing.status,
            'issues': [],
            'quality_score': 0.0,
            'content_analysis': {}
        }
        
        if listing.status != 'completed':
            results['issues'].append(f"Generation failed: {listing.status}")
            return results
        
        # Get content based on platform
        if marketplace.startswith('walmart'):
            title = getattr(listing, 'walmart_product_title', '')
            features = getattr(listing, 'walmart_key_features', '')
            description = getattr(listing, 'walmart_long_description', '')
            keywords = getattr(listing, 'walmart_search_terms', '')
        else:
            title = getattr(listing, 'amazon_title', '')
            features = getattr(listing, 'amazon_bullet_points', '')
            description = getattr(listing, 'amazon_description', '')
            keywords = getattr(listing, 'amazon_keywords', '')
        
        # Content analysis
        results['content_analysis'] = {
            'title_length': len(title) if title else 0,
            'title_present': bool(title),
            'features_count': len(features.split('\n')) if features else 0,
            'features_present': bool(features),
            'description_length': len(description.split()) if description else 0,
            'description_present': bool(description),
            'keywords_count': len(keywords.split(',')) if keywords else 0,
            'keywords_present': bool(keywords)
        }
        
        # Quality scoring (simplified 0-10 scale)
        score = 0.0
        
        # Title quality (0-3 points)
        if title:
            if 50 <= len(title) <= 200:
                score += 2.0
            elif title:
                score += 1.0
            if 'AudioPro' in title or 'professional' in title.lower():
                score += 1.0
        else:
            results['issues'].append("Missing title")
        
        # Features quality (0-2 points)
        if features:
            feature_count = len([f for f in features.split('\n') if f.strip()])
            if feature_count >= 4:
                score += 2.0
            elif feature_count >= 2:
                score += 1.0
        else:
            results['issues'].append("Missing features")
        
        # Description quality (0-2 points)
        if description:
            word_count = len(description.split())
            if word_count >= 100:
                score += 2.0
            elif word_count >= 50:
                score += 1.0
        else:
            results['issues'].append("Missing description")
        
        # Keywords quality (0-1 point)
        if keywords and len(keywords.split(',')) >= 5:
            score += 1.0
        else:
            results['issues'].append("Insufficient keywords")
        
        # Cultural/platform fit (0-2 points)
        all_content = f"{title} {features} {description}".lower()
        if marketplace.startswith('walmart'):
            if any(term in all_content for term in ['america', 'family', 'value']):
                score += 1.0
            if any(term in all_content for term in ['rollback', 'great value', 'save']):
                score += 1.0
        else:
            if any(term in all_content for term in ['prime', 'quality', 'professional']):
                score += 1.0
            if 'christmas' in all_content:
                score += 1.0
        
        results['quality_score'] = score
        
        return results

    def test_key_marketplaces(self) -> Dict[str, Any]:
        """Test key marketplaces quickly."""
        print('🎯 TARGETED MARKETPLACE QUALITY EVALUATION')
        print('=' * 50)
        
        key_markets = [
            ('walmart_usa', 'en-us', 'walmart'),
            ('walmart_canada', 'en-ca', 'walmart'),
            ('walmart_mexico', 'es-mx', 'walmart'),
            ('us', 'en-us', 'amazon'),
            ('uk', 'en-gb', 'amazon'),
            ('ca', 'en-ca', 'amazon'),
            ('de', 'de-de', 'amazon'),
            ('fr', 'fr-fr', 'amazon')
        ]
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'test_product': self.test_product['name'],
            'markets_tested': [],
            'summary': {}
        }
        
        for marketplace, language, platform in key_markets:
            print(f'\n🔍 Testing {marketplace.upper()}...')
            
            try:
                # Create test product
                product = Product.objects.create(
                    user=self.user,
                    target_platform=platform,
                    marketplace=marketplace,
                    marketplace_language=language,
                    **self.test_product
                )
                
                # Generate listing
                listing = self.service.generate_listing(product.id, platform)
                
                # Evaluate
                evaluation = self.quick_evaluate_listing(listing, marketplace)
                results['markets_tested'].append(evaluation)
                
                # Print results
                status_emoji = '✅' if evaluation['status'] == 'completed' else '❌'
                score_emoji = '🟢' if evaluation['quality_score'] >= 8 else '🟡' if evaluation['quality_score'] >= 6 else '🔴'
                
                print(f'   {status_emoji} Status: {evaluation["status"]}')
                print(f'   {score_emoji} Quality Score: {evaluation["quality_score"]:.1f}/10.0')
                
                if evaluation['content_analysis']:
                    ca = evaluation['content_analysis']
                    print(f'   📝 Content: Title({ca["title_length"]}c) Features({ca["features_count"]}) Description({ca["description_length"]}w)')
                
                if evaluation['issues']:
                    print(f'   ⚠️  Issues: {", ".join(evaluation["issues"])[:80]}...')
                    
            except Exception as e:
                print(f'   ❌ Error: {str(e)[:100]}...')
                results['markets_tested'].append({
                    'marketplace': marketplace,
                    'status': 'error',
                    'error': str(e),
                    'quality_score': 0.0
                })
            finally:
                # Cleanup
                if 'product' in locals():
                    try:
                        product.delete()
                    except:
                        pass
        
        # Calculate summary
        completed_results = [r for r in results['markets_tested'] if r['status'] == 'completed']
        if completed_results:
            results['summary'] = {
                'total_tested': len(results['markets_tested']),
                'successful': len(completed_results),
                'average_score': sum(r['quality_score'] for r in completed_results) / len(completed_results),
                'best_market': max(completed_results, key=lambda x: x['quality_score'])['marketplace'],
                'worst_market': min(completed_results, key=lambda x: x['quality_score'])['marketplace']
            }
        
        # Save results
        filename = f'targeted_evaluation_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f'\n📊 EVALUATION COMPLETE')
        if completed_results:
            print(f'   Average Score: {results["summary"]["average_score"]:.1f}/10.0')
            print(f'   Best Market: {results["summary"]["best_market"]}')
            print(f'   Worst Market: {results["summary"]["worst_market"]}')
        print(f'   Results saved: {filename}')
        
        return results

def main():
    evaluator = TargetedQualityEvaluator()
    evaluator.test_key_marketplaces()

if __name__ == '__main__':
    main()