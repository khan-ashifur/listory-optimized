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
        
        # Generate dynamic, human-centered prompt with heavy anti-template randomization
        import random
        
        # Create radical variation systems to prevent templating
        
        # Random emotional hooks (rotate these to prevent repetition)
        emotional_hooks = [
            "Think about the last time you felt genuinely satisfied with a purchase",
            "Imagine if this one change could shift your entire daily experience", 
            "What if I told you there's something you've been missing without even knowing it",
            "Here's the thing nobody talks about with these products",
            "You know that feeling when something just works perfectly",
            "Most people don't realize this, but there's a huge difference between",
            "Ever notice how some products just feel right from the moment you use them",
            "There's something almost magical about finding the perfect solution",
            "Picture this: it's six months from now and you're wondering why you waited so long"
        ]
        
        # Random conversation starters (completely different each time)
        conversation_starters = [
            "Let me tell you why this caught my attention",
            "So here's what makes this different from everything else",
            "I'll be honest - I was skeptical at first, but",
            "You know what surprised me most about this",
            "Can we talk about something for a minute",
            "I've been thinking about this lately",
            "Here's something interesting I discovered",
            "Want to know what changed my mind about these"
        ]
        
        # Random personality quirks (inject humanity)
        personality_elements = [
            "and honestly, it's kind of addictive",
            "which, let's be real, is exactly what we need",
            "and yes, I know how that sounds",
            "trust me on this one",
            "and I'm not just saying that",
            "which sounds dramatic but isn't",
            "and here's the kicker",
            "plot twist:",
            "spoiler alert:"
        ]
        
        # Random structural approaches (break the template)
        structure_variants = [
            "story_first", "problem_discovery", "benefit_reveal", "comparison_natural", 
            "personal_testimonial", "technical_curiosity", "lifestyle_integration", "surprise_factor"
        ]
        
        # Randomly select elements to inject variety
        chosen_hook = random.choice(emotional_hooks)
        chosen_starter = random.choice(conversation_starters)
        chosen_personality = random.choice(personality_elements)
        chosen_structure = random.choice(structure_variants)
        
        # Anti-template instructions based on tone
        tone_style = product.brand_tone.lower()
        
        # Create completely different writing approaches for each brand tone
        tone_specific_prompts = {
            'professional': f"""
WRITE AS A HUMAN EXPERT, NOT A MARKETING ROBOT

You're a respected professional who genuinely knows this field. Your job is to write like you're personally recommending this to a colleague, not creating marketing copy.

CRITICAL ANTI-ROBOT RULES:
❌ NEVER use "revolutionary", "game-changing", "cutting-edge", "state-of-the-art"
❌ NEVER start with brand name in title unless it naturally fits
❌ NEVER use the same bullet structure as other products
❌ NEVER start description with "Are you tired of..." or "Experience the..."
❌ NEVER use "**FEATURE NAME:**" format in bullets

HUMAN WRITING APPROACH:
✅ Write like you're explaining to a smart colleague
✅ Use specific, unusual details that show you actually understand the product
✅ Include subtle professional insights that only an expert would know
✅ Vary sentence structure dramatically - mix very short and longer explanations
✅ Use unexpected but professional language

TODAY'S EMOTIONAL HOOK: "{chosen_hook}"
TODAY'S CONVERSATION STARTER: "{chosen_starter}"
PERSONALITY ELEMENT TO INCLUDE: "{chosen_personality}"
STRUCTURAL APPROACH: "{chosen_structure}"

TITLE VARIATION: Create something that sounds like a professional wrote it, not a marketing team
BULLET VARIATION: Write each bullet completely differently - some short, some detailed, varied formats
DESCRIPTION VARIATION: Tell the story from a professional's perspective, not marketing copy
""",
            
            'casual': f"""
WRITE LIKE A REAL FRIEND WHO FOUND SOMETHING AMAZING

You're that friend who discovers cool stuff and can't wait to share it. Write like you're texting someone you care about, not creating an ad.

CRITICAL ANTI-ROBOT RULES:
❌ NEVER use "game-changer", "life-saver", "must-have"
❌ NEVER start bullets with "MAKES LIFE EASIER:" or similar templates
❌ NEVER use the same casual phrases everyone uses
❌ NEVER sound like you're trying to sell something
❌ NEVER use forced enthusiasm

HUMAN FRIEND APPROACH:
✅ Write like you're actually excited about this thing
✅ Use specific, quirky details that make it feel real
✅ Include slightly imperfect, conversational language
✅ Share it like you'd tell a story to a friend
✅ Use casual language that doesn't sound forced

TODAY'S EMOTIONAL HOOK: "{chosen_hook}"
TODAY'S CONVERSATION STARTER: "{chosen_starter}"
PERSONALITY ELEMENT TO INCLUDE: "{chosen_personality}"
STRUCTURAL APPROACH: "{chosen_structure}"

TITLE VARIATION: Write it like a casual recommendation, not marketing copy
BULLET VARIATION: Each bullet should sound completely different - some chatty, some quick, varied styles
DESCRIPTION VARIATION: Tell it like you're sharing a personal discovery with a friend
""",
            
            'luxury': f"""
WRITE AS A SOPHISTICATED CONNOISSEUR, NOT A LUXURY SALES PERSON

You appreciate true quality and understand what makes something genuinely exceptional. Write like you're sharing a rare discovery with someone who appreciates fine things.

CRITICAL ANTI-ROBOT RULES:
❌ NEVER use "exquisite", "handcrafted", "premium experience", "discerning"
❌ NEVER start with "for the discerning" or "exclusive collection"
❌ NEVER use obvious luxury buzzwords
❌ NEVER sound pretentious or trying-too-hard
❌ NEVER use "EXCEPTIONAL CRAFTSMANSHIP:" bullet format

SOPHISTICATED HUMAN APPROACH:
✅ Write with quiet confidence about genuine quality
✅ Use subtle language that shows real appreciation for quality
✅ Include specific details that only someone who knows quality would notice
✅ Let the quality speak for itself without shouting about it
✅ Use refined but not pretentious language

TODAY'S EMOTIONAL HOOK: "{chosen_hook}"
TODAY'S CONVERSATION STARTER: "{chosen_starter}"
PERSONALITY ELEMENT TO INCLUDE: "{chosen_personality}"
STRUCTURAL APPROACH: "{chosen_structure}"

TITLE VARIATION: Something that quietly suggests quality without screaming luxury
BULLET VARIATION: Each should demonstrate quality through specific details, not declarations
DESCRIPTION VARIATION: Show appreciation for quality through informed perspective
""",
            
            'playful': f"""
WRITE WITH GENUINE CREATIVITY, NOT FORCED ENTHUSIASM

You're naturally creative and see fun possibilities everywhere. Write like you're sharing something that genuinely delights you, not trying to be quirky.

CRITICAL ANTI-ROBOT RULES:
❌ NEVER use "seriously cool", "totally awesome", "mind-blowing", "game-changer"
❌ NEVER start bullets with "TOTALLY AWESOME:" or similar
❌ NEVER force quirky comparisons that don't fit
❌ NEVER sound like you're trying too hard to be fun
❌ NEVER use obviously playful templates

GENUINELY CREATIVE APPROACH:
✅ Find unexpected but fitting ways to describe things
✅ Use creativity that flows naturally from the product
✅ Include surprising details that make people smile
✅ Let your natural creativity show without forcing it
✅ Write with energy that feels authentic

TODAY'S EMOTIONAL HOOK: "{chosen_hook}"
TODAY'S CONVERSATION STARTER: "{chosen_starter}"
PERSONALITY ELEMENT TO INCLUDE: "{chosen_personality}"
STRUCTURAL APPROACH: "{chosen_structure}"

TITLE VARIATION: Something creative that fits the product naturally
BULLET VARIATION: Each should surprise in a different way - some clever, some simple, varied approaches
DESCRIPTION VARIATION: Share the creative possibility in a way that feels natural
""",
            
            'minimal': f"""
WRITE WITH PURPOSEFUL CLARITY, NOT STRIPPED-DOWN MARKETING

You understand that the best things are simple and clear. Write like someone who values substance over style and knows what really matters.

CRITICAL ANTI-ROBOT RULES:
❌ NEVER use "essential", "simply better", "pure", "refined"
❌ NEVER use "CLEAR BENEFIT:" bullet format
❌ NEVER artificially strip away all personality
❌ NEVER sound cold or robotic in pursuit of minimalism
❌ NEVER use obvious minimal buzzwords

THOUGHTFUL SIMPLICITY APPROACH:
✅ Say exactly what needs to be said, nothing more
✅ Use clear language that gets to the point
✅ Include only details that truly matter
✅ Let simplicity emerge from clarity, not force it
✅ Write with calm confidence in the essentials

TODAY'S EMOTIONAL HOOK: "{chosen_hook}"
TODAY'S CONVERSATION STARTER: "{chosen_starter}"
PERSONALITY ELEMENT TO INCLUDE: "{chosen_personality}"
STRUCTURAL APPROACH: "{chosen_structure}"

TITLE VARIATION: Clear and direct without unnecessary words
BULLET VARIATION: Each should be as long as it needs to be - some short, some longer, all clear
DESCRIPTION VARIATION: Focus on what matters most, explained clearly
""",
            
            'bold': f"""
WRITE WITH AUTHENTIC CONFIDENCE, NOT MARKETING HYPERBOLE

You believe strongly in what you're sharing and aren't afraid to make confident claims you can back up. Write like someone with genuine conviction, not a salesperson.

CRITICAL ANTI-ROBOT RULES:
❌ NEVER use "revolutionary", "breakthrough", "destroys", "shatters", "unleashes"
❌ NEVER start bullets with "BREAKTHROUGH POWER:" or similar
❌ NEVER use obvious bold/power buzzwords
❌ NEVER sound like you're compensating with volume
❌ NEVER use dramatic language that doesn't fit the product

GENUINELY CONFIDENT APPROACH:
✅ Make strong claims that you can actually support
✅ Use confident language that feels earned, not manufactured
✅ Include specific evidence for your bold statements
✅ Let your conviction show through substance, not adjectives
✅ Write with power that comes from genuine belief

TODAY'S EMOTIONAL HOOK: "{chosen_hook}"
TODAY'S CONVERSATION STARTER: "{chosen_starter}"
PERSONALITY ELEMENT TO INCLUDE: "{chosen_personality}"
STRUCTURAL APPROACH: "{chosen_structure}"

TITLE VARIATION: Confident but specific, not generically bold
BULLET VARIATION: Each should demonstrate confidence in different ways - some direct, some detailed
DESCRIPTION VARIATION: Show conviction through evidence and specific benefits
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
        
        # Create truly randomized product insights to prevent templating
        product_category = product.categories.split(',')[0].strip() if product.categories else "product"
        
        # Generate completely unique content approaches based on product analysis
        features_list = [f.strip() for f in product.features.split(',') if f.strip()] if product.features else []
        
        # Random content focus areas (rotate to prevent similarity)
        content_focus_options = [
            "unexpected_benefit", "specific_use_case", "problem_solving", "lifestyle_enhancement",
            "technical_advantage", "emotional_satisfaction", "practical_convenience", "unique_approach"
        ]
        chosen_focus = random.choice(content_focus_options)
        
        # Random title approaches (completely different each time)
        title_approaches = [
            "benefit_led", "problem_solution", "category_specific", "user_focused", 
            "feature_highlight", "outcome_driven", "comparison_based", "story_driven"
        ]
        chosen_title_approach = random.choice(title_approaches)
        
        # Random FAQ styles (break the Q&A template)
        faq_styles = [
            "conversational_honest", "technical_explained_simply", "comparison_focused", 
            "concern_addressing", "story_based", "practical_focused"
        ]
        chosen_faq_style = random.choice(faq_styles)

        # Now create the completely new human-focused prompt
        prompt = f"""
{base_prompt}

PRODUCT INFORMATION:
- Product: {product.name}
- Brand: {product.brand_name}
- Category: {product_category}
- Description: {product.description}
- Features: {', '.join(features_list) if features_list else 'Not specified'}
- Price: ${product.price if product.price else 'Not specified'}

RANDOMIZATION ELEMENTS FOR TODAY:
- Content Focus: {chosen_focus}
- Title Approach: {chosen_title_approach}  
- FAQ Style: {chosen_faq_style}
- Variety Emphasis: {variety_elements[0]}

YOUR MISSION: Write an Amazon listing that sounds like a real human expert wrote it. Each section should feel completely different from typical Amazon listings.

CRITICAL KEYWORD REQUIREMENTS:
- Generate EXACTLY 10-12 SHORT keywords (1-2 words): headphones, earbuds, bluetooth, wireless, audio, music, etc.
- Generate EXACTLY 25 LONG keywords (3+ words): noise cancelling wireless earbuds, bluetooth headphones for exercise, etc.
- Generate 15+ backend keywords (comprehensive search terms, misspellings, synonyms)
- Frontend displays keywords ≤2 words as "short-tail" and >2 words as "long-tail"
- TOTAL TARGET: 35+ keywords (10-12 short + 25 long)

CRITICAL JSON FORMATTING RULES:
1. ALL JSON field values MUST use double quotes (") not single quotes (')
2. INSIDE content text, use single quotes for contractions: dont, cant, wont, its  
3. NEVER use unescaped double quotes inside content text
4. JSON structure: {{"field": "content with single quotes inside"}}
5. Test your JSON structure before submitting
6. CORRECT: {{"title": "This is Johns favorite product"}}
7. WRONG: {{'title': 'This is Johns favorite product'}}

RESPONSE FORMAT: Return valid JSON with these fields (note the double quotes around all field names and values):

{{
  "productTitle": "Write 150-200 character Amazon-optimized title. MUST include: 1) Brand name '{product.brand_name}' at start, 2) Emotional hook or benefit, 3) Primary keywords (product type, main features), 4) Key specifications. Format: '{product.brand_name} [Emotional Hook] [Product Type] [Key Features] [Target Use/Benefit]'. Optimize for both PC and mobile Amazon search. Example: 'AudioMax Premium Wireless Noise Cancelling Bluetooth Headphones - Experience Studio-Quality Sound with 30Hr Battery for Travel, Work & Music'",
  
  "bulletPoints": [
    "EMOTIONAL LABEL: Write 150-500 characters with compelling emotional hook and specific benefit. Use format 'LABEL: detailed explanation with benefits and outcomes.' Must be minimum 150 characters.",
    "DIFFERENT LABEL: Write 150-500 characters with completely different label style. Mix features with emotional outcomes. Use format 'LABEL: comprehensive details.' Must be minimum 150 characters.",
    "UNIQUE LABEL: Write 150-500 characters with creative but relevant label. Focus on customer transformation or specific use case. Use format 'LABEL: rich detail with examples.' Must be minimum 150 characters.", 
    "COMPELLING LABEL: Write 150-500 characters with benefit-focused label. Include specific details, social proof, or technical advantages. Use format 'LABEL: detailed explanation.' Must be minimum 150 characters.",
    "STANDOUT LABEL: Write 150-500 characters with memorable label that captures attention. Add guarantee, uniqueness, or surprising benefit. Use format 'LABEL: comprehensive detail.' Must be minimum 150 characters."
  ],
  
  "productDescription": "Write this like you're personally recommending it. Start with '{chosen_starter}' and include '{chosen_personality}' naturally. Use the {chosen_structure} approach. Avoid the tired 'Are you tired of...' opening and 'Experience the...' language. Write 3 paragraphs that flow like human conversation.",
  
  "aPlusContentPlan": {{
    "hero_section": {{
      "title": "Write a compelling headline that fits the product naturally",
      "content": "2-3 sentences that feel authentic to your tone",
      "image_requirements": "Describe what image would genuinely help sell this product. Be specific about composition, setting, and mood but let it flow from the product's actual use case."
    }},
    "features_section": {{
      "title": "Create your own section title - doesn't have to be 'Key Features'",
      "content": "Explain the most important aspects in your authentic voice",
      "image_requirements": "Describe visual elements that would actually be helpful for this specific product. Focus on what customers really need to see."
    }},
    "comparison_section": {{
      "title": "Your comparison title that fits the product",
      "content": "Natural comparison in your voice",
      "image_requirements": "What visual comparison would actually help customers choose this product over alternatives?"
    }},
    "usage_section": {{
      "title": "Usage section title in your style",
      "content": "How to use/when to use in natural language",
      "image_requirements": "What images would actually help someone use this product successfully?"
    }},
    "lifestyle_section": {{
      "title": "Lifestyle section that fits the product's actual use",
      "content": "How this fits into real life, not forced lifestyle marketing",
      "image_requirements": "Real lifestyle scenarios where this product actually makes sense, not stock photo situations."
    }},
    "aplus_content_suggestions": {{
      "title": "Content Enhancement Suggestions",
      "content": "Specific suggestions for additional A+ content that would enhance this listing, including video content, comparison charts, technical specifications, customer testimonials integration, seasonal use cases, and maintenance/care instructions that would genuinely help customers.",
      "image_requirements": "Additional image types that would complete the customer's understanding of this product - technical diagrams, size comparisons, packaging contents, warranty information visuals, or instructional graphics."
    }}
  }},
  
  "brandSummary": "Write 200-400 characters about the brand like you actually know something about them. Include brand history, values, customer focus, product quality commitment, and what makes {product.brand_name} different from competitors. Make it feel authentic and detailed, not generic brand-speak.",
  
  "backendKeywords": "Write 240+ characters of actual search terms people might use. Include synonyms, related products, problem keywords, and variations. Make it comprehensive but real.",
  
  "topCompetitorKeywords": "What keywords would actually compete with this product?",
  
  "keywordStrategy": "Explain your keyword approach like you're talking to someone who knows marketing.",
  
  "ppcStrategy": {{
    "campaign_structure": "Detailed campaign organization with Auto, Exact, Phrase, and Broad campaigns for this specific product category",
    "exactMatch": {{
      "keywords": ["Minimum 8 actual exact match keywords for this specific product including brand + product type, specific model names, and high-intent terms"],
      "bidRange": "$0.75-1.25",
      "targetAcos": "20%",
      "dailyBudget": "$25-50"
    }},
    "phraseMatch": {{
      "keywords": ["Minimum 10 real phrase match keywords that make sense for this product category and target audience"],
      "bidRange": "$0.50-0.85", 
      "targetAcos": "30%",
      "dailyBudget": "$15-30"
    }},
    "broadMatch": {{
      "keywords": ["5-8 broad match keywords for discovery and reaching new customers"],
      "bidRange": "$0.30-0.65",
      "targetAcos": "35%",
      "dailyBudget": "$10-20"
    }},
    "negativeKeywords": ["Comprehensive list of negative keywords specific to this product category to avoid irrelevant traffic"],
    "targeting_strategy": "Detailed explanation of audience targeting, competitor targeting, and ASIN targeting specific to this product",
    "optimization_schedule": "Specific timeline for bid adjustments, keyword harvesting, and performance optimization"
  }},
  
  "keyword_cluster": {{
    "primary_keywords": ["Minimum 10 short keywords (1-2 words each) like: earbuds, headphones, bluetooth, wireless, audio, music, plus 2-3 brand/product terms"],
    "secondary_keywords": ["Generate EXACTLY 25 longer descriptive keywords (3+ words) with genuine search intent including problem-solving terms, specific use cases, detailed product descriptions, competitor alternatives, and niche applications"],
    "backend_search_terms": "240+ characters of comprehensive search terms including misspellings, synonyms, alternative product names, related accessories, and problem keywords",
    "misspellings_and_synonyms": ["Common misspellings and alternative terms customers might use when searching for this product"],
    "ppc_keywords": [
      {{"keyword": "real high-volume keyword", "match_type": "Exact", "bid": "0.75"}},
      {{"keyword": "another high-intent keyword", "match_type": "Phrase", "bid": "0.65"}},
      {{"keyword": "broad discovery keyword", "match_type": "Broad", "bid": "0.45"}},
      {{"keyword": "brand + product keyword", "match_type": "Exact", "bid": "0.80"}},
      {{"keyword": "problem-solving keyword", "match_type": "Phrase", "bid": "0.60"}},
      {{"keyword": "competitor alternative keyword", "match_type": "Phrase", "bid": "0.70"}},
      {{"keyword": "feature-specific keyword", "match_type": "Exact", "bid": "0.85"}},
      {{"keyword": "use-case keyword", "match_type": "Broad", "bid": "0.50"}}
    ]
  }}
}}"""        
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
                            {"role": "system", "content": "You are a creative copywriting expert who writes like a real human, not a marketing robot. CRITICAL: Return ONLY valid JSON - no markdown, no explanations, just pure JSON that parses correctly. JSON RULES: All field names and values must use double quotes, inside content use single quotes for contractions (dont, cant, wont, its), never use unescaped double quotes in content. CORRECT FORMAT: {\"field\": \"content with 'single quotes' inside\"}. Your mission is to break every predictable Amazon listing pattern and create content that sounds genuinely human and emotionally varied while maintaining perfect JSON formatting. Write each section in a completely different style and tone. Use unexpected but authentic language that fits the product. Vary everything - sentence length, structure, personality, approach. Sound like a real person who genuinely knows and likes this product. Include human quirks and conversational elements. Your goal is to create listings so human and varied that customers feel like theyre talking to a real expert, not reading marketing copy."},
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
                ('lifestyle_section', '🌟 Perfect For Your Lifestyle'),
                ('aplus_content_suggestions', '💡 A+ Content Suggestions')
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