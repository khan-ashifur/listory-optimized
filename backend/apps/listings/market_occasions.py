"""
Market-Specific Occasions for International Amazon Listings
Ensures culturally relevant occasions for each marketplace
"""

class MarketOccasions:
    """Handles market-specific occasions and removes inappropriate US occasions"""
    
    def __init__(self):
        # Define occasions for each market
        self.market_occasions = {
            'us': {
                'christmas': 'Christmas',
                'black_friday': 'Black Friday',
                'cyber_monday': 'Cyber Monday',
                'valentines_day': "Valentine's Day",
                'mothers_day': "Mother's Day",
                'fathers_day': "Father's Day",
                'halloween': 'Halloween',
                'thanksgiving': 'Thanksgiving',
                'independence_day': 'Independence Day (July 4th)',
                'memorial_day': 'Memorial Day',
                'labor_day': 'Labor Day',
                'back_to_school': 'Back to School',
                'new_year': "New Year's",
                'easter': 'Easter'
            },
            
            'de': {  # Germany
                'weihnachten': 'Weihnachten',  # Christmas
                'black_friday': 'Black Friday',
                'cyber_monday': 'Cyber Monday',
                'valentinstag': 'Valentinstag',  # Valentine's Day
                'muttertag': 'Muttertag',  # Mother's Day
                'vatertag': 'Vatertag',  # Father's Day
                'ostern': 'Ostern',  # Easter
                'oktoberfest': 'Oktoberfest',
                'silvester': 'Silvester',  # New Year's Eve
                'neujahr': 'Neujahr',  # New Year
                'fasching': 'Fasching/Karneval',  # Carnival
                'schulanfang': 'Schulanfang',  # Back to School
                'winterschlussverkauf': 'Winterschlussverkauf',  # Winter Sale
                'sommerschlussverkauf': 'Sommerschlussverkauf',  # Summer Sale
                'nikolaustag': 'Nikolaustag',  # St. Nicholas Day
                'advent': 'Adventszeit'  # Advent Season
            },
            
            'fr': {  # France
                'noel': 'Noël',  # Christmas
                'black_friday': 'Black Friday',
                'cyber_monday': 'Cyber Monday',
                'saint_valentin': 'Saint-Valentin',  # Valentine's Day
                'fete_des_meres': 'Fête des Mères',  # Mother's Day
                'fete_des_peres': 'Fête des Pères',  # Father's Day
                'paques': 'Pâques',  # Easter
                'jour_de_lan': "Jour de l'An",  # New Year's Day
                'rentree_scolaire': 'Rentrée Scolaire',  # Back to School
                'soldes_hiver': "Soldes d'Hiver",  # Winter Sales
                'soldes_ete': "Soldes d'Été",  # Summer Sales
                'beaujolais_nouveau': 'Beaujolais Nouveau',
                'fete_nationale': 'Fête Nationale (14 Juillet)',  # Bastille Day
                'epiphanie': 'Épiphanie',  # Epiphany
                'chandeleur': 'Chandeleur',  # Candlemas
                'toussaint': 'Toussaint'  # All Saints' Day
            },
            
            'it': {  # Italy
                'natale': 'Natale',  # Christmas
                'black_friday': 'Black Friday',
                'cyber_monday': 'Cyber Monday',
                'san_valentino': 'San Valentino',  # Valentine's Day
                'festa_della_mamma': 'Festa della Mamma',  # Mother's Day
                'festa_del_papa': 'Festa del Papà',  # Father's Day
                'pasqua': 'Pasqua',  # Easter
                'capodanno': 'Capodanno',  # New Year
                'befana': 'Befana',  # Epiphany
                'ferragosto': 'Ferragosto',  # August Holiday
                'ritorno_a_scuola': 'Ritorno a Scuola',  # Back to School
                'saldi_invernali': 'Saldi Invernali',  # Winter Sales
                'saldi_estivi': 'Saldi Estivi',  # Summer Sales
                'carnevale': 'Carnevale',  # Carnival
                'festa_della_repubblica': 'Festa della Repubblica',  # Republic Day
                'ognissanti': 'Ognissanti'  # All Saints' Day
            },
            
            'es': {  # Spain
                'navidad': 'Navidad',  # Christmas
                'black_friday': 'Black Friday',
                'cyber_monday': 'Cyber Monday',
                'san_valentin': 'San Valentín',  # Valentine's Day
                'dia_de_la_madre': 'Día de la Madre',  # Mother's Day
                'dia_del_padre': 'Día del Padre',  # Father's Day
                'semana_santa': 'Semana Santa',  # Easter/Holy Week
                'nochevieja': 'Nochevieja',  # New Year's Eve
                'reyes_magos': 'Reyes Magos',  # Three Kings Day
                'vuelta_al_cole': 'Vuelta al Cole',  # Back to School
                'rebajas_invierno': 'Rebajas de Invierno',  # Winter Sales
                'rebajas_verano': 'Rebajas de Verano',  # Summer Sales
                'el_gordo': 'El Gordo (Lotería)',  # Christmas Lottery
                'dia_hispanidad': 'Día de la Hispanidad',  # Hispanic Day
                'todos_los_santos': 'Todos los Santos',  # All Saints' Day
                'san_jorge': 'San Jorge',  # St. George's Day (Catalonia)
                'feria_abril': 'Feria de Abril'  # April Fair (Seville)
            },
            
            'jp': {  # Japan
                'oshogatsu': '正月',  # New Year (most important)
                'kurisumasu': 'クリスマス',  # Christmas
                'barentain_de': 'バレンタインデー',  # Valentine's Day
                'howaito_de': 'ホワイトデー',  # White Day (March 14)
                'haha_no_hi': '母の日',  # Mother's Day
                'chichi_no_hi': '父の日',  # Father's Day
                'kodomo_no_hi': 'こどもの日',  # Children's Day
                'bunka_no_hi': '文化の日',  # Culture Day
                'kinro_kansha': '勤労感謝の日',  # Labor Thanksgiving Day
                'seijin_no_hi': '成人の日',  # Coming of Age Day
                'keiro_no_hi': '敬老の日',  # Respect for the Aged Day
                'shichi_go_san': '七五三',  # Shichi-Go-San
                'ochutgen': 'お中元',  # Mid-year gift giving
                'oseibo': 'お歳暮',  # End-year gift giving
                'nyugaku_shiki': '入学式',  # School entrance ceremony
                'sotsugyou_shiki': '卒業式',  # Graduation ceremony
                'hanami': '花見',  # Cherry blossom viewing
                'tanabata': '七夕',  # Star Festival
                'obon': 'お盆',  # Obon (Festival of the Dead)
                'tsukimi': '月見',  # Moon viewing
                'bonenkai': '忘年会',  # End-of-year party
                'shinnenkai': '新年会',  # New Year party
                'black_friday': 'ブラックフライデー',  # Black Friday (growing)
                'amazon_prime_day': 'プライムデー'  # Amazon Prime Day
            },
            
            'ae': {  # United Arab Emirates
                'eid_al_fitr': 'عيد الفطر',  # Eid al-Fitr (most important)
                'eid_al_adha': 'عيد الأضحى',  # Eid al-Adha (Feast of Sacrifice)
                'ramadan': 'شهر رمضان',  # Ramadan (Holy Month)
                'new_year': 'رأس السنة الميلادية',  # New Year
                'uae_national_day': 'اليوم الوطني الإماراتي',  # UAE National Day (December 2)
                'mothers_day': 'يوم الأم',  # Mother's Day
                'fathers_day': 'يوم الأب',  # Father's Day
                'back_to_school': 'العودة إلى المدرسة',  # Back to School
                'summer_vacation': 'العطلة الصيفية',  # Summer Vacation
                'winter_shopping': 'تسوق الشتاء',  # Winter Shopping
                'iftar_gathering': 'تجمع الإفطار',  # Iftar Gathering
                'suhoor_preparation': 'تحضير السحور',  # Suhoor Preparation
                'hajj_preparation': 'تحضيرات الحج',  # Hajj Preparation
                'graduation_season': 'موسم التخرج',  # Graduation Season
                'wedding_season': 'موسم الأعراس',  # Wedding Season
                'black_friday': 'الجمعة البيضاء',  # Black Friday
                'white_friday': 'الجمعة البيضاء',  # White Friday (regional name)
                'dubai_shopping_festival': 'مهرجان دبي للتسوق',  # Dubai Shopping Festival
                'ramadan_iftar': 'إفطار رمضان',  # Ramadan Iftar
                'family_gathering': 'تجمع العائلة',  # Family Gathering
                'housewarming': 'حفل افتتاح المنزل'  # Housewarming
            },
            
            'mx': {  # Mexico
                'dia_de_muertos': 'Día de Muertos',  # Day of the Dead (most important)
                'navidad': 'Navidad',  # Christmas
                'dia_de_reyes': 'Día de Reyes',  # Three Kings Day (January 6)
                'dia_de_la_candelaria': 'Día de la Candelaria',  # Candlemas (February 2)
                'dia_de_la_madre': 'Día de la Madre',  # Mother's Day (May 10)
                'dia_del_padre': 'Día del Padre',  # Father's Day
                'dia_del_niño': 'Día del Niño',  # Children's Day (April 30)
                'cinco_de_mayo': 'Cinco de Mayo',  # May 5th
                'dia_de_independencia': 'Día de la Independencia',  # Independence Day (September 16)
                'revolucion_mexicana': 'Revolución Mexicana',  # Mexican Revolution (November 20)
                'posadas': 'Las Posadas',  # Christmas season celebrations
                'nochebuena': 'Nochebuena',  # Christmas Eve
                'año_nuevo': 'Año Nuevo',  # New Year
                'dia_de_san_valentin': 'Día de San Valentín',  # Valentine's Day
                'semana_santa': 'Semana Santa',  # Holy Week
                'corpus_christi': 'Corpus Christi',  # Corpus Christi
                'regreso_a_clases': 'Regreso a Clases',  # Back to School
                'dia_de_la_familia': 'Día de la Familia',  # Family Day
                'quinceañera': 'Quinceañera',  # 15th Birthday Celebration
                'boda': 'Boda',  # Wedding
                'bautizo': 'Bautizo',  # Baptism
                'primera_comunion': 'Primera Comunión',  # First Communion
                'graduacion': 'Graduación',  # Graduation
                'baby_shower': 'Baby Shower',  # Baby Shower
                'cumpleaños': 'Cumpleaños',  # Birthday
                'aniversario': 'Aniversario',  # Anniversary
                'el_buen_fin': 'El Buen Fin',  # Mexican Black Friday (November)
                'black_friday': 'Black Friday',  # Black Friday
                'cyber_monday': 'Cyber Monday',  # Cyber Monday
                'hotline': 'Hot Sale',  # Mexican Hot Sale (May)
                'verano': 'Verano',  # Summer
                'vacaciones': 'Vacaciones'  # Vacation
            },
            
            'in': {  # India
                'diwali': 'Diwali',  # Festival of Lights (most important)
                'holi': 'Holi',  # Festival of Colors
                'navratri': 'Navratri',  # Nine Nights Festival
                'dussehra': 'Dussehra',  # Victory of Good over Evil
                'karva_chauth': 'Karva Chauth',  # Festival for married women
                'raksha_bandhan': 'Raksha Bandhan',  # Brother-Sister festival
                'janmashtami': 'Janmashtami',  # Krishna's Birthday
                'ganesha_chaturthi': 'Ganesha Chaturthi',  # Lord Ganesha festival
                'eid_ul_fitr': 'Eid ul-Fitr',  # End of Ramadan
                'eid_ul_adha': 'Eid ul-Adha',  # Festival of Sacrifice
                'christmas': 'Christmas',  # Christmas
                'new_year': 'New Year',  # New Year
                'guru_nanak_jayanti': 'Guru Nanak Jayanti',  # Sikh festival
                'maha_shivratri': 'Maha Shivratri',  # Lord Shiva festival
                'ram_navami': 'Ram Navami',  # Lord Rama's birthday
                'hanuman_jayanti': 'Hanuman Jayanti',  # Lord Hanuman's birthday
                'republic_day': 'Republic Day',  # January 26
                'independence_day': 'Independence Day',  # August 15
                'gandhi_jayanti': 'Gandhi Jayanti',  # October 2
                'mothers_day': 'Mother\'s Day',  # Mother's Day
                'fathers_day': 'Father\'s Day',  # Father's Day
                'childrens_day': 'Children\'s Day',  # November 14
                'valentines_day': 'Valentine\'s Day',  # Valentine's Day
                'wedding_season': 'Wedding Season',  # November-February
                'monsoon_festival': 'Monsoon Festival',  # Monsoon celebrations
                'harvest_festival': 'Harvest Festival',  # Regional harvest festivals
                'back_to_school': 'Back to School',  # School reopening
                'family_gathering': 'Family Gathering',  # Joint family occasions
                'housewarming': 'Griha Pravesh',  # House blessing ceremony
                'baby_shower': 'Godh Bharai',  # Indian baby shower
                'birthday': 'Birthday',  # Birthday celebrations
                'anniversary': 'Anniversary',  # Wedding anniversary
                'big_billion_days': 'Big Billion Days',  # Flipkart sale
                'great_indian_festival': 'Great Indian Festival',  # Amazon sale
                'summer_vacation': 'Summer Vacation'  # Summer holidays
            },
            
            'br': {  # Brazil
                'carnaval': 'Carnaval',  # Carnival (most important Brazilian celebration)
                'natal': 'Natal',  # Christmas
                'ano_novo': 'Ano Novo',  # New Year
                'dia_das_maes': 'Dia das Mães',  # Mother's Day (2nd Sunday of May)
                'dia_dos_pais': 'Dia dos Pais',  # Father's Day
                'dia_das_criancas': 'Dia das Crianças',  # Children's Day (October 12)
                'dia_dos_namorados': 'Dia dos Namorados',  # Valentine's Day (June 12)
                'festa_junina': 'Festa Junina',  # June Festival
                'independencia_brasil': 'Independência do Brasil',  # Independence Day (September 7)
                'proclamacao_republica': 'Proclamação da República',  # Republic Day (November 15)
                'nossa_senhora_aparecida': 'Nossa Senhora Aparecida',  # Our Lady of Aparecida (October 12)
                'consciencia_negra': 'Consciência Negra',  # Black Awareness Day (November 20)
                'sao_joao': 'São João',  # Saint John's Day
                'oktoberfest_brasil': 'Oktoberfest Brasil',  # Brazilian Oktoberfest
                'dia_do_trabalho': 'Dia do Trabalho',  # Labor Day (May 1)
                'tiradentes': 'Tiradentes',  # Tiradentes Day (April 21)
                'corpus_christi': 'Corpus Christi',  # Corpus Christi
                'pascoa': 'Páscoa',  # Easter
                'volta_as_aulas': 'Volta às Aulas',  # Back to School
                'dia_da_familia': 'Dia da Família',  # Family Day
                'casamento': 'Casamento',  # Wedding
                'formatura': 'Formatura',  # Graduation
                'aniversario': 'Aniversário',  # Birthday
                'cha_de_bebe': 'Chá de Bebê',  # Baby Shower
                'cha_de_panela': 'Chá de Panela',  # Kitchen Shower
                'cha_de_lingerie': 'Chá de Lingerie',  # Lingerie Shower
                'black_friday': 'Black Friday',  # Black Friday
                'cyber_monday': 'Cyber Monday',  # Cyber Monday
                'liquidacao': 'Liquidação',  # Clearance Sale
                'verao': 'Verão',  # Summer
                'inverno': 'Inverno',  # Winter
                'ferias': 'Férias',  # Vacation
                'final_de_semana': 'Final de Semana'  # Weekend
            },
            
            'sa': {  # Saudi Arabia
                'eid_al_fitr': 'عيد الفطر',  # Eid al-Fitr (most important)
                'eid_al_adha': 'عيد الأضحى',  # Eid al-Adha (Feast of Sacrifice)
                'ramadan': 'شهر رمضان',  # Ramadan (Holy Month)
                'hijri_new_year': 'رأس السنة الهجرية',  # Hijri New Year
                'saudi_national_day': 'اليوم الوطني السعودي',  # Saudi National Day (September 23)
                'founding_day': 'يوم التأسيس',  # Saudi Founding Day (February 22)
                'mothers_day': 'يوم الأم',  # Mother's Day
                'fathers_day': 'يوم الأب',  # Father's Day
                'back_to_school': 'العودة إلى المدرسة',  # Back to School
                'summer_vacation': 'العطلة الصيفية',  # Summer Vacation
                'winter_shopping': 'تسوق الشتاء',  # Winter Shopping
                'iftar_gathering': 'تجمع الإفطار',  # Iftar Gathering
                'suhoor_preparation': 'تحضير السحور',  # Suhoor Preparation
                'hajj_preparation': 'تحضيرات الحج',  # Hajj Preparation
                'umrah_preparation': 'تحضيرات العمرة',  # Umrah Preparation
                'graduation_season': 'موسم التخرج',  # Graduation Season
                'wedding_season': 'موسم الأعراس',  # Wedding Season
                'black_friday': 'الجمعة البيضاء',  # Black Friday
                'white_friday': 'الجمعة البيضاء',  # White Friday (regional name)
                'riyadh_season': 'موسم الرياض',  # Riyadh Season
                'ramadan_iftar': 'إفطار رمضان',  # Ramadan Iftar
                'family_gathering': 'تجمع العائلة',  # Family Gathering
                'housewarming': 'حفل افتتاح المنزل',  # Housewarming
                'new_year': 'رأس السنة الميلادية',  # New Year
                'vision_2030': 'رؤية 2030',  # Vision 2030
                'qurban': 'قربان',  # Sacrifice
                'zakat_al_fitr': 'زكاة الفطر',  # Zakat al-Fitr
                'laylat_al_qadr': 'ليلة القدر',  # Night of Power
                'mawlid_nabawi': 'المولد النبوي',  # Prophet's Birthday
                'ashura': 'عاشوراء',  # Day of Ashura
                'isra_miraj': 'الإسراء والمعراج',  # Night Journey
                'dia_del_estudiante': 'يوم الطالب',  # Student Day
                'womens_day': 'يوم المرأة',  # Women's Day
                'youth_day': 'يوم الشباب',  # Youth Day
                'teachers_day': 'يوم المعلم',  # Teachers Day
                'cyber_monday': 'الاثنين الإلكتروني',  # Cyber Monday
                'valentine_day': 'عيد الحب',  # Valentine's Day
                'spring_season': 'فصل الربيع',  # Spring Season
                'autumn_season': 'فصل الخريف',  # Autumn Season
                'weekend': 'نهاية الأسبوع',  # Weekend
                'vacation': 'إجازة',  # Vacation
                'birthday': 'عيد ميلاد',  # Birthday
                'anniversary': 'ذكرى سنوية',  # Anniversary
                'engagement': 'خطوبة',  # Engagement
                'baby_shower': 'حفلة استقبال المولود',  # Baby Shower
                'business_meeting': 'اجتماع عمل',  # Business Meeting
                'office_gift': 'هدية المكتب'  # Office Gift
            },
            
            'nl': {  # Netherlands
                'koningsdag': 'Koningsdag',  # King's Day (most important Dutch celebration - April 27)
                'sinterklaas': 'Sinterklaas',  # Sinterklaas (December 5/6 - uniquely Dutch)
                'kerst': 'Kerst',  # Christmas
                'nieuwjaar': 'Nieuwjaar',  # New Year
                'moederdag': 'Moederdag',  # Mother's Day (2nd Sunday of May)
                'vaderdag': 'Vaderdag',  # Father's Day (3rd Sunday of June)
                'kinderdag': 'Kinderdag',  # Children's Day
                'valentijnsdag': 'Valentijnsdag',  # Valentine's Day
                'pasen': 'Pasen',  # Easter
                'bevrijdingsdag': 'Bevrijdingsdag',  # Liberation Day (May 5)
                'dodenherdenking': 'Dodenherdenking',  # Remembrance Day (May 4)
                'prinsjesdag': 'Prinsjesdag',  # Budget Day (3rd Tuesday of September)
                'zwarte_piet': 'Zwarte Piet',  # Black Pete (Sinterklaas helper)
                'kerstmis': 'Kerstmis',  # Christmas alternative term
                'tweede_kerstdag': 'Tweede Kerstdag',  # Boxing Day (December 26)
                'oudejaarsavond': 'Oudejaarsavond',  # New Year's Eve
                'carnaval': 'Carnaval',  # Carnival (mainly southern Netherlands)
                'tulpentijd': 'Tulpentijd',  # Tulip Season (Spring)
                'keukenhof': 'Keukenhof',  # Keukenhof Gardens season
                'schoolvakanties': 'Schoolvakanties',  # School holidays
                'zomervakantie': 'Zomervakantie',  # Summer vacation
                'terug_naar_school': 'Terug naar School',  # Back to School
                'familietijd': 'Familietijd',  # Family time
                'gezelligheid': 'Gezelligheid',  # Coziness/togetherness (uniquely Dutch concept)
                'bruiloft': 'Bruiloft',  # Wedding
                'verjaardag': 'Verjaardag',  # Birthday
                'afstuderen': 'Afstuderen',  # Graduation
                'babyshower': 'Babyshower',  # Baby Shower
                'housewarming': 'Housewarming',  # Housewarming
                'black_friday': 'Black Friday',  # Black Friday
                'cyber_monday': 'Cyber Monday',  # Cyber Monday
                'uitverkoop': 'Uitverkoop',  # Sale/Clearance
                'zomer': 'Zomer',  # Summer
                'winter': 'Winter',  # Winter
                'lente': 'Lente',  # Spring
                'herfst': 'Herfst',  # Autumn
                'weekend': 'Weekend',  # Weekend
                'vakantie': 'Vakantie',  # Vacation/Holiday
                'fietsseizoen': 'Fietsseizoen',  # Cycling season
                'voetbal': 'Voetbal',  # Football season
                'ek_wk': 'EK/WK',  # European/World Championship
                'oranje': 'Oranje'  # Dutch national team events
            }
        }
        
        # Occasions to REMOVE from international markets (US-specific)
        self.us_only_occasions = [
            'thanksgiving', 'independence_day', 'memorial_day', 'labor_day',
            'july 4th', 'fourth of july', '4th of july'
        ]
        
        # Universal occasions (work in all markets)
        self.universal_occasions = [
            'black_friday', 'cyber_monday', 'new_year', 'general'
        ]
    
    def get_market_occasions(self, marketplace):
        """Get appropriate occasions for a specific market"""
        return self.market_occasions.get(marketplace, self.market_occasions['us'])
    
    def translate_occasion(self, occasion, marketplace):
        """Translate occasion name to local language"""
        market_occasions = self.get_market_occasions(marketplace)
        
        # Check if occasion exists in market
        if occasion in market_occasions:
            return market_occasions[occasion]
        
        # Map common occasions to local equivalents
        occasion_mapping = {
            'christmas': {
                'de': 'Weihnachten',
                'fr': 'Noël',
                'it': 'Natale',
                'es': 'Navidad'
            },
            'valentines_day': {
                'de': 'Valentinstag',
                'fr': 'Saint-Valentin',
                'it': 'San Valentino',
                'es': 'San Valentín'
            },
            'mothers_day': {
                'de': 'Muttertag',
                'fr': 'Fête des Mères',
                'it': 'Festa della Mamma',
                'es': 'Día de la Madre'
            },
            'fathers_day': {
                'de': 'Vatertag',
                'fr': 'Fête des Pères',
                'it': 'Festa del Papà',
                'es': 'Día del Padre'
            },
            'easter': {
                'de': 'Ostern',
                'fr': 'Pâques',
                'it': 'Pasqua',
                'es': 'Semana Santa'
            },
            'back_to_school': {
                'de': 'Schulanfang',
                'fr': 'Rentrée Scolaire',
                'it': 'Ritorno a Scuola',
                'es': 'Vuelta al Cole'
            }
        }
        
        if occasion in occasion_mapping and marketplace in occasion_mapping[occasion]:
            return occasion_mapping[occasion][marketplace]
        
        # Default to original if no translation found
        return occasion
    
    def get_occasion_keywords(self, occasion, marketplace):
        """Get localized keywords for occasions"""
        keywords = {
            'de': {
                'weihnachten': ['weihnachtsgeschenk', 'weihnachten geschenk', 'christmas gift', 'heiligabend', 'adventsgeschenk'],
                'valentinstag': ['valentinstag geschenk', 'geschenk für sie', 'geschenk für ihn', 'liebesgeschenk'],
                'muttertag': ['muttertag geschenk', 'geschenk für mama', 'muttertagsgeschenk', 'mama geschenk'],
                'oktoberfest': ['oktoberfest', 'wiesn', 'bayern', 'dirndl', 'lederhose']
            },
            'fr': {
                'noel': ['cadeau noël', 'cadeau de noël', 'idée cadeau noël', 'père noël', 'réveillon'],
                'saint_valentin': ['cadeau saint valentin', 'cadeau amour', 'cadeau romantique', 'cadeau couple'],
                'fete_des_meres': ['cadeau fête des mères', 'cadeau maman', 'idée cadeau maman', 'cadeau mère']
            },
            'it': {
                'natale': ['regalo natale', 'regalo di natale', 'idea regalo natale', 'babbo natale', 'vigilia'],
                'san_valentino': ['regalo san valentino', 'regalo amore', 'regalo romantico', 'regalo coppia'],
                'festa_della_mamma': ['regalo festa della mamma', 'regalo mamma', 'idea regalo mamma']
            },
            'es': {
                'navidad': ['regalo navidad', 'regalo de navidad', 'regalo navideño', 'papá noel', 'nochebuena'],
                'reyes_magos': ['regalo reyes', 'regalo reyes magos', 'día de reyes', 'regalo 6 enero'],
                'san_valentin': ['regalo san valentín', 'regalo amor', 'regalo romántico', 'regalo pareja'],
                'dia_de_la_madre': ['regalo día de la madre', 'regalo mamá', 'regalo madre', 'idea regalo mamá']
            },
            'jp': {
                'oshogatsu': ['正月ギフト', '新年プレゼント', 'お年賀', '正月準備', '新春'],
                'kurisumasu': ['クリスマスプレゼント', 'クリスマスギフト', 'クリスマス限定', 'クリスマス特別'],
                'ochutgen': ['お中元ギフト', '夏のご挨拶', 'お中元プレゼント', '感謝の気持ち'],
                'oseibo': ['お歳暮ギフト', '年末のご挨拶', 'お歳暮プレゼント', '一年の感謝'],
                'haha_no_hi': ['母の日ギフト', 'お母さんプレゼント', '母の日感謝', '母の日限定'],
                'chichi_no_hi': ['父の日ギフト', 'お父さんプレゼント', '父の日感謝', '父の日限定'],
                'barentain_de': ['バレンタインギフト', 'バレンタイン限定', '特別な人へ'],
                'howaito_de': ['ホワイトデーお返し', 'ホワイトデーギフト', 'お返しプレゼント']
            },
            'sa': {
                'eid_al_fitr': ['هدية عيد الفطر', 'عيد الفطر المبارك', 'هدايا العيد', 'عيدية', 'فرحة العيد'],
                'eid_al_adha': ['هدية عيد الأضحى', 'عيد الأضحى المبارك', 'أضحى مبارك', 'عيد الحج', 'عيد القربان'],
                'ramadan': ['رمضان مبارك', 'شهر رمضان', 'رمضان كريم', 'إفطار رمضان', 'سحور رمضان'],
                'saudi_national_day': ['اليوم الوطني السعودي', 'هدية اليوم الوطني', 'السعودية', 'فخر السعودية'],
                'mothers_day': ['هدية يوم الأم', 'هدية أمي', 'عيد الأم', 'أمي الحبيبة'],
                'fathers_day': ['هدية يوم الأب', 'هدية أبي', 'عيد الأب', 'أبي العزيز'],
                'wedding_season': ['هدية زفاف', 'موسم الأعراس', 'هدايا العرس', 'زفاف سعودي'],
                'graduation_season': ['هدية تخرج', 'موسم التخرج', 'تهنئة التخرج', 'نجاح وتفوق']
            },
            'in': {
                'diwali': ['diwali gift', 'festival of lights', 'deepavali', 'diwali hamper', 'lakshmi puja', 'kitchen gift diwali', 'ghar ke liye gift', 'festival cooking gift'],
                'holi': ['holi gift', 'festival of colors', 'rangwali holi', 'holi celebration', 'color festival', 'kitchen holi gift'],
                'navratri': ['navratri gift', 'durga puja', 'nine nights', 'garba', 'dandiya', 'cooking navratri gift'],
                'dussehra': ['dussehra gift', 'vijayadashami', 'victory festival', 'ravan dahan', 'good over evil', 'kitchen dussehra'],
                'karva_chauth': ['karva chauth gift', 'wife gift', 'fasting gift', 'married women festival', 'patni ke liye gift', 'kitchen karva chauth'],
                'raksha_bandhan': ['rakhi gift', 'brother sister', 'raksha bandhan', 'sibling love', 'bhai gift', 'bhai ke liye kitchen gift'],
                'janmashtami': ['janmashtami gift', 'krishna jayanti', 'lord krishna', 'gokulashtami', 'krishna birthday', 'kitchen janmashtami'],
                'ganesha_chaturthi': ['ganesh chaturthi', 'lord ganesha', 'vinayaka chavithi', 'modak', 'elephant god', 'kitchen ganesh gift'],
                'wedding_season': ['wedding gift', 'shaadi gift', 'marriage gift', 'dulhan gift', 'couple gift', 'shaadi ka tohfa', 'kitchen shaadi gift', 'new bride gift', 'ghar basane gift'],
                'housewarming': ['housewarming gift', 'griha pravesh', 'new home gift', 'ghar warming gift', 'kitchen naya ghar', 'home blessing gift'],
                'birthday': ['birthday gift', 'janmadin gift', 'happy birthday', 'bday gift', 'celebration', 'kitchen birthday gift'],
                'anniversary': ['anniversary gift', 'wedding anniversary', 'love anniversary', 'couple gift', 'relationship', 'kitchen anniversary'],
                'mothers_day': ['mothers day gift', 'mom gift', 'mata gift', 'mother love', 'best mom', 'mummy ke liye gift', 'kitchen mom gift'],
                'fathers_day': ['fathers day gift', 'dad gift', 'papa gift', 'father love', 'best dad', 'papa ke liye gift'],
                'republic_day': ['republic day gift', 'january 26', 'tricolor', 'indian flag', 'patriotic', 'desh bhakti gift'],
                'independence_day': ['independence day', 'august 15', 'freedom fighter', 'indian independence', 'flag hoisting', 'azadi gift'],
                'valentines_day': ['valentine gift', 'love gift', 'romantic gift', 'february 14', 'couple gift', 'pyaar gift'],
                'christmas': ['christmas gift', 'xmas gift', 'santa gift', 'christian festival', 'december 25', 'kitchen christmas'],
                'new_year': ['new year gift', 'happy new year', 'january 1', 'new year resolution', 'celebration', 'naya saal gift'],
                'eid_ul_fitr': ['eid gift', 'ramadan gift', 'muslim festival', 'eid mubarak', 'eid celebration', 'kitchen eid gift'],
                'eid_ul_adha': ['eid ul adha', 'bakrid gift', 'qurbani eid', 'sacrifice festival', 'muslim eid', 'kitchen bakrid'],
                'big_billion_days': ['flipkart sale', 'big billion days', 'festival sale', 'discount offer', 'mega sale', 'kitchen sale'],
                'great_indian_festival': ['amazon sale', 'great indian festival', 'festival offers', 'diwali sale', 'mega discount', 'kitchen festival sale']
            }
        }
        
        market_keywords = keywords.get(marketplace, {})
        return market_keywords.get(occasion, [])
    
    def should_include_occasion(self, occasion_text, marketplace):
        """Check if occasion should be included for this market"""
        if marketplace == 'us':
            return True  # US can have all occasions
        
        # Remove US-specific occasions from international markets
        occasion_lower = occasion_text.lower()
        for us_occasion in self.us_only_occasions:
            if us_occasion in occasion_lower:
                return False
        
        return True
    
    def get_occasion_emotional_hooks(self, occasion, marketplace):
        """Get culturally appropriate emotional hooks for occasions"""
        hooks = {
            'de': {
                'weihnachten': [
                    "Machen Sie Weihnachten unvergesslich",
                    "Das perfekte Geschenk unterm Weihnachtsbaum",
                    "Bringen Sie Kinderaugen zum Leuchten"
                ],
                'muttertag': [
                    "Zeigen Sie Mama, wie wichtig sie ist",
                    "Weil Mama die Beste ist",
                    "Ein Dankeschön für alles, was Mama tut"
                ]
            },
            'fr': {
                'noel': [
                    "Rendez Noël magique",
                    "Le cadeau parfait sous le sapin",
                    "Faites briller les yeux de vos proches"
                ],
                'fete_des_meres': [
                    "Montrez à maman qu'elle est unique",
                    "Parce que maman le mérite",
                    "Un merci pour tout ce que maman fait"
                ]
            },
            'it': {
                'natale': [
                    "Rendi il Natale indimenticabile",
                    "Il regalo perfetto sotto l'albero",
                    "Fai brillare gli occhi dei tuoi cari"
                ],
                'festa_della_mamma': [
                    "Mostra alla mamma quanto è speciale",
                    "Perché la mamma è unica",
                    "Un grazie per tutto quello che fa la mamma"
                ]
            },
            'es': {
                'navidad': [
                    "Haz que la Navidad sea inolvidable",
                    "El regalo perfecto bajo el árbol",
                    "Ilumina los ojos de tus seres queridos"
                ],
                'reyes_magos': [
                    "El regalo que los Reyes Magos aprobarían",
                    "Sorprende el 6 de enero",
                    "La ilusión de los Reyes Magos"
                ],
                'dia_de_la_madre': [
                    "Demuestra a mamá lo especial que es",
                    "Porque mamá se lo merece todo",
                    "Un gracias por todo lo que hace mamá"
                ]
            },
            'jp': {
                'oshogatsu': [
                    "新年を特別なものにするために",
                    "新しい年の始まりにふさわしい品質",
                    "ご家族みんなに喜ばれるギフト"
                ],
                'kurisumasu': [
                    "大切な方への特別なプレゼント", 
                    "クリスマスの思い出を美しく彩る",
                    "心からの感謝を込めて"
                ],
                'ochutgen': [
                    "夏のご挨拶に心を込めて",
                    "日頃の感謝の気持ちをお届け",
                    "お世話になった方への真心"
                ],
                'oseibo': [
                    "一年間の感謝を込めて",
                    "年末のご挨拶に最適な品質",
                    "来年もよろしくお願いいたします"
                ],
                'haha_no_hi': [
                    "お母さんへの感謝を形に",
                    "いつもありがとうの気持ちを",
                    "母の日だからこそ特別なものを"
                ],
                'chichi_no_hi': [
                    "お父さんへの感謝を込めて",
                    "いつも頑張るお父さんに",
                    "父の日の特別なプレゼント"
                ],
                'barentain_de': [
                    "特別な人への愛を込めて",
                    "バレンタインにふさわしい品質",
                    "心からの気持ちをお届け"
                ]
            }
        }
        
        market_hooks = hooks.get(marketplace, {})
        return market_hooks.get(occasion, [])