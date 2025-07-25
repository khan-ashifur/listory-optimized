import json
from django.conf import settings
from .models import GeneratedListing, KeywordResearch
from apps.core.models import Product


class ListingGeneratorService:
    def __init__(self):
        try:
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
                self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
                print("OpenAI client initialized successfully - AI generation enabled!")
        except Exception as e:
            print(f"Error initializing OpenAI client: {e}")
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
            return listing
            
        except Exception as e:
            if 'listing' in locals():
                listing.status = 'failed'
                listing.save()
            raise e

    def _generate_amazon_listing(self, product, listing):
        competitor_context = self._get_competitor_context(product)
        
        prompt = f"""You are a CONVERSION-FOCUSED AMAZON COPYWRITER who writes like a persuasive friend helping someone make the best buying decision. Create an emotionally compelling, story-driven Amazon listing that converts browsers into buyers.

PRODUCT DETAILS:
- Product: {product.name}
- Brand: {product.brand_name}
- Description: {product.description}
- Key Features: {product.features}
- Categories: {product.categories}
- Price Point: ${product.price}
- Brand Voice: {product.brand_tone}
{competitor_context}

🎯 CONVERSION-FIRST REQUIREMENTS:

1️⃣ TITLE (Under 200 chars):
✅ Start with emotional hook or value ("Feel Weightless Support All Day")
✅ Include: Brand + Product + Key Benefit + Use Case
✅ Add urgency or transformation promise

2️⃣ BULLET POINTS (5 maximum):
✅ Each starts with relevant emoji
✅ Format: 🔥 Feature Name: Transformation/benefit explanation
✅ Focus on pain relief, lifestyle upgrade, daily use transformation
✅ Write like you're convincing a friend, not listing specs
✅ NO markdown formatting (no ** or bold text)

3️⃣ DESCRIPTION (Structured HTML with emotional hooks):
✅ Start with H2 headline featuring emotional benefit
✅ Opening paragraph: relatable pain point or scenario
✅ H3 sections with benefits, features, guarantee
✅ Use proper HTML tags: <h2>, <h3>, <p>, <ul>, <li>, <strong>
✅ Show transformation: "Imagine working 8 hours without back pain..."
✅ End with vision of better lifestyle or call to action

4️⃣ SEO KEYWORDS (10-12 total, grouped):
✅ Primary Keywords (3-4): Main product terms
✅ Related Keywords (3-4): Feature-based terms  
✅ Buyer Intent/Long-tail (4-5): Problem-solving phrases

5️⃣ A+ CONTENT (7 detailed modules with specific suggestions):
✅ Module 1: Hero Image with Value Prop
✅ Module 2: Feature Highlights Grid
✅ Module 3: Comparison Chart
✅ Module 4: Brand Story
✅ Module 5: Customer Journey/Testimonials
✅ Module 6: Size Guide/Technical Specs
✅ Module 7: Guarantee & Support
✅ Each module needs: Type, Title, Detailed Content, Specific Image Requirements

6️⃣ CONVERSION BOOSTERS (Complete toolkit):
✅ What's in the Box details
✅ Trust builders (warranty, support, reviews)
✅ Social proof numbers
✅ Comparison advantages  
✅ 3-5 FAQ pairs with answers

🧠 CUSTOMER PSYCHOLOGY: Write like you're talking to someone who's frustrated with their current situation and desperately wants a better solution. Every word should move them closer to "Add to Cart".

Return ONLY valid JSON:
{{
  "title": "Feel [Emotional Benefit] All Day - Brand ProductName with [Key Feature] for [Target Use] - [Unique Value Prop]",
  "bullet_points": [
    "🔥 [Feature Name]: [Transformation story - how this changes their daily experience]",
    "💪 [Unique Advantage]: [What competitors can't offer - why this matters to them]",
    "✨ [Quality Promise]: [Durability/materials story - why they can trust this]",
    "🎯 [Perfect For]: [Who this serves best - lifestyle/use case fit]",
    "💯 [Guarantee/Value]: [Risk reversal - why there's no downside to trying]"
  ],
  "long_description": "<h2>[Emotional Benefit] - Transform Your [Use Case] Today</h2><p><strong>Picture this:</strong> [Relatable scenario that highlights their pain]. You've tried everything, but nothing seems to work...</p><p>Now imagine [transformation vision]. That's exactly what happens when you experience the power of [product name].</p><h3>✨ What Makes This Different</h3><ul><li><strong>[Key Feature 1]:</strong> [How it solves a specific problem]</li><li><strong>[Key Feature 2]:</strong> [Another pain point it addresses]</li><li><strong>[Key Feature 3]:</strong> [Third major benefit]</li></ul><h3>🛡️ Our Promise to You</h3><p>We're so confident you'll love this that we offer a <strong>30-day money-back guarantee</strong>. If you don't experience [main benefit], we'll refund every penny.</p><p><strong>Join [number]+ satisfied customers</strong> who've already transformed their [use case]. Don't let another day go by feeling [pain point].</p>",
  "aplus_content": {{
    "module1": {{
      "type": "Hero Banner with Text Overlay",
      "title": "[Emotional Hook] - Experience the [Product] Difference",
      "content": "Transform your [use case] with [key benefit]. Join thousands who've discovered [unique value proposition].",
      "image_suggestion": "Lifestyle hero shot showing product in use with happy customer, overlay text highlighting main benefit, brand colors prominent"
    }},
    "module2": {{
      "type": "4-Feature Grid with Icons",
      "title": "Everything You Need for [Desired Outcome]",
      "content": "Feature 1: [Benefit] | Feature 2: [Benefit] | Feature 3: [Benefit] | Feature 4: [Benefit]",
      "image_suggestion": "Clean grid layout with custom icons for each feature, brief benefit text under each, cohesive design matching brand aesthetic"
    }},
    "module3": {{
      "type": "Comparison Chart Module",
      "title": "See Why [Product] Leads the Market",
      "content": "Side-by-side comparison showing [Product] vs. Generic/Competitor on 5-6 key features",
      "image_suggestion": "Professional comparison table with checkmarks/X marks, highlighting superior features, clean modern design"
    }},
    "module4": {{
      "type": "Brand Story with Timeline",
      "title": "Our Mission: [Core Brand Value]",
      "content": "[Brief brand story focusing on customer problem-solving journey, why you created this product, your commitment to quality]",
      "image_suggestion": "Brand founder photo or team image, timeline showing product development milestones, authentic and trustworthy imagery"
    }},
    "module5": {{
      "type": "Customer Testimonials Carousel",
      "title": "Real Stories from Real Customers",
      "content": "3-4 detailed customer stories showing transformation, including before/after scenarios",
      "image_suggestion": "Customer photos with quotes, star ratings visible, diverse representation, authentic real-life settings"
    }},
    "module6": {{
      "type": "Size Guide/Technical Specifications",
      "title": "Find Your Perfect Fit",
      "content": "Detailed sizing chart or technical specifications with visual guides",
      "image_suggestion": "Clear measurement diagrams, size comparison visuals, easy-to-read specifications table"
    }},
    "module7": {{
      "type": "Guarantee & Support Module",
      "title": "Shop with Complete Confidence",
      "content": "30-Day Money Back Guarantee | Free Shipping | Lifetime Support | Easy Returns",
      "image_suggestion": "Trust badges, guarantee seal, customer service representative, reassuring visual elements"
    }}
  }},
  "seo_keywords": {{
    "primary": ["main product keyword", "core feature term", "brand category"],
    "related": ["feature keyword", "material term", "use case term"],
    "buyer_intent": ["best [product] for [problem]", "[product] under $[price]", "how to choose [product]", "[problem] solution", "[brand] vs [competitor]"]
  }},
  "conversion_boosters": {{
    "whats_in_box": ["Main product", "Setup accessories", "User guide", "Additional items"],
    "trust_builders": ["X-year warranty", "24/7 customer support", "30-day satisfaction guarantee", "Certified quality standards"],
    "social_proof": "Loved by [number]+ happy customers - [rating] stars average",
    "comparison_advantage": "Vs. other brands: [3 key advantages that matter to customers]",
    "faqs": [
      {{"q": "[Common concern question]", "a": "[Reassuring, detailed answer]"}},
      {{"q": "[Compatibility question]", "a": "[Clear compatibility info]"}},
      {{"q": "[Quality/durability question]", "a": "[Quality assurance answer]"}},
      {{"q": "[Usage question]", "a": "[Easy usage explanation]"}},
      {{"q": "[Value/price question]", "a": "[Value justification]"}}
    ]
  }}
}}"""
        
        if self.client:
            try:
                print(f"Generating AI content for {product.name} on Amazon...")
                
                # Use new OpenAI API
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Use gpt-3.5-turbo for cost efficiency
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=2000
                )
                ai_content = response.choices[0].message.content
                print(f"AI Response received: {len(ai_content)} characters")
                
                result = json.loads(ai_content)
                
                # Enhanced parsing for new conversion-focused structure
                listing.title = result.get('title', '')[:200]  # Amazon allows up to 200 chars
                listing.bullet_points = '\n\n'.join(result.get('bullet_points', []))
                listing.long_description = result.get('long_description', '')
                
                # Parse nested SEO keywords structure
                seo_keywords = result.get('seo_keywords', {})
                if isinstance(seo_keywords, dict):
                    primary_keywords = seo_keywords.get('primary', [])
                    related_keywords = seo_keywords.get('related', [])
                    buyer_intent_keywords = seo_keywords.get('buyer_intent', [])
                    all_keywords = primary_keywords + related_keywords + buyer_intent_keywords
                    listing.keywords = ', '.join(all_keywords) if all_keywords else ''
                    listing.amazon_backend_keywords = ', '.join(primary_keywords + related_keywords)  # No buyer intent in backend
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
                    
                    listing.amazon_aplus_content = '\n\n'.join(aplus_sections)
                else:
                    listing.amazon_aplus_content = result.get('aplus_content', '')
                
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
                print(f"   Title length: {len(listing.title)} chars")
                print(f"   Bullet points: {len(result.get('bullet_points', []))} items")
                print(f"   Keywords: {len(all_keywords)} total")
                
            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {e}")
                print(f"Raw AI response: {ai_content}")
                self._generate_fallback_amazon(product, listing)
            except Exception as e:
                print(f"OpenAI API error: {e}")
                self._generate_fallback_amazon(product, listing)
        else:
            print("Cannot generate listing - OpenAI not configured properly")
            raise Exception("OpenAI API key not configured. Please set a valid OpenAI API key in your .env file to generate AI-powered listings.")

    def _generate_fallback_amazon(self, product, listing):
        listing.title = f"{product.brand_name} {product.name} - Premium Quality & Superior Performance"
        listing.bullet_points = f"""PREMIUM QUALITY - {product.description[:100]}...
SUPERIOR PERFORMANCE - Advanced features and reliable design
GUARANTEED SATISFACTION - High-quality materials and construction  
EASY TO USE - Simple setup and user-friendly operation
GREAT VALUE - Premium features at an affordable price"""
        listing.long_description = f"<h2>Experience Premium Quality with {product.name}</h2><p>{product.description}</p><h3>Key Features:</h3><ul><li>Premium construction</li><li>Superior performance</li><li>Easy to use</li></ul>"
        listing.amazon_backend_keywords = f"{product.name}, {product.brand_name}, premium quality, best seller"
        listing.amazon_aplus_content = "Module 1: Feature comparison\nModule 2: Quality guarantee\nModule 3: Customer testimonials"
        listing.keywords = listing.amazon_backend_keywords

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

    def _get_competitor_context(self, product):
        if not product.competitor_urls:
            return ""
        
        urls = [url.strip() for url in product.competitor_urls.split(',') if url.strip()]
        if urls:
            return f"\nCOMPETITOR ANALYSIS: Differentiate from competitors at {', '.join(urls[:3])}"
        return ""