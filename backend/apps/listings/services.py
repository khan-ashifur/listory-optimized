import json
import time
import re
from django.conf import settings
from .models import GeneratedListing, KeywordResearch
from apps.core.models import Product


class ListingGeneratorService:
    def __init__(self):
        try:
            print(f"[SERVICE INIT] Checking OpenAI configuration...")
            print(f"[SERVICE INIT] API Key exists: {bool(settings.OPENAI_API_KEY)}")
            
            # Check if OpenAI key is set and valid
            if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your-openai-api-key-here":
                print("WARNING: OpenAI API key not properly configured!")
                print("Please set your real OpenAI API key in the .env file")
                self.client = None
            elif not settings.OPENAI_API_KEY.startswith('sk-'):
                print("WARNING: Invalid OpenAI API key format!")
                print("OpenAI keys should start with 'sk-'")
                self.client = None
            else:
                # Use new OpenAI client
                from openai import OpenAI
                print(f"[SERVICE INIT] Creating OpenAI client with key starting: {settings.OPENAI_API_KEY[:10]}...")
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                print("OpenAI client initialized successfully - AI generation enabled!")
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
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
        print(f"\n=== GENERATING AMAZON LISTING FOR {product.name} ===")
        print(f"OpenAI client status: {'AVAILABLE' if self.client else 'NOT AVAILABLE'}")
        
        if not self.client:
            print("[ERROR] OpenAI client is None - using fallback content")
            print(f"API Key exists: {bool(settings.OPENAI_API_KEY)}")
            if settings.OPENAI_API_KEY:
                print(f"API Key starts with 'sk-': {settings.OPENAI_API_KEY.startswith('sk-') if settings.OPENAI_API_KEY else False}")
            raise Exception("OpenAI API key not configured. Please set your OPENAI_API_KEY in the .env file to generate AI content.")
            
        competitor_context = self._get_competitor_context(product)
        
        # Generate product-specific keywords and context
        product_context = self._analyze_product_context(product)
        
        # Temporarily use static defaults to avoid OSError
        category_tone = {
            'tone': 'Playful & Innovative',
            'guidelines': 'Fun, confident, slightly cheeky. Personality: Tech-savvy friend who makes complex simple. Use phrases like "Talk like a local", "Say it like you mean it", "Ready to [outcome]". Balance innovation with accessibility.'
        }
        template_style = {
            'name': 'Story-First Template',
            'brand_placement': 'Integrated naturally in middle of title',
            'title_format': '[Transformation/Outcome] – [Brand] [Product] for [Specific Use Case]',
            'description_approach': 'Start with customer story/problem, introduce solution, list benefits with social proof',
            'structure': 'Problem narrative → Solution introduction → Key benefits → Trust elements → Clear CTA'
        }
        
        # Advanced SEO + AEO optimized prompt with dynamic templates and tones
        prompt = f"""Create a comprehensive Amazon listing for {product.name} by {product.brand_name} using the specified TONE and TEMPLATE to avoid repetitive AI-generated content.

PRODUCT DETAILS:
- Name: {product.name}
- Brand: {product.brand_name} 
- Categories: {product.categories}
- Description: {product.description}
- Price: ${product.price}
- Features: {product.features}
- Target Keywords: {product.target_keywords}
- Generate SEO Keywords automatically based on product details  
- Generate Long-tail Keywords automatically based on product details
- Generate FAQs automatically based on product details
- Generate What's in the Box automatically based on product type
- ASSIGNED TONE: {category_tone['tone']}
- ASSIGNED TEMPLATE: {template_style['name']}

🎯 CRITICAL ANTI-REPETITION RULES:
1. AVOID generic phrases like "Feel Empowered", "Effortless Efficiency", "Experience unparalleled"
2. NO robotic all-caps headers
3. VARY sentence structure and length dramatically
4. Write like a human copywriter, not AI
5. Brand placement must feel natural, not tacked on

🎯 TONE GUIDELINES:
{category_tone['guidelines']}

🎯 TEMPLATE STRUCTURE:
{template_style['structure']}

🎯 TITLE REQUIREMENTS - AMAZON STANDARD:
- Lead with transformation/energy, NOT product labels
- Add personality that matches the tone (fun, confident, aspirational)
- Brand placement: {template_style['brand_placement']}
- Format: {template_style['title_format']}
- Include hook words: "Talk Like", "Say It Like", "Ready to", "Master"
- AMAZON LIMIT: Maximum 200 characters total (strictly enforced)
- Include primary keywords and key benefits within character limit
- Examples: "🌍 Talk Like a Local", "Say It Like You Mean It", "Ready to [outcome]"

🎯 BULLET POINTS - AMAZON STANDARD LENGTH:
- MUST use format: "LABEL: Detailed benefit explanation with comprehensive information"
- AMAZON LIMIT: Each bullet point maximum 1000 characters (use full length for rich content)
- Start with powerful benefit labels: "INSTANT CONFIDENCE:", "NO MORE PANIC:", "PERFECT FOR:"
- Provide comprehensive details, specifications, and emotional benefits
- Include use cases, technical details, and reassurance within each bullet
- Add personality that matches assigned tone throughout the full description
- Include keywords naturally without forced repetition
- Examples: 
  * "SPEAK LIKE A LOCAL: Master all 164 languages from Tokyo to Tuscany with real-time translation that works in crowded markets, business meetings, or romantic dinners. No awkward pauses or robotic voices - just natural conversation that builds confidence whether you're ordering authentic ramen or closing international deals."
  * "PRACTICE WITHOUT JUDGMENT: AI chat mode provides patient language practice that adapts to your learning pace, corrects pronunciation gently, and celebrates progress. Perfect for building confidence before your trip or improving skills for career advancement."

🎯 DESCRIPTION STRUCTURE - ADD PERSONALITY & STORYTELLING:
{template_style['description_approach']}
- Start with energy: "🌍 Ready to talk to the world?" / "Tired of [problem]?"
- Tell a story with personality that matches the assigned tone
- Use conversational language: "It's like having a [metaphor] in your [location]"
- Add emotional connection and transformation outcomes
- Break into 3-4 scannable blocks with varied, non-robotic headers
- Use benefit-led transitions: "No more waiting." "Say it. Mean it."
- Include confidence-building language and personality
- Mobile-optimized with shorter sentences and natural flow

🎯 FAQ REQUIREMENTS - NATURAL & FUN TONE:
- Write like a helpful human, not an instruction manual
- Match the assigned tone (playful, professional, premium, etc.)
- Use conversational language: "Just drop them in the case — no cords, no fuss"
- Add personality: "They'll be ready before your passport is"
- Answer real concerns with practical details AND personality
- Avoid robotic responses and forced enthusiasm
- Questions should match natural search queries and voice patterns
- Include confidence-building and reassuring language

CRITICAL: Return ONLY valid JSON. Use this EXACT format with comprehensive keyword categories:
{{
    "title": "🌍 [Energy Hook] – [Brand] [Product] with [Key Benefit] for [Target Use] - AMAZON STANDARD: Maximum 200 characters total",
    "bullet_points": [
        "BENEFIT LABEL: [Comprehensive emotional outcome with detailed explanation, use cases, and personality] - AMAZON STANDARD: Use up to 1000 characters for rich content",
        "ACTION LABEL: [Detailed capability with confidence-building language, specifications, and practical applications] - AMAZON STANDARD: Maximum 1000 characters with full details", 
        "RESULT LABEL: [Specific outcome with personality, technical details, and comprehensive benefits] - AMAZON STANDARD: Up to 1000 characters for complete information",
        "CONFIDENCE LABEL: [Peace of mind with detailed reassurance, certifications, and trust elements] - AMAZON STANDARD: Maximum 1000 characters with comprehensive trust-building",
        "POWER LABEL: [Performance details with specifications, comparisons, and emotional engagement] - AMAZON STANDARD: Use full 1000 character limit for complete value proposition"
    ],
    "long_description": "PERSONALITY STRUCTURE: 1)Energy hook question 2)Storytelling with personality 3)Metaphors and conversational language 4)Confidence-building 5)Strong personality-driven CTA - 2000+ chars with emotional connection",
    "short_tail_keywords": ["primary keyword", "secondary keyword 1", "secondary keyword 2", "category term", "use case keyword", "material/quality term", "brand keyword", "benefit keyword"],
    "long_tail_keywords": ["best [product] for [use case]", "[product] with [feature] for [benefit]", "what is the best [product]", "how to choose [product]", "[brand] [product] reviews"],
    "hero_title": "Compelling headline that captures main benefit and creates urgency",
    "hero_content": "Detailed 300+ character hero section that tells the product story and creates emotional connection",
    "features": [
        "Detailed feature 1 with specific measurements and benefits",
        "Detailed feature 2 with technical specifications and advantages", 
        "Detailed feature 3 with quality materials and construction details",
        "Detailed feature 4 with performance metrics and comparisons",
        "Detailed feature 5 with user experience and convenience factors",
        "Detailed feature 6 with safety and reliability information"
    ],
    "whats_in_box": [
        "Main product with full product name and model",
        "Essential accessory 1 with specific details",
        "Essential accessory 2 with specific details", 
        "Documentation package including user manual and warranty",
        "Premium packaging and gift box if applicable",
        "Additional items or bonuses that add value"
    ],
    "trust_builders": [
        "Best [product] for [use case] - Include exact semantic phrases AI models recognize",
        "Recommended by [#] customers - Use specific numbers for credibility and social proof", 
        "Trusted by [demographic] for [time period] - Target audience validation with timeframe",
        "Works great with [related accessories] - Cross-selling and compatibility signals",
        "Quality certifications and testing standards - Authority and safety validation"
    ],
    "faqs": [
        "Q: What is the best [product] for [primary use case]? A: [Conversational answer with personality] - Match assigned tone, add confidence-building elements",
        "Q: Can I use this [product] for [secondary use case]? A: [Natural spoken answer with metaphor/personality] - Include reassuring and encouraging language",
        "Q: Is this [product] safe for [safety concern]? A: [Trust-building answer with personality] - Add confidence and practical details with tone-appropriate language",
        "Q: How do I [maintain/clean/use] this [product]? A: [Step-by-step with personality] - Like 'Just drop them in the case — no cords, no fuss. Ready before your passport is.'",
        "Q: What makes this [product] better than [competitor type]? A: [Confident answer with personality] - Include unique selling points with assigned tone personality",
        "Q: Does this [product] work with [related item/compatibility]? A: [Compatibility answer with confidence] - Add cross-selling opportunities with personality"
    ],
    "social_proof": "Trusted by [#] globetrotters, language learners, and smooth talkers worldwide - Turn into story/persona with emotional appeal and specific demographics",
    "guarantee": "✈️ Ready to ditch the subtitles and speak freely? [Time period] guarantee with personality-driven CTA - Match assigned tone with confidence-boosting language"
}}

🎯 ADVANCED OPTIMIZATION REQUIREMENTS:

SEO + AEO INTEGRATION:
- Primary keyword density: 2-3% throughout all content
- Include question-based long-tail keywords for voice search
- Use schema-friendly structured data in descriptions  
- Optimize for "People Also Ask" Google queries
- Include related search terms and semantic keywords

CONVERSION PSYCHOLOGY:
- Problem-agitation-solution structure in description
- Social proof with specific numbers and demographics
- Risk reversal through strong guarantees
- Urgency through scarcity or time-sensitive benefits
- Authority through certifications and endorsements

VOICE SEARCH OPTIMIZATION:
- Conversational FAQ format matching spoken queries
- Natural language variations people actually use
- Question starters: "What's the best...", "How do I...", "Can this...", "Is it safe..."
- Local intent keywords where applicable
- Mobile-first readability with shorter sentences

CRITICAL EXECUTION RULES:
1. NO quotes or apostrophes inside JSON string values
2. Every section must include relevant keywords naturally
3. Focus on customer outcomes and transformations
4. Include specific measurements, numbers, and proof points
5. Write for humans first, optimize for machines second
5. FAQs must address real customer concerns
6. Optimize for both desktop and voice search"""        
        print(f"[SUCCESS] OpenAI client is available - proceeding with AI generation")
        try:
            print(f"Generating AI content for {product.name} on Amazon...")
            print(f"Product details: Name={product.name}, Brand={product.brand_name}, Categories={product.categories}")
            print(f"Using product context: {product_context[:200]}...")
            
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
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": f"You are an Amazon listing writer. Create unique, product-specific content for {product.name}. CRITICAL: Return ONLY valid JSON. All strings must be properly quoted. No syntax errors. Use double quotes only."},
                            {"role": "user", "content": prompt}
                        ],
                        functions=[function_schema],
                        function_call={"name": "create_amazon_listing"},
                        temperature=0.5 + (retry_count * 0.1),  # Slightly increase temperature on retries
                        max_tokens=3000,
                        presence_penalty=0.6,
                        frequency_penalty=0.6
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
            # Extract function call result (structured JSON)
            function_call = response.choices[0].message.function_call
            if function_call and function_call.name == "create_amazon_listing":
                ai_content = function_call.arguments
                print(f"AI Function call received: {len(ai_content)} characters")
                try:
                    print(f"Function arguments preview: {ai_content[:500]}...")
                except UnicodeEncodeError:
                    print(f"Function arguments preview: [Unicode content, {len(ai_content)} chars]")
                print("Function calling ensures valid JSON structure")
            else:
                # Fallback to regular content if function calling failed
                ai_content = response.choices[0].message.content or "{}"
                print(f"AI Response received: {len(ai_content)} characters")
                # Use safe encoding for Windows
                safe_preview = ai_content[:300].encode('ascii', errors='ignore').decode('ascii')
                safe_ending = ai_content[-200:].encode('ascii', errors='ignore').decode('ascii')
                print(f"AI Response preview: {safe_preview}...")
                print(f"AI Response ending: ...{safe_ending}")
            
            # First try to parse function args directly - they should be valid JSON
            result = None
            if function_call and function_call.name == "create_amazon_listing":
                try:
                    result = json.loads(ai_content)
                    print("Direct function args parsing successful!")
                    
                    # Clean up any double-quoted values that OpenAI might have added
                    def clean_quoted_values(obj):
                        if isinstance(obj, dict):
                            return {k: clean_quoted_values(v) for k, v in obj.items()}
                        elif isinstance(obj, list):
                            return [clean_quoted_values(item) for item in obj]
                        elif isinstance(obj, str) and obj.startswith('"') and obj.endswith('"'):
                            return obj[1:-1]  # Remove surrounding quotes
                        return obj
                    
                    result = clean_quoted_values(result)
                    print("Cleaned any double-quoted values")
                    # Skip all the cleaning steps since we have valid JSON
                except json.JSONDecodeError as e:
                    print(f"Direct parsing failed: {e}, falling back to cleaning")
                    cleaned_content = ai_content.strip()
            else:
                # For regular content, do the cleaning
                cleaned_content = ai_content.strip()
            
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
                    raise Exception(f"All JSON parsing methods failed. Manual reconstruction error: {str(manual_error)}. Raw content length: {len(cleaned_content)}")
            
            # Validate result has required fields
            required_fields = ["title", "bullet_points", "long_description", "seo_keywords", "hero_title", "hero_content", "features", "whats_in_box", "trust_builders", "faqs", "social_proof", "guarantee"]
            missing_fields = [field for field in required_fields if field not in result]
            if missing_fields:
                print(f"Warning: Missing fields {missing_fields}, adding defaults...")
                defaults = {
                    "title": f"{product.name} - Quality Product",
                    "bullet_points": ["High quality construction", "Reliable performance", "Great value", "Customer satisfaction", "Easy to use"],
                    "long_description": f"The {product.name} by {product.brand_name} offers exceptional quality and performance.",
                    "seo_keywords": {
                        "primary": [product.name.lower(), "quality", "reliable", "performance", "value"],
                        "long_tail": [f"best {product.name.lower()}", f"premium {product.name.lower()}", f"high quality {product.name.lower()}"],
                        "pain_point": ["problem solving", "solution", "fix"],
                        "high_intent": ["buy", "best", "cheap"],
                        "demographic": ["home", "family", "professional"],
                        "brand_terms": [product.brand_name.lower(), f"{product.brand_name.lower()} products", f"{product.brand_name.lower()} quality"]
                    },
                    "hero_title": "Premium Quality",
                    "hero_content": "Experience the difference with our premium product line",
                    "features": ["Quality materials", "Durable construction", "User-friendly design", "Reliable performance"],
                    "whats_in_box": ["Main product", "User manual", "Warranty information", "Support materials"],
                    "trust_builders": ["Quality tested", "Customer approved", "Satisfaction guaranteed"],
                    "faqs": ["Q: Is this product reliable? A: Yes, thoroughly tested for reliability"],
                    "social_proof": "Join thousands of satisfied customers",
                    "guarantee": "100% satisfaction guarantee or your money back"
                }
                for field in missing_fields:
                    result[field] = defaults.get(field, "Content available")
            
            # Simple parsing for JSON structure
            listing.title = result.get('title', '')[:200]  # Amazon allows up to 200 chars
            
            # Get bullet points directly (should be clean from AI)
            bullet_points = result.get('bullet_points', [])
            listing.bullet_points = '\n\n'.join(bullet_points) if bullet_points else ''
            
            listing.long_description = result.get('long_description', '')
            
            # Parse keywords (simple array)
            keywords = result.get('keywords', [])
            if isinstance(keywords, list):
                listing.keywords = ', '.join(keywords)
                listing.amazon_backend_keywords = ', '.join(keywords[:5])
            else:
                listing.keywords = str(keywords) if keywords else ''
                listing.amazon_backend_keywords = str(keywords) if keywords else ''
            
            # Parse A+ content from flat structure
            listing.hero_title = result.get('hero_title', '')
            listing.hero_content = result.get('hero_content', '')
            listing.features = '\n'.join(result.get('features', []))
            listing.whats_in_box = '\n'.join(result.get('whats_in_box', []))
            listing.trust_builders = '\n'.join(result.get('trust_builders', []))
            # Handle FAQs - they might be strings or dictionaries
            faqs = result.get('faqs', [])
            faq_strings = []
            for faq in faqs:
                if isinstance(faq, dict):
                    # If it's a dictionary, format it as Q: A:
                    q = faq.get('question', faq.get('q', ''))
                    a = faq.get('answer', faq.get('a', ''))
                    faq_strings.append(f"Q: {q} A: {a}")
                else:
                    # If it's already a string, use it as is
                    faq_strings.append(str(faq))
            listing.faqs = '\n'.join(faq_strings)
            listing.social_proof = result.get('social_proof', '')
            listing.guarantee = result.get('guarantee', '')
            
            # Create formatted A+ content HTML for display
            # Use the result values directly since listing fields aren't saved yet
            print("Generating A+ content HTML...")
            aplus_html = f"""
<div class="aplus-hero">
    <h2>{result.get('hero_title', '')}</h2>
    <p>{result.get('hero_content', '')}</p>
</div>

<div class="aplus-features">
    <h3>Key Features & Benefits</h3>
    <ul>
""" + '\n'.join([f"        <li>{feature}</li>" for feature in result.get('features', [])]) + f"""
    </ul>
</div>

<div class="aplus-whats-in-box">
    <h3>What's in the Box</h3>
    <ul>
""" + '\n'.join([f"        <li>{item}</li>" for item in result.get('whats_in_box', [])]) + f"""
    </ul>
</div>

<div class="aplus-trust">
    <h3>Trust & Quality</h3>
    <ul>
""" + '\n'.join([f"        <li>{trust}</li>" for trust in result.get('trust_builders', [])]) + f"""
    </ul>
</div>

<div class="aplus-testimonials">
    <h3>Customer Satisfaction</h3>
    <p>{result.get('social_proof', '')}</p>
    <p><strong>Our Guarantee:</strong> {result.get('guarantee', '')}</p>
</div>

<div class="aplus-faqs">
    <h3>Frequently Asked Questions</h3>
""" + '\n'.join([f"    <p><strong>{faq}</strong></p>" for faq in faq_strings]) + f"""
</div>"""
            listing.amazon_aplus_content = aplus_html
            print(f"A+ content HTML set: {len(aplus_html)} characters")
            
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
            
            # Skip the old complex parsing logic by removing this line:
            # bullet_points = result.get('bullet_points', [])
            cleaned_bullets = []
            for bullet in bullet_points:
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
                
                # Fix colon formatting
                cleaned_bullet = cleaned_bullet.replace(':', ' -')
                cleaned_bullet = cleaned_bullet.replace(' - ', ' - ')  # Ensure single dash
                
                # Clean up extra spaces and formatting
                cleaned_bullet = re.sub(r'\s+', ' ', cleaned_bullet).strip()
                
                # Ensure proper text + dash + description format
                if ' - ' not in cleaned_bullet and ':' not in cleaned_bullet:
                    # Try to add dash after first few words
                    parts = cleaned_bullet.split(' ')
                    if len(parts) > 3:
                        cleaned_bullet = ' '.join(parts[:3]) + ' - ' + ' '.join(parts[3:])
                
                cleaned_bullets.append(cleaned_bullet)
            
            listing.bullet_points = '\n\n'.join(cleaned_bullets)
            
            listing.long_description = result.get('long_description', '')
            
            # Parse enhanced SEO keywords structure
            seo_keywords = result.get('seo_keywords', {})
            if isinstance(seo_keywords, dict):
                primary_keywords = seo_keywords.get('primary', [])
                long_tail_keywords = seo_keywords.get('long_tail', [])
                pain_point_keywords = seo_keywords.get('pain_point', [])
                high_intent_keywords = seo_keywords.get('high_intent', [])
                demographic_keywords = seo_keywords.get('demographic', [])
                brand_terms = seo_keywords.get('brand_terms', [])
                
                all_keywords = (primary_keywords + long_tail_keywords + pain_point_keywords + 
                              high_intent_keywords + demographic_keywords + brand_terms)
                listing.keywords = ', '.join(all_keywords) if all_keywords else ''
                # Backend keywords focus on primary and long-tail for better relevancy
                listing.amazon_backend_keywords = ', '.join(primary_keywords + long_tail_keywords)
            else:
                listing.keywords = result.get('keywords', '')
                listing.amazon_backend_keywords = result.get('backend_keywords', '')
            
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
                print(f"   Bullet points: {len(result.get('bullet_points', []))} items")
                print(f"   First bullet: {bullet_points[0] if bullet_points else 'None'}")
            except UnicodeEncodeError:
                print(f"   Title: [Unicode title, {len(listing.title)} chars]")
                print(f"   Bullet points: {len(result.get('bullet_points', []))} items")
                print("   First bullet: [Unicode content]")
            
            # Continue to process A+ content fields
            print(f"   Keywords: {len(keywords)} total")
            
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

You deserve better than settling for average quality. That's where the {product.name} steps in - designed for excellence, built for reliability.

THE QUALITY DIFFERENCE

This isn't just another {product_category}. Our premium design delivers exceptional performance that enhances your daily experience. Feel the difference from the moment you start using it.

WHAT MAKES THIS SPECIAL

Built with attention to detail and quality materials that ensure long-lasting satisfaction. Every aspect designed for users who appreciate superior products - from construction to functionality.

JOIN THOUSANDS OF SATISFIED CUSTOMERS

"Finally, a {primary_keyword} that delivers on its promises" - Verified Customer. Experience why this is rated among the best for quality and performance."""
        
        listing.amazon_backend_keywords = f"{product.name}, {product.brand_name}, {primary_keyword}, premium {product_category}, quality {product_category}, kitchen accessories"
        
        # Enhanced A+ Content with all modules
        listing.amazon_aplus_content = """<div class='aplus-module module1'>
<p><strong>Module Type:</strong> Hero Banner with Text Overlay</p>
<h3>Experience the Gaming Difference</h3>
<p>Transform your gaming setup with professional-grade comfort. Join thousands who've discovered the ultimate gaming chair.</p>
<p><em>Image Requirements: Lifestyle hero shot showing chair in gaming setup with happy gamer</em></p>
</div>

<div class='aplus-module module2'>
<p><strong>Module Type:</strong> 4-Feature Grid with Icons</p>
<h3>Everything You Need for All-Day Gaming</h3>
<p>Ergonomic Support: Perfect posture | Memory Foam: Zero fatigue | Adjustable Design: Custom fit | Premium Build: Lasting durability</p>
</div>"""
        
        # CRITICAL: Add conversion boosters to short_description
        listing.short_description = """WHAT'S IN THE BOX:
• Premium gaming chair with all components
• Assembly hardware and tools
• Detailed setup guide
• Warranty registration card

TRUST & GUARANTEES:
• 2-year manufacturer warranty
• 30-day satisfaction guarantee
• Free shipping and returns
• Certified quality standards

SOCIAL PROOF:
Loved by 10,000+ happy gamers - 4.8 stars average

WHY CHOOSE US:
Vs. other brands: Better ergonomics, superior materials, 40% more affordable than premium competitors

FREQUENTLY ASKED QUESTIONS:

Q: Can I game for 8+ hours without back pain?
A: Absolutely! Our chair was tested by pro gamers during all-nighters. The adjustable lumbar support keeps your spine aligned.

Q: How does this compare to other gaming chairs?
A: Unlike basic gaming chairs, our design includes premium memory foam and 4D armrests. Gamers report 90% less fatigue.

Q: What makes this the best gaming chair for the price?
A: Three key factors: tested by streamers, rated #1 for comfort, costs 40% less than premium brands.

Q: Will this work for tall users?
A: Perfect fit! Designed for users up to 6'5" with fully adjustable components that adapt to your body.

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
- Generate What's in the Box automatically based on product type
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
- Generate What's in the Box automatically based on product type

ETSY REQUIREMENTS:
- Title: 140 characters with 13 keywords naturally integrated
- Description: Story-driven, personal, mentions process/materials
- Tags: Exactly 13 tags, highly searched Etsy terms
- Materials: What it's made from
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
            listing.title = f"This {product.name} hits different ✨"
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
  "product_description": "<div class='product-hero'><h2>Experience the Difference with [Product Name]</h2><p>Transform your [use case] with our premium [product]...</p></div><div class='features'><h3>Why Customers Love This:</h3><ul><li>✓ [Feature 1]: [Benefit]</li><li>✓ [Feature 2]: [Benefit]</li></ul></div><div class='guarantee'><h3>Our Promise</h3><p>30-day money-back guarantee, free shipping, exceptional customer service.</p></div>",
  "alt_texts": [
    "Premium [product name] shown in [context] - front view",
    "[Brand] [product] detail shot showing [feature]", 
    "[Product] lifestyle image with [usage context]",
    "[Product] size comparison and dimensions"
  ],
  "structured_data": {{
    "name": "{product.name}",
    "brand": "{product.brand_name}",
    "price": "{product.price}",
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
        listing.title = f"This {product.name} hits different ✨"
        listing.long_description = f"okay but seriously... {product.description} 💅\n\n✨ why you need this:\n• it's actually amazing\n• perfect for daily use\n• great quality\n\n#MustHave #GameChanger"
        listing.keywords = f"{product.name}, viral, trendy, {product.brand_name}"

    def _generate_fallback_shopify(self, product, listing):
        listing.title = f"Buy {product.name} Online | {product.brand_name}"
        listing.long_description = f"<h2>Premium {product.name}</h2><p>{product.description}</p><h3>Features:</h3><ul><li>High quality materials</li><li>Exceptional performance</li><li>Customer satisfaction guaranteed</li></ul>"
        listing.keywords = f"{product.name}, buy online, {product.brand_name}, premium quality"

    def _analyze_product_context(self, product):
        """Analyze product to generate dynamic, product-specific context for AI prompts"""
        
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
        
        context = f"""PRODUCT-SPECIFIC GUIDANCE:
- Product Type: {product_type.title()}
- Primary Keywords to Use: {', '.join(primary_keywords)}
- Target Pain Points: {', '.join(pain_points[:3])}
- Key Benefits to Highlight: {', '.join(benefit_focus[:3])}
- Price Point Context: ${product.price or '0'} - position as {'premium' if float(product.price or 0) > 100 else 'value' if float(product.price or 0) > 50 else 'budget'} option

CUSTOMIZATION REQUIREMENTS:
- TITLE: Use "{primary_keywords[0]}" as primary keyword, highlight main benefit from: {', '.join(benefit_focus[:2])}
- BULLETS: Address pain points: {', '.join(pain_points[:2])} with benefits: {', '.join(benefit_focus[:2])}
- KEYWORDS: Build around "{primary_keywords[0]}", "{product_type}", and product-specific terms from name/features
- A+ CONTENT: Focus on {product_type} use cases and {', '.join(benefit_focus[:3])} benefits"""
        
        return context

    def _get_competitor_context(self, product):
        if not product.competitor_urls:
            return ""
        
        urls = [url.strip() for url in product.competitor_urls.split(',') if url.strip()]
        if urls:
            return f"\nCOMPETITOR ANALYSIS: Differentiate from competitors at {', '.join(urls[:3])}"
        return ""
    
    def _queue_image_generation(self, listing):
        """Queue image generation for the listing"""
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
        """Determine appropriate tone based on product category"""
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
        """Select listing template to ensure variety"""
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