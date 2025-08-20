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
            
            "Weihnachten": {
                "emotional_hooks": [
                    "Machen Sie Weihnachten unvergesslich",
                    "Das Geschenk, über das sie sich wirklich freuen werden",
                    "Bringen Sie extra Zauber in die Feiertage",
                    "Weil die besten Geschenke durchdacht und nützlich sind",
                    "Starten Sie eine neue Weihnachtstradition"
                ],
                "title_patterns": [
                    "Weihnachtsgeschenk {product} - {benefit} - Perfektes Feiertagsgeschenk",
                    "{product} Weihnachts-Edition - {feature} für die Festtage",
                    "Ultimatives Weihnachtsgeschenk - {product} mit {unique_feature}",
                    "Feiertags-Spezial {product} - {benefit} unterm Tannenbaum"
                ],
                "power_words": ["festlich", "Feiertage", "Weihnachten", "saisonal", "fröhlich", "weihnachtlich", "Feier", "Tradition"],
                "urgency_phrases": ["Bestellen Sie bis 15. Dezember für Weihnachtslieferung", "Weihnachts-Versandfristen beachten", "Weihnachtsvorrat wird knapp"],
                "bullet_starters": [
                    "WEIHNACHTSGESCHENK-SIEGER:",
                    "FEIERTAGS-ESSENTIAL:",
                    "FESTLICH & FUNKTIONAL:",
                    "PERFEKTER NIKOLAUSSTIEFEL-FÜLLER:",
                    "WEIHNACHTSMORGEN-ÜBERRASCHUNG:"
                ],
                "keywords": [
                    "weihnachtsgeschenk", "weihnachtspresent", "nikolausstiefel füller",
                    "weihnachtsgeschenk ideen", "wichtelgeschenk", "schrottwichteln geschenk",
                    "weihnachts {product_type}", "geschenk guide weihnachten", "xmas geschenk",
                    "beste weihnachtsgeschenke 2024", "geschenk unterm tannenbaum"
                ],
                "description_hooks": [
                    "Dieses Weihnachten schenken Sie etwas, das nicht weiter verschenkt wird.",
                    "Stellen Sie sich ihr Gesicht vor, wenn sie das am Weihnachtsmorgen auspacken.",
                    "Die Feiertage sollen Freude bringen, nicht Stress – dieses Geschenk schafft beides."
                ],
                "gift_messaging": "Kostenlose Weihnachts-Geschenkverpackung. Weihnachtskarte mit Nachricht inklusive.",
                "seasonal_context": "Weihnachtslieferung garantiert bei Bestellung bis 15. Dezember!"
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
            },
            
            "Oktoberfest": {
                "emotional_hooks": [
                    "Feiern Sie das größte Volksfest der Welt",
                    "Bringen Sie Oktoberfest-Stimmung nach Hause",
                    "Das perfekte Geschenk für Oktoberfest-Fans",
                    "O'zapft is! Zeit für die richtigen Accessoires",
                    "Münchner Gemütlichkeit das ganze Jahr"
                ],
                "title_patterns": [
                    "Oktoberfest Geschenk {product} - {benefit} - Bayrische Tradition",
                    "{product} Oktoberfest Edition - {feature} für das Volksfest",
                    "Wiesn-Special {product} - {benefit} für echte Bayern",
                    "Oktoberfest Essential {product} - {unique_feature} zur Wiesn"
                ],
                "power_words": ["Oktoberfest", "Wiesn", "bayrisch", "Volksfest", "traditionell", "Lederhosen", "Dirndl", "gemütlich"],
                "urgency_phrases": ["Rechtzeitig zur Wiesn bestellen", "Oktoberfest-Lieferung verfügbar", "Limitierte Oktoberfest-Edition"],
                "bullet_starters": [
                    "OKTOBERFEST-BEREIT:",
                    "WIESN-ESSENTIAL:",
                    "BAYRISCHE TRADITION:",
                    "VOLKSFEST-PERFEKT:",
                    "MÜNCHNER GEMÜTLICHKEIT:"
                ],
                "keywords": [
                    "oktoberfest geschenk", "wiesn accessoire", "oktoberfest artikel",
                    "oktoberfest zubehör", "volksfest geschenk", "bayrisches geschenk",
                    "oktoberfest {product_type}", "wiesn ausstattung", "oktoberfest tradition",
                    "münchner oktoberfest", "oktoberfest souvenir"
                ],
                "description_hooks": [
                    "Oktoberfest ist mehr als nur ein Fest – es ist ein Lebensgefühl.",
                    "Von der Wiesn direkt zu Ihnen nach Hause.",
                    "Echte Bayern wissen: zur Wiesn gehört die richtige Ausstattung."
                ],
                "gift_messaging": "Oktoberfest-Geschenkverpackung verfügbar. Wiesn-Grüße inklusive!",
                "seasonal_context": "Oktoberfest (September-Oktober) - O'zapft is!"
            },
            
            "Karneval": {
                "emotional_hooks": [
                    "Alaaf und Helau - die fünfte Jahreszeit beginnt",
                    "Bringen Sie Karnevalsstimmung in Ihre Feier",
                    "Das perfekte Accessoire für die närrische Zeit",
                    "Karneval ohne Grenzen - feiern Sie mit",
                    "Von Köln bis Mainz - Karneval vereint uns alle"
                ],
                "title_patterns": [
                    "Karneval Geschenk {product} - {benefit} - Närrische Zeit",
                    "{product} Fasching Edition - {feature} für die fünfte Jahreszeit",
                    "Karnevals-Special {product} - {benefit} zum Feiern",
                    "Alaaf! {product} - {unique_feature} für echte Narren"
                ],
                "power_words": ["Karneval", "Fasching", "närrisch", "Alaaf", "Helau", "fünfte Jahreszeit", "Kostüm", "Party"],
                "urgency_phrases": ["Rechtzeitig zu Karneval bestellen", "Faschings-Lieferung garantiert", "Karnevalsvorrat wird knapp"],
                "bullet_starters": [
                    "KARNEVALS-BEREIT:",
                    "NÄRRISCH GUT:",
                    "FASCHING-ESSENTIAL:",
                    "PARTY-PERFEKT:",
                    "ALAAF & HELAU:"
                ],
                "keywords": [
                    "karneval geschenk", "fasching zubehör", "karnevals artikel",
                    "karneval accessoire", "fasching geschenk", "närrisches geschenk",
                    "karneval {product_type}", "faschings ausstattung", "karnevals tradition",
                    "kölner karneval", "mainzer fastnacht", "karnevals party"
                ],
                "description_hooks": [
                    "Karneval ist die Zeit, in der alles möglich ist.",
                    "Alaaf! Die fünfte Jahreszeit ruft nach den richtigen Accessoires.",
                    "Von Weiberfastnacht bis Aschermittwoch - feiern Sie richtig."
                ],
                "gift_messaging": "Karnevals-Geschenkverpackung. Alaaf-Grüße inklusive!",
                "seasonal_context": "Karnevals-Saison (Februar-März) - Alaaf und Helau!"
            },
            
            # SPANISH OCCASIONS 🇪🇸
            "Navidad": {
                "emotional_hooks": [
                    "Haz de esta Navidad la más especial",
                    "El regalo que realmente van a usar después de Reyes",
                    "Porque la Navidad se trata de crear momentos inolvidables",
                    "Dale un toque mágico a sus fiestas navideñas",
                    "El detalle perfecto para completar la Nochebuena"
                ],
                "title_patterns": [
                    "Regalo de Navidad {product} - {benefit} - Perfecto para las Fiestas",
                    "{product} Edición Navideña - {feature} para Navidad",
                    "Especial Navidad {product} - {benefit} Bajo el Árbol",
                    "Regalo Navideño Perfecto - {product} con {unique_feature}"
                ],
                "power_words": ["navideño", "fiestas", "navidad", "nochebuena", "villancico", "tradición", "familia", "celebración"],
                "urgency_phrases": ["Pedidos antes del 15 de diciembre para Navidad", "Entrega navideña garantizada", "Stock limitado navideño"],
                "bullet_starters": [
                    "REGALO NAVIDEÑO PERFECTO:",
                    "ESENCIAL PARA LAS FIESTAS:",
                    "NAVIDAD INOLVIDABLE:",
                    "TRADICIÓN FAMILIAR:",
                    "MAGIA NAVIDEÑA:"
                ],
                "keywords": [
                    "regalo navidad", "regalo navideño", "navidad 2024",
                    "regalo familia navidad", "nochebuena regalo", "fiestas navideñas",
                    "navidad {product_type}", "regalos bajo el árbol", "tradición navideña",
                    "mejores regalos navidad", "regalo especial navidad"
                ],
                "description_hooks": [
                    "Esta Navidad, regala algo que recordarán mucho después de que se acaben los turrones.",
                    "Imagínate su cara la mañana de Navidad cuando abran este regalo.",
                    "Las mejores navidades se construyen con detalles que importan."
                ],
                "gift_messaging": "Envoltorio navideño gratuito. Incluye tarjeta personalizada para Navidad.",
                "seasonal_context": "Navidad española - Entrega garantizada antes del 25 de diciembre!"
            },
            
            "Reyes Magos": {
                "emotional_hooks": [
                    "Para que los Reyes Magos traigan algo realmente especial",
                    "El regalo que sus majestades de Oriente aprobarían",
                    "Más emocionante que encontrar carbón en el zapato",
                    "La ilusión del 6 de enero merece el mejor regalo",
                    "Tradición española que nunca pasa de moda"
                ],
                "title_patterns": [
                    "Regalo Reyes Magos {product} - {benefit} - 6 de Enero Especial",
                    "{product} para Reyes - {feature} Melchor, Gaspar y Baltasar",
                    "Especial Reyes Magos {product} - {benefit} Ilusión de Enero",
                    "Regalo de Reyes Perfecto - {product} con {unique_feature}"
                ],
                "power_words": ["reyes magos", "melchor", "gaspar", "baltasar", "ilusión", "tradición", "enero", "zapatos", "cabalgata"],
                "urgency_phrases": ["Pedidos antes del 3 de enero para Reyes", "Los Reyes llegan el 6 de enero", "Entrega especial Reyes Magos"],
                "bullet_starters": [
                    "REGALO DE REYES PERFECTO:",
                    "ILUSIÓN DEL 6 DE ENERO:",
                    "TRADICIÓN ESPAÑOLA:",
                    "MAGIA DE LOS REYES:",
                    "ESPECIAL MELCHOR, GASPAR Y BALTASAR:"
                ],
                "keywords": [
                    "regalo reyes magos", "reyes magos 2025", "6 enero regalo",
                    "cabalgata reyes", "tradición reyes magos", "ilusión enero",
                    "reyes {product_type}", "melchor gaspar baltasar", "zapatos reyes",
                    "mejores regalos reyes magos", "regalo especial 6 enero"
                ],
                "description_hooks": [
                    "Los Reyes Magos saben que los mejores regalos son los que se usan todo el año.",
                    "Este 6 de enero, que la ilusión venga acompañada de un regalo útil.",
                    "Mantén viva la magia de los Reyes Magos con un regalo que realmente emocione."
                ],
                "gift_messaging": "Envoltorio especial Reyes Magos. Los Reyes saben que es especial.",
                "seasonal_context": "Reyes Magos - La tradición española más querida (6 de enero)!"
            },
            
            "Día de la Madre": {
                "emotional_hooks": [
                    "Porque mamá se merece más que flores que se marchitan",
                    "Para la mujer que siempre piensa en todos menos en ella",
                    "El detalle que le demuestre cuánto la quieres",
                    "Hacer que este Día de la Madre sea su favorito",
                    "Para la reina de la casa que lo merece todo"
                ],
                "title_patterns": [
                    "Regalo Día de la Madre - {product} que Mamá Adorará - {benefit}",
                    "Perfecto para Mamá - {product} con {feature} - Especial Día de la Madre",
                    "{product} Edición Día de la Madre - {benefit} para Mamás",
                    "Regalo Especial Mamá - {product} Día de la Madre"
                ],
                "power_words": ["mamá", "madre", "maternal", "cariño", "amor", "familia", "dedicación", "especial", "querida"],
                "urgency_phrases": ["Pedidos antes del 4 de mayo para el Día de la Madre", "Entrega Día de la Madre garantizada", "Stock especial mamás"],
                "bullet_starters": [
                    "MAMÁ LO ADORARÁ:",
                    "PERFECTO PARA MAMÁS:",
                    "ESPECIAL DÍA DE LA MADRE:",
                    "CARIÑO Y FUNCIONALIDAD:",
                    "REGALO MATERNAL IDEAL:"
                ],
                "keywords": [
                    "regalo dia madre", "regalo para mama", "dia madre españa",
                    "regalo mamá especial", "mayo regalo madre", "mejor regalo mama",
                    "dia madre {product_type}", "regalos madres 2025", "mama regalo",
                    "detalles dia madre", "regalo maternal"
                ],
                "description_hooks": [
                    "Mamá ha pasado años cuidando de todos. Este Día de la Madre, es su turno.",
                    "No es solo otro regalo del Día de la Madre que acabará olvidado en un cajón.",
                    "El tipo de regalo que hace que mamá diga 'cómo sabías que lo necesitaba'."
                ],
                "gift_messaging": "Envoltorio especial Día de la Madre. Incluye mensaje personalizado para mamá.",
                "seasonal_context": "Día de la Madre España (primer domingo de mayo) - ¡Demuéstrale tu cariño!"
            },
            
            "San Valentín": {
                "emotional_hooks": [
                    "Porque 'te quiero' merece más que palabras",
                    "Convierte el 14 de febrero en su recuerdo favorito",
                    "Olvídate de regalos cliché, regala algo que realmente usarán",
                    "Romance que se encuentra con la practicidad",
                    "El detalle perfecto para parejas que se entienden"
                ],
                "title_patterns": [
                    "Regalo San Valentín {product} - {benefit} - Especial Parejas",
                    "{product} Edición San Valentín - {feature} para Enamorados",
                    "Perfecto San Valentín - {product} con {unique_feature}",
                    "Regalo Romántico {product} - San Valentín Especial"
                ],
                "power_words": ["romántico", "amor", "parejas", "cariño", "san valentín", "corazón", "enamorados", "especial", "íntimo"],
                "urgency_phrases": ["Pedidos antes del 12 de febrero para San Valentín", "Entrega San Valentín garantizada", "Stock limitado San Valentín"],
                "bullet_starters": [
                    "PERFECCIÓN SAN VALENTÍN:",
                    "ROMÁNTICO Y PRÁCTICO:",
                    "AMOR REAL:",
                    "PAREJAS LO ADORARÁN:",
                    "DETALLE ROMÁNTICO:"
                ],
                "keywords": [
                    "regalo san valentin", "san valentin parejas", "14 febrero regalo",
                    "regalo romantico", "san valentin especial", "amor regalo",
                    "san valentin {product_type}", "regalos enamorados", "parejas san valentin",
                    "mejores regalos san valentin", "detalle romantico"
                ],
                "description_hooks": [
                    "Este San Valentín, olvídate de las flores que se marchitan y los chocolates que desaparecen.",
                    "El amor está en los detalles, y este {product} lo demuestra.",
                    "Transforma San Valentín de predecible a inolvidable."
                ],
                "gift_messaging": "Envoltorio romántico disponible. Añade tu mensaje de amor personalizado.",
                "seasonal_context": "San Valentín español - ¡El detalle perfecto para el 14 de febrero!"
            },
            
            "Día del Padre": {
                "emotional_hooks": [
                    "Para el papá que dice que no necesita nada",
                    "Demuestra a papá que es más que el manitas de la casa",
                    "Porque papá se merece más que otra corbata",
                    "Hacer que el Día del Padre signifique algo de verdad",
                    "El regalo del que papá presumirá"
                ],
                "title_patterns": [
                    "Regalo Día del Padre - {product} que Papá Usará Siempre - {benefit}",
                    "Perfecto para Papá - {product} con {feature} - Día del Padre",
                    "{product} Edición Día del Padre - {benefit} para Papás",
                    "Regalo Especial Papá - {product} Día del Padre"
                ],
                "power_words": ["papá", "padre", "paternal", "familia", "práctico", "útil", "resistente", "calidad", "duradero"],
                "urgency_phrases": ["Pedidos antes del 17 de marzo para el Día del Padre", "Entrega Día del Padre garantizada", "Aprobado por papás"],
                "bullet_starters": [
                    "PAPÁ LO ADORARÁ:",
                    "GANADOR DÍA DEL PADRE:",
                    "PRÁCTICO PARA PAPÁ:",
                    "CALIDAD APROBADA PAPÁ:",
                    "ESENCIAL PARA PADRES:"
                ],
                "keywords": [
                    "regalo dia padre", "regalo para papa", "dia padre españa",
                    "regalo papa especial", "marzo regalo padre", "mejor regalo papa",
                    "dia padre {product_type}", "regalos padres 2025", "papa regalo",
                    "detalles dia padre", "regalo paternal"
                ],
                "description_hooks": [
                    "Papá ha pasado años siendo el héroe de todos. Es hora de devolverle el favor.",
                    "Este Día del Padre, regala a papá algo que realmente usará, no solo agradecerá.",
                    "El tipo de regalo que hace que papá diga 'cómo sabías que necesitaba esto'."
                ],
                "gift_messaging": "Envoltorio Día del Padre disponible. Añade tu mensaje para papá.",
                "seasonal_context": "Día del Padre España (19 de marzo) - ¡Demuestra que papá es especial!"
            },
            
            "Semana Santa": {
                "emotional_hooks": [
                    "Para una Semana Santa de recogimiento y familia",
                    "El detalle perfecto para las vacaciones de Pascua",
                    "Celebra la renovación y los nuevos comienzos",
                    "Tradición española que merece regalos especiales",
                    "Para disfrutar en familia durante las vacaciones"
                ],
                "title_patterns": [
                    "Especial Semana Santa - {product} para las Vacaciones - {benefit}",
                    "{product} Semana Santa - {feature} para Pascua",
                    "Perfecto Semana Santa - {product} con {unique_feature}",
                    "Vacaciones Pascua {product} - Especial Abril"
                ],
                "power_words": ["semana santa", "pascua", "vacaciones", "tradición", "familia", "descanso", "renovación", "primavera", "celebración"],
                "urgency_phrases": ["Entrega antes de Semana Santa", "Especial vacaciones Pascua", "Stock limitado Semana Santa"],
                "bullet_starters": [
                    "PERFECTO SEMANA SANTA:",
                    "VACACIONES PASCUA:",
                    "TRADICIÓN FAMILIAR:",
                    "DESCANSO MERECIDO:",
                    "RENOVACIÓN PRIMAVERAL:"
                ],
                "keywords": [
                    "semana santa regalo", "pascua regalo", "vacaciones pascua",
                    "semana santa especial", "abril regalo", "tradicion pascua",
                    "semana santa {product_type}", "vacaciones familia", "pascua españa",
                    "regalo vacaciones pascua", "semana santa familia"
                ],
                "description_hooks": [
                    "Esta Semana Santa, añade un toque especial a las vacaciones familiares.",
                    "Las tradiciones se mantienen vivas con detalles que importan.",
                    "Celebra la renovación de la primavera con algo verdaderamente útil."
                ],
                "gift_messaging": "Presentación especial Semana Santa. Perfecto para las vacaciones.",
                "seasonal_context": "Semana Santa española - Tradición, familia y descanso merecido!"
            },
            
            "Día de Andalucía": {
                "emotional_hooks": [
                    "Celebra el orgullo andaluz con estilo",
                    "Para los que llevan Andalucía en el corazón",
                    "Tradición andaluza que merece ser celebrada",
                    "El detalle perfecto para el 28 de febrero",
                    "Andalucía universal, calidad excepcional"
                ],
                "title_patterns": [
                    "Especial Día de Andalucía - {product} Andaluz - {benefit}",
                    "{product} Andalucía - {feature} para el 28 de Febrero",
                    "Orgullo Andaluz {product} - {benefit} Tradición",
                    "Día de Andalucía {product} - Especial Regional"
                ],
                "power_words": ["andaluz", "andalucía", "tradición", "orgullo", "regional", "tierra", "cultura", "celebración", "febrero"],
                "urgency_phrases": ["Especial 28 de febrero", "Edición Día de Andalucía", "Orgullo andaluz garantizado"],
                "bullet_starters": [
                    "ORGULLO ANDALUZ:",
                    "TRADICIÓN REGIONAL:",
                    "ANDALUCÍA UNIVERSAL:",
                    "28 FEBRERO ESPECIAL:",
                    "CULTURA ANDALUZA:"
                ],
                "keywords": [
                    "dia andalucia regalo", "28 febrero regalo", "andalucia especial",
                    "orgullo andaluz", "tradicion andaluza", "andalucia regalo",
                    "dia andalucia {product_type}", "febrero andalucia", "regional andaluz",
                    "celebracion andaluza", "cultura andaluza"
                ],
                "description_hooks": [
                    "El 28 de febrero celebramos lo que nos hace únicos como andaluces.",
                    "Andalucía se lleva en el corazón, y este regalo lo demuestra.",
                    "Tradición andaluza con la calidad que nos caracteriza."
                ],
                "gift_messaging": "Presentación especial Día de Andalucía. Orgullo andaluz incluido.",
                "seasonal_context": "Día de Andalucía (28 febrero) - Celebra la tierra que nos vió nacer!"
            },
            
            # JAPANESE OCCASIONS 🇯🇵
            "正月": {
                "emotional_hooks": [
                    "新年を迎える特別な準備をしましょう",
                    "お正月にふさわしい品質の良い商品",
                    "新しい年に新しい生活の質を",
                    "家族みんなで迎える新年にぴったり",
                    "一年の始まりを大切にする方へ"
                ],
                "title_patterns": [
                    "お正月ギフト {product} - {benefit} - 新年特別版",
                    "{product} 正月特別仕様 - {feature} で新年を",
                    "新年プレゼント {product} - {benefit} 正月限定",
                    "お正月用 {product} - {unique_feature} 付き"
                ],
                "power_words": ["正月", "新年", "お年玉", "初売り", "年始", "祝い", "家族", "伝統", "縁起"],
                "urgency_phrases": ["お正月配送対応", "年始営業開始", "初売り特価"],
                "bullet_starters": [
                    "お正月にぴったり:",
                    "新年の贈り物に:",
                    "家族で楽しめる:",
                    "縁起の良い:",
                    "正月準備完了:"
                ],
                "keywords": [
                    "正月 ギフト", "新年 プレゼント", "お年玉",
                    "正月 用品", "新年 準備", "初売り",
                    "正月 {product_type}", "年始 セール", "正月 限定",
                    "家族 正月", "お正月 商品"
                ],
                "description_hooks": [
                    "新年は新しいものでスタートしませんか。",
                    "お正月の特別な時間にふさわしい品質です。",
                    "家族みんなで迎える新年を、より特別なものに。"
                ],
                "gift_messaging": "お正月ギフト包装承ります。新年のお祝いにぜひ。",
                "seasonal_context": "お正月(1月1日-3日) - 新年を迎える日本の最重要行事!"
            },
            
            "ゴールデンウィーク": {
                "emotional_hooks": [
                    "ゴールデンウィークを最高に楽しもう",
                    "連休だからこそできる特別な体験を",
                    "家族との時間をより充実させる",
                    "長期休暇を有効活用するために",
                    "旅行や外出をもっと快適に"
                ],
                "title_patterns": [
                    "GW特別企画 {product} - {benefit} - 連休対応",
                    "{product} ゴールデンウィーク仕様 - {feature}",
                    "連休にぴったり {product} - {benefit} GW版",
                    "GW旅行用 {product} - {unique_feature}"
                ],
                "power_words": ["GW", "連休", "旅行", "レジャー", "アウトドア", "家族時間", "休暇", "外出", "楽しい"],
                "urgency_phrases": ["GW前配送", "連休対応", "ゴールデンウィーク限定"],
                "bullet_starters": [
                    "GW旅行に最適:",
                    "連休の外出に:",
                    "家族レジャーに:",
                    "アウトドアで活躍:",
                    "長期休暇対応:"
                ],
                "keywords": [
                    "ゴールデンウィーク", "GW 旅行", "連休 グッズ",
                    "レジャー 用品", "家族旅行", "外出 便利",
                    "GW {product_type}", "連休 準備", "旅行 必需品",
                    "アウトドア", "休暇 楽しみ"
                ],
                "description_hooks": [
                    "ゴールデンウィークの思い出づくりをお手伝いします。",
                    "連休だからこそ、いつもより特別な体験を。",
                    "家族との時間を、もっと充実したものに変えてみませんか。"
                ],
                "gift_messaging": "GW旅行準備完了。連休を存分にお楽しみください。",
                "seasonal_context": "ゴールデンウィーク(4月29日-5月5日) - 日本の大型連休!"
            },
            
            "お盆": {
                "emotional_hooks": [
                    "お盆の帰省時に家族に喜ばれる",
                    "先祖を敬う心を込めた贈り物",
                    "夏の帰省土産にぴったり",
                    "久しぶりに会う家族への気遣い",
                    "お盆休みをより充実したものに"
                ],
                "title_patterns": [
                    "お盆ギフト {product} - {benefit} - 帰省土産に",
                    "{product} お盆特別版 - {feature} で夏を",
                    "夏の帰省用 {product} - {benefit} お盆限定",
                    "お盆休み用 {product} - {unique_feature}"
                ],
                "power_words": ["お盆", "帰省", "夏休み", "家族", "先祖", "伝統", "土産", "夏", "休暇"],
                "urgency_phrases": ["お盆配送対応", "帰省前お届け", "夏季限定"],
                "bullet_starters": [
                    "お盆帰省に:",
                    "夏の家族時間に:",
                    "帰省土産として:",
                    "お盆休みに:",
                    "夏季使用最適:"
                ],
                "keywords": [
                    "お盆 ギフト", "帰省 土産", "夏休み",
                    "お盆 用品", "夏季 限定", "家族 集合",
                    "お盆 {product_type}", "帰省 準備", "夏 プレゼント",
                    "お盆休み", "夏季 商品"
                ],
                "description_hooks": [
                    "お盆の帰省時に、家族みんなで使えるものを。",
                    "久しぶりに集まる家族への心のこもった贈り物です。",
                    "夏のお盆休みを、より思い出深いものにしませんか。"
                ],
                "gift_messaging": "お盆帰省ギフト対応。家族への思いやりを形に。",
                "seasonal_context": "お盆(8月13日-16日) - 先祖を敬う日本の夏の伝統行事!"
            },
            
            "敬老の日": {
                "emotional_hooks": [
                    "おじいちゃん、おばあちゃんに感謝を込めて",
                    "長寿をお祝いする特別な贈り物",
                    "日頃の感謝の気持ちを形にして",
                    "健康で長生きしてほしいという願いを込めて",
                    "世代を超えた愛情を表現する"
                ],
                "title_patterns": [
                    "敬老の日ギフト {product} - {benefit} - 感謝込めて",
                    "{product} 敬老の日特別版 - {feature} でお祝い",
                    "おじいちゃんおばあちゃんに {product} - {benefit}",
                    "敬老の日プレゼント {product} - {unique_feature}"
                ],
                "power_words": ["敬老", "感謝", "長寿", "健康", "おじいちゃん", "おばあちゃん", "祖父母", "孝行", "愛情"],
                "urgency_phrases": ["敬老の日配送", "9月第3月曜配達", "感謝の気持ちお届け"],
                "bullet_starters": [
                    "祖父母に最適:",
                    "敬老の日に:",
                    "感謝を込めて:",
                    "健康願って:",
                    "長寿お祝い:"
                ],
                "keywords": [
                    "敬老の日", "祖父母 ギフト", "おじいちゃん プレゼント",
                    "おばあちゃん 贈り物", "長寿 祝い", "感謝 気持ち",
                    "敬老 {product_type}", "高齢者 向け", "シニア 用品",
                    "祖父母 思い", "敬老 感謝"
                ],
                "description_hooks": [
                    "いつも優しいおじいちゃん、おばあちゃんに感謝を込めて。",
                    "長い人生を歩んでこられた方々への尊敬と愛情を表現します。",
                    "健康で長生きしてほしいという願いを込めた贈り物です。"
                ],
                "gift_messaging": "敬老の日ギフト包装。感謝の気持ちを丁寧にお包みします。",
                "seasonal_context": "敬老の日(9月第3月曜日) - 祖父母への感謝を表現する日!"
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
    
    def get_walmart_usa_occasion_enhancement(self, occasion):
        """Get Walmart USA specific occasion enhancements with American culture focus"""
        walmart_occasions = {
            "black_friday": """
🛒 WALMART BLACK FRIDAY DOORBUSTER OPTIMIZATION 🛒

CRITICAL WALMART BLACK FRIDAY REQUIREMENTS:
✓ Title MUST include "Black Friday Deal" or "Doorbuster Price"  
✓ Features emphasize VALUE: "Rollback Price", "Lowest Price of Year"
✓ Description opens with "Black Friday Exclusive" or similar
✓ Include urgency: "Limited Time", "While Supplies Last", "Doorbuster Hours Only"
✓ Walmart integration: "Pickup Available", "Same Day Delivery", "Price Match Guarantee"
✓ American values: "Made in USA", "Supporting American Families"

WALMART BLACK FRIDAY POWER LANGUAGE:
- "Rollback to Lowest Price" - "Early Bird Doorbuster" - "Black Friday Exclusive"
- "Save Big This Friday" - "Thanksgiving Weekend Deal" - "Holiday Savings Start Now"
- "Beat the Crowds - Order Online" - "Free Store Pickup" - "2-Day Free Shipping"

DESCRIPTION STRUCTURE:
Paragraph 1: Black Friday exclusive pricing and Walmart advantages
Paragraph 2: Product benefits with savings emphasis  
Paragraph 3: American family values and quality assurance
Paragraph 4: Walmart pickup/delivery options and urgency

MANDATORY ELEMENTS:
□ Black Friday prominently in title and features
□ Walmart-specific language (rollback, pickup, price match)
□ American family benefits and values
□ Urgency and scarcity messaging
□ Free shipping and pickup options highlighted
""",
            
            "christmas": """
🎄 WALMART CHRISTMAS FAMILY GIFT OPTIMIZATION 🎄

CRITICAL WALMART CHRISTMAS REQUIREMENTS:
✓ Title includes "Christmas Gift" or "Holiday Special"
✓ Features emphasize FAMILY: "Perfect for Families", "All Ages"
✓ Description focuses on American Christmas traditions
✓ Include gift messaging: "Gift Receipt Included", "Easy Returns"
✓ Walmart advantages: "Free Gift Wrap", "Christmas Eve Pickup Available"
✓ American Christmas: "Under the Tree", "Christmas Morning Magic"

WALMART CHRISTMAS POWER LANGUAGE:
- "Christmas Morning Surprise" - "Under the Christmas Tree" - "Holiday Magic"
- "Family Traditions" - "American Christmas" - "Santa Approved"
- "Gift Wrap Available" - "Christmas Eve Pickup" - "Easy Gift Returns"

DESCRIPTION STRUCTURE:
Paragraph 1: Christmas magic and family gift appeal
Paragraph 2: Product creates lasting Christmas memories
Paragraph 3: American family Christmas traditions
Paragraph 4: Walmart gift services and hassle-free returns

MANDATORY ELEMENTS:
□ Christmas prominently featured in title and bullets
□ American family Christmas traditions referenced
□ Walmart gift services highlighted (wrap, pickup, returns)
□ Family togetherness and memory-making emphasized
□ Easy gift-giving process with Walmart advantages
""",
            
            "thanksgiving": """
🦃 WALMART THANKSGIVING FAMILY GATHERING OPTIMIZATION 🦃

CRITICAL WALMART THANKSGIVING REQUIREMENTS:
✓ Title includes "Thanksgiving" or "Family Gathering"
✓ Features emphasize HOSTING: "Perfect for Entertaining", "Family Dinners"
✓ Description focuses on gratitude and American traditions
✓ Include family benefits: "Brings Family Together", "Creates Memories"
✓ Walmart convenience: "Same Day Pickup", "Last Minute Shopping"
✓ American values: "Grateful Families", "Thanksgiving Traditions"

WALMART THANKSGIVING POWER LANGUAGE:
- "Thanksgiving Memories" - "Family Gathering Essential" - "Grateful Hearts"
- "American Tradition" - "Thanksgiving Dinner" - "Family Togetherness"
- "Last Minute Pickup" - "Thanksgiving Day Delivery" - "Family Approved"

DESCRIPTION STRUCTURE:
Paragraph 1: Thanksgiving family gathering enhancement
Paragraph 2: Product brings families together with gratitude
Paragraph 3: American Thanksgiving traditions and memories
Paragraph 4: Walmart convenience for busy families

MANDATORY ELEMENTS:
□ Thanksgiving family focus in title and features
□ American gratitude and tradition references
□ Family gathering and hosting benefits
□ Walmart convenience for holiday preparations
□ Memory-making and togetherness emphasis
""",
            
            "independence_day": """
🇺🇸 WALMART JULY 4TH PATRIOTIC OPTIMIZATION 🇺🇸

CRITICAL WALMART JULY 4TH REQUIREMENTS:
✓ Title includes "July 4th", "Independence Day", or "Patriotic"
✓ Features emphasize AMERICAN PRIDE: "Made in USA", "Supports Veterans"
✓ Description celebrates American freedom and family
✓ Include patriotic elements: "Red White Blue", "Star Spangled"
✓ Walmart American values: "Supporting American Workers", "Local Communities"
✓ Celebration focus: "Backyard BBQ", "Family Celebration", "Freedom Party"

WALMART JULY 4TH POWER LANGUAGE:
- "Celebrate America" - "Independence Day Special" - "Patriotic Pride"
- "Red White and Blue" - "Freedom Celebration" - "American Made"
- "Support Our Troops" - "Land of the Free" - "American Family Values"

DESCRIPTION STRUCTURE:
Paragraph 1: Independence Day celebration and American pride
Paragraph 2: Product enhances patriotic gatherings and family fun
Paragraph 3: American values, quality, and supporting local communities
Paragraph 4: Walmart's commitment to American families and values

MANDATORY ELEMENTS:
□ July 4th/Independence Day prominently featured
□ American patriotic values and pride emphasized
□ Red, white, blue color schemes or themes
□ Family celebration and gathering focus
□ Made in USA or American quality highlighted
""",
            
            "mothers_day": """
👩 WALMART MOTHER'S DAY APPRECIATION OPTIMIZATION 👩

CRITICAL WALMART MOTHER'S DAY REQUIREMENTS:
✓ Title includes "Mother's Day Gift" or "For Mom"
✓ Features emphasize MOM APPRECIATION: "Shows You Care", "Mom Deserves Best"
✓ Description honors hardworking American mothers
✓ Include emotional appeal: "Thank You Mom", "Mother's Love"
✓ Walmart convenience: "Easy Gift Pickup", "Mom-Approved Quality"
✓ Family values: "Family Hero", "Supermom", "American Motherhood"

WALMART MOTHER'S DAY POWER LANGUAGE:
- "Thank You Mom" - "Mother's Day Special" - "Mom Appreciation"
- "Supermom Deserves" - "Best Mom Ever" - "Mother's Love"
- "Easy Gift Pickup" - "Mom-Approved" - "Family First"

DESCRIPTION STRUCTURE:
Paragraph 1: Mother's Day appreciation and gift appeal
Paragraph 2: Product shows love and appreciation for mom
Paragraph 3: American mom values and family importance
Paragraph 4: Walmart makes gift-giving easy for busy families

MANDATORY ELEMENTS:
□ Mother's Day gift focus in title and features
□ Mom appreciation and love emphasized
□ American family values and motherhood
□ Easy gift-giving with Walmart convenience
□ Quality that shows mom she's valued
""",
            
            "super_bowl": """
🏈 WALMART SUPER BOWL PARTY OPTIMIZATION 🏈

CRITICAL WALMART SUPER BOWL REQUIREMENTS:
✓ Title includes "Super Bowl" or "Game Day"
✓ Features emphasize PARTY HOSTING: "Perfect for Parties", "Game Day Essential"
✓ Description focuses on American football traditions
✓ Include party benefits: "Crowd Pleaser", "Party MVP"
✓ Walmart party convenience: "Party Supplies Available", "Same Day Pickup"
✓ American sports culture: "Football Sunday", "Team Spirit", "Championship"

WALMART SUPER BOWL POWER LANGUAGE:
- "Game Day Ready" - "Super Bowl Party" - "Football Sunday"
- "Team Spirit" - "Championship Quality" - "Party MVP"
- "Touchdown Deal" - "Game Time" - "All-American Fun"

DESCRIPTION STRUCTURE:
Paragraph 1: Super Bowl party enhancement and game day excitement
Paragraph 2: Product makes you the party MVP with team spirit
Paragraph 3: American football culture and championship quality
Paragraph 4: Walmart party convenience and sports fan support

MANDATORY ELEMENTS:
□ Super Bowl/Game Day prominently featured
□ American football culture and team spirit
□ Party hosting and entertainment focus
□ Walmart convenience for party planning
□ Championship quality and winning attitude
"""
        }
        
        return walmart_occasions.get(occasion.lower(), None)
    
    def get_walmart_canada_occasion_enhancement(self, occasion):
        """Get Walmart Canada specific occasion enhancements with Canadian culture focus and bilingual compliance"""
        walmart_canada_occasions = {
            "boxing_day": """
🇨🇦 WALMART CANADA BOXING DAY MEGA SALE OPTIMIZATION 🇨🇦

CRITICAL WALMART CANADA BOXING DAY REQUIREMENTS:
✓ Title MUST include "Boxing Day Sale" or "Boxing Day Special"
✓ Features emphasize CANADIAN VALUE: "Rollback Price Canada", "Coast to Coast Savings"
✓ Description opens with "Boxing Day Exclusive Canada" or similar
✓ Include urgency: "December 26th Only", "Limited Time Canada", "While Supplies Last"
✓ Walmart Canada integration: "Free Pickup Canada", "Same Day Delivery", "Price Match Canada"
✓ Canadian values: "Canadian Quality", "Supporting Canadian Families"

WALMART CANADA BOXING DAY POWER LANGUAGE:
- "Rollback to Lowest Canadian Price" - "Boxing Day Doorbuster Canada" - "Post-Christmas Exclusive"
- "Coast to Coast Savings" - "Canadian Boxing Day Tradition" - "Holiday Clearance Event"
- "Beat the Crowds - Order Online Canada" - "Free Store Pickup" - "Bilingual Customer Service"

BILINGUAL COMPLIANCE NOTES:
- Ready for French translation per Canadian law
- Use clear, translatable language structure
- Avoid idioms that don't translate well
""",
            
            "canada_day": """
🇨🇦 WALMART CANADA DAY CELEBRATION OPTIMIZATION 🇨🇦

CRITICAL WALMART CANADA DAY REQUIREMENTS:
✓ Title MUST include "Canada Day Special" or "July 1st Celebration"
✓ Features emphasize PATRIOTIC CANADIAN VALUE: "True North Strong", "Coast to Coast Pride"
✓ Description opens with "Celebrate Canada Day" or "Oh Canada Special"
✓ Include Canadian pride: "Made in Canada", "Canadian Heritage", "From Sea to Sea"
✓ Walmart Canada integration: "Available Nationwide", "Canadian Customers", "Bilingual Service"
✓ Canadian values: "Maple Leaf Quality", "Canadian Family Values"

WALMART CANADA DAY POWER LANGUAGE:
- "True North Strong and Free" - "Coast to Coast Celebration" - "Canadian Pride Special"
- "From Sea to Sea Savings" - "Oh Canada Deals" - "Red and White Sale"
- "Canadian Heritage Quality" - "Bilingual Customer Support" - "Canadian Family Tradition"

CANADIAN CULTURAL ELEMENTS:
- Reference maple syrup, hockey, cottage country, winter sports
- Include "eh" appropriately and sparingly for authenticity
- Mention Canadian symbols: maple leaf, beaver, loon
""",
            
            "victoria_day": """
🇨🇦 WALMART CANADA VICTORIA DAY LONG WEEKEND OPTIMIZATION 🇨🇦

CRITICAL WALMART VICTORIA DAY REQUIREMENTS:
✓ Title MUST include "Victoria Day Sale" or "May Long Weekend"
✓ Features emphasize LONG WEEKEND VALUE: "May Two-Four Special", "Long Weekend Savings"
✓ Description opens with "Victoria Day Long Weekend" or "May Long Celebration"
✓ Include cottage prep: "Cottage Season Ready", "May Long Tradition", "Weekend Getaway"
✓ Walmart Canada integration: "Perfect for Cottage Country", "Canadian Outdoor Life"
✓ Canadian values: "Royal Heritage", "Canadian Tradition", "Coast to Coast Quality"

WALMART VICTORIA DAY POWER LANGUAGE:
- "May Long Weekend Special" - "Cottage Season Kickoff" - "Victoria Day Tradition"
- "Long Weekend Savings" - "May Two-Four Deals" - "Canadian Outdoor Ready"
- "Cottage Country Quality" - "Weekend Warrior Approved" - "Royal Quality Standards"

CANADIAN COTTAGE CULTURE:
- Reference cottage life, lake activities, camping
- Include May long weekend traditions
- Mention Canadian outdoor lifestyle
""",
            
            "thanksgiving": """
🇨🇦 WALMART CANADA THANKSGIVING OPTIMIZATION (OCTOBER) 🇨🇦

CRITICAL WALMART CANADA THANKSGIVING REQUIREMENTS:
✓ Title MUST include "Canadian Thanksgiving" or "October Thanksgiving"
✓ Features emphasize GRATITUDE & HARVEST: "Harvest Festival", "Canadian Thanksgiving Tradition"
✓ Description opens with "Canadian Thanksgiving Celebration" or "October Harvest"
✓ Include family gathering: "Family Feast", "Thanksgiving Dinner", "Grateful Hearts"
✓ Walmart Canada integration: "Coast to Coast Gratitude", "Canadian Family Tradition"
✓ Canadian values: "Harvest Abundance", "Family Unity", "Canadian Hospitality"

WALMART CANADA THANKSGIVING POWER LANGUAGE:
- "Canadian Thanksgiving Tradition" - "October Harvest Celebration" - "Family Feast Ready"
- "Grateful Hearts, Canadian Style" - "Coast to Coast Thanksgiving" - "Harvest Festival Quality"
- "Canadian Family Gathering" - "Thanksgiving Dinner Perfection" - "Autumn Celebration"

CANADIAN THANKSGIVING DISTINCTIONS:
- Emphasize October timing (not November like US)
- Reference Canadian harvest traditions
- Include maple syrup, Canadian agriculture
""",
            
            "christmas": """
🇨🇦 WALMART CANADA CHRISTMAS/NOËL OPTIMIZATION 🇨🇦

CRITICAL WALMART CANADA CHRISTMAS REQUIREMENTS:
✓ Title MUST include "Christmas Special" or "Holiday Gift Canada"
✓ Features emphasize CANADIAN CHRISTMAS: "Canadian Christmas Magic", "Coast to Coast Joy"
✓ Description opens with "Canadian Christmas Tradition" or "Holiday Magic Canada"
✓ Include bilingual elements: "Merry Christmas / Joyeux Noël"
✓ Walmart Canada integration: "Canadian Holiday Tradition", "Bilingual Gift Service"
✓ Canadian values: "Canadian Christmas Spirit", "Family Traditions", "Winter Wonderland"

WALMART CANADA CHRISTMAS POWER LANGUAGE:
- "Canadian Christmas Magic" - "Holiday Tradition Coast to Coast" - "Merry Christmas Canada"
- "Joyeux Noël Special" - "Canadian Winter Wonderland" - "Holiday Gift Perfection"
- "Canadian Family Christmas" - "Bilingual Holiday Service" - "True North Christmas Spirit"

BILINGUAL CHRISTMAS ELEMENTS:
- Ready for French translation: "Joyeux Noël"
- Reference Canadian Christmas traditions
- Include winter sports, skating, sledding
""",
            
            "hockey_season": """
🇨🇦 WALMART CANADA HOCKEY SEASON OPTIMIZATION 🇨🇦

CRITICAL WALMART CANADA HOCKEY REQUIREMENTS:
✓ Title MUST include "Hockey Season" or "Hockey Night Canada"
✓ Features emphasize HOCKEY CULTURE: "Hockey Night Ready", "Canadian Hockey Heritage"
✓ Description opens with "Hockey Season Special" or "Canadian Hockey Tradition"
✓ Include hockey terms: "On Ice Performance", "Hat Trick Quality", "Championship Grade"
✓ Walmart Canada integration: "Hockey Mom/Dad Approved", "Rink to Home Quality"
✓ Canadian values: "Hockey Heritage", "Ice to Ice Excellence", "Canadian Championship"

WALMART CANADA HOCKEY POWER LANGUAGE:
- "Hockey Night in Canada Special" - "On Ice Excellence" - "Canadian Hockey Heritage"
- "Hat Trick Performance" - "Championship Quality" - "Hockey Mom/Dad Approved"
- "From Rink to Home" - "Canadian Ice Legend" - "Hockey Season Ready"

CANADIAN HOCKEY CULTURE:
- Reference NHL, hockey nights, arena culture
- Include "hockey mom/dad" lifestyle
- Mention community rink traditions
""",
            
            "cottage_season": """
🇨🇦 WALMART CANADA COTTAGE SEASON OPTIMIZATION 🇨🇦

CRITICAL WALMART CANADA COTTAGE REQUIREMENTS:
✓ Title MUST include "Cottage Season" or "Lake House Ready"
✓ Features emphasize COTTAGE CULTURE: "Cottage Life Ready", "Muskoka Quality"
✓ Description opens with "Cottage Season Special" or "Lake Life Canada"
✓ Include cottage terms: "Dock to Cottage", "Lake Life Quality", "Cottage Country Grade"
✓ Walmart Canada integration: "Cottage Country Approved", "Lake to Lake Quality"
✓ Canadian values: "Cottage Heritage", "Lake Life Excellence", "Canadian Getaway"

WALMART CANADA COTTAGE POWER LANGUAGE:
- "Cottage Season Special Canada" - "Lake Life Excellence" - "Cottage Country Quality"
- "Dock to Cottage Performance" - "Muskoka Grade" - "Canadian Lake Life"
- "From City to Cottage" - "Lake House Legend" - "Cottage Weekend Ready"

CANADIAN COTTAGE CULTURE:
- Reference Muskoka, lake country, summer getaways
- Include "cottage weekend" lifestyle
- Mention fishing, boating, lake traditions
""",
            
            "winter_carnival": """
🇨🇦 WALMART CANADA WINTER CARNIVAL OPTIMIZATION 🇨🇦

CRITICAL WALMART CANADA WINTER CARNIVAL REQUIREMENTS:
✓ Title MUST include "Winter Carnival" or "Ice Festival"
✓ Features emphasize WINTER CULTURE: "Winter Festival Ready", "Canadian Winter Spirit"
✓ Description opens with "Winter Carnival Special" or "Ice Festival Canada"
✓ Include winter terms: "Snow to Ice", "Winter Magic Quality", "Carnival Grade"
✓ Walmart Canada integration: "Winter Festival Approved", "Coast to Coast Winter"
✓ Canadian values: "Winter Heritage", "Ice Festival Excellence", "Canadian Winter Joy"

WALMART CANADA WINTER CARNIVAL POWER LANGUAGE:
- "Winter Carnival Special Canada" - "Ice Festival Excellence" - "Canadian Winter Magic"
- "Snow to Ice Performance" - "Winter Festival Grade" - "Canadian Winter Spirit"
- "From Snow to Celebration" - "Winter Magic Legend" - "Ice Festival Ready"

CANADIAN WINTER CULTURE:
- Reference winter festivals, ice sculptures, snow activities
- Include winter sports culture
- Mention community winter celebrations
"""
        }
        
        return walmart_canada_occasions.get(occasion.lower(), None)
    
    def get_walmart_mexico_occasion_enhancement(self, occasion):
        """Get Walmart Mexico specific occasion enhancements with Mexican culture focus and Spanish localization"""
        walmart_mexico_occasions = {
            "dia_de_los_muertos": """
🇲🇽 WALMART MÉXICO DÍA DE LOS MUERTOS OPTIMIZATION 🇲🇽

CRITICAL WALMART MEXICO DÍA DE LOS MUERTOS REQUIREMENTS:
✓ Title MUST include "Día de los Muertos" or "Día Muertos"
✓ Features emphasize MEXICAN TRADITION: "Tradición Mexicana", "Cultura Ancestral"
✓ Description opens with "Día de los Muertos Especial" or "Celebra Día Muertos"
✓ Include cultural elements: "Altar de Muertos", "Ofrenda Especial", "Tradición Familiar"
✓ Walmart México integration: "Disponible en Todo México", "Servicio Nacional"
✓ Mexican values: "Tradición Mexicana", "Cultura Familiar", "Herencia Nacional"

WALMART MÉXICO DÍA DE LOS MUERTOS POWER LANGUAGE:
- "Día de los Muertos Especial México" - "Tradición Ancestral Mexicana" - "Altar Perfecto"
- "Ofrenda Familiar Especial" - "Cultura Nacional México" - "Tradición de Noviembre"
- "Recuerda a los Seres Queridos" - "Herencia Cultural" - "Mexicano y Orgulloso"

MEXICAN CULTURAL ELEMENTS:
- Reference altars, ofrendas, marigolds (cempasúchil), calaveras
- Include family tradition and remembrance themes
- Mention Mexican cultural heritage and UNESCO recognition
""",
            
            "las_posadas": """
🇲🇽 WALMART MÉXICO LAS POSADAS CELEBRATION OPTIMIZATION 🇲🇽

CRITICAL WALMART MEXICO LAS POSADAS REQUIREMENTS:
✓ Title MUST include "Las Posadas" or "Posadas Navideñas"
✓ Features emphasize CHRISTMAS TRADITION: "Tradición Navideña", "Celebración Familiar"
✓ Description opens with "Las Posadas Especial" or "Celebra Posadas"
✓ Include tradition elements: "9 Días de Celebración", "Diciembre 16-24", "Piñata Tradicional"
✓ Walmart México integration: "Perfecto para Posadas", "Celebración Nacional"
✓ Mexican values: "Tradición Familiar", "Navidad Mexicana", "Unión Familiar"

WALMART MÉXICO LAS POSADAS POWER LANGUAGE:
- "Las Posadas Tradición México" - "Celebración Navideña Familiar" - "9 Días Especiales"
- "Piñata y Diversión" - "Navidad Mexicana Auténtica" - "Diciembre Tradicional"
- "Familia Unida en Navidad" - "Posadas Perfectas" - "Tradición de Diciembre"

MEXICAN CHRISTMAS CULTURE:
- Reference the 9-day celebration, piñatas, ponche
- Include family gathering and Mexican Christmas traditions
- Mention December 16-24 timing and religious significance
""",
            
            "cinco_de_mayo": """
🇲🇽 WALMART MÉXICO CINCO DE MAYO CELEBRATION OPTIMIZATION 🇲🇽

CRITICAL WALMART MEXICO CINCO DE MAYO REQUIREMENTS:
✓ Title MUST include "Cinco de Mayo" or "5 de Mayo"
✓ Features emphasize MEXICAN PRIDE: "Orgullo Mexicano", "Victoria Histórica"
✓ Description opens with "Cinco de Mayo Especial" or "Celebra 5 Mayo"
✓ Include historical elements: "Victoria de Puebla", "Batalla Histórica", "Orgullo Nacional"
✓ Walmart México integration: "Celebración Mexicana", "Orgullo Nacional"
✓ Mexican values: "Patriotismo Mexicano", "Historia Nacional", "Valor Mexicano"

WALMART MÉXICO CINCO DE MAYO POWER LANGUAGE:
- "Cinco de Mayo Orgullo México" - "Victoria Histórica Puebla" - "Patriotismo Nacional"
- "Celebración Mexicana Auténtica" - "Mayo Histórico" - "Orgullo y Tradición"
- "México Victorioso" - "Batalla de Puebla" - "Honor Mexicano"

MEXICAN PATRIOTIC CULTURE:
- Reference Battle of Puebla, Mexican victory, national pride
- Include patriotic colors (green, white, red)
- Mention Mexican historical significance
""",
            
            "dia_de_la_independencia": """
🇲🇽 WALMART MÉXICO INDEPENDENCIA CELEBRATION OPTIMIZATION 🇲🇽

CRITICAL WALMART MEXICO INDEPENDENCIA REQUIREMENTS:
✓ Title MUST include "Independencia" or "16 Septiembre"
✓ Features emphasize NATIONAL PRIDE: "Independencia Nacional", "Grito de Dolores"
✓ Description opens with "Independencia México" or "16 Septiembre Especial"
✓ Include patriotic elements: "Viva México", "Grito de Independencia", "Libertad Nacional"
✓ Walmart México integration: "Celebra la Patria", "Independencia Nacional"
✓ Mexican values: "Libertad Mexicana", "Patria Querida", "Independencia Nacional"

WALMART MÉXICO INDEPENDENCIA POWER LANGUAGE:
- "Independencia México Septiembre" - "Grito de Dolores Histórico" - "Viva México Libre"
- "16 Septiembre Patrio" - "Libertad Nacional" - "Independencia Gloriosa"
- "México Independiente" - "Patria y Libertad" - "Grito Libertador"

MEXICAN INDEPENDENCE CULTURE:
- Reference Grito de Dolores, Miguel Hidalgo, September 16th
- Include patriotic celebration and Mexican flags
- Mention national independence and freedom themes
""",
            
            "christmas": """
🇲🇽 WALMART MÉXICO NAVIDAD OPTIMIZATION 🇲🇽

CRITICAL WALMART MEXICO NAVIDAD REQUIREMENTS:
✓ Title MUST include "Navidad" or "Navideño"
✓ Features emphasize MEXICAN CHRISTMAS: "Navidad Mexicana", "Tradición Familiar"
✓ Description opens with "Navidad Especial México" or "Celebra Navidad"
✓ Include Christmas elements: "Feliz Navidad", "Familia Unida", "Regalos Especiales"
✓ Walmart México integration: "Navidad Perfecta", "Celebración Familiar"
✓ Mexican values: "Familia Mexicana", "Navidad Tradicional", "Amor Familiar"

WALMART MÉXICO NAVIDAD POWER LANGUAGE:
- "Navidad Mexicana Especial" - "Familia Unida Navidad" - "Feliz Navidad México"
- "Regalos Perfectos Navidad" - "Tradición Navideña" - "Celebración Familiar"
- "Navidad Mexicana Auténtica" - "Amor y Familia" - "Navidad Perfecta"

MEXICAN CHRISTMAS CULTURE:
- Reference Mexican Christmas traditions, family unity
- Include Nochebuena, piñatas, Mexican Christmas foods
- Mention family celebration and gift-giving traditions
"""
        }
        
        return walmart_mexico_occasions.get(occasion.lower(), None)

import random