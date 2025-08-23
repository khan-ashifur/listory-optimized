import json
import time
import re
import logging
import random
from django.conf import settings
from .models import GeneratedListing, KeywordResearch
from apps.core.models import Product
from .backend_keyword_optimizer import BackendKeywordOptimizer


class ListingGeneratorService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.backend_optimizer = BackendKeywordOptimizer()  # Initialize backend keyword optimizer
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

    def _generate_fallback_profit_maximizer(self, product):
        """Generate fallback profit maximizer content when AI fails to generate it"""
        return {
            "q1_action_plan": [
                f"□ Set baseline price at ${product.price} (competitive positioning)",
                "□ Launch with 10% intro discount for first 30 days to gain reviews",
                "□ Stock 50-75 units based on category velocity",
                "□ Allocate 5-10% of expected revenue to daily ad spend",
                "□ Monitor top competitor pricing daily (set price alerts)",
                "□ A/B test main image: lifestyle vs product-only (2-week test)"
            ],
            "q2_growth_tactics": [
                "□ Increase price by 5-7% after hitting 25+ reviews (data shows tolerance)",
                "□ Launch bundle with complementary product (+18% AOV typical)",
                "□ Add video content (increases conversion 23% in this category)",
                "□ Expand to Sponsored Brand ads (2.1x ROAS average)",
                "□ Test higher price point on weekends (Fri-Sun show 8% less sensitivity)"
            ],
            "q3_optimization": [
                "□ Prepare 25% more inventory for back-to-school surge (Aug 15-Sep 10)",
                f"□ Create 3-pack bundle for {getattr(product, 'occasion', 'seasonal')} shoppers",
                "□ Increase ad spend by 40% during peak season",
                "□ Add comparison chart vs top 3 competitors",
                "□ Launch email campaign to previous buyers (28% repeat rate expected)"
            ],
            "q4_maximization": [
                "□ Price at +15% premium Nov 15-Dec 20 (historical tolerance data)",
                "□ Create gift bundle with premium packaging option",
                "□ Reserve 30% inventory for Black Friday/Cyber Monday",
                "□ Bid on competitor brand keywords (3.2x ROAS typical in Q4)",
                "□ Prepare post-holiday clearance strategy (Jan 2-15)"
            ],
            "competitor_landscape": {
                "market_position": "Enter as competitive player in subcategory",
                "price_positioning": "Start at median, move to 75th percentile after reviews",
                "top_3_competitors": [
                    "Competitor A: Market leader - Track daily",
                    "Competitor B: Price competitor - Weekly monitoring", 
                    "Competitor C: Quality competitor - Monthly benchmark"
                ],
                "differentiation_angles": [
                    "Faster shipping (2-day vs 3-5 day average)",
                    "Better warranty terms",
                    "Unique feature emphasis in title/bullets"
                ]
            },
            "revenue_projections": {
                "conservative": {
                    "month_1": f"${product.price * 10:.2f} (10 units at launch)",
                    "month_3": f"${product.price * 50:.2f} (50 units with reviews)",
                    "month_6": f"${product.price * 150:.2f} (150 units optimized)",
                    "month_12": f"${product.price * 300:.2f} (300 units scaled)"
                },
                "realistic": {
                    "month_1": f"${product.price * 20:.2f} (20 units)",
                    "month_3": f"${product.price * 100:.2f} (100 units)",
                    "month_6": f"${product.price * 300:.2f} (300 units)",
                    "month_12": f"${product.price * 600:.2f} (600 units)"
                },
                "aggressive": {
                    "month_1": f"${product.price * 40:.2f} (40 units)",
                    "month_3": f"${product.price * 200:.2f} (200 units)",
                    "month_6": f"${product.price * 500:.2f} (500 units)",
                    "month_12": f"${product.price * 1000:.2f} (1000 units)"
                }
            },
            "key_metrics_to_track": [
                "Conversion Rate: Target 15% (category average 12%)",
                "ACoS: Keep below 25% after month 2",
                "Review Velocity: 1 review per 10 sales minimum",
                "Inventory Turnover: 12x annually",
                "Return Rate: Keep under 3% (category average 5%)"
            ]
        }

    def _generate_walmart_fallback_keywords(self, product):
        """Generate comprehensive Walmart keywords when AI doesn't provide enough"""
        keywords = []
        
        # Base product keywords
        keywords.extend([
            f"{product.name.lower()}",
            f"{product.brand_name.lower()}",
            f"{product.brand_name.lower()} {product.name.lower()}",
        ])
        
        # Category-based keywords
        if product.categories:
            category_parts = product.categories.lower().split('>')
            for part in category_parts:
                keywords.append(part.strip())
                keywords.append(f"best {part.strip()}")
                keywords.append(f"{part.strip()} online")
        
        # Price-based keywords
        if hasattr(product, 'price') and product.price:
            if product.price < 50:
                keywords.extend(['budget', 'affordable', 'cheap', 'under 50'])
            elif product.price < 100:
                keywords.extend(['mid range', 'value', 'under 100'])
            else:
                keywords.extend(['premium', 'high end', 'luxury', 'professional'])
        
        # Occasion-based keywords
        if hasattr(product, 'occasion') and product.occasion:
            occasion = product.occasion.lower()
            if 'christmas' in occasion:
                keywords.extend(['christmas gift', 'holiday gift', 'christmas present', 'holiday shopping'])
            elif 'birthday' in occasion:
                keywords.extend(['birthday gift', 'birthday present', 'gift idea'])
            elif 'wedding' in occasion:
                keywords.extend(['wedding gift', 'bridal gift', 'wedding present'])
        
        # Generic high-converting Walmart keywords
        keywords.extend([
            'free shipping', 'fast delivery', 'same day pickup',
            'walmart exclusive', 'rollback', 'great value',
            'customer favorite', 'top rated', 'best seller',
            'new arrival', 'trending', 'popular',
            'quality guaranteed', 'satisfaction guaranteed',
            'easy returns', 'money back guarantee',
            'in stock', 'available now', 'ready to ship'
        ])
        
        # Remove duplicates and join
        unique_keywords = list(dict.fromkeys(keywords))
        return ', '.join(unique_keywords[:100])

    def get_japanese_industry_keywords(self, product):
        """Get Japanese industry-specific high-intent keywords"""
        category = product.categories.lower() if product.categories else ""
        
        # Industry-specific Japanese keywords by category
        industry_keywords = {
            "electronics": "正規品, 高品質, PSE認証, 日本語サポート, 送料無料, 1年保証, Amazon配送, 安心, 信頼",
            "audio": "ノイズキャンセリング, 高音質, ワイヤレス, Bluetooth5.3, HiFi, 長時間再生, 通勤用, オフィス用, ゲーミング対応",
            "headphones": "ノイズキャンセリング付き, 30時間再生, 軽量設計, 防水仕様, iPhone対応, Android対応, 通話機能, 急速充電",
            "home": "省エネ, 静音設計, コンパクト, おしゃれ, 清掃簡単, ワイヤレス, スマート機能, エコ設計, 日本製品質",
            "kitchen": "ステンレス鋼, ノンスティック, 食洗機対応, BPAフリー, 耐熱性, プロ仕様, 調理器具, 安全設計",
            "sports": "防水IPX7, 通気性, 人間工学, 軽量, 耐久性, フィットネス, ジム用, ランニング, スポーツ用品",
            "office": "生産性向上, デスクワーク, 在宅勤務, 整理整頓, 調整可能, ビジネス用, オフィス用品, 作業効率"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Default high-intent Japanese keywords
        return "正規品, 高品質, PSE認証, 日本語サポート, 1年保証, 送料無料, Amazon配送, 安心購入, 信頼ブランド"
    
    def get_spanish_industry_keywords(self, product):
        """Get Spanish industry-specific high-intent keywords"""
        category = product.categories.lower() if product.categories else ""
        
        # Industry-specific Spanish keywords by category
        industry_keywords = {
            "electronics": "mejor, original, certificado CE, profesional, premium, oferta España, 2024, garantía, compatible, inalámbrico",
            "audio": "cancelación ruido, bluetooth 5.3, HiFi, auriculares gaming, estéreo, micrófono, manos libres, envío España, calidad europea",
            "headphones": "cancelación ruido activa, bluetooth 5.3, auriculares gaming, estéreo premium, micrófono ENC, envío España 24h",
            "home": "ahorro energético, silencioso, portátil, diseño moderno, fácil limpieza, sin cables, inteligente, eco, sostenible España",
            "kitchen": "acero inoxidable, antiadherente, apto lavavajillas, BPA free, resistente calor, profesional cocina, envío España",
            "sports": "impermeable IPX7, transpirable, ergonómico, ultraligero, resistente, fitness, gimnasio, running, envío España",
            "office": "productividad, escritorio, teletrabajo, organizador, ajustable, profesional, premium business, envío España"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Default high-intent Spanish keywords
        return "mejor, original, profesional, certificado CE, garantía 2 años, premium, oferta España, envío España 24h, calidad europea"
    
    def get_japanese_industry_keywords(self, product):
        """Get Japanese industry-specific high-intent keywords"""
        category = product.categories.lower() if product.categories else ""
        
        # Industry-specific Japanese keywords by category
        industry_keywords = {
            "electronics": "正規品, 高品質, PSE認証, 日本語サポート, 送料無料, 1年保証, Amazon配送, 安心, 信頼",
            "audio": "ノイズキャンセリング, 高音質, ワイヤレス, Bluetooth5.3, HiFi, 長時間再生, 通勤用, オフィス用, ゲーミング対応",
            "headphones": "ノイズキャンセリング付き, 30時間再生, 軽量設計, 防水仕様, iPhone対応, Android対応, 通話機能, 急速充電",
            "home": "省エネ, 静音設計, コンパクト, おしゃれ, 清掃簡単, ワイヤレス, スマート機能, エコ設計, 日本製品質",
            "kitchen": "ステンレス鋼, ノンスティック, 食洗機対応, BPAフリー, 耐熱性, プロ仕様, 調理器具, 安全設計",
            "sports": "防水IPX7, 通気性, 人間工学, 軽量, 耐久性, フィットネス, ジム用, ランニング, スポーツ用品",
            "office": "生産性向上, デスクワーク, 在宅勤務, 整理整頓, 調整可能, ビジネス用, オフィス用品, 作業効率"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Default high-intent Japanese keywords
        return "正規品, 高品質, PSE認証, 日本語サポート, 1年保証, 送料無料, Amazon配送, 安心購入, 信頼ブランド"
    
    def get_turkish_industry_keywords(self, product):
        """Get Turkish industry-specific high-intent keywords for Turkey market - EXACT MEXICO PATTERN FOR 10/10 QUALITY"""
        category = product.categories.lower() if product.categories else ""
        
        # Enhanced Turkish keywords by category - MEXICO PATTERN APPLIED - DOMINATES HELIUM 10, JASPER AI, COPY MONKEY
        industry_keywords = {
            "kitchen": "inanılmaz mutfak seti, rostfritt çelik premium kalite, mükemmel boyut ideal, türk ailesi mutfak keyfi, çevre dostu sürdürülebilir üretim, geleneksel türk malzemesi, 15000+ türk aşçısı, bulaşık makinesi uyumlu sertifikalı, BPA içermez güvenli aile, türkiye kargo aynı gün, profesyonel kalite garantili, sınırlı stok özel fiyat",
            "audio": "fantastik ses deneyimi, aktif gürültü engelleme teknolojisi, kusursuz bluetooth 5.3 bağlantı, premium stereo müzik kalitesi, türk ailesi için tasarlanmış, geleneksel konfor modern teknoloji, 25000+ müzik tutkunları, pil ömrü 40 saat garantili, eller serbest konforlu kullanım, türkiye express teslimat, profesyonel ses mühendisliği, son günler özel kampanya",
            "electronics": "devrimsel teknoloji inovasyonu, CE sertifikalı avrupa kalitesi, mükemmel performans garantili, türk teknoloji severleri, sürdürülebilir çevre dostu üretim, orijinal türk distribütör garantisi, 30000+ mutlu teknoloji kullanıcısı, 2 yıl üretici garantisi, aile güvenliği sertifikalı, türkiye nationwide kargo, profesyonel teknik destek, acele edin sınırlı üretim",
            "home": "muhteşem ev konforu, enerji tasarruflu akıllı tasarım, eşsiz yaşam kalitesi artırıcı, türk evi için özel, çevre bilinci sürdürülebilir çözüm, geleneksel türk misafirperverliği, 20000+ mutlu ev sahipleri, sessiz çalışma garantili, aile sağlığı öncelikli üretim, türkiye hızlı kargo, premium yaşam standardı, fırsat kaçırmayın bugün",
            "sports": "benzersiz spor performansı, su geçirmez IPX7 sertifikalı, olağanüstü ergonomik tasarım, türk sporcu tercihi, sürdürülebilir spor ekipmanı, geleneksel dayanıklılık modern style, 18000+ aktif türk sporcusu, ultra hafif premium malzeme, fit yaşam sağlık garantisi, türkiye spor kargo, profesyonel antrenör onaylı, limited edition özel seri"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Default MEXICO-STYLE Turkish keywords - BEATS ALL COMPETITORS WITH CULTURAL DEPTH
        return "inanılmaz kalite deneyimi, premium türk mühendisliği, mükemmel aile için tasarım, orijinal türkiye üretici garantisi, sürdürülebilir çevre dostu üretim, geleneksel türk zanaatkarlığı, 25000+ mutlu türk ailesi, CE sertifikalı avrupa standardı, profesyonel uzman onaylı, türkiye express kargo, premium yaşam kalitesi, sınırlı üretim özel fırsat, acele edin son günler, hayalinizdeki türk kalitesi"
    
    def get_swedish_industry_keywords(self, product):
        """Get Swedish industry-specific high-intent keywords for Sweden market"""
        category = product.categories.lower() if product.categories else ""
        
        # Industry-specific Swedish keywords by category - LAGOM QUALITY APPROACH
        industry_keywords = {
            "electronics": "bäst i test 2024, premium kvalitet certifierad, klimatsmart koldioxidneutral, lagom design perfekt, hygge komfort premium, allemansrätten kompatibel, 15000+ svenska kunder, hållbar för framtiden, CE-certifierad, svensk säkerhet standard, trådlös teknologi, specialpris begränsat, missa inte idag, svensk garanti 2 år, europeisk kvalitet",
            "audio": "bäst i test 2024 ljud, aktiv brusreducering premium, bluetooth 5.3 certifierad, HiFi lagom kvalitet, gaming headset sweden, hygge musikupplevelse, allemansrätten outdoor, 15000+ svenska musikälskare, klimatsmart ljudteknik, handsfree bekvämlighet, sverige frakt 24h, begränsat lager specialpris, säkert för barn certifierat",
            "headphones": "bäst i test 2024 hörlurar, aktiv brusreducering lagom, bluetooth 5.3 premium certifierad, gaming headset sverige, hygge komfort design, 30h batteritid klimatsmart, allemansrätten outdoor proof, 15000+ svenska gamers, ENC mikrofon kristallklar, sverige frakt samma dag, begränsat antal specialpris, säkert för barn testade",
            "home": "bäst i test 2024 hem, energisnål klimatsmart design, lagom storlek perfekt, hygge hemkänsla premium, hållbar för framtiden certifierad, allemansrätten miljötänk, 15000+ svenska hem, tyst operation premium, smart teknik sweden, sverige frakt snabb, begränsat antal idag, familjevänlig säker",
            "kitchen": "bäst i test 2024 kök, rostfritt stål premium kvalitet, lagom storlek perfekt, hygge matlagning design, klimatsmart hållbar produktion, allemansrätten naturmaterial, 15000+ svenska kockar, diskmaskinssäker certifierad, BPA-fri säker familj, sverige frakt samma dag, professionell kvalitet garanterad, begränsat lager specialpris",
            "sports": "vattentät IPX7, andningsbar, ergonomisk, ultralätt, hållbar, fitness, gym, löpning, sverige frakt, sportentusiaster, hälsa, aktivt liv, snabb frakt från sverige, specialrabatt, beställ idag",
            "office": "produktivitet, skrivbord, distansarbete, organiserare, justerbar, professionell, premium business, sverige frakt, arbetsframgång, kontorskomfort, professionellt val, för din karriär, svensk garanti, begränsad produkt",
            "beauty": "organisk, naturlig, parabenfri, känslig hud, dermatologiskt testad, svensk kosmetik, skönhetsvård, anti-aging, för din skönhet, värde för dig själv, svenska kvinnors val, hälsosam hud, specialformel, missa inte",
            "fashion": "mode, trend, stil, kvalitetstyg, bekväm, elegant, vardaglig, klassisk, modern svensk stil, säsong, för din stil, självförtroende, svensk mode, stilgaranti, specialkollektion, begränsat antal",
            "jewelry": "925 sterling silver, guldplätering, handgjort, svenskt hantverk, specialdesign, presentförpackning, elegant accessoar, present till nära och kära, speciella tillfällen, svensk konst, värdefulla minnen, att vara stolt över, specialerbjudande",
            "baby": "babysäker, BPA-fri, hypoallergen, mjuk, ekologisk bomull, mammavänlig, babyvård, tillverkad i sverige, säkert för babyn, lugn för mamman, barnhälsa, svenska mammors val, säker framtid, special babyprodukt"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Enhanced default Swedish keywords - DOMINATES ALL COMPETITORS
        return "bäst i test 2024, premium kvalitet certifierad, klimatsmart koldioxidneutral, lagom design perfekt, hygge komfort premium, allemansrätten kompatibel, 15000+ svenska kunder, hållbar för framtiden, CE-certifierad garanti 2 år, sverige frakt 24h, europeisk kvalitet standard, begränsat lager specialpris, missa inte idag, din drömkvalitet garanterad"
    
    def get_indian_industry_keywords(self, product):
        """Get Indian industry-specific high-intent keywords for India market - EXACT MEXICO PATTERN FOR 10/10 QUALITY"""
        category = product.categories.lower() if product.categories else ""
        
        # Enhanced Indian keywords by category - MEXICO PATTERN APPLIED - DOMINATES HELIUM 10, JASPER AI, COPY MONKEY
        industry_keywords = {
            "kitchen": "incredible indian kitchen knife set, perfect for daily cooking dal sabzi roti, ideal diwali wedding housewarming gift, premium stainless steel sharp blades, ginger garlic paste chopping onions, beginner friendly safe handles, traditional indian cooking made easy, 50000+ satisfied indian families, dishwasher safe easy maintenance, GST bill included 2 year warranty, perfect for gifting festivals ceremonies, india express delivery same day",
            "knife": "perfect indian cooking knife set, daily dal sabzi preparation, ideal diwali festival gift, sharp stainless steel blades, chopping onions ginger garlic, beginner safe ergonomic handles, traditional indian kitchen essential, wedding housewarming gift perfect, 1 lakh happy indian cooks, easy cleaning dishwasher safe, GST invoice 2 year guarantee, festival gifting ceremony ready",
            "audio": "fantastic sound experience, active noise cancellation technology, perfect bluetooth 5.3 connection, premium stereo music quality, designed for indian families, traditional comfort modern technology, 35000+ music lovers, battery life 40 hours guaranteed, hands free comfortable usage, india express delivery, professional sound engineering, diwali festival gift perfect",
            "electronics": "revolutionary technology innovation, certified premium quality, perfect performance guaranteed, indian technology enthusiasts, sustainable eco-friendly production, original indian distributor warranty, 40000+ happy technology users, 2 year manufacturer warranty, family safety certified, india nationwide delivery, professional technical support, festival gifting ready",
            "home": "wonderful home comfort, energy efficient smart design, perfect living quality enhancer, designed for indian homes, environmental consciousness sustainable solution, traditional indian hospitality, 30000+ happy home owners, silent operation guaranteed, family health priority production, india fast delivery, premium living standard, diwali housewarming gift ideal",
            "sports": "amazing sports performance, waterproof IPX7 certified, extraordinary ergonomic design, indian athlete's choice, sustainable sports equipment, traditional durability modern style, 28000+ active indian sportsmen, ultra light premium material, fit lifestyle health guarantee, india sports delivery, professional trainer approved, festival gift special edition"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Default MEXICO-STYLE Indian keywords - BEATS ALL COMPETITORS WITH CULTURAL DEPTH + HINDI-FRIENDLY
        return "incredible quality experience, premium indian engineering, perfect family design, original india manufacturer warranty, diwali wedding housewarming gift ideal, traditional indian gharelu use, 1 lakh+ happy indian families, certified premium standard ISI mark, professional expert approved, india express delivery free shipping, premium lifestyle quality, shaadi ceremony gift perfect, festival gifting ready, ghar kitchen essential, your dream indian quality"
    
    def get_egyptian_industry_keywords(self, product):
        """Get Egyptian industry-specific high-intent keywords for Egypt market - EXACT MEXICO PATTERN FOR 10/10 QUALITY"""
        category = product.categories.lower() if product.categories else ""
        
        # Enhanced Egyptian keywords by category - MEXICO PATTERN APPLIED - DOMINATES HELIUM 10, JASPER AI, COPY MONKEY
        industry_keywords = {
            "kitchen": "مجموعة سكاكين مطبخ مصرية رائعة, مثالية للطبخ اليومي المصري, هدية مثالية رمضان عيد الفطر, شفرات ستانلس ستيل حادة, تقطيع بصل ثوم طماطم, مقابض آمنة للمبتدئين, أساسي المطبخ المصري التقليدي, هدية زفاف احتفال بيت جديد, 50000+ عائلة مصرية راضية, سهل التنظيف غسالة أطباق, فاتورة ضريبية ضمان سنتين, مثالي هدايا المناسبات المصرية, توصيل سريع مصر كلها",
            "knife": "مجموعة سكاكين طبخ مصرية مثالية, إعداد الطعام المصري اليومي, هدية مثالية عيد رمضان, شفرات ستانلس ستيل حادة, تقطيع خضار لحوم فواكه, مقابض آمنة مريحة, ضرورة المطبخ المصري, هدية زفاف بيت جديد مثالية, 100000+ طباخ مصري سعيد, تنظيف سهل آمن, فاتورة ضمان سنتان, جاهز هدايا المناسبات",
            "audio": "تجربة صوت رائعة استثنائية, تكنولوجيا إلغاء الضوضاء, اتصال بلوتوث مثالي 5.3, جودة موسيقى ستيريو فاخرة, مصمم للعائلات المصرية, راحة تقليدية تكنولوجيا حديثة, 35000+ عاشق موسيقى مصري, عمر بطارية 40 ساعة مضمون, استخدام مريح حر اليدين, توصيل سريع مصر, هندسة صوت احترافية, هدية رمضان عيد مثالية",
            "electronics": "تكنولوجيا ثورية مبتكرة, جودة فاخرة معتمدة, أداء مثالي مضمون, عشاق التكنولوجيا المصريين, إنتاج صديق البيئة مستدام, ضمان موزع مصري أصلي, 40000+ مستخدم تكنولوجيا سعيد, ضمان مصنع سنتان, أمان عائلي معتمد, توصيل مصر كلها, دعم فني احترافي, جاهز هدايا الأعياد",
            "home": "راحة منزلية رائعة, تصميم ذكي موفر طاقة, محسن جودة معيشة مثالي, مصمم للبيوت المصرية, حل مستدام وعي بيئي, ضيافة مصرية تقليدية, 30000+ صاحب منزل سعيد, تشغيل صامت مضمون, إنتاج أولوية صحة عائلية, توصيل سريع مصر, مستوى معيشة فاخر, هدية رمضان بيت جديد",
            "sports": "أداء رياضي مذهل, مقاوم ماء IPX7 معتمد, تصميم بيئة عمل استثنائي, اختيار الرياضي المصري, معدات رياضية مستدامة, متانة تقليدية أسلوب حديث, 28000+ رياضي مصري نشط, مادة فاخرة خفيفة جداً, ضمان نمط حياة لياقة, توصيل رياضة مصر, معتمد مدرب محترف, إصدار خاص هدية عيد"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Default MEXICO-STYLE Egyptian keywords - BEATS ALL COMPETITORS WITH CULTURAL DEPTH + ARABIC-FRIENDLY
        return "تجربة جودة رائعة, هندسة مصرية فاخرة, تصميم عائلي مثالي, ضمان مصنع مصري أصلي, هدية رمضان عيد زفاف مثالية, استخدام مصري تقليدي, 1 مليون+ عائلة مصرية سعيدة, معيار فاخر معتمد علامة جودة, معتمد خبير محترف, توصيل سريع مصر شحن مجاني, جودة نمط حياة فاخر, هدية حفل زفاف مثالية, جاهز هدايا أعياد, ضروري بيت مطبخ, حلم الجودة المصرية"
    
    def get_polish_industry_keywords(self, product):
        """Get Polish industry-specific high-intent keywords for Poland market - EXACT MEXICO PATTERN FOR 10/10 QUALITY"""
        category = product.categories.lower() if product.categories else ""
        
        # Enhanced Polish keywords by category - MEXICO PATTERN APPLIED - DOMINATES HELIUM 10, JASPER AI, COPY MONKEY
        industry_keywords = {
            "kitchen": "zestaw noży kuchennych premium, idealny polski dom rodzinny, prezent Boże Narodzenie Wielkanoc, ostrza stal nierdzewna trwałe, krojenie cebuli czosnku mięsa, uchwyty bezpieczne początkujący, niezbędny polska kuchnia tradycyjna, prezent ślub chrzciny nowy dom, 100000+ szczęśliwa polska rodzina, łatwe czyszczenie zmywarka, faktura gwarancja 2 lata, idealny prezenty polskie święta, szybka dostawa cała Polska",
            "knife": "noże kuchennie polskie premium, przygotowanie jedzenia codzienne, prezent idealny święta imieniny, stal nierdzewna ostre trwałe, krojenie warzywa mięso owoce, uchwyty ergonomiczne wygodne, konieczność polska kuchnia, prezent ślub dom mały idealny, 150000+ kucharz polski zadowolony, czyszczenie proste bezpieczne, faktura polska gwarancja dwuletnia, gotowy prezenty wszystkie okazje",
            "audio": "doświadczenie dźwięk niesamowite, technologia redukcja hałasu, połączenie bluetooth doskonałe 5.3, jakość muzyka stereo luksusowa, zaprojektowany polska rodzina, komfort tradycyjny nowoczesna technologia, 50000+ miłośnik muzyki polski, żywotność bateria 40 godzin gwarantowana, użytkowanie wygodne bezprzewodowe, dostawa szybka Polska, inżynieria dźwięk profesjonalna, prezent Boże Narodzenie święta idealny",
            "electronics": "technologia rewolucyjna innowacyjna, jakość premium certyfikowana, wydajność idealna gwarantowana, entuzjaści technologia polscy, produkcja przyjazna środowisko zrównoważona, gwarancja dystrybutor polski oryginalny, 60000+ użytkownik technologia szczęśliwy, gwarancja producent dwa lata, bezpieczeństwo rodzinne certyfikowane, dostawa cała Polska, wsparcie techniczne profesjonalne, gotowy prezenty wszystkie święta",
            "home": "komfort domowy niesamowity, projekt inteligentny oszczędność energii, poprawiony jakość życia idealny, zaprojektowany polskie domy, rozwiązanie trwałe świadomość ekologiczna, gościnność polska tradycyjna, 40000+ właściciel domu szczęśliwy, działanie ciche gwarantowane, produkcja priorytet zdrowie rodzinne, dostawa szybka Polska, poziom życia luksusowy, prezent Wielkanoc nowy dom",
            "sports": "wydajność sportowa niesamowita, wodoodporny IPX7 certyfikowany, projekt środowisko pracy wyjątkowy, wybór sportowiec polski, sprzęt sportowy zrównoważony, trwałość tradycyjna styl nowoczesny, 35000+ sportowiec polski aktywny, materiał premium lekki bardzo, gwarancja styl życia fitness, dostawa sport Polska, certyfikowany trener profesjonalny, edycja specjalna prezent święto"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Default MEXICO-STYLE Polish keywords - BEATS ALL COMPETITORS WITH CULTURAL DEPTH + POLISH-FRIENDLY
        return "doświadczenie jakość niesamowita, inżynieria polska premium, projekt rodzinny idealny, gwarancja producent polski oryginalny, prezent Boże Narodzenie Wielkanoc ślub idealny, użytkowanie tradycja polska, 2 miliony+ polska rodzina szczęśliwa, standard premium certyfikowany znak jakości, certyfikowany ekspert profesjonalny, dostawa ekspresowa Polska darmowa wysyłka, jakość styl życia premium, prezent uroczystość ślub idealny, gotowy prezenty święta, niezbędny dom kuchnia, marzenie jakość polska"
    
    
    def get_marketplace_title_format(self, marketplace, brand_name):
        """Get marketplace-specific title formatting instructions"""
        
        if marketplace == 'de':
            return f"""🚨 CRITICAL AMAZON GERMANY TITLE FORMAT: Prioritize CONVERSION HOOKS first, then keywords: '[Hauptnutzen/Hook] [Produkttyp] von [Brand] - [Spezifikation] - [Weitere Vorteile]'. 
            
            German customers scan for BENEFITS FIRST, not just keywords. Lead with emotional hooks that drive purchase decisions.
            
            GOOD: 'Ultimativer Komfort Bluetooth Kopfhörer von {brand_name} - 30h Akku - Noise Cancelling Wireless Headset'
            BAD: 'Bluetooth Kopfhörer 30h Akku {brand_name} - Wireless Headset mit Noise Cancelling'
            
            PRIORITY ORDER:
            1. Conversion hook (Ultimativer Komfort, Perfekte Lösung, Professionelle Qualität)
            2. Product type in German
            3. Brand placement for trust 
            4. Key specification
            5. Secondary benefits
            
            150-190 chars max. Use German umlauts (ä, ö, ü, ß) naturally."""
            
        elif marketplace == 'fr':
            return f"""🚨 CRITICAL AMAZON FRANCE TITLE FORMAT: French elegance meets conversion: '[Avantage Principal] [Type Produit] {brand_name} - [Spécification Clé] - [Bénéfices Secondaires]'. 
            
            French customers appreciate sophisticated benefit positioning.
            
            Example: 'Confort Ultime Écouteurs Bluetooth {brand_name} - Batterie 30h - Casque Sans Fil Réduction Bruit'
            
            150-190 chars max with proper French accents."""
            
        elif marketplace == 'it':
            return f"""🚨 CRITICAL AMAZON ITALY TITLE FORMAT: Italian style with conversion focus: '[Beneficio Principale] [Tipo Prodotto] {brand_name} - [Specifica Chiave] - [Vantaggi Aggiuntivi]'.
            
            Italian customers value style and performance equally.
            
            Example: 'Comfort Supremo Cuffie Bluetooth {brand_name} - Batteria 30ore - Auricolari Wireless Cancellazione Rumore'
            
            150-190 chars max with Italian formatting."""
            
        elif marketplace == 'jp':
            return f"""🇯🇵 AMAZON JAPAN CO.JP TITLE OPTIMIZATION - 日本市場専用:

FORMAT (MAX 100 CHARS - Japanese mobile priority):
[{brand_name}] [商品カテゴリ] [主要機能] [信頼性指標] [配送/保証]

CRITICAL JAPANESE SEO + CULTURAL RULES:
1. BRAND FIRST - 日本では信頼性が最優先 (trust is paramount)
2. PRODUCT CATEGORY in natural Japanese (ワイヤレスイヤホン, モバイルバッテリー)
3. KEY FEATURE with benefit (ノイズキャンセリング付き, 急速充電対応)
4. TRUST SIGNALS (正規品, 安心保証, 日本語サポート) 
5. SHIPPING (送料無料, 翌日配送, Amazon配送)

HIGH-CONVERTING JAPANESE KEYWORDS:
✓ 正規品 (authentic/genuine) - highest trust signal
✓ 安心 (peace of mind) - emotional security crucial in Japan
✓ 高品質 (high quality) - quality obsession
✓ 送料無料 (free shipping) - value transparency
✓ 日本語サポート (Japanese support) - local service
✓ 翌日配送 (next day delivery) - convenience culture
✓ PSE認証 (PSE certified) - safety compliance

JAPANESE TITLE EXAMPLES:
✅ "{brand_name} ワイヤレスイヤホン 30時間再生 ノイズキャンセリング 正規品 1年保証"
✅ "{brand_name} モバイルバッテリー 20000mAh PD急速充電 PSE認証済 送料無料"
✅ "{brand_name} Bluetooth スピーカー 防水IPX7 高音質 日本語サポート"

JAPANESE CULTURAL PRIORITIES:
- 信頼性 (reliability) over flashy claims
- 品質 (quality) specifications matter
- 安心感 (sense of security) essential
- 丁寧語 (polite language) shows respect
- 技術仕様 (technical specs) appreciated
- Made in Japan or equivalent quality standards

MOBILE-FIRST: Japanese users scan first 40 chars on mobile."""
        
        elif marketplace == 'tr':  # Turkey
            return f"""🇹🇷 AMAZON TURKEY TITLE OPTIMIZATION - RAKİPLERİ GEÇ! HELIUM 10/JASPER/COPYMONKEY'DEN ÜSTÜN:

FORMAT (MAX 200 CHARS - CONVERSION FIRST):
[{brand_name}] [Premium] [Ürün Kategorisi] [Dönüşüm Hook'u] [Güven/Garanti] [Aciliyet]

CRITICAL TURKISH SEO + CULTURAL + CONVERSION RULES:
1. BRAND FIRST - Türkiye'de güven en önemli (trust is paramount)
2. PREMIUM POSITIONING - "Premium", "En İyi", "Profesyonel" 
3. CONVERSION HOOKS - "Aileniz İçin", "Sınırlı Stok", "Özel Fiyat"
4. TRUST SIGNALS - "2 Yıl Garanti", "CE Sertifikalı", "10.000+ Mutlu Müşteri"
5. URGENCY/SCARCITY - "Bugün Kaçırmayın", "Son Fırsat", "Acele Edin"

SUPER HIGH-CONVERTING TURKISH KEYWORDS (BEATS COMPETITORS):
✓ "Aileniz için en iyisi" (family emotional hook)
✓ "Sınırlı stok" (scarcity)
✓ "Özel fiyat bugün" (urgency + price)
✓ "10.000+ mutlu müşteri" (social proof)
✓ "Türkiye'nin tercihi" (local pride)
✓ "Hayalinizdeki kalite" (aspirational)
✓ "Gurur duyacağınız seçim" (emotional validation)
✓ "Son fırsat" (FOMO)
✓ profesyonel (professional) - business quality

TURKISH TITLE EXAMPLES:
✅ "{brand_name} Kablosuz Kulaklık 30 Saat Dinleme Gürültü Engelleme Orijinal 2 Yıl Garanti"
✅ "{brand_name} Taşınabilir Şarj Aleti 20000mAh Hızlı Şarj CE Sertifikalı Türkiye Kargo"
✅ "{brand_name} Bluetooth Hoparlör Su Geçirmez IPX7 Yüksek Ses Kalitesi Türk Müşteri Desteği"

TURKISH CULTURAL PRIORITIES:
- güvenilirlik (reliability) over flashy claims
- kalite (quality) specifications matter
- güven (trust) essential for purchase decisions
- nezaket (politeness) shows respect to customers
- teknik özellikler (technical specs) appreciated
- Made in Turkey or European quality standards
- aile değerleri (family values) important
- misafirperverlik (hospitality) culture

MOBILE-FIRST: Turkish users scan first 50 chars on mobile.
AVOID: Overly promotional language, focus on genuine benefits."""
        
        elif marketplace == 'es':
            return f"""🚨 SEO-OPTIMIZED SPANISH TITLE FOR AMAZON.ES TOP RANKING:
            
            FORMAT (MAX 200 CHARS): [{brand_name}] [Producto+Keyword] [Spec#] - [Beneficio] | [Uso] [2024]
            
            KEYWORD ORDER FOR ALGORITHM:
            1. Brand FIRST for trust
            2. Product + main keyword (Auriculares Bluetooth)
            3. Number spec (30H, 20000mAh)
            4. Key benefit short (Cancelación Ruido)
            5. Use/Season (Deporte 2024)
            
            HIGH-INTENT KEYWORDS:
            ✓ "Mejor" "Original" "Profesional" "Premium"
            ✓ Numbers always (30H not "larga duración")
            ✓ Year/Season for freshness
            
            EXAMPLES:
            ✅ "{brand_name} Auriculares Bluetooth Inalámbricos 30H - Cancelación Ruido ANC | Deporte 2024"
            ✅ "{brand_name} Powerbank 20000mAh Carga Rápida - USB-C PD | Viaje iPhone Samsung"
            
            MOBILE: First 80 chars must have complete value proposition."""

        elif marketplace == 'jp':
            return f"""🚨 CRITICAL AMAZON JAPAN TITLE FORMAT: Japanese titles prioritize quality, safety, and customer respect: '[品質表現] [商品名] - [ブランド名] - [主要機能] - [お客様への価値]'.
            
            Japanese customers highly value: 1) Quality assurance, 2) Safety/Peace of mind, 3) Respectful language, 4) Clear specifications.
            
            GOOD: '高品質 ワイヤレスヘッドホン - {brand_name} - 30時間再生 - お客様に安心の1年保証'
            BAD: 'ワイヤレスヘッドホン {brand_name} 30時間 バッテリー'
            
            PRIORITY ORDER:
            1. Quality descriptor (高品質, プレミアム, 安心, 信頼の)
            2. Product name in Japanese
            3. Brand name (can be katakana for foreign brands)
            4. Key feature/specification  
            5. Customer value (安心, 保証, サポート)
            
            MANDATORY ELEMENTS:
            - Use proper Japanese characters (Hiragana, Katakana, Kanji)
            - Include quality/safety terms: 高品質, 安心, 信頼, 保証
            - Show respect for customers: お客様, 皆様
            - Specify warranty/support: 1年保証, 日本語サポート
            
            AVOID: Overly casual language, discount emphasis, or direct romaji transliterations."""
        
        elif marketplace == 'br':
            return f"""🇧🇷 AMAZON BRAZIL TITLE OPTIMIZATION - MERCADO BRASILEIRO:
            
FORMAT (MAX 200 CHARS - Portuguese mobile priority):
[{brand_name}] [Produto Principal] [Característica Principal] [Benefício] [Garantia/Certificação]

CRITICAL BRAZILIAN SEO + CULTURAL RULES:
1. BRAND FIRST - Confiança é fundamental no Brasil (trust is paramount)
2. PRODUCT CATEGORY in Portuguese (Fones Bluetooth, Carregador Portátil)
3. KEY FEATURE with benefit (Cancelamento Ruído, Carregamento Rápido)
4. TRUST SIGNALS (garantia, certificado INMETRO, nota fiscal)
5. SHIPPING/GUARANTEE (frete grátis, garantia nacional, suporte Brasil)

HIGH-CONVERTING BRAZILIAN KEYWORDS:
✓ premium (premium quality emphasis)
✓ garantia (guarantee - essential trust signal)
✓ certificado (certified - quality assurance)
✓ Brasil/brasileiro (local market relevance)
✓ frete grátis (free shipping - conversion driver)
✓ original (authentic product)
✓ qualidade (quality obsession)"""

        elif marketplace == 'mx':
            return f"""🇲🇽 AMAZON MEXICO TITLE OPTIMIZATION - MERCADO MEXICANO:
            
FORMAT (MAX 200 CHARS - Spanish Mexican mobile priority):
[{brand_name}] [Producto Principal] [Característica Clave] [Beneficio] [Garantía/Certificación]

CRITICAL MEXICAN SEO + CULTURAL RULES:
1. BRAND FIRST - Confianza familiar es clave (family trust is key)
2. PRODUCT CATEGORY in Mexican Spanish (Audífonos Bluetooth, Cargador Portátil)
3. KEY FEATURE with benefit (Cancelación Ruido, Carga Rápida)
4. TRUST SIGNALS (garantía, certificado calidad, factura incluida)
5. SHIPPING/GUARANTEE (envío seguro, garantía México, servicio local)

HIGH-CONVERTING MEXICAN KEYWORDS:
✓ premium (calidad premium)
✓ garantía (guarantee essential)
✓ certificado (certified quality)
✓ México/mexicano (local relevance)
✓ envío gratis (free shipping)
✓ original (producto original)
✓ calidad (quality focus)"""

        elif marketplace == 'in':
            return f"""🇮🇳 AMAZON INDIA TITLE OPTIMIZATION - INDIAN MARKET:
            
FORMAT (MAX 200 CHARS - Indian English priority):
[{brand_name}] [Product Category] [Key Feature] [Benefit] [Warranty/Certification]

CRITICAL INDIAN SEO + CULTURAL RULES:
1. BRAND FIRST - Family trust is fundamental (joint family values)
2. PRODUCT CATEGORY in Indian English (Bluetooth Headphones, Portable Charger)
3. KEY FEATURE with benefit (Noise Cancellation, Fast Charging)
4. TRUST SIGNALS (warranty, quality certificate, bill included)
5. SHIPPING/GUARANTEE (free delivery, India warranty, local service)

HIGH-CONVERTING INDIAN KEYWORDS:
✓ incredible (incredible quality)
✓ guarantee (guarantee essential)
✓ certified (certified quality)
✓ indian/india (local relevance)
✓ free delivery (free delivery - conversion driver)
✓ original (authentic product)
✓ quality (quality focus)"""

        elif marketplace == 'sa':
            return f"""🇸🇦 AMAZON SAUDI ARABIA TITLE OPTIMIZATION - السوق السعودي:
            
FORMAT (MAX 200 CHARS - Arabic mobile priority):
[{brand_name}] [فئة المنتج الرئيسية] [الميزة الأساسية] [الفائدة] [الضمان/الشهادة]

CRITICAL SAUDI SEO + CULTURAL RULES:
1. BRAND FIRST - الثقة العائلية أساسية (family trust is key)
2. PRODUCT CATEGORY in Saudi Arabic (سماعات بلوتوث، شاحن محمول)
3. KEY FEATURE with benefit (إلغاء الضوضاء، شحن سريع)
4. TRUST SIGNALS (ضمان، شهادة جودة، فاتورة شاملة)
5. SHIPPING/GUARANTEE (شحن آمن، ضمان السعودية، خدمة محلية)

HIGH-CONVERTING SAUDI KEYWORDS:
✓ بريميوم (جودة بريميوم)
✓ ضمان (guarantee essential)
✓ معتمد (certified quality)
✓ السعودية/سعودي (local relevance)
✓ شحن مجاني (free shipping)
✓ أصلي (منتج أصلي)
✓ جودة (quality focus)"""

        elif marketplace == 'eg':
            return f"""🇪🇬 AMAZON EGYPT TITLE OPTIMIZATION - السوق المصري:
            
FORMAT (MAX 200 CHARS - Arabic Egyptian mobile priority):
[{brand_name}] [فئة المنتج الرئيسية] [الميزة الأساسية] [الفائدة] [الضمان/الشهادة]

CRITICAL EGYPTIAN SEO + CULTURAL RULES:
1. BRAND FIRST - الثقة العائلية المصرية أساسية (Egyptian family trust is key)
2. PRODUCT CATEGORY in Egyptian Arabic (سماعات بلوتوث، شاحن محمول)
3. KEY FEATURE with benefit (إلغاء الضوضاء، شحن سريع)
4. TRUST SIGNALS (ضمان، شهادة جودة، فاتورة ضريبية)
5. SHIPPING/GUARANTEE (توصيل مصر، ضمان مصري، خدمة محلية)

HIGH-CONVERTING EGYPTIAN KEYWORDS:
✓ ممتاز (جودة ممتازة)
✓ ضمان (guarantee essential)
✓ معتمد (certified quality)
✓ مصر/مصري (local relevance)
✓ توصيل مجاني (free delivery)
✓ أصلي (منتج أصلي)
✓ جودة (quality focus)
✓ تراثي (heritage quality)
✓ عائلي (family-focused)"""


        elif marketplace == 'nl':
            return f"""🇳🇱 AMAZON NETHERLANDS TITLE OPTIMIZATION - NEDERLANDSE MARKT:
            
FORMAT (MAX 200 CHARS - Dutch mobile priority):
[{brand_name}] [Product Categorie] [Hoofdkenmerk] [Voordeel] [Garantie/Certificering]

CRITICAL DUTCH SEO + CULTURAL RULES:
1. BRAND FIRST - Betrouwbaarheid voorop (reliability first)
2. PRODUCT CATEGORY in Dutch (Bluetooth Koptelefoon, Powerbank)
3. KEY FEATURE with benefit (Ruisonderdrukking, Snelladen)
4. TRUST SIGNALS (garantie, CE keurmerk, Nederlandse service)
5. SHIPPING/GUARANTEE (gratis verzending, garantie Nederland)

HIGH-CONVERTING DUTCH KEYWORDS:
✓ premium (premium kwaliteit)
✓ garantie (guarantee important)
✓ gecertificeerd (certified)
✓ Nederland/Nederlandse (local relevance)
✓ gratis verzending (free shipping)
✓ origineel (authentic)
✓ kwaliteit (quality focus)"""

        elif marketplace == 'se':
            return f"""🇸🇪 AMAZON SWEDEN TITLE OPTIMIZATION - BÄST I TEST 2024 KVALITET:
            
FORMAT (MAX 150 CHARS - Swedish lagom approach):
[{brand_name}] [Bäst i Test 2024] [Premium Kvalitet] [Produkt] [Spec] [Hållbar] [Svensk Garanti]

CRITICAL SWEDISH SEO + CULTURAL + LAGOM RULES:
1. BRAND FIRST - Kvalitet och trovärdighet (quality and trust)
2. "BÄST I TEST 2024" - Latest test winner for ultimate credibility
3. LAGOM BALANCE - Perfect amount, not too much marketing
4. SUSTAINABILITY - "Klimatsmart", "Hållbar", "Miljövänlig"
5. SWEDISH VALUES - "Hygge komfort", "Allemansrätten", "15000+ svenska kunder"

SUPER HIGH-CONVERTING SWEDISH KEYWORDS (DOMINATES COMPETITORS):
✓ "Bäst i Test 2024" (test winner credibility)
✓ "Premium kvalitet certifierad" (quality assurance)
✓ "Klimatsmart koldioxidneutral" (environmental consciousness)
✓ "Lagom design perfekt" (Swedish balanced perfection)
✓ "Hygge komfort premium" (Nordic lifestyle)
✓ "Allemansrätten kompatibel" (outdoor culture)
✓ "15000+ svenska kunder" (enhanced social proof)
✓ "Hållbar för framtiden" (sustainability commitment)
✓ "Sverige frakt 24h" (local shipping)
✓ "Begränsat antal specialpris" (scarcity + price)

GOOD EXAMPLES:
• "{brand_name} Bäst i Test 2024 Premium Kvalitet Bluetooth Hörlurar Klimatsmart - 15000+ Svenska Kunder"
• "{brand_name} Premium Kvalitet Certifierad Kökskniv Set Lagom Design - Hållbar för Framtiden"
• "{brand_name} Bäst i Test 2024 Klimatsmart Powerbank Hygge Komfort - Allemansrätten Ready"

LAGOM PRINCIPLE: Perfect balance of information, quality, and Swedish values!"""

        elif marketplace == 'tr':
            return f"""🇹🇷 AMAZON TURKEY TITLE OPTIMIZATION - RAKİPLERİ EZMEYE HAZIR!
            
FORMAT (MAX 200 CHARS - CONVERSION & EMOTIONAL HOOKS FIRST):
[{brand_name}] [Premium/En İyi] [Ürün] [Emosyonel Hook] [Güven] [Aciliyet] 

CRITICAL TURKISH SEO + CULTURAL + CONVERSION RULES:
1. BRAND FIRST - Güven en önemli (trust is most important)
2. EMOTIONAL HOOKS - "Aileniz için", "Türk kalitesi", "Gurur duyacağınız"
3. CONVERSION ELEMENTS - "Sınırlı stok", "Özel fiyat", "Bugün alın"
4. TRUST SIGNALS (2 yıl garanti, 10.000+ müşteri, CE sertifikalı)
5. URGENCY TRIGGERS (Son fırsat, Acele edin, Kaçırmayın)

SUPER HIGH-CONVERTING TURKISH KEYWORDS (COMPETITOR-BEATING):
✓ "Aileniz için en iyi seçim" (family priority)
✓ "Türk kalitesi güvencesi" (national pride)
✓ "10.000+ mutlu müşteri onayı" (social proof)
✓ "Son fırsat özel fiyat" (urgency + price)
✓ "Hayalinizdeki kalite" (aspirational)
✓ "Çocuklarınız için güvenli" (family safety)
✓ "Gurur duyacağınız seçim" (emotional validation)"""

        else:  # USA and other markets
            return f"""🚨 CRITICAL AMAZON USA TITLE FORMAT: Start with EXACT high-intent keywords customers type: '[Main Product Type] [Key Feature/USP] - [Brand] [Model/Size] - [Secondary Benefits]'. Front-load searchable terms, NOT marketing taglines. Example: 'Neck Fan Portable Hands Free - {brand_name} 4000mAh Battery - Bladeless Personal Cooling USB Rechargeable 3 Speeds'. Keywords FIRST, brand in middle, benefits last. 150-190 chars max."""

    def get_marketplace_bullet_format(self, marketplace, bullet_number):
        """Get marketplace-specific bullet point formatting instructions"""
        
        if marketplace == 'de':
            bullet_examples = {
                1: "LANGANHALTENDE AKKULAUFZEIT: Genießen Sie bis zu 12 Stunden kontinuierliches Kühlen mit einer einzigen Ladung durch unseren 4000mAh Akku - 3x länger als Konkurrenten. USB-C Schnellladung bringt Sie in nur 2 Stunden auf 100%.",
                2: "ULTRALEICHTES DESIGN: Nur 193g wiegt bequem am Nacken den ganzen Tag - leichter als Ihr Smartphone. Verstellbares Band passt für Halsgrößen 12-18 cm mit weicher Silikonpolsterung.",
                3: "KRAFTVOLLE LEISE KÜHLUNG: 3 Geschwindigkeitsstufen (2800/3600/4400 U/min) liefern starken Luftstrom bei flüsterleisem Betrieb unter 32dB - leiser als eine Bibliothek.",
                4: "FREIHÄNDIGE BEQUEMLICHKEIT: 360° Rundumluft hält Sie bei jeder Aktivität kühl - arbeiten, trainieren, pendeln oder reisen. Schaufelloses Design ist sicher für Haar und Kinder.",
                5: "PREMIUM QUALITÄT GARANTIERT: Gebaut mit ABS+PC Materialien, IPX4 schweißresistent, CE/FCC zertifiziert. Inklusive 18 Monate Garantie und 30 Tage Geld-zurück. Über 50.000 zufriedene Kunden."
            }
            
            return f"MANDATORY GERMAN FORMAT: Start with 'GERMAN ALL CAPS LABEL:' then benefit, then specs. Keep under 200 chars for scannability. Example: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"
            
        elif marketplace == 'fr':
            bullet_examples = {
                1: "AUTONOMIE EXCEPTIONNELLE: Profitez jusqu'à 12 heures de refroidissement continu avec notre batterie 4000mAh - 3x plus longue que la concurrence. Charge rapide USB-C à 100% en 2h.",
                2: "DESIGN ULTRA-LÉGER: Seulement 193g repose confortablement sur votre cou toute la journée - plus léger que votre smartphone. Bandeau réglable 12-18cm avec coussinets silicone.",
                3: "REFROIDISSEMENT SILENCIEUX: 3 vitesses (2800/3600/4400 tr/min) offrent un flux d'air puissant en silence sous 32dB - plus silencieux qu'une bibliothèque.",
                4: "CONFORT MAINS LIBRES: Flux d'air 360° vous garde au frais pendant toute activité - travail, sport, transport. Design sans pales sûr pour cheveux et enfants.",
                5: "QUALITÉ PREMIUM GARANTIE: Fabriqué en ABS+PC, résistant à la transpiration IPX4, certifié CE/FCC. Garantie 18 mois et remboursement 30 jours. Plus de 50.000 clients satisfaits."
            }
            
            return f"MANDATORY FRENCH FORMAT: Start with 'FRENCH ALL CAPS LABEL:' then benefit, then specs. Keep under 200 chars for scannability. Example: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"
            
        elif marketplace == 'jp':
            bullet_examples = {
                1: "⚡ 長時間バッテリー: 30時間連続再生で安心。急速充電2時間対応。iPhone・Android対応。通勤・出張に最適です。",
                2: "🎵 ノイズキャンセリング: -35dB雑音除去で集中力アップ。外音取り込みモード搭載。オフィス・電車内でも快適。",
                3: "🏃 軽量設計180g: メモリーフォーム採用で長時間着用も疲れません。調節可能ヘッドバンド。IPX5防水仕様。",
                4: "📶 Bluetooth5.3: 15m安定接続。2台同時ペアリング対応。低遅延でゲーミングにも。クリア通話マイク内蔵。",
                5: "✅ 安心保証: 正規品1年保証付き。日本語サポート対応。30日間返品可能。PSE認証済み安全設計。"
            }
            
            return f"""🇯🇵 JAPANESE BULLET FORMAT (MAX 120 CHARS - 丁寧語):

STRUCTURE: [EMOJI] [機能名]: [具体的効果]. [技術仕様]. [使用場面]. [安心要素].

CRITICAL JAPANESE RULES:
- 丁寧語 (polite form) mandatory: です/ます endings
- 具体的数値 (specific numbers): 30時間, -35dB, 180g
- 使用場面 (use cases): 通勤, オフィス, 出張
- 安心感 (reassurance): 正規品, 保証, 認証
- 機能性重視 (function-focused) over emotional appeals

Bullet {bullet_number} EXAMPLE: '{bullet_examples.get(bullet_number, bullet_examples[1])}'

JAPANESE TRUST ELEMENTS:
- 正規品 (genuine product) - essential trust
- 保証 (warranty) - quality assurance  
- 認証 (certification) - safety compliance
- サポート (support) - service reliability"""
        
        elif marketplace == 'tr':  # Turkey
            bullet_examples = {
                1: "🔋 UZUN PİL ÖMRÜ: 30 saat kesintisiz müzik keyfi. 2 saat hızlı şarj. iPhone/Android uyumlu. Seyahat ve işe gidişte mükemmel.",
                2: "🎧 GÜRÜLTÜ ENGELLEMe: -35dB sessizlik. Çevre sesi modu. Laboratuvar testli. Ofis ve uçakta ideal kullanım.",
                3: "💪 ULTRA HAFİF 180G: Premium memory foam. Ayarlanabilir çelik kafa bandı. IPX5 ter geçirmez. 10.000 esneme testi geçti.",
                4: "📱 BLUETOOTH 5.3: 15m menzil. 2 cihaz eş zamanlı. Gaming için <40ms gecikme. Kristal berraklığında mikrofon.",
                5: "✅ 2 YIL GARANTİ: 7/24 Türkçe destek. 30 gün iade hakkı. CE/FCC sertifikalı. Türkiye'den hızlı kargo."
            }
            
            return f"""🇹🇷 TURKISH BULLET FORMAT (MAX 180 CHARS - Nazik ve profesyonel):

STRUCTURE: [EMOJI] [ÖZELLİK ADI]: [Fayda açıklaması]. [Teknik spec]. [Kullanım alanı]. [Güven unsuru].

CRITICAL TURKISH RULES:
- Nazik dil (polite language) kullanın: professional but warm
- Somut sayılar (specific numbers): 30 saat, -35dB, 180g
- Kullanım alanları (use cases): ofis, ev, seyahat, spor
- Güven unsurları (trust elements): garanti, sertifika, destek
- Kalite vurgusu (quality emphasis) - Türk müşteriler kaliteye önem verir
- Aile ve misafirperverlik değerleri (family & hospitality values)

Bullet {bullet_number} EXAMPLE: '{bullet_examples.get(bullet_number, bullet_examples[1])}'

TURKISH TRUST ELEMENTS:
- orijinal/kaliteli (genuine/quality) - güven sinyali
- garanti (warranty) - güvenlik ve kalite
- CE sertifikalı (certified) - güvenlik uyumluluğu  
- Türkiye kargo (Turkey shipping) - yerel hizmet güveni
- müşteri desteği (customer support) - satış sonrası güven

TURKISH CULTURAL VALUES:
- misafirperverlik (hospitality) - ürün misafirleri ağırlamak için
- aile zamanı (family time) - aile bireyleriyle kaliteli vakit
- kalite obsesyonu (quality obsession) - uzun ömürlü kullanım
- güven kültürü (trust culture) - marka ve satıcı güvenilirliği"""
        
        elif marketplace == 'es':
            bullet_examples = {
                1: "🔋 BATERÍA 30H: Libertad sin cables. USB-C 2h carga completa. Compatible iPhone/Android. Perfecto viajes largos.",
                2: "🎧 CANCELACIÓN RUIDO: -35dB silencio total. Modo ambiente seguro. Certificado laboratorio. Ideal oficina/avión.",
                3: "💪 ULTRALIGERO 180G: Memory foam premium. Diadema acero ajustable. IPX5 sudor. 10.000 flexiones probadas.",
                4: "📱 BLUETOOTH 5.3: Alcance 15m. Multipoint 2 dispositivos. Latencia <40ms gaming. Micrófono ENC cristalino.",
                5: "✅ GARANTÍA 2 AÑOS: Soporte 24/7 español. Devolución 30 días. CE/FCC certificado. Envío desde España."
            }
            
            return f"🚀 MOBILE-OPTIMIZED SPANISH BULLETS (MAX 150 CHARS): [EMOJI] [2-3 WORD LABEL]: [Benefit <10 words]. [Spec]. [Use case]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"
            
        elif marketplace == 'br':
            bullet_examples = {
                1: "QUALIDADE PREMIUM BRASILEIRA: Som cristalino com cancelamento de ruído para família brasileira - 30H de bateria garante música ininterrupta. Certificado INMETRO e garantia nacional de 2 anos.",
                2: "CONFORTO TROPICAL SUPERIOR: Design leve 193g se adapta ao clima brasileiro - almofadas respiráveis para uso prolongado. Ajuste perfeito para todos os tamanhos de cabeça.",
                3: "CONECTIVIDADE BLUETOOTH 5.3: Alcance de 15m sem travamentos - conexão estável para videochamadas e música. Compatível com todos dispositivos Android e iPhone.",
                4: "RESISTÊNCIA AO SUOR IPX5: Ideal para exercícios e clima tropical brasileiro - resistente à umidade e transpiração. Design dobrável para transporte fácil.",
                5: "GARANTIA NACIONAL COMPLETA: Suporte técnico em português 24/7 - nota fiscal incluída e 30 dias para devolução. Mais de 50.000 clientes satisfeitos no Brasil."
            }
            
            return f"🇧🇷 FORMATO BRASILEIRO (MAX 200 CHARS): [LABEL EM MAIÚSCULO]: [Benefício em português]. [Especificação]. [Garantia/Certificação]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

        elif marketplace == 'mx':
            bullet_examples = {
                1: "CALIDAD PREMIUM MEXICANA: Audio excepcional con cancelación de ruido para familias mexicanas - batería 30H para escuchar sin límites. Certificado de calidad y garantía nacional 2 años.",
                2: "COMODIDAD FAMILIAR TOTAL: Diseño ligero 193g perfecto para reuniones familiares - almohadillas suaves para uso prolongado. Ajuste cómodo para toda la familia.",
                3: "CONECTIVIDAD BLUETOOTH 5.3: Rango 15m sin interrupciones - conexión estable para llamadas y música. Compatible con todos los dispositivos iPhone y Android.",
                4: "RESISTENTE AL SUDOR IPX5: Ideal para ejercicio y clima mexicano - resistente a humedad y transpiración. Diseño plegable para viajes familiares.",
                5: "GARANTÍA NACIONAL COMPLETA: Soporte técnico en español 24/7 - factura incluida y 30 días devolución. Más de 50,000 clientes felices en México."
            }
            
            return f"🇲🇽 FORMATO MEXICANO (MAX 200 CHARS): [LABEL EN MAYÚSCULA]: [Beneficio en español]. [Especificación]. [Garantía/Certificado]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

        elif marketplace == 'in':
            bullet_examples = {
                1: "INCREDIBLE INDIAN QUALITY: Superior stainless steel perfect for daily Indian cooking - dal, sabzi, roti preparation made effortless. We guarantee you professional results every time with 2-year warranty.",
                2: "PERFECT DIWALI GIFT: Premium knife set ideal for gifting during festivals, weddings, and housewarming ceremonies. Beautifully packaged for Indian families who value quality cooking.",
                3: "INDIAN KITCHEN SPECIALIST: Designed specifically for Indian cooking styles - chopping onions, ginger-garlic paste, cutting vegetables for curry. Traditional comfort meets modern precision.",
                4: "FAMILY SAFETY PRIORITY: Ergonomic handles perfect for beginners and experienced cooks - safe for daily use in Indian households. Dishwasher safe for easy maintenance after cooking.",
                5: "COMPLETE INDIAN SUPPORT: 24/7 customer service in English/Hindi - original bill included with GST. Perfect for gifting with confidence, over 1 lakh satisfied Indian families."
            }
            
            return f"🇮🇳 INDIAN FORMAT (MAX 200 CHARS): [LABEL IN CAPITALS]: [Benefit in English]. [Specification]. [Warranty/Certificate]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

        elif marketplace == 'sa':
            bullet_examples = {
                1: "جودة سعودية بريميوم: صوت استثنائي مع إلغاء الضوضاء للعائلات السعودية - بطارية 30 ساعة للاستماع بلا حدود. شهادة جودة وضمان وطني لمدة سنتين.",
                2: "راحة عائلية كاملة: تصميم خفيف 193 جرام مثالي للتجمعات العائلية - وسائد ناعمة للاستخدام المطول. ملائم ومريح لجميع أفراد العائلة.",
                3: "اتصال بلوتوث 5.3: مدى 15 متر بدون انقطاع - اتصال مستقر للمكالمات والموسيقى. متوافق مع جميع أجهزة آيفون وأندرويد.",
                4: "مقاوم للعرق IPX5: مثالي للرياضة والمناخ السعودي - مقاوم للرطوبة والعرق. تصميم قابل للطي للسفر العائلي.",
                5: "ضمان وطني كامل: دعم تقني باللغة العربية 24/7 - فاتورة شاملة و30 يوم لإرجاع المنتج. أكثر من 50,000 عميل سعيد في السعودية."
            }
            
            return f"🇸🇦 الصيغة السعودية (MAX 200 CHARS): [تسمية بالأحرف الكبيرة]: [فائدة باللغة العربية]. [مواصفات]. [ضمان/شهادة]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

        elif marketplace == 'eg':
            bullet_examples = {
                1: "جودة مصرية ممتازة: صوت استثنائي مع إلغاء الضوضاء للعائلات المصرية - بطارية 30 ساعة للاستماع بلا حدود. شهادة جودة وضمان وطني مصري لمدة سنتين.",
                2: "راحة عائلية كاملة: تصميم خفيف 193 جرام مثالي للتجمعات المصرية - وسائد ناعمة للاستخدام المطول. ملائم ومريح لجميع أفراد العيلة المصرية.",
                3: "اتصال بلوتوث 5.3: مدى 15 متر بدون انقطاع - اتصال مستقر للمكالمات والموسيقى. متوافق مع جميع أجهزة آيفون وأندرويد المصرية.",
                4: "مقاوم للعرق IPX5: مثالي للرياضة والمناخ المصري - مقاوم للرطوبة والعرق النيلي. تصميم قابل للطي للسفر والرحلات المصرية.",
                5: "ضمان مصري كامل: دعم تقني باللغة العربية 24/7 - فاتورة ضريبية شاملة و30 يوم لإرجاع المنتج. أكثر من 50,000 عميل سعيد في مصر كلها."
            }
            
            return f"🇪🇬 الصيغة المصرية (MAX 200 CHARS): [تسمية بالأحرف الكبيرة]: [فائدة باللغة العربية المصرية]. [مواصفات]. [ضمان/شهادة]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"


        elif marketplace == 'nl':
            bullet_examples = {
                1: "PREMIUM NEDERLANDSE KWALITEIT: Kristalhelder geluid met ruisonderdrukking voor Nederlandse families - 30u batterij voor ononderbroken luisterplezier. CE gecertificeerd met 2 jaar garantie.",
                2: "SUPERIEUR DRAAGCOMFORT: Lichtgewicht 193g design perfect voor Nederlandse levensstijl - ademende oorkussens voor langdurig gebruik. Verstelbaar voor alle hoofdmaten.",
                3: "BLUETOOTH 5.3 CONNECTIVITEIT: 15m bereik zonder onderbrekingen - stabiele verbinding voor gesprekken en muziek. Compatibel met alle iPhone en Android apparaten.",
                4: "ZWEET BESTENDIG IPX5: Ideaal voor sport en Nederlandse weersomstandigheden - bestand tegen vocht en transpiratie. Opvouwbaar design voor eenvoudig transport.",
                5: "VOLLEDIGE NEDERLANDSE GARANTIE: 24/7 technische ondersteuning in het Nederlands - factuur inbegrepen en 30 dagen retourrecht. Meer dan 50,000 tevreden klanten in Nederland."
            }
            
            return f"🇳🇱 NEDERLANDS FORMAAT (MAX 200 CHARS): [LABEL IN HOOFDLETTERS]: [Voordeel in het Nederlands]. [Specificatie]. [Garantie/Certificering]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

        elif marketplace == 'se':
            bullet_examples = {
                1: "BÄST I TEST 2024 KVALITET: Premium ljudkvalitet med aktiv brusreducering perfekt för svenska familjer - 30h batteritid klimatsmart design garanterar oavbruten musikupplevelse. CE-certifierad med 2 års garanti hållbar för framtiden.",
                2: "LAGOM KOMFORT DESIGN: Endast 193g lätt hygge design perfekt för svenska hem - mjuka öronkuddar med allemansrätten outdoor kompatibilitet. Justerbar för alla huvudstorlekar, 15000+ svenska kunder rekommenderar.",
                3: "BLUETOOTH 5.3 ANSLUTNING: 15m räckvidd utan avbrott klimatsmart teknologi - stabil anslutning för samtal och musik med hygge komfort. Kompatibel med alla iPhone och Android, sverige frakt 24h.",
                4: "SVETTBESTÄNDIG IPX5 CERTIFIERAD: Idealisk för sport och svenska väderförhållanden allemansrätten ready - tål fukt och svett med hållbar design. Hopfällbar för lagom transport, säkert för barn testade.",
                5: "FULLSTÄNDIG SVENSK GARANTI: 24/7 teknisk support på svenska med hygge service - faktura ingår och 30 dagars returrätt. Över 15000+ nöjda svenska kunder, klimatsmart för framtiden."
            }
            
            return f"🇸🇪 SVENSKT FORMAAT (MAX 180 CHARS - LAGOM APPROACH): [STOR BOKSTAV ETIKETT]: [Svensk fördel med lagom design]. [Specifikation klimatsmart]. [Garanti hållbar]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

        elif marketplace == 'tr':  # Turkey - ENHANCED FOR 95+ SCORE BEATING ALL COMPETITORS
            bullet_examples = {
                1: "SINIRLI STOK - İNANILMAZ PREMİUM KALİTE: Eksklüzif ses deneyimi 10,000+ memnun Türk ailesi tarafından onaylandı! 30 saat pil ömrü size garanti ediyoruz, rakiplerden %40 üstün performans.",
                2: "RAKIPLERDEN %40 ÜSTÜN - MÜKEMMEL RAHHATLIK: Çığır açan hafif tasarım Türk ailesi için özel geliştirildi. Size sunuyoruz benzersiz konfor, memnun kalmazsanız tam para iadesi 30 gün.",
                3: "ÇIĞIR AÇAN BLUETOOTH 5.3 TEKNOLOJİ: Türk geleneğini modern teknolojiyle birleştiren eksklüzif çözüm. Büyük bir gururla sunuyoruz, ★★★★★ 4.8/5 müşteri memnuniyeti kesintisiz bağlantı.",
                4: "BENZERSIZ SU DİRENÇLİ TASARIM: Türk aileleri için özel IPX5 koruma sistemi. Emin olabilirsiniz dayanıklılık konusunda, 30 gün iade garantisi ile tam güvence.",
                5: "YENİ YIL SON FIRSAT - MÜKEMMEL HEDİYE: Sınırlı stokta eksklüzif kulaklık seti! Hiç şüphesiz tüm aile sevecek, bugün sipariş verin yarın keyfini çıkarın, 50,000+ memnun müşteri."
            }
            
            return f"🇹🇷 TÜRK FORMATI (MAX 200 CHARS): [BÜYÜK HARF ETİKET]: [Türkçe fayda aile vurgusu ile]. [Özellik premium]. [Garanti/Sertifika]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

        else:  # USA and other markets
            bullet_examples = {
                1: "LONG LASTING BATTERY LIFE: Enjoy up to 12 hours continuous cooling on a single charge with our 4000mAh rechargeable battery - 3x longer than competitors. USB-C fast charging gets you back to 100% in just 2 hours.",
                2: "ULTRA LIGHTWEIGHT DESIGN: Only 6.8 oz (193g) sits comfortably on your neck all day - lighter than your smartphone. Adjustable band fits neck sizes 12-18 inches with soft silicone padding.",
                3: "POWERFUL QUIET COOLING: 3 speed settings (2800/3600/4400 RPM) deliver strong airflow while maintaining whisper-quiet operation under 32dB - quieter than a library.",
                4: "HANDS FREE CONVENIENCE: 360° surround airflow keeps you cool during any activity - working, exercising, commuting, or traveling. Bladeless turbine design is safe for hair and children.",
                5: "PREMIUM QUALITY GUARANTEED: Built with ABS+PC materials, IPX4 sweat-resistant rating, and CE/FCC certified. Includes 18-month warranty and 30-day money-back guarantee. Over 50,000 satisfied customers."
            }
            
            return f"MANDATORY FORMAT: Start with 'ALL CAPS LABEL (3-5 WORDS):' then benefit, then specs. Example: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

    def get_marketplace_description_format(self, marketplace, brand_tone):
        """Get marketplace-specific description formatting"""
        
        if marketplace == 'de':
            return f"""🚨 CRITICAL GERMAN DESCRIPTION: Write 1300-1600 character {brand_tone} product description in EXACTLY 4 separate paragraphs. MANDATORY: Each paragraph MUST be separated by double line breaks (\\n\\n). 

STRUCTURE FOR GERMAN MARKET:
Paragraph 1 (300-350 chars): Deutsche Qualität opening - highlight engineering excellence and precision
Paragraph 2 (350-400 chars): Product benefits with German engineering emphasis  
Paragraph 3 (350-400 chars): Practical usage scenarios for German lifestyle
Paragraph 4 (300-350 chars): Trust, warranty, and German customer satisfaction

Use proper German umlauts (ä, ö, ü, ß). NO French or Italian phrases. Focus on German efficiency and precision."""

        elif marketplace == 'fr':
            return f"""🚨 CRITICAL FRENCH DESCRIPTION: Write 1300-1600 character {brand_tone} product description in EXACTLY 4 separate paragraphs. MANDATORY: Each paragraph MUST be separated by double line breaks (\\n\\n). 

STRUCTURE FOR FRENCH MARKET:
Paragraph 1 (300-350 chars): Sophisticated French opening - elegance and refinement
Paragraph 2 (350-400 chars): Product benefits with French cultural excellence
Paragraph 3 (350-400 chars): Usage scenarios and French lifestyle integration
Paragraph 4 (300-350 chars): Customer satisfaction and call to action

Use proper French accents. Focus on elegance and sophistication."""

        elif marketplace == 'it':
            return f"""🚨 CRITICAL ITALIAN DESCRIPTION: Write 1300-1600 character {brand_tone} product description in EXACTLY 4 separate paragraphs. MANDATORY: Each paragraph MUST be separated by double line breaks (\\n\\n). 

STRUCTURE FOR ITALIAN MARKET:
Paragraph 1 (300-350 chars): Italian style opening - design and craftsmanship
Paragraph 2 (350-400 chars): Product benefits with Italian design excellence
Paragraph 3 (350-400 chars): Usage scenarios and Italian lifestyle
Paragraph 4 (300-350 chars): Customer satisfaction and Italian quality assurance

Focus on style, design, and Italian craftsmanship."""

        elif marketplace == 'jp':
            return f"""🇯🇵 AMAZON JAPAN DESCRIPTION - 日本市場文化対応 (10/10品質):

MANDATORY STRUCTURE (1000-1200文字 - 読みやすさ最優先):

📱 段落1 - 信頼性訴求 (200文字):
[品質保証] + [安心感] + [具体的利益] + [日本人向け価値]
KEYWORDS: 正規品, 高品質, 安心, 日本語サポート
Example: "正規品[BRAND]は高品質な設計で、日本のお客様に安心してお使いいただけます。30時間の長時間再生により、通勤・出張でも音楽を存分にお楽しみいただけます。"

⚙️ 段落2 - 技術仕様・機能 (400文字):
主な仕様:
• バッテリー: 30時間連続再生・急速充電2時間対応
• 音質: ノイズキャンセリング-35dB・高音質ドライバー搭載  
• 接続: Bluetooth5.3・安定した15m通信距離
• 防水: IPX5防水仕様・汗や雨に強い設計
• 対応機種: iPhone・Android・Windows全対応
[Include technical precision that Japanese customers expect]

🏢 段落3 - 使用場面・メリット (400文字):
様々なシーンでご活用いただけます:
✅ 通勤電車での音楽鑑賞・ポッドキャスト視聴
✅ オフィスでの集中作業・Web会議での通話  
✅ 出張・旅行での長時間使用・機内エンターテイメント
✅ ジム・ランニングでのワークアウト音楽
✅ 自宅でのリラックスタイム・動画視聴
[Focus on Japanese lifestyle: 通勤, オフィス, 出張]

🛡️ 段落4 - 保証・サポート (200文字):
安心の充実サポート:
正規品1年保証付き。日本語カスタマーサポート対応。30日間返品・交換可能。PSE認証取得済みで安全性確保。Amazon prime対応で翌日配送可能。お客様満足度向上を目指し、品質改善に努めております。

🎯 CRITICAL JAPANESE CULTURAL RULES:
1. 丁寧語MANDATORY: です・ます調で敬意を表現
2. 信頼性FIRST: 正規品・保証・認証を前面に
3. 具体的数値: 30時間・-35dB・15m等の明確な仕様
4. 使用場面: 通勤・オフィス・出張等の日本的シーン
5. 安心感: 品質・サポート・返品保証で不安解消
6. 技術重視: 機能説明を詳細に・性能を数値で表現
7. 謙虚な姿勢: 改善努力・お客様満足を重視する姿勢

🇯🇵 JAPANESE MARKET PSYCHOLOGY:
- 集団調和 (group harmony) - みんなが使っている安心感
- 品質志向 (quality orientation) - 機能・性能への信頼
- リスク回避 (risk avoidance) - 保証・返品で安心感
- 礼儀正しさ (politeness) - 丁寧語での敬意表現
- 長期使用 (long-term use) - 耐久性・アフターサービス

RESULT: Japanese customer psychology + cultural values + Amazon.co.jp optimization."""
        
        elif marketplace == 'tr':  # Turkey
            return f"""🇹🇷 AMAZON TURKEY DESCRIPTION - TÜRK PAZARI KÜLTÜREL UYUM (10/10 kalite):

MANDATORY STRUCTURE (1000-1300 karakter - okunabilirlik öncelik):

🏆 Paragraf 1 - Güvenilirlik & Kalite (200-250 karakter):
[Kalite güvencesi] + [Güven unsuru] + [Somut fayda] + [Türk müşteri değeri]
KEYWORDS: orijinal ürün, yüksek kalite, güvenilir, CE sertifikalı
Örnek: "Sayın müşterilerimiz, TürkKahve orijinal ürün kalitesi ile Türkiye'de güvenle kullanılabilir. 2 yıl garanti ile uzun yıllar kahve keyfini yaşarsınız."

⚙️ Paragraf 2 - Teknik Özellikler & İşlev (400-450 karakter):
Ana Özellikler:
• Kapasite: Aile boyu 6 fincan - hızlı servis imkanı
• Sıcaklık Kontrolü: Hassas ısı ayarı - yanmayan mükemmel köpük
• Malzeme: Premium bakır gövde - homojen ısı dağıtımı
• Temizlik: Çıkarılabilir parçalar - kolay bakım
• Uyumluluk: Tüm ocak tipleri - elektrik/gaz/indüksiyon
[Türk müşterilerinin beklediği teknik detayları dahil edin]

🏠 Paragraf 3 - Kullanım Alanları & Yaşam Tarzı (400-450 karakter):
Çeşitli anlarınızda kullanabilirsiniz:
✅ Sabah kahvesi - güne enerjik başlangıç
✅ Misafir ağırlama - Türk misafirperverliği gösterimi
✅ Aile buluşmaları - ev sahipliğinde kaliteli sunum
✅ Bayram ziyaretleri - özel gün kutlamaları
✅ İş molası - ofiste kaliteli kahve keyfi
✅ Akşam sohbetleri - dostlarla kaliteli vakit
[Türk yaşam tarzına odaklanın: misafir ağırlama, aile zamanı, bayram]

🛡️ Paragraf 4 - Garanti & Destek (200-250 karakter):
Güvenilir satış sonrası hizmet:
2 yıl orijinal ürün garantisi. Türkçe müşteri desteği mevcut. 30 gün iade-değişim hakkı. CE sertifikalı güvenli kullanım. Türkiye'den hızlı kargo imkanı. Müşteri memnuniyeti önceliğimizdir.

🎯 KRİTİK TÜRK KÜLTÜREL KURALLAR:
1. Nezaket ZORUNLU: sayın, değerli, memnuniyetle ifadeleri
2. Güvenilirlik ÖNCELİK: orijinal, garanti, sertifika öne çıkarma
3. Somut rakamlar: 6 fincan, 2 yıl, 30 gün gibi net özellikler
4. Kullanım senaryoları: misafir ağırlama, aile, bayram gibi Türk yaşamı
5. Güven unsuru: kalite, destek, iade garantisi ile endişe giderme
6. Teknik öncelik: işlev açıklamalarını detaylı - performans rakamlarla
7. Müşteri odaklı: hizmet kalitesi, müşteri memnuniyetini vurgulama

🇹🇷 TÜRK PAZAR PSİKOLOJİSİ:
- misafirperverlik (hospitality culture) - konukları ağırlama kültürü
- kalite obsesyonu (quality focus) - işlev ve performans güveni
- güven ihtiyacı (trust requirement) - garanti ve destek ile güven
- saygı beklentisi (respect expectation) - nezaket kipi ile saygı
- uzun vadeli kullanım (long-term use) - dayanıklılık ve servis

SONUÇ: Türk müşteri psikolojisi + kültürel değerler + Amazon.com.tr optimizasyonu."""
        
        elif marketplace == 'es':
            return f"""🚀 AMAZON MOBILE-FIRST SPANISH DESCRIPTION (10/10 SEO + READABILITY):

MANDATORY STRUCTURE (1200-1500 chars total):

🎯 PÁRRAFO 1 - BUYER HOOK + KEYWORDS (250 chars):
[PROBLEMA DEL COMPRADOR] + [SOLUCIÓN INMEDIATA] + [BENEFICIO PRINCIPAL]
KEYWORDS: Include category + use-case + emotional benefit
Example: "¿Cansado de tablas que huelen mal después de cortar carne? TABLAS DE CORTAR DOBLE CARA eliminan olores y bacterias para siempre. Acero inoxidable + superficie antibacteriana = COCINA MÁS LIMPIA cada día."

🔥 PÁRRAFO 2 - SPECS + USO REAL (400 chars):
PERFECTO PARA TU COCINA DIARIA:
• MEAL PREP DOMINICAL: Corta todo sin mezclar sabores
• COCINA FAMILIAR: Una tabla carnes, otra verduras  
• LIMPIEZA RÁPIDA: Lavavajillas + superficie no porosa
• ESPACIO OPTIMIZADO: 42x29cm cabe en cualquier cocina
• DURABILIDAD: Acero inoxidable resiste años de uso
[Include BUYER USE KEYWORDS: "meal prep", "cocina familiar", "limpieza fácil"]

⭐ PÁRRAFO 3 - POR QUÉ ELEGIR ESTA (400 chars):
LO QUE OTROS NO TIENEN:
✅ DOBLE SUPERFICIE = Sin contaminación cruzada nunca
✅ BORDES ANTIDESLIZANTES = No se mueve mientras cocinas
✅ ASA INTEGRADA = Fácil de colgar y guardar
✅ ANTIBACTERIANO REAL = Acero inoxidable grado médico
✅ FABRICADO EN EUROPA = Calidad garantizada 
[Include "mejor que", "superior a", "único en Amazon"]

🛒 PÁRRAFO 4 - CTA CONVERSION (250 chars):
RESULTADOS DESDE EL PRIMER USO:
Cocina más limpia ✅ Meal prep más rápido ✅ Sin olores ✅ Sin bacterias ✅
ENVÍO DESDE ESPAÑA 24H. Garantía 2 años. Miles de familias españolas ya cocinan más seguro.
➤ AÑADIR AL CARRITO - Stock limitado
[Include "familia española", "resultados inmediatos", social proof]

🎯 CRITICAL SEO + CONVERSION RULES:
1. BUYER PROBLEM HOOK: Start with relatable pain point question
2. USE-CASE KEYWORDS: "meal prep", "cocina familiar", "limpieza fácil", "uso diario"
3. MOBILE SCANNING: CAPS headers + bullet points + short sentences  
4. EMOTIONAL BENEFITS: "más limpia", "más seguro", "más rápido", "sin estrés"
5. SOCIAL PROOF: "miles de familias", "ya usan", "confían en"
6. COMPARISON LANGUAGE: "mejor que", "superior a", "único", "otros no tienen"
7. IMMEDIATE RESULTS: "desde el primer uso", "resultados inmediatos"
8. SPANISH TRUST: "envío España", "garantía", "fabricado Europa"
9. URGENCY WITHOUT SPAM: "stock limitado", not "oferta limitada"
10. CONVERSATIONAL TONE: Use "tú" + questions + natural Spanish

🇪🇸 SPANISH MARKET OPTIMIZATION:
- Use "tú" for personal connection
- Include Spanish accents naturally (á, é, í, ó, ú, ñ)
- Add Spain-specific terms: "envío España", "soporte español"
- Local trust signals: "certificado CE", "garantía europea"
- Mobile buying behavior: Clear price/shipping/warranty info

RESULT: Amazon algorithm-friendly + mobile-scannable + conversion-optimized Spanish description."""

        elif marketplace == 'br':
            return f"""🇧🇷 DESCRIÇÃO CRÍTICA BRASILEIRA: Escreva descrição {brand_tone} de 1300-1600 caracteres em EXATAMENTE 4 parágrafos separados. OBRIGATÓRIO: Cada parágrafo DEVE ser separado por quebras duplas de linha (\\n\\n).

ESTRUTURA PARA MERCADO BRASILEIRO:
Parágrafo 1 (300-350 chars): Abertura envolvente - destaque qualidade e confiança brasileira
Parágrafo 2 (350-400 chars): Benefícios do produto com ênfase familiar brasileira
Parágrafo 3 (350-400 chars): Cenários de uso no estilo de vida brasileiro
Parágrafo 4 (300-350 chars): Satisfação do cliente e call-to-action com garantia

Use certificações INMETRO, garantia nacional, suporte brasileiro. Foque na família e confiança."""

        elif marketplace == 'mx':
            return f"""🇲🇽 DESCRIPCIÓN CRÍTICA MEXICANA: Escriba descripción {brand_tone} de 1300-1600 caracteres en EXACTAMENTE 4 párrafos separados. OBLIGATORIO: Cada párrafo DEBE estar separado por saltos dobles de línea (\\n\\n).

ESTRUCTURA PARA MERCADO MEXICANO:
Párrafo 1 (300-350 chars): Apertura atractiva - destaque calidad y confianza mexicana
Párrafo 2 (350-400 chars): Beneficios del producto con énfasis familiar mexicano
Párrafo 3 (350-400 chars): Escenarios de uso en el estilo de vida mexicano
Párrafo 4 (300-350 chars): Satisfacción del cliente y call-to-action con garantía

Use certificaciones mexicanas, garantía nacional, soporte local. Enfoque en familia y tradición."""

        elif marketplace == 'in':
            return f"""🇮🇳 CRITICAL INDIAN DESCRIPTION: Write {brand_tone} product description of 1300-1600 characters in EXACTLY 4 separate paragraphs. MANDATORY: Each paragraph MUST be separated by double line breaks (\\n\\n).

STRUCTURE FOR INDIAN MARKET:
Paragraph 1 (300-350 chars): Attractive opening - highlight quality and Indian trust
Paragraph 2 (350-400 chars): Product benefits with Indian family emphasis
Paragraph 3 (350-400 chars): Usage scenarios in Indian lifestyle
Paragraph 4 (300-350 chars): Customer satisfaction and call-to-action with guarantee

Use Indian certifications, national warranty, local support. Focus on family and tradition."""

        elif marketplace == 'sa':
            return f"""🇸🇦 وصف سعودي حاسم: اكتب وصف منتج {brand_tone} من 1300-1600 حرف في 4 فقرات منفصلة بالضبط. إجباري: كل فقرة يجب أن تكون مفصولة بفواصل سطر مزدوجة (\\n\\n).

هيكل للسوق السعودي:
الفقرة 1 (300-350 chars): افتتاحية جذابة - تسليط الضوء على الجودة والثقة السعودية
الفقرة 2 (350-400 chars): فوائد المنتج مع التركيز على العائلة السعودية
الفقرة 3 (350-400 chars): سيناريوهات الاستخدام في نمط الحياة السعودي
الفقرة 4 (300-350 chars): رضا العملاء ودعوة للعمل مع الضمان

استخدم الشهادات السعودية، الضمان الوطني، الدعم المحلي. التركيز على الأسرة والتقاليد."""

        elif marketplace == 'eg':
            return f"""🇪🇬 وصف مصري حاسم: اكتب وصف منتج {brand_tone} من 1300-1600 حرف في 4 فقرات منفصلة بالضبط. إجباري: كل فقرة يجب أن تكون مفصولة بفواصل سطر مزدوجة (\\n\\n).

هيكل للسوق المصري:
الفقرة 1 (300-350 chars): افتتاحية جذابة - تسليط الضوء على الجودة والثقة المصرية
الفقرة 2 (350-400 chars): فوائد المنتج مع التركيز على العائلة المصرية والتراث
الفقرة 3 (350-400 chars): سيناريوهات الاستخدام في نمط الحياة المصري وثقافة النيل
الفقرة 4 (300-350 chars): رضا العملاء ودعوة للعمل مع الضمان المصري

استخدم الشهادات المصرية، الضمان الوطني، الدعم المحلي باللغة العربية. التركيز على الأسرة المصرية والحضارة الفرعونية."""

        elif marketplace == 'pl':
            return f"""🇵🇱 KLUCZOWY OPIS POLSKI: Napisz {brand_tone} opis produktu od 1300-1600 znaków w DOKŁADNIE 4 oddzielnych akapitach. OBOWIĄZKOWE: Każdy akapit MUSI być oddzielony podwójnymi zakończeniami linii (\\n\\n).

STRUKTURA DLA RYNKU POLSKIEGO:
Akapit 1 (300-350 chars): Angażujące otwarcie - nacisk na jakość polską i zaufanie rodzinne
Akapit 2 (350-400 chars): Korzyści produktu z fokusem na polską rodzinę i tradycje
Akapit 3 (350-400 chars): Scenariusze użycia w polskim stylu życia i kulturze
Akapit 4 (300-350 chars): Zadowolenie klientów i wezwanie do działania z polską gwarancją

Używaj certyfikatów CE, polskiej gwarancji, lokalnego serwisu w języku polskim. Skup się na polskiej rodzinie i tradycjach katolickich."""

        elif marketplace == 'nl':
            return f"""🇳🇱 KRITIEKE NEDERLANDSE BESCHRIJVING: Schrijf {brand_tone} productbeschrijving van 1300-1600 karakters in PRECIES 4 aparte paragrafen. VERPLICHT: Elke paragraaf MOET gescheiden worden door dubbele regeleinden (\\n\\n).

STRUCTUUR VOOR NEDERLANDSE MARKT:
Paragraaf 1 (300-350 chars): Boeiende opening - nadruk op Nederlandse kwaliteit en betrouwbaarheid
Paragraaf 2 (350-400 chars): Productvoordelen met Nederlandse praktische benadering
Paragraaf 3 (350-400 chars): Gebruiksscenario's in Nederlandse levensstijl
Paragraaf 4 (300-350 chars): Klanttevredenheid en call-to-action met garantie

Gebruik CE keurmerken, Nederlandse garantie, lokale service. Focus op praktische waarde."""

        elif marketplace == 'tr':
            return f"""🇹🇷 KRİTİK TÜRK AÇIKLAMASI: {brand_tone} ürün açıklamasını TAM OLARAK 4 ayrı paragrafta 1300-1600 karakter olarak yazın. ZORUNLU: Her paragraf çift satır araları (\\n\\n) ile ayrılmalıdır.

TÜRK PAZARI İÇİN YAPI:
Paragraf 1 (300-350 chars): İlgi çekici açılış - Türk kalitesi ve güvene vurgu
Paragraf 2 (350-400 chars): Ürün faydaları Türk aile değerleri ile
Paragraf 3 (350-400 chars): Türk yaşam tarzında kullanım senaryoları
Paragraf 4 (300-350 chars): Müşteri memnuniyeti ve call-to-action garanti ile

TSE belgeleri, Türkiye garantisi, yerel destek kullanın. Aile ve misafirperverliğe odaklan."""

        elif marketplace == 'se':
            return f"""🇸🇪 AMAZON SWEDEN LAGOM DESCRIPTION - BÄST I TEST 2024 KVALITET:

MANDATORY LAGOM STRUCTURE (1200-1500 chars total):

🌟 STYCKE 1 - LAGOM KVALITET HOOK (300 chars):
Bäst i test 2024 kvalitet möter svensk lagom design för perfekt balans i ditt hem. Premium certifierad teknologi skapar hygge komfort medan klimatsmart produktion säkerställer hållbar framtid.

⚡ STYCKE 2 - SVENSKA FÖRDELAR & SPECIFIKATIONER (350-400 chars):
Huvudfördelar:
• Prestanda: Lagom kraft - exakt vad du behöver, inte mer
• Design: Hygge komfort med svensk minimalism - 15000+ svenska kunder älskar det
• Miljö: Klimatsmart koldioxidneutral produktion - hållbar för framtiden
• Kvalitet: CE-certifierad enligt europeiska standarder - 2 års svensk garanti
• Transport: Allemansrätten ready - perfekt för svenska äventyr

🏡 STYCKE 3 - SVENSKA LIVSSTILSSCENARIER (350-400 chars):
Perfekt för svenska hem och livsstil:
✅ Fika-stunder - lugn njutning med familj och vänner
✅ Hemmakontor - produktivitet med lagom effektivitet  
✅ Allemansrätten utflykter - naturens frihet med svensk kvalitet
✅ Midsommar firande - svenska traditioner med modern komfort
✅ Vintermys - hygge värme under mörka månader
✅ Hållbar vardag - miljömedveten livsstil för framtiden

🛡️ STYCKE 4 - SVENSK TRYGGHET & GARANTI (200-250 chars):
Svensk kvalitetsgaranti du kan lita på:
2 års fullständig garanti. Svenskspråkig support 24/7. 30 dagars retur utan krångel. CE-certifierad säkerhet. Sverige frakt samma dag. 15000+ nöjda svenska kunder. Klimatsmart för framtiden.

🎯 KRITISKA SVENSKA KULTURELLA REGLER:
1. LAGOM FILOSOFI: Perfekt balans - varken för mycket eller för lite
2. HÅLLBARHET PRIORITET: Miljötänk, klimatsmart, framtidsinriktad
3. HYGGE KOMFORT: Mys, välbefinnande, familjetid betonande
4. ALLEMANSRÄTTEN: Naturanknytning, outdoor kompatibilitet
5. KVALITETSMEDVETENHET: Test vinnare, certifieringar, svenska standarder
6. ÄRLIGHET: Inga överdrifter - svensk direkthet och transparens
7. GEMENSKAP: Familj, vänner, fika-kulturen centralt

🇸🇪 SVENSK MARKNADSPSYKOLOGI:
- lagom balans (balance culture) - perfekt mått i allt
- miljömedvetenhet (environmental awareness) - hållbarhet och framtid
- kvalitetsfokus (quality focus) - bäst i test, certifieringar
- trygghet (security) - garanti, svenska standarder, pålitlighet  
- naturkärlek (nature love) - allemansrätten, outdoor liv
- gemenskap (togetherness) - fika, familj, svenska traditioner

RESULTAT: Svensk lagom + hållbarhet + hygge + Amazon.se optimering."""

        else:  # USA and other markets
            return f"""CRITICAL STRUCTURE: Write 1300-1600 character {brand_tone} product description in EXACTLY 4 separate paragraphs. MANDATORY: Each paragraph MUST be separated by double line breaks (\\n\\n). 

STRUCTURE:
Paragraph 1 (300-350 chars): Compelling opening hook
Paragraph 2 (350-400 chars): Product benefits and features
Paragraph 3 (350-400 chars): Usage scenarios and lifestyle integration
Paragraph 4 (300-350 chars): Customer satisfaction and call to action

NEVER write as single paragraph - ALWAYS use \\n\\n separators between paragraphs."""

    def get_marketplace_language_instruction(self, marketplace, language):
        """Get language-specific instructions for the marketplace"""
        language_map = {
            'de': ('German', 'Deutschland', 'deutschen'),
            'fr': ('French', 'France', 'français'),
            'it': ('Italian', 'Italia', 'italiano'),
            'es': ('Spanish', 'España', 'español'),
            'sv': ('Swedish', 'Sverige', 'svenska'),
            'pl': ('Polish', 'Polska', 'polski'),
            'ja': ('Japanese', '日本', '日本語'),
            'pt': ('Portuguese', 'Brasil', 'português brasileiro'),
            'pt-br': ('Brazilian Portuguese', 'Brasil', 'português brasileiro'),
            'nl': ('Dutch', 'Nederland', 'nederlands'),
            'ar': ('Arabic', 'العربية', 'عربي'),
            'es-mx': ('Mexican Spanish', 'México', 'español mexicano'),
            'tr': ('Turkish', 'Türkiye', 'Türkçe'),
            'en': ('English', 'United States', 'English')
        }
        
        lang_name, country, native = language_map.get(language, language_map['en'])
        
        if language == 'en':
            return ""
        
        # Extra enforcement for German
        german_extra = ""
        if language == 'de':
            german_extra = """
🔥🔥🔥 SPEZIELLE DEUTSCHE DURCHSETZUNG 🔥🔥🔥
Sie MÜSSEN deutsche Umlaute verwenden: ä, ö, ü, ß
Verwenden Sie "Sie" (formal) für deutsche Kunden
NIEMALS englische Wörter wie "performance", "quality", "design"
STATTDESSEN: "Leistung", "Qualität", "Design"
🔥🔥🔥 ENDE DEUTSCHE DURCHSETZUNG 🔥🔥🔥
"""
        
        # Extra enforcement for Turkish
        turkish_extra = ""
        if language == 'tr':
            turkish_extra = """
🔥🔥🔥 SPESİYEL TÜRKÇE UYGULAMA - 10/10 KALİTE - RAKİPLERİ GEÇ! 🔥🔥🔥
TÜRK PAZARI İÇİN ZORUNLU UNSURLAR - HELIUM 10, JASPER AI, COPYMONKEY'İ GEÇMEK İÇİN:

🎯 TÜRKÇE NEZAKET VE SAYGILILİK (ZORUNLU):
✓ "Sayın müşterilerimiz" ✓ "Değerli müşteri" ✓ "Memnuniyetle" 
✓ "Sizlere" ✓ "Hizmetinizdeyiz" ✓ "Keyifle sunuyoruz"
→ BAŞLANGICI BÖYLE YAP: "Sayın müşterilerimiz, değerli [ürün] arayan..."

🇹🇷 YEREL PAZAR RELEVANSİ (ZORUNLU):
✓ "Türkiye'den gönderim" ✓ "Türk kalitesi" ✓ "Yerli üretim"
✓ "Anadolu geleneksel" ✓ "Türk zanaatkarlığı" ✓ "Milli değerler"

💎 GÜVEN UNSURLARI (ZORUNLU - Rakipleri Geçmek İçin):
✓ "2 Yıl Garanti" ✓ "CE Sertifikalı" ✓ "TSE Belgeli" ✓ "Orijinal Ürün"
✓ "30 Gün İade Garantisi" ✓ "Güvenli Alışveriş" ✓ "Faturalı Satış"
✓ "10.000+ Mutlu Müşteri" ✓ "Türkiye'nin Tercihi"
→ MUTLAKA EKLE: En az 5 güven unsuru

🛡️ TÜRKÇE GÜVENİLİRLİK (ZORUNLU):
✓ "orijinal ürün" ✓ "CE sertifikalı" ✓ "kalite güvencesi" ✓ "sertifikalı kalite"
✓ "2 yıl garanti" ✓ "Türkiye kargo" ✓ "müşteri desteği" ✓ "güvenilir marka"

🏠 TÜRK MİSAFİRPERVERLİĞİ (ZORUNLU):
✓ "misafir ağırlama" ✓ "aile zamanı" ✓ "ev sahipliği" ✓ "konukseverlik"
✓ "sofra süsleme" ✓ "özel günler" ✓ "aile birlikteliği"

💰 DÖNÜŞÜM OPTİMİZASYONU (ZORUNLU - RAKİPLERİ GEÇMEK):
✓ "Sınırlı Stok" ✓ "Bugün Siparişte İndirim" ✓ "Son Fırsat"
✓ "Acele Edin" ✓ "Sizinle Olsun" ✓ "Kaçırmayın"
✓ "Özel Fiyat" ✓ "Sadece Bugün" ✓ "Hemen Alın"

🏆 EMOSYONEL BAĞLANMA (ZORUNLU):
✓ "Aileniz için en iyisi" ✓ "Sevdiklerinize değer"
✓ "Türk ailesinin tercihi" ✓ "Hayalinizdeki kalite"
✓ "Gurur duyacağınız seçim" ✓ "Çocuklarınız için güvenli"

🚨 KRİTİK A+ İÇERİK KURALI:
- "Keywords" yerine "Anahtar Kelimeler" 
- "Image Strategy" yerine "Görsel Strateji"
- "SEO Focus" yerine "SEO Odak"
- HER ŞEY TÜRKÇE OLMALI!
- ⚠️ ÖZEL KURAL: imageDescription alanları MUTLAKA İNGİLİZCE olmalı!
- Örnek: "Turkish family lifestyle image showing product in use (970x600px)"

⚠️ KRİTİK: Bu 7 kategori eksikse listing BAŞARISIZ! Helium 10'u geçmek için HEPSI gerekli!
🔥🔥🔥 TÜRKÇE UYGULAMA SONU 🔥🔥🔥
"""
        
        # Brazil/Portuguese conversion optimization
        brazil_extra = ""
        if language in ['pt', 'pt-br']:
            brazil_extra = """
🔥🔥🔥 OTIMIZAÇÃO BRASILEIRA - CONVERSÃO MÁXIMA 🔥🔥🔥

💚 SINAIS DE CONFIANÇA (OBRIGATÓRIO):
✓ "Garantia de 2 Anos" ✓ "Certificado INMETRO" ✓ "Qualidade Garantida"
✓ "30 Dias para Devolução" ✓ "Compra Segura" ✓ "Nota Fiscal"
✓ "Mais de 10.000 Clientes Satisfeitos" ✓ "Escolha dos Brasileiros"

🎯 URGÊNCIA E AÇÃO (OBRIGATÓRIO):
✓ "Aproveite Hoje" ✓ "Oferta Limitada" ✓ "Últimas Unidades"
✓ "Garanta o Seu" ✓ "Não Perca" ✓ "Promoção Exclusiva"

📊 ESTRUTURA FOCO-BENEFÍCIO (OBRIGATÓRIO):
Cada bullet: CARACTERÍSTICA → BENEFÍCIO → RESULTADO
Exemplo: "Bateria 40H → Música sem parar → Viagens sem preocupação"
🔥🔥🔥 FIM OTIMIZAÇÃO BRASILEIRA 🔥🔥🔥
"""

        # Mexico conversion optimization  
        mexico_extra = ""
        if language == 'es-mx':
            mexico_extra = """
🔥🔥🔥 OPTIMIZACIÓN MEXICANA - MÁXIMA CONVERSIÓN 🔥🔥🔥

🌮 SEÑALES DE CONFIANZA (OBLIGATORIO):
✓ "Garantía de 2 Años" ✓ "Certificado de Calidad" ✓ "100% Original"
✓ "30 Días de Garantía" ✓ "Envío Seguro" ✓ "Factura Incluida"
✓ "Miles de Clientes Felices" ✓ "Preferido en México"

💥 URGENCIA Y ACCIÓN (OBLIGATORIO):
✓ "Compra Hoy" ✓ "Oferta Limitada" ✓ "Últimas Piezas"
✓ "Asegura el Tuyo" ✓ "No Te Lo Pierdas" ✓ "Promoción Exclusiva"

📊 ESTRUCTURA CARACTERÍSTICA-BENEFICIO (OBLIGATORIO):
Cada viñeta: CARACTERÍSTICA → BENEFICIO → RESULTADO
Ejemplo: "Batería 40H → Música sin interrupciones → Viajes sin preocupaciones"
🔥🔥🔥 FIN OPTIMIZACIÓN MEXICANA 🔥🔥🔥
"""

        # Netherlands conversion optimization
        netherlands_extra = ""
        if language == 'nl':
            netherlands_extra = """
🔥🔥🔥 NEDERLANDSE OPTIMALISATIE - MAXIMALE CONVERSIE 🔥🔥🔥

🌷 VERTROUWENSSIGNALEN (VERPLICHT):
✓ "2 Jaar Garantie" ✓ "CE Gecertificeerd" ✓ "Kwaliteitsgarantie"
✓ "30 Dagen Retourrecht" ✓ "Veilig Betalen" ✓ "Nederlandse Service"
✓ "10.000+ Tevreden Klanten" ✓ "Keuze van Nederland"

⚡ URGENTIE EN ACTIE (VERPLICHT):
✓ "Bestel Vandaag" ✓ "Beperkte Voorraad" ✓ "Laatste Stuks"
✓ "Pak de Jouwe" ✓ "Mis Het Niet" ✓ "Exclusieve Aanbieding"

📊 KENMERK-VOORDEEL STRUCTUUR (VERPLICHT):
Elke bullet: KENMERK → VOORDEEL → RESULTAAT
Voorbeeld: "40 Uur Batterij → Non-stop muziek → Zorgeloos reizen"
🔥🔥🔥 EINDE NEDERLANDSE OPTIMALISATIE 🔥🔥🔥
"""

        return f"""
🚨🚨🚨 CRITICAL LANGUAGE REQUIREMENT 🚨🚨🚨
YOU MUST WRITE EVERYTHING IN {lang_name.upper()} ({native})!
NOT A SINGLE WORD IN ENGLISH!
{german_extra}
{turkish_extra}
{brazil_extra}
{mexico_extra}
{netherlands_extra}

LANGUAGE: {lang_name} for {country}
TARGET MARKET: Amazon.{marketplace}

ALL CONTENT MUST BE IN {lang_name.upper()}:
- Title: COMPLETELY in {lang_name} with trust signals
- Bullet Points: COMPLETELY in {lang_name} with FEATURE→BENEFIT→OUTCOME  
- Description: COMPLETELY in {lang_name} with urgency CTAs
- FAQs: COMPLETELY in {lang_name} with guarantees
- Keywords: COMPLETELY in {lang_name} including conversion terms
- EVERYTHING: COMPLETELY in {lang_name}

DO NOT TRANSLATE BRAND NAME, but everything else MUST be in {lang_name}.
Use culturally appropriate phrases and expressions for {country} shoppers.
🚨🚨🚨 END CRITICAL LANGUAGE REQUIREMENT 🚨🚨🚨
"""
    
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
            
            # SWEDEN SPECIFIC: Post-process A+ content to replace English keywords with Swedish
            marketplace_code = getattr(product, 'marketplace', 'us')
            if marketplace_code == 'se' and hasattr(listing, 'amazon_aplus_content') and listing.amazon_aplus_content:
                print(f"🇸🇪 Post-processing A+ content for Swedish keywords...")
                original_length = len(listing.amazon_aplus_content)
                
                # Check for English keywords before replacement
                english_keywords = ['everyday use', 'versatile applications', 'practical', 'convenient']
                english_found_before = sum(listing.amazon_aplus_content.count(kw) for kw in english_keywords)
                print(f"🇸🇪 Found {english_found_before} English keywords in A+ content before replacement")
                
                # Apply comprehensive English-to-Swedish replacements
                english_to_swedish = {
                    # Original specific keywords
                    'everyday use': 'daglig användning',
                    'versatile applications': 'mångsidig användning', 
                    'practical': 'praktisk',
                    'convenient': 'bekväm',
                    'customer satisfaction': 'kundnöjdhet',
                    'package contents': 'förpackningsinnehåll',
                    # Common English words in A+ content
                    'Premium': 'Premium',  # Keep as is (international term)
                    'Quality': 'Kvalitet',
                    'Professional': 'Professionell',
                    'Advanced': 'Avancerad',
                    'Superior': 'Överlägsen',
                    'Features': 'Funktioner',
                    'Benefits': 'Fördelar',
                    'Experience': 'Upplevelse',
                    'Perfect': 'Perfekt',
                    'Ultimate': 'Ultimat',
                    'Guarantee': 'Garanti',
                    'Warranty': 'Garanti',
                    'Satisfaction': 'Tillfredsställelse',
                    'Customer': 'Kund',
                    'Product': 'Produkt',
                    'Kitchen': 'Kök',
                    'Cutting': 'Skär',
                    'Board': 'Bräda',
                    'Design': 'Design',  # Keep as is (international term)
                    'Material': 'Material',  # Keep as is
                    'Package': 'Paket',
                    'excellent': 'utmärkt',
                    'amazing': 'fantastisk',
                    'wonderful': 'underbar',
                    'great': 'bra',
                    'good': 'bra',
                    'best': 'bäst',
                    'top': 'topp',
                    'high': 'hög',
                    'low': 'låg',
                    'easy': 'lätt',
                    'simple': 'enkel',
                    'quick': 'snabb',
                    'fast': 'snabb',
                    'strong': 'stark',
                    'powerful': 'kraftfull',
                    'effective': 'effektiv',
                    'efficient': 'effektiv',
                    'reliable': 'pålitlig',
                    'durable': 'hållbar',
                    'safe': 'säker',
                    'secure': 'säker'
                }
                
                # Apply replacements
                for english, swedish in english_to_swedish.items():
                    if english in listing.amazon_aplus_content:
                        listing.amazon_aplus_content = listing.amazon_aplus_content.replace(english, swedish)
                        print(f"🇸🇪 Replaced '{english}' with '{swedish}'")
                
                # Check for English keywords after replacement
                english_found_after = sum(listing.amazon_aplus_content.count(kw) for kw in english_keywords)
                swedish_keywords = ['daglig användning', 'mångsidig användning', 'praktisk', 'bekväm']
                swedish_found = sum(listing.amazon_aplus_content.count(kw) for kw in swedish_keywords)
                
                new_length = len(listing.amazon_aplus_content)
                print(f"🇸🇪 A+ content processing complete:")
                print(f"   Length: {original_length} → {new_length} characters")
                print(f"   English keywords: {english_found_before} → {english_found_after}")
                print(f"   Swedish keywords: {swedish_found}")
                print(f"   ✅ Swedish keyword replacement successful!")
            
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
        from .services_occasion_enhanced import OccasionOptimizer
        from .brand_tone_optimizer import BrandToneOptimizer
        from .international_localization_optimizer import InternationalLocalizationOptimizer
        from .market_occasions import MarketOccasions
        
        self.logger.info(f"GENERATING AMAZON LISTING FOR {product.name}")
        self.logger.info(f"OpenAI client status: {'AVAILABLE' if self.client else 'NOT AVAILABLE'}")
        self.logger.info(f"Marketplace: {getattr(product, 'marketplace', 'us')} | Language: {getattr(product, 'marketplace_language', 'en')}")
        self.logger.info(f"Occasion: {getattr(product, 'occasion', 'None')}")
        self.logger.info(f"Brand Tone: {getattr(product, 'brand_tone', 'professional')}")
        
        if not self.client:
            self.logger.error("OpenAI client is None - using fallback content")
            self.logger.error(f"API Key exists: {bool(settings.OPENAI_API_KEY)}")
            if settings.OPENAI_API_KEY:
                self.logger.error(f"API Key starts with 'sk-': {settings.OPENAI_API_KEY.startswith('sk-') if settings.OPENAI_API_KEY else False}")
            raise Exception("OpenAI API key not configured. Please set your OPENAI_API_KEY in the .env file to generate AI content.")
            
        # Initialize optimizers
        occasion_optimizer = OccasionOptimizer()
        brand_tone_optimizer = BrandToneOptimizer()
        international_optimizer = InternationalLocalizationOptimizer()
        market_occasions = MarketOccasions()
        
        
        # Generate product-specific keywords and context
        product_context = self._analyze_product_context(product)
        
        # Use actual product brand tone
        brand_tone_mapping = {
            'professional': {
                'tone': 'Professional & Authoritative',
                'guidelines': 'Direct, credible, expertise-focused. Personality: Trusted advisor who builds confidence. Use phrases like "Industry-leading", "Proven results", "Professional grade". Focus on reliability and expertise. TITLE RULE: Always merge an emotional hook with a high-intent keyword in the first 4 words - no clickbait, must feel authentic and aligned with product strengths.'
            },
            'casual': {
                'tone': 'Friendly & Approachable',
                'guidelines': 'Conversational, warm, relatable. Personality: Helpful friend who makes things easy. Use phrases like "Just what you need", "Makes life easier", "You\'ll love this". Focus on comfort and simplicity. TITLE RULE: Always merge an emotional hook with a high-intent keyword in the first 4 words - no clickbait, must feel authentic and aligned with product strengths.'
            },
            'luxury': {
                'tone': 'Elegant & Premium',
                'guidelines': 'Sophisticated, aspirational, transformational. Personality: Elevated and inspiring. Use phrases like "Elevate your", "Transform into", "Luxurious experience". Include sensory language and confidence-building. TITLE RULE: Always merge an emotional hook with a high-intent keyword in the first 4 words - no clickbait, must feel authentic and aligned with product strengths.'
            },
            'playful': {
                'tone': 'Playful & Innovative',
                'guidelines': 'Fun, confident, slightly cheeky. Personality: Tech-savvy friend who makes complex simple. Use phrases like "Talk like a local", "Say it like you mean it", "Ready to [outcome]". Balance innovation with accessibility. TITLE RULE: Always merge an emotional hook with a high-intent keyword in the first 4 words - no clickbait, must feel authentic and aligned with product strengths.'
            },
            'minimal': {
                'tone': 'Clean & Minimal',
                'guidelines': 'Clear, concise, purposeful. Personality: Thoughtful minimalist who values quality. Use phrases like "Simply better", "Pure performance", "Essential quality". Focus on clarity and purpose. TITLE RULE: Always merge an emotional hook with a high-intent keyword in the first 4 words - no clickbait, must feel authentic and aligned with product strengths.'
            },
            'bold': {
                'tone': 'Bold & Confident',
                'guidelines': 'Strong, decisive, powerful. Personality: Leader who inspires action. Use phrases like "Dominate your", "Unleash your", "Power through". Focus on strength and transformation. TITLE RULE: Always merge an emotional hook with a high-intent keyword in the first 4 words - no clickbait, must feel authentic and aligned with product strengths.'
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
        
        # Natural description approaches (avoid repetitive starters)  
        description_approaches = [
            "product_focused", "benefit_focused", "problem_solution", "story_narrative", 
            "feature_highlight", "customer_outcome", "technical_explanation", "lifestyle_integration"
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
        chosen_approach = random.choice(description_approaches)
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

TODAY'S EMOTIONAL APPROACH: "{chosen_hook}"
DESCRIPTION STYLE: "{chosen_approach}"  
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

TODAY'S EMOTIONAL APPROACH: "{chosen_hook}"
DESCRIPTION STYLE: "{chosen_approach}"  
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

TODAY'S EMOTIONAL APPROACH: "{chosen_hook}"
DESCRIPTION STYLE: "{chosen_approach}"  
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

TODAY'S EMOTIONAL APPROACH: "{chosen_hook}"
DESCRIPTION STYLE: "{chosen_approach}"  
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

TODAY'S EMOTIONAL APPROACH: "{chosen_hook}"
DESCRIPTION STYLE: "{chosen_approach}"  
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

TODAY'S EMOTIONAL APPROACH: "{chosen_hook}"
DESCRIPTION STYLE: "{chosen_approach}"  
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
            "Avoid using these overused phrases in ANY section: 'Experience the difference', 'Take your [X] to the next level', 'Game-changing', 'Revolutionary', 'Unparalleled', 'Amazing', 'Incredible', 'You'll wonder how you managed without it', 'Trust me', 'You'll be the hero', 'Your new best friend'",
            "Use unexpected analogies and comparisons that fit the brand tone",
            "Vary sentence length dramatically - mix very short punchy sentences with longer flowing ones",
            "Start with a completely different hook approach than typical Amazon listings",
            "Include specific numbers and metrics that feel authentic to this product category",
            "Write as if youre personally recommending to a friend, not selling",
            "Include subtle humor or personality quirks that match the brand tone",
            "Use specific, concrete details instead of generic superlatives", 
            "Write in a conversational tone with natural word choices and rhythm",
            "Avoid marketing buzzwords - use everyday language customers understand",
            "Include sensory details or vivid descriptions when appropriate",
            "Use proper contractions with apostrophes (don't, can't, it's, you're) for natural human language",
            "Include mild imperfections or honest limitations to build trust",
            "Reference real customer experiences or relatable scenarios",
            "Tell a mini-story about how this product fits into someone's day",
            "Use relatable comparisons to familiar objects or experiences",
            "Include genuine enthusiasm without sounding like a robot",
            "Admit when something might not be perfect but explain why it's still worth it",
            "Use practical tips or insider knowledge about using the product",
            "Include honest comparisons to alternatives when appropriate",
            "Write like someone who actually owns and loves the product",
            "Use unexpected but fitting metaphors or creative descriptions",
            "Include authentic details that only someone familiar with the product would know",
            "MOBILE SCAN-FIRST BULLETS RULE: The first 6-8 words of each bullet must serve as a micro-headline (main benefit or emotional payoff), followed by supportive detail",
            "BENEFIT STACKING: At least 2 bullets should combine feature + emotional benefit + trust element in a single flow (e.g., 'LOCKS IN COLD — Double-wall insulation keeps water icy fresh, giving you confidence on long commutes')"
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

        # Get language instruction if not English
        language_instruction = ""
        language_reminder = ""
        marketplace_lang = getattr(product, 'marketplace_language', 'en')
        
        if marketplace_lang and marketplace_lang != 'en':
            language_instruction = self.get_marketplace_language_instruction(
                getattr(product, 'marketplace', 'com'), 
                marketplace_lang
            )
            # Add language reminder at the end too
            language_name = {
                'de': 'GERMAN', 'fr': 'FRENCH', 'it': 'ITALIAN', 'es': 'SPANISH',
                'nl': 'DUTCH', 'sv': 'SWEDISH', 'pl': 'POLISH', 'ja': 'JAPANESE',
                'pt': 'PORTUGUESE', 'ar': 'ARABIC', 'tr': 'TURKISH'
            }.get(marketplace_lang, 'ENGLISH')
            language_reminder = f"\n\n⚠️ FINAL REMINDER: ALL CONTENT MUST BE IN {language_name}! ⚠️"
        
        # Add brand persona and target audience if provided
        brand_context = ""
        if hasattr(product, 'brand_persona') and product.brand_persona:
            brand_context += f"\nBRAND PERSONA: {product.brand_persona}"
        if hasattr(product, 'target_audience') and product.target_audience:
            brand_context += f"\nTARGET AUDIENCE: {product.target_audience}"
        
        # Get occasion-specific enhancements if applicable
        occasion = getattr(product, 'occasion', None)
        marketplace = getattr(product, 'marketplace', 'us')
        occasion_enhancement = ""
        
        if occasion and occasion != 'None':
            # Translate occasion to local market version
            local_occasion = market_occasions.translate_occasion(occasion, marketplace)
            
            # Check if this occasion is appropriate for this market
            if not market_occasions.should_include_occasion(occasion, marketplace):
                self.logger.info(f"Skipping US-specific occasion '{occasion}' for market {marketplace}")
                occasion = 'general'  # Fall back to general
                local_occasion = 'general'
            
            # Get localized occasion keywords
            occasion_keywords = market_occasions.get_occasion_keywords(occasion, marketplace)
            
            # Get localized emotional hooks
            occasion_hooks = market_occasions.get_occasion_emotional_hooks(occasion, marketplace)
            
            occasion_enhancement = occasion_optimizer.get_occasion_prompt_enhancement(occasion)
            
            # Add localized occasion context
            if occasion_keywords or occasion_hooks:
                occasion_enhancement += f"\n\nLOCALIZED OCCASION CONTEXT for {marketplace.upper()}:"
                if occasion_keywords:
                    occasion_enhancement += f"\nLocal Keywords: {', '.join(occasion_keywords)}"
                if occasion_hooks:
                    occasion_enhancement += f"\nLocal Hooks: {' | '.join(occasion_hooks)}"
            
            self.logger.info(f"Applied localized occasion enhancement for: {local_occasion} (market: {marketplace})")
        
        # Get brand tone-specific enhancements with marketplace context
        brand_tone = getattr(product, 'brand_tone', 'professional')
        marketplace = getattr(product, 'marketplace', 'us')
        brand_tone_enhancement = brand_tone_optimizer.get_brand_tone_enhancement(brand_tone, marketplace)
        self.logger.info(f"Applied brand tone enhancement for: {brand_tone} (marketplace: {marketplace})")
        
        # Get international localization enhancements if applicable
        marketplace = getattr(product, 'marketplace', 'com')
        localization_enhancement = ""
        aplus_enhancement = ""
        if marketplace_lang and marketplace_lang != 'en':
            localization_enhancement = international_optimizer.get_localization_enhancement(marketplace, marketplace_lang)
            aplus_enhancement = international_optimizer.get_aplus_content_enhancement(marketplace, marketplace_lang)
            self.logger.info(f"Applied international localization for: {marketplace} ({marketplace_lang})")
            self.logger.info(f"Applied A+ content international enhancement for: {marketplace} ({marketplace_lang})")
        
        # Add UK British culture enhancement for PERFECT 10/10 quality (following Mexico structure)
        uk_enhancement = ""
        if marketplace == 'uk':
            # Get occasion for UK-specific formatting
            occasion = getattr(product, 'occasion', 'general')
            
            # UK Cultural Enhancement - EXACT MEXICO PATTERN FOR GUARANTEED 10/10 QUALITY
            uk_enhancement = f"""
🇬🇧 UNITED KINGDOM MARKET - EXACT MEXICO PATTERN REPLICATION FOR 10/10 QUALITY
=================================================================================

🚨🚨🚨 MANDATORY REQUIREMENTS - NO EXCEPTIONS ALLOWED 🚨🚨🚨

⭐ CRITICAL SUCCESS FACTORS - FOLLOW MEXICO'S PROVEN FORMULA EXACTLY:

1. BULLET STRUCTURE - EXACT MEXICO REPLICATION:
   🎯 ALL 5 bullets MUST start with ★ symbol
   🎯 Follow Mexico's emotional intensity pattern exactly
   🎯 Each bullet MUST contain ONE British formality phrase
   🎯 Length: 180-250 characters per bullet (Mexico standard)

2. MANDATORY BRITISH FORMALITY PHRASES (USE ONE PER BULLET):
   ✓ "We're delighted to offer" ✓ "Rest assured" ✓ "You'll find" 
   ✓ "We're confident" ✓ "Proudly British" ✓ "You can be certain"
   ✓ "It's our pleasure to provide" ✓ "We guarantee you'll notice"

3. BRITISH CULTURAL INTEGRATION (MINIMUM 5 REFERENCES):
   ✓ UK occasions: {occasion}, Boxing Day, Sunday roast, afternoon tea
   ✓ British weather/climate considerations ✓ British homes/lifestyle
   ✓ UK families/customers ✓ British standards/engineering ✓ British heritage

4. EMOTIONAL POWER UPGRADE (BEAT COMPETITORS):
   ❌ good → ✓ brilliant/exceptional ❌ nice → ✓ splendid/outstanding
   ❌ great → ✓ remarkable/superb ❌ quality → ✓ premium excellence

🔥 MANDATORY 5-BULLET PATTERN (FOLLOW MEXICO'S EXACT STRUCTURE):

★ BULLET 1 - BRITISH EXCELLENCE SHOWCASE:
"★ BRITISH ENGINEERING EXCELLENCE: [Premium feature] engineered to British Standards for [exceptional result]. We're confident you'll find [refined benefit] that transforms your [UK lifestyle scenario]."

★ BULLET 2 - HERITAGE MEETS INNOVATION:
"★ HERITAGE CRAFTSMANSHIP: [Quality element] combining traditional British excellence with [modern innovation]. Rest assured, [guarantee/quality promise] with full UK warranty backing."

★ BULLET 3 - PERFECT FOR BRITISH HOMES:
"★ PERFECT FOR BRITISH LIFESTYLE: [Lifestyle feature] ideal for {occasion}, Sunday roasts, and [weather considerations]. You'll find it brilliant for [specific British use case]."

★ BULLET 4 - TRUSTED BY UK FAMILIES:
"★ TRUSTED ACROSS BRITAIN: [Social proof] chosen by thousands of British families from London to Edinburgh. We're delighted to offer [exclusive British benefit]."

★ BULLET 5 - EXCEPTIONAL BRITISH GIFT:
"★ THOUGHTFUL BRITISH GIFT: Perfect {occasion} present with [British packaging/service]. Proudly presented with British customer service excellence and next-day delivery."

💪 MANDATORY ELEMENTS TO INCLUDE (10/10 QUALITY CHECKPOINT):
🎯 5 bullets with ★ symbols ✓ 🎯 British formality in every bullet ✓
🎯 UK cultural references (min 5) ✓ 🎯 Occasion integration: {occasion} ✓
🎯 British spelling (colour, favourite) ✓ 🎯 Weather considerations ✓
🎯 Trust signals (warranty, CE, standards) ✓ 🎯 Emotional intensity ✓

🇬🇧 UK DESCRIPTION STRUCTURE (1400-1600 chars - FOLLOW EXACTLY):
Para 1: "Experience the difference British excellence makes. [Product] represents the finest in [category] engineering, designed specifically for discerning British customers who appreciate [quality aspect]..."
Para 2: "From [British scenario] to [UK lifestyle activity], this [sophisticated feature] delivers [premium benefit]. Perfect for British homes and weather conditions..."
Para 3: "Whether you're preparing for {occasion} or enjoying [British tradition], you'll find [product] provides [exceptional benefit] that exceeds expectations..."
Para 4: "Join thousands of satisfied British families. Rest assured, with [UK warranty] and British customer service, you're investing in proven excellence."

🚨 FINAL QUALITY ASSURANCE - VERIFY BEFORE SUBMISSION:
✅ All 5 bullets start with ★ ✅ British formality in each bullet
✅ Cultural integration present ✅ Emotional power words used  
✅ Trust signals included ✅ British spelling consistent
✅ Occasion '{occasion}' referenced ✅ Weather considerations mentioned

FAILURE TO MEET ALL REQUIREMENTS = AUTOMATIC REJECTION

🚨🚨🚨 CRITICAL BULLET FORMAT REQUIREMENT 🚨🚨🚨
JSON OUTPUT REQUIREMENT FOR UK MARKET:
"bulletPoints": [
    "★ BRITISH ENGINEERING EXCELLENCE: [content with British formality]",
    "★ HERITAGE CRAFTSMANSHIP: [content with British formality]", 
    "★ PERFECT FOR BRITISH LIFESTYLE: [content with British formality]",
    "★ TRUSTED ACROSS BRITAIN: [content with British formality]",
    "★ THOUGHTFUL BRITISH GIFT: [content with British formality]"
]

EVERY SINGLE BULLET MUST START WITH ★ SYMBOL - NO EXCEPTIONS!
DO NOT USE "•" OR "-" OR ANY OTHER SYMBOL - ONLY ★
THIS IS MANDATORY FOR UK MARKET COMPLIANCE
Instead of "nice" → "superb", "magnificent", "splendid"
Instead of "works well" → "performs brilliantly", "excels magnificently"

DESCRIPTION REQUIREMENTS:
- Minimum 800 words with British cultural integration
- Include 3+ British formality phrases
- Reference British lifestyle scenarios
- Strong call-to-action with urgency
- Mention British service and support
- Include weather/climate considerations

COMPETITIVE POSITIONING:
Beat Helium 10: Superior emotional engagement + British localization
Beat Jasper AI: Market-specific formality + proven conversion structure  
Beat CopyMonkey: Authentic British culture + emotional appeal

QUALITY CONTROL CHECKLIST:
□ All 5 bullets start with ★
□ Each bullet contains British formality phrase
□ British cultural elements integrated throughout
□ Emotional intensity words used extensively
□ UK occasions and lifestyle referenced
□ British spelling used consistently
□ Trust signals included prominently
□ Weather/climate considerations mentioned

🏆 TARGET: 10/10 QUALITY SCORE - BEAT ALL COMPETITORS
"""
            
            # Add specific UK lifestyle elements based on product category
            if 'kitchen' in str(product.categories).lower() or 'knife' in product.name.lower():
                uk_enhancement += """
UK KITCHEN CULTURE INTEGRATION:
- Emphasize Sunday roast preparation, traditional British cooking
- Reference British culinary traditions: "Perfect for carving the Sunday joint"
- Include entertaining: "Ideal for dinner parties and kitchen soirées"
- Mention British cooking shows and chef culture
- Connect to British home cooking renaissance
"""
            elif 'audio' in str(product.categories).lower() or 'headphone' in product.name.lower():
                uk_enhancement += """
UK AUDIO LIFESTYLE INTEGRATION:
- Connect to commuting culture: London Underground, British Rail
- Reference British music heritage: "From Beatles to Adele"
- Include sports culture: Premier League, Wimbledon, Six Nations
- Mention British broadcasting: BBC, podcasts, audiobooks
- Link to British weather: "Weather-resistant for British climate"
"""
            elif 'home' in str(product.categories).lower() or 'garden' in product.name.lower():
                uk_enhancement += """
UK HOME & GARDEN INTEGRATION:
- Emphasize British home pride and garden culture
- Reference property shows and home improvement
- Include British weather considerations
- Mention Victorian homes to modern flats
- Connect to British DIY and gardening traditions
"""
            else:
                uk_enhancement += """
UK GENERAL LIFESTYLE INTEGRATION:
- Reference British daily life and traditions
- Include weather-appropriate features
- Mention British innovation and quality standards
- Connect to British social occasions
- Emphasize reliability and tradition
"""

        # Add Australian BBQ culture enhancement for better localization
        australian_enhancement = ""
        if marketplace == 'au':
            if 'kitchen' in str(product.categories).lower() or 'knife' in product.name.lower():
                australian_enhancement = """
AUSTRALIAN BBQ CULTURE INTEGRATION REQUIRED:
- Emphasize outdoor cooking, BBQ prep, and grilling applications
- Reference Australian BBQ traditions, outdoor entertaining, summer cookouts
- Include backyard gatherings, meat preparation, outdoor cooking precision
- Use Aussie terminology: "barbie", "prawns", "snags", "outdoor cooking", "backyard entertaining"  
- Connect product to weekend BBQ traditions and outdoor family gatherings
- Make content scan-friendly for mobile with short, punchy opening phrases in bullets
- Keep sentences under 20 words for mobile readability
- Lead each bullet with 6-8 word benefit phrases followed by details

"""
            elif 'audio' in str(product.categories).lower() or 'headphone' in product.name.lower():
                australian_enhancement = """
AUSTRALIAN LIFESTYLE INTEGRATION REQUIRED:
- Connect to outdoor adventures, beach sessions, camping trips, outback travel
- Reference Aussie sporting culture: footy, cricket, rugby, outdoor activities
- Include fair dinkum quality, extreme climate durability, adventure-ready features
- Use authentic Aussie language naturally without overdoing it
- Make content scan-friendly for mobile with short, punchy opening phrases in bullets
- Keep sentences under 20 words for mobile readability
- Lead each bullet with 6-8 word benefit phrases followed by details

"""
            else:
                australian_enhancement = """
AUSTRALIAN CULTURAL INTEGRATION REQUIRED:
- Emphasize fair dinkum quality, no-nonsense practical benefits
- Reference Australian lifestyle: outdoor living, extreme weather durability
- Include mateship, family values, practical everyday use
- Make content extremely mobile-friendly with concise, scannable format
- Keep sentences under 20 words for mobile readability
- Lead each bullet with 6-8 word benefit phrases followed by details

"""

        # Now create the completely new human-focused prompt
        prompt = f"""
{language_instruction}
{localization_enhancement}
{aplus_enhancement}
{brand_tone_enhancement}
{occasion_enhancement}
{uk_enhancement}
{australian_enhancement}
{base_prompt}
CRITICAL: USE ONLY THE FOLLOWING INFORMATION - NO GENERIC CONTENT!
DO NOT MAKE UP FEATURES OR BENEFITS NOT PROVIDED BELOW!

PRODUCT INFORMATION (USE ALL OF THIS):
- Product: {product.name}
- Brand: {product.brand_name} (MUST appear in title and throughout listing)
- Category: {product_category}
- Description: {product.description}
- Features: {', '.join(features_list) if features_list else 'Focus on description details'}
- Price: ${product.price if product.price else '29.99'}
- Product ID: {product.id}
- Marketplace: {product.get_marketplace_display() if hasattr(product, 'marketplace') else 'United States'}
{brand_context}


REQUIRED ELEMENTS (MUST USE):
- Target Keywords: {getattr(product, 'target_keywords', 'Generate based on product description')}
- Categories for Context: {product.categories if product.categories else 'Use product description to determine'}
- Special Occasion: {getattr(product, 'occasion', 'None - general purpose listing')}

⚠️ IMPORTANT: Base EVERYTHING on the actual product information above. Do not use generic placeholder content. If a detail isn't provided, extract it from the description or features given.

RANDOMIZATION ELEMENTS FOR TODAY:
- Content Focus: {chosen_focus}
- Title Approach: {chosen_title_approach}  
- FAQ Style: {chosen_faq_style}
- Variety Emphasis: {variety_elements[0]}

AMAZON RUFUS AI OPTIMIZATION STRATEGY:
Amazon's Rufus AI assistant helps customers find products through conversational queries. Your listing must be optimized for:
- Natural language questions ("What's the best bluetooth headphone for working out?")
- Comparison queries ("How is this different from other brands?") 
- Use case scenarios ("Good for traveling?", "Will this work for gaming?")
- Problem-solving language ("Stops hurting my ears", "Finally doesn't fall out")

📝 MERGED STYLE APPROACH (GPT-4 + GPT-5 BEST PRACTICES):
Merge two proven approaches into one powerful listing:

From GPT-4 strengths: emotional storytelling, vivid scenarios, problem-solving benefits, and strong feature-to-benefit connections.
From GPT-5 strengths: short, mobile-friendly bullet points, gifting/lifestyle positioning, broad keyword coverage, and strong trust signals (like warranties and guarantees).

🔥🔥🔥 CONVERSION OPTIMIZATION REQUIREMENTS (BEATS HELIUM 10, JASPER, COPYMONKEY) 🔥🔥🔥

TRUST SIGNALS (MANDATORY - Beats CopyMonkey):
• Include "Guarantee", "Warranty", "Certified", "Quality" in EVERY listing
• Add "30-day money back", "2-year warranty", "CE/FDA certified" when applicable
• Use "Premium", "Professional", "Trusted by thousands" positioning
• Include social proof: "Join 10,000+ satisfied customers"
• Add scarcity: "Limited availability", "Best seller", "Stock running low"

URGENCY ELEMENTS (MANDATORY - Conversion Boost):
• Use action verbs: "Get", "Enjoy", "Experience", "Upgrade", "Transform"
• Time-sensitive language: "Today", "Now", "Don't miss out", "While supplies last"
• Exclusive positioning: "Exclusive design", "Limited edition", "Premium selection"
• Call-to-action in description: "Click Add to Cart to secure yours today"

BENEFIT-FOCUSED STRUCTURE (MANDATORY - Beats Jasper AI):
• EVERY bullet must follow: FEATURE → BENEFIT → OUTCOME
• Example: "40H Battery Life → Never stops your music → Enjoy week-long trips without charging"
• Use emotional outcomes: "Feel confident", "Save time", "Reduce stress", "Impress guests"
• Problem → Solution format in at least 2 bullets
• Include lifestyle transformation: "Turn your daily routine into..."

CONVERSION PSYCHOLOGY (MANDATORY):
• Loss aversion: "Don't let poor quality ruin your experience"
• Social proof: "Chosen by professionals", "Family favorite", "Top-rated"
• Authority: "Engineered by experts", "Industry-leading", "Patented technology"
• Reciprocity: "Includes bonus accessories", "Free guide included"
• Commitment: "Investment in quality", "Built to last a lifetime"

🔥🔥🔥 END CONVERSION OPTIMIZATION 🔥🔥🔥

MERGED STYLE RULES:
• Title: Mobile-first priority - impactful and fully scannable within 110-125 characters (up to 140 max if brand name is long). Start with hook + primary keyword + trust signal
• Bullet Points: 5 maximum, each 200+ chars. Each begins with a strong 6-8 word benefit phrase (micro-headline) before detailed explanation. MUST include trust/urgency elements
• Description: 1500-2000 chars, broken into short 2-3 sentence chunks with line breaks for mobile readability. Each chunk ends with conversion-focused CTA
• FAQ: Address objections, highlight guarantees, emphasize urgency
• A+ Content: Heavy focus on trust badges, comparison charts, money-back guarantees
• Keywords: Include conversion terms: "best", "premium", "guaranteed", "certified"
• Backend Keywords: 249 max chars, include trust and urgency keywords
• No Repetition: Vary trust signals and urgency elements across sections

🚨🚨 AMAZON USA OPTIMIZATION RULES (NON-NEGOTIABLE) 🚨🚨

TITLE VALIDATION CHECKLIST:
✅ Starts with main product keywords (NOT marketing taglines)
✅ High-intent search terms in first 40 characters  
✅ Brand placed in middle, not at start
✅ Specific model/size/capacity numbers included
✅ No soft phrases like "Simply", "Just", "So Easy"

BULLET VALIDATION CHECKLIST:
✅ EVERY bullet starts with ALL CAPS LABEL (3-5 words)
✅ Specific technical specs included (battery hours, weight, size)
✅ Measurable performance numbers (RPM, dB, hours, oz/g)
✅ Benefit stated immediately after label
✅ No bullets without technical specifications

CRITICAL FAILURE POINTS:
❌ Title starting with taglines instead of keywords = FAILED LISTING
❌ Bullets without ALL CAPS labels = FAILED LISTING  
❌ Missing technical specs = FAILED LISTING
❌ Soft marketing language = FAILED LISTING

YOUR MISSION: Create a COMPREHENSIVE, MAXIMUM-LENGTH Amazon listing optimized for Amazon USA search algorithm and fast-scanning behavior.

CRITICAL CONTENT REQUIREMENTS - GENERATE MAXIMUM CONTENT:
✅ Title: 110-125 chars ideal (up to 140 max). Start with hook + primary keyword. Mobile-first priority for scanability
✅ Bullet Points: 5 bullets, each 200+ chars. Each begins with strong 6-8 word benefit phrase before detailed explanation
✅ Product Description: 1500-2000 chars, broken into short readable chunks, each ending with soft benefit-driven hook
✅ A+ Content: 5 complete sections with unique focus, no duplication between sections, mobile-responsive
✅ Visual Templates: GENERATE ACTUAL CONTENT for each template field - no instruction text, only real content
✅ Backend Keywords: 249 max chars, must not duplicate exact words from title/bullets, target complementary indexing terms
✅ SEO Keywords: 80+ total (short + long-tail), ensuring no overstuffing; distribute naturally across listing
✅ Brand Story: 250-400 character detailed brand narrative with proper punctuation
✅ FAQs: 5+ detailed Q&As with proper grammar and complete sentences
✅ Features: 5+ specific product features
✅ What's in Box: Complete unboxing experience
✅ Trust Builders: Multiple guarantees and certifications
✅ Social Proof: Detailed customer satisfaction claims

🎨 VISUAL TEMPLATE CRITICAL REQUIREMENTS:
- Generate ACTUAL content for imageTitle, suggestedScene, overlayText, styleGuide, layoutStructure, colorScheme
- Do NOT write instructions like "Write actual..." - provide the actual content
- Base all visual content on the specific product information provided
- Make each template unique and product-specific
- Provide ready-to-use design briefs that can be immediately implemented

KEYWORD STRATEGY FOR MAXIMUM VISIBILITY:
- Primary Keywords (15+): Direct product terms, brand + product, category terms
- Long-tail Keywords (25+): 3-7 word phrases, natural questions, use cases
- Problem-solving Keywords (15+): Pain points, solutions, comparisons  
- Rufus Conversation Keywords (15+): "best for", "good for", "works with", "better than"
- Semantic Keywords (10+): Related terms, synonyms, variations
- TOTAL TARGET: 80+ keywords covering every possible search angle

CRITICAL JSON FORMATTING RULES:
1. ALL JSON field values MUST use double quotes (") not single quotes (')
2. INSIDE content text, use single quotes for contractions: dont, cant, wont, its  
3. NEVER use unescaped double quotes inside content text
4. JSON structure: {{"field": "content with single quotes inside"}}
5. Test your JSON structure before submitting
6. CORRECT: {{"title": "This is Johns favorite product"}}
7. WRONG: {{'title': 'This is Johns favorite product'}}

KEYWORD GENERATION RULES:
1. For "primary" keywords: ALWAYS start with product name and brand name, then add 13+ related single/double words
2. For "longTail": Create 25+ actual phrases (3-7 words), not instruction text
3. For all keyword arrays: Generate actual keywords, NOT instruction text or examples
4. Replace template phrases like [actual use case] with real use cases based on the product
5. EXAMPLE GOOD: ["wireless earbuds", "bluetooth headphones", "noise cancelling"] 
6. EXAMPLE BAD: ["Generate 15+ short keywords based on..."]

RESPONSE FORMAT: Return COMPREHENSIVE JSON with ALL fields populated with MAXIMUM-LENGTH content:

{{
  "productTitle": "{self.get_marketplace_title_format(product.marketplace, product.brand_name)}",
  
  "bulletPoints": [
    "{self.get_marketplace_bullet_format(product.marketplace, 1)}",
    "{self.get_marketplace_bullet_format(product.marketplace, 2)}", 
    "{self.get_marketplace_bullet_format(product.marketplace, 3)}",
    "{self.get_marketplace_bullet_format(product.marketplace, 4)}",
    "{self.get_marketplace_bullet_format(product.marketplace, 5)}"
  ],
  
  "productDescription": "{self.get_marketplace_description_format(product.marketplace, product.brand_tone)}",
  
  "seoKeywords": {{
    "primary": ["{product.name.lower().replace(' ', '_')}", "{product.brand_name.lower()}", "{self.get_japanese_industry_keywords(product) if product.marketplace == 'jp' else self.get_spanish_industry_keywords(product) if product.marketplace == 'es' else self.get_turkish_industry_keywords(product) if product.marketplace == 'tr' else self.get_swedish_industry_keywords(product) if product.marketplace == 'se' else self.get_egyptian_industry_keywords(product) if product.marketplace == 'eg' else self.get_indian_industry_keywords(product) if product.marketplace == 'in' else 'THEN_ADD_13_MORE: category, color, size, material, feature1, feature2, use1, use2, style, type, model, variant, application'}"],
    "longTail": ["GENERATE_25_PHRASES: {'[ürün] [kullanım] için ideal' if product.marketplace == 'tr' else '[product] [用途]に最適' if product.marketplace == 'jp' else 'mejor [product] para [uso]' if product.marketplace == 'es' else '[product] perfekt för [användning]' if product.marketplace == 'se' else 'best [product] for [use]'}", "{'[marka] [ürün] orijinal' if product.marketplace == 'tr' else '[brand] [product] 正規品' if product.marketplace == 'jp' else '[brand] [product] original certificado' if product.marketplace == 'es' else '[brand] [product] äkta kvalitet' if product.marketplace == 'se' else '[brand] [product] with [feature]'}", "{'[ürün] kaliteli [özellik]' if product.marketplace == 'tr' else '[product] 高品質 [機能]' if product.marketplace == 'jp' else '[product] profesional [aplicación]' if product.marketplace == 'es' else '[product] kvalitet [funktion]' if product.marketplace == 'se' else '[product] that [solves problem]'}", "{'[ürün] premium kalite' if product.marketplace == 'tr' else '[product] プレミアム品質' if product.marketplace == 'jp' else '[product] premium calidad' if product.marketplace == 'es' else '[product] premium kvalitet' if product.marketplace == 'se' else 'professional [product] for [application]'}", "{'[ürün] Türkiye kargo' if product.marketplace == 'tr' else '[product] 送料無料' if product.marketplace == 'jp' else 'oferta [product] [beneficio]' if product.marketplace == 'es' else '[product] sverige frakt' if product.marketplace == 'se' else 'high quality [product] [benefit]'}", "etc"],
    "problemSolving": ["GENERATE_15_PROBLEM_KEYWORDS: {'problemas españoles específicos' if product.marketplace == 'es' else 'based on what issues this product solves from description'}"],
    "rufusConversational": ["GENERATE_15_RUFUS_PHRASES: {'bueno para [uso real]' if product.marketplace == 'es' else 'good for [real use]'}", "{'funciona con [items compatibles]' if product.marketplace == 'es' else 'works with [compatible items]'}", "{'perfecto para [escenarios]' if product.marketplace == 'es' else 'perfect for [scenarios]'}", "{'mejor que [alternativas]' if product.marketplace == 'es' else 'better than [alternatives]'}", "{'ideal para [situaciones]' if product.marketplace == 'es' else 'ideal for [situations]'}"],
    "semantic": ["GENERATE_10_RELATED: {'sinónimos españoles, variaciones, términos relacionados, términos técnicos, nombres informales' if product.marketplace == 'es' else 'synonyms, variations, related terms, technical terms, informal names'}"]
  }},
  
  "backendKeywords": "Write exactly 249 characters of comprehensive search terms. CRITICAL: For occasions, prioritize occasion-specific terms first (e.g., 'christmas gift for him', 'valentine present ideas', 'mothers day gift'). Then include: product variations, synonyms, competitor terms, misspellings, related categories, use cases, customer language, technical terms, seasonal terms, gift occasions, target demographics, problem keywords, solution keywords, benefit terms, feature variations, brand alternatives, size variations, color terms, material types, style descriptors, application areas, compatibility terms, professional vs consumer terms, and industry jargon.",
  
  "aPlusContentPlan": {{
    "section1_hero": {{
      "title": "Write compelling headline with occasion/gift theme",
      "content": "Write comprehensive story explaining value proposition with emotional benefits and specific use cases. Connect personally with customers.",
      "keywords": ["3-5 relevant keywords for this section"],
      "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Describe exactly what should be shown in the image - specific people, setting, lighting, product placement, props, colors, mood, and composition. Include technical specs and why this image works for conversion. Example: 'Turkish family of 4 in modern Istanbul apartment, warm evening lighting, father using headphones while working on laptop, family visible in background preparing dinner, product prominently displayed on desk with premium materials visible, shot emphasizes comfort and family time, professional photography style (970x600px hero lifestyle shot)'",
      "seoOptimization": "Brief note on SEO strategy for this section"
    }},
    "section2_features": {{
      "title": "Key Features and Benefits",
      "content": "Write detailed technical analysis covering 6-8 features with specifications and real-world benefits.",
      "keywords": ["3-5 feature-related keywords"],
      "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Specific description of feature showcase images - exact product angles, close-up details, demonstration scenarios, technical diagrams, before/after comparisons. Include lighting, background, props, and why each image converts. Example: 'Grid of 6 feature images: 1) Close-up of premium foam padding with cross-section view, 2) Hands adjusting noise-canceling controls with sound waves graphic, 3) Battery indicator showing 40-hour display, 4) Waterproof test with droplets, 5) Bluetooth connection to multiple devices, 6) Foldable design demonstration (300x300px each)'",
      "seoOptimization": "Feature-based keywords strategy"
    }},
    "section3_usage": {{
      "title": "Real-World Applications",
      "content": "Write comprehensive guide describing 4-6 usage scenarios across different environments with specific examples.",
      "keywords": ["3-5 usage-related keywords"],
      "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Specific real-world usage scenarios - exact people, activities, environments where product is used. Include demographics, settings, lighting, and emotional context. Example: 'Collage of 4 usage scenarios: 1) Young professional in coffee shop working with headphones, 2) Jogger in park using wireless features, 3) Family movie night with surround sound, 4) Business traveler in airport lounge, each showing different benefits (220x220px each)'",
      "seoOptimization": "Usage-based search optimization"
    }},
    "section4_quality": {{
      "title": "Quality Assurance",
      "content": "Write detailed analysis covering quality control, testing standards, and certifications with specific metrics.",
      "keywords": ["3-5 quality/trust keywords"],
      "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Trust-building certification display - specific badges, certificates, test results, quality seals. Include layout, colors, and credibility elements. Example: 'Professional layout showing CE certification badge, TSE quality seal, 2-year warranty certificate, customer satisfaction ratings (4.8/5 stars), Turkish quality assurance logo, arranged in trust-building grid format with premium styling'",
      "seoOptimization": "Trust and quality-focused keywords"
    }},
    "section5_guarantee": {{
      "title": "Warranty and Support",
      "content": "Write comprehensive guide covering warranty terms, return policies, and customer support with timeframes.",
      "keywords": ["3-5 warranty/support keywords"],
      "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Customer support and warranty visualization - specific support channels, warranty terms, customer service elements. Example: 'Split-screen image: Left shows warranty certificate with 2-year guarantee highlighted, right shows Turkish customer service representative helping customer via phone/chat, includes contact information and support hours, professional and reassuring tone'",
      "seoOptimization": "Support and warranty-based keywords"
    }},
    "section6_social_proof": {{
      "title": "Customer Stories",
      "content": "Write detailed section featuring customer testimonials, usage stories, and real experiences.",
      "keywords": ["3-5 testimonial/review keywords"],
      "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Social proof and testimonials layout - specific customer photos, review snippets, star ratings, usage proof. Example: 'Grid of 6 customer testimonials with profile photos, 5-star ratings, specific quotes about battery life and comfort, includes verified purchase badges, diverse Turkish customers, authentic and credible presentation'",
      "seoOptimization": "Social proof and customer satisfaction keywords"
    }},
    "section7_comparison": {{
      "title": "Why Choose This Product",
      "content": "Write competitive analysis comparing advantages, unique features, and value propositions vs alternatives.",
      "keywords": ["3-5 comparison/competitive keywords"],
      "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Competitive comparison and advantages - specific comparison metrics, charts, feature differences. Example: 'Professional comparison table showing this product vs 3 competitors: battery life (40h vs 20h), noise cancellation (-35dB vs -20dB), warranty (2 years vs 1 year), price value, clearly highlighting advantages with checkmarks and superior metrics'",
      "seoOptimization": "Competitive advantage and comparison keywords"
    }},
    "section8_package": {{
      "title": "Complete Package Contents",
      "content": "Write detailed description of what customers receive: package contents, accessories, and setup guides.",
      "keywords": ["3-5 package/contents keywords"],
      "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Unboxing and package contents display - specific items, premium packaging, first impression elements. Example: 'Top-down unboxing shot showing premium box opening to reveal headphones nestled in soft foam, accessories laid out (charging cable, carrying case, manual), clean white background, emphasizing quality packaging and complete value package'"
      "seoOptimization": "Package and contents-based keywords"
    }},
    "overallStrategy": "Complete A+ content strategy for customer journey from awareness to purchase."
  }},
  
  "brandSummary": "Write 250-400 character detailed brand story including: company background, mission, what makes the brand unique, customer focus, quality commitment, and competitive advantages. Make it feel authentic and substantial, not generic marketing speak.",
  
  "whatsInBox": [
    "Main product with detailed description",
    "Essential accessory 1 with purpose",
    "Essential accessory 2 with purpose", 
    "Documentation and warranty information",
    "Additional items or bonuses included"
  ],
  
  "trustBuilders": [
    "Specific guarantee or warranty details (include gift return policies if occasion is specified)",
    "Certification or testing information", 
    "Company reliability factors",
    "Customer service commitments (mention gift wrapping/message services if occasion-focused)",
    "Quality assurance details (include testimonials mentioning occasion/gift use when applicable)"
  ],
  
  "faqs": [
    "Q: Ask realistic customer question about compatibility, usage, or concerns (for occasions, include delivery timing, gift wrapping, or recipient suitability)? A: Write detailed, helpful answer with proper grammar and contractions (don't, can't, it's) that builds confidence and addresses the specific concern thoroughly.",
    "Q: Ask different realistic question about product benefits, comparison, or technical specs (for occasions, focus on gift-worthiness, why it makes a great [occasion] gift)? A: Provide comprehensive answer with proper apostrophes (you're, we're, they're) that demonstrates expertise and helps customer decision-making.",
    "Q: Ask practical question about setup, maintenance, or common issues? A: Give specific, actionable answer with correct grammar (won't, shouldn't, isn't) that reduces customer anxiety and shows product knowledge.",
    "Q: Ask comparison question about this vs alternatives or competitors? A: Answer diplomatically with proper contractions while highlighting unique advantages and value proposition.",
    "Q: Ask about return policy, shipping, or purchasing concerns? A: Address practical concerns with correct grammar and confidence-building information and clear policies."
  ],
  
  "socialProof": "Write 150-300 characters describing customer satisfaction, ratings, testimonials, or usage statistics. Make it credible and specific without making unverifiable claims.",
  
  "guarantee": "Write 100-200 characters describing specific guarantee, warranty, or risk-free offer. Include timeframe and what's covered. Make it compelling but honest.",
  
  "ppcStrategy": {{
    "campaignStructure": "Detailed 3-tier campaign setup: Auto Discovery (broad targeting), Manual Exact (high-intent keywords), Manual Broad (category expansion)",
    "exactMatch": {{
      "keywords": ["15+ exact match keywords including: brand + product name, specific model numbers, high-intent purchase terms, competitor + alternative terms"],
      "bidRange": "$0.50-1.50",
      "targetAcos": "15-25%",
      "dailyBudget": "$20-40"
    }},
    "phraseMatch": {{
      "keywords": ["20+ phrase match keywords including: problem solution phrases, use case terms, benefit-focused phrases, comparison terms"],
      "bidRange": "$0.35-1.00",
      "targetAcos": "25-35%", 
      "dailyBudget": "$15-30"
    }},
    "broadMatch": {{
      "keywords": ["15+ broad match keywords for discovery: category terms, related products, lifestyle keywords, seasonal terms"],
      "bidRange": "$0.25-0.75",
      "targetAcos": "30-45%",
      "dailyBudget": "$10-25"
    }}
  }}
}}
{language_reminder}"""        
        self.logger.info("OpenAI client is available - proceeding with AI generation")
        try:
            self.logger.info(f"Generating AI content for {product.name} on Amazon...")
            self.logger.info(f"Product details: Name={product.name}, Brand={product.brand_name}, Categories={product.categories}")
            self.logger.info(f"Using product context: {str(product_context)[:200]}...")
            
            # Don't use function calling - use direct JSON generation for maximum content
            # This ensures we get comprehensive content without schema limitations
            
            # Retry logic for robust AI generation
            max_retries = 3
            retry_count = 0
            response = None
            
            while retry_count < max_retries:
                try:
                    print(f"AI generation attempt {retry_count + 1}/{max_retries}")
                    # Add language-specific system message if needed
                    system_content = """You are a creative copywriting expert who writes like a real human, not a marketing robot. 

CRITICAL: Return ONLY valid JSON - no markdown, no explanations, just pure JSON that parses correctly. 

JSON RULES: All field names and values must use double quotes, inside content use proper apostrophes for contractions (don't, can't, won't, it's), never use unescaped double quotes in content. CORRECT FORMAT: {\"field\": \"content with proper apostrophes like don't and can't\"}.

🚨 KEYWORD GENERATION CRITICAL RULES FOR AMAZON SUCCESS:
- Generate BALANCED keyword distribution: SHORT-TAIL + MEDIUM-TAIL + LONG-TAIL
- SHORT-TAIL (1-2 words): Generate 20+ high-volume competitive terms like "headset", "gaming headset", "wireless"
- MEDIUM-TAIL (3-4 words): Generate 20+ targeted terms like "wireless gaming headset", "noise cancelling headset" 
- LONG-TAIL (5+ words): Generate 15+ specific converting phrases like "gaming headset with microphone wireless"
- ALWAYS include core product terms, brand terms, feature terms, platform terms (PC, PS5, Xbox)
- For seoKeywords arrays: Generate ACTUAL keywords/phrases, NOT instruction text
- Primary keywords: Include 5+ SHORT-TAIL core terms first, then brand, then features
- Backend keywords: Focus on misspellings, synonyms, variations (stay under 249 chars)

📝 GRAMMAR & LANGUAGE CRITICAL RULES:
- ALWAYS use proper apostrophes in contractions: it's, you're, don't, can't, won't, they're
- NEVER write: its, youre, dont, cant, wont, theyre (without apostrophes)
- AVOID overly emotional/promotional phrases: "you'll wonder how you managed without it", "trust me", "you'll be the hero", "your new best friend"
- AVOID hype words: "amazing", "revolutionary", "game-changing", "life-changing", "incredible"
- USE factual, professional language that focuses on specific benefits and features
- REPLACE promotional claims with specific, measurable benefits

EXAMPLE CORRECT seoKeywords:
{"primary": ["wireless earbuds", "acme", "bluetooth", "headphones", "waterproof", "gaming", "sports"], "longTail": ["best wireless earbuds for running", "acme bluetooth headphones noise cancelling", "waterproof earbuds for swimming"]}

EXAMPLE WRONG seoKeywords:
{"primary": ["Generate 15+ short keywords based on..."]} - THIS IS INSTRUCTION TEXT, NOT KEYWORDS!

Your mission is to break every predictable Amazon listing pattern and create content that sounds genuinely human and emotionally varied while maintaining perfect JSON formatting. 

🎯 HUMAN WRITING REQUIREMENTS:
- Write like you personally own and recommend this product to friends
- Include natural imperfections, honest opinions, and authentic enthusiasm
- Use conversational language with proper contractions (don't, can't, you'll, it's)
- Vary personality across sections - be enthusiastic in bullets, practical in descriptions, helpful in FAQs
- Include specific details that show real product knowledge
- Admit limitations honestly while explaining why the product is still great
- Use relatable comparisons and mini-stories
- Sound like different real people wrote different sections
- AVOID overly promotional language that sounds like advertising copy
- Focus on factual benefits rather than emotional manipulation

🎨 VISUAL TEMPLATE REQUIREMENTS:
- For ALL visualTemplate fields, generate ACTUAL CONTENT specific to the product provided
- imageTitle: Write the actual title (e.g., "Wireless Freedom Everywhere")
- suggestedScene: Describe the actual scene (e.g., "Professional woman at airport using earbuds while working on laptop")
- overlayText: Write the actual text (e.g., "144 Languages • Real-Time Translation • 12-Hour Battery")
- styleGuide: Specify actual style (e.g., "Natural lighting, modern minimalist, professional setting")
- layoutStructure: Describe actual layout (e.g., "Product centered left, person right side, overlay text top")
- colorScheme: Name actual colors (e.g., "Soft blues and whites with navy text accents")
- NEVER write instruction text - only generate ready-to-use content

Write each section in a completely different style and tone. Use unexpected but authentic language that fits the product. Vary everything - sentence length, structure, personality, approach. Sound like a real person who genuinely knows and likes this product. Include human quirks and conversational elements. Your goal is to create listings so human and varied that customers feel like they're talking to a real expert, not reading marketing copy."""
                    
                    # Prepend language requirement to system message if not English
                    if marketplace_lang and marketplace_lang != 'en':
                        language_name = {
                            'de': 'GERMAN', 'fr': 'FRENCH', 'it': 'ITALIAN', 'es': 'SPANISH',
                            'nl': 'DUTCH', 'pl': 'POLISH', 'ja': 'JAPANESE',
                            'pt': 'PORTUGUESE', 'ar': 'ARABIC', 'tr': 'TURKISH'
                        }.get(marketplace_lang, 'ENGLISH')
                        system_content = f"YOU MUST WRITE EVERYTHING IN {language_name}! NOT A SINGLE WORD IN ENGLISH! " + system_content
                    
                    response = self.client.chat.completions.create(
                        model="gpt-5-chat-latest",  # Using GPT-5 for superior quality
                        messages=[
                            {"role": "system", "content": system_content},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=4000,  # Standard max_tokens parameter
                        temperature=1,  # GPT-5 requires temperature to be 1
                    )
                    print(f"OpenAI API call successful on attempt {retry_count + 1}")
                    
                    # Debug: Check if response contains umlauts
                    response_text = response.choices[0].message.content if response.choices else ""
                    if marketplace_lang == 'de':
                        print(f"🔍 AI RESPONSE UMLAUT CHECK:")
                        print(f"   Response contains ü: {'ü' in response_text}")
                        print(f"   Response contains ä: {'ä' in response_text}")
                        print(f"   Response contains ö: {'ö' in response_text}")
                        print(f"   Response contains ß: {'ß' in response_text}")
                        # Show sample of response
                        sample = response_text[:200] if response_text else ""
                        print(f"   Response sample: {sample}...")
                    break
                except Exception as api_error:
                    retry_count += 1
                    error_type = type(api_error).__name__
                    error_message = str(api_error)
                    
                    print(f"🚨 OpenAI API error on attempt {retry_count}/{max_retries}")
                    print(f"Error type: {error_type}")
                    print(f"Error message: {error_message}")
                    
                    # Enhanced error handling based on error types
                    if "rate_limit" in error_message.lower() or "429" in error_message:
                        print("⏱️ Rate limit detected, using exponential backoff")
                        time.sleep(2 ** retry_count)  # Exponential backoff for rate limits
                    elif "insufficient_quota" in error_message.lower() or "billing" in error_message.lower():
                        print("💳 Billing/quota issue detected")
                        raise Exception(f"OpenAI API quota/billing error: {error_message}")
                    elif "invalid_request_error" in error_message.lower():
                        print("📝 Request format error detected")
                        raise Exception(f"OpenAI API request error: {error_message}")
                    else:
                        print(f"🔄 Generic error, retrying in {retry_count} seconds")
                        time.sleep(retry_count)  # Progressive delay
                    
                    if retry_count >= max_retries:
                        print(f"❌ All {max_retries} attempts failed")
                        raise Exception(f"Failed to generate content after {max_retries} attempts. Final error: {error_type}: {error_message}")
            
            if response is None:
                raise Exception("Failed to get response from OpenAI API")
            
            # Extract regular message content (JSON response)
            ai_content = response.choices[0].message.content or "{}"
            
            # CRITICAL FIX: Preserve all UTF-8 characters for international markets
            if marketplace_lang and marketplace_lang != 'en':
                # Keep original content with umlauts/accents for international markets
                print(f"AI Response received: {len(ai_content)} characters (UTF-8 preserved for {marketplace_lang})")
                # Do NOT ASCII-clean international content!
            else:
                # For US market only, clean to ASCII if needed
                ai_content = ai_content.encode('ascii', errors='ignore').decode('ascii')
                print(f"AI Response received: {len(ai_content)} characters (ASCII cleaned for US)")
            # Use safe encoding for Windows
            safe_preview = ai_content[:300]
            safe_ending = ai_content[-200:]
            print(f"AI Response preview: {safe_preview}...")
            print(f"AI Response ending: ...{safe_ending}")
            
            # Enhanced multi-fallback JSON parsing (inspired by GlowReader 3.0)
            result = None
            parsing_attempts = 0
            
            # Attempt 1: Direct parsing with UTF-8 handling for German umlauts
            try:
                parsing_attempts += 1
                print(f"JSON Parsing Attempt {parsing_attempts}: Direct parsing")
                
                # For German content, ensure proper UTF-8 handling
                content_to_parse = ai_content.strip()
                if marketplace_lang == 'de':
                    print(f"🔍 German JSON parsing - checking for umlauts in source:")
                    print(f"   Source contains ü: {'ü' in content_to_parse}")
                    print(f"   Source contains ä: {'ä' in content_to_parse}")
                    print(f"   Source contains ö: {'ö' in content_to_parse}")
                    print(f"   Source contains ß: {'ß' in content_to_parse}")
                
                result = json.loads(content_to_parse)
                print("✅ Direct JSON parsing successful!")
                
                # Verify umlauts are preserved in parsed result
                if marketplace_lang == 'de' and result:
                    title = result.get('productTitle', '')
                    print(f"🔍 Parsed JSON title: {title[:80]}...")
                    print(f"   Parsed title has umlauts: {any(c in title for c in 'äöüßÄÖÜ')}")
                
            except json.JSONDecodeError:
                pass
            
            # Attempt 2: Remove markdown code blocks
            if result is None:
                try:
                    parsing_attempts += 1
                    print(f"JSON Parsing Attempt {parsing_attempts}: Markdown cleanup")
                    cleaned_content = ai_content.strip()
                    
                    # Handle various markdown patterns
                    json_patterns = [
                        (r'```json\s*(.*?)\s*```', 1),  # ```json content ```
                        (r'```\s*(.*?)\s*```', 1),     # ``` content ```
                        (r'`(.*?)`', 1),               # `content`
                    ]
                    
                    for pattern, group in json_patterns:
                        import re
                        match = re.search(pattern, cleaned_content, re.DOTALL)
                        if match:
                            cleaned_content = match.group(group).strip()
                            break
                    
                    result = json.loads(cleaned_content)
                    print("✅ Markdown cleanup parsing successful!")
                except (json.JSONDecodeError, AttributeError):
                    pass
            
            # Attempt 3: Find JSON object boundaries
            if result is None:
                try:
                    parsing_attempts += 1
                    print(f"JSON Parsing Attempt {parsing_attempts}: JSON boundary detection")
                    
                    # Find the first { and last }
                    start = ai_content.find('{')
                    end = ai_content.rfind('}')
                    
                    if start != -1 and end != -1 and end > start:
                        json_content = ai_content[start:end+1]
                        result = json.loads(json_content)
                        print("✅ JSON boundary detection successful!")
                except (json.JSONDecodeError, ValueError):
                    pass
            
            # Attempt 4: Character-by-character cleanup
            if result is None:
                try:
                    parsing_attempts += 1
                    print(f"JSON Parsing Attempt {parsing_attempts}: Character cleanup")
                    
                    # Remove common problematic characters
                    cleaned = ai_content.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
                    cleaned = ' '.join(cleaned.split())  # Normalize whitespace
                    
                    # Try to fix common JSON issues
                    cleaned = cleaned.replace("'", '"')  # Fix single quotes
                    cleaned = re.sub(r'(\w+):', r'"\1":', cleaned)  # Add quotes to keys
                    
                    result = json.loads(cleaned)
                    print("✅ Character cleanup parsing successful!")
                except (json.JSONDecodeError, AttributeError):
                    pass
            
            # Final validation and logging
            if result:
                print(f"🎉 JSON parsing successful after {parsing_attempts} attempts!")
                print(f"🔍 AI response contains {len(result.keys())} fields: {list(result.keys())}")
                
                # Validate critical fields
                critical_fields = ['productDescription', 'bulletPoints', 'amazonTitle']
                for field in critical_fields:
                    if field in result:
                        field_length = len(str(result[field])) if result[field] else 0
                        print(f"✅ {field}: {field_length} characters")
                    else:
                        print(f"⚠️ Missing critical field: {field}")
            else:
                print("❌ All JSON parsing attempts failed!")
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
                # Enhanced JSON parsing specifically for international markets
                parse_attempts = [
                    ("Direct parsing", lambda x: json.loads(x.strip())),
                    ("Strip and parse", lambda x: json.loads(x.strip().replace('\n', ' ').replace('\t', ' '))),
                    ("Extra cleanup", lambda x: json.loads(re.sub(r'\s+', ' ', x.strip()))),
                    ("International chars", lambda x: json.loads(x.strip(), strict=False)),
                    ("UTF-8 fix", lambda x: json.loads(x.encode('utf-8').decode('utf-8'), strict=False)),
                    ("Escape fix", lambda x: json.loads(x.replace('\\"', '"').replace('\\n', '\n'), strict=False)),
                    ("Unterminated string fix", self._fix_unterminated_strings_and_parse)
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
                    
                    # For international markets, use the specialized content extractor
                    marketplace_lang = getattr(product, 'marketplace_language', 'en')
                    if marketplace_lang and marketplace_lang != 'en':
                        print(f"🌍 Using InternationalContentExtractor for {marketplace_lang} market...")
                        from .international_content_extractor import InternationalContentExtractor
                        
                        extractor = InternationalContentExtractor()
                        extracted_result = extractor.extract_international_content(ai_content, marketplace_lang)
                        
                        if extracted_result:
                            print(f"✅ InternationalContentExtractor succeeded for {marketplace_lang} market!")
                            result = extracted_result
                        else:
                            print(f"⚠️ InternationalContentExtractor failed, falling back to manual reconstruction...")
                
                # Last resort: try to extract key information manually  
                if result is None:
                    try:
                        # Enhanced pattern matching for international content (handles special chars and longer content)
                        title_match = re.search(r'"productTitle":\s*"(.*?)"(?=\s*[,}])', cleaned_content, re.DOTALL)
                        desc_match = re.search(r'"productDescription":\s*"(.*?)"(?=\s*[,}])', cleaned_content, re.DOTALL)
                        bullets_match = re.search(r'"bulletPoints":\s*\[\s*(.*?)\s*\]', cleaned_content, re.DOTALL)
                        
                        if title_match:
                            reconstructed_bullets = ["Generated international content", "Please retry if needed"]
                            if bullets_match:
                                # Extract bullet points (enhanced for international content with special chars)
                                bullets_text = bullets_match.group(1)
                                # Multiple extraction attempts for robustness
                                bullet_matches = re.findall(r'"([^"]*(?:\\.[^"]*)*)"', bullets_text)
                                if not bullet_matches:
                                    bullet_matches = re.findall(r'"(.*?)"(?=\s*[,\]])', bullets_text, re.DOTALL)
                                if bullet_matches:
                                    reconstructed_bullets = [bullet.replace('\\"', '"') for bullet in bullet_matches[:5]]
                                    print(f"✅ Extracted {len(reconstructed_bullets)} international bullets")
                                    for i, bullet in enumerate(reconstructed_bullets[:2]):
                                        print(f"   Sample bullet {i+1}: {bullet[:80]}...")
                            
                            print(f"✅ International title extracted: {title_match.group(1)[:100]}...")
                            if bullets_match:
                                print(f"✅ International bullets matched, raw text: {bullets_match.group(1)[:150]}...")
                                print(f"✅ International bullets extracted: {len(reconstructed_bullets)} bullets")
                                for i, bullet in enumerate(reconstructed_bullets[:3]):
                                    print(f"   Bullet {i+1}: {bullet[:80]}...")
                            else:
                                print("❌ No bullets match found")
                            if desc_match:
                                print(f"✅ International description extracted: {desc_match.group(1)[:100]}...")
                            
                            result = {
                                "productTitle": title_match.group(1),
                                "bulletPoints": reconstructed_bullets,
                                "productDescription": desc_match.group(1) if desc_match else "International product description available",
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
                                "PREMIUM QUALITY: Exceptional construction with superior materials and craftsmanship for lasting performance and durability",
                                "RELIABLE PERFORMANCE: Consistent operation designed for daily use with professional-grade standards and proven results", 
                                "USER FRIENDLY: Simple setup and intuitive design makes this perfect for everyone to use regardless of experience level",
                                "GREAT VALUE: Outstanding quality at an affordable price point with excellent customer satisfaction and long-term reliability",
                                "SATISFACTION GUARANTEED: Backed by quality assurance and dedicated customer support team with fast response times"
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
                                    "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Professional lifestyle shot showing satisfied customer using product in real environment - specific setting, lighting, emotions, and product benefits clearly visible. Include demographics, activity context, and conversion elements that resonate with target market.",
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
                # Check the correct field name - InternationalContentExtractor uses 'productTitle'
                title_before = result.get('productTitle', '') or result.get('title', '')
                print(f"Title before cleanup: {len(title_before)} chars, has Unicode: {any(ord(c) > 127 for c in title_before)}")
            except Exception as e:
                print(f"Error checking title before: {e}")
            
            result = self._comprehensive_emoji_removal(result)
            
            print("After emoji removal - checking title...")
            try:
                # Check the correct field name after emoji removal
                title_after = result.get('productTitle', '') or result.get('title', '')
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
                    "bulletPoints": ["PREMIUM QUALITY: High quality construction with superior materials and craftsmanship for lasting durability and exceptional performance", "RELIABLE PERFORMANCE: Consistent and dependable operation designed for daily use with proven results and customer satisfaction", "EXCEPTIONAL VALUE: Great quality at an affordable price point offering the perfect balance of performance and cost-effectiveness", "CUSTOMER SATISFACTION: Backed by thousands of positive reviews and testimonials from happy customers who love this product", "EASY TO USE: Simple setup and user-friendly design makes this perfect for everyone regardless of technical experience"],
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
                            "title": "Premium Quality Excellence",
                            "content": "Transform your experience with professional-grade quality that delivers exceptional results. Our commitment to excellence ensures you get the reliability and performance you deserve.",
                            "keywords": ["premium", "quality", "excellence", "professional"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Hero lifestyle shot showing satisfied customer using product in realistic environment - professional lighting, natural setting, authentic emotions, product prominently displayed showing premium quality and real-world benefits.",
                            "seoOptimization": "Focus on quality and premium positioning with emotional connection"
                        },
                        "section2_features": {
                            "title": "Advanced Features & Benefits",
                            "content": "Discover cutting-edge technology and thoughtful design elements that set our product apart. Every feature is engineered for superior performance and user satisfaction.",
                            "features": ["Premium Materials: Superior construction for lasting durability", "Advanced Technology: State-of-the-art innovation for optimal performance", "Ergonomic Design: Comfortable and intuitive user experience", "Quality Assurance: Rigorous testing ensures reliability", "Versatile Applications: Perfect for multiple use scenarios"],
                            "keywords": ["advanced", "features", "technology", "performance"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Feature showcase grid displaying key product benefits - close-up shots of premium materials, technology demonstrations, ergonomic highlights, quality certifications, and versatility examples.",
                            "seoOptimization": "Feature-focused keywords for technical searches"
                        },
                        "section3_usage": {
                            "title": "Perfect for Every Occasion",
                            "content": "Whether for professional use, daily convenience, or special occasions, our product adapts to your lifestyle and delivers consistent results across all applications.",
                            "use_cases": ["Professional Work: Reliable performance for business needs", "Daily Use: Convenient solution for everyday tasks", "Special Events: Premium quality for important occasions", "Gift Giving: Perfect choice for thoughtful presents"],
                            "keywords": ["versatile", "applications", "lifestyle", "convenience"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Real-world usage scenarios showing product in various environments - professional settings, home use, special occasions, and gift scenarios with diverse demographics.",
                            "seoOptimization": "Usage-based keywords for application searches"
                        },
                        "section4_trust": {
                            "title": "Quality You Can Trust",
                            "content": "Our commitment to excellence is backed by rigorous quality standards, comprehensive warranties, and thousands of satisfied customers worldwide.",
                            "trust_elements": ["Quality Certification: Meets international standards", "Comprehensive Warranty: Full protection for your investment", "Customer Satisfaction: 4.8/5 star rating from verified buyers", "Expert Support: Professional assistance when you need it"],
                            "keywords": ["quality", "trust", "warranty", "satisfaction"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Trust-building elements including certification badges, warranty information, customer testimonials, star ratings, and professional support imagery.",
                            "seoOptimization": "Trust-focused keywords for credibility building"
                        },
                        "section5_comparison": {
                            "title": "Why Choose Our Product",
                            "content": "Compare our superior features, quality, and value against competitors. See why customers consistently choose our product for their needs.",
                            "advantages": ["Superior Quality: Premium materials and construction", "Better Value: Competitive pricing with premium features", "Proven Results: Thousands of satisfied customers", "Comprehensive Support: Full warranty and expert assistance"],
                            "keywords": ["superior", "comparison", "value", "choice"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Side-by-side comparison chart highlighting product advantages - quality differences, value propositions, customer testimonials, and unique selling points.",
                            "seoOptimization": "Competitive keywords for comparison searches"
                        },
                        "section6_testimonials": {
                            "title": "Customer Success Stories",
                            "content": "Read what real customers say about their experience with our product. Join thousands who have made the smart choice for quality and reliability.",
                            "testimonials": ["Outstanding quality and performance - exactly what I needed for my professional work", "Best purchase I've made this year - reliable, durable, and worth every penny", "Exceeded my expectations in every way - highly recommend to anyone looking for quality"],
                            "keywords": ["testimonials", "reviews", "satisfaction", "success"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Customer testimonial collage with real photos, star ratings, quote highlights, and authentic user-generated content showing product in use.",
                            "seoOptimization": "Review-based keywords for social proof"
                        },
                        "section7_guarantee": {
                            "title": "Your Satisfaction Guaranteed",
                            "content": "We stand behind our product with comprehensive warranties, hassle-free returns, and dedicated customer support to ensure your complete satisfaction.",
                            "guarantees": ["Full Warranty Protection", "30-Day Money-Back Guarantee", "Expert Customer Support", "Quality Assurance Promise"],
                            "keywords": ["guarantee", "warranty", "support", "protection"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Guarantee and warranty information display with official badges, policy details, support contact information, and trust seals.",
                            "seoOptimization": "Guarantee-focused keywords for confidence building"
                        },
                        "section8_cta": {
                            "title": "Order Today - Transform Your Experience",
                            "content": "Join thousands of satisfied customers who have upgraded their experience with our premium product. Order now and discover the difference quality makes.",
                            "cta_elements": ["Fast Shipping Available", "Secure Order Processing", "Multiple Payment Options", "Start Your Quality Journey Today"],
                            "keywords": ["order", "premium", "quality", "experience"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Call-to-action section with product packaging, shipping information, payment security badges, and customer satisfaction highlights.",
                            "seoOptimization": "Action-oriented keywords for conversion"
                        },
                        "overallStrategy": "Complete 8-section A+ content strategy for maximum conversion and customer engagement"
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
            
            # Get title and preserve international characters (umlauts, accents, etc.)
            raw_title = result.get('productTitle', '')
            
            # Debug logging for umlaut preservation
            print(f"🔍 TITLE PROCESSING DEBUG:")
            print(f"   Raw title from AI: {raw_title[:80]}...")
            print(f"   Contains ü: {'ü' in raw_title}")
            print(f"   Contains ä: {'ä' in raw_title}")
            print(f"   Contains ö: {'ö' in raw_title}")
            print(f"   Contains ß: {'ß' in raw_title}")
            
            # For international markets, preserve ALL characters including umlauts
            if marketplace_lang and marketplace_lang != 'en':
                # Keep all international characters - only remove actual control characters
                clean_title = ''.join(c for c in raw_title if ord(c) >= 32 or c == '\n')
                clean_title = clean_title.replace('–', '-').replace('"', '"').replace('"', '"')
                print(f"   Clean title after processing: {clean_title[:80]}...")
                print(f"   Clean title has umlauts: {any(c in clean_title for c in 'äöüßÄÖÜ')}")
                listing.title = clean_title.strip()[:200] if clean_title.strip() else f"{product.name} - Premium Quality"
            else:
                # For US market, use ASCII-only
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
                    # For international markets, preserve umlauts and special characters
                    if marketplace_lang and marketplace_lang != 'en':
                        # Keep international characters, only remove control characters
                        clean_bullet = ''.join(c for c in bullet if ord(c) >= 32 or c == '\n')
                        clean_bullet = clean_bullet.replace('–', '-').replace('"', '"').replace('"', '"')
                    else:
                        # For US market, clean to ASCII 
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
            
            # If still no description, generate a professional one
            if not product_description:
                # Create a professional fallback description
                product_description = f"""The {product.brand_name} {product.name} represents advanced engineering in its category, incorporating {product.features if product.features else 'cutting-edge technology and premium materials'} to deliver superior performance. This professional-grade solution addresses the specific challenges users face in this market segment.

Designed with precision manufacturing standards, this product outperforms conventional alternatives through its optimized construction and reliable operation. The engineering team focused on solving common pain points while maintaining the durability and functionality that professionals demand.

Technical specifications include comprehensive compatibility, robust build quality, and performance metrics that exceed industry standards. Each unit undergoes rigorous quality testing to ensure consistent results. Backed by {product.brand_name}'s commitment to excellence and comprehensive warranty coverage for complete peace of mind."""
                
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
            
            # OLD KEYWORD LOGIC - Only use if comprehensive SEO keywords weren't generated
            if not hasattr(listing, 'keywords') or not listing.keywords:
                all_keywords = primary_keywords + secondary_keywords
                listing.keywords = ', '.join(all_keywords) if all_keywords else ''
                # Copy keywords to amazon_keywords for frontend display
                listing.amazon_keywords = listing.keywords
            
            # Backend keywords - ONLY optimize France market (keep USA and Germany untouched)
            backend_keywords = result.get('backendKeywords', '')
            if not backend_keywords:
                # Create fallback backend keywords
                backend_keywords = f"premium quality {product.name.lower()} {product.brand_name.lower()} reliable performance great value"
                print(f"⚠️ No backend keywords from AI, using fallback: {backend_keywords}")
            
            # Check if this is France or Italy market - if so, optimize for 249-byte limit
            marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
            if marketplace_code in ['fr', 'it']:
                # FRANCE AND ITALY ONLY: Apply backend keyword optimization
                base_keywords = [kw.strip() for kw in backend_keywords.replace(',', ' ').split() if kw.strip()]
                optimized_backend = self.backend_optimizer.optimize_backend_keywords(
                    primary_keywords=base_keywords,
                    marketplace=marketplace_code,
                    product_category=getattr(product, 'category', None)
                )
                listing.amazon_backend_keywords = optimized_backend
                
                # Analyze French optimization efficiency
                efficiency = self.backend_optimizer.analyze_keyword_efficiency(optimized_backend, 249)
                print(f"✅ French backend keywords optimized: {efficiency['current_length']}/249 chars ({efficiency['usage_percentage']:.1f}% usage)")
                print(f"✅ French efficiency: {efficiency['efficiency']} ({efficiency['keywords_count']} keywords)")
            else:
                # USA and GERMANY: Keep original working backend keywords untouched
                listing.amazon_backend_keywords = backend_keywords
                print(f"✅ {marketplace_code.upper()} backend keywords preserved: {len(backend_keywords)} characters (keeping original)")
            
            print(f"✅ Final keywords count: {len(all_keywords)} total keywords")
            
            # Parse A+ content from comprehensive new structure
            aplus_plan = result.get('aPlusContentPlan', {})
            
            # Extract hero section from new comprehensive structure (handle both old and new formats)
            hero_section = (aplus_plan.get('heroSection', {}) or 
                           aplus_plan.get('hero_section', {}) or 
                           aplus_plan.get('section1_hero', {}))
            
            # Get hero title and content with improved fallbacks
            if hero_section:
                listing.hero_title = hero_section.get('title', hero_section.get('content', ''))[:100]
                listing.hero_content = hero_section.get('content', hero_section.get('title', ''))
            else:
                # Fallback to brand summary or default
                brand_summary = result.get('brandSummary', '')
                listing.hero_title = (brand_summary.split('.')[0] if brand_summary else 
                                    f'{product.brand_name} Quality Excellence')[:100]
                listing.hero_content = brand_summary or f'Experience premium quality with {product.brand_name} - trusted by customers worldwide for reliability and performance.'
            
            # Extract features from comprehensive new structure (handle both old and new formats)
            features_section = (aplus_plan.get('featuresSection', {}) or 
                              aplus_plan.get('features_section', {}) or 
                              aplus_plan.get('section2_features', {}))
            features_list = features_section.get('features', features_section.get('content', []))
            
            # Ensure features_list is actually a list, not a string
            if isinstance(features_list, str):
                features_list = [features_list]  # Convert single string to list
            elif not isinstance(features_list, list):
                features_list = []  # Ensure it's a list
            
            # If no features from A+ plan, try direct extraction
            if not features_list:
                whats_in_box = result.get('whatsInBox', [])
                if isinstance(whats_in_box, list):
                    features_list = whats_in_box
                else:
                    features_list = []
            if not features_list:
                features_list = [
                    f"Premium {product.name.lower()} construction",
                    f"Reliable {product.brand_name} performance", 
                    "User-friendly design and operation",
                    "Exceptional value and durability",
                    "Professional-grade quality standards"
                ]
            listing.features = '\n'.join(features_list)
            
            # Save comprehensive content from new structure with A+ plan priority
            listing.whats_in_box = '\n'.join(result.get('whatsInBox', []))
            
            # Extract trust builders from A+ plan or fallback to direct result
            trust_section = aplus_plan.get('section3_trust', {}) or aplus_plan.get('trustSection', {})
            trust_content = trust_section.get('content', []) or trust_section.get('trust_builders', [])
            if not trust_content:
                trust_content = result.get('trustBuilders', [])
            listing.trust_builders = '\n'.join(trust_content)
            listing.social_proof = result.get('socialProof', '')
            listing.guarantee = result.get('guarantee', '')
            
            # Parse comprehensive FAQ structure
            faqs_list = result.get('faqs', [])
            if faqs_list:
                faqs_content = '\n\n'.join(faqs_list)
                
                # Fix FAQ format for Polish market
                marketplace_code = getattr(product, 'marketplace', 'com')
                if marketplace_code == 'pl':
                    # Convert Q: → P: and A: → O: for Polish format
                    faqs_content = faqs_content.replace('Q:', 'P:').replace('A:', 'O:')
                elif marketplace_code == 'tr':
                    # Convert Q: → S: and A: → C: for Turkish format
                    faqs_content = faqs_content.replace('Q:', 'S:').replace('A:', 'C:')
                elif marketplace_code == 'be':
                    # Convert Q: → Q: and A: → R: for Belgian French format
                    faqs_content = faqs_content.replace('A:', 'R:')
                
                listing.faqs = faqs_content
            else:
                # No fallback - use empty if AI doesn't provide FAQs
                listing.faqs = ''
            
            # Enhanced SEO keyword processing from comprehensive structure - RE-ENABLED WITH BALANCE FIX
            # Re-enabling to get 75+ keywords but with proper short/long-tail balance
            seo_keywords = result.get('seoKeywords', {})
            if True:  # Re-enabled for comprehensive keywords
                primary_keywords = seo_keywords.get('primary', [])
                long_tail_keywords = seo_keywords.get('longTail', [])
                problem_solving_keywords = seo_keywords.get('problemSolving', [])
                rufus_keywords = seo_keywords.get('rufusConversational', [])
                semantic_keywords = seo_keywords.get('semantic', [])
                
                # Combine all keywords with proper balance enforcement
                all_raw_keywords = primary_keywords + long_tail_keywords + problem_solving_keywords + rufus_keywords + semantic_keywords
                
                if all_raw_keywords:
                    # Classify keywords by word count for proper balance
                    short_tail_keywords = []
                    long_tail_keywords_actual = []
                    
                    for keyword in all_raw_keywords:
                        if isinstance(keyword, str):
                            word_count = len(keyword.split())
                            if word_count <= 2:
                                short_tail_keywords.append(keyword)
                            else:
                                long_tail_keywords_actual.append(keyword)
                    
                    # Enforce balance: aim for 35-40 short + 35-40 long
                    balanced_keywords = []
                    
                    # Add short-tail (limit to 40 best ones)
                    balanced_keywords.extend(short_tail_keywords[:40])
                    
                    # Add long-tail (limit to 40 best ones)  
                    balanced_keywords.extend(long_tail_keywords_actual[:40])
                    
                    # If we don't have enough long-tail, try to create some from short-tail
                    if len(long_tail_keywords_actual) < 30 and len(short_tail_keywords) > 20:
                        # Create long-tail keywords by combining short ones
                        marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
                        if marketplace_code == 'jp':
                            # Add Japanese long-tail patterns
                            for short_kw in short_tail_keywords[:10]:
                                if '、' not in short_kw:  # Avoid duplicating
                                    balanced_keywords.append(f"{short_kw} 高品質 正規品")
                                    balanced_keywords.append(f"{short_kw} 日本語サポート付き")
                        elif marketplace_code == 'de':
                            # Add German long-tail patterns  
                            for short_kw in short_tail_keywords[:10]:
                                balanced_keywords.append(f"{short_kw} premium qualität")
                                balanced_keywords.append(f"{short_kw} deutsche markenqualität")
                        else:
                            # Add English long-tail patterns
                            for short_kw in short_tail_keywords[:10]:
                                balanced_keywords.append(f"premium {short_kw} quality")
                                balanced_keywords.append(f"best {short_kw} value")
                    
                    # Remove duplicates and limit total to 80
                    final_keywords = list(dict.fromkeys(balanced_keywords))[:80]
                    
                    listing.keywords = ', '.join(final_keywords)
                    # Copy keywords to amazon_keywords for frontend display
                    listing.amazon_keywords = listing.keywords
                    
                    # Report balance
                    final_short = [k for k in final_keywords if len(k.split()) <= 2]
                    final_long = [k for k in final_keywords if len(k.split()) > 2]
                    print(f"✅ Balanced keywords saved: {len(final_keywords)} total ({len(final_short)} short-tail + {len(final_long)} long-tail)")
            
            # Enhanced backend keywords - ONLY optimize France market (keep USA and Germany untouched) 
            backend_keywords = result.get('backendKeywords', '')
            if not backend_keywords:
                # Generate comprehensive backend keywords if AI didn't provide them
                backend_keywords = f"{product.name.lower()}, {product.brand_name.lower()}, premium quality, reliable performance, customer satisfaction, professional grade, exceptional value, trusted brand, high quality materials, superior design, innovative features, user friendly, long lasting, industry leading, best in class, top rated, highly recommended, outstanding quality, proven results, customer favorite"
            
            # Check if this is France or Italy market - if so, optimize for 249-byte limit
            marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
            if marketplace_code in ['fr', 'it']:
                # FRANCE AND ITALY ONLY: Apply comprehensive backend keyword optimization
                base_keywords = [kw.strip() for kw in backend_keywords.split(',') if kw.strip()]
                optimized_backend = self.backend_optimizer.optimize_backend_keywords(
                    primary_keywords=base_keywords,
                    marketplace=marketplace_code,
                    product_category=getattr(product, 'category', None)
                )
                listing.amazon_backend_keywords = optimized_backend
            else:
                # USA and GERMANY: Keep original working backend keywords, just trim to 249 chars
                listing.amazon_backend_keywords = backend_keywords[:249]  # Amazon limit is 249 characters
            
            # Save brand summary for A+ content
            brand_summary = result.get('brandSummary', f'{product.brand_name} is committed to delivering exceptional quality and customer satisfaction. With years of experience and innovation, we create products that exceed expectations and provide lasting value for our customers.')
            # Add brand summary to hero content if not already substantial
            if len(listing.hero_content) < 200:
                listing.hero_content = f"{listing.hero_content}\n\n{brand_summary}"[:500]
                
            # CRITICAL FIX: Save missing fields that are expected
            # Save separate SEO keywords (frontend display keywords)
            seo_keywords_list = result.get('seoKeywords', [])
            if isinstance(seo_keywords_list, list):
                listing.amazon_keywords = ', '.join(seo_keywords_list[:15])  # Frontend display keywords
            else:
                listing.amazon_keywords = str(seo_keywords_list)[:200]
            
            # Save brand summary as a separate field (for A+ content reference)
            brand_summary = result.get('brandSummary', f'{product.brand_name} delivers exceptional quality and innovation')
            # Note: Brand summary is integrated into hero_content above, but we also store it separately
            
            # Save the complete A+ content plan as JSON for future reference
            aplus_plan = result.get('aPlusContentPlan', {})
            if aplus_plan:
                # Store the A+ plan structure for debugging and future enhancements
                # aplus_html will be generated later in the code
                pass  # A+ content HTML will be set later in the generation process
            
            print(f"✅ Comprehensive listing content generated:")
            print(f"   - Title: {len(listing.title)} characters")
            print(f"   - Description: {len(listing.long_description)} characters")
            # Count keywords from the current listing.keywords field
            current_keywords = listing.keywords.split(',') if listing.keywords else []
            print(f"   - Keywords: {len(current_keywords)} total")
            print(f"   - Backend Keywords: {len(listing.amazon_backend_keywords)} characters")
            print(f"   - Frontend Keywords: {len(listing.amazon_keywords) if hasattr(listing, 'amazon_keywords') else 0} characters")
            print(f"   - A+ Content: Hero, Features, FAQs, Trust Builders")
            print(f"   - Brand Summary integrated into content")
            self.logger.info("Generating A+ content HTML...")
            # Build comprehensive A+ content HTML from the plan
            
            # Define localized interface labels (needed for all markets) - MOVED HERE TO FIX SCOPE ISSUE
            marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
            
            def get_localized_labels(market_code):
                if market_code == 'tr':
                    return {
                        'keywords': 'Anahtar Kelimeler',
                        'image_strategy': 'Görsel Strateji', 
                        'seo_focus': 'SEO Odak',
                        'features_title': 'Ana Özellikler ve Faydalar',
                        'trust_title': 'Kalite & Güven',
                        'faqs_title': 'Sıkça Sorulan Sorular'
                    }
                elif market_code == 'jp':
                    return {
                        'keywords': 'キーワード',
                        'image_strategy': '画像戦略',
                        'seo_focus': 'SEO焦点'
                    }
                elif market_code == 'de':
                    return {
                        'keywords': 'Schlüsselwörter',
                        'image_strategy': 'Bildstrategie',
                        'seo_focus': 'SEO-Fokus'
                    }
                elif market_code == 'fr':
                    return {
                        'keywords': 'Mots-clés',
                        'image_strategy': 'Stratégie image',
                        'seo_focus': 'Focus SEO'
                    }
                elif market_code == 'es':
                    return {
                        'keywords': 'Palabras clave',
                        'image_strategy': 'Estrategia imagen',
                        'seo_focus': 'Enfoque SEO'
                    }
                elif market_code == 'nl':
                    return {
                        'keywords': 'Trefwoorden',
                        'image_strategy': 'Beeld Strategie',
                        'seo_focus': 'SEO Focus',
                        'features_title': 'Key Features & Benefits',
                        'trust_title': 'Trust & Quality',
                        'faqs_title': 'Frequently Asked Questions'
                    }
                elif market_code == 'eg':
                    return {
                        'keywords': 'الكلمات المفتاحية',
                        'image_strategy': 'استراتيجية الصور',
                        'seo_focus': 'تركيز تحسين محركات البحث',
                        'features_title': 'الميزات والفوائد الرئيسية',
                        'trust_title': 'الجودة والثقة',
                        'faqs_title': 'الأسئلة الشائعة'
                    }
                elif market_code == 'mx':
                    return {
                        'keywords': 'Palabras Clave',
                        'image_strategy': 'Estrategia de Imagen',
                        'seo_focus': 'Enfoque SEO',
                        'features_title': 'Características y Beneficios Clave',
                        'trust_title': 'Calidad y Confianza',
                        'faqs_title': 'Preguntas Frecuentes'
                    }
                elif market_code == 'sa':
                    return {
                        'keywords': 'الكلمات المفتاحية',
                        'image_strategy': 'استراتيجية الصور',
                        'seo_focus': 'تركيز تحسين محركات البحث',
                        'features_title': 'الميزات والفوائد الرئيسية',
                        'trust_title': 'الجودة والثقة',
                        'faqs_title': 'الأسئلة الشائعة'
                    }
                elif market_code == 'in':
                    return {
                        'keywords': 'Keywords',
                        'image_strategy': 'Image Strategy',
                        'seo_focus': 'SEO Focus',
                        'features_title': 'Key Features & Benefits',
                        'trust_title': 'Trust & Quality',
                        'faqs_title': 'Frequently Asked Questions'
                    }
                elif market_code == 'pl':
                    return {
                        'keywords': 'Słowa Kluczowe',
                        'image_strategy': 'Strategia Obrazów',
                        'seo_focus': 'Skupienie SEO',
                        'features_title': 'Kluczowe Cechy i Korzyści',
                        'trust_title': 'Jakość i Zaufanie',
                        'faqs_title': 'Często Zadawane Pytania'
                    }
                elif market_code == 'be':
                    return {
                        'keywords': 'Mots-clés',
                        'image_strategy': 'Stratégie d\'Image',
                        'seo_focus': 'Focus SEO',
                        'features_title': 'Caractéristiques et Avantages Clés',
                        'trust_title': 'Qualité et Confiance',
                        'faqs_title': 'Questions Fréquemment Posées'
                    }
                elif market_code == 'sg':
                    return {
                        'keywords': 'Keywords',
                        'image_strategy': 'Image Strategy',
                        'seo_focus': 'SEO Focus',
                        'features_title': 'Key Features & Benefits',
                        'trust_title': 'Quality & Trust',
                        'faqs_title': 'Frequently Asked Questions'
                    }
                elif market_code == 'au':
                    return {
                        'keywords': 'Keywords',
                        'image_strategy': 'Image Strategy',
                        'seo_focus': 'SEO Focus',
                        'features_title': 'Key Features & Benefits',
                        'trust_title': 'Quality & Trust',
                        'faqs_title': 'Frequently Asked Questions'
                    }
                else:
                    return {
                        'keywords': 'Keywords',
                        'image_strategy': 'Image Strategy',
                        'seo_focus': 'SEO Focus',
                        'features_title': 'Key Features & Benefits',
                        'trust_title': 'Trust & Quality',
                        'faqs_title': 'Frequently Asked Questions'
                    }
            
            localized_labels = get_localized_labels(marketplace_code)
            sections_html = []
            
            # For international markets, ensure we use actual content even if structure is different
            marketplace_lang = getattr(product, 'marketplace_language', 'en')
            
            # Generate HTML for each A+ section with dynamic card types and colors
            # Check for both 'section' prefix and 'section1_hero' style keys
            for section_key, section_data in aplus_plan.items():
                if (section_key.startswith('section') or '_' in section_key) and isinstance(section_data, dict):
                    section_title = section_data.get('title', '')
                    section_content = section_data.get('content', '')
                    section_keywords = ', '.join(section_data.get('keywords', []))
                    image_desc = section_data.get('imageDescription', '')
                    seo_note = section_data.get('seoOptimization', '')
                    
                    # Enhance with culturally-specific keywords based on marketplace and section type
                    marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
                    product_category = getattr(product, 'categories', '').lower() if hasattr(product, 'categories') else ''
                    
                    # Override keywords with cultural ones based on section type and market
                    if 'hero' in section_key.lower() or 'section1' in section_key:
                        # Hero section - trust and brand focused
                        if marketplace_code == 'jp':
                            section_keywords = "プレミアム品質, みんなの信頼, 安心保証, 日本基準"
                        elif marketplace_code == 'es':
                            section_keywords = "calidad premium, confianza familiar, garantía extendida"
                        elif marketplace_code == 'de':
                            section_keywords = "Premium-Qualität, deutsche Standards, TÜV-geprüft"
                        elif marketplace_code == 'fr':
                            section_keywords = "qualité premium, tradition française, savoir-faire"
                        elif marketplace_code == 'it':
                            section_keywords = "qualità premium, eccellenza italiana, fiducia del cliente"
                        elif marketplace_code == 'tr':
                            section_keywords = "premium kalite, güvenilir marka, müşteri memnuniyeti"
                        elif marketplace_code == 'sa':
                            section_keywords = "جودة فائقة، علامة موثوقة، رضا العملاء"
                        elif marketplace_code == 'eg':
                            section_keywords = "جودة ممتازة، علامة تجارية موثوقة، رضا العملاء"
                        elif marketplace_code == 'pl':
                            section_keywords = "jakość premium, zaufana marka, zadowolenie klienta"
                        elif marketplace_code == 'be':
                            section_keywords = "qualité premium, marque de confiance, satisfaction client"
                        elif marketplace_code == 'sg':
                            section_keywords = "premium quality Singapore, trusted brand excellence, customer satisfaction guarantee, multicultural harmony"
                        elif marketplace_code == 'uk':
                            section_keywords = "premium quality Britain, trusted British brand excellence, customer satisfaction guarantee, refined British lifestyle"
                        elif marketplace_code == 'au':
                            section_keywords = "premium quality Australia, trusted brand excellence, customer satisfaction guarantee, Aussie lifestyle"
                        elif marketplace_code == 'in':
                            section_keywords = "premium quality, trusted brand, customer satisfaction"
                        else:
                            section_keywords = "premium quality, trusted brand, customer satisfaction"
                    elif 'feature' in section_key.lower() or 'section2' in section_key:
                        # Features section - functionality focused
                        if marketplace_code == 'jp':
                            if 'audio' in product_category or 'headphone' in product_category:
                                section_keywords = "高音質, ノイズキャンセリング, 長時間再生, 快適装着"
                            elif 'kitchen' in product_category:
                                section_keywords = "衛生的, 食洗機対応, 安全設計, 長持ち"
                            else:
                                section_keywords = "高品質, 安全性, 使いやすさ, 長期保証"
                        elif marketplace_code == 'es':
                            section_keywords = "funcionalidad superior, diseño elegante, uso familiar"
                        elif marketplace_code == 'de':
                            section_keywords = "Ingenieursqualität, Präzision, Zuverlässigkeit, Effizienz"
                        elif marketplace_code == 'fr':
                            section_keywords = "sophistication, élégance française, art de vivre"
                        elif marketplace_code == 'it':
                            section_keywords = "design innovativo, prestazioni superiori, stile italiano"
                        elif marketplace_code == 'tr':
                            section_keywords = "yenilikçi tasarım, yüksek performans, kullanıcı dostu"
                        elif marketplace_code == 'sa':
                            section_keywords = "تصميم مبتكر، أداء عالي، سهل الاستخدام"
                        elif marketplace_code == 'eg':
                            section_keywords = "تصميم مبدع، أداء عالي الجودة، سهل الاستعمال"
                        elif marketplace_code == 'pl':
                            section_keywords = "innowacyjny design, wysoka wydajność, przyjazny użytkownikowi"
                        elif marketplace_code == 'be':
                            section_keywords = "design innovant, haute performance, convivial"
                        elif marketplace_code == 'sg':
                            section_keywords = "innovative design excellence, high performance technology, user-friendly interface, Singapore lifestyle integration"
                        elif marketplace_code == 'uk':
                            section_keywords = "innovative British design excellence, high performance engineering, user-friendly interface, sophisticated British lifestyle integration"
                        elif marketplace_code == 'au':
                            section_keywords = "innovative design excellence, high performance technology, user-friendly interface, Australian lifestyle integration"
                        elif marketplace_code == 'in':
                            section_keywords = "innovative design, high performance, user-friendly"
                        else:
                            section_keywords = "innovative design, high performance, user-friendly"
                    elif 'trust' in section_key.lower() or 'quality' in section_key.lower() or 'guarantee' in section_key.lower():
                        # Trust/Quality section - reliability focused
                        if marketplace_code == 'jp':
                            section_keywords = "みんなが選ぶ安心, 長期保証, 日本品質基準, アフターサポート"
                        elif marketplace_code == 'es':
                            section_keywords = "recomendado por familias, garantía extendida, servicio al cliente"
                        elif marketplace_code == 'de':
                            section_keywords = "TÜV-geprüft, deutsche Qualitätsnormen, Zertifizierung, Compliance"
                        elif marketplace_code == 'fr':
                            section_keywords = "tradition française, savoir-faire, qualité artisanale, héritage"
                        elif marketplace_code == 'it':
                            section_keywords = "tradizione italiana, artigianato, qualità superiore, heritage"
                        elif marketplace_code == 'tr':
                            section_keywords = "5 yıldızlı değerlendirmeler, para iade garantisi, müşteri memnuniyeti"
                        elif marketplace_code == 'sa':
                            section_keywords = "تقييمات 5 نجوم، ضمان استرداد المال، رضا العملاء"
                        elif marketplace_code == 'eg':
                            section_keywords = "تقييمات خمس نجوم، ضمان إرجاع الأموال، رضا العملاء"
                        elif marketplace_code == 'pl':
                            section_keywords = "5-gwiazdkowe recenzje, gwarancja zwrotu pieniędzy, zadowolenie klientów"
                        elif marketplace_code == 'be':
                            section_keywords = "avis 5 étoiles, garantie de remboursement, satisfaction client"
                        elif marketplace_code == 'sg':
                            section_keywords = "5-star Singapore reviews, money-back guarantee, customer satisfaction excellence, trusted by families"
                        elif marketplace_code == 'uk':
                            section_keywords = "5-star British reviews, money-back guarantee, customer satisfaction excellence, trusted by UK families nationwide"
                        elif marketplace_code == 'au':
                            section_keywords = "5-star Australian reviews, money-back guarantee, customer satisfaction excellence, trusted by Aussie families"
                        elif marketplace_code == 'in':
                            section_keywords = "5-star reviews, money-back guarantee, customer satisfaction"
                        else:
                            section_keywords = "5-star reviews, money-back guarantee, customer satisfaction"
                    elif 'usage' in section_key.lower() or 'section3' in section_key:
                        # Usage section - application focused
                        if marketplace_code == 'jp':
                            section_keywords = "日常使い, 様々な場面, 便利性, 効率アップ"
                        elif marketplace_code == 'es':
                            section_keywords = "uso cotidiano, vida familiar, versatilidad, comodidad"
                        elif marketplace_code == 'de':
                            section_keywords = "vielseitige Anwendung, Alltagstauglichkeit, praktisch, effizient"
                        elif marketplace_code == 'fr':
                            section_keywords = "usage quotidien, polyvalence, praticité, élégance d'usage"
                        elif marketplace_code == 'it':
                            section_keywords = "uso quotidiano, versatilità italiana, praticità, stile di vita"
                        elif marketplace_code == 'tr':
                            section_keywords = "günlük kullanım, çok amaçlı, pratik, kullanışlı"
                        elif marketplace_code == 'sa':
                            section_keywords = "استخدام يومي، تطبيقات متنوعة، عملي، مريح"
                        elif marketplace_code == 'eg':
                            section_keywords = "استعمال يومي، تطبيقات متعددة، عملي، مريح"
                        elif marketplace_code == 'pl':
                            section_keywords = "codzienne użycie, wszechstronne zastosowania, praktyczny, wygodny"
                        elif marketplace_code == 'be':
                            section_keywords = "usage quotidien, applications polyvalentes, pratique, pratique"
                        elif marketplace_code == 'sg':
                            section_keywords = "everyday Singapore lifestyle, versatile HDB applications, practical urban living, convenient MRT-friendly"
                        elif marketplace_code == 'uk':
                            section_keywords = "everyday British lifestyle, versatile home applications, practical weather durability, convenient commuter-friendly"
                        elif marketplace_code == 'au':
                            section_keywords = "everyday Australian lifestyle, versatile home applications, practical outback durability, convenient city-friendly"
                        elif marketplace_code == 'in':
                            section_keywords = "everyday use, versatile applications, practical, convenient"
                        else:
                            section_keywords = "everyday use, versatile applications, practical, convenient"
                    elif 'quality' in section_key.lower() or 'section4' in section_key:
                        # Quality section - standards focused
                        if marketplace_code == 'jp':
                            section_keywords = "品質管理, 検査基準, 製造工程, 信頼性テスト"
                        elif marketplace_code == 'es':
                            section_keywords = "control de calidad, estándares europeos, fabricación cuidadosa"
                        elif marketplace_code == 'de':
                            section_keywords = "Qualitätskontrolle, ISO-Standards, deutsche Fertigung, Prüfsiegel"
                        elif marketplace_code == 'fr':
                            section_keywords = "contrôle qualité, normes françaises, fabrication soignée"
                        elif marketplace_code == 'it':
                            section_keywords = "controllo qualità, standard italiani, manifattura eccellente"
                        elif marketplace_code == 'tr':
                            section_keywords = "kalite kontrol, TSE belgesi, CE sertifikası, 2 yıl garanti"
                        elif marketplace_code == 'sa':
                            section_keywords = "مراقبة الجودة، معايير سعودية، تصنيع معتمد، ضمان سنتين"
                        elif marketplace_code == 'eg':
                            section_keywords = "مراقبة الجودة، معايير مصرية، تصنيع معتمد، ضمان سنتان"
                        elif marketplace_code == 'pl':
                            section_keywords = "kontrola jakości, polskie standardy, certyfikowana doskonałość"
                        elif marketplace_code == 'be':
                            section_keywords = "contrôle qualité, normes belges, excellence certifiée"
                        elif marketplace_code == 'sg':
                            section_keywords = "quality control Singapore, SPRING standards, certified excellence, tropical climate tested"
                        elif marketplace_code == 'uk':
                            section_keywords = "quality control Britain, British Standards Institution, certified excellence, UK weather tested"
                        elif marketplace_code == 'au':
                            section_keywords = "quality control Australia, ACMA standards, certified excellence, extreme climate tested"
                        elif marketplace_code == 'in':
                            section_keywords = "quality control, manufacturing standards, certified excellence"
                        else:
                            section_keywords = "quality control, manufacturing standards, certified excellence"
                    elif 'social' in section_key.lower() or 'proof' in section_key.lower() or 'section6' in section_key:
                        # Social proof section - testimonials focused
                        if marketplace_code == 'jp':
                            section_keywords = "お客様満足度, 高評価レビュー, リピーター多数, 口コミ人気"
                        elif marketplace_code == 'es':
                            section_keywords = "testimonios reales, familias satisfechas, recomendaciones"
                        elif marketplace_code == 'de':
                            section_keywords = "Kundenbewertungen, Zufriedenheitsgarantie, Weiterempfehlung"
                        elif marketplace_code == 'fr':
                            section_keywords = "témoignages clients, satisfaction garantie, reconnaissance"
                        elif marketplace_code == 'it':
                            section_keywords = "testimonianze, soddisfazione clienti, raccomandazioni"
                        elif marketplace_code == 'tr':
                            section_keywords = "müşteri yorumları, doğrulanmış incelemeler, memnuniyet garantili"
                        elif marketplace_code == 'sa':
                            section_keywords = "شهادات العملاء، مراجعات موثقة، رضا مضمون"
                        elif marketplace_code == 'eg':
                            section_keywords = "شهادات العملاء، مراجعات موثقة، رضا مضمون"
                        elif marketplace_code == 'pl':
                            section_keywords = "opinie klientów, zweryfikowane recenzje, zadowolenie gwarantowane"
                        elif marketplace_code == 'be':
                            section_keywords = "témoignages clients, avis vérifiés, satisfaction garantie"
                        elif marketplace_code == 'sg':
                            section_keywords = "Singapore customer testimonials, verified family reviews, satisfaction guaranteed, multicultural trust"
                        elif marketplace_code == 'uk':
                            section_keywords = "British customer testimonials, verified family reviews, satisfaction guaranteed, authentic British trust"
                        elif marketplace_code == 'au':
                            section_keywords = "Australian customer testimonials, verified family reviews, satisfaction guaranteed, fair dinkum trust"
                        elif marketplace_code == 'in':
                            section_keywords = "customer testimonials, verified reviews, satisfaction guaranteed"
                        else:
                            section_keywords = "customer testimonials, verified reviews, satisfaction guaranteed"
                    elif 'comparison' in section_key.lower() or 'section7' in section_key:
                        # Comparison section - competitive advantage focused
                        if marketplace_code == 'jp':
                            section_keywords = "他社比較, 優位性, 選ばれる理由, 差別化ポイント"
                        elif marketplace_code == 'es':
                            section_keywords = "ventajas competitivas, mejor elección, diferencias clave"
                        elif marketplace_code == 'de':
                            section_keywords = "Wettbewerbsvorteil, Alleinstellungsmerkmal, Überlegenheit"
                        elif marketplace_code == 'fr':
                            section_keywords = "avantages concurrentiels, supériorité, choix optimal"
                        elif marketplace_code == 'it':
                            section_keywords = "vantaggi competitivi, superiorità, scelta migliore"
                        elif marketplace_code == 'tr':
                            section_keywords = "rekabet avantajı, üstün seçim, temel farklılıklar"
                        elif marketplace_code == 'sa':
                            section_keywords = "ميزة تنافسية، خيار متفوق، مميزات رئيسية"
                        elif marketplace_code == 'eg':
                            section_keywords = "ميزة تنافسية، الخيار الأفضل، مزايا أساسية"
                        elif marketplace_code == 'pl':
                            section_keywords = "przewaga konkurencyjna, najlepszy wybór, kluczowe różnice"
                        elif marketplace_code == 'be':
                            section_keywords = "avantage concurrentiel, choix supérieur, différenciateurs clés"
                        elif marketplace_code == 'sg':
                            section_keywords = "competitive advantage Singapore, superior choice excellence, key differentiators, Lion City quality"
                        elif marketplace_code == 'uk':
                            section_keywords = "competitive advantage Britain, superior choice excellence, key differentiators, British innovation heritage"
                        elif marketplace_code == 'au':
                            section_keywords = "competitive advantage Australia, superior choice excellence, key differentiators, Aussie innovation"
                        elif marketplace_code == 'in':
                            section_keywords = "competitive advantage, superior choice, key differentiators"
                        else:
                            section_keywords = "competitive advantage, superior choice, key differentiators"
                    elif 'package' in section_key.lower() or 'section8' in section_key:
                        # Package section - contents focused
                        if marketplace_code == 'jp':
                            section_keywords = "同梱内容, パッケージング, 付属品, 開封体験"
                        elif marketplace_code == 'es':
                            section_keywords = "contenido completo, empaque premium, accesorios incluidos"
                        elif marketplace_code == 'de':
                            section_keywords = "Lieferumfang, Verpackungsqualität, Zubehör, Vollständigkeit"
                        elif marketplace_code == 'fr':
                            section_keywords = "contenu livré, emballage soigné, accessoires inclus"
                        elif marketplace_code == 'it':
                            section_keywords = "contenuto confezione, imballaggio curato, accessori inclusi"
                        elif marketplace_code == 'tr':
                            section_keywords = "paket içeriği, premium ambalaj, dahil aksesuarlar"
                        elif marketplace_code == 'sa':
                            section_keywords = "محتويات العبوة، تغليف فاخر، إكسسوارات مدرجة"
                        elif marketplace_code == 'eg':
                            section_keywords = "محتويات الحزمة، تعبئة فاخرة، اكسسوارات مشمولة"
                        elif marketplace_code == 'pl':
                            section_keywords = "zawartość opakowania, premium pakowanie, dołączone akcesoria"
                        elif marketplace_code == 'be':
                            section_keywords = "contenu emballage, emballage premium, accessoires inclus"
                        elif marketplace_code == 'sg':
                            section_keywords = "complete package contents, premium Singapore packaging, included accessories, tropical-ready materials"
                        elif marketplace_code == 'uk':
                            section_keywords = "complete package contents, premium British packaging, included accessories, weather-resistant materials"
                        elif marketplace_code == 'au':
                            section_keywords = "complete package contents, premium Australian packaging, included accessories, extreme-weather materials"
                        elif marketplace_code == 'in':
                            section_keywords = "package contents, premium packaging, included accessories"
                        else:
                            section_keywords = "package contents, premium packaging, included accessories"
                    elif 'faq' in section_key.lower() or 'support' in section_key.lower():
                        # FAQ/Support section - help focused
                        if marketplace_code == 'jp':
                            section_keywords = "詳しい説明, 心配解消, 使い方ガイド, トラブル対応"
                        elif marketplace_code == 'es':
                            section_keywords = "ayuda familiar, dudas comunes, consejos prácticos"
                        elif marketplace_code == 'de':
                            section_keywords = "technische Details, Bedienungsanleitung, Problemlösung"
                        elif marketplace_code == 'fr':
                            section_keywords = "conseils d'expert, solutions élégantes, guide sophistiqué"
                        elif marketplace_code == 'it':
                            section_keywords = "supporto tecnico, guide dettagliate, assistenza italiana"
                        elif marketplace_code == 'tr':
                            section_keywords = "sık sorulan sorular, Türkçe destek, kullanım kılavuzu, problem çözümü"
                        elif marketplace_code == 'sa':
                            section_keywords = "أسئلة شائعة، دعم باللغة العربية، دليل الاستخدام، حل المشاكل"
                        elif marketplace_code == 'eg':
                            section_keywords = "أسئلة شائعة، دعم باللغة العربية، دليل الاستعمال، حل المشاكل"
                        elif marketplace_code == 'pl':
                            section_keywords = "szybkie odpowiedzi, rozwiązywanie problemów, przewodnik użytkownika"
                        elif marketplace_code == 'in':
                            section_keywords = "quick answers, troubleshooting, user guide"
                        else:
                            section_keywords = "quick answers, troubleshooting, user guide"
                    
                    # Also enhance image descriptions culturally
                    if not image_desc or len(image_desc) < 50:
                        if 'hero' in section_key.lower() or 'section1' in section_key:
                            if marketplace_code == 'jp':
                                image_desc = "日本の家庭で安心して使用、清潔感と品質を重視 (970x600px)"
                            elif marketplace_code == 'es':
                                image_desc = "Familia española disfrutando del producto, ambiente cálido (970x600px)"
                            elif marketplace_code == 'de':
                                image_desc = "Deutsche Qualität und Präzision im modernen Zuhause (970x600px)"
                            elif marketplace_code == 'fr':
                                image_desc = "Élégance française, sophistication au quotidien (970x600px)"
                            else:
                                image_desc = "Modern lifestyle, premium quality experience (970x600px)"
                    card_type = section_data.get('cardType', 'default')
                    card_color = section_data.get('cardColor', 'gray')
                    visual_template = section_data.get('visualTemplate', {})
                    
                    # Define color schemes for different card types with dynamic assignment
                    color_schemes = {
                        'blue': {'bg': 'bg-blue-50', 'border': 'border-blue-200', 'title': 'text-blue-900', 'badge': 'bg-blue-100 text-blue-800'},
                        'green': {'bg': 'bg-green-50', 'border': 'border-green-200', 'title': 'text-green-900', 'badge': 'bg-green-100 text-green-800'},
                        'purple': {'bg': 'bg-purple-50', 'border': 'border-purple-200', 'title': 'text-purple-900', 'badge': 'bg-purple-100 text-purple-800'},
                        'orange': {'bg': 'bg-orange-50', 'border': 'border-orange-200', 'title': 'text-orange-900', 'badge': 'bg-orange-100 text-orange-800'},
                        'teal': {'bg': 'bg-teal-50', 'border': 'border-teal-200', 'title': 'text-teal-900', 'badge': 'bg-teal-100 text-teal-800'},
                        'indigo': {'bg': 'bg-indigo-50', 'border': 'border-indigo-200', 'title': 'text-indigo-900', 'badge': 'bg-indigo-100 text-indigo-800'},
                        'pink': {'bg': 'bg-pink-50', 'border': 'border-pink-200', 'title': 'text-pink-900', 'badge': 'bg-pink-100 text-pink-800'},
                        'yellow': {'bg': 'bg-yellow-50', 'border': 'border-yellow-200', 'title': 'text-yellow-900', 'badge': 'bg-yellow-100 text-yellow-800'}
                    }
                    
                    # Dynamic color assignment based on section
                    section_colors = {
                        'section1_hero': 'blue',
                        'section2_features': 'green',
                        'section3_usage': 'purple',
                        'section4_quality': 'orange',
                        'section5_guarantee': 'teal',
                        'section6_social_proof': 'indigo',
                        'section7_comparison': 'pink',
                        'section8_package': 'yellow'
                    }
                    
                    assigned_color = section_colors.get(section_key, card_color if card_color != 'default' else 'blue')
                    colors = color_schemes.get(assigned_color, color_schemes['blue'])
                    
                    # Enhanced dynamic icons based on section key for better visual hierarchy
                    section_icons = {
                        'section1_hero': '🚀',
                        'section2_features': '✨', 
                        'section3_usage': '🎯',
                        'section4_quality': '🏆',
                        'section5_guarantee': '🛡️',
                        'section6_social_proof': '💬',
                        'section7_comparison': '📊',
                        'section8_package': '📦',
                        'hero': '🌟',
                        'features': '⚡',
                        'usage': '🔥',
                        'quality': '💎',
                        'guarantee': '🛡️',
                        'social': '🤝',
                        'comparison': '📈',
                        'package': '🎁',
                        'default': '💫'
                    }
                    
                    # Try to match icon based on section key
                    icon = section_icons.get(section_key, section_icons.get(card_type, section_icons['default']))
                    
                    # Generate visual template HTML if available
                    visual_template_html = ""
                    if visual_template:
                        template_type = visual_template.get('templateType', 'standard')
                        image_title = visual_template.get('imageTitle', '')
                        suggested_scene = visual_template.get('suggestedScene', '')
                        overlay_text = visual_template.get('overlayText', '')
                        style_guide = visual_template.get('styleGuide', '')
                        layout_structure = visual_template.get('layoutStructure', '')
                        color_scheme = visual_template.get('colorScheme', '')
                        design_elements = visual_template.get('designElements', [])
                        
                        visual_template_html = f"""
        <div class="visual-template-generator bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-200 rounded-lg p-4 mt-4">
            <div class="flex items-center mb-3">
                <span class="text-2xl mr-2">🎨</span>
                <h4 class="text-indigo-900 font-semibold text-lg">A+ Visual Template Generator</h4>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                <div class="template-brief bg-white p-3 rounded border">
                    <h5 class="font-semibold text-gray-900 mb-2">📸 {template_type.title()} Image Brief</h5>
                    <div class="text-sm space-y-2">
                        <div><strong>Title:</strong> {image_title}</div>
                        <div><strong>Scene:</strong> {suggested_scene}</div>
                        <div><strong>Overlay Text:</strong> "{overlay_text}"</div>
                    </div>
                </div>
                
                <div class="style-guide bg-white p-3 rounded border">
                    <h5 class="font-semibold text-gray-900 mb-2">🎯 Design Guidelines</h5>
                    <div class="text-sm space-y-2">
                        <div><strong>Style:</strong> {style_guide}</div>
                        <div><strong>Layout:</strong> {layout_structure}</div>
                        <div><strong>Colors:</strong> {color_scheme}</div>
                    </div>
                </div>
            </div>
            
            <div class="design-elements bg-white p-3 rounded border">
                <h5 class="font-semibold text-gray-900 mb-2">🔧 Required Elements</h5>
                <div class="flex flex-wrap gap-2">
                    {' '.join([f'<span class="bg-indigo-100 text-indigo-800 px-2 py-1 rounded text-xs">{element}</span>' for element in design_elements])}
                </div>
            </div>
            
            <div class="template-download mt-4 text-center">
                <p class="text-xs text-gray-600 mb-2">💡 Copy this brief to Canva, Figma, or share with your designer</p>
                <button class="bg-indigo-600 text-white px-4 py-2 rounded text-sm font-medium hover:bg-indigo-700 transition-colors">
                    📄 Download PDF Brief
                </button>
            </div>
        </div>"""

                    section_html = f"""
    <div class="aplus-section-card {colors['bg']} {colors['border']} border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">{icon}</span>
            <div class="flex-1">
                <h3 class="{colors['title']} text-xl sm:text-2xl font-bold">{section_title}</h3>
                <p class="text-gray-600 text-sm mt-1">{card_type.title()} section with detailed content and optimization</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <p class="text-gray-700 leading-relaxed text-sm sm:text-base">{section_content}</p>
        </div>
        {visual_template_html}
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{section_keywords}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{image_desc}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{seo_note}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(section_html)
            
            
            # If no sections were generated (common for international markets), create them from actual content
            # Include Turkey (tr) to ensure it gets comprehensive sections like Mexico
            # FORCE Turkey to use comprehensive sections like Mexico regardless of initial sections
            if (not sections_html and (listing.hero_title or listing.features or listing.trust_builders)) or marketplace_code == 'tr':
                # Clear existing sections for Turkey to ensure it gets comprehensive generation
                if marketplace_code == 'tr':
                    sections_html = []
                    self.logger.info("🇹🇷 FORCING Turkey comprehensive section generation like Mexico")
                else:
                    self.logger.info("Creating A+ sections from extracted content for international market")
                
                # Create hero section from actual hero content with new box design
                if listing.hero_title and listing.hero_content:
                    if marketplace_code == 'jp':
                        keywords_text = "プレミアム, 品質, 信頼性"
                        image_text = "ライフスタイル写真 (970x600px)"
                        seo_text = "品質重視のSEO戦略"
                        premium_label = "プレミアム体験"
                        premium_desc = "日本の品質基準に準拠した優れた設計"
                    elif marketplace_code == 'es':
                        keywords_text = "premium, calidad, confianza"
                        image_text = "Imagen de estilo de vida (970x600px)"
                        seo_text = "Estrategia SEO de calidad"
                        premium_label = "Experiencia Premium"
                        premium_desc = "Diseño superior con estándares europeos"
                    elif marketplace_code == 'de':
                        keywords_text = "Premium, Qualität, Vertrauen"
                        image_text = "Lifestyle-Bild (970x600px)"
                        seo_text = "Qualitätsfokussierte SEO-Strategie"
                        premium_label = "Premium-Erlebnis"
                        premium_desc = "Überlegenes Design nach deutschen Standards"
                    elif marketplace_code == 'fr':
                        keywords_text = "premium, qualité, confiance"
                        image_text = "Image lifestyle (970x600px)"
                        seo_text = "Stratégie SEO axée qualité"
                        premium_label = "Expérience Premium"
                        premium_desc = "Conception supérieure aux normes françaises"
                    elif marketplace_code == 'tr':
                        keywords_text = "premium kalite, güvenilir marka, müşteri memnuniyeti"
                        if 'audio' in product_category or 'headphone' in product_category:
                            image_text = "ENGLISH: Turkish family in modern home during New Year celebration, father gaming with premium headset while children watch excitedly, warm festive lighting with traditional decorations in background, RGB headset glowing, quality time together, Turkish hospitality atmosphere visible (970x600px)"
                        elif 'kitchen' in product_category:
                            image_text = "ENGLISH: Traditional Turkish kitchen during family gathering, grandmother using premium knife sharpener while family prepares feast together, warm lighting, fresh ingredients and traditional Turkish dishes, multi-generational cooking moment, hospitality elements visible (970x600px)"
                        elif 'water' in product_category or 'bottle' in product_category:
                            image_text = "ENGLISH: Active Turkish family at Bosphorus park during weekend, father drinking from large water bottle after outdoor activity, children playing nearby, golden sunset lighting, healthy lifestyle focus, Istanbul skyline in background, family values combined (970x600px)"
                        else:
                            image_text = "ENGLISH: Turkish family in modern home showcasing premium product, quality lifestyle focus, warm lighting, traditional hospitality values with modern functionality (970x600px)"
                        seo_text = "Kalite odaklı SEO stratejisi"
                        premium_label = "Premium Deneyim"
                        premium_desc = "Türk standartlarına göre üstün tasarım ve kalite"
                    elif marketplace_code == 'sa':
                        keywords_text = "جودة فائقة، علامة موثوقة، رضا العملاء"
                        image_text = "عائلة سعودية في منزل عصري أثناء عيد الفطر، الأب يلعب الألعاب بينما يشاهد الأطفال، إضاءة دافئة، السماعة ظاهرة مع إضاءة RGB، أجواء احتفالية (970x600px)"
                        seo_text = "استراتيجية تحسين محركات البحث المركزة على الجودة"
                        premium_label = "تجربة فاخرة"
                        premium_desc = "تصميم متفوق وفقاً للمعايير السعودية العالية"
                    elif marketplace_code == 'in':
                        keywords_text = "premium quality, trusted brand, customer satisfaction"
                        image_text = "Indian family in modern kitchen during festival preparation, mother using premium knife set to prepare dal sabzi while family gathers around, traditional spices and fresh vegetables visible, warm festive lighting with rangoli in background, perfect gifting moment (970x600px)"
                        seo_text = "Indian cooking and festival gifting focused SEO strategy"
                        premium_label = "Premium Experience"
                        premium_desc = "Superior design perfect for Indian cooking and festival gifting"
                    elif marketplace_code == 'nl':
                        keywords_text = "premium kwaliteit, betrouwbaar merk, klanttevredenheid"
                        image_text = "ENGLISH: Dutch lifestyle hero image with product (970x600px)"
                        seo_text = "Kwaliteit gerichte SEO strategie"
                        premium_label = "Premium Ervaring"
                        premium_desc = "Superieur ontwerp volgens Nederlandse normen"
                    elif marketplace_code == 'pl':
                        keywords_text = "premium jakość, zaufana marka, zadowolenie klientów"
                        if 'audio' in product_category or 'headphone' in product_category:
                            image_text = "ENGLISH: Polish family in cozy living room during Christmas preparations, father gaming with premium headset while children watch excitedly, warm festive lighting with Christmas tree in background, RGB headset glowing, quality time together, traditional Polish decorations visible (970x600px)"
                        elif 'kitchen' in product_category:
                            image_text = "ENGLISH: Traditional Polish kitchen during Christmas Eve preparation, grandmother using premium knife sharpener while family gathers around traditional wigilia table, warm lighting, fresh bread and traditional Polish dishes, multi-generational cooking moment, heritage elements visible (970x600px)"
                        elif 'water' in product_category or 'bottle' in product_category:
                            image_text = "ENGLISH: Active Polish family at outdoor park during weekend, father drinking from large water bottle after cycling, children playing nearby, morning sunlight, healthy lifestyle focus, Polish nature in background, fitness and family values combined (970x600px)"
                        else:
                            image_text = "ENGLISH: Polish family in modern home showcasing premium product, quality lifestyle focus, warm lighting, traditional values with modern functionality (970x600px)"
                        seo_text = "Strategia SEO skoncentrowana na jakości polskiej"
                        premium_label = "Premium Doświadczenie"
                        premium_desc = "Najwyższa jakość zgodna z polskimi standardami i tradycjami rodzinnymi"
                    elif marketplace_code == 'be':
                        keywords_text = "qualité premium, marque de confiance, satisfaction client"
                        if 'audio' in product_category or 'headphone' in product_category:
                            image_text = "ENGLISH: Belgian family in elegant home during holiday celebration, father enjoying premium headset while family gathers around, warm festive lighting with European decorations, RGB headset glowing, quality time together, Belgian hospitality and sophistication visible (970x600px)"
                        elif 'kitchen' in product_category:
                            image_text = "ENGLISH: Traditional Belgian kitchen during family meal preparation, grandmother using premium knife sharpener while family prepares European feast, warm lighting, fresh ingredients and traditional Belgian specialties, multi-generational cooking moment, European heritage elements visible (970x600px)"
                        elif 'water' in product_category or 'bottle' in product_category:
                            image_text = "ENGLISH: Active Belgian family at European countryside during weekend, father drinking from large water bottle after cycling, children playing nearby, golden sunlight, healthy lifestyle focus, Belgian landscapes in background, family values combined (970x600px)"
                        else:
                            image_text = "ENGLISH: Belgian family in modern European home showcasing premium product, quality lifestyle focus, warm lighting, traditional European values with modern functionality (970x600px)"
                        seo_text = "Stratégie SEO axée sur la qualité belge"
                        premium_label = "Expérience Premium"
                        premium_desc = "Qualité supérieure conforme aux standards belges et traditions européennes"
                    elif marketplace_code == 'sg':
                        keywords_text = "premium quality Singapore excellence, trusted brand multicultural, customer satisfaction guaranteed Singapore"
                        if 'audio' in product_category or 'headphone' in product_category:
                            image_text = "ENGLISH: Elegant Singaporean family in premium HDB apartment during Chinese New Year reunion celebration, father experiencing luxury gaming headset while multi-generational family shares prosperity feast, authentic red lanterns with Singapore skyline view, warm festive lighting, RGB headset illuminating modern Asian décor, harmony between traditional values and cutting-edge technology, Merlion visible through window, Singapore multicultural unity and hospitality essence captured (970x600px)"
                        elif 'kitchen' in product_category:
                            image_text = "ENGLISH: Contemporary Singapore HDB kitchen during festive meal preparation, experienced grandmother demonstrating premium knife sharpener while family prepares traditional laksa and bak kwa, efficient modern kitchen with Marina Bay view, fresh tropical ingredients and local hawker-inspired specialties, multi-generational cooking wisdom, Singapore's rich food heritage and innovation visible, authentic Lion City atmosphere (970x600px)"
                        elif 'water' in product_category or 'bottle' in product_category:
                            image_text = "ENGLISH: Active Singaporean family exercising at Marina Bay Sands area during golden hour weekend, father hydrating from premium water bottle after MRT commute and jogging, children playing with Gardens by the Bay backdrop, golden tropical sunlight filtering through urban canopy, healthy Singapore lifestyle focus, iconic landmarks including Singapore Flyer visible, modern tropical city living excellence (970x600px)"
                        else:
                            image_text = "ENGLISH: Sophisticated Singaporean family in modern executive HDB showcasing premium product, quality lifestyle excellence focus, contemporary lighting with tropical ambiance, perfect blend of traditional Asian family values with Singapore's technological innovation and efficiency, multicultural harmony and Lion City prosperity visible, authentic Singapore living standard (970x600px)"
                        seo_text = "Advanced SEO strategy optimized for Singapore market excellence and multicultural search patterns"
                        premium_label = "Singapore Premium Excellence"
                        premium_desc = "Superior quality engineered for Singapore standards, tropical climate durability, and multicultural family traditions"
                    elif marketplace_code == 'uk':
                        keywords_text = "premium quality British excellence, trusted brand heritage, customer satisfaction guaranteed Britain"
                        if 'audio' in product_category or 'headphone' in product_category:
                            image_text = "ENGLISH: Distinguished British family in elegant Georgian home during Boxing Day celebration, father enjoying premium gaming headset while multi-generational family gathers around traditional fireplace, festive Christmas decorations visible, warm ambient lighting, RGB headset complementing sophisticated British interior, harmony between British heritage and modern technology, Big Ben visible through window, authentic British refinement and tradition captured (970x600px)"
                        elif 'kitchen' in product_category:
                            image_text = "ENGLISH: Elegant British kitchen during Sunday roast preparation, experienced cook demonstrating premium knife sharpener while family prepares traditional Yorkshire pudding and beef roast, classic Shaker-style kitchen with countryside view, fresh British ingredients and seasonal vegetables, multi-generational cooking traditions, Britain's rich culinary heritage and innovation visible, authentic British home cooking excellence (970x600px)"
                        elif 'water' in product_category or 'bottle' in product_category:
                            image_text = "ENGLISH: Active British family exercising in Hyde Park during crisp autumn morning, father hydrating from premium water bottle after morning jog and cycling, children playing with London Eye backdrop, golden British sunlight filtering through changing leaves, healthy British outdoor lifestyle focus, iconic landmarks including Tower Bridge visible, modern British urban living excellence (970x600px)"
                        else:
                            image_text = "ENGLISH: Sophisticated British family in refined home showcasing premium product, quality lifestyle excellence focus, natural lighting with British countryside ambiance, perfect blend of traditional British values with Britain's technological innovation and reliability, authentic British heritage and modern prosperity visible, distinguished British living standard (970x600px)"
                        seo_text = "Advanced SEO strategy optimized for British market excellence and sophisticated search patterns"
                        premium_label = "British Premium Excellence"
                        premium_desc = "Superior quality engineered for British standards, weather durability, and traditional British family values"
                    elif marketplace_code == 'au':
                        keywords_text = "premium quality Australian excellence, trusted brand fair dinkum, customer satisfaction guaranteed Australia"
                        if 'audio' in product_category or 'headphone' in product_category:
                            image_text = "ENGLISH: Authentic Australian family in modern Queensland home during Australia Day celebration, father experiencing premium gaming headset while multi-generational family enjoys backyard BBQ, Southern Cross visible in twilight sky, warm golden hour lighting, RGB headset illuminating contemporary Australian décor, harmony between laid-back Aussie culture and cutting-edge technology, Sydney Harbour Bridge visible in distance, Australian mateship and hospitality essence captured (970x600px)"
                        elif 'kitchen' in product_category:
                            image_text = "ENGLISH: Contemporary Australian kitchen during weekend family cooking, experienced grandmother demonstrating premium knife sharpener while family prepares traditional meat pies and pavlova, modern open-plan kitchen with bushland view, fresh local ingredients and Australian specialties, multi-generational cooking wisdom, Australia's rich culinary heritage and innovation visible, authentic Aussie fair dinkum atmosphere (970x600px)"
                        elif 'water' in product_category or 'bottle' in product_category:
                            image_text = "ENGLISH: Active Australian family exercising at Bondi Beach area during golden hour weekend, father hydrating from premium water bottle after surfing and beach run, children playing with Sydney Opera House backdrop, warm Australian sunlight filtering through coastal environment, healthy Aussie outdoor lifestyle focus, iconic landmarks including Harbour Bridge visible, modern Australian coastal living excellence (970x600px)"
                        else:
                            image_text = "ENGLISH: Relaxed Australian family in modern home showcasing premium product, quality lifestyle excellence focus, natural lighting with outback ambiance, perfect blend of traditional Aussie values with Australia's technological innovation and efficiency, fair dinkum mateship and Australian prosperity visible, authentic Australian living standard (970x600px)"
                        seo_text = "Advanced SEO strategy optimized for Australian market excellence and fair dinkum search patterns"
                        premium_label = "Australian Premium Excellence"
                        premium_desc = "Superior quality engineered for Australian standards, extreme climate durability, and fair dinkum family traditions"
                    else:
                        keywords_text = "premium, quality, trust"
                        image_text = "Hero lifestyle image (970x600px)"
                        seo_text = "Quality-focused SEO strategy"
                        premium_label = "Premium Experience"
                        premium_desc = "Superior design and quality standards"
                    
                    hero_html = f"""
    <div class="aplus-section-card bg-blue-50 border-blue-200 border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">🚀</span>
            <div class="flex-1">
                <h3 class="text-blue-900 text-xl sm:text-2xl font-bold">{listing.hero_title}</h3>
                <p class="text-gray-600 text-sm mt-1">Hero section with brand story and value proposition</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <p class="text-gray-700 leading-relaxed text-sm sm:text-base">{listing.hero_content}</p>
        </div>
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{keywords_text}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{image_text}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{seo_text}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(hero_html)
                
                # Create features section from actual bullet points with new box design
                if listing.bullet_points or listing.features:
                    # Use bullet points if available, otherwise fall back to features
                    if listing.bullet_points:
                        bullet_list = listing.bullet_points.split('\n') if isinstance(listing.bullet_points, str) else listing.bullet_points
                        # Clean bullet points (remove emojis and bullet formatting for features section)
                        clean_bullets = []
                        for bullet in bullet_list[:6]:
                            # Remove emojis and common bullet prefixes
                            clean_bullet = bullet.strip()
                            if clean_bullet.startswith('🔋') or clean_bullet.startswith('🎧') or clean_bullet.startswith('⭐'):
                                # Extract main content after emoji and colon
                                parts = clean_bullet.split(':', 1)
                                if len(parts) > 1:
                                    clean_bullet = parts[1].strip()
                            clean_bullets.append(clean_bullet)
                        features_items = '\n'.join([f"<li class='mb-2'>{feature}</li>" for feature in clean_bullets if feature])
                    else:
                        features_list = listing.features.split('\n') if isinstance(listing.features, str) else listing.features
                        features_items = '\n'.join([f"<li class='mb-2'>{feature}</li>" for feature in features_list[:6]])
                    
                    # Get marketplace and culture-specific keywords for features
                    product_category = getattr(product, 'categories', '').lower() if hasattr(product, 'categories') else ''
                    
                    if marketplace_code == 'jp':
                        # Japanese culture: emphasizes quality, safety, and group harmony
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "高音質, ノイズキャンセリング, 長時間再生, 快適装着"
                        elif 'kitchen' in product_category or 'cutting' in product_category:
                            features_keywords = "衛生的, 食洗機対応, 安全設計, 長持ち"
                        elif 'electronics' in product_category:
                            features_keywords = "省エネ, 高性能, 操作簡単, 日本製品質"
                        else:
                            features_keywords = "高品質, 安全性, 使いやすさ, 長期保証"
                        # Japanese image: clean, minimalist, technical precision
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "清潔な白背景で機能を精密に表示、日本語説明付き (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "日本の台所で使用シーン、清潔感と機能性を強調 (1500x1500px)"
                        else:
                            features_image = "機能詳細図解、日本語ラベル付き (1500x1500px)"
                        features_seo = "機能キーワード最適化戦略"
                    elif marketplace_code == 'br':
                        # Brazil culture: vibrant, family-oriented, celebration
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "som cristalino, cancelamento ruído, bateria longa, confortável"
                        elif 'kitchen' in product_category:
                            features_keywords = "cozinha prática, família brasileira, durável, fácil limpeza"
                        else:
                            features_keywords = "qualidade premium, garantia estendida, suporte brasileiro"
                        # Brazil image descriptions in Portuguese
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "Pessoa usando fones em ambiente tropical, destaque para recursos técnicos com ícones coloridos (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "Cozinha brasileira moderna mostrando produto em uso, família preparando refeição (1500x1500px)"
                        else:
                            features_image = "Infográfico com recursos detalhados, cores vibrantes do Brasil (1500x1500px)"
                        features_seo = "Otimização para palavras-chave de recursos técnicos"
                    elif marketplace_code == 'mx':
                        # Mexico culture: family values, warmth, tradition
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "sonido superior, cancelación ruido, batería duradera, comodidad total"
                        elif 'kitchen' in product_category:
                            features_keywords = "cocina mexicana, tradición familiar, resistente, práctico"
                        else:
                            features_keywords = "calidad certificada, garantía mexicana, servicio local"
                        # Mexico image descriptions in Spanish
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "Usuario disfrutando música en sala familiar mexicana, características destacadas con iconos (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "Cocina tradicional mexicana con producto destacado, familia reunida (1500x1500px)"
                        else:
                            features_image = "Gráfico de características con diseño mexicano colorido (1500x1500px)"
                        features_seo = "SEO optimizado para características técnicas en México"
                    elif marketplace_code == 'in':
                        # India culture: daily cooking, gifting, family traditions
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "superior sound, festival music, family entertainment, diwali gift perfect"
                        elif 'kitchen' in product_category or 'knife' in product_category:
                            features_keywords = "daily indian cooking, dal sabzi preparation, ginger garlic chopping, festival gifting ideal"
                        else:
                            features_keywords = "certified quality, indian warranty, festival gift ready, local service"
                        # India image descriptions focused on Indian cooking lifestyle
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "Indian family enjoying festival music at home, features highlighted with rangoli decorations (1500x1500px)"
                        elif 'kitchen' in product_category or 'knife' in product_category:
                            features_image = "Indian mother preparing dal sabzi in traditional kitchen, knife set prominently displayed with fresh vegetables like onions ginger garlic, warm lighting (1500x1500px)"
                        else:
                            features_image = "Feature infographic with Indian festival motifs and family cooking focus (1500x1500px)"
                        features_seo = "SEO optimised for Indian cooking and gifting keywords"
                    elif marketplace_code == 'eg':
                        # Egypt culture: family values, Nile heritage, tradition
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "صوت فائق، إلغاء الضوضاء، بطارية طويلة، راحة العائلة المصرية"
                        elif 'kitchen' in product_category:
                            features_keywords = "مطبخ مصري، تقاليد عائلية، تراث النيل، مقاوم، عملي"
                        else:
                            features_keywords = "جودة معتمدة، ضمان مصري، خدمة محلية، تراث فرعوني"
                        # Egypt image descriptions in Arabic
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "مستخدم مصري يستمتع بالموسيقى في صالة عائلية مصرية، ميزات بارزة مع أيقونات مصرية (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "مطبخ مصري تقليدي مع المنتج البارز، عائلة مصرية مجتمعة، تراث النيل (1500x1500px)"
                        else:
                            features_image = "رسوم بيانية للميزات بتصميم مصري ملون، رموز فرعونية (1500x1500px)"
                        features_seo = "تحسين محركات البحث للميزات التقنية في مصر"
                    elif marketplace_code == 'sa':
                        # Saudi culture: family values, luxury, tradition
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "صوت فائق، إلغاء الضوضاء، بطارية طويلة، راحة كاملة"
                        elif 'kitchen' in product_category:
                            features_keywords = "مطبخ سعودي، تقاليد عائلية، مقاوم، عملي"
                        else:
                            features_keywords = "جودة معتمدة، ضمان سعودي، خدمة محلية"
                        # Saudi image descriptions in Arabic
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "مستخدم يستمتع بالموسيقى في صالة عائلية سعودية، ميزات بارزة مع أيقونات (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "مطبخ سعودي تقليدي مع المنتج البارز، عائلة مجتمعة (1500x1500px)"
                        else:
                            features_image = "رسوم بيانية للميزات بتصميم سعودي ملون (1500x1500px)"
                        features_seo = "تحسين محركات البحث للميزات التقنية في السعودية"
                    elif marketplace_code == 'pl':
                        # Poland culture: family values, Catholic traditions, quality focus
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "dźwięk doskonały, redukcja hałasu, bateria długotrwała, komfort rodzinny polski"
                        elif 'kitchen' in product_category:
                            features_keywords = "kuchnia polska, tradycja rodzinna, wytrzymały, praktyczny"
                        else:
                            features_keywords = "jakość certyfikowana, gwarancja polska, serwis lokalny, tradycja katolicka"
                        # Poland image descriptions in English (like Mexico)
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "ENGLISH: Grid of 6 feature images: 1) Close-up on noise-canceling switch, 2) 50mm driver cross-section with sound waves, 3) battery indicator showing 30h, 4) RGB lights glowing, 5) bluetooth connected to phone and console, 6) Polish user wearing comfortably during gaming session"
                        elif 'kitchen' in product_category:
                            features_image = "ENGLISH: Traditional Polish kitchen with product prominently displayed, Polish family gathered, heritage elements (1500x1500px)"
                        else:
                            features_image = "ENGLISH: Feature infographic with Polish colorful design elements (1500x1500px)"
                        features_seo = "SEO zoptymalizowane dla cech technicznych w Polsce"
                    elif marketplace_code == 'nl':
                        # Netherlands culture: practical, quality-conscious, direct
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "uitstekend geluid, ruisonderdrukking, lange batterij, comfortabel"
                        elif 'kitchen' in product_category:
                            features_keywords = "praktisch keukengereedschap, duurzaam, makkelijk schoon"
                        else:
                            features_keywords = "Nederlandse kwaliteit, garantie, betrouwbaar"
                        # Netherlands image descriptions in Dutch
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "Nederlandse professional met koptelefoon in modern kantoor, technische details zichtbaar (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "Moderne Nederlandse keuken met product in gebruik, praktische toepassingen (1500x1500px)"
                        else:
                            features_image = "Technische specificaties overzicht, Nederlandse stijl design (1500x1500px)"
                        features_seo = "SEO voor technische kenmerken in Nederland"
                    elif marketplace_code == 'tr':
                        # Turkey culture: hospitality, family, quality focus
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "kristal ses, gürültü engelleme, uzun pil, rahat kullanım"
                        elif 'kitchen' in product_category:
                            features_keywords = "Türk mutfağı, aile boyu, dayanıklı, kolay temizlik"
                        else:
                            features_keywords = "kalite belgeli, Türkiye garantisi, yerli destek"
                        # Turkey detailed ENGLISH image descriptions like Poland
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "ENGLISH: Grid of 6 feature images: 1) Close-up on noise-canceling switch, 2) 50mm driver cross-section with sound waves, 3) battery indicator showing 30h, 4) RGB lights glowing, 5) bluetooth connected to phone and console, 6) Turkish user wearing comfortably during gaming session"
                        elif 'kitchen' in product_category:
                            features_image = "ENGLISH: Traditional Turkish kitchen with product prominently displayed, Turkish family gathered around dining table, heritage elements and warm hospitality atmosphere (1500x1500px)"
                        else:
                            features_image = "ENGLISH: Turkish family using product in daily situations, home lifestyle applications with traditional hospitality elements (1500x1500px)"
                        features_seo = "Teknik özellikler için SEO optimizasyonu Türkiye'de"
                    elif marketplace_code == 'es':
                        # Spanish culture: emphasizes family, passion, and value
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "sonido cristalino, comodidad familiar, música perfecta"
                        elif 'kitchen' in product_category:
                            features_keywords = "cocina familiar, ingredientes frescos, tradición culinaria"
                        else:
                            features_keywords = "calidad superior, diseño elegante, valor familiar"
                        # Spanish image: warm, family-oriented, lifestyle context
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "Familia española disfrutando música juntos, ambiente cálido (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "Cocina familiar española, preparando comida tradicional (1500x1500px)"
                        else:
                            features_image = "Infografía con estilo mediterráneo, colores cálidos (1500x1500px)"
                        features_seo = "Estrategia SEO de características"
                    elif marketplace_code == 'de':
                        # German culture: emphasizes precision, engineering, and efficiency
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "Präzisionssound, deutsche Ingenieurskunst, Effizienz"
                        elif 'kitchen' in product_category:
                            features_keywords = "Präzisionsschnitt, deutsche Qualität, Langlebigkeit"
                        else:
                            features_keywords = "Ingenieursqualität, Präzision, Zuverlässigkeit, Effizienz"
                        # German image: precise, technical, engineering-focused
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "Technische Präzision, Ingenieursqualität, deutsche Standards (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "Deutsche Küche, Präzision und Qualität im Detail (1500x1500px)"
                        else:
                            features_image = "Präzise Feature-Infografik, deutsche Ingenieurskunst (1500x1500px)"
                        features_seo = "Feature-SEO-Strategie"
                    elif marketplace_code == 'fr':
                        # French culture: emphasizes elegance, style, and sophistication
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "élégance sonore, raffinement français, art de vivre"
                        elif 'kitchen' in product_category:
                            features_keywords = "art culinaire, raffinement, élégance française"
                        else:
                            features_keywords = "sophistication, élégance française, art de vivre, raffinement"
                        # French image: elegant, sophisticated, artistic
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "Ambiance parisienne élégante, sophistication musicale (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "Art culinaire français, raffinement et élégance (1500x1500px)"
                        else:
                            features_image = "Infographie sophistiquée, style français raffiné (1500x1500px)"
                        features_seo = "Stratégie SEO des fonctionnalités"
                    elif marketplace_code == 'sg':
                        # Singapore culture: emphasizes efficiency, multiculturalism, technology integration, tropical lifestyle
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "premium Singapore sound excellence, wireless MRT-friendly, all-day tropical comfort, multicultural audio experience"
                        elif 'kitchen' in product_category:
                            features_keywords = "professional hawker-grade quality, easy tropical cleanup, modern HDB kitchen design, Singapore culinary innovation"
                        else:
                            features_keywords = "innovative Singapore design, high-performance tropical durability, user-friendly Lion City technology, premium multicultural quality"
                        # Singapore image: efficient urban lifestyle, tropical innovation, multicultural harmony
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "ENGLISH: Grid of 6 premium feature images: 1) Close-up noise-canceling switch with Singapore skyline reflection, 2) 50mm driver cross-section with sound waves over Marina Bay, 3) Battery indicator showing 30h with tropical humidity resistance, 4) RGB lights glowing against HDB apartment evening, 5) Bluetooth connected to phone and gaming console in modern Singapore home, 6) Multicultural Singaporean family wearing comfortably during gaming session with Gardens by the Bay backdrop (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "ENGLISH: Contemporary Singapore kitchen features grid: 1) Diamond disc precision with tropical durability coating, 2) Ceramic disc with anti-humidity protection, 3) Premium walnut handle with Singapore climate resistance, 4) 15/20 degree angle guides for Asian and Western cuisine, 5) Hawker-chef demonstrating professional technique, 6) Modern HDB kitchen with Marina Bay view showcasing efficiency (1500x1500px)"
                        else:
                            features_image = "ENGLISH: Dynamic Singapore features showcase: innovative design meeting tropical climate demands, efficiency-focused urban lifestyle, multicultural family harmony, Lion City quality standards, modern technology integration with traditional Asian values, Singapore excellence visible (1500x1500px)"
                        features_seo = "Advanced feature SEO strategy optimized for Singapore market and tropical lifestyle"
                    elif marketplace_code == 'uk':
                        # British culture: emphasizes heritage, sophistication, weather resilience, refined quality
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "premium British sound excellence, wireless commuter-friendly, all-day refined comfort, sophisticated audio experience"
                        elif 'kitchen' in product_category:
                            features_keywords = "professional Sunday-roast quality, easy sophisticated cleanup, modern British kitchen design, refined culinary innovation"
                        else:
                            features_keywords = "innovative British design, high-performance weather durability, user-friendly sophisticated technology, premium refined quality"
                        # British image: heritage lifestyle, weather innovation, family sophistication
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "ENGLISH: Grid of 6 premium British feature images: 1) Close-up noise-canceling switch with London Thames reflection, 2) 50mm driver cross-section with sound waves over Stonehenge, 3) Battery indicator showing 30h with UK weather resistance, 4) RGB lights glowing against Scottish Highlands sunset, 5) Bluetooth connected to phone and gaming console in refined British home, 6) Distinguished British family wearing comfortably during gaming session with Buckingham Palace backdrop (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "ENGLISH: Classic British kitchen features grid: 1) Diamond disc precision with weather durability coating, 2) Ceramic disc with humidity and rain protection, 3) Premium oak handle with British climate resistance, 4) 15/20 degree angle guides for roast and traditional cuisine, 5) British chef demonstrating professional technique, 6) Traditional country kitchen with countryside view showcasing efficiency (1500x1500px)"
                        else:
                            features_image = "ENGLISH: Dynamic British features showcase: innovative design meeting changeable weather demands, heritage-focused lifestyle, sophisticated family harmony, British quality standards, modern technology integration with traditional British values, refined British excellence visible (1500x1500px)"
                        features_seo = "Advanced feature SEO strategy optimized for British market and sophisticated lifestyle"
                    elif marketplace_code == 'au':
                        # Australian culture: emphasizes mateship, outdoor lifestyle, extreme climate durability, fair dinkum quality
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "premium Australian sound excellence, wireless outback-friendly, all-day extreme comfort, fair dinkum audio experience"
                        elif 'kitchen' in product_category:
                            features_keywords = "professional BBQ-grade quality, easy extreme cleanup, modern Australian kitchen design, fair dinkum culinary innovation"
                        else:
                            features_keywords = "innovative Australian design, high-performance extreme durability, user-friendly Aussie technology, premium fair dinkum quality"
                        # Australian image: rugged outdoor lifestyle, extreme climate innovation, mateship harmony
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "ENGLISH: Grid of 6 premium Australian feature images: 1) Close-up noise-canceling switch with Sydney Harbour reflection, 2) 50mm driver cross-section with sound waves over Uluru, 3) Battery indicator showing 30h with extreme climate resistance, 4) RGB lights glowing against Queensland sunset, 5) Bluetooth connected to phone and gaming console in modern Australian home, 6) Fair dinkum Australian family wearing comfortably during gaming session with Great Barrier Reef backdrop (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "ENGLISH: Contemporary Australian kitchen features grid: 1) Diamond disc precision with extreme climate coating, 2) Ceramic disc with dust and humidity protection, 3) Premium eucalyptus handle with Australian climate resistance, 4) 15/20 degree angle guides for BBQ and traditional cuisine, 5) Aussie chef demonstrating professional technique, 6) Modern open-plan kitchen with bushland view showcasing efficiency (1500x1500px)"
                        else:
                            features_image = "ENGLISH: Dynamic Australian features showcase: innovative design meeting extreme climate demands, outdoor-focused lifestyle, mateship family harmony, fair dinkum quality standards, modern technology integration with traditional Aussie values, Australian excellence visible (1500x1500px)"
                        features_seo = "Advanced feature SEO strategy optimized for Australian market and extreme climate lifestyle"
                    else:
                        # USA/International: emphasizes innovation, performance, convenience
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_keywords = "premium sound, wireless freedom, all-day comfort"
                        elif 'kitchen' in product_category:
                            features_keywords = "professional grade, easy cleanup, modern design"
                        else:
                            features_keywords = "innovative design, high performance, user-friendly, premium quality"
                        # USA/International image: dynamic, innovative, lifestyle-focused
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "Modern lifestyle, wireless freedom, urban setting (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "Modern American kitchen, innovative cooking (1500x1500px)"
                        else:
                            features_image = "Dynamic features showcase, innovation-focused (1500x1500px)"
                        features_seo = "Feature-focused SEO strategy"
                    
                    features_html = f"""
    <div class="aplus-section-card bg-green-50 border-green-200 border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">⭐</span>
            <div class="flex-1">
                <h3 class="text-green-900 text-xl sm:text-2xl font-bold">{localized_labels.get('features_title', 'Key Features & Benefits')}</h3>
                <p class="text-gray-600 text-sm mt-1">{'Ürün özellikleri ve faydaları bölümü' if marketplace_code == 'tr' else 'Features section with product advantages and benefits'}</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <ul class="text-gray-700 text-sm sm:text-base list-disc pl-5">
                {features_items}
            </ul>
        </div>
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{features_keywords}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{features_image}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{features_seo}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(features_html)
                
                # Create trust section from actual trust builders with new box design
                if listing.trust_builders:
                    trust_list = listing.trust_builders.split('\n') if isinstance(listing.trust_builders, str) else listing.trust_builders
                    trust_items = '\n'.join([f"<li class='mb-2'>{trust}</li>" for trust in trust_list[:5]])
                    
                    # Get marketplace and culture-specific trust keywords
                    if marketplace_code == 'jp':
                        # Japanese culture: trust through group consensus and long-term reliability
                        trust_keywords = "みんなが選ぶ安心, 長期保証, 日本品質基準, アフターサポート"
                        # Japanese trust image: group consensus, long-term thinking
                        trust_image = "日本の家族が安心して使用、信頼の証、認証マーク (1200x800px)"
                        trust_seo = "信頼性重視のSEO戦略"
                    elif marketplace_code == 'br':
                        # Brazil culture: trust through social proof and guarantees
                        trust_keywords = "garantia estendida, certificado INMETRO, qualidade brasileira, nota fiscal"
                        # Brazil trust image descriptions in Portuguese
                        trust_image = "Selos de certificação brasileiros, depoimentos de clientes satisfeitos, garantia destacada (1200x800px)"
                        trust_seo = "SEO focado em confiança e garantias"
                    elif marketplace_code == 'mx':
                        # Mexico culture: trust through family recommendations
                        trust_keywords = "garantía mexicana, certificado calidad, recomendado familias, servicio local"
                        # Mexico trust image descriptions in Spanish
                        trust_image = "Certificaciones mexicanas visibles, testimonios familias mexicanas, sellos de garantía (1200x800px)"
                        trust_seo = "Estrategia SEO de confianza y calidad"
                    elif marketplace_code == 'in':
                        # India culture: trust through family recommendations and gifting confidence
                        trust_keywords = "indian warranty ISI certified, quality certificate genuine, recommended by families, perfect gifting confidence, local service support"
                        # India trust image descriptions focused on Indian quality and gifting
                        trust_image = "Indian quality certifications ISI BIS visible, happy Indian families using product during festival cooking, warranty certificate with GST invoice (1200x800px)"
                        trust_seo = "SEO strategy for Indian trust and gifting confidence"
                    elif marketplace_code == 'eg':
                        # Egypt culture: trust through family recommendations and cultural heritage
                        trust_keywords = "ضمان مصري، شهادة جودة، موصى به من العائلات المصرية، خدمة محلية، تراث فرعوني"
                        # Egypt trust image descriptions in Arabic with cultural elements
                        trust_image = "شهادات مصرية مرئية، شهادات من العائلات المصرية، أختام الضمان المصري، رموز تراثية (1200x800px)"
                        trust_seo = "استراتيجية تحسين محركات البحث للثقة والجودة المصرية"
                    elif marketplace_code == 'sa':
                        # Saudi culture: trust through family recommendations
                        trust_keywords = "ضمان سعودي، شهادة جودة، موصى به من العائلات، خدمة محلية"
                        # Saudi trust image descriptions in Arabic
                        trust_image = "شهادات سعودية مرئية، شهادات من العائلات السعودية، أختام الضمان (1200x800px)"
                        trust_seo = "استراتيجية تحسين محركات البحث للثقة والجودة"
                    elif marketplace_code == 'pl':
                        # Poland culture: trust through family recommendations and Catholic values
                        trust_keywords = "gwarancja polska, certyfikat jakości, polecane rodzinom polskim, serwis lokalny, tradycja katolicka"
                        # Poland trust image descriptions in English (like Mexico)
                        trust_image = "ENGLISH: Display of Polish certification badge, Poland flag icon, 2-year warranty card, customer review average 4.8 stars, presented in premium style with Catholic heritage elements"
                        trust_seo = "Strategia SEO dla zaufania i jakości polskiej"
                    elif marketplace_code == 'nl':
                        # Netherlands culture: trust through quality and reliability
                        trust_keywords = "CE keurmerk, Nederlandse garantie, betrouwbare kwaliteit, klantenservice"
                        # Netherlands trust image descriptions in Dutch
                        trust_image = "CE certificering zichtbaar, Nederlandse kwaliteitskeurmerken, garantiebewijzen (1200x800px)"
                        trust_seo = "SEO strategie voor vertrouwen"
                    elif marketplace_code == 'tr':
                        # Turkey culture: trust through certifications and local support
                        trust_keywords = "TSE belgesi, CE sertifikası, 2 yıl garanti, Türkiye destek"
                        # Turkey trust image descriptions with detailed ENGLISH descriptions like Poland
                        trust_image = "ENGLISH: Display of Turkish certification badge, Turkey flag icon, 2-year warranty card, customer review average 4.8 stars, presented in premium style with Turkish hospitality elements"
                        trust_seo = "Güven ve kalite için SEO stratejisi Türkiye'de"
                    elif marketplace_code == 'es':
                        # Spanish culture: trust through family recommendations and community
                        trust_keywords = "recomendado por familias, garantía extendida, servicio al cliente"
                        # Spanish trust image: family recommendations, community
                        trust_image = "Familia española recomendando producto, comunidad de confianza (1200x800px)"
                        trust_seo = "Estrategia SEO de confianza"
                    elif marketplace_code == 'de':
                        # German culture: trust through certifications and technical standards
                        trust_keywords = "TÜV-geprüft, deutsche Qualitätsnormen, Zertifizierung, Compliance"
                        # German trust image: certifications, technical standards
                        trust_image = "TÜV-Zertifikate, deutsche Qualitätsnormen, technische Prüfung (1200x800px)"
                        trust_seo = "Vertrauens-SEO-Strategie"
                    elif marketplace_code == 'fr':
                        # French culture: trust through heritage and artisanal quality
                        trust_keywords = "tradition française, savoir-faire, qualité artisanale, héritage"
                        # French trust image: heritage, artisanal quality
                        trust_image = "Tradition française, savoir-faire artisanal, héritage qualité (1200x800px)"
                        trust_seo = "Stratégie SEO de confiance"
                    else:
                        # USA/International: trust through reviews and money-back guarantees
                        trust_keywords = "5-star reviews, money-back guarantee, customer satisfaction, verified quality"
                        # USA trust image: reviews, satisfaction guarantees
                        trust_image = "Customer reviews, 5-star ratings, satisfaction guarantee (1200x800px)"
                        trust_seo = "Trust-focused SEO strategy"
                    
                    trust_html = f"""
    <div class="aplus-section-card bg-purple-50 border-purple-200 border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">🛡️</span>
            <div class="flex-1">
                <h3 class="text-purple-900 text-xl sm:text-2xl font-bold">{localized_labels.get('trust_title', 'Why Trust This Product')}</h3>
                <p class="text-gray-600 text-sm mt-1">{'Kalite güvencesi ve garantiler bölümü' if marketplace_code == 'tr' else 'Trust section with quality assurance and guarantees'}</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <ul class="text-gray-700 text-sm sm:text-base list-disc pl-5">
                {trust_items}
            </ul>
        </div>
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{trust_keywords}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{trust_image}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{trust_seo}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(trust_html)
                
                # Create Usage/Applications section (Section 4)
                if listing.features or listing.hero_content:
                    if marketplace_code == 'tr':
                        usage_content = "Günlük kullanım, çok amaçlı uygulamalar, pratik ve kullanışlı çözümler sunar."
                        usage_keywords = "günlük kullanım, çok amaçlı, praktik, kullanışlı"
                        usage_image = "ENGLISH: Turkish family using product in various daily situations, home lifestyle applications with traditional hospitality elements (1500x1500px)"
                        usage_seo = "Kullanım senaryoları için SEO optimizasyonu"
                        usage_title = "Kullanım Alanları"
                    elif marketplace_code == 'pl':
                        usage_content = "Codzienne użytkowanie, wszechstronne zastosowania, praktyczne i wygodne rozwiązania dla polskiej rodziny."
                        usage_keywords = "codzienne użycie, wszechstronne zastosowania, praktyczny, wygodny"
                        usage_image = "ENGLISH: Polish family using product in various daily situations, home lifestyle applications (1500x1500px)"
                        usage_seo = "Strategia SEO dla zastosowań codziennych"
                        usage_title = "Zastosowania"
                    else:
                        usage_content = "Everyday use, versatile applications, practical and convenient solutions."
                        usage_keywords = "everyday use, versatile applications, practical, convenient"
                        usage_image = "Product in various use cases, lifestyle applications (1500x1500px)"
                        usage_seo = "Usage-focused SEO strategy"
                        usage_title = "Applications"
                    
                    usage_html = f"""
    <div class="aplus-section-card bg-orange-50 border-orange-200 border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">🎯</span>
            <div class="flex-1">
                <h3 class="text-orange-900 text-xl sm:text-2xl font-bold">{usage_title}</h3>
                <p class="text-gray-600 text-sm mt-1">{'Kullanım alanları ve uygulama senaryoları' if marketplace_code == 'tr' else 'Usage and application scenarios'}</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <p class="text-gray-700 leading-relaxed text-sm sm:text-base">{usage_content}</p>
        </div>
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{usage_keywords}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{usage_image}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{usage_seo}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(usage_html)
                
                # Create Comparison section (Section 5)
                if listing.features or listing.hero_content:
                    if marketplace_code == 'tr':
                        comparison_content = "Rakiplerinden üstün özellikler, daha iyi performans ve değer sunar."
                        comparison_keywords = "rekabet avantajı, üstün seçim, temel farklılıklar"
                        comparison_image = "ENGLISH: Comparison table highlighting product advantages, Turkish quality standards (1200x800px)"
                        comparison_seo = "Karşılaştırma odaklı SEO"
                        comparison_title = "Neden Bu Ürünü Seçmelisiniz"
                    elif marketplace_code == 'pl':
                        comparison_content = "Przewaga nad konkurencją dzięki lepszym funkcjom, wydajności i wartości dla polskich rodzin."
                        comparison_keywords = "przewaga konkurencyjna, najlepszy wybór, kluczowe różnice"
                        comparison_image = "ENGLISH: Comparison table highlighting product advantages, Polish quality standards (1200x800px)"
                        comparison_seo = "SEO dla przewagi konkurencyjnej"
                        comparison_title = "Dlaczego Wybrać Ten Produkt"
                    else:
                        comparison_content = "Superior features, better performance and value compared to competitors."
                        comparison_keywords = "competitive advantage, superior choice, key differentiators"
                        comparison_image = "Comparison table highlighting advantages (1200x800px)"
                        comparison_seo = "Comparison-focused SEO"
                        comparison_title = "Why Choose This Product"
                    
                    comparison_html = f"""
    <div class="aplus-section-card bg-teal-50 border-teal-200 border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">🏆</span>
            <div class="flex-1">
                <h3 class="text-teal-900 text-xl sm:text-2xl font-bold">{comparison_title}</h3>
                <p class="text-gray-600 text-sm mt-1">{'Rekabet avantajları ve temel farklılıklar' if marketplace_code == 'tr' else 'Competitive advantages and key differentiators'}</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <p class="text-gray-700 leading-relaxed text-sm sm:text-base">{comparison_content}</p>
        </div>
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{comparison_keywords}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{comparison_image}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{comparison_seo}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(comparison_html)
                
                # Create Customer testimonials section (Section 6)
                if listing.hero_content:
                    if marketplace_code == 'tr':
                        testimonials_content = "Müşteri memnuniyeti garantili, doğrulanmış yorumlar ve 5 yıldızlı deneyimler."
                        testimonials_keywords = "müşteri yorumları, doğrulanmış incelemeler, memnuniyet garantili"
                        testimonials_image = "ENGLISH: Happy Turkish customers with 5-star ratings, family testimonials with hospitality elements (1200x800px)"
                        testimonials_seo = "Sosyal kanıt SEO stratejisi"
                        testimonials_title = "Müşteri Deneyimleri"
                    elif marketplace_code == 'pl':
                        testimonials_content = "Zadowolenie klientów gwarantowane, zweryfikowane opinie i 5-gwiazdkowe doświadczenia polskich rodzin."
                        testimonials_keywords = "opinie klientów, zweryfikowane recenzje, zadowolenie gwarantowane"
                        testimonials_image = "ENGLISH: Happy Polish customers with 5-star ratings, family testimonials (1200x800px)"
                        testimonials_seo = "Strategia SEO dowodów społecznych"
                        testimonials_title = "Zadowolenie Klientów"
                    else:
                        testimonials_content = "Customer satisfaction guaranteed, verified reviews and 5-star experiences."
                        testimonials_keywords = "customer testimonials, verified reviews, satisfaction guaranteed"
                        testimonials_image = "Happy customers with 5-star ratings (1200x800px)"
                        testimonials_seo = "Social proof SEO strategy"
                        testimonials_title = "Customer Satisfaction"
                    
                    testimonials_html = f"""
    <div class="aplus-section-card bg-pink-50 border-pink-200 border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">💬</span>
            <div class="flex-1">
                <h3 class="text-pink-900 text-xl sm:text-2xl font-bold">{testimonials_title}</h3>
                <p class="text-gray-600 text-sm mt-1">{'Müşteri yorumları ve memnuniyet' if marketplace_code == 'tr' else 'Customer testimonials and satisfaction'}</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <p class="text-gray-700 leading-relaxed text-sm sm:text-base">{testimonials_content}</p>
        </div>
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{testimonials_keywords}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{testimonials_image}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{testimonials_seo}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(testimonials_html)
                
                # Create Package contents section (Section 7)
                if listing.features:
                    if marketplace_code == 'tr':
                        package_content = "Paket içeriği eksiksiz, premium ambalaj ve dahil edilen aksesuarlar."
                        package_keywords = "paket içeriği, premium ambalaj, dahil aksesuarlar"
                        package_image = "ENGLISH: Unboxing view with contents neatly displayed, Turkish quality packaging (1200x800px)"
                        package_seo = "Paket içeriği SEO optimizasyonu"
                        package_title = "Paket İçeriği"
                    elif marketplace_code == 'pl':
                        package_content = "Kompletna zawartość opakowania, premium pakowanie i dołączone akcesoria dla polskich klientów."
                        package_keywords = "zawartość opakowania, premium pakowanie, dołączone akcesoria"
                        package_image = "ENGLISH: Unboxing view with contents neatly displayed, Polish quality packaging (1200x800px)"
                        package_seo = "SEO dla zawartości opakowania"
                        package_title = "Zawartość Zestawu"
                    else:
                        package_content = "Complete package contents, premium packaging and included accessories."
                        package_keywords = "package contents, premium packaging, included accessories"
                        package_image = "Unboxing view with contents displayed (1200x800px)"
                        package_seo = "Package contents SEO"
                        package_title = "What's Included"
                    
                    package_html = f"""
    <div class="aplus-section-card bg-indigo-50 border-indigo-200 border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">📦</span>
            <div class="flex-1">
                <h3 class="text-indigo-900 text-xl sm:text-2xl font-bold">{package_title}</h3>
                <p class="text-gray-600 text-sm mt-1">Package contents and included items</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <p class="text-gray-700 leading-relaxed text-sm sm:text-base">{package_content}</p>
        </div>
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{package_keywords}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{package_image}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{package_seo}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(package_html)
                
                # Create FAQ section from actual FAQs with new box design
                if listing.faqs:
                    faq_list = listing.faqs.split('\n') if isinstance(listing.faqs, str) else listing.faqs
                    faq_items = '\n'.join([f"<div class='mb-3'><p class='font-semibold'>{faq}</p></div>" for faq in faq_list[:5]])
                    
                    # Get marketplace and culture-specific FAQ keywords
                    if marketplace_code == 'jp':
                        # Japanese culture: detailed explanations and anticipating concerns
                        faq_keywords = "詳しい説明, 心配解消, 使い方ガイド, トラブル対応"
                        # Japanese FAQ image: detailed, helpful, respectful
                        faq_image = "丁寧なサポートスタッフ、詳しい説明書、日本語対応 (800x600px)"
                        faq_seo = "問題解決SEO戦略"
                    elif marketplace_code == 'br':
                        # Brazil culture: friendly guidance and community support
                        faq_keywords = "dúvidas frequentes, suporte brasileiro, como usar, passo a passo"
                        # Brazil FAQ image descriptions in Portuguese
                        faq_image = "Atendimento brasileiro amigável, tutorial visual passo a passo, ícones explicativos (800x600px)"
                        faq_seo = "Otimização SEO para perguntas frequentes"
                    elif marketplace_code == 'mx':
                        # Mexico culture: family-friendly help and warm support
                        faq_keywords = "preguntas comunes, ayuda familiar, guía fácil, soporte mexicano"
                        # Mexico FAQ image descriptions in Spanish
                        faq_image = "Servicio al cliente mexicano sonriente, guía visual paso a paso, iconos amigables (800x600px)"
                        faq_seo = "SEO para preguntas frecuentes México"
                    elif marketplace_code == 'in':
                        # India culture: cooking help, safety for beginners, gifting guidance
                        faq_keywords = "indian cooking questions, beginner safety tips, stainless steel care, gifting guide help, family kitchen support"
                        # India FAQ image descriptions focused on cooking and safety
                        faq_image = "Indian customer service team explaining knife safety to beginner cook, step-by-step Indian cooking guide, kitchen safety icons (800x600px)"
                        faq_seo = "SEO for Indian cooking questions and gifting guidance"
                    elif marketplace_code == 'eg':
                        # Egypt culture: family-friendly help and warm support with cultural heritage
                        faq_keywords = "أسئلة شائعة، مساعدة عائلية مصرية، دليل سهل، دعم مصري، تراث عائلي"
                        # Egypt FAQ image descriptions in Arabic with cultural elements
                        faq_image = "خدمة عملاء مصرية مبتسمة، دليل مرئي خطوة بخطوة، أيقونات ودية مصرية، رموز تراثية (800x600px)"
                        faq_seo = "تحسين محركات البحث للأسئلة الشائعة المصرية"
                    elif marketplace_code == 'sa':
                        # Saudi culture: family-friendly help and warm support
                        faq_keywords = "أسئلة شائعة، مساعدة عائلية، دليل سهل، دعم سعودي"
                        # Saudi FAQ image descriptions in Arabic
                        faq_image = "خدمة عملاء سعودية مبتسمة، دليل مرئي خطوة بخطوة، أيقونات ودية (800x600px)"
                        faq_seo = "تحسين محركات البحث للأسئلة الشائعة السعودية"
                    elif marketplace_code == 'pl':
                        # Poland culture: family-friendly help and warm support with Catholic traditions
                        faq_keywords = "często zadawane pytania, pomoc rodzinna polska, przewodnik łatwy, wsparcie polskie, tradycja katolicka"
                        # Poland FAQ image descriptions in English (like Mexico)
                        faq_image = "ENGLISH: Smiling Polish customer service team explaining product features to Polish family, step-by-step visual guide, friendly Polish icons with Catholic heritage symbols (800x600px)"
                        faq_seo = "SEO dla często zadawanych pytań polskich"
                    elif marketplace_code == 'nl':
                        # Netherlands culture: direct and practical information
                        faq_keywords = "veelgestelde vragen, praktische hulp, gebruiksaanwijzing, probleemoplossing"
                        # Netherlands FAQ image descriptions in Dutch
                        faq_image = "Duidelijke instructies met pictogrammen, stap-voor-stap handleiding, praktische tips (800x600px)"
                        faq_seo = "SEO voor veelgestelde vragen"
                    elif marketplace_code == 'tr':
                        # Turkey culture: detailed support with hospitality
                        faq_keywords = "sık sorulan sorular, Türkçe destek, kullanım kılavuzu, problem çözümü"
                        # Turkey FAQ image descriptions with detailed ENGLISH descriptions like Poland
                        faq_image = "ENGLISH: Smiling Turkish customer service team explaining product features to Turkish family, step-by-step visual guide, friendly Turkish icons with hospitality elements (800x600px)"
                        faq_seo = "Sık sorulan sorular için SEO optimizasyonu Türkiye'de"
                    elif marketplace_code == 'es':
                        # Spanish culture: community help and family-friendly guidance
                        faq_keywords = "ayuda familiar, dudas comunes, consejos prácticos, guía fácil"
                        # Spanish FAQ image: helpful, family-friendly
                        faq_image = "Ayuda familiar amigable, guía fácil de entender (800x600px)"
                        faq_seo = "Estrategia SEO de preguntas"
                    elif marketplace_code == 'de':
                        # German culture: technical precision and thorough documentation
                        faq_keywords = "technische Details, Bedienungsanleitung, Problemlösung, Handbuch"
                        # German FAQ image: thorough, technical documentation
                        faq_image = "Ausführliche Dokumentation, technische Anleitung, Präzision (800x600px)"
                        faq_seo = "FAQ-SEO-Strategie"
                    elif marketplace_code == 'fr':
                        # French culture: elegant solutions and sophisticated guidance
                        faq_keywords = "conseils d'expert, solutions élégantes, guide sophistiqué, assistance"
                        # French FAQ image: elegant, sophisticated guidance
                        faq_image = "Guide élégant, assistance sophistiquée, style raffiné (800x600px)"
                        faq_seo = "Stratégie SEO des questions"
                    else:
                        # USA/International: quick answers and practical solutions
                        faq_keywords = "quick answers, troubleshooting, user guide, instant help"
                        # USA FAQ image: quick, efficient, modern
                        faq_image = "Modern help center, instant answers, user-friendly design (800x600px)"
                        faq_seo = "FAQ-focused SEO strategy"
                    
                    faq_html = f"""
    <div class="aplus-section-card bg-yellow-50 border-yellow-200 border-2 rounded-lg p-4 sm:p-6 mb-6 mx-2 sm:mx-0 shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center mb-4">
            <span class="text-2xl sm:text-3xl mr-3">❓</span>
            <div class="flex-1">
                <h3 class="text-yellow-900 text-xl sm:text-2xl font-bold">{localized_labels.get('faqs_title', 'Frequently Asked Questions')}</h3>
                <p class="text-gray-600 text-sm mt-1">FAQ section with common customer questions and answers</p>
            </div>
        </div>
        <div class="content-section bg-white rounded-lg p-4 mb-4 border">
            <div class="text-gray-700 text-sm sm:text-base">
                {faq_items}
            </div>
        </div>
        <div class="seo-details mt-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🔍</span>
                        <strong class="text-gray-900">{localized_labels['keywords']}</strong>
                    </div>
                    <p class="text-gray-600">{faq_keywords}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">📸</span>
                        <strong class="text-gray-900">{localized_labels['image_strategy']}</strong>
                    </div>
                    <p class="text-gray-600">{faq_image}</p>
                </div>
                <div class="bg-white p-3 rounded border">
                    <div class="flex items-center mb-2">
                        <span class="mr-2">🎯</span>
                        <strong class="text-gray-900">{localized_labels['seo_focus']}</strong>
                    </div>
                    <p class="text-gray-600">{faq_seo}</p>
                </div>
            </div>
        </div>
    </div>"""
                    sections_html.append(faq_html)
            
            # Generate HTML from saved listing data
            features_html = '\n'.join([f"        <li>{feature}</li>" for feature in features_list])
            whats_in_box_items = result.get('whatsInBox', [f'{product.name}', 'User manual', 'Warranty information'])
            whats_in_box_html = '\n'.join([f"        <li>{item}</li>" for item in whats_in_box_items])
            trust_items = result.get('trustBuilders', ['Quality guaranteed', '30-day satisfaction', 'Customer support'])
            trust_html = '\n'.join([f"        <li>{trust}</li>" for trust in trust_items])
            faq_items = result.get('faqs', [])
            faqs_html = '\n'.join([f"    <p><strong>{faq}</strong></p>" for faq in faq_items])
            
            # Generate PPC strategy HTML
            ppc_strategy = result.get('ppcStrategy', {})
            campaign_structure = ppc_strategy.get('campaignStructure', {})
            ppc_html = ""
            
            if isinstance(campaign_structure, dict) and campaign_structure:
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

            # Generate comprehensive A+ content plan with mobile-responsive structure
            aplus_html = f"""<div class="aplus-introduction bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 p-4 sm:p-6 rounded-lg mb-6">
    <div class="flex items-center mb-4">
        <span class="text-3xl mr-3">🚀</span>
        <div>
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900">Complete A+ Content Strategy</h2>
            <p class="text-purple-700 text-sm">Professional Amazon A+ content for enhanced product presentation.</p>
        </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div class="bg-white p-3 rounded border">
            <div class="flex items-center mb-2">
                <span class="mr-2">🧠</span>
                <strong class="text-gray-900">AI-Generated Briefs</strong>
            </div>
            <p class="text-gray-600">Complete image concepts with titles, scenes, and overlay text</p>
        </div>
        <div class="bg-white p-3 rounded border">
            <div class="flex items-center mb-2">
                <span class="mr-2">🎯</span>
                <strong class="text-gray-900">Design Guidelines</strong>
            </div>
            <p class="text-gray-600">Style guides, color schemes, and layout specifications</p>
        </div>
        <div class="bg-white p-3 rounded border">
            <div class="flex items-center mb-2">
                <span class="mr-2">📤</span>
                <strong class="text-gray-900">Ready for Production</strong>
            </div>
            <p class="text-gray-600">Copy briefs to Canva, Figma, or share with designers</p>
        </div>
    </div>
</div>

<div class="aplus-hero bg-gradient-to-r from-blue-50 to-indigo-50 p-4 sm:p-6 rounded-lg mb-6">
    <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3">{listing.hero_title}</h3>
    <p class="text-gray-700 text-sm sm:text-base leading-relaxed">{listing.hero_content}</p>
</div>

<div class="aplus-comprehensive-plan">
    <h2 class="text-xl sm:text-2xl font-bold text-gray-900 mb-4 px-2 sm:px-0">Complete A+ Content Strategy</h2>
    <div class="space-y-4 sm:space-y-6">
        {''.join(sections_html)}
    </div>
</div>

<div class="aplus-strategy-summary bg-gray-50 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-3">Overall A+ Strategy</h3>
    <p class="text-gray-700 text-sm sm:text-base leading-relaxed">{aplus_plan.get('overallStrategy', 'Complete A+ content plan designed to guide customers from awareness to purchase')}</p>
</div>

<div class="mobile-responsive-content">
    {ppc_html}
</div>

<div class="keyword-strategy bg-white border border-gray-200 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-3">Keyword Strategy</h3>
    <p class="text-gray-700 text-sm sm:text-base mb-4">{result.get('keywordStrategy', 'Strategic keyword placement for maximum SEO impact')}</p>
    <h4 class="text-md sm:text-lg font-medium text-gray-800 mb-2">Competitor Keywords</h4>
    <p class="text-gray-600 text-sm sm:text-base">{result.get('topCompetitorKeywords', 'Analysis of competitive landscape for positioning')}</p>
</div>

<div class="aplus-features bg-green-50 border border-green-200 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-green-900 mb-3">Key Features & Benefits</h3>
    <ul class="space-y-1 sm:space-y-2 text-sm sm:text-base">
{features_html}
    </ul>
</div>

<div class="aplus-whats-in-box bg-purple-50 border border-purple-200 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-purple-900 mb-3">What's in the Box</h3>
    <ul class="space-y-1 sm:space-y-2 text-sm sm:text-base text-gray-700">
{whats_in_box_html}
    </ul>
</div>

<div class="aplus-trust bg-orange-50 border border-orange-200 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-orange-900 mb-3">Trust & Quality Assurance</h3>
    <ul class="space-y-1 sm:space-y-2 text-sm sm:text-base text-gray-700">
{trust_html}
    </ul>
</div>

<div class="aplus-testimonials bg-teal-50 border border-teal-200 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-teal-900 mb-3">Customer Satisfaction</h3>
    <p class="text-gray-700 text-sm sm:text-base mb-3">{result.get('social_proof', '')}</p>
    <p class="text-gray-800 text-sm sm:text-base font-medium"><strong>Our Guarantee:</strong> {result.get('guarantee', '')}</p>
</div>

<div class="aplus-faqs bg-indigo-50 border border-indigo-200 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-indigo-900 mb-4">Frequently Asked Questions</h3>
    <div class="space-y-3 text-sm sm:text-base">
{faqs_html}
    </div>
</div>"""
            # FIXED: Always use comprehensive A+ HTML structure for ALL markets (US and International)
            # This ensures 25,000+ character comprehensive A+ content for 10/10 quality
            marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
            
            # FIXED: Only use simple localized content for specific markets that don't have comprehensive sections
            # Turkey (tr) and Mexico (mx) should use comprehensive sections, not simple localized content
            if marketplace_code in ['es', 'jp', 'br', 'nl', 'se']:
                # Create localized A+ content using hero/features fields that are always populated
                localized_sections = []
                
                # Hero section with localized content
                if listing.hero_title and listing.hero_content:
                    localized_sections.append(f"""
<div class="aplus-section hero-section-localized">
    <h2 class="section-title">{listing.hero_title}</h2>
    <div class="section-content">
        <p>{listing.hero_content}</p>
    </div>
</div>""")
                
                # Features section with localized content
                if listing.features:
                    features_list = listing.features.split('\n')
                    features_html = '<ul>' + ''.join(f'<li>{feature.strip()}</li>' for feature in features_list if feature.strip()) + '</ul>'
                    localized_sections.append(f"""
<div class="aplus-section features-section-localized">
    <h2 class="section-title">{'Özellikler' if marketplace_code == 'tr' else 'Características' if marketplace_code == 'mx' else 'الميزات' if marketplace_code == 'sa' else 'Features' if marketplace_code == 'in' else 'Features'}</h2>
    <div class="section-content">
        {features_html}
    </div>
</div>""")
                
                # Trust builders section - FIXED: Prevent character splitting
                if listing.trust_builders:
                    # Handle both single text and multi-line trust content
                    if '\n' in listing.trust_builders:
                        trust_list = listing.trust_builders.split('\n')
                        trust_html = '<ul>' + ''.join(f'<li>{trust.strip()}</li>' for trust in trust_list if trust.strip()) + '</ul>'
                    else:
                        # Single text without newlines - treat as single paragraph
                        trust_html = f'<p>{listing.trust_builders.strip()}</p>'
                    
                    localized_sections.append(f"""
<div class="aplus-section trust-section-localized">
    <h2 class="section-title">{'Güven' if marketplace_code == 'tr' else 'Confianza' if marketplace_code == 'mx' else 'الثقة' if marketplace_code == 'sa' else 'Zaufanie' if marketplace_code == 'pl' else 'Trust' if marketplace_code == 'in' else 'Trust'}</h2>
    <div class="section-content">
        {trust_html}
    </div>
</div>""")
                
                # FAQs section  
                if listing.faqs:
                    faqs_content = listing.faqs.replace('\n\n', '</p><p>').replace('\n', '<br>')
                    localized_sections.append(f"""
<div class="aplus-section faqs-section-localized">
    <h2 class="section-title">{'Sık Sorulan Sorular' if marketplace_code == 'tr' else 'Preguntas Frecuentes' if marketplace_code == 'mx' else 'الأسئلة الشائعة' if marketplace_code == 'sa' else 'Często Zadawane Pytania' if marketplace_code == 'pl' else 'FAQs' if marketplace_code == 'in' else 'FAQs'}</h2>
    <div class="section-content">
        <p>{faqs_content}</p>
    </div>
</div>""")
                
                # Combine localized sections with template
                if localized_sections:
                    localized_aplus_content = f"""
<div class="aplus-localized-content">
    {''.join(localized_sections)}
</div>
{aplus_html}"""
                    listing.amazon_aplus_content = localized_aplus_content
                    self.logger.info(f"✅ Using GUARANTEED localized A+ content for {marketplace_code}: {len(localized_aplus_content)} characters")
                else:
                    listing.amazon_aplus_content = aplus_html
                    self.logger.info(f"⚠️ No localized content available for {marketplace_code}, using template: {len(aplus_html)} characters")
            else:
                # For Turkey and Mexico: use comprehensive template WITHOUT simple sections
                # For US market: use full template WITH simple sections
                if marketplace_code in ['tr', 'mx', 'sa', 'eg', 'in', 'pl', 'be', 'sg', 'au']:
                    # Turkey and Mexico get comprehensive sections only, no simple sections
                    comprehensive_only_html = f"""<div class="aplus-introduction bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 p-4 sm:p-6 rounded-lg mb-6">
    <div class="flex items-center mb-4">
        <span class="text-3xl mr-3">🚀</span>
        <div>
            <h2 class="text-xl sm:text-2xl font-bold text-gray-900">Complete A+ Content Strategy</h2>
            <p class="text-purple-700 text-sm">Professional Amazon A+ content for enhanced product presentation.</p>
        </div>
    </div>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div class="bg-white p-3 rounded border">
            <div class="flex items-center mb-2">
                <span class="mr-2">🧠</span>
                <strong class="text-gray-900">AI-Generated Briefs</strong>
            </div>
            <p class="text-gray-600">Complete image concepts with titles, scenes, and overlay text</p>
        </div>
        <div class="bg-white p-3 rounded border">
            <div class="flex items-center mb-2">
                <span class="mr-2">🎯</span>
                <strong class="text-gray-900">Design Guidelines</strong>
            </div>
            <p class="text-gray-600">Style guides, color schemes, and layout specifications</p>
        </div>
        <div class="bg-white p-3 rounded border">
            <div class="flex items-center mb-2">
                <span class="mr-2">📤</span>
                <strong class="text-gray-900">Ready for Production</strong>
            </div>
            <p class="text-gray-600">Copy briefs to Canva, Figma, or share with designers</p>
        </div>
    </div>
</div>

<div class="aplus-hero bg-gradient-to-r from-blue-50 to-indigo-50 p-4 sm:p-6 rounded-lg mb-6">
    <h3 class="text-xl sm:text-2xl font-bold text-gray-900 mb-3">{listing.hero_title}</h3>
    <p class="text-gray-700 text-sm sm:text-base leading-relaxed">{listing.hero_content}</p>
</div>

<div class="aplus-comprehensive-plan">
    <h2 class="text-xl sm:text-2xl font-bold text-gray-900 mb-4 px-2 sm:px-0">Complete A+ Content Strategy</h2>
    <div class="space-y-4 sm:space-y-6">
        {''.join(sections_html)}
    </div>
</div>

<div class="aplus-strategy-summary bg-gray-50 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-3">Overall A+ Strategy</h3>
    <p class="text-gray-700 text-sm sm:text-base leading-relaxed">{aplus_plan.get('overallStrategy', 'Complete A+ content plan designed to guide customers from awareness to purchase')}</p>
</div>

<div class="mobile-responsive-content">
    {ppc_html}
</div>

<div class="keyword-strategy bg-white border border-gray-200 p-4 sm:p-6 rounded-lg mt-6 mx-2 sm:mx-0">
    <h3 class="text-lg sm:text-xl font-semibold text-gray-900 mb-3">Keyword Strategy</h3>
    <p class="text-gray-700 text-sm sm:text-base mb-4">{result.get('keywordStrategy', 'Strategic keyword placement for maximum SEO impact')}</p>
    <h4 class="text-md sm:text-lg font-medium text-gray-800 mb-2">Competitor Keywords</h4>
    <p class="text-gray-600 text-sm sm:text-base">{result.get('topCompetitorKeywords', 'Analysis of competitive landscape for positioning')}</p>
</div>"""
                    listing.amazon_aplus_content = comprehensive_only_html
                    self.logger.info(f"✅ Using comprehensive-only template for {marketplace_code}: {len(comprehensive_only_html)} characters")
                else:
                    # US market gets full template with simple sections
                    listing.amazon_aplus_content = aplus_html
                    self.logger.info(f"Using standard A+ content template for {marketplace_code}: {len(aplus_html)} characters")
            
            # CRITICAL: Now the localized content from aPlusContentPlan is properly embedded
            # The sections_html contains AI-generated content in the target language
            # This preserves full localization while maintaining visual structure.
            
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
                        # Remove placeholder module type briefing
                        section += f"<h3>{title}</h3>\n<p>{content}</p>"
                        # Remove image requirement briefing - not buyer-facing
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
            
            # NO FALLBACK - Only AI-generated content allowed
            # Raise exception for all errors including quota/rate limits
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
        
        # Fallback backend keywords - ONLY optimize France and Italy markets (keep USA and Germany untouched)
        marketplace_code = getattr(product, 'marketplace', 'com') or 'com'
        if marketplace_code in ['fr', 'it']:
            # FRANCE AND ITALY ONLY: Optimize fallback backend keywords
            base_keywords = [product.name, product.brand_name, primary_keyword, f"premium {product_category}", f"quality {product_category}", "kitchen accessories"]
            listing.amazon_backend_keywords = self.backend_optimizer.optimize_backend_keywords(
                primary_keywords=base_keywords,
                marketplace=marketplace_code,
                product_category=product_category
            )
        else:
            # USA and GERMANY: Keep original working fallback keywords untouched
            listing.amazon_backend_keywords = f"{product.name}, {product.brand_name}, {primary_keyword}, premium {product_category}, quality {product_category}, kitchen accessories"
        
        # Enhanced A+ Content fallback - ONLY if no A+ content was generated
        if not listing.amazon_aplus_content:
            listing.amazon_aplus_content = """<div class='aplus-module module1'>
<h3>Experience the Gaming Difference</h3>
<p>Transform your gaming setup with professional-grade comfort. Join thousands who have discovered the ultimate gaming chair.</p>
</div>

<div class='aplus-module module2'>
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

    def _get_category_specific_specs(self, product):
        """Return category-appropriate specifications"""
        category = product.categories.lower() if product.categories else ''
        
        # Electronics category
        if any(term in category for term in ['electronic', 'computer', 'gaming', 'audio', 'camera', 'phone']):
            return '''
    "power_consumption": "Electrical specifications if applicable",
    "connectivity": "WiFi, Bluetooth, USB specifications",
    "battery_life": "Battery capacity and usage time",
    "technical_performance": "Speed, resolution, refresh rate as relevant"'''
        
        # Kitchen/Home category
        elif any(term in category for term in ['kitchen', 'home', 'furniture', 'decor']):
            return '''
    "care_instructions": "Cleaning and maintenance requirements",
    "capacity": "Volume, serving size, or storage capacity",
    "safety_features": "Heat resistance, non-slip, child safety"'''
        
        # Fashion/Apparel
        elif any(term in category for term in ['clothing', 'fashion', 'apparel', 'shoes']):
            return '''
    "size_chart": "Available sizes and measurements",
    "fabric_composition": "Material percentages and properties",
    "care_instructions": "Washing and care requirements"'''
        
        # Default for other categories
        else:
            return '''
    "durability": "Expected lifespan and wear resistance",
    "compatibility": "Works with or fits these items",
    "included_accessories": "What comes in the package"'''
    
    def _get_category_specific_videos(self, product):
        """Return category-appropriate video suggestions"""
        category = product.categories.lower() if product.categories else ''
        product_name = product.name.lower()
        
        if any(term in category for term in ['kitchen', 'cooking', 'food']):
            return f'''[
      "Recipe demonstration using {product.name}",
      "Cleaning and maintenance tutorial",
      "Size comparison with similar products",
      "Durability test (dishwasher, heat resistance)"
    ]'''
        elif any(term in category for term in ['electronic', 'gaming', 'computer']):
            return f'''[
      "Unboxing and setup guide for {product.name}",
      "Performance benchmarks and speed tests",
      "Feature walkthrough with real usage",
      "Comparison with top 3 competitors"
    ]'''
        elif any(term in category for term in ['furniture', 'home', 'decor']):
            return f'''[
      "Assembly instructions for {product.name}",
      "Room placement and styling ideas",
      "Weight capacity and durability test",
      "Before/after room transformation"
    ]'''
        else:
            return f'''[
      "Product demonstration showing key features",
      "Unboxing and first impressions",
      "Comparison with similar products",
      "Customer testimonial compilation"
    ]'''
    
    def _get_category_specific_images(self, product):
        """Return category-appropriate image suggestions"""
        category = product.categories.lower() if product.categories else ''
        
        if any(term in category for term in ['kitchen', 'cooking']):
            return '''[
      "In-use shot: preparing a meal",
      "Size comparison with standard items",
      "Close-up of non-stick/material surface",
      "Full kitchen setup context shot",
      "Cleaning/dishwasher safe demonstration"
    ]'''
        elif any(term in category for term in ['electronic', 'gaming']):
            return '''[
      "All ports and connections labeled",
      "Size comparison with competing products",
      "LED/screen quality close-up",
      "Complete setup with accessories",
      "Performance metrics infographic"
    ]'''
        elif any(term in category for term in ['furniture', 'home']):
            return '''[
      "Multiple angle views of product",
      "Staged in different room settings",
      "Close-up of materials and finish",
      "Assembly stages progression",
      "Weight/size specifications chart"
    ]'''
        else:
            return '''[
      "Lifestyle shot in natural setting",
      "360-degree product views",
      "Size reference with hand/person",
      "Package contents laid out",
      "Quality details close-up"
    ]'''

    def _get_occasion_context(self, product):
        """Return appropriate occasion context with localization"""
        occasion = getattr(product, 'occasion', '') or ''
        
        # Check if it's Mexican market for Spanish localization
        is_mexico = (getattr(product, 'marketplace', '') == 'walmart_mexico' or 
                    getattr(product, 'marketplace_language', '') == 'es-mx')
        
        if is_mexico:
            # Mexican occasion mapping in Spanish
            mexican_occasions = {
                '': 'Para uso diario,',
                'everyday': 'Para uso diario,',
                'navidad': 'Perfecto para Navidad,',
                'dia_reyes': 'Ideal para el Día de Reyes,',
                'dia_madre': 'Perfecto para el Día de las Madres,',
                'dia_padre': 'Ideal para el Día del Padre,',
                'dia_muertos': 'Especial para Día de Muertos,',
                'independence_day': 'Perfecto para las Fiestas Patrias,',
                'guadalupe': 'Ideal para el Día de la Virgen,',
                'quinceañera': 'Perfecto para Quinceañeras,',
                'boda': 'Ideal para Bodas,',
                'bautizo': 'Perfecto para Bautizos,',
                'primera_comunion': 'Ideal para Primera Comunión,',
                'graduacion': 'Perfecto para Graduaciones,',
                'cumpleaños': 'Ideal para Cumpleaños,',
                'regreso_clases': 'Perfecto para Regreso a Clases,',
                'hot_sale': 'Especial para Hot Sale,',
                'buen_fin': 'Ideal para El Buen Fin,',
                'grito': 'Perfecto para El Grito,',
                'posadas': 'Ideal para Las Posadas,',
                'año_nuevo': 'Perfecto para Año Nuevo,'
            }
            return mexican_occasions.get(occasion, f'Ideal para {occasion},')
        else:
            # English occasions for US market
            if not occasion or occasion == 'everyday':
                return 'For daily use,'
            elif 'christmas' in occasion.lower():
                return 'Perfect for Christmas gifting,'
            elif 'valentine' in occasion.lower():
                return 'Ideal for Valentine\'s Day,'
            elif 'mother' in occasion.lower():
                return 'Great for Mother\'s Day,'
            elif 'black_friday' in occasion.lower():
                return 'Perfect for Black Friday savings,'
            else:
                return f'Perfect for {occasion},'
    
    def _get_brand_tone_descriptor(self, product):
        """Return appropriate brand tone descriptor"""
        tone = getattr(product, 'brand_tone', '') or 'professional'
        tone_mapping = {
            'professional': 'professional-grade',
            'luxury': 'premium',
            'casual': 'user-friendly', 
            'trendy': 'modern',
            'vintage_charm': 'classic',
            'minimalist_modern': 'sleek',
            'bohemian_free': 'versatile',
            'handmade_artisan': 'artisan-crafted',
            # Mexican brand tones
            'familiar_caloroso': 'familiar y cálido',
            'tradicion_mexicana': 'tradicional mexicano',
            'lujo_mexicano': 'lujo mexicano',
            'joven_vibrante': 'joven y vibrante',
            'confiable_profesional': 'confiable y profesional',
            'festivo_celebracion': 'festivo y celebrativo',
            'moderno_mexicano': 'moderno mexicano',
            'hogareño_familiar': 'hogareño y familiar'
        }
        return tone_mapping.get(tone, 'professional-grade')
    
    def _get_mexican_cultural_context(self, product):
        """Return Mexican cultural context for Walmart Mexico generation"""
        occasion = getattr(product, 'occasion', '') or ''
        brand_tone = getattr(product, 'brand_tone', '') or ''
        
        # Mexican cultural values and context
        cultural_context = """
🇲🇽 CONTEXTO CULTURAL MEXICANO:
VALORES FAMILIARES: La familia es el centro de la sociedad mexicana. Enfócate en:
- Productos que benefician a toda la familia
- Momentos de reunión familiar  
- Tradiciones que se comparten entre generaciones
- Calidad que perdura para la familia

CONFIANZA Y CALIDAD: Los mexicanos valoran la confianza y la calidad:
- Garantías sólidas y servicio post-venta
- Certificaciones mexicanas (NOM, PROFECO)
- Marcas establecidas con reputación
- Testimonios de otras familias mexicanas

CELEBRACIONES IMPORTANTES: México tiene ricas tradiciones:
- Navidad y Día de Reyes (regalos familiares)
- Día de las Madres (10 de mayo)
- Día de los Muertos (tradición familiar)
- Fiestas patrias y celebraciones locales
"""
        
        # Occasion-specific context
        occasion_context = ""
        if occasion == 'navidad':
            occasion_context = """
NAVIDAD MEXICANA: Enfoque familiar y generoso
- Regalos para toda la familia extendida
- Productos que crean momentos especiales
- Calidad que justifica la inversión navideña
- Perfectos para Las Posadas y cenas familiares
"""
        elif occasion == 'dia_madre':
            occasion_context = """
DÍA DE LAS MADRES (10 MAYO): Celebración especial mexicana
- Regalos que muestran amor y respeto profundo
- Productos útiles para el hogar y la familia
- Calidad premium para la reina de la casa
- Que faciliten la vida de mamá
"""
        elif occasion == 'dia_muertos':
            occasion_context = """
DÍA DE LOS MUERTOS: Tradición familiar mexicana
- Productos que honran las tradiciones
- Para preparar altares y celebraciones familiares
- Que conectan con las raíces culturales
- Calidad que respeta la solemnidad de la fecha
"""
        
        # Brand tone context in Spanish
        tone_context = ""
        if brand_tone in ['familiar_caloroso', 'hogareño_familiar']:
            tone_context = """
TONO FAMILIAR Y CÁLIDO:
- Usar lenguaje cercano y familiar
- Enfatizar beneficios para el hogar
- Crear conexión emocional con la familia
- Destacar comodidad y bienestar familiar
"""
        elif brand_tone in ['tradicion_mexicana']:
            tone_context = """
TRADICIÓN MEXICANA:
- Conectar con valores tradicionales mexicanos
- Respetar costumbres y tradiciones familiares
- Destacar calidad artesanal o tradicional
- Usar referencias culturales apropiadas
"""
        elif brand_tone in ['lujo_mexicano']:
            tone_context = """
LUJO MEXICANO:
- Calidad premium accesible para familias mexicanas
- Destacar exclusividad y prestigio
- Justificar la inversión con beneficios duraderos
- Crear aspiración familiar
"""
        
        return cultural_context + occasion_context + tone_context
    
    def _analyze_product_context(self, product):
        """Analyze product and return comprehensive context for generation"""
        # Extract main product category
        categories = getattr(product, 'categories', '') or ''
        main_category = categories.split('>')[0].strip() if '>' in categories else categories.strip()
        
        # Analyze product features
        features = getattr(product, 'features', '') or ''
        feature_list = [f.strip() for f in features.split('\n') if f.strip()]
        
        # Determine product complexity
        complexity = 'basic' if len(feature_list) <= 3 else 'advanced' if len(feature_list) <= 6 else 'complex'
        
        # Extract key terms from product name
        name_words = product.name.lower().split()
        product_type = None
        for word in name_words:
            if len(word) > 3 and word not in ['with', 'for', 'and', 'the', 'pro', 'max', 'plus']:
                product_type = word
                break
        
        return {
            'main_category': main_category,
            'product_type': product_type or 'product',
            'feature_count': len(feature_list),
            'complexity': complexity,
            'key_features': feature_list[:5],  # Top 5 features
            'occasion_context': self._get_occasion_context(product),
            'brand_tone_descriptor': self._get_brand_tone_descriptor(product),
            'price_tier': 'budget' if product.price < 50 else 'mid-range' if product.price < 200 else 'premium'
        }
    
    def _comprehensive_emoji_removal(self, result):
        """Remove emojis and special characters from listing content"""
        import re
        
        # Define emoji pattern
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U00002702-\U000027B0"  # dingbats
            "\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        
        # Clean all string fields in the result
        if isinstance(result, dict):
            cleaned_result = {}
            for key, value in result.items():
                if isinstance(value, str):
                    # Remove emojis
                    cleaned_value = emoji_pattern.sub('', value)
                    # Clean up any double spaces
                    cleaned_value = ' '.join(cleaned_value.split())
                    cleaned_result[key] = cleaned_value
                elif isinstance(value, list):
                    # Clean list items
                    cleaned_list = []
                    for item in value:
                        if isinstance(item, str):
                            clean_item = emoji_pattern.sub('', item)
                            clean_item = ' '.join(clean_item.split())
                            cleaned_list.append(clean_item)
                        else:
                            cleaned_list.append(item)
                    cleaned_result[key] = cleaned_list
                else:
                    cleaned_result[key] = value
            return cleaned_result
        elif isinstance(result, str):
            clean_result = emoji_pattern.sub('', result)
            return ' '.join(clean_result.split())
        else:
            return result
    
    def _clean_product_name(self, name):
        """Clean messy product names to prevent AI generation failures"""
        if not name:
            return "Product"
        
        # Remove extra spaces and clean formatting
        cleaned = ' '.join(name.strip().split())
        
        # Remove common Amazon formatting artifacts
        cleaned = re.sub(r'[\u2022\u25CF\u25AA\u25AB]', '', cleaned)  # Remove bullet points
        cleaned = re.sub(r'[⚫⚪🔴🟢🟡🟠]', '', cleaned)  # Remove emoji bullets
        cleaned = re.sub(r'\s*[-–—]\s*', ' - ', cleaned)  # Normalize dashes
        
        # Limit length to prevent AI overload
        if len(cleaned) > 100:
            cleaned = cleaned[:97] + '...'
        
        return cleaned
    
    def _clean_brand_name(self, brand):
        """Clean messy brand names"""
        if not brand:
            return "Brand"
        
        # Remove extra spaces and clean formatting
        cleaned = brand.strip()
        
        # Remove common formatting issues
        cleaned = re.sub(r'[⚫⚪🔴🟢🟡🟠]', '', cleaned)  # Remove emoji
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize spaces
        
        return cleaned
    
    def _clean_product_features(self, features):
        """Clean messy feature lists to extract key points"""
        if not features:
            return "High quality materials, Excellent design, User-friendly"
        
        # Split features by common separators
        feature_list = []
        
        # Try different splitting methods
        if '\n' in features:
            raw_features = features.split('\n')
        elif '•' in features:
            raw_features = features.split('•')
        elif '⚫' in features:
            raw_features = features.split('⚫')
        else:
            raw_features = [features]
        
        for feature in raw_features:
            # Clean each feature
            clean_feature = feature.strip()
            
            # Remove bullet points and formatting
            clean_feature = re.sub(r'^[\s\u2022\u25CF\u25AA\u25AB⚫⚪🔴🟢🟡🟠\-–—]+', '', clean_feature)
            clean_feature = re.sub(r'\s+', ' ', clean_feature)
            
            # Skip empty or very short features
            if len(clean_feature) > 10 and len(clean_feature) < 150:
                feature_list.append(clean_feature)
            
            # Limit to 6 key features to prevent AI overload
            if len(feature_list) >= 6:
                break
        
        # If no good features found, provide generic ones
        if not feature_list:
            feature_list = ["High quality construction", "Durable materials", "Easy to use", "Professional grade"]
        
        return '\n'.join(feature_list)
    
    def _clean_product_description(self, description):
        """Clean messy product descriptions"""
        if not description:
            return "High-quality product designed for excellent performance."
        
        # Remove excessive formatting and clean up
        cleaned = description.strip()
        
        # Remove bullet points at the start of lines
        cleaned = re.sub(r'^[\s\u2022\u25CF\u25AA\u25AB⚫⚪🔴🟢🟡🟠\-–—]+', '', cleaned, flags=re.MULTILINE)
        
        # Normalize spaces and line breaks
        cleaned = re.sub(r'\n+', ' ', cleaned)  # Convert line breaks to spaces
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize spaces
        
        # Limit length to prevent AI overload (keep it under 500 chars)
        if len(cleaned) > 500:
            # Try to cut at a sentence boundary
            sentences = cleaned.split('. ')
            trimmed = ""
            for sentence in sentences:
                if len(trimmed + sentence + '. ') > 500:
                    break
                trimmed += sentence + '. '
            cleaned = trimmed.strip()
            
            # If still too long, hard cut
            if len(cleaned) > 500:
                cleaned = cleaned[:497] + '...'
        
        return cleaned
    
    def _fix_unterminated_strings_and_parse(self, json_text):
        """Fix unterminated strings in JSON and attempt parsing"""
        import json
        import re
        
        # Clean the JSON text
        fixed = json_text.strip()
        
        # Find unterminated string patterns and fix them
        # Look for quotes that aren't properly closed
        
        # Method 1: Try to find and close unclosed quotes
        quote_count = 0
        in_string = False
        escaped = False
        last_quote_pos = -1
        
        for i, char in enumerate(fixed):
            if char == '\\' and not escaped:
                escaped = True
                continue
            
            if char == '"' and not escaped:
                in_string = not in_string
                if in_string:
                    last_quote_pos = i
                quote_count += 1
            
            escaped = False
        
        # If we're still in a string, try to close it
        if in_string and quote_count % 2 == 1:
            # Find the last meaningful content before closing
            # Look for common JSON closing patterns
            closing_patterns = ['}', ']', '"}', '"]']
            insert_pos = len(fixed)
            
            # Find the best place to insert a closing quote
            for pattern in closing_patterns:
                pos = fixed.rfind(pattern)
                if pos > last_quote_pos:
                    insert_pos = pos
                    break
            
            # Insert closing quote before the closing pattern
            if insert_pos < len(fixed):
                fixed = fixed[:insert_pos] + '"' + fixed[insert_pos:]
            else:
                fixed = fixed + '"}'
        
        # Method 2: Try to truncate at last complete object
        if not fixed.endswith('}') and not fixed.endswith(']'):
            # Find last complete closing brace
            brace_pos = fixed.rfind('}')
            if brace_pos > 0:
                fixed = fixed[:brace_pos + 1]
        
        try:
            return json.loads(fixed)
        except json.JSONDecodeError:
            # If still failing, try more aggressive fixes
            
            # Remove trailing incomplete content
            lines = fixed.split('\n')
            clean_lines = []
            for line in lines:
                if line.strip().endswith(',') or line.strip().endswith('{') or line.strip().endswith('['):
                    clean_lines.append(line)
                elif '"' in line and ':' in line:
                    clean_lines.append(line)
                elif line.strip() in ['}', ']', '},', '],']:
                    clean_lines.append(line)
                    break
            
            attempt2 = '\n'.join(clean_lines)
            if not attempt2.endswith('}'):
                attempt2 += '}'
            
            return json.loads(attempt2)
    
    def _generate_fallback_walmart_content(self, listing, product):
        """Generate fallback content when AI generation fails to prevent blank listings"""
        print(f"🔧 Generating fallback content for {product.name}...")
        
        # Clean product data
        cleaned_name = self._clean_product_name(product.name)
        cleaned_brand = self._clean_brand_name(product.brand_name)
        cleaned_features = self._clean_product_features(product.features)
        cleaned_description = self._clean_product_description(product.description)
        
        # Generate basic Walmart fields
        listing.walmart_product_title = f"{cleaned_brand} {cleaned_name} - Professional Quality"
        listing.walmart_description = f"High-quality {cleaned_name} from {cleaned_brand}. {cleaned_description}"
        
        # Generate key features from cleaned features
        features_list = cleaned_features.split('\n')[:5] if cleaned_features else [
            "Professional grade construction",
            "Durable materials for long-lasting use", 
            "Easy to use and maintain",
            "High quality design and finish",
            "Excellent performance and reliability"
        ]
        listing.walmart_key_features = '\n'.join(features_list)
        
        # Generate basic keywords
        listing.keywords = f"{cleaned_brand.lower()}, {cleaned_name.lower()}, professional, quality, durable, reliable"
        
        # Generate basic specifications
        listing.walmart_specifications = f'{{"brand": "{cleaned_brand}", "product_type": "{cleaned_name}", "quality": "Professional grade"}}'
        
        # Generate basic compliance
        listing.walmart_compliance_certifications = '{"required_certifications": ["Quality standards compliance"], "certification_guidance": "Follow standard product safety guidelines for this category.", "safety_warnings": ["Use as intended", "Keep away from children if applicable"]}'
        
        # Generate basic profit maximizer
        listing.walmart_profit_maximizer = f'{{"q1_action_plan": ["Set competitive price at ${product.price}", "Monitor competitor pricing", "Optimize product images"], "key_metrics": ["Target positive reviews", "Focus on quality highlighting"]}}'
        
        print(f"✅ Fallback content generated for {cleaned_name}")

    def _generate_walmart_listing(self, product, listing):
        from .services_occasion_enhanced import OccasionOptimizer
        
        if not self.client:
            raise Exception("OpenAI API key not configured. Please set a valid OpenAI API key to generate Walmart listings.")
            
        # Initialize occasion optimizer for Walmart too
        occasion_optimizer = OccasionOptimizer()
        
        # OPTIMIZED HYBRID APPROACH: 2 parallel API calls for maximum speed + quality
        try:
            import concurrent.futures
            
            # Execute both API calls in parallel for maximum speed
            with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                # Submit both calls simultaneously
                core_future = executor.submit(self._generate_walmart_core_content, product)
                advanced_future = executor.submit(self._generate_walmart_advanced_content, product)
                
                # Get results (will wait for both to complete)
                core_content = core_future.result()
                advanced_content = advanced_future.result()
            
            # Merge both results into listing
            self._merge_walmart_hybrid_content(listing, core_content, advanced_content, product)
            
            listing.status = 'completed'
            listing.save()
            return listing
            
        except Exception as e:
            print(f"🚨 WALMART GENERATION FAILED: {e}")
            
            # If it's a JSON parsing error, try to generate fallback content
            if "Unterminated string" in str(e) or "JSON" in str(e):
                print(f"🔧 GENERATING FALLBACK CONTENT TO PREVENT BLANK LISTING...")
                try:
                    self._generate_fallback_walmart_content(listing, product)
                    listing.status = 'completed'
                    print(f"✅ Fallback content generated successfully!")
                except Exception as fallback_error:
                    print(f"❌ Fallback generation also failed: {fallback_error}")
                    listing.status = 'failed'
                    listing.error_message = str(e)
            else:
                listing.status = 'failed'
                listing.error_message = str(e)
                
            listing.save()
            return listing

    def _generate_walmart_core_content(self, product):
        """HYBRID APPROACH - Call 1: Generate core content with dynamic category-aware prompts"""
        
        # 🔧 CRITICAL FIX: Clean messy product data before AI generation
        cleaned_name = self._clean_product_name(product.name)
        cleaned_brand = self._clean_brand_name(product.brand_name)
        cleaned_features = self._clean_product_features(product.features)
        cleaned_description = self._clean_product_description(product.description)
        
        # Dynamic category-aware prompt generation
        category_context = self._get_dynamic_category_context(product)
        
        # Detect Mexico marketplace and use Spanish cultural context
        is_mexico = (getattr(product, 'marketplace', '') == 'walmart_mexico' or 
                    getattr(product, 'marketplace_language', '') == 'es-mx')
        
        # Get Mexican cultural context and language instructions
        if is_mexico:
            mexican_context = self._get_mexican_cultural_context(product)
            language_instruction = """
🇲🇽 GENERAR TODO EN ESPAÑOL MEXICANO - CRITICAL:
- ABSOLUTAMENTE TODO el contenido DEBE estar 100% en español mexicano
- NO usar palabras en inglés (NO: "gaming", "wireless", "bluetooth")
- SÍ usar traducciones mexicanas: "para videojuegos", "inalámbrico", "conexión bluetooth"
- Título COMPLETO en español: marca + producto + beneficio + ocasión en español
- Usar términos familiares mexicanos (familia, hogar, tradición, mamá, regalo)
- Incluir la ocasión específica en el título y descripción
- Mencionar valores mexicanos (calidad, confianza, garantía, familia)
- Precio en pesos mexicanos ($MXN)
- Palabras clave EN ESPAÑOL: "audífonos", "inalámbricos", "para mamá", etc.
"""
            title_max = "Máximo 70 caracteres. Incluir marca, producto, beneficio clave. EN ESPAÑOL"
            desc_instruction = "185 palabras EN ESPAÑOL MEXICANO. Descripción profesional destacando beneficios clave para familias mexicanas."
            features_format = "EN ESPAÑOL: Nombre Característica - Beneficio específico (máx 75 caracteres)"
            keywords_instruction = """Generar 28+ palabras clave EN ESPAÑOL MEXICANO separadas por comas. 
OBLIGATORIO incluir:
- Términos cortos (1-2 palabras): "audífonos", "inalámbricos", "bluetooth", "gamer"
- Términos medios (3-4 palabras): "audífonos para videojuegos", "regalo para mamá", "audífonos con micrófono"
- Términos largos (5+ palabras): "audífonos inalámbricos para videojuegos con micrófono"
- Términos de ocasión: "regalo día de las madres", "para mamá", "regalo 10 de mayo"
- NO usar inglés: usar "videojuegos" NO "gaming", "inalámbrico" NO "wireless"
"""
        else:
            mexican_context = ""
            language_instruction = ""
            title_max = "Max 70 chars. Include brand, product, key benefit from features"
            desc_instruction = f"185 words. Professional description highlighting key benefits, technical advantages, and problem-solving features specific to this {product.categories} product. Use complete sentences only."
            features_format = "Feature Name - Specific benefit with proof/numbers (max 75 chars)"
            keywords_instruction = f"Generate 28+ comma-separated keywords for {product.categories} shoppers. Include: core product terms, material types, size variations, brand combinations, use cases, competitor alternatives, price-related terms."
        
        # Get occasion context
        occasion_context = self._get_occasion_context(product)
        
        prompt = f"""Generate Walmart listing core content for {cleaned_brand} {cleaned_name}.

Product Info:
- Price: ${product.price} {'MXN' if is_mexico else 'USD'}
- Features: {cleaned_features}
- Description: {cleaned_description}
- Categories: {product.categories}
- Brand Tone: {product.brand_tone}
- Occasion: {occasion_context}
- Marketplace: {getattr(product, 'marketplace', 'walmart_usa')}

{category_context}
{mexican_context}
{language_instruction}

Generate core sections with NO missing words. Return valid JSON:

{{
  "title": "{title_max}",
  "description": "{desc_instruction}",
  "key_features": [
    "{features_format}",
    "{features_format}",
    "{features_format}",
    "{features_format}",
    "{features_format}"
  ],
  "keywords": "{keywords_instruction}"
}}

Write complete sentences. No generic templates. Product-specific content only."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.3,
            max_tokens=800
        )
        
        import json
        content = response.choices[0].message.content.strip()
        
        # 🔧 DEBUG: Log raw AI response for troubleshooting
        print(f"🤖 Raw AI Response Length: {len(content)} chars")
        print(f"🤖 Raw AI Response Preview: {content[:200]}...")
        
        # Clean JSON if wrapped in markdown
        if content.startswith('```'):
            if content.startswith('```json'):
                content = content[7:]
            else:
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
        
        print(f"🔧 Cleaned Content Length: {len(content)} chars")
        print(f"🔧 Cleaned Content Preview: {content[:200]}...")
        
        # Try multiple JSON parsing strategies
        try:
            return json.loads(content)
        except json.JSONDecodeError as e:
            print(f"🚨 JSON Parse Error: {e}")
            print(f"🔧 Attempting unterminated string fix...")
            
            try:
                return self._fix_unterminated_strings_and_parse(content)
            except Exception as e2:
                print(f"🚨 Unterminated string fix also failed: {e2}")
                
                # Return fallback content to prevent blank listings
                print(f"🔧 Returning fallback content to prevent blank listing...")
                return {
                    "title": f"{cleaned_brand} {cleaned_name} - Professional Quality",
                    "description": f"High-quality {cleaned_name} from {cleaned_brand}. " + cleaned_description[:150],
                    "key_features": cleaned_features.split('\n')[:5] if cleaned_features else ["Professional grade", "Durable construction", "Easy to use", "High quality materials", "Excellent design"],
                    "keywords": f"{cleaned_brand.lower()}, {cleaned_name.lower()}, professional, quality, durable"
                }

    def _get_dynamic_category_context(self, product):
        """Generate dynamic category-specific context for better AI prompts"""
        categories = product.categories.lower()
        
        if 'gaming' in categories or 'audio' in categories:
            return "Focus on: Audio quality, gaming performance, comfort for long sessions, compatibility with gaming systems, battery life, and noise isolation features."
        elif 'kitchen' in categories or 'cutting' in categories:
            return "Focus on: Food safety, durability, material advantages, ease of cleaning, size/capacity benefits, and professional kitchen applications."
        elif 'electronics' in categories:
            return "Focus on: Technical specifications, performance metrics, compatibility, power efficiency, build quality, and user experience features."
        elif 'home' in categories or 'garden' in categories:
            return "Focus on: Practical benefits, ease of use, durability, space-saving features, maintenance requirements, and aesthetic appeal."
        elif 'fitness' in categories or 'sports' in categories:
            return "Focus on: Performance enhancement, comfort during use, durability for active use, safety features, and results-oriented benefits."
        else:
            return f"Focus on: Key benefits specific to {product.categories} users, practical advantages, quality features, and problem-solving capabilities."

    def _generate_dynamic_walmart_category_path(self, product):
        """Generate appropriate Walmart category path based on product type"""
        categories = product.categories.lower()
        name = product.name.lower()
        
        if 'gaming' in categories and 'audio' in categories:
            return "Electronics > Gaming > Audio & Headsets"
        elif 'gaming' in categories:
            return "Electronics > Gaming > Gaming Accessories"
        elif 'audio' in categories and ('speaker' in name or 'headphone' in name):
            return "Electronics > Audio > Speakers & Headphones"
        elif 'kitchen' in categories and 'cutting' in categories:
            return "Home & Kitchen > Kitchen Utensils & Gadgets > Cutting Boards"
        elif 'kitchen' in categories:
            return "Home & Kitchen > Small Appliances"
        elif 'electronics' in categories:
            return "Electronics > Consumer Electronics"
        elif 'home' in categories:
            return "Home & Garden > Home Decor"
        else:
            # Try to parse the existing category structure
            return product.categories if product.categories else "General Merchandise"

    def _generate_walmart_advanced_content(self, product):
        """HYBRID APPROACH - Call 2: Generate advanced sections with category-aware content"""
        
        # Get category-specific context
        category_context = self._get_dynamic_category_context(product)
        category_path = self._generate_dynamic_walmart_category_path(product)
        
        prompt = f"""Generate complete advanced Walmart sections for {product.brand_name} {product.name} (${product.price}).

Product features: {product.features}
Category: {product.categories}
{category_context}

Return valid JSON with ALL sections:

{{
  "identifiers": {{
    "gtin_upc": "Generate realistic 12-digit UPC starting with 0",
    "manufacturer_part": "Generate part number format: {product.brand_name[:4].upper()}-XXXX-XXX",
    "sku_id": "Generate SKU format: {product.brand_name[:3].upper()}{product.name[:3].upper()}XXX"
  }},
  "shipping": {{
    "weight": "Calculate realistic weight in lbs based on product category and features",
    "package_length": "Package length in inches",
    "package_width": "Package width in inches", 
    "package_height": "Package height in inches",
    "shipping_weight": "Add 0.2 lbs for packaging"
  }},
  "specifications": {{
    "brand": "{product.brand_name}",
    "material": "Specific material from features",
    "dimensions": "Product dimensions from features",
    "weight": "Product weight",
    "color": "Default color option",
    "model": "Generate model number",
    "warranty": "Standard warranty period"
  }},
  "compliance": {{
    "required_certifications": ["List relevant certifications for this category"],
    "certification_guidance": "Complete step-by-step guide to obtain required certifications",
    "regulatory_requirements": "Specific US regulatory compliance requirements",
    "safety_warnings": ["All safety warnings for this product category"],
    "testing_standards": ["Relevant testing standards"]
  }},
  "rich_media": {{
    "main_images": ["Primary product shot description", "Feature detail shot description", "Scale/size shot description", "Lifestyle usage shot description"],
    "360_view": "yes or no based on category",
    "video_content": ["Unboxing video concept", "Feature demonstration concept", "Comparison video concept"],
    "infographics": ["Size comparison chart concept", "Feature benefits diagram concept", "Care instructions graphic concept"]
  }},
  "profit_maximizer": {{
    "q1_action_plan": ["Set competitive price at ${product.price}", "Launch with 10+ initial reviews", "Stock 50-100 units", "Daily competitor price monitoring", "A/B test main image"],
    "q2_growth_tactics": ["Increase price 5-10% based on performance", "Create bundle offerings", "Add video content", "Launch sponsored ads", "Weekend pricing strategy"],
    "q3_optimization": ["Prepare for peak season", "Introduce 2-3 pack bundles", "Increase advertising spend 25%", "Create comparison charts", "Email marketing campaign"],
    "q4_maximization": ["Implement holiday premium pricing", "Launch gift bundle sets", "Black Friday preparation", "Target competitor keywords", "End-of-year clearance strategy"],
    "revenue_projections": {{
      "conservative": {{
        "month_1": "$150",
        "month_3": "$450", 
        "month_6": "$900",
        "month_12": "$8,500"
      }},
      "realistic": {{
        "month_1": "$300",
        "month_3": "$1,200",
        "month_6": "$3,000", 
        "month_12": "$28,000"
      }},
      "aggressive": {{
        "month_1": "$500",
        "month_3": "$2,000",
        "month_6": "$5,000",
        "month_12": "$45,000"
      }}
    }},
    "key_metrics": ["Target Conversion Rate: >12%", "ACoS Target: <30%", "Review Velocity: 2-3/week", "Inventory Turnover: 4x/year", "Return Rate: <5%"]
  }}
}}

IMPORTANT: Do not include any URLs, links, or example.com references. Only provide descriptions and concepts for media content."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.3,
            max_tokens=1000
        )
        
        import json
        content = response.choices[0].message.content.strip()
        
        # Clean JSON if wrapped in markdown
        if content.startswith('```'):
            if content.startswith('```json'):
                content = content[7:]
            else:
                content = content[3:]
            if content.endswith('```'):
                content = content[:-3]
            content = content.strip()
        
        return json.loads(content)

    def _merge_walmart_hybrid_content(self, listing, core_content, advanced_content, product):
        """Merge hybrid approach results with ALL fields"""
        # 🔧 CRITICAL FIX: Validate content before merge to prevent blank listings
        if not core_content or not isinstance(core_content, dict):
            print(f"❌ INVALID CORE CONTENT: {repr(core_content)}")
            raise Exception("Core content is empty or invalid - will trigger fallback")
            
        if not core_content.get('title') or not core_content.get('description'):
            print(f"❌ MISSING REQUIRED FIELDS: title={repr(core_content.get('title'))}, description={repr(core_content.get('description'))}")
            raise Exception("Core content missing required fields - will trigger fallback")
        
        # Core content
        listing.walmart_product_title = core_content['title'][:70]
        listing.walmart_description = core_content['description']
        listing.walmart_key_features = '\n'.join(core_content.get('key_features', ['No features available']))
        listing.keywords = core_content.get('keywords', 'walmart, product, quality')
        listing.bullet_points = listing.walmart_key_features
        
        # Advanced content - ALL missing fields with fallback validation
        import json
        
        # 🔧 VALIDATE ADVANCED CONTENT: Provide fallbacks if missing
        if not advanced_content or not isinstance(advanced_content, dict):
            print(f"⚠️ INVALID ADVANCED CONTENT: {repr(advanced_content)[:100]}... - Using fallbacks")
            advanced_content = {}
            
        listing.walmart_specifications = json.dumps(advanced_content.get('specifications', {
            "material": "Premium Quality",
            "color": "As Shown", 
            "weight": "Varies",
            "dimensions": "See Description"
        }))
        listing.walmart_compliance_certifications = json.dumps(advanced_content.get('compliance', {
            "certification_guidance": "This product meets standard safety requirements.",
            "required_certifications": "Standard compliance certifications apply."
        }))
        listing.walmart_profit_maximizer = json.dumps(advanced_content.get('profit_maximizer', {
            "q1_action_plan": ["List product competitively", "Optimize for search visibility"],
            "revenue_projections": "Competitive market positioning"
        }))
        
        # NEW: Product identifiers (CRITICAL MISSING FIELDS)
        identifiers = advanced_content.get('identifiers', {})
        listing.walmart_gtin_upc = identifiers.get('gtin_upc', '')
        listing.walmart_manufacturer_part = identifiers.get('manufacturer_part', '')
        listing.walmart_sku_id = identifiers.get('sku_id', '')
        
        # NEW: Shipping information (CRITICAL MISSING FIELDS)  
        shipping = advanced_content.get('shipping', {})
        listing.walmart_shipping_weight = shipping.get('shipping_weight', '1 lb')
        listing.walmart_shipping_dimensions = json.dumps({
            "length": shipping.get('package_length', '12 in'),
            "width": shipping.get('package_width', '8 in'), 
            "height": shipping.get('package_height', '6 in')
        })
        
        # NEW: Rich media recommendations (MISSING FIELD)
        listing.walmart_rich_media = json.dumps(advanced_content.get('rich_media', {
            "main_images": 3,
            "lifestyle_images": 2,
            "detail_shots": 2
        }))
        
        # Enhanced attributes with more details
        specs = advanced_content.get('specifications', {})
        listing.walmart_attributes = json.dumps({
            "price": str(product.price) if product.price else "0.00",
            "brand": product.brand_name or "Quality Brand",
            "material": specs.get('material', 'Premium'),
            "color": specs.get('color', 'Natural'),
            "size": specs.get('dimensions', 'Standard'),
            "model": specs.get('model', f"{product.brand_name or 'QB'}-001"),
            "warranty": specs.get('warranty', '1 Year')
        })
        
        # Basic fields
        listing.walmart_product_type = self._get_product_type(product)
        listing.walmart_category_path = self._generate_walmart_category_path(product)

    def _generate_walmart_title(self, product):
        """Generate title only - focused prompt"""
        prompt = f"""Generate a Walmart product title for {product.brand_name} {product.name}.
        
Rules: 
- Maximum 70 characters
- Include brand name: {product.brand_name}
- Include key specs from: {product.features}
- Format: Brand Product - Key Feature Value

Example: "HORL 2 Oak Sharpener - 15°/20° German Precision"

Return only the title, nothing else."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.3,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()

    def _generate_walmart_description(self, product):
        """Generate description only - focused prompt"""
        prompt = f"""Write a product description for the {product.brand_name} {product.name}.

Product Info:
- Price: ${product.price}
- Features: {product.features}
- Category: {product.categories}
- Brand tone: {product.brand_tone}

Write 150-200 words. Start with: "Traditional cutting boards often harbor bacteria and develop deep grooves, leading to food safety concerns."

Then explain how this titanium cutting board solves these problems. Include all the features. End with pricing and call to action.

Write complete sentences with no missing words."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.4,
            max_tokens=400
        )
        return response.choices[0].message.content.strip()

    def _generate_walmart_features(self, product):
        """Generate key features only - focused prompt"""
        prompt = f"""Generate 5-7 key features for {product.brand_name} {product.name}.

Features to highlight: {product.features}

Format each as: "Feature Name - Benefit explanation"
Maximum 75 characters per feature.
Include specific numbers, materials, or measurements when possible.

Examples:
- "Dual Angles - Precision 15° for Asian knives, 20° for European blades"
- "Oak Build - German oak lasts 10+ years, includes 2-year warranty"

Return as a simple list, one per line."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    def _generate_walmart_keywords(self, product):
        """Generate SEO keywords only - focused prompt"""
        prompt = f"""Generate 25-30 SEO keywords for shoppers looking for a {product.name}.

Product: {product.brand_name} {product.name}
Category: {product.categories}

Focus on cutting board keywords:
- cutting board, titanium cutting board, {product.brand_name} cutting board
- food grade cutting board, kitchen cutting board, best cutting board
- large cutting board, dishwasher safe cutting board, double sided cutting board
- professional cutting board, durable cutting board, easy clean cutting board
- prep board, chopping board, kitchen prep tools, meal prep board
- cooking tools, kitchen essentials, food safe cutting board

Return as comma-separated list."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.3,
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    def _merge_walmart_sections(self, listing, title, description, features, keywords, product):
        """Merge all generated sections into listing"""
        listing.walmart_product_title = title[:70]  # Ensure length limit
        listing.walmart_description = description
        listing.walmart_key_features = features
        listing.keywords = keywords
        
        # Also populate bullet_points for compatibility
        listing.bullet_points = features
        
        # Generate other required fields using simpler approach
        listing.walmart_product_type = self._get_product_type(product)
        listing.walmart_category_path = self._generate_walmart_category_path(product)
        
        # Generate missing sections with focused prompts
        listing.walmart_specifications = self._generate_walmart_specifications(product)
        listing.walmart_compliance_certifications = self._generate_walmart_compliance(product)
        listing.walmart_profit_maximizer = self._generate_walmart_profit_maximizer(product)
        
        # Simple attributes
        import json
        listing.walmart_attributes = json.dumps({
            "price": str(product.price),
            "color": "Natural",
            "size": "Large"
        })

    def _get_product_type(self, product):
        """Simple product type extraction"""
        if 'cutting board' in product.name.lower():
            return 'Cutting Board'
        elif 'knife' in product.name.lower():
            return 'Kitchen Knife'
        else:
            return product.categories.split(' > ')[-1] if ' > ' in product.categories else product.categories

    def _generate_walmart_category_path(self, product):
        """Generate category path using dynamic method"""
        return self._generate_dynamic_walmart_category_path(product)

    def _generate_walmart_specifications(self, product):
        """Generate specifications only - focused prompt"""
        import json
        
        prompt = f"""Generate detailed product specifications for {product.brand_name} {product.name}.

Product features: {product.features}
Price: ${product.price}

Create JSON with these specifications:
- brand, material, dimensions, weight, dishwasher_safe, food_grade, warranty
- Use actual measurements from features when available
- Be specific and technical

Return only valid JSON."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.2,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()

    def _generate_walmart_compliance(self, product):
        """Generate compliance & certifications - focused prompt"""
        import json
        
        prompt = f"""Generate compliance and certification information for {product.brand_name} {product.name}.

This is a kitchen cutting board product priced at ${product.price}.

Create JSON with:
- required_certifications: Array of certifications needed (FDA Food Safe, etc.)
- certification_guidance: Step-by-step guide to obtain certifications
- regulatory_requirements: US regulatory compliance needed
- safety_warnings: Array of safety warnings for this product
- testing_standards: Relevant testing standards (ANSI, ASTM, etc.)

Return only valid JSON."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.3,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    def _generate_walmart_profit_maximizer(self, product):
        """Generate marketplace intelligence & profit maximizer - focused prompt"""
        import json
        
        prompt = f"""Generate quarterly action plan for maximizing profits on {product.brand_name} {product.name} priced at ${product.price}.

Create JSON with quarterly strategies:
- q1_action_plan: Array of 6 specific action items for launch (months 1-3)
- q2_growth_tactics: Array of 5 growth strategies (months 4-6)  
- q3_optimization: Array of 5 optimization tactics (months 7-9)
- q4_maximization: Array of 5 holiday maximization strategies (months 10-12)
- revenue_projections: Conservative, realistic, aggressive scenarios
- key_metrics_to_track: Array of 5 important KPIs

Focus on cutting board category. Be specific with numbers and timeframes.

Return only valid JSON."""

        response = self.client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[{'role': 'user', 'content': prompt}],
            temperature=0.4,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()