#!/usr/bin/env python
"""
Quality Validation System Demonstration

This script demonstrates the comprehensive Amazon listing quality validator
that ensures 10/10 emotional, conversion-focused output.
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'listory.settings')
django.setup()

from apps.listings.quality_validator import ListingQualityValidator
import json


def test_poor_quality_listing():
    """Test validation of a poor-quality listing."""
    print("\n" + "="*80)
    print("TESTING POOR QUALITY LISTING")
    print("="*80)
    
    poor_listing = {
        "title": "Product for sale",
        "bullet_points": "Good quality\nNice product\nWorks well\nRecommended\nGreat value",
        "long_description": "This is a good product. It has many features. You should buy it. It works.",
        "faqs": "Q: Is it good? A: Yes."
    }
    
    validator = ListingQualityValidator()
    report = validator.get_validation_json(poor_listing)
    
    print(f"Overall Score: {report['overall_score']}/10 (Grade: {report['grade']})")
    print(f"Emotion Score: {report['emotion_score']}/10")
    print(f"Conversion Score: {report['conversion_score']}/10")
    print(f"Trust Score: {report['trust_score']}/10")
    
    print(f"\nSummary: {report['summary']}")
    
    print(f"\nSection Breakdown:")
    for section in report['section_scores']:
        print(f"  {section['section']}: {section['score']}/{section['max_score']} ({section['percentage']}%)")
    
    print(f"\nTop Issues Found:")
    for i, issue in enumerate(report['issues'][:3], 1):
        print(f"  {i}. {issue['type'].upper()}: {issue['message']}")
        print(f"     Solution: {issue['suggestion']}")
    
    print(f"\nAction Items:")
    for i, action in enumerate(report['action_items'][:5], 1):
        print(f"  {i}. {action}")


def test_excellent_quality_listing():
    """Test validation of an excellent-quality listing."""
    print("\n" + "="*80)
    print("TESTING EXCELLENT QUALITY LISTING")
    print("="*80)
    
    excellent_listing = {
        "title": "Finally, Translation Earbuds That Actually Work in Real Conversations - TIMEKETTLE WT2 Edge for Instant Confidence Anywhere",
        "bullet_points": """INSTANT CONFIDENCE: Feel like a local anywhere in the world with real-time translation that actually captures context and emotion - trusted by 50,000+ travelers who refuse to let language barriers limit their adventures

NEVER STRUGGLE AGAIN: End those awkward 'smile and nod' moments forever with AI that understands slang, cultural nuances, and technical terms - business executives report closing international deals they couldn't before

BREAKTHROUGH RESULTS: Experience the freedom of natural conversations in 40+ languages with 95% accuracy that outperforms Google Translate - users say it's like having a personal interpreter in your ear

LIFE-CHANGING CONVENIENCE: Transform from confused tourist to confident communicator in seconds with touch-free operation and 12-hour battery life - perfect for meetings, travel, or learning new languages

GUARANTEED SUCCESS: Join 10,000+ satisfied customers with our 30-day money-back guarantee and 1-year warranty - if you're not amazed by your first conversation, return it risk-free""",
        "long_description": """Tired of awkward language barriers ruining your travels and business opportunities? You're not alone. Studies show 73% of international travelers avoid meaningful conversations due to language anxiety, missing out on authentic experiences and connections.

That's exactly why we created the TIMEKETTLE WT2 Edge - the breakthrough translation device that finally delivers on the promise of effortless global communication.

TRANSFORM YOUR EXPERIENCE
Imagine walking into any restaurant in Tokyo, striking up conversations with locals in Paris, or confidently presenting to international clients - all without the stress of miscommunication. The WT2 Edge makes this your new reality with AI translation that understands context, emotion, and cultural nuances.

JOIN THE COMMUNICATION REVOLUTION
Over 50,000 professionals, travelers, and language learners worldwide have already discovered the confidence that comes with perfect translation. Business leaders report closing deals they couldn't before, travelers share authentic cultural experiences, and families connect across language barriers like never before.

Ready to experience the difference? Order your WT2 Edge today and join the thousands who've discovered true global communication freedom.""",
        "faqs": """Q: Will this actually work for someone like me who's terrible with technology? A: That's exactly who we designed this for! Sarah, a 67-year-old grandmother, went from confused to confident in under 5 minutes. The setup is literally just 'turn on and go' - no apps, no complicated steps.

Q: I've been burned by cheap knockoffs before. How do I know this is different? A: Great question! Unlike those flimsy imitations, this uses the same translation technology that powers Google Translate, but optimized for real conversations. Plus, our 30-day 'love it or return it' guarantee means zero risk to you.

Q: Can it handle fast conversations or technical business terms? A: Absolutely! We tested this with international CEOs during rapid-fire negotiations. The AI processes context and industry jargon in real-time. Users report it's actually faster than human interpreters for technical discussions."""
    }
    
    validator = ListingQualityValidator()
    report = validator.get_validation_json(excellent_listing)
    
    print(f"Overall Score: {report['overall_score']}/10 (Grade: {report['grade']})")
    print(f"Emotion Score: {report['emotion_score']}/10")
    print(f"Conversion Score: {report['conversion_score']}/10")
    print(f"Trust Score: {report['trust_score']}/10")
    
    print(f"\nSummary: {report['summary']}")
    
    print(f"\nSection Breakdown:")
    for section in report['section_scores']:
        print(f"  {section['section']}: {section['score']}/{section['max_score']} ({section['percentage']}%)")
        if section['strengths']:
            print(f"    Strengths: {section['strengths'][0]}")
    
    if report['issues']:
        print(f"\nRemaining Improvement Opportunities:")
        for i, issue in enumerate(report['issues'][:2], 1):
            print(f"  {i}. {issue['message']}")
            print(f"     Enhancement: {issue['suggestion']}")


def test_api_integration():
    """Test the API integration for quality validation."""
    print("\n" + "="*80)
    print("TESTING API INTEGRATION")
    print("="*80)
    
    # Simulate API request data
    api_request_data = {
        "title": "Gaming Chair with LED Lights",
        "bullet_points": "Comfortable seating\nLED lighting\nAdjustable height\nGood for gaming",
        "long_description": "This gaming chair has LED lights and is comfortable.",
        "faqs": ""
    }
    
    validator = ListingQualityValidator()
    api_response = validator.get_validation_json(api_request_data)
    
    print("API Response Format:")
    print(json.dumps({
        "status": "success",
        "message": "Quality validation completed",
        "validation_report": {
            "overall_score": api_response["overall_score"],
            "grade": api_response["grade"],
            "emotion_score": api_response["emotion_score"],
            "conversion_score": api_response["conversion_score"],
            "trust_score": api_response["trust_score"],
            "summary": api_response["summary"][:100] + "...",
            "section_count": len(api_response["section_scores"]),
            "issues_count": len(api_response["issues"]),
            "action_items_count": len(api_response["action_items"])
        }
    }, indent=2))
    
    print(f"\nKey Improvement Recommendations:")
    for action in api_response["action_items"][:3]:
        print(f"  • {action}")


def demonstrate_validation_features():
    """Demonstrate specific validation features."""
    print("\n" + "="*80)
    print("QUALITY VALIDATION FEATURES DEMONSTRATION")
    print("="*80)
    
    print("\n1. EMOTIONAL ENGAGEMENT DETECTION:")
    print("   ✓ Identifies power words (breakthrough, finally, transform)")
    print("   ✓ Scores urgency language (limited time, never again)")
    print("   ✓ Detects transformation outcomes (feel confident, achieve success)")
    
    print("\n2. CONVERSION OPTIMIZATION ANALYSIS:")
    print("   ✓ Problem-Agitation-Solution structure validation")
    print("   ✓ Social proof element detection")
    print("   ✓ Call-to-action strength assessment")
    print("   ✓ Risk reversal identification")
    
    print("\n3. AI WRITING ISSUE DETECTION:")
    print("   ✓ Robotic corporate language flagging")
    print("   ✓ Generic feature-focused content identification")
    print("   ✓ Keyword stuffing detection")
    print("   ✓ Missing emotional hooks analysis")
    
    print("\n4. TRUST & CREDIBILITY SCORING:")
    print("   ✓ Guarantee and warranty mention tracking")
    print("   ✓ Specific social proof number validation")
    print("   ✓ Certification and testing references")
    print("   ✓ FAQ quality and completeness assessment")
    
    print("\n5. ACTIONABLE IMPROVEMENT SYSTEM:")
    print("   ✓ Prioritized issue identification (Critical > Major > Minor)")
    print("   ✓ Specific rewrite suggestions with examples")
    print("   ✓ Section-by-section improvement roadmap")
    print("   ✓ Grade-based performance tracking (A+ to F)")


if __name__ == "__main__":
    print("AMAZON LISTING QUALITY VALIDATION SYSTEM")
    print("Ensuring 10/10 Emotional, Conversion-Focused Output")
    
    # Run all demonstrations
    demonstrate_validation_features()
    test_poor_quality_listing()
    test_excellent_quality_listing()
    test_api_integration()
    
    print("\n" + "="*80)
    print("VALIDATION SYSTEM READY FOR INTEGRATION")
    print("="*80)
    print("\nAPI Endpoints Available:")
    print("  POST /api/listings/listings/validate_quality/")
    print("    - Standalone quality validation")
    print("  GET /api/listings/listings/{id}/quality_report/")
    print("    - Quality report for existing listing")
    print("\nIntegration:")
    print("  - Automatic validation during listing generation")
    print("  - Quality scores stored in database")
    print("  - Real-time feedback for content improvement")
    print("\nNext Steps:")
    print("  1. Test API endpoints with real listing data")
    print("  2. Integrate validation into frontend interface")
    print("  3. Add quality score dashboard for performance tracking")