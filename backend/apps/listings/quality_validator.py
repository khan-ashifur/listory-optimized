"""
Amazon Listing Quality Validation System

This module provides comprehensive validation for Amazon listings to ensure
10/10 emotional, conversion-focused output that transforms browsers into buyers.
"""

import re
import json
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class IssueType(Enum):
    CRITICAL = "critical"
    MAJOR = "major"
    MINOR = "minor"
    ENHANCEMENT = "enhancement"


@dataclass
class ValidationIssue:
    type: IssueType
    section: str
    message: str
    suggestion: str
    example: str = ""
    score_impact: float = 0.0


@dataclass
class SectionScore:
    section: str
    score: float
    max_score: float
    feedback: str
    improvements: List[str]
    strengths: List[str]


@dataclass
class QualityReport:
    overall_score: float
    max_score: float
    section_scores: List[SectionScore]
    issues: List[ValidationIssue]
    emotion_score: float
    conversion_score: float
    trust_score: float
    summary: str
    action_items: List[str]


class ListingQualityValidator:
    """
    Comprehensive Amazon listing quality validator that ensures 10/10 
    emotional, conversion-focused output.
    """
    
    def __init__(self):
        # Enhanced emotional power words with international variations
        self.emotional_power_words = {
            'high': ['breakthrough', 'revolutionary', 'game-changing', 'instantly', 'finally', 
                    'obsessed', 'never again', 'secret', 'unleash', 'transform', 'dominate',
                    'irresistible', 'magnetic', 'life-changing', 'unstoppable', 'mind-blowing',
                    'jaw-dropping', 'unbelievable', 'phenomenal', 'extraordinary'],
            'medium': ['amazing', 'incredible', 'perfect', 'ultimate', 'premium', 'superior',
                      'exceptional', 'outstanding', 'remarkable', 'exclusive', 'proven',
                      'luxurious', 'professional', 'elegant', 'sophisticated', 'refined'],
            'low': ['good', 'nice', 'great', 'quality', 'reliable', 'effective', 'useful',
                   'practical', 'convenient', 'simple', 'easy', 'comfortable']
        }
        
        # Add international emotional power words
        self.international_power_words = {
            'de': {
                'high': ['revolutionär', 'bahnbrechend', 'unglaublich', 'endlich', 'perfekt',
                        'verwandelt', 'ultimativ', 'unwiderstehlich', 'lebensverändernd'],
                'medium': ['erstaunlich', 'außergewöhnlich', 'premium', 'luxuriös', 'elegant',
                          'professionell', 'hochwertig', 'exklusiv', 'bewährt'],
                'comfort': ['gemütlich', 'mühelos', 'bequem', 'praktisch', 'zuverlässig']
            },
            'fr': {
                'high': ['révolutionnaire', 'incroyable', 'exceptionnel', 'enfin', 'parfait',
                        'transforme', 'ultime', 'irrésistible', 'magique'],
                'medium': ['élégant', 'raffiné', 'luxueux', 'sophistiqué', 'exclusif',
                          'prestigieux', 'supérieur', 'remarquable', 'authentique'],
                'comfort': ['confortable', 'pratique', 'facile', 'simple', 'fiable']
            },
            'it': {
                'high': ['rivoluzionario', 'incredibile', 'eccezionale', 'finalmente', 'perfetto',
                        'trasforma', 'ultimo', 'irresistibile', 'magico'],
                'medium': ['elegante', 'raffinato', 'lussuoso', 'sofisticato', 'esclusivo',
                          'prestigioso', 'superiore', 'straordinario', 'autentico'],
                'comfort': ['comodo', 'pratico', 'facile', 'semplice', 'affidabile']
            },
            'es': {
                'high': ['revolucionario', 'increíble', 'excepcional', 'finalmente', 'perfecto',
                        'transforma', 'último', 'irresistible', 'mágico'],
                'medium': ['elegante', 'refinado', 'lujoso', 'sofisticado', 'exclusivo',
                          'prestigioso', 'superior', 'extraordinario', 'auténtico'],
                'comfort': ['cómodo', 'práctico', 'fácil', 'simple', 'fiable']
            },
            'jp': {
                'high': ['最高', '究極', '革命的', '画期的', '完璧', '変革', '究極的', '魅力的', '素晴らしい'],
                'medium': ['高品質', 'プレミアム', '優秀', '特別', '安心', '信頼', '快適', '便利', '効果的'],
                'comfort': ['安全', '簡単', '使いやすい', 'お客様', '満足', '品質', '保証', '安心']
            },
            'ae': {
                'high': ['ثوري', 'مذهل', 'استثنائي', 'أخيراً', 'مثالي', 'يحول', 'نهائي', 'لا يقاوم', 'سحري'],
                'medium': ['أنيق', 'متقدم', 'فاخر', 'متطور', 'حصري', 'مرموق', 'متفوق', 'رائع', 'أصيل'],
                'comfort': ['مريح', 'عملي', 'سهل', 'بسيط', 'موثوق', 'آمن', 'مضمون', 'جودة عالية']
            },
            'mx': {
                'high': ['increíble', 'revolucionario', 'extraordinario', 'fantástico', 'perfecto', 'transforma', 'último', 'irresistible', 'mágico'],
                'medium': ['excelente', 'premium', 'de lujo', 'profesional', 'súper', 'genial', 'padrísimo', 'fabuloso', 'auténtico'],
                'comfort': ['cómodo', 'fácil', 'práctico', 'confiable', 'seguro', 'garantizado', 'mexicano', 'familiar']
            }
        }
        
        self.urgency_words = ['now', 'today', 'limited', 'exclusive', 'before', 'until', 
                             'hurry', 'expires', 'only', 'last chance', 'final', 'ending soon']
        
        self.social_proof_indicators = ['customers', 'users', 'people', 'reviews', 'rated',
                                       'recommended', 'trusted', 'verified', 'testimonials']
        
        self.trust_builders = ['guarantee', 'warranty', 'certified', 'tested', 'approved',
                              'money-back', 'risk-free', 'satisfaction', 'return']
        
        self.robotic_phrases = [
            'state-of-the-art', 'cutting-edge', 'innovative solution', 
            'comprehensive solution', 'market-leading', 'industry-standard',
            'world-class', 'next-generation', 'advanced technology',
            'enterprise-grade', 'professional-grade', 'commercial-grade'
        ]
        
        self.generic_corporate_language = [
            'leverage', 'synergy', 'paradigm', 'holistic', 'streamline',
            'optimize', 'maximize', 'facilitate', 'enhance', 'implement',
            'utilize', 'deliverables', 'best-in-class', 'turnkey solution'
        ]

    def validate_listing(self, listing_data: Dict[str, Any]) -> QualityReport:
        """
        Validates an Amazon listing and returns a comprehensive quality report.
        
        Args:
            listing_data: Dictionary containing listing fields (title, bullet_points, 
                         long_description, faqs, etc.)
        
        Returns:
            QualityReport with scores, feedback, and improvement suggestions
        """
        issues = []
        section_scores = []
        
        # Validate each section
        title_score = self._validate_title(listing_data.get('title', ''), issues)
        section_scores.append(title_score)
        
        bullets_score = self._validate_bullets(listing_data.get('bullet_points', ''), issues)
        section_scores.append(bullets_score)
        
        description_score = self._validate_description(listing_data.get('long_description', ''), issues)
        section_scores.append(description_score)
        
        faqs_score = self._validate_faqs(listing_data.get('faqs', ''), issues)
        section_scores.append(faqs_score)
        
        # Calculate overall scores
        total_score = sum(score.score for score in section_scores)
        max_total_score = sum(score.max_score for score in section_scores)
        overall_score = (total_score / max_total_score) * 10 if max_total_score > 0 else 0
        
        # Calculate emotional metrics
        emotion_score = self._calculate_emotion_score(listing_data)
        conversion_score = self._calculate_conversion_score(listing_data)
        trust_score = self._calculate_trust_score(listing_data)
        
        # Generate summary and action items
        summary = self._generate_summary(overall_score, emotion_score, conversion_score, trust_score)
        action_items = self._generate_action_items(issues, section_scores)
        
        return QualityReport(
            overall_score=round(overall_score, 1),
            max_score=10.0,
            section_scores=section_scores,
            issues=issues,
            emotion_score=emotion_score,
            conversion_score=conversion_score,
            trust_score=trust_score,
            summary=summary,
            action_items=action_items
        )

    def _validate_title(self, title: str, issues: List[ValidationIssue]) -> SectionScore:
        """Validates the product title for emotional engagement and SEO."""
        score = 0
        max_score = 20
        feedback_parts = []
        improvements = []
        strengths = []
        
        if not title or len(title.strip()) == 0:
            issues.append(ValidationIssue(
                type=IssueType.CRITICAL,
                section="Title",
                message="Title is missing or empty",
                suggestion="Create a compelling title with emotional hook and primary keywords",
                example="Finally, Translation Earbuds That Actually Work in Real Conversations",
                score_impact=10.0
            ))
            return SectionScore("Title", 0, max_score, "Title is missing", improvements, strengths)
        
        # Check length (optimal 150-200 characters)
        title_length = len(title)
        if title_length < 50:
            issues.append(ValidationIssue(
                type=IssueType.MAJOR,
                section="Title",
                message=f"Title too short ({title_length} chars) - missing keyword opportunities",
                suggestion="Expand title to 150-200 characters with more keywords and benefits",
                example="The Cleaning Tool Busy Parents Are Obsessed With - Premium Microfiber Kit",
                score_impact=3.0
            ))
            improvements.append("Expand title length to 150-200 characters for better SEO")
        elif title_length > 200:
            issues.append(ValidationIssue(
                type=IssueType.MINOR,
                section="Title",
                message=f"Title too long ({title_length} chars) - may be truncated",
                suggestion="Trim to 200 characters while keeping emotional hook and main keywords",
                score_impact=1.0
            ))
            improvements.append("Optimize title length to stay under 200 characters")
        else:
            score += 3
            strengths.append("Title length is optimized for Amazon")
        
        # Check for emotional hooks
        emotional_hook_score = self._check_emotional_hooks(title)
        if emotional_hook_score >= 2:
            score += 5
            strengths.append("Strong emotional hook that captures attention")
        elif emotional_hook_score >= 1:
            score += 3
            feedback_parts.append("Good emotional elements present")
        else:
            issues.append(ValidationIssue(
                type=IssueType.MAJOR,
                section="Title",
                message="Title lacks emotional engagement",
                suggestion="Start with transformation language or urgent problem-solving words",
                example="Never Struggle Again: Professional-Grade Translation Device",
                score_impact=4.0
            ))
            improvements.append("Add emotional transformation language at the beginning")
        
        # Check for urgency/transformation words
        urgency_words_found = self._count_words_in_text(title.lower(), self.urgency_words)
        transformation_words = ['finally', 'never again', 'breakthrough', 'game-changer', 'instantly']
        transformation_found = self._count_words_in_text(title.lower(), transformation_words)
        
        if urgency_words_found > 0 or transformation_found > 0:
            score += 4
            strengths.append("Includes urgency or transformation language")
        else:
            improvements.append("Add urgency or transformation words like 'Finally' or 'Never Again'")
        
        # Check for benefit-focused vs feature-focused
        benefit_words = ['experience', 'feel', 'enjoy', 'discover', 'achieve', 'get', 'become']
        feature_words = ['with', 'includes', 'has', 'features', 'contains']
        
        benefit_count = self._count_words_in_text(title.lower(), benefit_words)
        feature_count = self._count_words_in_text(title.lower(), feature_words)
        
        if benefit_count > feature_count:
            score += 3
            strengths.append("Focuses on benefits over features")
        else:
            improvements.append("Focus more on customer benefits than product features")
        
        # Check for robotic/corporate language
        robotic_count = self._count_phrases_in_text(title.lower(), self.robotic_phrases)
        if robotic_count > 0:
            issues.append(ValidationIssue(
                type=IssueType.MAJOR,
                section="Title",
                message="Contains robotic corporate language",
                suggestion="Replace corporate jargon with emotional, conversational language",
                example="Replace 'cutting-edge technology' with 'breakthrough that finally works'",
                score_impact=3.0
            ))
            improvements.append("Remove corporate jargon and use conversational language")
        else:
            score += 2
            strengths.append("Avoids robotic corporate language")
        
        # Check for specific keyword integration
        if self._has_natural_keyword_integration(title):
            score += 3
            strengths.append("Keywords are naturally integrated")
        else:
            improvements.append("Integrate keywords more naturally into emotional hooks")
        
        feedback = self._compile_feedback(feedback_parts, score, max_score)
        
        return SectionScore(
            section="Title",
            score=min(score, max_score),
            max_score=max_score,
            feedback=feedback,
            improvements=improvements,
            strengths=strengths
        )

    def _validate_bullets(self, bullet_points: str, issues: List[ValidationIssue]) -> SectionScore:
        """Validates bullet points for emotional benefits and conversion focus."""
        score = 0
        max_score = 25
        feedback_parts = []
        improvements = []
        strengths = []
        
        if not bullet_points or len(bullet_points.strip()) == 0:
            issues.append(ValidationIssue(
                type=IssueType.CRITICAL,
                section="Bullets",
                message="Bullet points are missing",
                suggestion="Create 5 benefit-focused bullets with emotional outcomes",
                example="INSTANT CONFIDENCE: Feel like a local anywhere with real-time translation",
                score_impact=15.0
            ))
            return SectionScore("Bullets", 0, max_score, "Bullets are missing", improvements, strengths)
        
        # Split bullets and analyze each
        bullets = [bullet.strip() for bullet in bullet_points.split('\n') if bullet.strip()]
        
        if len(bullets) < 3:
            issues.append(ValidationIssue(
                type=IssueType.MAJOR,
                section="Bullets",
                message=f"Only {len(bullets)} bullets found - need at least 5 for maximum impact",
                suggestion="Create 5 comprehensive bullets covering different benefits",
                score_impact=5.0
            ))
            improvements.append("Add more bullet points (aim for 5 comprehensive bullets)")
        elif len(bullets) >= 5:
            score += 3
            strengths.append("Good number of bullet points for comprehensive coverage")
        
        # Check bullet format and structure
        proper_format_count = 0
        emotional_label_count = 0
        social_proof_count = 0
        
        for i, bullet in enumerate(bullets):
            bullet_score = 0
            
            # Check for proper format: "LABEL: content"
            if ':' in bullet and bullet.split(':')[0].isupper():
                proper_format_count += 1
                bullet_score += 1
                
                # Check for emotional labels
                label = bullet.split(':')[0].strip()
                emotional_labels = ['INSTANT CONFIDENCE', 'NEVER STRUGGLE', 'BREAKTHROUGH RESULTS', 
                                  'LIFE-CHANGING', 'GAME-CHANGER', 'FINALLY', 'TRANSFORM YOUR']
                if any(em_label in label for em_label in emotional_labels):
                    emotional_label_count += 1
                    bullet_score += 2
            else:
                improvements.append(f"Bullet {i+1}: Use format 'EMOTIONAL LABEL: benefit explanation'")
            
            # Check for social proof elements
            if any(proof in bullet.lower() for proof in self.social_proof_indicators):
                social_proof_count += 1
                bullet_score += 1
            
            # Check for emotional outcomes vs features
            emotional_outcomes = ['feel', 'experience', 'enjoy', 'achieve', 'become', 'discover', 'transform']
            if any(outcome in bullet.lower() for outcome in emotional_outcomes):
                bullet_score += 1
            
            # Check for specific details and metrics
            if re.search(r'\d+', bullet) or any(word in bullet.lower() for word in ['proven', 'tested', 'verified']):
                bullet_score += 1
            
            score += min(bullet_score, 3)  # Max 3 points per bullet
        
        # Overall bullet analysis
        if proper_format_count >= len(bullets) * 0.8:
            strengths.append("Bullets follow proper LABEL: format structure")
        else:
            improvements.append("Use consistent 'EMOTIONAL LABEL: content' format for all bullets")
        
        if emotional_label_count >= 3:
            score += 4
            strengths.append("Strong emotional labels that create desire")
        else:
            improvements.append("Use more emotional transformation labels like 'INSTANT CONFIDENCE' or 'NEVER STRUGGLE AGAIN'")
        
        if social_proof_count >= 2:
            score += 3
            strengths.append("Includes social proof elements")
        else:
            improvements.append("Add social proof elements (customer numbers, testimonials)")
        
        # Check for feature-dumping vs benefit storytelling
        feature_indicators = ['includes', 'has', 'features', 'comes with', 'contains']
        benefit_indicators = ['helps you', 'allows you to', 'means you can', 'so you', 'experience']
        
        feature_heavy = sum(1 for bullet in bullets if any(feat in bullet.lower() for feat in feature_indicators))
        benefit_heavy = sum(1 for bullet in bullets if any(ben in bullet.lower() for ben in benefit_indicators))
        
        if benefit_heavy > feature_heavy:
            score += 4
            strengths.append("Focuses on customer benefits over product features")
        else:
            issues.append(ValidationIssue(
                type=IssueType.MAJOR,
                section="Bullets",
                message="Bullets are too feature-focused instead of benefit-focused",
                suggestion="Rewrite bullets to focus on customer outcomes and emotional benefits",
                example="Instead of 'Features real-time translation' use 'INSTANT CONFIDENCE: Feel like a local anywhere in the world'",
                score_impact=4.0
            ))
            improvements.append("Transform feature descriptions into emotional benefit stories")
        
        feedback = self._compile_feedback(feedback_parts, score, max_score)
        
        return SectionScore(
            section="Bullets",
            score=min(score, max_score),
            max_score=max_score,
            feedback=feedback,
            improvements=improvements,
            strengths=strengths
        )

    def _validate_description(self, description: str, issues: List[ValidationIssue]) -> SectionScore:
        """Validates product description for Problem-Agitation-Solution structure."""
        score = 0
        max_score = 25
        feedback_parts = []
        improvements = []
        strengths = []
        
        if not description or len(description.strip()) == 0:
            issues.append(ValidationIssue(
                type=IssueType.CRITICAL,
                section="Description",
                message="Product description is missing",
                suggestion="Create compelling description with Problem-Agitation-Solution structure",
                example="Tired of awkward language barriers? You're not alone. That's why we created...",
                score_impact=15.0
            ))
            return SectionScore("Description", 0, max_score, "Description is missing", improvements, strengths)
        
        # Check length (should be substantial for Amazon)
        if len(description) < 500:
            improvements.append("Expand description to at least 500 characters for better engagement")
        elif len(description) > 2000:
            score += 2
            strengths.append("Comprehensive description length")
        
        # Check for Problem-Agitation-Solution structure
        problem_indicators = ['tired of', 'frustrated with', 'struggle with', 'ever wondered', 'hate when']
        agitation_indicators = ['you\'re not alone', 'millions struggle', 'studies show', 'research reveals']
        solution_indicators = ['that\'s why we created', 'introducing', 'now you can', 'finally']
        
        has_problem = any(indicator in description.lower() for indicator in problem_indicators)
        has_agitation = any(indicator in description.lower() for indicator in agitation_indicators)
        has_solution = any(indicator in description.lower() for indicator in solution_indicators)
        
        if has_problem and has_solution:
            score += 6
            if has_agitation:
                score += 2
                strengths.append("Perfect Problem-Agitation-Solution structure")
            else:
                strengths.append("Good Problem-Solution structure")
                improvements.append("Add agitation section to intensify the problem before presenting solution")
        else:
            issues.append(ValidationIssue(
                type=IssueType.MAJOR,
                section="Description",
                message="Missing Problem-Agitation-Solution structure",
                suggestion="Start with customer pain point, agitate the problem, then present your product as the solution",
                example="'Tired of language barriers? You're not alone - 73% of travelers avoid conversations. That's exactly why we created...'",
                score_impact=6.0
            ))
            improvements.append("Restructure using Problem-Agitation-Solution framework")
        
        # Check for social proof integration
        social_proof_score = 0
        if any(proof in description.lower() for proof in self.social_proof_indicators):
            social_proof_score += 2
            if re.search(r'\d+[,%]?\s*(customers|users|people)', description.lower()):
                social_proof_score += 2
                strengths.append("Includes specific social proof with numbers")
            else:
                strengths.append("Includes social proof elements")
        else:
            improvements.append("Add social proof with specific customer numbers or testimonials")
        score += social_proof_score
        
        # Check for strong Call-to-Action
        cta_indicators = ['order now', 'buy today', 'add to cart', 'join thousands', 'experience the difference', 'ready to']
        if any(cta in description.lower() for cta in cta_indicators):
            score += 3
            strengths.append("Includes compelling call-to-action")
        else:
            improvements.append("Add strong call-to-action with emotional appeal")
        
        # Check for urgency/scarcity
        urgency_count = self._count_words_in_text(description.lower(), self.urgency_words)
        if urgency_count > 0:
            score += 2
            strengths.append("Creates urgency to drive action")
        else:
            improvements.append("Add urgency elements like 'limited time' or 'before they sell out'")
        
        # Check for transformation language
        transformation_words = ['transform', 'change your life', 'never be the same', 'revolutionize', 'breakthrough']
        if any(word in description.lower() for word in transformation_words):
            score += 3
            strengths.append("Uses powerful transformation language")
        else:
            improvements.append("Include transformation language to paint picture of customer's improved life")
        
        # Check for robotic language
        robotic_count = self._count_phrases_in_text(description.lower(), self.robotic_phrases)
        corporate_count = self._count_phrases_in_text(description.lower(), self.generic_corporate_language)
        
        if robotic_count > 0 or corporate_count > 0:
            issues.append(ValidationIssue(
                type=IssueType.MAJOR,
                section="Description",
                message="Contains robotic or corporate language",
                suggestion="Replace with conversational, emotional language that speaks to customers directly",
                example="Replace 'innovative solution' with 'game-changing breakthrough'",
                score_impact=3.0
            ))
            improvements.append("Remove corporate jargon and write like you're talking to a friend")
        else:
            score += 3
            strengths.append("Uses natural, conversational language")
        
        feedback = self._compile_feedback(feedback_parts, score, max_score)
        
        return SectionScore(
            section="Description",
            score=min(score, max_score),
            max_score=max_score,
            feedback=feedback,
            improvements=improvements,
            strengths=strengths
        )

    def _validate_faqs(self, faqs: str, issues: List[ValidationIssue]) -> SectionScore:
        """Validates FAQs for natural conversation and trust building."""
        score = 0
        max_score = 15
        feedback_parts = []
        improvements = []
        strengths = []
        
        if not faqs or len(faqs.strip()) == 0:
            issues.append(ValidationIssue(
                type=IssueType.MAJOR,
                section="FAQs",
                message="FAQs are missing - major trust-building opportunity lost",
                suggestion="Create 3-5 FAQs that address real customer concerns in conversational tone",
                example="Q: Will this work for someone terrible with technology? A: That's exactly who we designed this for!",
                score_impact=8.0
            ))
            return SectionScore("FAQs", 0, max_score, "FAQs are missing", improvements, strengths)
        
        # Parse FAQ entries
        faq_entries = []
        for line in faqs.split('\n'):
            line = line.strip()
            if line and ('Q:' in line or 'A:' in line):
                faq_entries.append(line)
        
        # Group Q&A pairs
        qa_pairs = []
        current_q = ""
        for entry in faq_entries:
            if entry.startswith('Q:'):
                current_q = entry[2:].strip()
            elif entry.startswith('A:') and current_q:
                qa_pairs.append((current_q, entry[2:].strip()))
                current_q = ""
        
        if len(qa_pairs) < 3:
            improvements.append("Add more FAQ pairs (aim for 3-5 comprehensive Q&As)")
        elif len(qa_pairs) >= 3:
            score += 3
            strengths.append("Good number of FAQ pairs")
        
        # Analyze each Q&A pair
        conversational_count = 0
        empathy_count = 0
        confidence_building_count = 0
        specific_answer_count = 0
        
        for question, answer in qa_pairs:
            # Check for conversational tone
            conversational_indicators = ['that\'s exactly', 'great question', 'absolutely', 'actually', 'honestly']
            if any(indicator in answer.lower() for indicator in conversational_indicators):
                conversational_count += 1
            
            # Check for empathy and understanding
            empathy_indicators = ['i understand', 'we get it', 'you\'re right', 'that makes sense', 'totally get']
            if any(indicator in answer.lower() for indicator in empathy_indicators):
                empathy_count += 1
            
            # Check for confidence building
            confidence_indicators = ['guaranteed', 'proven', 'tested', 'works every time', 'you\'ll love']
            if any(indicator in answer.lower() for indicator in confidence_indicators):
                confidence_building_count += 1
            
            # Check for specific, detailed answers
            if len(answer) > 50 and (re.search(r'\d+', answer) or 'example' in answer.lower()):
                specific_answer_count += 1
        
        # Score conversational tone
        if conversational_count >= len(qa_pairs) * 0.7:
            score += 4
            strengths.append("FAQs use natural, conversational tone")
        else:
            improvements.append("Make FAQ answers more conversational with phrases like 'That's exactly' or 'Great question'")
        
        # Score empathy and understanding
        if empathy_count > 0:
            score += 2
            strengths.append("Shows empathy and understanding of customer concerns")
        else:
            improvements.append("Add empathy to answers - acknowledge customer feelings and concerns")
        
        # Score confidence building
        if confidence_building_count >= 2:
            score += 3
            strengths.append("Builds confidence and reduces purchase anxiety")
        else:
            improvements.append("Add confidence-building elements like guarantees or proof points")
        
        # Score specificity
        if specific_answer_count >= len(qa_pairs) * 0.5:
            score += 3
            strengths.append("Provides specific, detailed answers")
        else:
            improvements.append("Make answers more specific with examples, numbers, or detailed explanations")
        
        # Check for addressing real concerns vs generic questions
        real_concern_indicators = ['will this work for me', 'what if', 'how do i know', 'is this worth', 'compared to']
        real_concerns = sum(1 for q, a in qa_pairs if any(concern in q.lower() for concern in real_concern_indicators))
        
        if real_concerns >= len(qa_pairs) * 0.6:
            score += 2
            strengths.append("Addresses real customer concerns and objections")
        else:
            improvements.append("Focus on real customer concerns rather than generic product questions")
        
        feedback = self._compile_feedback(feedback_parts, score, max_score)
        
        return SectionScore(
            section="FAQs",
            score=min(score, max_score),
            max_score=max_score,
            feedback=feedback,
            improvements=improvements,
            strengths=strengths
        )

    def _calculate_emotion_score(self, listing_data: Dict[str, Any]) -> float:
        """Calculate overall emotional engagement score (0-10)."""
        all_text = ' '.join([
            listing_data.get('title', ''),
            listing_data.get('bullet_points', ''),
            listing_data.get('long_description', ''),
            listing_data.get('faqs', '')
        ]).lower()
        
        # Count emotional power words
        high_emotion_count = self._count_words_in_text(all_text, self.emotional_power_words['high'])
        medium_emotion_count = self._count_words_in_text(all_text, self.emotional_power_words['medium'])
        
        # Weight high-emotion words more heavily
        emotion_score = min((high_emotion_count * 2 + medium_emotion_count) * 0.5, 10)
        
        return round(emotion_score, 1)

    def _calculate_conversion_score(self, listing_data: Dict[str, Any]) -> float:
        """Calculate conversion optimization score (0-10)."""
        conversion_elements = 0
        max_elements = 8
        
        all_text = ' '.join([
            listing_data.get('title', ''),
            listing_data.get('bullet_points', ''),
            listing_data.get('long_description', ''),
            listing_data.get('faqs', '')
        ]).lower()
        
        # Check for urgency
        if any(word in all_text for word in self.urgency_words):
            conversion_elements += 1
        
        # Check for social proof
        if any(word in all_text for word in self.social_proof_indicators):
            conversion_elements += 1
        
        # Check for specific numbers/metrics
        if re.search(r'\d+[,%]?\s*(customers|users|people|stars|rating)', all_text):
            conversion_elements += 1
        
        # Check for guarantee/risk reversal
        if any(word in all_text for word in self.trust_builders):
            conversion_elements += 1
        
        # Check for problem-solution structure
        problem_words = ['tired of', 'frustrated', 'struggle', 'problem']
        solution_words = ['solution', 'answer', 'fix', 'solve']
        if any(word in all_text for word in problem_words) and any(word in all_text for word in solution_words):
            conversion_elements += 1
        
        # Check for transformation language
        transformation_words = ['transform', 'change your life', 'never be the same', 'breakthrough']
        if any(word in all_text for word in transformation_words):
            conversion_elements += 1
        
        # Check for call-to-action
        cta_words = ['order now', 'buy today', 'get yours', 'experience', 'discover']
        if any(word in all_text for word in cta_words):
            conversion_elements += 1
        
        # Check for benefit focus
        benefit_words = ['you get', 'you\'ll feel', 'experience', 'enjoy', 'achieve']
        if any(word in all_text for word in benefit_words):
            conversion_elements += 1
        
        conversion_score = (conversion_elements / max_elements) * 10
        return round(conversion_score, 1)

    def _calculate_trust_score(self, listing_data: Dict[str, Any]) -> float:
        """Calculate trust and credibility score (0-10)."""
        trust_elements = 0
        max_elements = 6
        
        all_text = ' '.join([
            listing_data.get('title', ''),
            listing_data.get('bullet_points', ''),
            listing_data.get('long_description', ''),
            listing_data.get('faqs', '')
        ]).lower()
        
        # Check for trust builders
        if any(word in all_text for word in self.trust_builders):
            trust_elements += 1
        
        # Check for specific social proof numbers
        if re.search(r'\d+[,%]?\s*(customers|reviews|stars)', all_text):
            trust_elements += 1
        
        # Check for certifications/testing
        cert_words = ['certified', 'tested', 'approved', 'verified']
        if any(word in all_text for word in cert_words):
            trust_elements += 1
        
        # Check for warranty/guarantee
        guarantee_words = ['warranty', 'guarantee', 'money-back', 'risk-free']
        if any(word in all_text for word in guarantee_words):
            trust_elements += 1
        
        # Check for brand credibility indicators
        brand_words = ['trusted by', 'recommended by', 'used by professionals']
        if any(word in all_text for word in brand_words):
            trust_elements += 1
        
        # Check for transparency (detailed FAQs, specifications)
        faqs = listing_data.get('faqs', '')
        if faqs and len(faqs.split('Q:')) >= 3:
            trust_elements += 1
        
        trust_score = (trust_elements / max_elements) * 10
        return round(trust_score, 1)

    def _check_emotional_hooks(self, text: str) -> int:
        """Check for emotional hooks in text. Returns 0-3 score."""
        text_lower = text.lower()
        score = 0
        
        # High-impact transformation words
        transformation_hooks = ['finally', 'never again', 'breakthrough', 'game-changer', 'instantly']
        if any(hook in text_lower for hook in transformation_hooks):
            score += 2
        
        # Urgency/desire words
        urgency_hooks = ['obsessed', 'secret', 'unleash', 'transform', 'dominate']
        if any(hook in text_lower for hook in urgency_hooks):
            score += 1
        
        # Emotional outcomes
        outcome_hooks = ['feel confident', 'experience freedom', 'enjoy peace', 'achieve success']
        if any(hook in text_lower for hook in outcome_hooks):
            score += 1
        
        return min(score, 3)

    def _count_words_in_text(self, text: str, word_list: List[str]) -> int:
        """Count occurrences of words from word_list in text."""
        return sum(1 for word in word_list if word in text)

    def _count_phrases_in_text(self, text: str, phrase_list: List[str]) -> int:
        """Count occurrences of phrases from phrase_list in text."""
        return sum(1 for phrase in phrase_list if phrase in text)

    def _has_natural_keyword_integration(self, text: str) -> bool:
        """Check if keywords are naturally integrated vs stuffed."""
        # Simple heuristic: check for repeated phrases that might indicate keyword stuffing
        words = text.lower().split()
        word_counts = {}
        for word in words:
            if len(word) > 3:  # Only check meaningful words
                word_counts[word] = word_counts.get(word, 0) + 1
        
        # If any word appears more than 3 times in a title, it might be stuffed
        max_count = max(word_counts.values()) if word_counts else 0
        return max_count <= 3

    def _compile_feedback(self, feedback_parts: List[str], score: float, max_score: float) -> str:
        """Compile feedback parts into a coherent feedback message."""
        if score == max_score:
            return "Perfect! This section hits all the marks for emotional engagement and conversion."
        elif score >= max_score * 0.8:
            return "Strong performance with room for minor improvements."
        elif score >= max_score * 0.6:
            return "Good foundation but needs enhancement for maximum impact."
        else:
            return "Significant improvements needed to reach conversion-focused quality."

    def _generate_summary(self, overall_score: float, emotion_score: float, 
                         conversion_score: float, trust_score: float) -> str:
        """Generate an overall summary of the listing quality."""
        if overall_score >= 9.0:
            return f"Exceptional listing quality! Your content is emotionally engaging (emotion: {emotion_score}/10), conversion-optimized (conversion: {conversion_score}/10), and trust-building (trust: {trust_score}/10). This listing should convert browsers into buyers effectively."
        elif overall_score >= 7.0:
            return f"Strong listing with good emotional appeal (emotion: {emotion_score}/10) and conversion elements (conversion: {conversion_score}/10). Focus on the improvement suggestions to reach 10/10 quality."
        elif overall_score >= 5.0:
            return f"Decent foundation but significant improvements needed. Current emotion score: {emotion_score}/10, conversion score: {conversion_score}/10, trust score: {trust_score}/10. Address the major issues identified."
        else:
            return f"This listing needs major improvements to be effective. Low scores across emotion ({emotion_score}/10), conversion ({conversion_score}/10), and trust ({trust_score}/10) indicate fundamental issues that must be addressed."

    def _generate_action_items(self, issues: List[ValidationIssue], 
                              section_scores: List[SectionScore]) -> List[str]:
        """Generate prioritized action items based on issues and scores."""
        action_items = []
        
        # Add critical issues first
        critical_issues = [issue for issue in issues if issue.type == IssueType.CRITICAL]
        for issue in critical_issues:
            action_items.append(f"CRITICAL: {issue.message} - {issue.suggestion}")
        
        # Add major issues
        major_issues = [issue for issue in issues if issue.type == IssueType.MAJOR]
        for issue in major_issues[:3]:  # Limit to top 3 major issues
            action_items.append(f"MAJOR: {issue.message} - {issue.suggestion}")
        
        # Add section-specific improvements for lowest scoring sections
        section_scores.sort(key=lambda x: x.score / x.max_score)
        for section in section_scores[:2]:  # Focus on 2 lowest scoring sections
            if section.improvements:
                action_items.append(f"{section.section.upper()}: {section.improvements[0]}")
        
        return action_items[:8]  # Limit to 8 action items to avoid overwhelm

    def get_validation_json(self, listing_data: Dict[str, Any]) -> Dict[str, Any]:
        """Return validation results as JSON for API responses."""
        report = self.validate_listing(listing_data)
        
        return {
            "overall_score": report.overall_score,
            "max_score": report.max_score,
            "grade": self._get_letter_grade(report.overall_score),
            "emotion_score": report.emotion_score,
            "conversion_score": report.conversion_score,
            "trust_score": report.trust_score,
            "summary": report.summary,
            "section_scores": [
                {
                    "section": section.section,
                    "score": section.score,
                    "max_score": section.max_score,
                    "percentage": round((section.score / section.max_score) * 100, 1),
                    "feedback": section.feedback,
                    "strengths": section.strengths,
                    "improvements": section.improvements
                }
                for section in report.section_scores
            ],
            "issues": [
                {
                    "type": issue.type.value,
                    "section": issue.section,
                    "message": issue.message,
                    "suggestion": issue.suggestion,
                    "example": issue.example,
                    "score_impact": issue.score_impact
                }
                for issue in report.issues
            ],
            "action_items": report.action_items
        }

    def _get_letter_grade(self, score: float) -> str:
        """Convert numeric score to letter grade."""
        if score >= 9.5:
            return "A+"
        elif score >= 9.0:
            return "A"
        elif score >= 8.0:
            return "B+"
        elif score >= 7.0:
            return "B"
        elif score >= 6.0:
            return "C+"
        elif score >= 5.0:
            return "C"
        elif score >= 4.0:
            return "D"
        else:
            return "F"