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
        """Get Turkish industry-specific high-intent keywords for Turkey market"""
        category = product.categories.lower() if product.categories else ""
        
        # Industry-specific Turkish keywords by category - BEATS ALL COMPETITORS
        industry_keywords = {
            "electronics": "en iyi, orijinal, CE sertifikalı, profesyonel, premium, türkiye fırsatı, 2024, garanti, uyumlu, kablosuz, teknoloji, sınırlı stok, özel fiyat, bugün kaçırmayın, aileniz için güvenli, türk kalitesi, 10000+ mutlu müşteri",
            "audio": "gürültü engelleme, bluetooth 5.3, HiFi, gaming kulaklık, stereo, mikrofon, eller serbest, türkiye kargo, avrupa kalitesi, müzik keyfi, ses teknolojisi, profesyonel ses, ailenize değer, türkiye'nin tercihi, sınırlı süre",
            "headphones": "aktif gürültü engelleme, bluetooth 5.3, gaming kulaklık, premium stereo, ENC mikrofon, türkiye kargo 24h, uzun pil ömrü, müzik tutkunları, ses kalitesi, konfor, çocuklarınız için güvenli, türk ailesinin seçimi, acele edin",
            "home": "enerji tasarruflu, sessiz, taşınabilir, modern tasarım, kolay temizlik, kablosuz, akıllı, eco, sürdürülebilir türkiye, ev konfor, aile zamanı, misafir ağırlama, özel günler, ev sahipliği, son fırsat",
            "kitchen": "paslanmaz çelik, yapışmaz, bulaşık makinesi uyumlu, BPA içermez, ısı dayanıklı, profesyonel mutfak, türkiye kargo, aile sofrası, mutfak keyfi, lezzet garantisi, türk mutfağı, sevdiklerinize değer, hemen alın",
            "sports": "su geçirmez IPX7, nefes alır, ergonomik, ultra hafif, dayanıklı, fitness, spor salonu, koşu, türkiye kargo, spor tutkunları, sağlık, aktif yaşam, türkiye'den hızlı kargo, özel indirim, bugün siparişte",
            "office": "verimlilik, masa, uzaktan çalışma, organize edici, ayarlanabilir, profesyonel, premium business, türkiye kargo, iş başarısı, ofis konfor, profesyonel seçim, kariyeriniz için, türkiye garantisi, sınırlı ürün",
            "beauty": "organik, doğal, paraben içermez, hassas cilt, dermatolojik test, türk kozmetik, güzellik bakım, anti-aging, güzelliğiniz için, kendine değer, türk kadınının tercihi, sağlıklı cilt, özel formül, kaçırmayın",
            "fashion": "moda, trend, stil, kaliteli kumaş, rahat, şık, günlük, klasik, modern türk tarzı, sezonluk, tarzınız için, kendine güven, türk modası, şıklık garantisi, özel koleksiyon, sınırlı sayıda",
            "jewelry": "925 ayar gümüş, altın kaplama, el işçiliği, türk zanaatkarlığı, özel tasarım, hediye kutusu, şık aksesuvar, sevdiklerinize hediye, özel günler, türk sanatı, değerli anılar, gurur duyacağınız, özel fırsat",
            "baby": "bebek güvenli, BPA içermez, hipoalerjenik, yumuşak, organik pamuk, anne dostu, bebek bakım, türkiye üretimi, bebeğiniz için güvenli, anne kalbi rahatlığı, çocuk sağlığı, türk anne tercihi, güvenli gelecek, özel bebek ürünü"
        }
        
        # Find matching category keywords
        for key, keywords in industry_keywords.items():
            if key in category:
                return keywords
        
        # Default high-intent Turkish keywords - BEATS ALL COMPETITORS
        return "en iyi, orijinal, profesyonel, CE sertifikalı, garanti 2 yıl, premium, türkiye fırsatı, türkiye kargo 24h, avrupa kalitesi, güvenilir marka, sınırlı stok, özel fiyat, aileniz için, türk kalitesi, 10000+ mutlu müşteri, bugün kaçırmayın, son fırsat, acele edin, hayalinizdeki kalite"
    
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

        elif marketplace == 'nl':
            bullet_examples = {
                1: "PREMIUM NEDERLANDSE KWALITEIT: Kristalhelder geluid met ruisonderdrukking voor Nederlandse families - 30u batterij voor ononderbroken luisterplezier. CE gecertificeerd met 2 jaar garantie.",
                2: "SUPERIEUR DRAAGCOMFORT: Lichtgewicht 193g design perfect voor Nederlandse levensstijl - ademende oorkussens voor langdurig gebruik. Verstelbaar voor alle hoofdmaten.",
                3: "BLUETOOTH 5.3 CONNECTIVITEIT: 15m bereik zonder onderbrekingen - stabiele verbinding voor gesprekken en muziek. Compatibel met alle iPhone en Android apparaten.",
                4: "ZWEET BESTENDIG IPX5: Ideaal voor sport en Nederlandse weersomstandigheden - bestand tegen vocht en transpiratie. Opvouwbaar design voor eenvoudig transport.",
                5: "VOLLEDIGE NEDERLANDSE GARANTIE: 24/7 technische ondersteuning in het Nederlands - factuur inbegrepen en 30 dagen retourrecht. Meer dan 50,000 tevreden klanten in Nederland."
            }
            
            return f"🇳🇱 NEDERLANDS FORMAAT (MAX 200 CHARS): [LABEL IN HOOFDLETTERS]: [Voordeel in het Nederlands]. [Specificatie]. [Garantie/Certificering]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

        elif marketplace == 'tr':
            bullet_examples = {
                1: "TÜRK KALİTESİ PREMİUM: Kristal ses kalitesi gürültü engelleme ile Türk aileleri için - 30 saat pil ömrü kesintisiz müzik keyfini garantiler. TSE belgeli, 2 yıl garanti.",
                2: "ÜSTÜN RAHATLIK TASARIMI: 193g hafif tasarım Türk yaşam tarzına uygun - nefes alan kulaklık pedleri uzun süreli kullanım için. Tüm baş boyutlarına ayarlanabilir.",
                3: "BLUETOOTH 5.3 BAĞLANTI: 15m menzil kesintisiz bağlantı - kararlı bağlantı görüşmeler ve müzik için. Tüm iPhone ve Android cihazlarla uyumlu.",
                4: "TER DİRENÇLİ IPX5: Spor ve Türkiye iklimi için ideal - nem ve tere karşı dayanıklı. Seyahat için katlanabilir tasarım.",
                5: "TAM TÜRKİYE GARANTİSİ: 7/24 Türkçe teknik destek - fatura dahil 30 gün iade hakkı. Türkiye'de 50,000'den fazla memnun müşteri."
            }
            
            return f"🇹🇷 TÜRK FORMATI (MAX 200 CHARS): [BÜYÜK HARF ETİKET]: [Türkçe fayda]. [Özellik]. [Garanti/Sertifika]. Bullet {bullet_number}: '{bullet_examples.get(bullet_number, bullet_examples[1])}'"

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
        
        # Now create the completely new human-focused prompt
        prompt = f"""
{language_instruction}
{localization_enhancement}
{aplus_enhancement}
{brand_tone_enhancement}
{occasion_enhancement}
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
    "primary": ["{product.name.lower().replace(' ', '_')}", "{product.brand_name.lower()}", "{self.get_japanese_industry_keywords(product) if product.marketplace == 'jp' else self.get_spanish_industry_keywords(product) if product.marketplace == 'es' else self.get_turkish_industry_keywords(product) if product.marketplace == 'tr' else 'THEN_ADD_13_MORE: category, color, size, material, feature1, feature2, use1, use2, style, type, model, variant, application'}"],
    "longTail": ["GENERATE_25_PHRASES: {'[ürün] [kullanım] için ideal' if product.marketplace == 'tr' else '[product] [用途]に最適' if product.marketplace == 'jp' else 'mejor [product] para [uso]' if product.marketplace == 'es' else 'best [product] for [use]'}", "{'[marka] [ürün] orijinal' if product.marketplace == 'tr' else '[brand] [product] 正規品' if product.marketplace == 'jp' else '[brand] [product] original certificado' if product.marketplace == 'es' else '[brand] [product] with [feature]'}", "{'[ürün] kaliteli [özellik]' if product.marketplace == 'tr' else '[product] 高品質 [機能]' if product.marketplace == 'jp' else '[product] profesional [aplicación]' if product.marketplace == 'es' else '[product] that [solves problem]'}", "{'[ürün] premium kalite' if product.marketplace == 'tr' else '[product] プレミアム品質' if product.marketplace == 'jp' else '[product] premium calidad' if product.marketplace == 'es' else 'professional [product] for [application]'}", "{'[ürün] Türkiye kargo' if product.marketplace == 'tr' else '[product] 送料無料' if product.marketplace == 'jp' else 'oferta [product] [beneficio]' if product.marketplace == 'es' else 'high quality [product] [benefit]'}", "etc"],
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
            self.logger.info(f"Using product context: {product_context[:200]}...")
            
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

🚨 KEYWORD GENERATION CRITICAL RULES:
- For seoKeywords arrays: Generate ACTUAL keywords/phrases, NOT instruction text
- Do NOT include text like "Generate 15+ keywords..." - that's instruction, not content
- Primary keywords: Start with product name, brand name, then add 13+ real keywords
- Long-tail: Create 25+ actual 3-7 word phrases customers would search
- Problem-solving: List 15+ actual problems this product solves as keywords
- Rufus conversational: List 15+ actual questions/phrases people ask
- Semantic: List 10+ actual related terms and synonyms

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
                    ("Escape fix", lambda x: json.loads(x.replace('\\"', '"').replace('\\n', '\n'), strict=False))
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
                            "title": "Why Choose Our Premium Quality?",
                            "content": "Experience the difference with our superior product design and customer-focused approach.",
                            "keywords": ["premium", "quality", "superior"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Hero lifestyle shot showing satisfied customer using product - specific person demographics, setting details, lighting mood, product placement, emotional context, and why this image drives conversion for the target market.",
                            "seoOptimization": "Focus on quality and premium positioning"
                        },
                        "section2_features": {
                            "title": "Key Features & Benefits",
                            "content": "Discover what makes our product stand out with premium materials and thoughtful design.",
                            "keywords": ["features", "benefits", "premium materials"],
                            "imageDescription": "DETAILED ENGLISH IMAGE STRATEGY: Feature callouts with detailed product shots - specific angles, close-ups, technical details, demonstration scenarios, and visual proof of key benefits. Include composition, lighting, and conversion-focused elements.",
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
            
            # Get title and preserve international characters (umlauts, accents, etc.)
            raw_title = result.get('productTitle', f"{product.name} - Premium Quality")
            
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
            listing.whats_in_box = '\n'.join(result.get('whatsInBox', [f'{product.name}', 'User manual', 'Warranty information', 'Quality assurance certificate']))
            
            # Extract trust builders from A+ plan or fallback to direct result
            trust_section = aplus_plan.get('section3_trust', {}) or aplus_plan.get('trustSection', {})
            trust_content = trust_section.get('content', []) or trust_section.get('trust_builders', [])
            if not trust_content:
                trust_content = result.get('trustBuilders', ['30-day satisfaction guarantee', 'Quality tested and certified', '24/7 customer support', 'Manufacturer warranty included'])
            listing.trust_builders = '\n'.join(trust_content)
            listing.social_proof = result.get('socialProof', f'Thousands of satisfied customers choose {product.brand_name} for quality and reliability.')
            listing.guarantee = result.get('guarantee', f'100% satisfaction guarantee - if you are not completely satisfied, return within 30 days for full refund.')
            
            # Parse comprehensive FAQ structure
            faqs_list = result.get('faqs', [])
            if faqs_list:
                listing.faqs = '\n\n'.join(faqs_list)
            else:
                # Create default FAQs if none provided
                default_faqs = [
                    f"Q: Is this {product.name.lower()} compatible with my needs? A: Yes, this {product.name.lower()} is designed to work with a wide variety of applications and requirements.",
                    f"Q: What makes {product.brand_name} different from other brands? A: {product.brand_name} focuses on quality, reliability, and customer satisfaction with rigorous testing and premium materials.",
                    f"Q: What is included with my purchase? A: You receive the complete {product.name.lower()}, comprehensive documentation, warranty coverage, and dedicated customer support."
                ]
                listing.faqs = '\n\n'.join(default_faqs)
            
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
                        'seo_focus': 'SEO Odak'
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
                        'seo_focus': 'SEO Focus'
                    }
                else:
                    return {
                        'keywords': 'Keywords',
                        'image_strategy': 'Image Strategy',
                        'seo_focus': 'SEO Focus'
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
            # EXCEPTION: Turkey (tr) and Netherlands (nl) should ONLY use AI-generated content, no fallback
            if not sections_html and (listing.hero_title or listing.features or listing.trust_builders) and marketplace_code not in ['tr', 'nl']:
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
                        image_text = "ENGLISH: Turkish family lifestyle image showing product in use (970x600px)"
                        seo_text = "Kalite odaklı SEO stratejisi"
                        premium_label = "Premium Deneyim"
                        premium_desc = "Türk standartlarına göre üstün tasarım ve kalite"
                    elif marketplace_code == 'nl':
                        keywords_text = "premium kwaliteit, betrouwbaar merk, klanttevredenheid"
                        image_text = "ENGLISH: Dutch lifestyle hero image with product (970x600px)"
                        seo_text = "Kwaliteit gerichte SEO strategie"
                        premium_label = "Premium Ervaring"
                        premium_desc = "Superieur ontwerp volgens Nederlandse normen"
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
                
                # Create features section from actual features with new box design
                if listing.features:
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
                        # Turkey image descriptions in English (like Netherlands)
                        if 'audio' in product_category or 'headphone' in product_category:
                            features_image = "ENGLISH: Turkish family listening to music, technical features displayed with Turkish labels (1500x1500px)"
                        elif 'kitchen' in product_category:
                            features_image = "ENGLISH: Turkish kitchen with product in use, hospitality scene showcased (1500x1500px)"
                        else:
                            features_image = "ENGLISH: Features infographic with Turkish design patterns (1500x1500px)"
                        features_seo = "Teknik özellikler için SEO optimizasyonu"
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
                <h3 class="text-green-900 text-xl sm:text-2xl font-bold">Key Features & Benefits</h3>
                <p class="text-gray-600 text-sm mt-1">Features section with product advantages and benefits</p>
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
                    elif marketplace_code == 'nl':
                        # Netherlands culture: trust through quality and reliability
                        trust_keywords = "CE keurmerk, Nederlandse garantie, betrouwbare kwaliteit, klantenservice"
                        # Netherlands trust image descriptions in Dutch
                        trust_image = "CE certificering zichtbaar, Nederlandse kwaliteitskeurmerken, garantiebewijzen (1200x800px)"
                        trust_seo = "SEO strategie voor vertrouwen"
                    elif marketplace_code == 'tr':
                        # Turkey culture: trust through certifications and local support
                        trust_keywords = "TSE belgesi, CE sertifikası, 2 yıl garanti, Türkiye destek"
                        # Turkey trust image descriptions in English (like Netherlands)
                        trust_image = "ENGLISH: TSE and CE certificates visible, Turkish customer testimonials, warranty badges (1200x800px)"
                        trust_seo = "Güven odaklı SEO stratejisi"
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
                <h3 class="text-purple-900 text-xl sm:text-2xl font-bold">Why Trust This Product</h3>
                <p class="text-gray-600 text-sm mt-1">Trust section with quality assurance and guarantees</p>
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
                    elif marketplace_code == 'nl':
                        # Netherlands culture: direct and practical information
                        faq_keywords = "veelgestelde vragen, praktische hulp, gebruiksaanwijzing, probleemoplossing"
                        # Netherlands FAQ image descriptions in Dutch
                        faq_image = "Duidelijke instructies met pictogrammen, stap-voor-stap handleiding, praktische tips (800x600px)"
                        faq_seo = "SEO voor veelgestelde vragen"
                    elif marketplace_code == 'tr':
                        # Turkey culture: detailed support with hospitality
                        faq_keywords = "sık sorulan sorular, Türkçe destek, kullanım kılavuzu, problem çözümü"
                        # Turkey FAQ image descriptions in English (like Netherlands)
                        faq_image = "ENGLISH: Turkish customer service smiling, step-by-step visual guide, helpful icons (800x600px)"
                        faq_seo = "SSS için SEO optimizasyonu"
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
                <h3 class="text-yellow-900 text-xl sm:text-2xl font-bold">Frequently Asked Questions</h3>
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
            
            # Always save the full comprehensive aplus_html structure
            # The aplus_html already contains properly localized content from the AI response
            # because the AI was instructed to generate localized content in the aplus_plan sections
            listing.amazon_aplus_content = aplus_html
            self.logger.info(f"Comprehensive A+ content HTML saved for {marketplace_code}: {len(aplus_html)} characters")
            
            # CRITICAL: The localized content is already embedded within aplus_html structure
            # because the HTML generation above (lines 2085-2430) processes the localized aplus_plan
            # sections that contain titles, content, and other fields in the target language.
            # This preserves the full visual template structure while maintaining localization.
            
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

    def _generate_walmart_listing(self, product, listing):
        from .services_occasion_enhanced import OccasionOptimizer
        
        if not self.client:
            raise Exception("OpenAI API key not configured. Please set a valid OpenAI API key to generate Walmart listings.")
            
        # Initialize occasion optimizer for Walmart too
        occasion_optimizer = OccasionOptimizer()
            
        
        # Extract brand tone details
        brand_tone_mapping = {
            'professional': {
                'tone': 'Professional & Authoritative',
                'style': 'Focus on specifications, certifications, and professional benefits'
            },
            'casual': {
                'tone': 'Friendly & Approachable', 
                'style': 'Conversational, relatable, emphasize everyday benefits'
            },
            'luxury': {
                'tone': 'Premium & Sophisticated',
                'style': 'Emphasize quality, exclusivity, and superior craftsmanship'
            },
            'trendy': {
                'tone': 'Modern & Dynamic',
                'style': 'Highlight innovation, trending features, and contemporary design'
            }
        }
        
        brand_details = brand_tone_mapping.get(product.brand_tone, brand_tone_mapping['professional'])
        
        # Generate category-specific attributes based on product
        category_prompt = self._get_walmart_category_context(product)
        
        # Get occasion-specific enhancements if applicable
        occasion = getattr(product, 'occasion', None)
        occasion_enhancement = ""
        if occasion and occasion != 'None':
            occasion_enhancement = occasion_optimizer.get_occasion_prompt_enhancement(occasion)
            self.logger.info(f"Applied Walmart occasion enhancement for: {occasion}")
        
        prompt = f"""Create a professional Walmart listing for this product. Return ONLY valid JSON with no extra text.

{occasion_enhancement}

PRODUCT: {product.name}
BRAND: {product.brand_name}
DESCRIPTION: {product.description}  
FEATURES: {product.features}
PRICE: ${product.price}
SPECIAL OCCASION: {getattr(product, 'occasion', 'None - general purpose listing')}

Requirements:
- Title: Under 100 characters with brand and key benefit
- Features: Exactly 5-7 bullet points, max 80 characters each
- Description: 200-250 words, professional tone, no generic templates
- Keywords: 20 diverse SEO terms covering primary, long-tail, technical, brand, competitive, and demographic terms
- Include specific measurements and technical details

{{
  "product_title": "Professional title under 100 chars with brand and benefit",
  "key_features": [
    "Technical detail with measurement (under 80 chars)",
    "Certification or safety standard included",
    "Performance metric with specific numbers",
    "Material advantage or technology feature",
    "Compatibility or capacity specification",
    "Design or convenience benefit",
    "Warranty or reliability information"
  ],
  "description": "Write 200-250 word professional description focusing on technical advantages, performance benefits, and product superiority. Include specific details about materials, certifications, and real-world performance. Avoid generic templates.",
  "seo_keywords": [
    "primary keyword 1",
    "primary keyword 2",
    "primary keyword 3", 
    "long tail benefit phrase 1",
    "long tail benefit phrase 2",
    "problem solving phrase 1",
    "problem solving phrase 2",
    "technical specification term 1",
    "technical specification term 2",
    "brand specific term 1",
    "brand specific term 2",
    "category keyword 1",
    "category keyword 2",
    "comparison vs competitor keyword",
    "use case specific keyword",
    "feature specific keyword",
    "price range keyword",
    "quality indicator keyword",
    "seasonal/trending keyword",
    "demographic target keyword"
  ]
}}"""

        self.logger.info("Calling OpenAI for Walmart listing generation...")
        response = self.client.chat.completions.create(
            model="gpt-5-chat-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=3000
        )
        
        try:
            response_content = response.choices[0].message.content
            self.logger.info(f"Walmart AI Response received: {len(response_content)} characters")
            self.logger.info(f"Walmart Response preview: {response_content[:200]}...")
            
            # Try to parse JSON
            if not response_content.strip():
                raise ValueError("Empty response from AI")
            
            # Strip markdown code blocks if present
            if response_content.strip().startswith('```'):
                # Remove ```json from start and ``` from end
                response_content = response_content.strip()
                if response_content.startswith('```json'):
                    response_content = response_content[7:]
                elif response_content.startswith('```'):
                    response_content = response_content[3:]
                if response_content.endswith('```'):
                    response_content = response_content[:-3]
                response_content = response_content.strip()
                
            result = json.loads(response_content)
            
            # Validate and process Walmart-specific fields
            product_title = result.get('product_title', '')[:100]  # Hard cap at 100 chars
            description = result.get('description', '')
            key_features = result.get('key_features', [])
            
            # Validate description word count (minimum 150 words)
            word_count = len(description.split()) if description else 0
            if word_count < 150:
                self.logger.warning(f"Walmart description only has {word_count} words, minimum is 150")
                # Use enhanced fallback description that meets requirements
                description = self._generate_walmart_fallback_description(product)
            
            # Validate and truncate key features (max 80 chars each)
            validated_features = []
            for feature in key_features[:10]:  # Max 10 features
                if len(feature) > 80:
                    self.logger.warning(f"Feature truncated from {len(feature)} to 80 chars: {feature[:80]}")
                    validated_features.append(feature[:80])
                else:
                    validated_features.append(feature)
            
            # Core Walmart content (platform-specific fields only)
            listing.walmart_product_title = product_title
            listing.walmart_description = description
            listing.walmart_key_features = '\n'.join(validated_features)
            
            # General fields for all platforms (NOT platform-specific content)
            listing.title = product_title
            listing.short_description = description[:200] + "..." if len(description) > 200 else description
            listing.long_description = description
            # DO NOT SET bullet_points for Walmart - this is Amazon-specific
            
            # Identifiers
            identifiers = result.get('identifiers', {})
            listing.walmart_gtin_upc = identifiers.get('gtin_upc', '')
            listing.walmart_manufacturer_part = identifiers.get('manufacturer_part', '')
            listing.walmart_sku_id = identifiers.get('sku_id', '')
            
            # Category and attributes
            listing.walmart_product_type = result.get('product_type', '')
            listing.walmart_category_path = result.get('category_path', '')
            listing.walmart_attributes = json.dumps(result.get('attributes', {}))
            
            # Specifications
            specs = result.get('specifications', {})
            listing.walmart_specifications = json.dumps(specs)
            
            # Shipping
            shipping = result.get('shipping', {})
            listing.walmart_shipping_weight = shipping.get('weight', '')
            listing.walmart_shipping_dimensions = shipping.get('dimensions', '')
            
            # Warranty and compliance
            warranty = result.get('warranty', {})
            listing.walmart_warranty_info = json.dumps(warranty)
            
            compliance = result.get('compliance', {})
            listing.walmart_compliance_certifications = json.dumps(compliance.get('certifications', []))
            
            # Assembly
            assembly = result.get('assembly', {})
            listing.walmart_assembly_required = assembly.get('required', False)
            
            # Rich media
            rich_media = result.get('rich_media', {})
            listing.walmart_video_urls = json.dumps(rich_media.get('videos', []))
            listing.walmart_swatch_images = json.dumps(rich_media.get('additional_images', []))
            
            # SEO keywords (simplified format)
            seo_keywords = result.get('seo_keywords', [])
            if isinstance(seo_keywords, list):
                listing.keywords = ', '.join(seo_keywords[:20])  # Limit to 20 keywords
            else:
                # Handle old complex format if still present
                all_keywords = seo_keywords.get('primary', []) + seo_keywords.get('long_tail', []) + seo_keywords.get('category', [])
                listing.keywords = ', '.join(all_keywords[:20])
            
            # DO NOT SET bullet_points for Walmart - this is Amazon-specific
            
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error(f"Failed to parse Walmart AI response: {e}")
            self.logger.error(f"Response content: {response_content[:500] if 'response_content' in locals() else 'No content'}")
            
            # Generate fallback content based on product data (following Walmart requirements)
            listing.walmart_product_title = f"{product.brand_name} {product.name}"[:100]  # 100 char limit
            listing.title = listing.walmart_product_title
            
            # Generate fallback description
            fallback_desc = self._generate_walmart_fallback_description(product)
            listing.walmart_description = fallback_desc
            listing.short_description = fallback_desc[:200] + "..." if len(fallback_desc) > 200 else fallback_desc
            listing.long_description = fallback_desc
            
            # Generate basic identifiers
            import random
            listing.walmart_gtin_upc = f"{random.randint(100000000000, 999999999999):012d}"
            listing.walmart_manufacturer_part = f"{product.brand_name.upper()[:3]}-{product.name[:3].upper()}-2024"
            listing.walmart_sku_id = f"SKU-{product.id:04d}"
            
            # Basic features from product (generate 5-7 features for Walmart)
            if product.features:
                base_features = [f.strip() for f in product.features.split(',')]
                # Ensure we have 5-7 features for Walmart requirements
                while len(base_features) < 5:
                    base_features.extend([
                        f"Premium {product.name.lower()} construction",
                        f"Designed for {product.categories.lower() if product.categories else 'everyday'} use",
                        f"Quality materials ensure lasting durability",
                        f"Easy to use and maintain design",
                        f"Trusted {product.brand_name} quality guarantee"
                    ])
                
                # Take exactly 5-7 features as preferred by Walmart
                walmart_features = base_features[:7]  # Max 7 features
                listing.walmart_key_features = '\n'.join(walmart_features)
                # DO NOT SET bullet_points for Walmart - this is Amazon-specific
            
            # Basic specifications
            listing.walmart_specifications = json.dumps({
                "Brand": product.brand_name,
                "Price": str(product.price),
                "Category": product.categories if product.categories else "General"
            })
            
            # Basic category info
            listing.walmart_product_type = product.categories.split(',')[0] if product.categories else "General Product"
            listing.walmart_category_path = product.categories.replace(',', ' > ') if product.categories else "Home > General"
            
            # Basic attributes
            listing.walmart_attributes = json.dumps({
                "brand": product.brand_name,
                "price": str(product.price)
            })
            
            # Keywords from product
            if product.seo_keywords or product.long_tail_keywords:
                all_keywords = []
                if product.seo_keywords:
                    all_keywords.extend(product.seo_keywords.split(','))
                if product.long_tail_keywords:
                    all_keywords.extend(product.long_tail_keywords.split(','))
                listing.keywords = ', '.join([k.strip() for k in all_keywords[:20]])
            
    def _get_walmart_category_context(self, product):
        """Generate category-specific context for Walmart listings"""
        category_contexts = {
            'electronics': """
- Product Type: Consumer Electronics
- Required Attributes: Screen size, resolution, connectivity, power consumption
- Certifications: FCC, UL, Energy Star
""",
            'home': """
- Product Type: Home & Garden
- Required Attributes: Room type, style, assembly required, care instructions
- Certifications: Safety standards, material certifications
""",
            'beauty': """
- Product Type: Beauty & Personal Care
- Required Attributes: Skin type, ingredients, volume/size, scent
- Certifications: FDA compliance, cruelty-free, organic certifications
""",
            'sports': """
- Product Type: Sports & Outdoors
- Required Attributes: Activity type, skill level, age range, weather resistance
- Certifications: Safety standards, performance ratings
""",
            'toys': """
- Product Type: Toys & Games
- Required Attributes: Age range, number of players, educational value, choking hazards
- Certifications: CPSC, ASTM, age appropriate ratings
"""
        }
        
        # Try to match category
        product_categories = product.categories.lower() if product.categories else ''
        for key, context in category_contexts.items():
            if key in product_categories:
                return context
                
        # Default context
        return """
- Product Type: General Merchandise
- Required Attributes: Size, color, material, intended use
- Certifications: Relevant safety and quality standards
"""
    
    def _generate_walmart_fallback_description(self, product):
        """Generate a 200-250 word Walmart-compliant description"""
        description = f"The {product.brand_name} {product.name} delivers exceptional performance through advanced engineering and quality construction that sets it apart from standard alternatives in this category. "
        
        if product.description:
            description += f"{product.description} But here's what makes it really special - it's designed with your daily needs in mind, not just as another product on the shelf. "
        
        description += f"When you're considering a {product.name.lower()}, you want to know it will actually work for your lifestyle. That's exactly what {product.brand_name} delivers with this thoughtfully engineered solution. "
        
        if product.features:
            description += f"The key features that customers consistently rave about include {product.features.lower()}. These aren't just fancy add-ons or marketing gimmicks; they're practical solutions to real problems you face every day. "
        
        description += f"What makes this {product.name.lower()} different from others in its category? It's the attention to detail and unwavering commitment to quality that {product.brand_name} brings to every single product they make. "
        
        # Add category-specific benefits
        if product.categories:
            description += f"As a premium {product.categories.lower()} solution, this product addresses the specific challenges you encounter in this category. "
        
        description += f"Whether you're looking for durability that stands the test of time, functionality that actually works as promised, or style that complements your space perfectly, this product delivers on all fronts without compromise. "
        
        # Add price/value proposition
        if product.price:
            description += f"At ${product.price}, this represents exceptional value compared to similar products that often cost significantly more while delivering less. "
        
        description += f"Many customers tell us they wish they'd found this {product.name.lower()} sooner - it would have saved them from disappointment with other products that promise much but deliver little. "
        
        description += f"It's not just another purchase; it's an investment in better daily experiences and genuine peace of mind. The difference becomes apparent from the very first use. "
        
        description += f"Perfect for both everyday use and those special moments when you need something reliable, this {product.name.lower()} adapts to your lifestyle seamlessly. The quality construction and thoughtful design mean you can count on it for years to come. "
        
        description += f"With {product.brand_name}'s reputation for excellence backing every purchase, you're not just buying a product - you're joining thousands of satisfied customers who made the smart choice."
        
        return description

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
            model="gpt-5-chat-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_completion_tokens=1500
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
            model="gpt-5-chat-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_completion_tokens=2000
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
            model="gpt-5-chat-latest",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1500
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
                
                # INTERNATIONAL CHARACTER PRESERVING emoji removal
                # Only remove actual emojis, keep international letters (ä, ö, ü, ß, é, ñ, etc.)
                
                # Define emoji ranges to remove while preserving international letters
                # Carefully exclude Japanese Unicode ranges: U+3040-U+309F (Hiragana), U+30A0-U+30FF (Katakana), U+4E00-U+9FAF (Kanji)
                emoji_pattern = re.compile(
                    "["
                    "\U0001F600-\U0001F64F"  # emoticons
                    "\U0001F300-\U0001F5FF"  # symbols & pictographs
                    "\U0001F680-\U0001F6FF"  # transport & map symbols
                    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
                    "\U00002702-\U000027B0"  # dingbats (safe range)
                    "\U0001F900-\U0001F9FF"  # supplemental symbols
                    "\U00002600-\U000026FF"  # miscellaneous symbols
                    "\U00002700-\U000027BF"  # dingbats
                    # REMOVED: "\U000024C2-\U0001F251" - this range was too broad and included Japanese
                    "]+", flags=re.UNICODE)
                
                # Remove only emojis, preserve international characters
                clean_text = emoji_pattern.sub('', text)
                
                # Clean up multiple spaces but preserve all text characters
                clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                
                # Debug logging
                final_length = len(clean_text)
                has_unicode_after = any(ord(c) > 127 for c in clean_text) if clean_text else False
                self.logger.debug(f"Emoji removal output: {final_length} chars, has Unicode: {has_unicode_after}")
                
                return clean_text if clean_text else text
                
            except Exception as e:
                self.logger.error(f"Emoji removal failed: {e}")
                # Fallback - return original text to preserve international content
                return text
        
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


    def _create_structured_aplus_html(self, aplus_plan, result, marketplace='com'):
        """Create structured HTML A+ content from JSON data for better display."""
        import json
        try:
            # Define localized interface labels at the beginning
            marketplace_code = marketplace
            
            def get_localized_labels(market_code):
                if market_code == 'tr':
                    return {
                        'keywords': 'Anahtar Kelimeler',
                        'image_strategy': 'Görsel Strateji', 
                        'seo_focus': 'SEO Odak'
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
                        'seo_focus': 'SEO Focus'
                    }
                else:
                    return {
                        'keywords': 'Keywords',
                        'image_strategy': 'Image Strategy',
                        'seo_focus': 'SEO Focus'
                    }
            
            localized_labels = get_localized_labels(marketplace_code)
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