"""
Enhanced Amazon Listing Service with Perfect Occasion Integration
Each occasion gets custom prompts, keywords, and emotional triggers
"""

class OccasionOptimizer:
    """Handles occasion-specific optimizations for Amazon listings"""
    
    def __init__(self):
        self.occasion_configs = {
            "Valentine's Day": {
                "emotional_hooks": [
                    "Show them what real love looks like",
                    "Because 'I love you' deserves more than words",
                    "Turn February 14th into their favorite memory",
                    "Skip the cliché gifts, give something they'll actually use",
                    "Romance meets practicality"
                ],
                "title_patterns": [
                    "Perfect Valentine's Gift - {product} for {benefit}",
                    "Valentine's Day Special {product} - {unique_feature} for Couples",
                    "Romantic {product} Gift Set - {benefit} This Valentine's",
                    "{product} Valentine Edition - {feature} for Your Special Someone"
                ],
                "power_words": ["romantic", "love", "couples", "sweetheart", "passion", "intimate", "special someone", "beloved"],
                "urgency_phrases": ["Order by Feb 10th for Valentine's delivery", "Limited Valentine's stock", "Valentine's Day shipping guaranteed"],
                "bullet_starters": [
                    "VALENTINE'S GIFT PERFECTION:",
                    "ROMANTIC & PRACTICAL:",
                    "LOVE MEETS FUNCTION:",
                    "COUPLES WILL ADORE:",
                    "VALENTINE'S DAY READY:"
                ],
                "keywords": [
                    "valentine gift for her", "valentine gift for him", "romantic gift ideas",
                    "valentine day present", "couples gift", "february 14 gift",
                    "valentine special", "romantic surprise", "love gift",
                    "valentine's day {product_type}", "best valentine gifts 2025"
                ],
                "description_hooks": [
                    "This Valentine's Day, skip the flowers that wilt and chocolates that disappear.",
                    "Love is in the details, and this {product} proves it.",
                    "Transform Valentine's Day from predictable to unforgettable."
                ],
                "gift_messaging": "Gift-wrap available. Add a personalized Valentine's message at checkout.",
                "seasonal_context": "Perfect for Valentine's Day (February 14th) - Order now for guaranteed delivery!"
            },
            
            "Mother's Day": {
                "emotional_hooks": [
                    "Because Mom deserves more than a card",
                    "Show Mom she's appreciated every single day",
                    "The gift that says what words can't",
                    "Make this Mother's Day her favorite one yet",
                    "For the woman who does it all"
                ],
                "title_patterns": [
                    "Mother's Day Gift - {product} Mom Will Love - {benefit}",
                    "Perfect for Mom - {product} with {feature} - Mother's Day Special",
                    "{product} Mother's Day Edition - {benefit} for Busy Moms",
                    "Mom-Approved {product} - {unique_feature} This Mother's Day"
                ],
                "power_words": ["mom", "mother", "maternal", "nurturing", "caring", "thoughtful", "appreciation", "pamper"],
                "urgency_phrases": ["Order by May 7th for Mother's Day", "Mother's Day delivery guaranteed", "Limited Mother's Day stock"],
                "bullet_starters": [
                    "MOM WILL LOVE THIS:",
                    "PERFECT FOR BUSY MOMS:",
                    "MOTHER'S DAY FAVORITE:",
                    "THOUGHTFUL & PRACTICAL:",
                    "PAMPER MOM WITH:"
                ],
                "keywords": [
                    "mothers day gift", "gift for mom", "best mom gift",
                    "mother's day present", "mom birthday gift", "new mom gift",
                    "gifts for mothers", "may gift for mom", "mom appreciation gift",
                    "mother's day {product_type}", "thoughtful mom gifts"
                ],
                "description_hooks": [
                    "Mom's been putting everyone else first for years. This Mother's Day, it's her turn.",
                    "Finding the perfect gift for Mom shouldn't be this hard—until now, it isn't.",
                    "This isn't just another Mother's Day gift that ends up in a drawer."
                ],
                "gift_messaging": "Free Mother's Day gift wrapping. Add your personal message for Mom.",
                "seasonal_context": "Mother's Day (May 12, 2025) - Show Mom she's appreciated!"
            },
            
            "Christmas": {
                "emotional_hooks": [
                    "Make their Christmas morning unforgettable",
                    "The gift they'll actually be excited to unwrap",
                    "Bringing extra magic to the holidays",
                    "Because the best gifts are both thoughtful and useful",
                    "Start a new Christmas tradition"
                ],
                "title_patterns": [
                    "Christmas Gift {product} - {benefit} - Perfect Holiday Present",
                    "{product} Christmas Edition - {feature} for Holiday Season",
                    "Ultimate Christmas Gift - {product} with {unique_feature}",
                    "Holiday Special {product} - {benefit} Under the Tree"
                ],
                "power_words": ["festive", "holiday", "Christmas", "seasonal", "jolly", "merry", "celebration", "tradition"],
                "urgency_phrases": ["Order by Dec 15th for Christmas delivery", "Holiday shipping deadlines apply", "Christmas stock running low"],
                "bullet_starters": [
                    "CHRISTMAS GIFT WINNER:",
                    "HOLIDAY ESSENTIAL:",
                    "FESTIVE & FUNCTIONAL:",
                    "PERFECT STOCKING STUFFER:",
                    "CHRISTMAS MORNING SURPRISE:"
                ],
                "keywords": [
                    "christmas gift", "holiday present", "stocking stuffer",
                    "christmas gift ideas", "secret santa gift", "white elephant gift",
                    "christmas {product_type}", "holiday gift guide", "xmas present",
                    "best christmas gifts 2024", "gift under tree"
                ],
                "description_hooks": [
                    "This Christmas, give a gift that won't be re-gifted next year.",
                    "Picture their face on Christmas morning when they unwrap this.",
                    "The holidays are about joy, not stress—this gift delivers both."
                ],
                "gift_messaging": "Free holiday gift wrap. Include a Christmas card message.",
                "seasonal_context": "Christmas delivery guaranteed if ordered by December 15th!"
            },
            
            "Birthday": {
                "emotional_hooks": [
                    "Make their birthday wish come true",
                    "The birthday gift they didn't know they needed",
                    "Celebrate another year with something special",
                    "Because birthdays deserve better than gift cards",
                    "Turn their special day into a special year"
                ],
                "title_patterns": [
                    "Perfect Birthday Gift - {product} with {benefit}",
                    "{product} Birthday Edition - {feature} for Special Celebrations",
                    "Birthday Present Winner - {product} They'll Love",
                    "Unique Birthday Gift - {product} with {unique_feature}"
                ],
                "power_words": ["celebration", "special day", "milestone", "surprise", "memorable", "wishes", "party", "festive"],
                "urgency_phrases": ["Next-day delivery available", "Birthday shipping options", "Rush delivery for last-minute gifts"],
                "bullet_starters": [
                    "BIRTHDAY GIFT PERFECTION:",
                    "CELEBRATION READY:",
                    "SPECIAL DAY ESSENTIAL:",
                    "BIRTHDAY SURPRISE:",
                    "YEAR-ROUND ENJOYMENT:"
                ],
                "keywords": [
                    "birthday gift", "birthday present", "bday gift ideas",
                    "unique birthday gift", "best birthday gifts", "birthday surprise",
                    "gift for him birthday", "gift for her birthday", "milestone birthday",
                    "birthday {product_type}", "special occasion gift"
                ],
                "description_hooks": [
                    "Birthdays come once a year, but great gifts are remembered forever.",
                    "Skip the predictable birthday presents and give something they'll actually use.",
                    "Make their birthday memorable with a gift that keeps on giving."
                ],
                "gift_messaging": "Free birthday gift wrap and personalized message card included.",
                "seasonal_context": "Perfect birthday gift for any age - Fast shipping available!"
            },
            
            "Wedding": {
                "emotional_hooks": [
                    "For the couple who has everything except this",
                    "Start their marriage with something special",
                    "The wedding gift they'll actually use",
                    "Celebrating love with practical elegance",
                    "A gift as unique as their love story"
                ],
                "title_patterns": [
                    "Wedding Gift - {product} for Newlyweds - {benefit}",
                    "Elegant Wedding Present - {product} with {feature}",
                    "{product} Wedding Edition - Perfect Couples Gift",
                    "Unique Wedding Gift - {product} They'll Treasure"
                ],
                "power_words": ["newlyweds", "couples", "marriage", "elegant", "sophisticated", "timeless", "union", "together"],
                "urgency_phrases": ["Wedding registry eligible", "Elegant gift wrap included", "Direct shipping to couple available"],
                "bullet_starters": [
                    "PERFECT WEDDING GIFT:",
                    "NEWLYWEDS WILL LOVE:",
                    "ELEGANT & PRACTICAL:",
                    "COUPLES' FAVORITE:",
                    "MARRIAGE MILESTONE:"
                ],
                "keywords": [
                    "wedding gift", "wedding present", "newlywed gift",
                    "couples wedding gift", "bridal shower gift", "engagement gift",
                    "unique wedding gifts", "wedding registry", "marriage gift",
                    "wedding {product_type}", "mr and mrs gift"
                ],
                "description_hooks": [
                    "Help the happy couple start their journey with a gift that matters.",
                    "While others give picture frames, you're giving something they'll use daily.",
                    "The best wedding gifts are both beautiful and functional."
                ],
                "gift_messaging": "Elegant wedding gift presentation. Card with your message included.",
                "seasonal_context": "Wedding season special - Perfect for couples starting their journey!"
            },
            
            "Anniversary": {
                "emotional_hooks": [
                    "Celebrate years of love with something meaningful",
                    "Because every anniversary deserves recognition",
                    "Mark the milestone with more than dinner",
                    "For couples who appreciate thoughtful gifts",
                    "Another year, another reason to celebrate"
                ],
                "title_patterns": [
                    "Anniversary Gift - {product} for Celebrating Love - {benefit}",
                    "{product} Anniversary Edition - {feature} for Couples",
                    "Perfect Anniversary Present - {product} with {unique_feature}",
                    "Romantic Anniversary Gift - {product} They'll Cherish"
                ],
                "power_words": ["milestone", "celebration", "romantic", "memorable", "years together", "love", "commitment", "special"],
                "urgency_phrases": ["Anniversary date delivery available", "Romantic packaging included", "Express shipping for special dates"],
                "bullet_starters": [
                    "ANNIVERSARY PERFECT:",
                    "CELEBRATE LOVE WITH:",
                    "ROMANTIC & USEFUL:",
                    "COUPLES APPRECIATION:",
                    "MILESTONE MARKER:"
                ],
                "keywords": [
                    "anniversary gift", "anniversary present", "wedding anniversary",
                    "1st anniversary gift", "25th anniversary", "50th anniversary",
                    "romantic anniversary gift", "couples anniversary", "year anniversary",
                    "anniversary {product_type}", "husband wife gift"
                ],
                "description_hooks": [
                    "Anniversaries mark time, but great gifts make memories.",
                    "Show them the spark is still there with a gift that surprises.",
                    "Celebrate your journey together with something you'll both enjoy."
                ],
                "gift_messaging": "Anniversary gift wrap available. Include your love message.",
                "seasonal_context": "Perfect for any anniversary milestone - 1st to 50th and beyond!"
            },
            
            "Father's Day": {
                "emotional_hooks": [
                    "For the dad who says he doesn't need anything",
                    "Show Dad he's more than just the fix-it guy",
                    "Because Dad deserves better than another tie",
                    "Make Father's Day actually mean something",
                    "The gift Dad will brag about"
                ],
                "title_patterns": [
                    "Father's Day Gift - {product} Dad Will Use Daily - {benefit}",
                    "Perfect for Dad - {product} with {feature} - Father's Day",
                    "{product} Father's Day Edition - {benefit} for Busy Dads",
                    "Dad-Approved {product} - {unique_feature} This June"
                ],
                "power_words": ["dad", "father", "paternal", "practical", "rugged", "reliable", "quality", "durable"],
                "urgency_phrases": ["Order by June 10th for Father's Day", "Dad-approved guarantee", "Father's Day shipping included"],
                "bullet_starters": [
                    "DAD WILL LOVE THIS:",
                    "FATHER'S DAY WINNER:",
                    "PRACTICAL FOR DAD:",
                    "DAD-APPROVED QUALITY:",
                    "PERFECT FOR POPS:"
                ],
                "keywords": [
                    "fathers day gift", "gift for dad", "best dad gift",
                    "father's day present", "dad birthday gift", "new dad gift",
                    "gifts for fathers", "june gift for dad", "dad appreciation",
                    "father's day {product_type}", "practical dad gifts"
                ],
                "description_hooks": [
                    "Dad's spent years being everyone's hero. Time to return the favor.",
                    "This Father's Day, give Dad something he'll actually use, not just appreciate.",
                    "The kind of gift that makes Dad say 'How did you know I needed this?'"
                ],
                "gift_messaging": "Father's Day gift wrap available. Add your message for Dad.",
                "seasonal_context": "Father's Day (June 16, 2025) - Show Dad he's appreciated!"
            },
            
            "Easter": {
                "emotional_hooks": [
                    "Add something special to their Easter basket",
                    "Spring into the season with the perfect gift",
                    "Because Easter is about new beginnings",
                    "Make their Easter morning extra special",
                    "Celebrate renewal with something fresh"
                ],
                "title_patterns": [
                    "Easter Gift - {product} for Spring Celebrations - {benefit}",
                    "{product} Easter Special - {feature} for the Holiday",
                    "Perfect Easter Basket Addition - {product} with {unique_feature}",
                    "Spring Gift - {product} for Easter Morning"
                ],
                "power_words": ["spring", "renewal", "fresh", "basket", "holiday", "celebration", "family", "tradition"],
                "urgency_phrases": ["Easter delivery available", "Spring special pricing", "Limited Easter edition"],
                "bullet_starters": [
                    "EASTER BASKET PERFECT:",
                    "SPRING CELEBRATION:",
                    "HOLIDAY SPECIAL:",
                    "EASTER MORNING JOY:",
                    "SEASONAL FAVORITE:"
                ],
                "keywords": [
                    "easter gift", "easter basket stuffer", "spring gift",
                    "easter present", "easter basket ideas", "easter sunday",
                    "easter {product_type}", "spring celebration", "easter special",
                    "holiday gift easter", "easter morning surprise"
                ],
                "description_hooks": [
                    "This Easter, go beyond chocolate eggs and plastic grass.",
                    "Spring is about fresh starts—make their Easter gift count.",
                    "Add something unexpected to their Easter celebration."
                ],
                "gift_messaging": "Easter gift presentation available. Spring into the season!",
                "seasonal_context": "Easter Sunday delivery - Perfect spring gift!"
            },
            
            "Halloween": {
                "emotional_hooks": [
                    "Treat them to something better than candy",
                    "Make Halloween memorable beyond the costume",
                    "For those who take Halloween seriously",
                    "Spooky season deserves special gifts",
                    "Because Halloween is more fun with the right gear"
                ],
                "title_patterns": [
                    "Halloween Special - {product} for Spooky Season - {benefit}",
                    "{product} Halloween Edition - {feature} for October Fun",
                    "Perfect Halloween Gift - {product} with {unique_feature}",
                    "Trick or Treat Yourself - {product} This Halloween"
                ],
                "power_words": ["spooky", "fun", "trick or treat", "costume", "October", "autumn", "festive", "scary good"],
                "urgency_phrases": ["Halloween delivery guaranteed", "October special", "Limited Halloween edition"],
                "bullet_starters": [
                    "HALLOWEEN PERFECT:",
                    "SPOOKY SEASON SPECIAL:",
                    "OCTOBER ESSENTIAL:",
                    "TRICK OR TREAT:",
                    "FRIGHTENINGLY GOOD:"
                ],
                "keywords": [
                    "halloween gift", "halloween special", "october gift",
                    "spooky season", "trick or treat", "halloween party",
                    "halloween {product_type}", "autumn gift", "fall special",
                    "october 31 gift", "halloween treats"
                ],
                "description_hooks": [
                    "This Halloween, give them something scarier than a sugar crash.",
                    "Make their Halloween complete with more than just a costume.",
                    "October 31st is about more than candy—make it memorable."
                ],
                "gift_messaging": "Halloween themed packaging available. Spooky surprises included!",
                "seasonal_context": "Halloween ready - Perfect for October celebrations!"
            },
            
            "Thanksgiving": {
                "emotional_hooks": [
                    "Show gratitude with a gift that matters",
                    "Because Thanksgiving is about more than turkey",
                    "Give thanks with something thoughtful",
                    "Make their Thanksgiving gathering complete",
                    "Gratitude looks good on everyone"
                ],
                "title_patterns": [
                    "Thanksgiving Gift - {product} for Grateful Hearts - {benefit}",
                    "{product} Thanksgiving Special - {feature} for Family Time",
                    "Perfect for Thanksgiving - {product} with {unique_feature}",
                    "Gratitude Gift - {product} This Thanksgiving"
                ],
                "power_words": ["grateful", "thankful", "family", "gathering", "harvest", "autumn", "blessing", "appreciation"],
                "urgency_phrases": ["Thanksgiving delivery available", "November special", "Family gathering ready"],
                "bullet_starters": [
                    "THANKSGIVING ESSENTIAL:",
                    "GRATEFUL FOR THIS:",
                    "FAMILY GATHERING READY:",
                    "HARVEST SEASON SPECIAL:",
                    "THANKFUL MOMENTS:"
                ],
                "keywords": [
                    "thanksgiving gift", "gratitude gift", "november gift",
                    "thanksgiving present", "family gathering", "harvest gift",
                    "thanksgiving {product_type}", "thankful gift", "autumn present",
                    "turkey day gift", "thanksgiving host gift"
                ],
                "description_hooks": [
                    "This Thanksgiving, show gratitude with more than just words.",
                    "Make the family gathering even more special this year.",
                    "Give thanks in a way they'll remember long after the turkey's gone."
                ],
                "gift_messaging": "Thanksgiving gift wrap available. Express your gratitude!",
                "seasonal_context": "Thanksgiving special - Perfect for showing appreciation!"
            },
            
            "New Year": {
                "emotional_hooks": [
                    "Start their year off right",
                    "New year, new possibilities, perfect gift",
                    "Because resolutions need the right tools",
                    "Ring in the new year with something special",
                    "Make this year different from day one"
                ],
                "title_patterns": [
                    "New Year Gift - {product} for Fresh Starts - {benefit}",
                    "{product} New Year Edition - {feature} for 2025",
                    "Perfect New Year Present - {product} with {unique_feature}",
                    "Resolution Ready - {product} for the New Year"
                ],
                "power_words": ["fresh start", "resolution", "new beginning", "goals", "celebration", "midnight", "champagne", "possibilities"],
                "urgency_phrases": ["New Year delivery available", "January special", "Resolution season deal"],
                "bullet_starters": [
                    "NEW YEAR PERFECT:",
                    "RESOLUTION READY:",
                    "FRESH START ESSENTIAL:",
                    "2025 MUST-HAVE:",
                    "JANUARY FAVORITE:"
                ],
                "keywords": [
                    "new year gift", "new years eve", "january gift",
                    "resolution gift", "fresh start", "new year present",
                    "new year {product_type}", "2025 gift", "new beginning",
                    "midnight celebration", "year starter gift"
                ],
                "description_hooks": [
                    "New Year's resolutions are easier to keep with the right tools.",
                    "Start 2025 with something that actually makes a difference.",
                    "This year, give a gift that helps them become who they want to be."
                ],
                "gift_messaging": "New Year gift presentation. Start 2025 right!",
                "seasonal_context": "New Year special - Perfect for fresh starts and resolutions!"
            },
            
            "Graduation": {
                "emotional_hooks": [
                    "Celebrate their achievement with something meaningful",
                    "For the next chapter of their journey",
                    "Because graduation is just the beginning",
                    "Mark the milestone with more than a card",
                    "The gift that grows with their success"
                ],
                "title_patterns": [
                    "Graduation Gift - {product} for New Beginnings - {benefit}",
                    "{product} Graduation Edition - {feature} for Success",
                    "Perfect Graduation Present - {product} for the Future",
                    "Class of 2025 Gift - {product} They'll Treasure"
                ],
                "power_words": ["achievement", "success", "future", "milestone", "accomplishment", "journey", "opportunity", "pride"],
                "urgency_phrases": ["Graduation day delivery", "Class of 2025 special", "Commencement ready"],
                "bullet_starters": [
                    "GRADUATION PERFECT:",
                    "FUTURE SUCCESS:",
                    "ACHIEVEMENT WORTHY:",
                    "NEW CHAPTER READY:",
                    "MILESTONE MARKER:"
                ],
                "keywords": [
                    "graduation gift", "graduation present", "class of 2025",
                    "college graduation", "high school graduation", "grad gift",
                    "graduation {product_type}", "commencement gift", "degree celebration",
                    "achievement gift", "graduate present"
                ],
                "description_hooks": [
                    "They worked hard for this moment—give them a gift that honors it.",
                    "Graduation marks the end of one chapter and the beginning of another.",
                    "Help them step into their future with confidence and the right tools."
                ],
                "gift_messaging": "Graduation gift wrap included. Celebrate their achievement!",
                "seasonal_context": "Graduation season - Perfect for celebrating achievements!"
            },
            
            "Baby Shower": {
                "emotional_hooks": [
                    "Welcome the little one with something special",
                    "For parents who want the best start",
                    "Because new parents need all the help they can get",
                    "Make their nursery complete",
                    "The baby shower gift they'll actually use"
                ],
                "title_patterns": [
                    "Baby Shower Gift - {product} for New Parents - {benefit}",
                    "{product} Baby Edition - {feature} for Growing Families",
                    "Perfect Baby Shower Present - {product} Parents Love",
                    "New Parent Essential - {product} for Baby's Comfort"
                ],
                "power_words": ["nursery", "newborn", "parents", "baby", "gentle", "safe", "comfort", "precious"],
                "urgency_phrases": ["Baby shower ready", "Nursery essential", "New parent approved"],
                "bullet_starters": [
                    "BABY SHOWER PERFECT:",
                    "NEW PARENT ESSENTIAL:",
                    "NURSERY READY:",
                    "BABY-SAFE DESIGN:",
                    "PARENT APPROVED:"
                ],
                "keywords": [
                    "baby shower gift", "new baby gift", "newborn present",
                    "baby shower ideas", "nursery gift", "new parent gift",
                    "baby {product_type}", "expecting parents", "baby registry",
                    "infant gift", "baby shower essential"
                ],
                "description_hooks": [
                    "New parents have enough to worry about—make one thing easier.",
                    "The baby shower gift that stands out from the pile of onesies.",
                    "Help them prepare for the beautiful chaos ahead."
                ],
                "gift_messaging": "Baby shower gift wrap available. Welcome the little one!",
                "seasonal_context": "Baby shower ready - Perfect gift for expecting parents!"
            },
            
            "Housewarming": {
                "emotional_hooks": [
                    "Help them turn a house into a home",
                    "For fresh starts in new spaces",
                    "Because every home needs the essentials",
                    "Make their new place feel special",
                    "The housewarming gift they'll use every day"
                ],
                "title_patterns": [
                    "Housewarming Gift - {product} for New Homes - {benefit}",
                    "{product} Home Edition - {feature} for Fresh Starts",
                    "Perfect Housewarming Present - {product} They'll Love",
                    "New Home Essential - {product} for Daily Comfort"
                ],
                "power_words": ["home", "cozy", "welcoming", "fresh start", "comfortable", "essential", "daily use", "settling in"],
                "urgency_phrases": ["New home ready", "Moving day special", "Housewarming party perfect"],
                "bullet_starters": [
                    "HOUSEWARMING PERFECT:",
                    "NEW HOME ESSENTIAL:",
                    "DAILY USE GUARANTEED:",
                    "FRESH START READY:",
                    "HOME COMFORT:"
                ],
                "keywords": [
                    "housewarming gift", "new home gift", "moving gift",
                    "housewarming present", "home essentials", "new apartment",
                    "housewarming {product_type}", "first home gift", "moving day",
                    "home decor gift", "practical home gift"
                ],
                "description_hooks": [
                    "Help them settle into their new space with something they'll use daily.",
                    "The housewarming gift that doesn't end up in storage.",
                    "Make their new house feel like home from day one."
                ],
                "gift_messaging": "Housewarming gift presentation. Welcome them home!",
                "seasonal_context": "Housewarming ready - Perfect for new homeowners!"
            }
        }
    
    def get_occasion_prompt_enhancement(self, occasion):
        """Get the complete prompt enhancement for a specific occasion"""
        if occasion not in self.occasion_configs:
            return self._get_generic_occasion_prompt(occasion)
            
        config = self.occasion_configs[occasion]
        
        prompt = f"""
🎁 CRITICAL OCCASION OPTIMIZATION FOR {occasion.upper()} 🎁

This listing MUST be deeply integrated with {occasion} throughout every element.
The customer is specifically searching for {occasion} gifts, so generic listings will fail.

EMOTIONAL HOOK TO USE:
"{random.choice(config['emotional_hooks'])}"

TITLE REQUIREMENTS:
- MUST include "{occasion}" or related term in the title
- Use this pattern: {random.choice(config['title_patterns'])}
- Include these power words: {', '.join(random.sample(config['power_words'], 3))}
- Add urgency: {config['urgency_phrases'][0]}

BULLET POINT REQUIREMENTS:
- At least 2 bullets MUST mention {occasion} specifically
- Start bullets with variations of: {config['bullet_starters']}
- Include gift-giving benefits and occasion-specific use cases
- Mention timing/delivery for the occasion

DESCRIPTION REQUIREMENTS:
- Open with: {config['description_hooks'][0]}
- Mention {occasion} at least 3 times naturally
- Include {config['gift_messaging']}
- Add seasonal context: {config['seasonal_context']}
- Create urgency around the occasion date

KEYWORD REQUIREMENTS:
Must include ALL of these occasion-specific keywords:
{chr(10).join(f'- {kw}' for kw in config['keywords'])}

A+ CONTENT REQUIREMENTS:
- Hero section: Feature {occasion} gifting scenario with title like "Perfect {occasion} Gift" 
- Hero content: Include {occasion}-specific use cases and emotional benefits
- Trust builders: Include gift-giving testimonials mentioning {occasion}
- FAQs: Address {occasion} delivery timing, gift wrapping, personalization options
- Features section: Highlight why this works for {occasion} gifting
- Add dedicated section: "Why This Makes the Perfect {occasion} Gift"

CRITICAL A+ CONTENT INTEGRATION:
Every A+ section MUST mention {occasion} or gift-giving context:
- section1_hero title: Include "{occasion} Gift" or "{occasion} Perfect" 
- section1_hero content: Reference {occasion} usage scenarios
- section2_features title: "Perfect for {occasion}" or "{occasion} Ready"
- trustBuilders: Add {occasion} testimonials and gift stories
- faqs: Include {occasion} delivery, gifting, timing questions

PPC STRATEGY:
- Target {occasion} gift searches specifically
- Use occasion + product type combinations
- Include "last minute {occasion}" keywords
- Target gift-related long-tail keywords

CRITICAL SUCCESS FACTORS FOR 10/10 QUALITY:
✅ {occasion} mentioned in title, bullets (2+), description (3+), A+ content, keywords
✅ Emotional connection to the occasion established throughout
✅ Gift-giving benefits clearly stated in every major section
✅ Urgency and delivery timing addressed prominently
✅ Occasion-specific keywords prioritized in backend search
✅ A+ Content hero title includes "{occasion} Gift" or "{occasion} Perfect"
✅ Trust builders mention gift policies and testimonials
✅ FAQs address occasion delivery, gifting, recipient questions
✅ Bullet points use occasion-specific labels and benefits
✅ All content feels authentic to the occasion, not forced

MANDATORY INTEGRATION CHECKLIST:
□ Title contains {occasion} + "Gift" or similar
□ At least 2 bullets mention {occasion} with gift benefits
□ Description opens with {occasion} context or closes with gift appeal
□ A+ hero title: "Perfect {occasion} Gift" or "{occasion} Special"
□ A+ hero content: {occasion} use cases and emotional benefits
□ Trust builders: Gift return policy or {occasion} testimonials
□ Keywords: 5+ {occasion}-specific terms prioritized first
□ FAQs: {occasion} delivery timing and gift questions
□ Backend keywords: {occasion} gift searches prioritized

❌ FAILURE CONDITIONS:
❌ Generic listing with {occasion} only mentioned once
❌ No gift-focused benefits or language
❌ Missing {occasion} in A+ content sections
❌ Keywords don't prioritize {occasion} gift searches
❌ No urgency around {occasion} timing
"""
        return prompt
    
    def _get_generic_occasion_prompt(self, occasion):
        """Fallback for occasions not in the config"""
        return f"""
🎁 OCCASION OPTIMIZATION FOR {occasion.upper()} 🎁

CRITICAL: This listing must be optimized for {occasion} gift searches.

REQUIREMENTS:
- Title MUST include "{occasion}" or related terms
- At least 2 bullet points must mention {occasion}
- Description must reference {occasion} gifting 3+ times
- Include {occasion}-specific keywords throughout
- Add gift messaging and wrapping options
- Create urgency around {occasion} timing
"""

import random