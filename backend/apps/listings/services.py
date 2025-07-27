import json
import time
import re
import logging
from django.conf import settings
from .models import GeneratedListing, KeywordResearch
from apps.core.models import Product


class ListingGeneratorService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.logger.info("Checking OpenAI configuration...")
            self.logger.info(f"API Key exists: {bool(settings.OPENAI_API_KEY)}")
            
            # Check if OpenAI key is set and valid
            if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-openai-api-key-here":
                self.logger.warning("OpenAI API key not properly configured!")
                self.logger.warning("Please set your real OpenAI API key in the .env file")
                self.client = None
            elif not settings.OPENAI_API_KEY.startswith('sk-'):
                self.logger.warning("Invalid OpenAI API key format!")
                self.logger.warning("OpenAI keys should start with 'sk-'")
                self.client = None
            else:
                # Use new OpenAI client
                from openai import OpenAI
                self.logger.info(f"Creating OpenAI client with key starting: {settings.OPENAI_API_KEY[:10]}...")
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                self.logger.info("OpenAI client initialized successfully - AI generation enabled!")
        except Exception as e:
            self.logger.error(f"Error initializing OpenAI client: {e}")
            import traceback
            self.logger.error(f"Traceback: {traceback.format_exc()}")
            self.client = None

    def generate_listing(self, product_id, platform):
        try:
            product = Product.objects.get(id=product_id)
            listing = GeneratedListing.objects.create(
                product=product,
                platform=platform,
                status='processing'
            )
            
            if platform == 'amazon':
                self._generate_amazon_listing(product, listing)
            elif platform == 'walmart':
                self._generate_walmart_listing(product, listing)
            elif platform == 'etsy':
                self._generate_etsy_listing(product, listing)
            elif platform == 'tiktok':
                self._generate_tiktok_listing(product, listing)
            elif platform == 'shopify':
                self._generate_shopify_listing(product, listing)
            else:
                raise Exception(f"Unsupported platform: {platform}")
            
            listing.status = 'completed'
            listing.save()
            
            # Note: Image generation is now triggered separately from frontend
            # This allows the listing to be shown immediately
            
            return listing
            
        except Exception as e:
            if 'listing' in locals():
                listing.status = 'failed'
                listing.save()
            raise e

    def _generate_amazon_listing(self, product, listing):
        import json
        import re
        self.logger.info(f"GENERATING AMAZON LISTING FOR {product.name}")
        self.logger.info(f"OpenAI client status: {'AVAILABLE' if self.client else 'NOT AVAILABLE'}")
        
        if not self.client:
            self.logger.error("OpenAI client is None - using fallback content")
            self.logger.error(f"API Key exists: {bool(settings.OPENAI_API_KEY)}")
            if settings.OPENAI_API_KEY:
                self.logger.error(f"API Key starts with 'sk-': {settings.OPENAI_API_KEY.startswith('sk-') if settings.OPENAI_API_KEY else False}")
            raise Exception("OpenAI API key not configured. Please set your OPENAI_API_KEY in the .env file to generate AI content.")
            
        competitor_context = self._get_competitor_context(product)
        
        # Generate product-specific keywords and context
        product_context = self._analyze_product_context(product)
        
        # Use actual product brand tone
        brand_tone_mapping = {
            'professional': {
                'tone': 'Professional & Authoritative',
                'guidelines': 'Direct, credible, expertise-focused. Personality: Trusted advisor who builds confidence. Use phrases like "Industry-leading", "Proven results", "Professional grade". Focus on reliability and expertise.'
            },
            'casual': {
                'tone': 'Friendly & Approachable',
                'guidelines': 'Conversational, warm, relatable. Personality: Helpful friend who makes things easy. Use phrases like "Just what you need", "Makes life easier", "You\'ll love this". Focus on comfort and simplicity.'
            },
            'luxury': {
                'tone': 'Elegant & Premium',
                'guidelines': 'Sophisticated, aspirational, transformational. Personality: Elevated and inspiring. Use phrases like "Elevate your", "Transform into", "Luxurious experience". Include sensory language and confidence-building.'
            },
            'playful': {
                'tone': 'Playful & Innovative',
                'guidelines': 'Fun, confident, slightly cheeky. Personality: Tech-savvy friend who makes complex simple. Use phrases like "Talk like a local", "Say it like you mean it", "Ready to [outcome]". Balance innovation with accessibility.'
            },
            'minimal': {
                'tone': 'Clean & Minimal',
                'guidelines': 'Clear, concise, purposeful. Personality: Thoughtful minimalist who values quality. Use phrases like "Simply better", "Pure performance", "Essential quality". Focus on clarity and purpose.'
            },
            'bold': {
                'tone': 'Bold & Confident',
                'guidelines': 'Strong, decisive, powerful. Personality: Leader who inspires action. Use phrases like "Dominate your", "Unleash your", "Power through". Focus on strength and transformation.'
            }
        }
        category_tone = brand_tone_mapping.get(product.brand_tone, brand_tone_mapping['professional'])
        template_style = {
            'name': 'Story-First Template',
            'brand_placement': 'Integrated naturally in middle of title',
            'title_format': '[Transformation/Outcome] – [Brand] [Product] for [Specific Use Case]',
            'description_approach': 'Start with customer story/problem, introduce solution, list benefits with social proof',
            'structure': 'Problem narrative → Solution introduction → Key benefits → Trust elements → Clear CTA'
        }
        
        # Generate dynamic, brand-specific prompt based on tone
        tone_style = product.brand_tone.lower()
        
        # Create completely different writing approaches for each brand tone
        tone_specific_prompts = {
            'professional': f"""
You are writing for {product.brand_name} using a PROFESSIONAL tone. Write like an industry expert consultant who builds credibility through expertise and proven results.

BRAND PERSONALITY: Authoritative advisor who leads with facts, certifications, and proven track record. Think "Harvard Business Review meets technical excellence."

TITLE APPROACH: Lead with industry authority and measurable outcomes
- Patterns: "Industry-Leading [Product]", "Professional-Grade [Product] Used by [Professionals]", "Certified [Product] with Proven [Benefit]"
- Keywords: Professional, Certified, Industry-Standard, Proven, Validated, Trusted by Professionals

BULLET STYLE: Technical specifications with business impact
- Format: "PROVEN PERFORMANCE: [Specific metric] delivers [business outcome] as validated by [authority/study]"
- Focus: ROI, efficiency gains, professional standards, certifications
- Language: Precise, data-driven, outcome-focused

DESCRIPTION STYLE: Case study approach
- Structure: Challenge → Solution → Results → Validation
- Include: Performance metrics, industry standards, professional testimonials
- Tone: Confident expertise without being arrogant
""",
            
            'casual': f"""
You are writing for {product.brand_name} using a CASUAL tone. Write like a helpful friend sharing an amazing discovery - warm, relatable, and genuinely excited to help.

BRAND PERSONALITY: That friend who always finds the best stuff and loves sharing discoveries. Think "your most helpful friend who makes everything simple."

TITLE APPROACH: Friendly recommendations and relatable benefits
- Patterns: "This [Product] Makes [Daily Task] So Much Easier", "The [Product] Everyone's Talking About", "Simple [Product] That Just Works"
- Keywords: Easy, Simple, Perfect for, Just Works, Love This, Game-Changer

BULLET STYLE: Conversational benefits with relatable scenarios
- Format: "MAKES LIFE EASIER: [Relatable situation] becomes [simple outcome] - just like [familiar comparison]"
- Focus: Daily convenience, stress reduction, time-saving
- Language: Conversational, reassuring, down-to-earth

DESCRIPTION STYLE: Friend-to-friend recommendation
- Structure: Personal connection → shared frustration → discovery → how it helps → encouragement
- Include: Relatable stories, simple explanations, reassuring tone
- Tone: Warm, helpful, like texting a friend
""",
            
            'luxury': f"""
You are writing for {product.brand_name} using a LUXURY tone. Write like a curator of exceptional experiences who understands discerning taste and elevated lifestyle.

BRAND PERSONALITY: Sophisticated connoisseur who appreciates craftsmanship and exclusivity. Think "private concierge meets museum curator."

TITLE APPROACH: Elevated language emphasizing exclusivity and refinement
- Patterns: "Exquisite [Product] for the Discerning [User]", "Handcrafted [Product] Collection", "Premium [Product] Experience"
- Keywords: Exquisite, Handcrafted, Curated, Exclusive, Premium, Artisan, Heritage

BULLET STYLE: Craftsmanship and elevated experience
- Format: "EXCEPTIONAL CRAFTSMANSHIP: [Artisan detail] creates [elevated experience] worthy of [prestigious comparison]"
- Focus: Materials, craftsmanship, exclusivity, elevated experience
- Language: Sophisticated, appreciative of quality, sensory-rich

DESCRIPTION STYLE: Connoisseur's appreciation
- Structure: Heritage → craftsmanship → experience → exclusivity → invitation
- Include: Artisan details, premium materials, elevated experiences
- Tone: Sophisticated appreciation without pretension
""",
            
            'playful': f"""
You are writing for {product.brand_name} using a PLAYFUL tone. Write with energy, creativity, and fun - like a cool friend who makes everything more interesting.

BRAND PERSONALITY: Creative innovator who brings joy and excitement to everyday moments. Think "best friend who makes everything fun meets creative genius."

TITLE APPROACH: Fun, energetic language with creative twists
- Patterns: "The [Product] That's Changing Everything", "Seriously Cool [Product] for [Fun Outcome]", "[Product] That Makes [Activity] Actually Fun"
- Keywords: Seriously Cool, Amazing, Awesome, Game-Changer, Revolutionary, Mind-Blowing

BULLET STYLE: Energetic benefits with creative comparisons
- Format: "TOTALLY AWESOME: [Fun outcome] happens [creative way] - it's like [surprising comparison] but better"
- Focus: Excitement, creativity, unexpected benefits, fun factor
- Language: Energetic, creative, surprising, delightful

DESCRIPTION STYLE: Enthusiastic discovery
- Structure: Excitement → surprising benefit → creative explanation → community → fun invitation
- Include: Creative metaphors, surprising comparisons, community feeling
- Tone: Energetic enthusiasm that's infectious
""",
            
            'minimal': f"""
You are writing for {product.brand_name} using a MINIMAL tone. Write with clarity, purpose, and elegant simplicity - every word must earn its place.

BRAND PERSONALITY: Thoughtful designer who values essence over excess. Think "Steve Jobs meets zen master - profound simplicity."

TITLE APPROACH: Clear, essential benefits without unnecessary words
- Patterns: "Essential [Product] for [Pure Benefit]", "Simply Better [Product]", "[Product]. [Clear Benefit]. Done."
- Keywords: Essential, Pure, Simply, Clean, Clear, Focused, Refined

BULLET STYLE: Clean statements of clear value
- Format: "CLEAR BENEFIT: [Direct outcome] through [simple method] - nothing more, nothing less"
- Focus: Core functionality, clear benefits, purposeful design
- Language: Clean, direct, purposeful, uncluttered

DESCRIPTION STYLE: Essential clarity
- Structure: Purpose → function → benefit → simplicity
- Include: Core benefits only, clean explanations, purposeful details
- Tone: Calm confidence in essential value
""",
            
            'bold': f"""
You are writing for {product.brand_name} using a BOLD tone. Write with power, confidence, and transformative energy - make bold claims and back them up.

BRAND PERSONALITY: Powerful leader who inspires transformation and isn't afraid to challenge the status quo. Think "motivational speaker meets industry disruptor."

TITLE APPROACH: Strong, transformative language that commands attention
- Patterns: "Revolutionary [Product] That Destroys [Problem]", "The [Product] That Changes Everything", "Breakthrough [Product] for [Transformation]"
- Keywords: Revolutionary, Breakthrough, Destroys, Dominates, Unleashes, Transforms, Shatters

BULLET STYLE: Powerful transformation statements
- Format: "BREAKTHROUGH POWER: [Dramatic transformation] destroys [old problem] and unleashes [powerful outcome]"
- Focus: Dramatic change, power, breakthrough results, dominance
- Language: Strong, transformative, confident, commanding

DESCRIPTION STYLE: Manifesto approach
- Structure: Challenge status quo → breakthrough moment → transformation → power → dominance
- Include: Strong claims, dramatic benefits, transformative outcomes
- Tone: Confident authority with transformative energy
"""
        }
        
        # Get the tone-specific prompt
        base_prompt = tone_specific_prompts.get(tone_style, tone_specific_prompts['professional'])
        
        # Add variety through randomization techniques
        import random
        variety_elements = [
            "Avoid using these overused phrases in ANY section: 'Experience the difference', 'Take your [X] to the next level', 'Game-changing', 'Revolutionary', 'Unparalleled'",
            "Use unexpected analogies and comparisons that fit the brand tone",
            "Vary sentence length dramatically - mix very short punchy sentences with longer flowing ones",
            "Start with a completely different hook approach than typical Amazon listings",
            "Include specific numbers and metrics that feel authentic to this product category"
        ]
        random.shuffle(variety_elements)
        
        # Extract key product insights
        product_category = product.categories.split(',')[0].strip() if product.categories else "product"
        primary_keywords = [product.name.lower(), product_category.lower(), product.brand_name.lower()]
        
        # Analyze features to extract benefits
        feature_list = product.features.split(',') if product.features else []
        benefit_keywords = []
        for feature in feature_list[:3]:
            feature = feature.strip()
            if feature:
                benefit_keywords.append(feature.lower())
        
        # Analyze the product to create unique content strategy
        product_type = "unknown"
        if "fan" in product.name.lower() or "cooling" in product.description.lower():
            product_type = "cooling_device"
        elif "watch" in product.name.lower() or "timepiece" in product.description.lower():
            product_type = "luxury_watch"
        elif "earbuds" in product.name.lower() or "headphones" in product.name.lower():
            product_type = "audio_device"
        elif "blanket" in product.name.lower() or "weighted" in product.description.lower():
            product_type = "comfort_item"
        elif "chair" in product.name.lower() or "gaming" in product.description.lower():
            product_type = "furniture"
        
        # Extract unique features and benefits
        features_list = [f.strip() for f in product.features.split(',') if f.strip()] if product.features else []
        unique_features = features_list[:3]  # Focus on top 3 features
        
        # Determine customer pain points based on product type
        pain_point_map = {
            "cooling_device": ["overheating", "sweating", "discomfort in heat", "bulky fans", "noisy cooling"],
            "luxury_watch": ["ordinary timepieces", "lack of elegance", "poor craftsmanship", "status anxiety"],
            "audio_device": ["language barriers", "poor translation", "communication problems", "travel difficulties"],
            "comfort_item": ["poor sleep", "anxiety", "restlessness", "stress", "discomfort"],
            "furniture": ["back pain", "poor posture", "uncomfortable seating", "fatigue"],
            "unknown": ["daily frustrations", "inconvenience", "poor performance", "wasted time"]
        }
        pain_points = pain_point_map.get(product_type, ["daily problems"])
        
        # Create unique emotional hooks based on product analysis
        emotion_starters = ["Finally", "Breakthrough", "Never Again", "Transform Your", "Revolutionary", "Game-Changing"]
        import random
        chosen_starter = random.choice(emotion_starters)
        
        # Prepare data for the comprehensive prompt
        data = {
            'productTitle': product.name,
            'brandName': product.brand_name,
            'category': product.categories.split(',')[0].strip() if product.categories else product_type,
            'mainFeaturesBenefits': product.features or product.description,
            'productDescription': product.description,
            'brandTone': product.brand_tone,
            'competitorUrl': getattr(product, 'competitor_url', ''),
            'competitorASIN': getattr(product, 'competitor_asin', ''),
            'useCaseOccasion': getattr(product, 'use_case', ''),
            'materialSizeColor': getattr(product, 'material_size_color', ''),
            'targetBuyerPersona': getattr(product, 'target_persona', ''),
            'keywordsToTarget': ', '.join(pain_points) if pain_points else ''
        }

        prompt = f"""
            Generate a complete Amazon product listing JSON for: {data.get('productTitle')} by {data.get('brandName')}.

            Product Details:
            - Product: {data.get('productTitle')}
            - Brand: {data.get('brandName')} 
            - Category: {data.get('category')}
            - Features: {data.get('mainFeaturesBenefits')}
            - Description: {data.get('productDescription')}
            - Brand Tone: {data.get('brandTone')}

            Return ONLY a valid JSON object with this structure:

            {{
              "productTitle": "An SEO-optimized, Amazon-standard product title (max 200 characters). Start with brand name '{data.get('brandName')}', followed by high-volume keywords, product type, key features/benefits from '{data.get('mainFeaturesBenefits')}', material/size/color (if applicable). Prioritize concise phrasing and natural flow. Avoid redundant words. Consider including a 'Gift-Ready' or similar modifier if applicable.",
              "bulletPoints": [
                "**FEATURE 1:** Write actual compelling benefit for this product (max 200 chars)",
                "**FEATURE 2:** Write actual compelling benefit for this product (max 200 chars)",
                "**FEATURE 3:** Write actual compelling benefit for this product (max 200 chars)",
                "**FEATURE 4:** Write actual compelling benefit for this product (max 200 chars)",
                "**FEATURE 5:** Write actual compelling benefit for this product (max 200 chars)"
              ],
              "productDescription": "A detailed Product Description (max 2000 chars). Structure into 3 shorter, well-formatted paragraphs. The first paragraph must start with an emotional hook or question. The second should elaborate on features and benefits, naturally embedding relevant long-tail keyword phrases. Include a 'What's Included' line. The third should end with a strong, product-specific Call-to-Action (CTA). Use concise, scannable language. Mention giftability if applicable. EXAMPLE: 'Are you tired of cold lunches at work? The {data.get('brandName')} {data.get('productTitle')} transforms your dining experience with revolutionary heating technology that delivers restaurant-quality warmth in minutes. This compact powerhouse features advanced temperature control, leak-proof design, and dishwasher-safe components perfect for busy professionals. What's Included: heated lunch box, power cord, user manual, and recipe guide. Make every meal a moment to savor - order your {data.get('brandName')} today and taste the difference quality makes!'",
              "aPlusContentPlan": {{
                "hero_section": {{
                  "title": "Write compelling headline for this product",
                  "content": "Write 2-3 sentences about product benefits",
                  "image_requirements": "DETAILED IMAGE DESCRIPTION: Professional lifestyle photo showing real person actively using the product in its intended environment. SPECIFICATIONS: High-resolution (300+ DPI), well-lit natural lighting, clean background that complements but doesn't distract from the product. COMPOSITION: Rule of thirds placement, product should occupy 40-60% of frame. STYLING: Models should represent target demographic, genuine expressions of satisfaction/happiness. TECHNICAL: No watermarks, logos, or text overlays. Product branding should be clearly visible. COLOR PALETTE: Brand-consistent colors, avoid oversaturated filters."
                }},
                "features_section": {{
                  "title": "Key Features",
                  "content": "List 4-5 main features with benefits", 
                  "image_requirements": "DETAILED IMAGE DESCRIPTION: Clean product infographic with feature callouts and annotations. LAYOUT: Grid or circular layout showing 4-6 key features with icons and brief descriptions. DESIGN STYLE: Modern, minimalist design with plenty of white space. TYPOGRAPHY: Sans-serif fonts, hierarchical text sizing. VISUAL ELEMENTS: Use branded color scheme, consistent icon style (line art or filled), arrow callouts pointing to specific product areas. TECHNICAL SPECS: Vector-based graphics preferred, 1500x1500px minimum, Amazon-compliant (no promotional text like 'Best' or 'Sale')."
                }},
                "comparison_section": {{
                  "title": "Why Choose This Product",
                  "content": "Comparison vs competitors",
                  "image_requirements": "DETAILED IMAGE DESCRIPTION: Professional comparison chart or side-by-side product shots. COMPARISON FORMAT: Table or grid layout comparing 3-4 key differentiators. VISUAL HIERARCHY: Clear headers, consistent spacing, readable fonts (minimum 14pt). CONTENT FOCUS: Feature comparisons, not price comparisons. Use checkmarks, stars, or other visual indicators. COLOR CODING: Green for advantages, neutral colors for standard features. BACKGROUND: Clean white or light gray, ensure high contrast for text readability. SIZE: Optimized for mobile viewing while maintaining legibility."
                }},
                "usage_section": {{
                  "title": "How to Use",
                  "content": "Step-by-step usage instructions or scenarios",
                  "image_requirements": "DETAILED IMAGE DESCRIPTION: Step-by-step instructional images or usage scenarios. FORMAT: Sequential panels (2-4 steps) showing product setup/use process. CLARITY: Each step clearly numbered, actions easy to follow visually. PHOTOGRAPHY: Multiple angles if needed, hands-on demonstration shots. CONSISTENCY: Same lighting and background across all steps. TEXT OVERLAY: Minimal text, focus on visual storytelling. SAFETY: If applicable, show proper handling or safety measures. DEMOGRAPHIC: Models should match target customer base."
                }},
                "lifestyle_section": {{
                  "title": "Perfect For Your Lifestyle",
                  "content": "Show product fitting into customer's daily life",
                  "image_requirements": "DETAILED IMAGE DESCRIPTION: Multiple lifestyle scenarios showing product versatility. SCENES: 2-3 different environments where product would be used (home, office, travel, etc.). AUTHENTICITY: Real-life settings, not staged studio shots. DIVERSITY: Show different user types/ages if applicable. EMOTIONAL CONNECTION: Capture moments of satisfaction, convenience, or joy. PRODUCT PROMINENCE: Product visible but naturally integrated into scene. ASPIRATIONAL: Slightly elevated lifestyle while remaining relatable. LIGHTING: Natural lighting preferred, avoid harsh shadows or overexposure."
                }}
              }},
              "brandSummary": "Brief, emotional, and unique brand summary for '{data.get('brandName')}' (max 300 chars). Start with a compelling tagline. Focus on emotionally differentiating the brand and its core promise or solution. End with a customer-focused line encouraging joining the brand's community or highlighting brand values.",
              "backendKeywords": "A single space-separated string of hidden backend keywords (exactly 249 bytes max). Exclude terms already present in the product title, bullet points, primary keywords, or secondary keywords. Include problem-solving terms, gifting keywords, and semantic intent variations.",
              "topCompetitorKeywords": "Comma-separated 5-10 highly relevant and high-performing keywords extracted from competitor analysis (if competitor info provided).",
              "keywordStrategy": "Brief explanation of the overall keyword strategy (max 500 chars). Provide reasoning for keyword selection per section. Discuss keyword clustering logic: 'Top of Funnel = lifestyle terms', 'Mid-Funnel = comfort terms', 'Bottom of Funnel = technical terms', or 'Informational vs. Transactional keywords'.",
              "ppcStrategy": {{
                "exactMatch": {{
                  "keywords": ["List 3-5 exact match keywords for this product"],
                  "bidRange": "$0.75-1.25",
                  "targetAcos": "20%"
                }},
                "phraseMatch": {{
                  "keywords": ["List 3-5 phrase match keywords for this product"],
                  "bidRange": "$0.50-0.85", 
                  "targetAcos": "30%"
                }},
                "negativeKeywords": ["cheap", "free", "used", "broken"]
              }},
              "keyword_cluster": {{
                "primary_keywords": ["REQUIRED: Generate exactly 8 high-volume primary keywords", "Include brand + product name", "Include main product category", "Include 5 more relevant primary keywords"],
                "secondary_keywords": ["REQUIRED: Generate exactly 10 long-tail secondary keywords", "Include problem-solving phrases", "Include user intent keywords", "Include 7 more specific long-tail variations"],
                "backend_search_terms": "REQUIRED: Generate space-separated backend keywords (MUST be exactly 240-249 characters). Include synonyms, misspellings, alternate spellings, related terms, seasonal keywords, gift keywords, and demographic terms.",
                "ppc_keywords": [
                  {{"keyword": "main exact match keyword", "match_type": "Exact", "bid": "0.75"}},
                  {{"keyword": "secondary phrase match keyword", "match_type": "Phrase", "bid": "0.65"}},
                  {{"keyword": "broad match keyword", "match_type": "Broad", "bid": "0.45"}},
                  {{"keyword": "another exact match", "match_type": "Exact", "bid": "0.80"}},
                  {{"keyword": "another phrase match", "match_type": "Phrase", "bid": "0.60"}}
                ]
              }}
            }}

            User Input Details:
            Product Title: {data.get('productTitle')}
            Brand Name: {data.get('brandName')}
            Category: {data.get('category')}
            Main Features/Benefits: {data.get('mainFeaturesBenefits')}
            Product Description (from seller): {data.get('productDescription')}
            Brand Tone: {data.get('brandTone')}
            {f"Competitor URL: {data.get('competitorUrl')}" if data.get('competitorUrl') else ''}
            {f"Competitor ASIN: {data.get('competitorASIN')}" if data.get('competitorASIN') else ''}
            {f"Use Case/Occasion: {data.get('useCaseOccasion')}" if data.get('useCaseOccasion') else ''}
            {f"Material/Size/Color: {data.get('materialSizeColor')}" if data.get('materialSizeColor') else ''}
            {f"Target Buyer Persona: {data.get('targetBuyerPersona')}" if data.get('targetBuyerPersona') else ''}
            {f"Keywords to Target: {data.get('keywordsToTarget')}" if data.get('keywordsToTarget') else ''}

            CRITICAL REQUIREMENTS - MUST GENERATE ALL FIELDS:

            1. productDescription - REQUIRED: Write a compelling 3-paragraph description about {data.get('productTitle')}
            2. keyword_cluster - REQUIRED: Generate comprehensive keywords for {data.get('productTitle')}
               - primary_keywords: EXACTLY 8 keywords (must include brand+product, category, and 6 more)
               - secondary_keywords: EXACTLY 10 long-tail keywords (problem-solving + intent-based)
               - backend_search_terms: EXACTLY 240-249 characters of space-separated terms
               - ppc_keywords: EXACTLY 5 PPC keyword objects with different match types
            3. bulletPoints - REQUIRED: Write 5 bullet points with **BOLD** format
            4. All other fields must be completed with actual content
            
            KEYWORD GENERATION RULES:
            - NO generic examples - use actual product-specific keywords
            - Include synonyms, alternate spellings, and related terms
            - Backend keywords must be comprehensive and reach character limit

            EXAMPLE of what you MUST generate for productDescription:
            "Are you tired of [problem]? The {data.get('brandName')} {data.get('productTitle')} solves this with [specific solution]. 

            This premium product features [list actual features from input]. Perfect for [target users], it delivers [specific benefits]. Built with [quality materials] and designed for [use case].

            What's Included: [product], user manual, warranty. Order your {data.get('brandName')} {data.get('productTitle')} today and experience the difference!"

            EXAMPLE of what you MUST generate for keywords:
            {{"primary_keywords": ["{data.get('productTitle').lower()}", "premium {data.get('category').lower()}", "best {data.get('productTitle').lower()}"]}}

            OUTPUT ONLY THE JSON - NO OTHER TEXT:
            """        
        self.logger.info("OpenAI client is available - proceeding with AI generation")
        try:
            self.logger.info(f"Generating AI content for {product.name} on Amazon...")
            self.logger.info(f"Product details: Name={product.name}, Brand={product.brand_name}, Categories={product.categories}")
            self.logger.info(f"Using product context: {product_context[:200]}...")
            
            # Use OpenAI Function Calling to enforce JSON schema
            function_schema = {
                "name": "create_amazon_listing",
                "description": f"Create an Amazon listing for {product.name}",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string", "description": "SEO title under 200 chars"},
                        "bullet_points": {"type": "array", "items": {"type": "string"}, "description": "5 bullet points"},
                        "long_description": {"type": "string", "description": "Detailed description"},
                        "seo_keywords": {
                            "type": "object", 
                            "description": "Comprehensive keyword categories for SEO",
                            "properties": {
                                "primary": {"type": "array", "items": {"type": "string"}, "description": "5 primary short-tail keywords"},
                                "long_tail": {"type": "array", "items": {"type": "string"}, "description": "10 long-tail keyword phrases"},
                                "pain_point": {"type": "array", "items": {"type": "string"}, "description": "5 problem-solving keywords"},
                                "high_intent": {"type": "array", "items": {"type": "string"}, "description": "5 high commercial intent keywords"},
                                "demographic": {"type": "array", "items": {"type": "string"}, "description": "5 target audience keywords"},
                                "brand_terms": {"type": "array", "items": {"type": "string"}, "description": "3 brand-related keywords"}
                            },
                            "required": ["primary", "long_tail", "pain_point", "high_intent", "demographic", "brand_terms"]
                        },
                        "hero_title": {"type": "string", "description": "Main benefit headline"},
                        "hero_content": {"type": "string", "description": "Hero description"},
                        "features": {"type": "array", "items": {"type": "string"}, "description": "4 features"},
                        "whats_in_box": {"type": "array", "items": {"type": "string"}, "description": "4 items"},
                        "trust_builders": {"type": "array", "items": {"type": "string"}, "description": "3 trust elements"},
                        "faqs": {"type": "array", "items": {"type": "string"}, "description": "3 FAQ strings, each formatted as 'Q: question? A: answer'"},
                        "social_proof": {"type": "string", "description": "Customer satisfaction text"},
                        "guarantee": {"type": "string", "description": "Guarantee text"}
                    },
                    "required": ["title", "bullet_points", "long_description", "seo_keywords", "hero_title", "hero_content", "features", "whats_in_box", "trust_builders", "faqs", "social_proof", "guarantee"]
                }
            }
            
            # Retry logic for robust AI generation
            max_retries = 3
            retry_count = 0
            response = None
            
            while retry_count < max_retries:
                try:
                    print(f"AI generation attempt {retry_count + 1}/{max_retries}")
                    response = self.client.chat.completions.create(
                        model="gpt-4o-mini",  # Use a model capable of JSON output
                        messages=[
                            {"role": "system", "content": "You are a highly skilled Amazon listing copywriter, SEO expert, and PPC strategist with expertise in visual content direction. Your goal is to generate comprehensive and optimized Amazon listings with detailed A+ content strategies. CRITICAL REQUIREMENTS: 1) Generate ALL required fields including productTitle, bulletPoints, productDescription, aPlusContentPlan, ppcStrategy, keyword_cluster, brandSummary, and backendKeywords. 2) The productDescription field must be a detailed, compelling 3-paragraph description. 3) The aPlusContentPlan must include comprehensive, professional image_requirements for each section - these should be detailed enough for a photographer/designer to execute without additional guidance. 4) Always return a valid JSON object strictly following the user's schema. Focus on creating conversion-optimized content that drives sales through emotional connection and clear value proposition."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=4000,  # Increased max_tokens to accommodate detailed JSON output
                        temperature=0.7,
                    )
                    print(f"OpenAI API call successful on attempt {retry_count + 1}")
                    break
                except Exception as api_error:
                    retry_count += 1
                    print(f"OpenAI API error on attempt {retry_count}: {str(api_error)}")
                    if retry_count >= max_retries:
                        raise Exception(f"Failed to generate content after {max_retries} attempts: {str(api_error)}")
                    time.sleep(1)  # Brief pause before retry
            
            if response is None:
                raise Exception("Failed to get response from OpenAI API")
            
            # Extract regular message content (JSON response)
            ai_content = response.choices[0].message.content or "{}"
            # Immediately clean content to avoid Unicode errors
            ai_content = ai_content.encode('ascii', errors='ignore').decode('ascii')
            print(f"AI Response received: {len(ai_content)} characters")
            # Use safe encoding for Windows
            safe_preview = ai_content[:300]
            safe_ending = ai_content[-200:]
            print(f"AI Response preview: {safe_preview}...")
            print(f"AI Response ending: ...{safe_ending}")
            
            # Try to parse the JSON response directly
            result = None
            try:
                # Clean the content first
                cleaned_content = ai_content.strip()
                # Remove markdown code blocks if present
                if cleaned_content.startswith('```json'):
                    cleaned_content = cleaned_content[7:]
                if cleaned_content.endswith('```'):
                    cleaned_content = cleaned_content[:-3]
                cleaned_content = cleaned_content.strip()
                
                result = json.loads(cleaned_content)
                print("Direct JSON parsing successful!")
                print(f"🔍 AI response fields: {list(result.keys())}")
                print(f"🔍 Has productDescription: {'productDescription' in result}")
                if 'productDescription' in result:
                    desc_length = len(result['productDescription']) if result['productDescription'] else 0
                    print(f"🔍 Description length: {desc_length} characters")
                    if result['productDescription']:
                        print(f"🔍 Description preview: {result['productDescription'][:200]}...")
                    else:
                        print(f"🔍 productDescription field exists but is empty!")
                else:
                    print(f"🔍 productDescription field missing from AI response!")
                    # Check what description-related fields exist
                    desc_fields = [k for k in result.keys() if 'desc' in k.lower()]
                    print(f"🔍 Description-related fields found: {desc_fields}")
                
            except json.JSONDecodeError as e:
                print(f"Direct parsing failed: {e}, falling back to aggressive cleaning")
                cleaned_content = ai_content.strip()
                
                # More aggressive JSON cleaning for complex responses
                # Remove any text before the first {
                start_brace = cleaned_content.find('{')
                if start_brace > 0:
                    cleaned_content = cleaned_content[start_brace:]
                
                # Remove any text after the last }
                end_brace = cleaned_content.rfind('}')
                if end_brace > 0:
                    cleaned_content = cleaned_content[:end_brace + 1]
                
                # Try parsing again after aggressive cleaning
                try:
                    result = json.loads(cleaned_content)
                    print("✅ Aggressive cleaning successful!")
                except json.JSONDecodeError as e2:
                    print(f"❌ Even aggressive cleaning failed: {e2}")
                    # Continue to fallback methods below
            
            # If we already have a valid result, skip all the cleaning
            if result is not None:
                print("Using directly parsed result from function calling")
            else:
                # Only do cleaning if we don't have a result yet
                # Remove markdown code blocks if present
                if cleaned_content.startswith('```json'):
                    cleaned_content = cleaned_content[7:]
                if cleaned_content.endswith('```'):
                    cleaned_content = cleaned_content[:-3]
                
                # Remove all non-printable characters and control characters
                cleaned_content = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', cleaned_content)
            
                # Fix escaped quotes inside strings that break JSON
                # Pattern: "text \"quoted text\" more text" -> "text 'quoted text' more text"
                cleaned_content = re.sub(r'\\\"', "'", cleaned_content)
            
                # Fix double-quoted strings (like "long_description":"\"text\"")
                cleaned_content = re.sub(r':"\\?"([^"]+)\\?"",', r':"\1",', cleaned_content)
                cleaned_content = re.sub(r':"\\?"([^"]+)\\?"}', r':"\1"}', cleaned_content)
            
                # Fix common JSON formatting issues
                # Remove trailing commas before closing brackets/braces  
                cleaned_content = re.sub(r',(\s*[}\]])', r'\1', cleaned_content)
            
                # Remove any extra commas at end of arrays/objects
                cleaned_content = re.sub(r',\s*}', '}', cleaned_content)
                cleaned_content = re.sub(r',\s*]', ']', cleaned_content)
            
                # Try to find the start and end of JSON more precisely
                start_idx = cleaned_content.find('{')
                end_idx = cleaned_content.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    cleaned_content = cleaned_content[start_idx:end_idx]
            
                # Fix common AI JSON errors systematically
            
                # 1. Fix trailing commas before closing brackets/braces
                cleaned_content = re.sub(r',(\s*[}\]])', r'\1', cleaned_content)
            
                # 2. Fix FAQ malformed JSON - the most common error
                # Fix the specific malformed FAQ pattern we're seeing
                # Pattern: "faqs":["Q": "question?"A": Yes", it is...]
                faqs_match = re.search(r'"faqs":\s*\[(.*?)\]', cleaned_content, re.DOTALL)
                if faqs_match:
                    faqs_content = faqs_match.group(1)
                    # Fix each malformed FAQ entry
                    fixed_faqs = []
                    # Split carefully to handle the malformed structure
                    parts = re.split(r'",\s*"(?=Q":|Q\d+":)', faqs_content)
                    for part in parts:
                        part = part.strip().strip('"')
                        # Extract Q and A from malformed format
                        q_match = re.search(r'Q\d*":\s*"([^"]+)"', part)
                        a_match = re.search(r'"A\d*":\s*([^,]+)', part)
                        if q_match and a_match:
                            question = q_match.group(1)
                            answer = a_match.group(1).strip('"').strip()
                            # Remove trailing quote and comma
                            answer = re.sub(r'[",]+$', '', answer)
                            fixed_faqs.append(f'"Q: {question} A: {answer}"')
                    
                    if fixed_faqs:
                        fixed_faqs_str = '[' + ', '.join(fixed_faqs) + ']'
                        cleaned_content = re.sub(r'"faqs":\s*\[.*?\]', f'"faqs":{fixed_faqs_str}', cleaned_content, flags=re.DOTALL)
                # Fix pattern: "Q1": "question?"A1": "answer" should be "Q1: question? A1: answer"
                cleaned_content = re.sub(r'"(Q\d+)":\s*"([^"]*)"(A\d+)":\s*"([^"]*)"', r'"\1: \2 \3: \4"', cleaned_content)
                # Fix unquoted Yes/No answers
                cleaned_content = re.sub(r'"A":\s*Yes"', r'A: Yes"', cleaned_content)
                cleaned_content = re.sub(r'"A":\s*No"', r'A: No"', cleaned_content)
            
                # 3. Fix unquoted strings in arrays (like: 1 x 4-quart colander)
                # Look for patterns like: "word", unquoted text, "word" or unquoted text]
                cleaned_content = re.sub(r'",\s*([^"\[\]{}]+),\s*"', r'", "\1", "', cleaned_content)
                cleaned_content = re.sub(r'",\s*([^"\[\]{}]+)\s*\]', r'", "\1"]', cleaned_content)
                cleaned_content = re.sub(r'\[\s*([^"\[\]{}]+),\s*"', r'["\1", "', cleaned_content)
            
                # 4. Fix unquoted property names (like guarantee: instead of "guarantee":)
                cleaned_content = re.sub(r'[\s\t]*"?(\w+)"?\s*:', r'"\1":', cleaned_content)
            
                # 5. Fix missing quotes around string values
                # Pattern: "property": unquoted text (not starting with [ { " or number)
                cleaned_content = re.sub(r':\s*([^"\[\{0-9][^,\}\]]*[^,\}\]\s]),?', r': "\1",', cleaned_content)
                cleaned_content = re.sub(r':\s*([^"\[\{0-9][^,\}\]]*[^,\}\]\s])$', r': "\1"', cleaned_content, flags=re.MULTILINE)
            
                # Ensure proper closing
                if not cleaned_content.strip().endswith('}'):
                    cleaned_content = cleaned_content.strip() + '}'
            
                # Save cleaned content for debugging (disabled to prevent file permission issues)
                # with open('debug_cleaned_response.json', 'w', encoding='utf-8') as f:
                #     f.write(cleaned_content)
                print("Cleaned JSON content prepared (debug file writing disabled)")
            
            # Multiple JSON parsing attempts with different strategies (only if we don't have result yet)
            if result is None:
                parse_attempts = [
                    ("Direct parsing", lambda x: json.loads(x.strip())),
                    ("Strip and parse", lambda x: json.loads(x.strip().replace('\n', ' ').replace('\t', ' '))),
                    ("Extra cleanup", lambda x: json.loads(re.sub(r'\s+', ' ', x.strip()))),
                    ("Final fallback", lambda x: json.loads(re.sub(r'[^\x20-\x7E]', '', x).strip()))
                ]
                
                for attempt_name, parse_func in parse_attempts:
                    try:
                        print(f"Attempting JSON parse: {attempt_name}")
                        result = parse_func(cleaned_content)
                        print(f"JSON parsing successful with: {attempt_name}")
                        break
                    except json.JSONDecodeError as e:
                        print(f"JSON parse failed ({attempt_name}): {str(e)}")
                        continue
            
                if result is None:
                    print("All JSON parsing attempts failed, trying manual reconstruction...")
                # Last resort: try to extract key information manually
                try:
                    # Basic pattern matching to extract essential fields
                    title_match = re.search(r'"title":\s*"([^"]*)"', cleaned_content)
                    desc_match = re.search(r'"long_description":\s*"([^"]*)"', cleaned_content)
                    
                    if title_match and desc_match:
                        result = {
                            "title": title_match.group(1),
                            "bullet_points": ["Generated content available", "Please retry if needed"],
                            "long_description": desc_match.group(1),
                            "keywords": ["product", "listing"],
                            "hero_title": "Product Benefits",
                            "hero_content": "Quality product for your needs",
                            "features": ["Quality construction", "Reliable performance"],
                            "whats_in_box": ["Main product", "Documentation"],
                            "trust_builders": ["Quality assured", "Customer satisfaction"],
                            "faqs": ["Q: Is this reliable? A: Yes, very reliable"],
                            "social_proof": "Customers love this product",
                            "guarantee": "Satisfaction guaranteed"
                        }
                        print("Manual JSON reconstruction successful")
                    else:
                        raise Exception("Could not extract essential fields from malformed JSON")
                except Exception as manual_error:
                    print(f"⚠️ Manual reconstruction also failed: {manual_error}")
                    # Create minimal valid structure as absolute fallback
                    print("🔧 Creating minimal fallback JSON structure...")
                    result = {
                        "productTitle": f"{product.brand_name} {product.name} - Premium Quality Product",
                        "bulletPoints": [
                            "**PREMIUM QUALITY:** Exceptional construction with superior materials and craftsmanship for lasting performance",
                            "**RELIABLE PERFORMANCE:** Consistent operation designed for daily use with professional-grade standards", 
                            "**USER FRIENDLY:** Simple setup and intuitive design makes this perfect for everyone to use",
                            "**GREAT VALUE:** Outstanding quality at an affordable price point with excellent customer satisfaction",
                            "**SATISFACTION GUARANTEED:** Backed by quality assurance and dedicated customer support team"
                        ],
                        "productDescription": f"Transform your experience with the {product.brand_name} {product.name}. This premium product combines innovative design with reliable performance to deliver exceptional results. Whether you're looking for quality, durability, or value, this product exceeds expectations. What's Included: Main product, user manual, warranty information. Experience the {product.brand_name} difference - order yours today and discover why customers choose quality.",
                        "keyword_cluster": {
                            "primary_keywords": [product.name.lower(), "premium quality", "reliable performance", "great value"],
                            "secondary_keywords": [f"best {product.name.lower()}", f"premium {product.name.lower()}", f"quality {product.name.lower()}"],
                            "backend_search_terms": f"quality reliable premium value {product.name.lower()} {product.brand_name.lower()}",
                            "misspellings_and_synonyms": [product.name.lower()],
                            "ppc_keywords": [{"keyword": product.name.lower(), "match_type": "Exact", "goal": "Conversion", "bid_suggestion": "0.75", "target_acos": "20%"}]
                        },
                        "brandSummary": f"## Quality First ## At {product.brand_name}, we deliver premium products that exceed expectations and provide lasting value.",
                        "backendKeywords": f"premium quality reliable performance great value {product.name.lower()} {product.brand_name.lower()}",
                        "aPlusContentPlan": {
                            "section1_hero": {
                                "title": "Why Choose Premium Quality?",
                                "content": "Experience superior performance and reliability with our premium product line.",
                                "keywords": ["premium", "quality", "reliable"],
                                "imageDescription": "Professional lifestyle image showing satisfied customer using product",
                                "seoOptimization": "Focus on quality and premium positioning"
                            },
                            "overallStrategy": "Premium positioning with quality focus"
                        },
                        "ppcStrategy": {
                            "campaignStructure": {
                                "exactMatchCampaign": {
                                    "keywords": [product.name.lower()],
                                    "bidStrategy": "Fixed bids starting at $0.75",
                                    "dailyBudget": "$30",
                                    "targetAcos": "20%"
                                }
                            }
                        }
                    }
                    print("✅ Fallback JSON structure created successfully")
            
            # Remove any emojis from all text fields FIRST before any processing
            print("Before emoji removal - checking title...")
            try:
                title_before = result.get('title', '')
                print(f"Title before cleanup: {len(title_before)} chars, has Unicode: {any(ord(c) > 127 for c in title_before)}")
            except Exception as e:
                print(f"Error checking title before: {e}")
            
            result = self._comprehensive_emoji_removal(result)
            
            print("After emoji removal - checking title...")
            try:
                title_after = result.get('title', '')
                print(f"Title after cleanup: {len(title_after)} chars, has Unicode: {any(ord(c) > 127 for c in title_after)}")
            except Exception as e:
                print(f"Error checking title after: {e}")
            
            # Validate result has required fields for new JSON structure
            required_fields = ["productTitle", "bulletPoints", "productDescription", "keyword_cluster", "brandSummary", "backendKeywords", "aPlusContentPlan", "ppcStrategy"]
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                # Safe console output - avoid Unicode errors
                try:
                    print(f"Warning: Missing fields {len(missing_fields)} fields, adding defaults...")
                except UnicodeEncodeError:
                    print("Warning: Missing fields detected, adding defaults...")
                defaults = {
                    "productTitle": f"{product.brand_name} {product.name} - Quality Product",
                    "bulletPoints": ["**PREMIUM QUALITY:** High quality construction with superior materials and craftsmanship", "**RELIABLE PERFORMANCE:** Consistent and dependable operation for daily use", "**EXCEPTIONAL VALUE:** Great quality at an affordable price point", "**CUSTOMER SATISFACTION:** Backed by thousands of positive reviews and testimonials", "**EASY TO USE:** Simple setup and user-friendly design for everyone"],
                    "productDescription": f"The {product.name} by {product.brand_name} offers exceptional quality and performance.",
                    "keyword_cluster": {
                        "primary_keywords": [product.name.lower(), "quality", "reliable", "performance", "value"],
                        "secondary_keywords": [f"best {product.name.lower()}", f"premium {product.name.lower()}", f"high quality {product.name.lower()}"],
                        "backend_search_terms": "problem solving solution fix buy best cheap home family professional",
                        "misspellings_and_synonyms": [product.name.lower()],
                        "ppc_keywords": [{"keyword": product.name.lower(), "match_type": "Exact", "goal": "Conversion", "bid_suggestion": "0.75", "target_acos": "20%"}]
                    },
                    "brandSummary": f"## Quality First ## At {product.brand_name}, we believe in making quality products that enhance your life. Join thousands who trust {product.brand_name} for reliable performance.",
                    "backendKeywords": "quality reliable performance value home family professional problem solving solution",
                    "aPlusContentPlan": {
                        "section1_hero": {
                            "title": "Why Choose Our Premium Quality?",
                            "content": "Experience the difference with our superior product design and customer-focused approach.",
                            "keywords": ["premium", "quality", "superior"],
                            "imageDescription": "Hero lifestyle shot showing satisfied customer using product",
                            "seoOptimization": "Focus on quality and premium positioning"
                        },
                        "section2_features": {
                            "title": "Key Features & Benefits",
                            "content": "Discover what makes our product stand out with premium materials and thoughtful design.",
                            "keywords": ["features", "benefits", "premium materials"],
                            "imageDescription": "Feature callouts with detailed product shots",
                            "seoOptimization": "Feature-based keywords for detailed searches"
                        },
                        "overallStrategy": "Complete A+ content strategy for maximum conversion"
                    },
                    "ppcStrategy": {
                        "campaignStructure": {
                            "exactMatchCampaign": {
                                "keywords": [product.name.lower()],
                                "bidStrategy": "Fixed bids starting at $0.75",
                                "dailyBudget": "$30",
                                "targetAcos": "20%"
                            }
                        },
                        "negativeKeywords": {
                            "immediate": ["cheap", "free", "used"],
                            "strategy": "Protect budget from low-intent traffic"
                        }
                    }
                }
                for field in missing_fields:
                    result[field] = defaults.get(field, "Content available")
            
            # FORCE ASCII-ONLY title regardless of AI output or emoji removal function
            raw_title = result.get('productTitle', f"{product.name} - Premium Quality")
            # AGGRESSIVE ASCII conversion with multiple methods
            ascii_title = raw_title.encode('ascii', errors='ignore').decode('ascii')
            ascii_title = ''.join(c for c in ascii_title if 32 <= ord(c) <= 126)
            ascii_title = ascii_title.replace('–', '-').replace('"', '"').replace('"', '"')
            listing.title = ascii_title.strip()[:200] if ascii_title.strip() else f"{product.name} - Premium Quality"
            
            # Get bullet points from new structure
            bullet_points = result.get('bulletPoints', [])
            if bullet_points:
                # Clean bullet points and ensure proper format
                cleaned_bullets = []
                for bullet in bullet_points:
                    # Clean ASCII
                    clean_bullet = bullet.encode('ascii', errors='ignore').decode('ascii')
                    clean_bullet = ''.join(c for c in clean_bullet if 32 <= ord(c) <= 126)
                    cleaned_bullets.append(clean_bullet)
                listing.bullet_points = '\n\n'.join(cleaned_bullets)
            else:
                listing.bullet_points = ''
            
            # Handle product description with comprehensive debugging
            print(f"🔍 DEBUG: Checking for productDescription in result...")
            print(f"🔍 Available keys in result: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}")
            
            product_description = result.get('productDescription', '')
            print(f"🔍 productDescription from result: {'Found' if product_description else 'Empty/Missing'}")
            
            if not product_description:
                # Try alternative field names in case AI used different naming
                alternatives = ['long_description', 'description', 'product_description', 'productDesc', 'desc']
                for alt in alternatives:
                    product_description = result.get(alt, '')
                    if product_description:
                        print(f"🔍 Found description in alternative field '{alt}': {len(product_description)} chars")
                        break
            
            # If still no description, generate a comprehensive one
            if not product_description:
                # Create a detailed fallback description
                product_description = f"""Are you looking for a reliable and high-quality {product.name}? The {product.brand_name} {product.name} delivers exceptional performance and value that exceeds expectations.

This premium product features {product.features if product.features else 'advanced functionality and superior design'}. Whether you're using it daily or for special occasions, our {product.name} provides the reliability and quality you deserve. Built with attention to detail and customer satisfaction in mind.

What's Included: {product.name}, user manual, warranty information, and customer support. Experience the {product.brand_name} difference today - order now and discover why customers choose quality and performance. Your satisfaction is our guarantee."""
                
                print(f"⚠️ No AI description found in any field, generated fallback: {len(product_description)} characters")
                print(f"⚠️ Fallback preview: {product_description[:150]}...")
            else:
                print(f"✅ Product description found: {len(product_description)} characters")
                print(f"✅ Description preview: {product_description[:150]}...")
            
            listing.long_description = product_description
            
            # Parse keywords from new structure with debugging
            print(f"🔍 DEBUG: Checking for keywords in result...")
            keyword_cluster = result.get('keyword_cluster', {})
            print(f"🔍 keyword_cluster found: {'Yes' if keyword_cluster else 'No'}")
            
            if keyword_cluster:
                print(f"🔍 keyword_cluster keys: {list(keyword_cluster.keys())}")
                primary_keywords = keyword_cluster.get('primary_keywords', [])
                secondary_keywords = keyword_cluster.get('secondary_keywords', [])
                print(f"🔍 Primary keywords: {len(primary_keywords)} found")
                print(f"🔍 Secondary keywords: {len(secondary_keywords)} found")
                if primary_keywords:
                    print(f"🔍 Primary keyword examples: {primary_keywords[:3]}")
            else:
                print(f"🔍 No keyword_cluster found, checking for alternative keyword fields...")
                # Try alternative keyword field names
                keyword_alternatives = ['keywords', 'seo_keywords', 'primary_keywords', 'keywordCluster']
                for alt in keyword_alternatives:
                    if alt in result:
                        print(f"🔍 Found keywords in '{alt}' field")
                        break
                else:
                    print(f"🔍 No keyword fields found in any format")
            
            primary_keywords = keyword_cluster.get('primary_keywords', []) if keyword_cluster else []
            secondary_keywords = keyword_cluster.get('secondary_keywords', []) if keyword_cluster else []
            
            # Generate fallback keywords if none found
            if not primary_keywords and not secondary_keywords:
                print(f"⚠️ No keywords generated by AI, creating fallback keywords...")
                primary_keywords = [
                    product.name.lower(),
                    f"{product.name.lower()} {product.brand_name.lower()}",
                    f"premium {product.name.lower()}",
                    f"quality {product.name.lower()}",
                    f"best {product.name.lower()}"
                ]
                secondary_keywords = [
                    f"buy {product.name.lower()} online",
                    f"{product.name.lower()} for sale",
                    f"top rated {product.name.lower()}",
                    f"professional {product.name.lower()}"
                ]
                print(f"⚠️ Generated {len(primary_keywords)} primary + {len(secondary_keywords)} secondary fallback keywords")
            
            all_keywords = primary_keywords + secondary_keywords
            listing.keywords = ', '.join(all_keywords) if all_keywords else ''
            
            backend_keywords = result.get('backendKeywords', '')
            if not backend_keywords:
                # Generate fallback backend keywords
                backend_keywords = f"premium quality {product.name.lower()} {product.brand_name.lower()} reliable performance great value"
                print(f"⚠️ No backend keywords from AI, using fallback: {backend_keywords}")
            
            listing.amazon_backend_keywords = backend_keywords
            
            print(f"✅ Final keywords count: {len(all_keywords)} total keywords")
            print(f"✅ Backend keywords length: {len(backend_keywords)} characters")
            
            # Parse A+ content from comprehensive new structure
            aplus_plan = result.get('aPlusContentPlan', {})
            
            # Extract hero section from simplified structure
            hero_section = aplus_plan.get('hero_section', {}) or aplus_plan.get('section1_hero', {})
            listing.hero_title = hero_section.get('title', result.get('brandSummary', '').split('##')[1].strip() if '##' in result.get('brandSummary', '') else 'Premium Quality')
            listing.hero_content = hero_section.get('content', result.get('brandSummary', ''))
            
            # Extract features from A+ plan (handle both old and new structure)
            features_section = aplus_plan.get('features_section', {}) or aplus_plan.get('section2_features', {})
            features_content = features_section.get('content', '')
            if features_content:
                # Extract feature points from the content or use keywords as features
                feature_keywords = features_section.get('keywords', [])
                features_list = feature_keywords if feature_keywords else [
                    "Premium quality construction",
                    "Reliable performance", 
                    "User-friendly design",
                    "Exceptional value"
                ]
            else:
                features_list = [
                    "Premium quality construction",
                    "Reliable performance",
                    "User-friendly design", 
                    "Exceptional value"
                ]
            listing.features = '\n'.join(features_list)
            
            # Create whats in box from usage section or defaults
            usage_section = aplus_plan.get('section4_usage', {})
            whats_in_box_list = [
                "Main product",
                "User manual", 
                "Warranty information",
                "Quick start guide"
            ]
            listing.whats_in_box = '\n'.join(whats_in_box_list)
            
            # Extract trust builders from social proof and guarantee sections
            social_section = aplus_plan.get('section5_social_proof', {})
            guarantee_section = aplus_plan.get('section6_guarantee', {})
            trust_list = [
                "Quality tested and verified",
                "Trusted by thousands of customers",
                "Satisfaction guaranteed",
                "Backed by manufacturer warranty"
            ]
            listing.trust_builders = '\n'.join(trust_list)
            
            # Create comprehensive FAQs based on A+ sections
            faq_strings = [
                "Q: What makes this product different from competitors? A: Our unique features and superior quality set us apart from generic alternatives.",
                "Q: How do I use this product effectively? A: Follow the included quick start guide for optimal results and performance.", 
                "Q: What's included in the package? A: Complete kit with main product, user manual, warranty information, and quick start guide.",
                "Q: Is there a warranty or guarantee? A: Yes, backed by manufacturer warranty and 100% satisfaction guarantee.",
                "Q: How long does shipping take? A: Fast and reliable shipping with tracking information provided."
            ]
            listing.faqs = '\n'.join(faq_strings)
            listing.social_proof = social_section.get('content', "Join thousands of satisfied customers who trust our products for quality and performance")
            listing.guarantee = guarantee_section.get('content', "100% satisfaction guarantee - if you're not completely happy, we'll make it right")
            
            # Create structured HTML A+ content from the JSON data
            aplus_html = self._create_structured_aplus_html(aplus_plan, result)
            listing.amazon_aplus_content = aplus_html
            
            # Create formatted A+ content HTML for display
            # Use the result values directly since listing fields aren't saved yet
            self.logger.info("Generating A+ content HTML...")
            # Build comprehensive A+ content HTML from the plan
            sections_html = []
            
            # Generate HTML for each A+ section
            for section_key, section_data in aplus_plan.items():
                if section_key.startswith('section') and isinstance(section_data, dict):
                    section_title = section_data.get('title', '')
                    section_content = section_data.get('content', '')
                    section_keywords = ', '.join(section_data.get('keywords', []))
                    image_desc = section_data.get('imageDescription', '')
                    seo_note = section_data.get('seoOptimization', '')
                    
                    section_html = f"""
    <div class="aplus-section">
        <h3>{section_title}</h3>
        <p>{section_content}</p>
        <div class="seo-info">
            <small><strong>Keywords:</strong> {section_keywords}</small><br>
            <small><strong>Image:</strong> {image_desc}</small><br>
            <small><strong>SEO Focus:</strong> {seo_note}</small>
        </div>
    </div>"""
                    sections_html.append(section_html)
            
            # Traditional content as fallback
            features_html = '\n'.join([f"        <li>{feature}</li>" for feature in features_list])
            whats_in_box_html = '\n'.join([f"        <li>{item}</li>" for item in whats_in_box_list])
            trust_html = '\n'.join([f"        <li>{trust}</li>" for trust in trust_list])
            faqs_html = '\n'.join([f"    <p><strong>{faq}</strong></p>" for faq in faq_strings])
            
            # Generate PPC strategy HTML
            ppc_strategy = result.get('ppcStrategy', {})
            campaign_structure = ppc_strategy.get('campaignStructure', {})
            ppc_html = ""
            
            if campaign_structure:
                ppc_sections = []
                for campaign_type, campaign_data in campaign_structure.items():
                    if isinstance(campaign_data, dict):
                        keywords = ', '.join(campaign_data.get('keywords', []))
                        bid_strategy = campaign_data.get('bidStrategy', '')
                        budget = campaign_data.get('dailyBudget', '')
                        acos = campaign_data.get('targetAcos', '')
                        
                        ppc_sections.append(f"""
        <div class="ppc-campaign">
            <h4>{campaign_type.replace('Campaign', ' Campaign').title()}</h4>
            <p><strong>Keywords:</strong> {keywords}</p>
            <p><strong>Bid Strategy:</strong> {bid_strategy}</p>
            <p><strong>Daily Budget:</strong> {budget}</p>
            <p><strong>Target ACoS:</strong> {acos}</p>
        </div>""")
                
                ppc_html = f"""
<div class="ppc-strategy">
    <h3>PPC Campaign Strategy</h3>
    {''.join(ppc_sections)}
    <div class="ppc-negatives">
        <h4>Negative Keywords Strategy</h4>
        <p><strong>Immediate Negatives:</strong> {', '.join(ppc_strategy.get('negativeKeywords', {}).get('immediate', []))}</p>
        <p><strong>Strategy:</strong> {ppc_strategy.get('negativeKeywords', {}).get('strategy', '')}</p>
    </div>
</div>"""

            # Generate comprehensive A+ content plan
            aplus_html = f"""<div class="aplus-hero">
    <h2>{listing.hero_title}</h2>
    <p>{listing.hero_content}</p>
</div>

<div class="aplus-comprehensive-plan">
    <h2>Complete A+ Content Strategy</h2>
    {''.join(sections_html)}
</div>

<div class="aplus-strategy-summary">
    <h3>Overall A+ Strategy</h3>
    <p>{aplus_plan.get('overallStrategy', 'Complete A+ content plan designed to guide customers from awareness to purchase')}</p>
</div>

{ppc_html}

<div class="keyword-strategy">
    <h3>Keyword Strategy</h3>
    <p>{result.get('keywordStrategy', 'Strategic keyword placement for maximum SEO impact')}</p>
    <h4>Competitor Keywords</h4>
    <p>{result.get('topCompetitorKeywords', 'Analysis of competitive landscape for positioning')}</p>
</div>

<div class="aplus-features">
    <h3>Key Features & Benefits</h3>
    <ul>
{features_html}
    </ul>
</div>

<div class="aplus-whats-in-box">
    <h3>What is in the Box</h3>
    <ul>
{whats_in_box_html}
    </ul>
</div>

<div class="aplus-trust">
    <h3>Trust & Quality</h3>
    <ul>
{trust_html}
    </ul>
</div>

<div class="aplus-testimonials">
    <h3>Customer Satisfaction</h3>
    <p>{result.get('social_proof', '')}</p>
    <p><strong>Our Guarantee:</strong> {result.get('guarantee', '')}</p>
</div>

<div class="aplus-faqs">
    <h3>Frequently Asked Questions</h3>
{faqs_html}
</div>"""
            # Keep the JSON data instead of overwriting with HTML
            # The HTML is nice but we want to preserve the structured data with image suggestions
            # listing.amazon_aplus_content = aplus_html  # Disabled to preserve JSON structure
            self.logger.info(f"A+ content HTML set: {len(aplus_html)} characters")
            
            # Parse conversion elements (only if they exist and have content)
            conversion_elements = result.get('conversion_elements', {})
            print(f"Conversion elements: {conversion_elements}")
            if False:  # Disable this block to preserve our A+ content HTML
                conversion_sections = []
                
                # What's in the box
                whats_in_box = conversion_elements.get('whats_in_box', [])
                if whats_in_box:
                    conversion_sections.append("WHAT'S IN THE BOX:\n" + '\n'.join([f"• {item}" for item in whats_in_box]))
                
                # Trust builders
                trust_builders = conversion_elements.get('trust_builders', [])
                if trust_builders:
                    conversion_sections.append("TRUST & GUARANTEES:\n" + '\n'.join([f"• {trust}" for trust in trust_builders]))
                
                # Social proof
                social_proof = conversion_elements.get('social_proof', '')
                if social_proof:
                    conversion_sections.append(f"CUSTOMER SATISFACTION:\n{social_proof}")
                
                # Guarantee
                guarantee = conversion_elements.get('guarantee', '')
                if guarantee:
                    conversion_sections.append(f"OUR GUARANTEE:\n{guarantee}")
                
                # FAQs
                faqs = conversion_elements.get('faqs', [])
                if faqs:
                    faq_section = "FREQUENTLY ASKED QUESTIONS:\n"
                    for faq in faqs:
                        if isinstance(faq, dict):
                            question = faq.get('q', '')
                            answer = faq.get('a', '')
                            faq_section += f"\nQ: {question}\nA: {answer}\n"
                    conversion_sections.append(faq_section)
                
                listing.short_description = '\n\n'.join(conversion_sections)
            else:
                listing.short_description = result.get('short_description', '')
            
            # Skip the old complex parsing logic - bullets already processed above
            # The bullet points are already cleaned and set above, so we don't need this section
            
            # This section has been disabled as bullets are already processed above
            if False:  # Disabled bullet processing section
                cleaned_bullets = []
                for bullet in []:
                    # Remove all markdown formatting and emojis VERY aggressively
                    import re
                    # Multiple passes to ensure all markdown and emojis are removed
                    cleaned_bullet = bullet
                
                    # Remove all emojis first
                    # Unicode ranges for emojis
                    emoji_pattern = re.compile(
                        "["
                        "\U0001F600-\U0001F64F"  # emoticons
                        "\U0001F300-\U0001F5FF"  # symbols & pictographs
                        "\U0001F680-\U0001F6FF"  # transport & map symbols
                        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                        "\U00002702-\U000027B0"
                        "\U000024C2-\U0001F251"
                        "]+", flags=re.UNICODE)
                    cleaned_bullet = emoji_pattern.sub('', cleaned_bullet)
                
                    # Remove all variations of bold formatting
                    cleaned_bullet = re.sub(r'\*\*(.*?)\*\*', r'\1', cleaned_bullet)  # **text**
                    cleaned_bullet = re.sub(r'\*\*([^*]+)\*\*', r'\1', cleaned_bullet)  # **text** (non-greedy)
                    cleaned_bullet = re.sub(r'\*\*', '', cleaned_bullet)  # Remove remaining **
                    
                    # Remove single asterisks
                    cleaned_bullet = re.sub(r'\*([^*]+)\*', r'\1', cleaned_bullet)  # *text*
                    cleaned_bullet = cleaned_bullet.replace('*', '')  # Remove all remaining *
                    
                    # Keep colon formatting as specified in prompt
                    # DO NOT convert colons to dashes - follow prompt requirements
                    
                    # Clean up extra spaces and formatting
                    cleaned_bullet = re.sub(r'\s+', ' ', cleaned_bullet).strip()
                
                    # Ensure proper colon format as per prompt requirements
                    if ':' not in cleaned_bullet and len(cleaned_bullet) > 20:
                        # Add colon after first few words to match prompt format
                        parts = cleaned_bullet.split(' ')
                        if len(parts) > 2:
                            label = ' '.join(parts[:2]).upper()
                            content = ' '.join(parts[2:])
                            cleaned_bullet = f"{label}: {content}"
                    
                    cleaned_bullets.append(cleaned_bullet)
                
                # This line is disabled since bullets are already processed above
                # listing.bullet_points = '\n\n'.join(cleaned_bullets)
            
            # Don't overwrite long_description - it's already set above from productDescription
            
            # Parse enhanced SEO keywords structure - DISABLED (keywords already processed above)
            # The keyword processing is already handled correctly above, so we don't need this section
            # which was overwriting the good keyword data
            
            # Parse nested A+ content modules
            aplus_content = result.get('aplus_content', {})
            if isinstance(aplus_content, dict):
                aplus_sections = []
                for module_key, module_data in aplus_content.items():
                    if isinstance(module_data, dict):
                        module_type = module_data.get('type', '')
                        title = module_data.get('title', '')
                        content = module_data.get('content', '')
                        image_suggestion = module_data.get('image_suggestion', '')
                        
                        section = f"<div class='aplus-module {module_key}'>\n"
                        if module_type:
                            section += f"<p><strong>Module Type:</strong> {module_type}</p>\n"
                        section += f"<h3>{title}</h3>\n<p>{content}</p>"
                        if image_suggestion:
                            section += f"\n<p><em>Image Requirements: {image_suggestion}</em></p>"
                        section += "</div>"
                        aplus_sections.append(section)
                
                # listing.amazon_aplus_content = '\n\n'.join(aplus_sections)
                print(f"CONVERSION ELEMENTS BLOCK - DISABLED TO PRESERVE HTML")
            # else:
            #     listing.amazon_aplus_content = result.get('aplus_content', '')
            #     print(f"OVERWRITING A+ content with result.aplus_content: {len(listing.amazon_aplus_content)} chars")
            
            # Parse comprehensive conversion boosters
            conversion_boosters = result.get('conversion_boosters', {})
            if isinstance(conversion_boosters, dict):
                booster_sections = []
                
                # What's in the box
                whats_in_box = conversion_boosters.get('whats_in_box', [])
                if whats_in_box:
                    booster_sections.append("📦 WHAT'S IN THE BOX:\n" + '\n'.join([f"• {item}" for item in whats_in_box]))
                
                # Trust builders
                trust_builders = conversion_boosters.get('trust_builders', [])
                if trust_builders:
                    booster_sections.append("🛡️ TRUST & GUARANTEES:\n" + '\n'.join([f"• {trust}" for trust in trust_builders]))
                
                # Social proof
                social_proof = conversion_boosters.get('social_proof', '')
                if social_proof:
                    booster_sections.append(f"⭐ SOCIAL PROOF:\n{social_proof}")
                
                # Comparison advantages
                comparison_advantage = conversion_boosters.get('comparison_advantage', '')
                if comparison_advantage:
                    booster_sections.append(f"🆚 WHY CHOOSE US:\n{comparison_advantage}")
                    
                # FAQs
                faqs = conversion_boosters.get('faqs', [])
                if faqs:
                    faq_section = "❓ FREQUENTLY ASKED QUESTIONS:\n"
                    for faq in faqs:
                        if isinstance(faq, dict):
                            question = faq.get('q', '')
                            answer = faq.get('a', '')
                            faq_section += f"\nQ: {question}\nA: {answer}\n"
                    booster_sections.append(faq_section)
                
                listing.short_description = '\n\n'.join(booster_sections)
            else:
                # Fallback for simple array format
                boosters = result.get('conversion_boosters', [])
                if boosters:
                    listing.short_description = '\n'.join(boosters)
            
            print("AI content successfully parsed and saved!")
            try:
                print(f"   Title: {listing.title[:100]}...")
                print(f"   Bullet points: {len(result.get('bulletPoints', []))} items")
                print(f"   First bullet: {bullet_points[0] if bullet_points else 'None'}")
            except UnicodeEncodeError:
                print(f"   Title: [Unicode title, {len(listing.title)} chars]")
                print(f"   Bullet points: {len(result.get('bulletPoints', []))} items")
                print("   First bullet: [Unicode content]")
            
            # Continue to process A+ content fields
            print(f"   Keywords: {len(all_keywords)} total")
            
            # QUALITY VALIDATION - Validate listing for 10/10 conversion quality
            try:
                from .quality_validator import ListingQualityValidator
                validator = ListingQualityValidator()
                
                # Prepare listing data for validation
                validation_data = {
                    'title': listing.title,
                    'bullet_points': listing.bullet_points,
                    'long_description': listing.long_description,
                    'faqs': listing.faqs
                }
                
                # Get quality report
                quality_report = validator.get_validation_json(validation_data)
                print(f"\n=== QUALITY VALIDATION RESULTS ===")
                print(f"Overall Score: {quality_report['overall_score']}/10 (Grade: {quality_report['grade']})")
                print(f"Emotion Score: {quality_report['emotion_score']}/10")
                print(f"Conversion Score: {quality_report['conversion_score']}/10")
                print(f"Trust Score: {quality_report['trust_score']}/10")
                
                # Log section scores
                for section in quality_report['section_scores']:
                    print(f"{section['section']}: {section['score']}/{section['max_score']} ({section['percentage']}%)")
                
                # Show critical issues if any
                critical_issues = [issue for issue in quality_report['issues'] if issue['type'] == 'critical']
                if critical_issues:
                    print(f"\nCRITICAL ISSUES TO ADDRESS:")
                    for issue in critical_issues:
                        print(f"- {issue['message']}")
                        print(f"  Solution: {issue['suggestion']}")
                
                # Store quality metrics (could be saved to database later)
                listing.quality_score = quality_report['overall_score']
                listing.emotion_score = quality_report['emotion_score']
                listing.conversion_score = quality_report['conversion_score']
                listing.trust_score = quality_report['trust_score']
                
                print(f"=== END QUALITY VALIDATION ===\n")
                
            except Exception as validation_error:
                print(f"Quality validation failed: {validation_error}")
                # Don't fail listing generation if validation fails
                pass
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print(f"Error position: line {e.lineno} column {e.colno}")
            safe_first = ai_content[:1000].encode('ascii', errors='ignore').decode('ascii')
            safe_last = ai_content[-500:].encode('ascii', errors='ignore').decode('ascii')
            print(f"Raw AI response (first 1000 chars): {safe_first}")
            print(f"Raw AI response (last 500 chars): ...{safe_last}")
            
            # Save the full response to debug file for analysis (disabled to prevent file permission issues)
            # with open('debug_ai_response.json', 'w', encoding='utf-8') as f:
            #     f.write(ai_content)
            print("Full AI response content prepared (debug file writing disabled)")
            
            # Try to clean and re-parse the JSON
            try:
                import re
                cleaned_content = ai_content.strip()
                
                # Remove markdown code blocks
                if cleaned_content.startswith('```json'):
                    cleaned_content = cleaned_content[7:]
                if cleaned_content.endswith('```'):
                    cleaned_content = cleaned_content[:-3]
                
                # Remove trailing commas before closing brackets/braces
                cleaned_content = re.sub(r',\s*}', '}', cleaned_content)
                cleaned_content = re.sub(r',\s*]', ']', cleaned_content)
                
                result = json.loads(cleaned_content.strip())
                print("Successfully parsed cleaned JSON - proceeding with AI content")
                    
                    # Continue with normal parsing
                listing.title = result.get('title', '')[:200]
                
                # Add A+ content parsing in the cleanup section
                listing.hero_title = result.get('hero_title', '')
                listing.hero_content = result.get('hero_content', '')
                listing.features = '\n'.join(result.get('features', []))
                listing.whats_in_box = '\n'.join(result.get('whats_in_box', []))
                listing.trust_builders = '\n'.join(result.get('trust_builders', []))
                
                # Handle FAQs
                faqs = result.get('faqs', [])
                faq_strings = []
                for faq in faqs:
                    if isinstance(faq, dict):
                        q = faq.get('question', faq.get('q', ''))
                        a = faq.get('answer', faq.get('a', ''))
                        faq_strings.append(f"Q: {q} A: {a}")
                    else:
                        faq_strings.append(str(faq))
                listing.faqs = '\n'.join(faq_strings)
                listing.social_proof = result.get('social_proof', '')
                listing.guarantee = result.get('guarantee', '')
                
                print("AI content successfully parsed and saved to all A+ fields!")
                
                # Process bullet points and other content normally...
                
            except Exception as cleanup_error:
                print(f"[ERROR] JSON cleanup also failed: {cleanup_error}")
                safe_cleaned = cleaned_content[-300:].encode('ascii', errors='ignore').decode('ascii')
                print(f"[ERROR] Cleaned content (last 300 chars): ...{safe_cleaned}")
                raise Exception(f"AI generated invalid JSON that could not be parsed: {str(cleanup_error)}. Please try again.")
        except Exception as e:
            print(f"[ERROR] OpenAI API error: {e}")
            import traceback
            print(f"[ERROR] Full error traceback: {traceback.format_exc()}")
            # DO NOT use fallback content - raise the error instead
            raise Exception(f"AI generation failed: {str(e)}. Please check your OpenAI API key and try again.")

    def _generate_fallback_amazon(self, product, listing):
        print(f"[WARNING] USING FALLBACK CONTENT for {product.name} (AI generation failed or unavailable)")
        # Generate dynamic fallback based on product context
        product_context = self._analyze_product_context(product)
        
        # Extract better product descriptor from name
        product_name_lower = product.name.lower()
        
        # Try to get meaningful product category instead of just first word
        if 'cutting board' in product_name_lower:
            primary_keyword = "cutting board"
            product_category = "kitchen tool"
        elif 'chair' in product_name_lower:
            primary_keyword = "chair"
            product_category = "seating"
        elif any(term in product_name_lower for term in ['laptop', 'computer', 'monitor']):
            primary_keyword = "computer accessory"
            product_category = "technology"
        elif any(term in product_name_lower for term in ['board', 'mat', 'surface']):
            primary_keyword = "board"
            product_category = "kitchen accessory"
        else:
            # Use last two words if available, or full name if short
            words = product.name.split()
            if len(words) >= 2:
                primary_keyword = ' '.join(words[-2:]).lower()
                product_category = "product"
            else:
                primary_keyword = product.name.lower()
                product_category = "item"
            
        listing.title = f"{product.name} - {product.brand_name} Premium {product_category.title()} with Superior Quality - Satisfaction Guaranteed"[:200]
        listing.bullet_points = f"""Enhances Performance - Experience superior {primary_keyword} quality that transforms your daily routine with professional-grade reliability
Maximizes Durability - Premium materials and thoughtful design work together ensuring long-lasting satisfaction throughout extended use
Delivers Quality Results - Advanced features provide consistent performance that exceeds expectations and outperforms standard alternatives  
Fits Your Lifestyle - Versatile design accommodates different preferences and requirements for optimal user experience
Guarantees Satisfaction - Feel the difference from first use, backed by our commitment to quality and customer satisfaction"""
        
        # Determine context based on product category for description
        context_area = "experience"
        if product_category in ["kitchen tool", "kitchen accessory"]:
            context_area = "kitchen"
        elif product_category == "seating":
            context_area = "workspace"
        elif product_category == "technology":
            context_area = "setup"
            
        listing.long_description = f"""EXPERIENCE PREMIUM QUALITY - TRANSFORM YOUR {context_area.upper()} TODAY

You deserve better than settling for average quality. That is where the {product.name} steps in - designed for excellence, built for reliability.

THE QUALITY DIFFERENCE

This is not just another {product_category}. Our premium design delivers exceptional performance that enhances your daily experience. Feel the difference from the moment you start using it.

WHAT MAKES THIS SPECIAL

Built with attention to detail and quality materials that ensure long-lasting satisfaction. Every aspect designed for users who appreciate superior products - from construction to functionality.

JOIN THOUSANDS OF SATISFIED CUSTOMERS

\"Finally, a {primary_keyword} that delivers on its promises\" - Verified Customer. Experience why this is rated among the best for quality and performance."""
        
        listing.amazon_backend_keywords = f"{product.name}, {product.brand_name}, {primary_keyword}, premium {product_category}, quality {product_category}, kitchen accessories"
        
        # Enhanced A+ Content with all modules
        listing.amazon_aplus_content = """<div class='aplus-module module1'>
<p><strong>Module Type:</strong> Hero Banner with Text Overlay</p>
<h3>Experience the Gaming Difference</h3>
<p>Transform your gaming setup with professional-grade comfort. Join thousands who have discovered the ultimate gaming chair.</p>
<p><em>Image Requirements: Lifestyle hero shot showing chair in gaming setup with happy gamer</em></p>
</div>

<div class='aplus-module module2'>
<p><strong>Module Type:</strong> 4-Feature Grid with Icons</p>
<h3>Everything You Need for All-Day Gaming</h3>
<p>Ergonomic Support: Perfect posture | Memory Foam: Zero fatigue | Adjustable Design: Custom fit | Premium Build: Lasting durability</p>
</div>"""
        
        # CRITICAL: Add conversion boosters to short_description
        listing.short_description = """WHAT IS IN THE BOX:
- Premium gaming chair with all components
- Assembly hardware and tools
- Detailed setup guide
- Warranty registration card

TRUST & GUARANTEES:
- 2-year manufacturer warranty
- 30-day satisfaction guarantee
- Free shipping and returns
- Certified quality standards

SOCIAL PROOF:
Loved by 10,000+ happy gamers - 4.8 stars average

WHY CHOOSE US:
Vs. other brands: Better ergonomics, superior materials, 40% more affordable than premium competitors

FREQUENTLY ASKED QUESTIONS:

Q: Can I game for 8+ hours without back pain?
A: Absolutely! Our chair was tested by pro gamers during all-nighters. The adjustable lumbar support keeps your spine aligned.

Q: How does this compare to other gaming chairs?
A: Unlike basic gaming chairs, our design includes premium memory foam and four-dimensional armrests. Gamers report 90% less fatigue.

Q: What makes this the best gaming chair for the price?
A: Three key factors: tested by streamers, rated #1 for comfort, costs 40% less than premium brands.

Q: Will this work for tall users?
A: Perfect fit! Designed for users up to 6 feet 5 inches with fully adjustable components that adapt to your body.

Q: How quickly will I notice the comfort difference?
A: Most gamers feel the difference within their first session. Say goodbye to that 2-hour fatigue mark."""
        
        listing.keywords = f"gaming chair, ergonomic chair, gaming chair with footrest for tall users, best gaming chair under $200, gaming chair for back pain relief, comfortable chair for long gaming sessions, gaming chair with lumbar support, {product.brand_name}"

    def _generate_walmart_listing(self, product, listing):
        if not self.client:
            raise Exception("OpenAI API key not configured. Please set a valid OpenAI API key to generate Walmart listings.")
            
        competitor_context = self._get_competitor_context(product)
        
        prompt = f"""You are a Walmart marketplace expert. Create a conversion-optimized Walmart product listing.

PRODUCT INFO:
- Name: {product.name}
- Brand: {product.brand_name}
- Description: {product.description} 
- Brand Tone: {product.brand_tone}
- Features: {product.features}
- Price: ${product.price}
- Generate SEO Keywords automatically based on product details  
- Generate Long-tail Keywords automatically based on product details
- Generate FAQs automatically based on product details
- Generate What is in the Box automatically based on product type
{competitor_context}

WALMART REQUIREMENTS:
- Title: 75 characters max, brand + key features
- Short description: 4000 chars, rich HTML allowed
- Key features: Bullet list of specifications
- Rich media: Video and image suggestions

Return ONLY valid JSON:
{{
  "title": "Brand Name Product Name - Key Feature (under 75 chars)",
  "short_description": "<p>Compelling opening paragraph that hooks the customer...</p><ul><li>Key benefit 1</li><li>Key benefit 2</li></ul>",
  "key_features": [
    "Dimension: X x Y x Z inches",
    "Material: Premium grade materials", 
    "Warranty: X year manufacturer warranty",
    "Certification: Relevant safety certifications"
  ],
  "specifications": {{
    "Brand": "{product.brand_name}",
    "Model": "Product model number",
    "Color": "Available colors",
    "Size": "Dimensions and weight"
  }},
  "rich_media_suggestions": "360-degree product view, unboxing video, lifestyle shots, size comparison",
  "seo_keywords": ["primary keyword", "secondary keyword", "long tail keyword"]
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            listing.title = result.get('title', '')[:500]
            listing.short_description = result.get('short_description', '')
            listing.long_description = result.get('short_description', '')
            listing.walmart_key_features = '\n'.join(result.get('key_features', []))
            listing.walmart_specifications = json.dumps(result.get('specifications', {}))
            listing.keywords = ', '.join(result.get('seo_keywords', []))
        except json.JSONDecodeError:
            listing.title = f"{product.brand_name} {product.name}"
            listing.short_description = "AI generation failed - please regenerate"

    def _generate_etsy_listing(self, product, listing):
        if not self.client:
            raise Exception("OpenAI API key not configured. Please set a valid OpenAI API key to generate Etsy listings.")
            
        prompt = f"""You are an Etsy SEO expert specializing in handmade/vintage items. Create a story-driven Etsy listing.

PRODUCT INFO:
- Name: {product.name}
- Brand: {product.brand_name}
- Description: {product.description}
- Brand Tone: {product.brand_tone} 
- Features: {product.features}
- Generate SEO Keywords automatically based on product details  
- Generate Long-tail Keywords automatically based on product details
- Generate FAQs automatically based on product details
- Generate What is in the Box automatically based on product type

ETSY REQUIREMENTS:
- Title: 140 characters with 13 keywords naturally integrated
- Description: Story-driven, personal, mentions process/materials
- Tags: Exactly 13 tags, highly searched Etsy terms
- Materials: What it is made from
- Personal touch: Artist story, inspiration

Return ONLY valid JSON:
{{
  "title": "Handcrafted [Product] | Unique [Style] | Perfect for [Use Case] | [Material] [Item Type]",
  "description": "**The Story Behind This Piece**\n\nWhen I first dreamed up this [product], I wanted to create something truly special...\n\n**What Makes This Special:**\n• Handcrafted with love and attention to detail\n• Made from premium [materials]\n• Perfect for [specific use cases]\n\n**Care Instructions:**\n[How to maintain the product]\n\n**Shipping & Policies:**\n[Shipping timeline and shop policies]",
  "tags": ["handmade jewelry", "boho necklace", "gift for her", "artisan made", "unique design", "natural stone", "bohemian style", "statement piece", "handcrafted", "one of a kind", "spiritual jewelry", "healing crystal", "custom jewelry"],
  "materials": ["Sterling silver", "Natural gemstones", "Organic cotton cord"],
  "sections": {{
    "story": "Personal inspiration and creation process",
    "features": "Unique qualities and benefits", 
    "care": "How to maintain and store",
    "shipping": "Processing time and shipping details"
  }},
  "seo_focus": "Long-tail keywords that Etsy buyers actually search for"
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=1500
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            listing.title = result.get('title', '')[:500]
            listing.long_description = result.get('description', '')
            listing.etsy_tags = ', '.join(result.get('tags', [])[:13])
            listing.etsy_materials = ', '.join(result.get('materials', []))
            listing.keywords = ', '.join(result.get('tags', []))
        except json.JSONDecodeError:
            listing.title = f"Handmade {product.name} by {product.brand_name}"
            listing.long_description = "AI generation failed - please regenerate"

    def _generate_tiktok_listing(self, product, listing):
        if not self.client:
            raise Exception("OpenAI API key not configured. Please set a valid OpenAI API key to generate TikTok listings.")
            
        prompt = f"""You are a viral TikTok Shop expert. Create engaging content that converts Gen Z buyers.

PRODUCT INFO:
- Name: {product.name}
- Brand: {product.brand_name}
- Description: {product.description}
- Brand Tone: {product.brand_tone}
- Features: {product.features}
- Price: ${product.price}

TIKTOK REQUIREMENTS:
- Title: Catchy, trending language, under 60 chars
- Description: Casual, engaging, emoji-rich
- Video scripts: 15-30 seconds, viral hooks
- Hashtags: Mix of trending + niche tags
- Gen Z language: authentic, not corporate

Return ONLY valid JSON:
{{
  "title": "This [Product] is Actually Genius ✨",
  "description": "okay but why is nobody talking about this?? 😭 literally game-changing for [use case] and it's only $X 💅\n\n✨ what you get:\n• [benefit with emoji]\n• [benefit with emoji] \n• [benefit with emoji]\n\n#MainCharacterEnergy #ThatGirl",
  "video_scripts": [
    {{
      "hook": "POV: You found the perfect [product] and it's only $X",
      "script": "okay bestie, let me put you on... [15-second explanation with visual demonstrations] literally obsessed ✨",
      "cta": "link in bio before these sell out!"
    }},
    {{
      "hook": "Things that just make sense: [Product name]",
      "script": "[Problem setup] → [Product solution] → [Amazing result] this is why I love the internet",
      "cta": "who else needs this?? 👇"
    }},
    {{
      "hook": "Replying to @user who asked about [product]",
      "script": "[Answer format] here's everything you need to know... [quick demo] hope this helps babe!",
      "cta": "drop more questions below! 💕"
    }}
  ],
  "hashtags": ["#TikTokMadeMeBuyIt", "#MustHave", "#ThatGirl", "#MainCharacter", "#Obsessed", "#GameChanger", "#LinkInBio", "#SmallBusiness"],
  "hooks": [
    "This is your sign to try [product]",
    "POV: You discover the best [category] ever",
    "Things that just make sense:",
    "Obsessed is an understatement"
  ]
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=2000
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            listing.title = result.get('title', '')[:500]
            listing.long_description = result.get('description', '')
            
            scripts = result.get('video_scripts', [])
            script_text = '\n\n---\n\n'.join([f"HOOK: {s.get('hook', '')}\nSCRIPT: {s.get('script', '')}\nCTA: {s.get('cta', '')}" for s in scripts])
            listing.tiktok_video_script = script_text
            
            listing.tiktok_hashtags = ' '.join(result.get('hashtags', []))
            listing.tiktok_hooks = '\n'.join(result.get('hooks', []))
            listing.keywords = ', '.join(result.get('hashtags', []))
        except json.JSONDecodeError:
            listing.title = f"This {product.name} hits different"
            listing.long_description = "AI generation failed - please regenerate"

    def _generate_shopify_listing(self, product, listing):
        if not self.client:
            raise Exception("OpenAI API key not configured. Please set a valid OpenAI API key to generate Shopify listings.")
            
        prompt = f"""You are a Shopify conversion expert. Create a high-converting product page optimized for SEO and sales.

PRODUCT INFO:
- Name: {product.name}
- Brand: {product.brand_name}
- Description: {product.description}
- Brand Tone: {product.brand_tone}
- Features: {product.features}  
- Price: ${product.price}

SHOPIFY REQUIREMENTS:
- SEO Title: 60 characters, keyword-optimized for Google
- Meta Description: 160 chars, compelling with CTA
- Product Description: HTML formatted, conversion-focused
- Alt text: SEO-optimized image descriptions
- Schema markup: Product structured data

Return ONLY valid JSON:
{{
  "seo_title": "Buy [Product] Online | Premium [Category] | Brand Name",
  "meta_description": "Discover the best [product] with [key benefit]. ⭐ Free shipping ⭐ 30-day returns ⭐ Shop now!",
  "product_description": "<div class=\"product-hero\"><h2>Experience the Difference with [Product Name]</h2><p>Transform your [use case] with our premium [product]...</p></div><div class=\"features\"><h3>Why Customers Love This:</h3><ul><li>✓ [Feature 1]: [Benefit]</li><li>✓ [Feature 2]: [Benefit]</li></ul></div><div class=\"guarantee\"><h3>Our Promise</h3><p>30-day money-back guarantee, free shipping, exceptional customer service.</p></div>",
  "alt_texts": [
    "Premium [product name] shown in [context] - front view",
    "[Brand] [product] detail shot showing [feature]", 
    "[Product] lifestyle image with [usage context]",
    "[Product] size comparison and dimensions"
  ],
  "structured_data": {{
    "name": "[product_name]",
    "brand": "[brand_name]",
    "price": "[product_price]",
    "availability": "InStock",
    "condition": "NewCondition"
  }},
  "conversion_elements": [
    "Social proof section with reviews",
    "Urgency indicators (limited stock, sale timer)",
    "Trust badges (security, guarantees)", 
    "Related products recommendations"
  ]
}}"""

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1500
        )
        
        try:
            result = json.loads(response.choices[0].message.content)
            listing.title = result.get('seo_title', '')[:500]
            listing.shopify_seo_title = result.get('seo_title', '')
            listing.shopify_meta_description = result.get('meta_description', '')
            listing.long_description = result.get('product_description', '')
            listing.keywords = f"{result.get('seo_title', '')}, {result.get('meta_description', '')}"
        except json.JSONDecodeError:
            listing.title = f"Buy {product.name} Online | {product.brand_name}"
            listing.shopify_seo_title = f"{product.name} - Premium Quality"

    def _generate_fallback_walmart(self, product, listing):
        listing.title = f"{product.brand_name} {product.name}"
        listing.short_description = f"<p>{product.description}</p><ul><li>Premium quality</li><li>Great value</li><li>Customer satisfaction guaranteed</li></ul>"
        listing.long_description = listing.short_description
        listing.keywords = f"{product.name}, {product.brand_name}, quality, value"

    def _generate_fallback_etsy(self, product, listing):
        listing.title = f"Handmade {product.name} by {product.brand_name}"
        listing.long_description = f"**Handcrafted with Love**\n\n{product.description}\n\n**What Makes This Special:**\n• Unique design\n• Quality materials\n• Made with care"
        listing.keywords = f"handmade, {product.name}, artisan, unique, {product.brand_name}"

    def _generate_fallback_tiktok(self, product, listing):
        listing.title = f"This {product.name} hits different"
        listing.long_description = f"okay but seriously... {product.description}\n\nwhy you need this:\n• it's actually amazing\n• perfect for daily use\n• great quality\n\n#MustHave #GameChanger"
        listing.keywords = f"{product.name}, viral, trendy, {product.brand_name}"

    def _generate_fallback_shopify(self, product, listing):
        listing.title = f"Buy {product.name} Online | {product.brand_name}"
        listing.long_description = f"<h2>Premium {product.name}</h2><p>{product.description}</p><h3>Features:</h3><ul><li>High quality materials</li><li>Exceptional performance</li><li>Customer satisfaction guaranteed</li></ul>"
        listing.keywords = f"{product.name}, buy online, {product.brand_name}, premium quality"

    def _analyze_product_context(self, product):
        # Analyze product to generate dynamic, product-specific context for AI prompts
        
        # Extract product type and category
        product_name = product.name.lower()
        categories = product.categories.lower() if product.categories else ""
        description = product.description.lower() if product.description else ""
        features = product.features.lower() if product.features else ""
        
        # Determine product type
        product_type = "product"
        if any(term in product_name + categories for term in ['chair', 'seat', 'furniture']):
            product_type = "furniture"
        elif any(term in product_name + categories for term in ['electronic', 'device', 'gadget', 'tech']):
            product_type = "electronics"
        elif any(term in product_name + categories for term in ['clothing', 'apparel', 'wear', 'fashion']):
            product_type = "apparel"
        elif any(term in product_name + categories for term in ['beauty', 'cosmetic', 'skincare', 'makeup']):
            product_type = "beauty"
        elif any(term in product_name + categories for term in ['kitchen', 'cooking', 'utensil', 'appliance']):
            product_type = "kitchen"
        elif any(term in product_name + categories for term in ['fitness', 'exercise', 'workout', 'gym']):
            product_type = "fitness"
        elif any(term in product_name + categories for term in ['home', 'decor', 'garden', 'outdoor']):
            product_type = "home_garden"
        
        # Generate target keywords based on product
        primary_keywords = []
        if 'chair' in product_name:
            primary_keywords = ['chair', 'seating', 'furniture']
        elif any(term in product_name for term in ['laptop', 'computer', 'monitor']):
            primary_keywords = ['computer', 'electronics', 'tech']
        elif any(term in product_name for term in ['shirt', 'dress', 'pants']):
            primary_keywords = ['clothing', 'apparel', 'fashion']
        else:
            # Extract first significant word as primary keyword
            words = product_name.split()
            primary_keywords = [words[0]] if words else ['product']
        
        # Generate pain points based on product type
        pain_points = {
            "furniture": ["discomfort", "poor quality", "difficult assembly", "back pain", "durability issues"],
            "electronics": ["slow performance", "poor battery life", "connectivity issues", "overheating", "compatibility problems"],
            "apparel": ["poor fit", "low quality fabric", "fading colors", "uncomfortable", "sizing issues"],
            "beauty": ["skin irritation", "ineffective results", "harsh chemicals", "drying", "allergic reactions"],
            "kitchen": ["difficult cleaning", "poor durability", "inefficient", "space consuming", "safety concerns"],
            "fitness": ["injury risk", "poor results", "uncomfortable", "space limitations", "motivation issues"],
            "home_garden": ["maintenance difficulty", "weather damage", "poor aesthetics", "space limitations", "cost efficiency"]
        }.get(product_type, ["poor quality", "high price", "ineffective", "durability issues"])
        
        # Generate benefit focus based on product type
        benefit_focus = {
            "furniture": ["comfort", "durability", "ergonomic support", "easy assembly", "space efficiency"],
            "electronics": ["performance", "reliability", "connectivity", "user-friendly", "energy efficiency"],
            "apparel": ["perfect fit", "premium quality", "style", "comfort", "versatility"],
            "beauty": ["effective results", "gentle formula", "natural ingredients", "anti-aging", "skin health"],
            "kitchen": ["efficiency", "durability", "easy cleaning", "safety", "space-saving"],
            "fitness": ["effective workouts", "safety", "convenience", "results", "motivation"],
            "home_garden": ["low maintenance", "weather resistance", "aesthetic appeal", "space optimization", "value"]
        }.get(product_type, ["quality", "value", "effectiveness", "convenience", "satisfaction"])
        
        # Build context string
        price_tier = 'premium' if float(product.price or 0) > 100 else 'value' if float(product.price or 0) > 50 else 'budget'
        primary_kw = primary_keywords[0] if primary_keywords else 'product'
        
        context = f"PRODUCT-SPECIFIC GUIDANCE:\n"
        context += f"- Product Type: {product_type.title()}\n"
        context += f"- Primary Keywords to Use: {', '.join(primary_keywords)}\n"
        context += f"- Target Pain Points: {', '.join(pain_points[:3])}\n"
        context += f"- Key Benefits to Highlight: {', '.join(benefit_focus[:3])}\n"
        context += f"- Price Point Context: ${product.price or '0'} - position as {price_tier} option\n\n"
        context += f"CUSTOMIZATION REQUIREMENTS:\n"
        context += f"- TITLE: Use {primary_kw} as primary keyword, highlight main benefit\n"
        context += f"- BULLETS: Address pain points with benefits\n"
        context += f"- KEYWORDS: Build around {primary_kw}, {product_type}, and product-specific terms\n"
        context += f"- A+ CONTENT: Focus on {product_type} use cases and benefits"
        
        return context

    def _get_competitor_context(self, product):
        if not product.competitor_urls:
            return ""
        
        urls = [url.strip() for url in product.competitor_urls.split(',') if url.strip()]
        if urls:
            return f"\nCOMPETITOR ANALYSIS: Differentiate from competitors at {', '.join(urls[:3])}"
        return ""
    
    def _queue_image_generation(self, listing):
        # Queue image generation for the listing
        try:
            from .image_service import ImageGenerationService, CELERY_AVAILABLE
            
            service = ImageGenerationService()
            if CELERY_AVAILABLE:
                from .image_service import generate_all_listing_images
                # Queue the task asynchronously
                generate_all_listing_images.delay(listing.id)
                print(f"Queued image generation for listing {listing.id}")
            else:
                # Generate images synchronously
                print(f"Generating images synchronously for listing {listing.id}")
                service.queue_all_images(listing)
                
        except Exception as e:
            print(f"Error with image generation: {e}")
            # Don't fail the listing generation if image generation fails
            pass

    def _determine_category_tone(self, product):
        # Determine appropriate tone based on product category
        try:
            # Create categories mapping
            categories = product.categories.lower() if product.categories else ""
            name = product.name.lower() if product.name else ""
            description = product.description.lower() if product.description else ""
        except Exception as e:
            print(f"Error in category tone detection: {e}")
            # Fallback to default
            return {
                'tone': 'Confident & Trustworthy',
                'guidelines': 'Professional yet personable, confidence-building. Focus on value and customer satisfaction.'
            }
        
        # Define tone categories
        if any(word in categories + name + description for word in ['home', 'kitchen', 'cleaning', 'appliance', 'tool']):
            return {
                'tone': 'Clean & Professional',
                'guidelines': 'Direct, helpful, solution-focused. Personality: Confident problem-solver. Use phrases like "No more [problem]", "Get it done", "Works like magic". Emphasize efficiency and reliability with energy.'
            }
        elif any(word in categories + name + description for word in ['beauty', 'skincare', 'wellness', 'luxury', 'premium']):
            return {
                'tone': 'Elegant & Premium',
                'guidelines': 'Sophisticated, aspirational, transformational. Personality: Elevated and inspiring. Use phrases like "Elevate your", "Transform into", "Luxurious experience". Include sensory language and confidence-building.'
            }
        elif any(word in categories + name + description for word in ['tech', 'gadget', 'electronic', 'smart', 'digital', 'translation', 'ai']):
            return {
                'tone': 'Playful & Innovative',
                'guidelines': 'Fun, confident, slightly cheeky. Personality: Tech-savvy friend who makes complex simple. Use phrases like "Talk like a local", "Say it like you mean it", "Ready to [outcome]". Balance innovation with accessibility.'
            }
        else:
            return {
                'tone': 'Confident & Trustworthy',
                'guidelines': 'Professional yet personable, confidence-building. Personality: Knowledgeable guide who builds trust. Use phrases like "Master your", "Trusted by", "Ready when you are". Focus on empowerment and reliability.'
            }

    def _select_listing_template(self, product):
        # Select listing template to ensure variety
        try:
            import hashlib
            
            # Use product name hash to ensure consistent but varied template selection
            product_string = f"{product.name or 'default'}{product.brand_name or 'brand'}"
            product_hash = int(hashlib.md5(product_string.encode('utf-8')).hexdigest(), 16)
            template_index = product_hash % 3
        except Exception as e:
            print(f"Error in template selection: {e}")
            # Fallback to first template
            template_index = 0
        
        templates = [
            {
                'name': 'Story-First Template',
                'brand_placement': 'Integrated naturally in middle of title',
                'title_format': '[Transformation/Outcome] – [Brand] [Product] for [Specific Use Case]',
                'description_approach': 'Start with customer story/problem, introduce solution, list benefits with social proof',
                'structure': 'Problem narrative → Solution introduction → Key benefits → Trust elements → Clear CTA'
            },
            {
                'name': 'Feature Cluster Template', 
                'brand_placement': 'Lead with brand for authority',
                'title_format': '[Brand] [Product]: [Primary Benefit] + [Secondary Benefit] for [Target Audience]',
                'description_approach': 'Organized feature groups with bold headers, bullet-friendly format',
                'structure': 'Quick hook → Feature clusters with headers → Compatibility info → Guarantee'
            },
            {
                'name': 'FAQ-First Template',
                'brand_placement': 'End with brand as trust signal',
                'title_format': '[Direct Benefit Statement] [Product] for [Use Case] by [Brand]',
                'description_approach': 'Address common concerns upfront, then dive into benefits and specifications',
                'structure': 'Address main concern → Core benefits → Technical details → Brand trust → Strong close'
            }
        ]
        
        return templates[template_index]
    
    def _comprehensive_emoji_removal(self, result):
        # Remove emojis and unicode symbols from all text fields in the result
        import re
        
        def remove_emojis(text):
            if not isinstance(text, str):
                return text
            
            try:
                # Debug logging
                original_length = len(text)
                has_unicode = any(ord(c) > 127 for c in text)
                self.logger.debug(f"Emoji removal input: {original_length} chars, has Unicode: {has_unicode}")
                
                # AGGRESSIVE ASCII-ONLY conversion - multiple approaches
                
                # Method 1: Direct ASCII encoding
                clean_text = text.encode('ascii', errors='ignore').decode('ascii')
                
                # Method 2: Manual character filtering for printable ASCII only
                clean_text = ''.join(c for c in clean_text if 32 <= ord(c) <= 126)
                
                # Method 3: Remove any remaining problematic patterns
                clean_text = re.sub(r'[^\x20-\x7E]', '', clean_text)
                
                # Method 4: Clean up spaces and formatting
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                
                # Debug logging
                final_length = len(clean_text)
                has_unicode_after = any(ord(c) > 127 for c in clean_text) if clean_text else False
                self.logger.debug(f"Emoji removal output: {final_length} chars, has Unicode: {has_unicode_after}")
                
                return clean_text if clean_text else text.encode('ascii', errors='ignore').decode('ascii')
                
            except Exception as e:
                self.logger.error(f"Emoji removal failed: {e}")
                # Ultimate fallback - just return empty string if all fails
                return ""
        
        def clean_object(obj):
            if isinstance(obj, dict):
                return {key: clean_object(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [clean_object(item) for item in obj]
            elif isinstance(obj, str):
                return remove_emojis(obj)
            else:
                return obj
        
        return clean_object(result)

    def _create_structured_aplus_html(self, aplus_plan, result):
        """Create structured HTML A+ content from JSON data for better display."""
        import json
        try:
            sections_html = []
            
            # Define section order and display names
            section_order = [
                ('hero_section', '🎯 Hero Section'),
                ('features_section', '⭐ Key Features'), 
                ('comparison_section', '🏆 Why Choose This'),
                ('usage_section', '📖 How to Use'),
                ('lifestyle_section', '🌟 Perfect For Your Lifestyle')
            ]
            
            # Generate HTML for each A+ section
            for section_key, display_name in section_order:
                section_data = aplus_plan.get(section_key, {})
                if isinstance(section_data, dict) and section_data:
                    section_title = section_data.get('title', display_name)
                    section_content = section_data.get('content', '')
                    image_requirements = section_data.get('image_requirements', section_data.get('image_suggestion', ''))
                    
                    section_html = f"""
<div class="aplus-section {section_key}">
    <h2 class="section-title">{section_title}</h2>
    <div class="section-content">
        <p>{section_content}</p>
    </div>
    {f'<div class="image-requirements"><h4>📸 Image Requirements:</h4><p class="image-desc">{image_requirements}</p></div>' if image_requirements else ''}
</div>"""
                    sections_html.append(section_html)
            
            # Add PPC Strategy section
            ppc_strategy = result.get('ppcStrategy', {})
            if ppc_strategy:
                ppc_html = f"""
<div class="aplus-section ppc-strategy">
    <h2 class="section-title">💰 PPC Strategy</h2>
    <div class="ppc-content">
        <div class="ppc-campaigns">
            <h4>Campaign Structure:</h4>
            <ul>
                <li><strong>Exact Match:</strong> {', '.join(ppc_strategy.get('exactMatch', {}).get('keywords', []))}</li>
                <li><strong>Phrase Match:</strong> {', '.join(ppc_strategy.get('phraseMatch', {}).get('keywords', []))}</li>
                <li><strong>Target ACOS:</strong> {ppc_strategy.get('exactMatch', {}).get('targetAcos', 'Not specified')}</li>
            </ul>
        </div>
    </div>
</div>"""
                sections_html.append(ppc_html)
            
            # Add Brand Summary section
            brand_summary = result.get('brandSummary', '')
            if brand_summary:
                brand_html = f"""
<div class="aplus-section brand-summary">
    <h2 class="section-title">🏢 Brand Summary</h2>
    <div class="brand-content">
        <p>{brand_summary}</p>
    </div>
</div>"""
                sections_html.append(brand_html)
            
            # Add Keyword Strategy section
            keyword_strategy = result.get('keywordStrategy', '')
            if keyword_strategy:
                keywords_html = f"""
<div class="aplus-section keyword-strategy">
    <h2 class="section-title">🔑 Keyword Strategy</h2>
    <div class="keyword-content">
        <p>{keyword_strategy}</p>
        <h4>Top Competitor Keywords:</h4>
        <p>{result.get('topCompetitorKeywords', 'Analysis of competitive landscape')}</p>
    </div>
</div>"""
                sections_html.append(keywords_html)
            
            # Combine all sections with styling
            full_html = f"""
<style>
.aplus-container {{
    font-family: Arial, sans-serif;
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}}
.aplus-section {{
    margin-bottom: 30px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    padding: 20px;
    background: #fafafa;
}}
.section-title {{
    color: #232f3e;
    border-bottom: 2px solid #ff9900;
    padding-bottom: 10px;
    margin-bottom: 15px;
}}
.section-content {{
    line-height: 1.6;
    margin-bottom: 15px;
}}
.image-requirements {{
    background: #fff;
    padding: 15px;
    border-left: 4px solid #ff9900;
    margin-top: 15px;
}}
.image-desc {{
    font-size: 14px;
    color: #555;
    margin: 0;
}}
.ppc-content ul {{
    margin: 10px 0;
    padding-left: 20px;
}}
.keyword-content h4 {{
    margin-top: 15px;
    color: #232f3e;
}}
</style>

<div class="aplus-container">
    <h1 style="text-align: center; color: #232f3e; margin-bottom: 30px;">🎨 Complete A+ Content Strategy</h1>
    {''.join(sections_html)}
</div>"""
            
            return full_html
            
        except Exception as e:
            self.logger.error(f"Error creating structured A+ HTML: {e}")
            # Fallback to JSON if HTML creation fails
            comprehensive_strategy = {
                'aPlusContentPlan': aplus_plan,
                'ppcStrategy': result.get('ppcStrategy', {}),
                'keywordStrategy': result.get('keywordStrategy', ''),
                'topCompetitorKeywords': result.get('topCompetitorKeywords', ''),
                'brandSummary': result.get('brandSummary', '')
            }
            return json.dumps(comprehensive_strategy, indent=2)