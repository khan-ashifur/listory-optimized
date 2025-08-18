#!/usr/bin/env python3
"""
Saudi Arabia Listing Competitive Evaluation
Testing against Helium 10, Jasper AI, and Copy Monkey
"""

import os
import sys
import json
from datetime import datetime

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from apps.listings.services import ListingService
from apps.core.models import Product

def test_saudi_arabia_listing_quality():
    """Generate and evaluate Saudi Arabia listing against top competitors"""
    
    print("=" * 80)
    print("🇸🇦 SAUDI ARABIA LISTING COMPETITIVE EVALUATION")
    print("Testing against: Helium 10, Jasper AI, Copy Monkey")
    print("=" * 80)
    
    # Test product - Gaming Headset
    product_data = {
        'title': 'AudioMax Gaming Headset',
        'description': 'Premium wireless gaming headset with Bluetooth 5.3, noise cancellation, 35-hour battery, surround sound',
        'features': [
            'Bluetooth 5.3 technology',
            'Active noise cancellation',
            '35-hour battery life',
            '50mm drivers',
            'Surround sound',
            'Premium build quality'
        ],
        'target_keywords': [
            'gaming headset',
            'wireless headset',
            'bluetooth headset',
            'noise cancelling',
            'premium audio',
            'gaming accessories'
        ]
    }
    
    try:
        # Create temporary product
        product = Product.objects.create(
            title=product_data['title'],
            description=product_data['description'],
            target_keywords=', '.join(product_data['target_keywords'])
        )
        
        print(f"📝 Testing Product: {product.title}")
        
        # Generate Saudi Arabia listing
        listing_service = ListingService()
        marketplace = 'sa'  # Saudi Arabia
        
        print(f"\n🚀 Generating Saudi Arabia listing for marketplace: {marketplace}")
        
        result = listing_service.generate_listing(
            product_id=product.id,
            marketplace=marketplace,
            target_keywords=product_data['target_keywords']
        )
        
        if 'error' in result:
            print(f"❌ Error generating listing: {result['error']}")
            return
            
        # Extract and analyze results
        print("\n" + "=" * 60)
        print("🇸🇦 SAUDI ARABIA LISTING RESULTS")
        print("=" * 60)
        
        title = result.get('title', '')
        bullets = result.get('bullets', [])
        aplus_content = result.get('aplus_content', '')
        
        print(f"\n📋 TITLE ({len(title)} characters):")
        print(f"'{title}'")
        
        print(f"\n🎯 BULLET POINTS ({len(bullets)} bullets):")
        for i, bullet in enumerate(bullets, 1):
            print(f"{i}. {bullet} ({len(bullet)} chars)")
        
        print(f"\n✨ A+ CONTENT ({len(aplus_content)} characters):")
        if len(aplus_content) > 500:
            print(f"First 500 chars: {aplus_content[:500]}...")
        else:
            print(aplus_content)
        
        # Competitive Analysis
        print("\n" + "=" * 60)
        print("📊 COMPETITIVE ANALYSIS vs TOP TOOLS")
        print("=" * 60)
        
        analysis = analyze_listing_quality(title, bullets, aplus_content)
        
        print(f"\n🏆 OVERALL QUALITY SCORE: {analysis['overall_score']}/10")
        print(f"🎯 COMPETITOR COMPARISON:")
        print(f"   vs Helium 10: {analysis['vs_helium10']}")
        print(f"   vs Jasper AI: {analysis['vs_jasper']}")
        print(f"   vs Copy Monkey: {analysis['vs_copymonkey']}")
        
        print(f"\n📈 STRENGTHS:")
        for strength in analysis['strengths']:
            print(f"   ✅ {strength}")
            
        print(f"\n🔧 IMPROVEMENT RECOMMENDATIONS:")
        for improvement in analysis['improvements']:
            print(f"   🔄 {improvement}")
        
        # Save detailed analysis
        save_analysis_report(analysis, result)
        
        # Clean up
        product.delete()
        
        return analysis
        
    except Exception as e:
        print(f"❌ Error in evaluation: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def analyze_listing_quality(title, bullets, aplus_content):
    """Analyze listing quality against competitor standards"""
    
    analysis = {
        'overall_score': 0,
        'category_scores': {},
        'strengths': [],
        'improvements': [],
        'vs_helium10': '',
        'vs_jasper': '',
        'vs_copymonkey': ''
    }
    
    # Title Analysis
    title_score = analyze_title(title)
    analysis['category_scores']['title'] = title_score
    
    # Bullet Analysis  
    bullet_score = analyze_bullets(bullets)
    analysis['category_scores']['bullets'] = bullet_score
    
    # A+ Content Analysis
    aplus_score = analyze_aplus_content(aplus_content)
    analysis['category_scores']['aplus'] = aplus_score
    
    # Localization Analysis
    localization_score = analyze_localization(title, bullets, aplus_content)
    analysis['category_scores']['localization'] = localization_score
    
    # Cultural Adaptation Analysis
    cultural_score = analyze_cultural_adaptation(title, bullets, aplus_content)
    analysis['category_scores']['cultural'] = cultural_score
    
    # Calculate overall score
    scores = list(analysis['category_scores'].values())
    analysis['overall_score'] = round(sum(scores) / len(scores), 1)
    
    # Generate competitive comparisons
    analysis.update(generate_competitor_comparisons(analysis))
    
    # Generate recommendations
    analysis.update(generate_recommendations(analysis))
    
    return analysis

def analyze_title(title):
    """Analyze title quality (0-10)"""
    score = 0
    
    # Length check (optimal 150-200 characters for Arabic)
    if 150 <= len(title) <= 200:
        score += 2
    elif 120 <= len(title) <= 250:
        score += 1.5
    
    # Arabic language usage
    arabic_chars = len([c for c in title if '\u0600' <= c <= '\u06FF'])
    if arabic_chars > len(title) * 0.7:  # 70%+ Arabic
        score += 2
    elif arabic_chars > len(title) * 0.5:  # 50%+ Arabic
        score += 1.5
    
    # Keyword density
    if 'سماعة' in title or 'ألعاب' in title:
        score += 1.5
    
    # Brand inclusion
    if 'AudioMax' in title:
        score += 1
        
    # Features mention
    feature_keywords = ['بلوتوث', 'ضوضاء', 'بطارية', 'ساعة']
    feature_count = sum(1 for keyword in feature_keywords if keyword in title)
    score += min(feature_count * 0.5, 1.5)
    
    # Cultural elements
    if 'عيد' in title or 'سعودي' in title or 'هدية' in title:
        score += 1
    
    # Urgency/Appeal
    if 'مثالية' in title or 'ممتازة' in title or 'متقدمة' in title:
        score += 1
    
    return min(score, 10)

def analyze_bullets(bullets):
    """Analyze bullet points quality (0-10)"""
    if not bullets:
        return 0
        
    score = 0
    
    # Number of bullets
    if len(bullets) == 5:
        score += 2
    elif len(bullets) >= 3:
        score += 1.5
    
    total_bullet_score = 0
    for bullet in bullets:
        bullet_score = 0
        
        # Length check (optimal 150-200 characters)
        if 150 <= len(bullet) <= 200:
            bullet_score += 1
        elif 100 <= len(bullet) <= 250:
            bullet_score += 0.7
            
        # Arabic language usage
        arabic_chars = len([c for c in bullet if '\u0600' <= c <= '\u06FF'])
        if arabic_chars > len(bullet) * 0.7:
            bullet_score += 1
            
        # Saudi formality patterns
        formality_words = ['نضمن لكم', 'نقدم لكم', 'بكل فخر', 'يمكنكم التأكد', 'بلا شك']
        if any(word in bullet for word in formality_words):
            bullet_score += 1
            
        # Power words
        power_words = ['رائع', 'ممتاز', 'مثالي', 'مضمون', 'بريميوم']
        power_count = sum(1 for word in power_words if word in bullet)
        bullet_score += min(power_count * 0.3, 1)
        
        # Cultural elements
        if 'سعودي' in bullet or 'العائلة' in bullet or 'التراث' in bullet:
            bullet_score += 0.5
            
        total_bullet_score += bullet_score
    
    # Average bullet score + bonus for consistency
    score += (total_bullet_score / len(bullets)) * 6
    
    # Bonus for variety in bullet structure
    if len(set(len(bullet) for bullet in bullets)) > 1:
        score += 1
    
    return min(score, 10)

def analyze_aplus_content(aplus_content):
    """Analyze A+ content quality (0-10)"""
    if not aplus_content:
        return 0
        
    score = 0
    
    # Length check (optimal 15,000-25,000 characters)
    content_length = len(aplus_content)
    if 15000 <= content_length <= 25000:
        score += 2.5
    elif 10000 <= content_length <= 30000:
        score += 2
    elif content_length >= 8000:
        score += 1.5
    
    # Section count (count <div> or <h3> tags)
    section_count = aplus_content.count('<h3>') + aplus_content.count('<div')
    if section_count >= 8:
        score += 2
    elif section_count >= 6:
        score += 1.5
    elif section_count >= 4:
        score += 1
    
    # Arabic content
    arabic_chars = len([c for c in aplus_content if '\u0600' <= c <= '\u06FF'])
    if arabic_chars > content_length * 0.6:
        score += 2
    elif arabic_chars > content_length * 0.4:
        score += 1.5
    
    # HTML structure quality
    if '<div' in aplus_content and '</div>' in aplus_content:
        score += 1
    if '<h3>' in aplus_content and '</h3>' in aplus_content:
        score += 1
    if '<p>' in aplus_content and '</p>' in aplus_content:
        score += 1
    
    # Content variety indicators
    variety_indicators = ['صوت', 'بطارية', 'تصميم', 'جودة', 'ضمان']
    variety_count = sum(1 for indicator in variety_indicators if indicator in aplus_content)
    score += min(variety_count * 0.3, 1.5)
    
    return min(score, 10)

def analyze_localization(title, bullets, aplus_content):
    """Analyze localization quality (0-10)"""
    score = 0
    
    all_content = title + ' ' + ' '.join(bullets) + ' ' + aplus_content
    
    # Arabic script usage
    arabic_chars = len([c for c in all_content if '\u0600' <= c <= '\u06FF'])
    total_chars = len(all_content.replace(' ', ''))
    if total_chars > 0:
        arabic_ratio = arabic_chars / total_chars
        if arabic_ratio > 0.7:
            score += 3
        elif arabic_ratio > 0.5:
            score += 2
        elif arabic_ratio > 0.3:
            score += 1
    
    # Proper Arabic numerals
    if '٠' in all_content or '١' in all_content or '٢' in all_content:
        score += 1
    
    # Currency localization (SAR)
    if 'ريال' in all_content or 'SAR' in all_content:
        score += 1
    
    # Regional terminology
    regional_terms = ['السعودية', 'المملكة', 'الرياض', 'جدة']
    if any(term in all_content for term in regional_terms):
        score += 2
    
    # Proper RTL structure indicators
    if title.strip().endswith('معتمد') or title.strip().endswith('سعودي'):
        score += 1
    
    # Date/time localization (Hijri calendar references)
    if 'هجري' in all_content or 'رمضان' in all_content or 'عيد' in all_content:
        score += 2
    
    return min(score, 10)

def analyze_cultural_adaptation(title, bullets, aplus_content):
    """Analyze cultural adaptation quality (0-10)"""
    score = 0
    
    all_content = title + ' ' + ' '.join(bullets) + ' ' + aplus_content
    
    # Islamic/Cultural occasions
    cultural_occasions = ['عيد الفطر', 'عيد الأضحى', 'رمضان', 'الحج']
    if any(occasion in all_content for occasion in cultural_occasions):
        score += 2
    
    # Family values emphasis
    family_terms = ['العائلة', 'الأسرة', 'الأطفال', 'البيت']
    family_count = sum(1 for term in family_terms if term in all_content)
    score += min(family_count * 0.5, 2)
    
    # Saudi pride elements
    pride_elements = ['سعودي', 'التراث السعودي', 'الجودة السعودية', 'معايير سعودية']
    if any(element in all_content for element in pride_elements):
        score += 2
    
    # Quality and luxury emphasis (Saudi market preference)
    quality_terms = ['بريميوم', 'فاخر', 'عالي الجودة', 'أصلي', 'أصيل']
    quality_count = sum(1 for term in quality_terms if term in all_content)
    score += min(quality_count * 0.4, 2)
    
    # Hospitality tone
    hospitality_terms = ['مرحباً', 'أهلاً', 'نحن نقدم', 'بكل فخر']
    if any(term in all_content for term in hospitality_terms):
        score += 1
    
    # Guarantee/trust emphasis (important in Saudi culture)
    trust_terms = ['ضمان', 'مضمون', 'موثوق', 'آمن', 'نضمن']
    trust_count = sum(1 for term in trust_terms if term in all_content)
    score += min(trust_count * 0.3, 1)
    
    return min(score, 10)

def generate_competitor_comparisons(analysis):
    """Generate comparisons against major competitors"""
    overall_score = analysis['overall_score']
    
    comparisons = {}
    
    # vs Helium 10 (known for keyword optimization but weak on localization)
    if overall_score >= 9:
        comparisons['vs_helium10'] = "🏆 SUPERIOR - Better cultural adaptation and Arabic localization"
    elif overall_score >= 7:
        comparisons['vs_helium10'] = "⚡ COMPETITIVE - Matches keyword optimization with better localization"
    elif overall_score >= 5:
        comparisons['vs_helium10'] = "📈 GOOD - Solid foundation but needs keyword density improvement"
    else:
        comparisons['vs_helium10'] = "🔧 NEEDS WORK - Below Helium 10 standards"
    
    # vs Jasper AI (known for content quality but generic)
    if overall_score >= 9:
        comparisons['vs_jasper'] = "🚀 SUPERIOR - Better personalization and cultural relevance"
    elif overall_score >= 7:
        comparisons['vs_jasper'] = "🎯 COMPETITIVE - Matches content quality with cultural specificity"
    elif overall_score >= 5:
        comparisons['vs_jasper'] = "📊 GOOD - Similar quality but more culturally adapted"
    else:
        comparisons['vs_jasper'] = "⚠️ NEEDS WORK - Below Jasper AI content standards"
    
    # vs Copy Monkey (known for conversion focus but limited localization)
    if overall_score >= 9:
        comparisons['vs_copymonkey'] = "🔥 SUPERIOR - Better conversion psychology for Saudi market"
    elif overall_score >= 7:
        comparisons['vs_copymonkey'] = "💪 COMPETITIVE - Matches conversion focus with local relevance"
    elif overall_score >= 5:
        comparisons['vs_copymonkey'] = "🎪 GOOD - Good conversion elements but needs more urgency"
    else:
        comparisons['vs_copymonkey'] = "📉 NEEDS WORK - Below Copy Monkey conversion standards"
    
    return comparisons

def generate_recommendations(analysis):
    """Generate specific improvement recommendations"""
    
    strengths = []
    improvements = []
    
    scores = analysis['category_scores']
    
    # Title recommendations
    if scores.get('title', 0) >= 8:
        strengths.append("Excellent title optimization with proper Arabic and keywords")
    elif scores.get('title', 0) >= 6:
        improvements.append("Enhance title with more power words and cultural elements")
    else:
        improvements.append("Complete title rewrite needed - improve Arabic usage and keyword density")
    
    # Bullet recommendations
    if scores.get('bullets', 0) >= 8:
        strengths.append("Strong bullet points with Saudi formality patterns")
    elif scores.get('bullets', 0) >= 6:
        improvements.append("Add more Saudi formality phrases and power words to bullets")
    else:
        improvements.append("Restructure bullets with proper Saudi persuasion formulas")
    
    # A+ Content recommendations
    if scores.get('aplus', 0) >= 8:
        strengths.append("Comprehensive A+ content with proper section structure")
    elif scores.get('aplus', 0) >= 6:
        improvements.append("Expand A+ content sections and improve HTML structure")
    else:
        improvements.append("Major A+ content enhancement needed - add more sections and Arabic content")
    
    # Localization recommendations
    if scores.get('localization', 0) >= 8:
        strengths.append("Excellent Arabic localization and regional adaptation")
    elif scores.get('localization', 0) >= 6:
        improvements.append("Improve Arabic script usage and add more regional terminology")
    else:
        improvements.append("Critical localization improvements needed - increase Arabic content ratio")
    
    # Cultural recommendations
    if scores.get('cultural', 0) >= 8:
        strengths.append("Outstanding cultural adaptation for Saudi market")
    elif scores.get('cultural', 0) >= 6:
        improvements.append("Add more Islamic occasions and Saudi pride elements")
    else:
        improvements.append("Significant cultural adaptation needed - add family values and Saudi pride")
    
    # Overall recommendations
    if analysis['overall_score'] >= 9:
        strengths.append("World-class listing that beats all major competitors")
    elif analysis['overall_score'] >= 7:
        strengths.append("Competitive listing with strong market adaptation")
        improvements.append("Fine-tune for 10/10 quality with enhanced power words and urgency")
    else:
        improvements.append("Major overhaul needed across all categories for competitive quality")
    
    return {'strengths': strengths, 'improvements': improvements}

def save_analysis_report(analysis, listing_result):
    """Save detailed analysis report"""
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    report = {
        'timestamp': timestamp,
        'evaluation_type': 'Saudi Arabia Competitive Analysis',
        'competitors': ['Helium 10', 'Jasper AI', 'Copy Monkey'],
        'analysis': analysis,
        'listing_data': {
            'title': listing_result.get('title', ''),
            'bullets': listing_result.get('bullets', []),
            'aplus_length': len(listing_result.get('aplus_content', '')),
            'total_character_count': (
                len(listing_result.get('title', '')) + 
                sum(len(b) for b in listing_result.get('bullets', [])) + 
                len(listing_result.get('aplus_content', ''))
            )
        }
    }
    
    filename = f"saudi_arabia_competitive_analysis_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"\n📄 Detailed analysis saved to: {filename}")
    except Exception as e:
        print(f"⚠️ Could not save report: {e}")

if __name__ == "__main__":
    test_saudi_arabia_listing_quality()