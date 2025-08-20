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
            
            'eg': {  # Egypt
                'ramadan': 'رمضان',  # Ramadan (most important)
                'eid_al_fitr': 'عيد الفطر',  # Eid al-Fitr
                'eid_al_adha': 'عيد الأضحى',  # Eid al-Adha
                'coptic_christmas': 'عيد الميلاد القبطي',  # Coptic Christmas (January 7)
                'sham_el_nessim': 'شم النسيم',  # Sham el-Nessim (Spring festival)
                'milad_nabawi': 'المولد النبوي',  # Prophet's Birthday
                'mother_day': 'عيد الأم',  # Mother's Day (March 21)
                'revolution_day': 'يوم ثورة 25 يناير',  # Revolution Day (January 25)
                'sinai_liberation': 'عيد تحرير سيناء',  # Sinai Liberation Day (April 25)
                'coptic_easter': 'عيد القيامة القبطي',  # Coptic Easter
                'isra_miraj': 'الإسراء والمعراج',  # Night Journey
                'ashura': 'عاشوراء',  # Day of Ashura
                'laylat_al_qadr': 'ليلة القدر',  # Night of Power
                'wedding_season': 'موسم الأعراس',  # Wedding Season
                'graduation': 'التخرج',  # Graduation
                'engagement': 'الخطوبة',  # Engagement
                'baby_shower': 'حفلة استقبال المولود',  # Baby Shower
                'housewarming': 'احتفال المنزل الجديد',  # Housewarming
                'birthday': 'عيد ميلاد',  # Birthday
                'anniversary': 'ذكرى سنوية',  # Anniversary
                'new_year': 'رأس السنة الميلادية',  # New Year
                'valentine_day': 'عيد الحب',  # Valentine's Day
                'father_day': 'عيد الأب',  # Father's Day
                'teachers_day': 'يوم المعلم',  # Teachers Day
                'womens_day': 'يوم المرأة العالمي',  # International Women's Day
                'children_day': 'يوم الطفل',  # Children's Day
                'youth_day': 'يوم الشباب',  # Youth Day
                'back_to_school': 'العودة للمدارس',  # Back to School
                'summer_vacation': 'أجازة الصيف',  # Summer Vacation
                'winter_season': 'فصل الشتاء',  # Winter Season
                'spring_season': 'فصل الربيع',  # Spring Season
                'nile_flood': 'فيضان النيل',  # Nile Flood (historical)
                'pharaonic_heritage': 'التراث الفرعوني',  # Pharaonic Heritage
                'cairo_festival': 'مهرجان القاهرة',  # Cairo Festival
                'family_gathering': 'تجمع العائلة',  # Family Gathering
                'ramadan_iftar': 'إفطار رمضان',  # Ramadan Iftar
                'ramadan_suhoor': 'سحور رمضان',  # Ramadan Suhoor
                'black_friday': 'الجمعة السوداء',  # Black Friday
                'cyber_monday': 'الاثنين الإلكتروني',  # Cyber Monday
                'weekend': 'نهاية الأسبوع',  # Weekend
                'vacation': 'إجازة',  # Vacation
                'business_meeting': 'اجتماع عمل',  # Business Meeting
                'office_gift': 'هدية المكتب',  # Office Gift
                'egyptian_culture': 'الثقافة المصرية',  # Egyptian Culture
                'alexandria_heritage': 'تراث الإسكندرية',  # Alexandria Heritage
                'coptic_culture': 'الثقافة القبطية'  # Coptic Culture
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
            },
            
            'pl': {  # Poland
                'boze_narodzenie': 'Boże Narodzenie',  # Christmas (most important Polish celebration)
                'wielkanoc': 'Wielkanoc',  # Easter (major Polish holiday)
                'swieto_niepodleglosci': 'Święto Niepodległości',  # Independence Day (November 11)
                'swieto_konstytucji': 'Święto Konstytucji 3 Maja',  # Constitution Day (May 3)
                'dzien_matki': 'Dzień Matki',  # Mother's Day (May 26)
                'dzien_ojca': 'Dzień Ojca',  # Father's Day (June 23)
                'dzien_dziecka': 'Dzień Dziecka',  # Children's Day (June 1)
                'walentynki': 'Walentynki',  # Valentine's Day
                'andrzejki': 'Andrzejki',  # St. Andrew's Day (November 30)
                'mikolajki': 'Mikołajki',  # St. Nicholas Day (December 6)
                'nowy_rok': 'Nowy Rok',  # New Year
                'sylwester': 'Sylwester',  # New Year's Eve
                'dzien_babci': 'Dzień Babci',  # Grandmother's Day (January 21)
                'dzien_dziadka': 'Dzień Dziadka',  # Grandfather's Day (January 22)
                'dzien_kobiet': 'Dzień Kobiet',  # Women's Day (March 8)
                'dzien_nauczyciela': 'Dzień Nauczyciela',  # Teacher's Day (October 14)
                'wszystkich_swietych': 'Wszystkich Świętych',  # All Saints' Day (November 1)
                'zaduszki': 'Zaduszki',  # All Souls' Day (November 2)
                'wigilia': 'Wigilia',  # Christmas Eve
                'trzech_kroli': 'Trzech Króli',  # Epiphany (January 6)
                'tlusty_czwartek': 'Tłusty Czwartek',  # Fat Thursday
                'powrot_do_szkoly': 'Powrót do Szkoły',  # Back to School
                'urlop_letni': 'Urlop Letni',  # Summer Vacation
                'ferie_zimowe': 'Ferie Zimowe',  # Winter Break
                'slub': 'Ślub',  # Wedding
                'wesele': 'Wesele',  # Wedding Reception
                'chrzciny': 'Chrzciny',  # Baptism
                'pierwsza_komunia': 'Pierwsza Komunia',  # First Communion
                'bierzmowanie': 'Bierzmowanie',  # Confirmation
                'studniowka': 'Studniówka',  # Prom/100 days before graduation
                'matura': 'Matura',  # High School Finals
                'promocja': 'Promocja',  # University Graduation
                'urodziny': 'Urodziny',  # Birthday
                'rocznica': 'Rocznica',  # Anniversary
                'imieniny': 'Imieniny',  # Name Day (very important in Poland)
                'baby_shower': 'Baby Shower',  # Baby Shower
                'panieński': 'Wieczór Panieński',  # Bachelorette Party
                'kawalerski': 'Wieczór Kawalerski',  # Bachelor Party
                'housewarming': 'Parapetówka',  # Housewarming
                'black_friday': 'Black Friday',  # Black Friday
                'cyber_monday': 'Cyber Monday',  # Cyber Monday
                'lato': 'Lato',  # Summer
                'zima': 'Zima',  # Winter
                'wiosna': 'Wiosna',  # Spring
                'jesien': 'Jesień',  # Autumn
                'weekend': 'Weekend',  # Weekend
                'wakacje': 'Wakacje',  # Holidays
                'majowka': 'Majówka',  # May holidays (long weekend)
                'euro_mistrzostwa': 'Euro/Mistrzostwa Świata',  # European/World Championship
                'reprezentacja': 'Mecz Reprezentacji',  # National team match
                'dzien_flagi': 'Dzień Flagi',  # Flag Day (May 2)
                'dzien_polonii': 'Dzień Polonii'  # Polonia Day (May 2)
            },
            
            'be': {  # Belgium
                'noel': 'Noël',  # Christmas (most important Belgian celebration)
                'saint_valentin': 'Saint-Valentin',  # Valentine's Day
                'paques': 'Pâques',  # Easter (major Belgian holiday)
                'fete_des_meres': 'Fête des Mères',  # Mother's Day (second Sunday of May)
                'fete_des_peres': 'Fête des Pères',  # Father's Day (second Sunday of June)
                'fete_nationale': 'Fête Nationale Belge',  # Belgian National Day (July 21)
                'jour_de_lan': "Jour de l'An",  # New Year's Day
                'saint_nicolas': 'Saint-Nicolas',  # St. Nicholas Day (December 6)
                'epiphanie': 'Épiphanie',  # Epiphany (January 6)
                'ascension': 'Ascension',  # Ascension Day
                'pentecote': 'Pentecôte',  # Whit Monday
                'assomption': 'Assomption',  # Assumption of Mary (August 15)
                'toussaint': 'Toussaint',  # All Saints' Day (November 1)
                'armistice': 'Armistice',  # Armistice Day (November 11)
                'rentree_scolaire': 'Rentrée Scolaire',  # Back to School
                'soldes_hiver': "Soldes d'Hiver",  # Winter Sales
                'soldes_ete': "Soldes d'Été",  # Summer Sales
                'black_friday': 'Black Friday',  # Black Friday
                'cyber_monday': 'Cyber Monday',  # Cyber Monday
                'carnaval': 'Carnaval',  # Carnival (Binche and other Belgian carnivals)
                'ducasse': 'Ducasse',  # Local festivals (Mons, Ath)
                'ommegang': 'Ommegang',  # Brussels Historical Pageant
                'gentse_feesten': 'Gentse Feesten',  # Ghent Festival (if targeting Flemish)
                'braderie': 'Braderie',  # Street sales/markets
                'kermesse': 'Kermesse',  # Village fair
                'communion': 'Première Communion',  # First Communion
                'confirmation': 'Confirmation',  # Confirmation
                'mariage': 'Mariage',  # Wedding
                'anniversaire': 'Anniversaire',  # Anniversary
                'anniversaire_naissance': 'Anniversaire de Naissance',  # Birthday
                'pendaison_cremaillere': 'Pendaison de Crémaillère',  # Housewarming
                'diplome': 'Remise de Diplôme',  # Graduation
                'retraite': 'Départ en Retraite',  # Retirement
                'week_end': 'Week-end',  # Weekend
                'vacances_ete': "Vacances d'Été",  # Summer Holidays
                'vacances_hiver': "Vacances d'Hiver",  # Winter Holidays
                'vacances_paques': 'Vacances de Pâques',  # Easter Holidays
                'euro_football': "Championnat d'Europe de Football",  # European Football Championship
                'diables_rouges': 'Diables Rouges',  # Belgian National Football Team
                'printemps': 'Printemps',  # Spring
                'ete': 'Été',  # Summer
                'automne': 'Automne',  # Autumn
                'hiver': 'Hiver'  # Winter
            },
            
            'sg': {  # Singapore
                'chinese_new_year': 'Chinese New Year',  # Most important celebration in Singapore
                'chinese_valentine': "Chinese Valentine's Day",  # Qixi Festival
                'valentines_day': "Valentine's Day",  # Valentine's Day
                'mothers_day': "Mother's Day",  # Mother's Day (second Sunday of May)
                'fathers_day': "Father's Day",  # Father's Day (third Sunday of June)
                'national_day': 'National Day',  # Singapore National Day (August 9)
                'new_year': "New Year's Day",  # New Year's Day
                'deepavali': 'Deepavali',  # Festival of Lights (October/November)
                'hari_raya_puasa': 'Hari Raya Puasa',  # Eid al-Fitr
                'hari_raya_haji': 'Hari Raya Haji',  # Eid al-Adha
                'christmas': 'Christmas',  # Christmas
                'good_friday': 'Good Friday',  # Good Friday
                'vesak_day': 'Vesak Day',  # Buddha's Birthday
                'labour_day': 'Labour Day',  # May 1
                'back_to_school': 'Back to School',  # School term starts
                'mid_autumn_festival': 'Mid-Autumn Festival',  # Mooncake Festival
                'dragon_boat_festival': 'Dragon Boat Festival',  # Duanwu Festival
                'hungry_ghost_festival': 'Hungry Ghost Festival',  # Zhongyuan Festival
                'black_friday': 'Black Friday',  # Black Friday
                'cyber_monday': 'Cyber Monday',  # Cyber Monday
                'singles_day': "Singles' Day",  # 11.11 Shopping Festival
                'great_singapore_sale': 'Great Singapore Sale',  # Annual shopping event
                'f1_singapore_gp': 'Formula 1 Singapore Grand Prix',  # F1 race weekend
                'singapore_food_festival': 'Singapore Food Festival',  # Food culture celebration
                'chingay_parade': 'Chingay Parade',  # Street parade after CNY
                'hungry_ghost_month': 'Hungry Ghost Month',  # Seventh lunar month
                'mooncake_season': 'Mooncake Season',  # Leading up to Mid-Autumn
                'wedding_season': 'Wedding Season',  # Popular wedding periods
                'graduation_season': 'Graduation Season',  # School/university graduations
                'housewarming': 'Housewarming',  # New home celebrations
                'baby_shower': 'Baby Shower',  # Baby celebrations
                'birthday': 'Birthday',  # Birthday celebrations
                'anniversary': 'Anniversary',  # Wedding anniversaries
                'retirement': 'Retirement',  # Retirement celebrations
                'promotion': 'Job Promotion',  # Career advancement
                'weekend': 'Weekend',  # Weekend gatherings
                'public_holiday': 'Public Holiday',  # General public holidays
                'school_holiday': 'School Holiday',  # School vacation periods
                'monsoon_season': 'Monsoon Season',  # Rainy season (Nov-Jan)
                'dry_season': 'Dry Season',  # Hot season (Feb-Apr)
                'haze_season': 'Haze Season',  # Seasonal haze period
                'durian_season': 'Durian Season',  # Durian fruit season
                'year_end_bonus': 'Year-End Bonus',  # 13th month bonus period
                'cny_bonus': 'CNY Bonus',  # Chinese New Year bonus
                'exam_season': 'Exam Season',  # School examination periods
                'ns_enlistment': 'NS Enlistment',  # National Service
                'university_admission': 'University Admission',  # Higher education
                'job_hunting': 'Job Hunting',  # Employment search
                'property_viewing': 'Property Viewing',  # Real estate
                'renovation': 'Home Renovation',  # Home improvement
                'staycation': 'Staycation',  # Local vacation
                'overseas_travel': 'Overseas Travel'  # International travel
            },
            
            'uk': {  # United Kingdom
                'boxing_day': 'Boxing Day',  # December 26 - Major shopping day
                'christmas': 'Christmas',  # December 25 - Most important UK celebration
                'bonfire_night': 'Bonfire Night',  # November 5 - Guy Fawkes Night
                'remembrance_day': 'Remembrance Day',  # November 11 - Poppy Day
                'burns_night': 'Burns Night',  # January 25 - Scottish celebration
                'st_patricks_day': "St Patrick's Day",  # March 17 - Irish celebration
                'easter': 'Easter',  # Easter Sunday and Monday
                'bank_holiday': 'Bank Holiday',  # Various UK bank holidays
                'mothers_day': 'Mothering Sunday',  # Fourth Sunday of Lent
                'fathers_day': "Father's Day",  # Third Sunday of June
                'valentines_day': "Valentine's Day",  # February 14
                'halloween': 'Halloween',  # October 31
                'new_year': "New Year's Day",  # January 1
                'hogmanay': 'Hogmanay',  # Scottish New Year's Eve
                'pancake_day': 'Pancake Day',  # Shrove Tuesday
                'queens_birthday': "Queen's Official Birthday",  # June celebration
                'st_georges_day': "St George's Day",  # April 23 - England's patron saint
                'st_andrews_day': "St Andrew's Day",  # November 30 - Scotland's patron saint
                'st_davids_day': "St David's Day",  # March 1 - Wales' patron saint
                'black_friday': 'Black Friday',  # November shopping event
                'cyber_monday': 'Cyber Monday',  # Online shopping Monday
                'january_sales': 'January Sales',  # Post-Christmas sales
                'summer_sales': 'Summer Sales',  # July-August sales
                'back_to_school': 'Back to School',  # September term start
                'freshers_week': "Freshers' Week",  # University start
                'graduation': 'Graduation Season',  # University ceremonies
                'wedding_season': 'Wedding Season',  # May-September
                'henley_regatta': 'Henley Royal Regatta',  # July rowing event
                'wimbledon': 'Wimbledon Championships',  # Tennis tournament
                'royal_ascot': 'Royal Ascot',  # Horse racing event
                'chelsea_flower': 'Chelsea Flower Show',  # May gardening event
                'edinburgh_festival': 'Edinburgh Festival',  # August arts festival
                'notting_hill': 'Notting Hill Carnival',  # August Caribbean festival
                'glastonbury': 'Glastonbury Festival',  # Music festival
                'six_nations': 'Six Nations Rugby',  # Rugby championship
                'fa_cup_final': 'FA Cup Final',  # Football cup final
                'premier_league': 'Premier League Season',  # Football season
                'cricket_season': 'Cricket Season',  # Summer cricket
                'the_ashes': 'The Ashes',  # Cricket series
                'grand_national': 'Grand National',  # Horse racing
                'boat_race': 'The Boat Race',  # Oxford vs Cambridge
                'commonwealth_day': 'Commonwealth Day',  # March celebration
                'harvest_festival': 'Harvest Festival',  # Autumn celebration
                'diwali': 'Diwali',  # Festival of Lights
                'eid': 'Eid Celebrations',  # Muslim celebrations
                'chinese_new_year': 'Chinese New Year',  # Lunar New Year
                'pride': 'Pride Month',  # June LGBTQ+ celebrations
                'movember': 'Movember',  # November men's health
                'comic_relief': 'Comic Relief',  # Red Nose Day
                'children_in_need': 'Children in Need',  # BBC charity event
                'poppy_appeal': 'Poppy Appeal',  # Remembrance charity
                'jubilee': 'Jubilee Celebrations',  # Royal celebrations
                'coronation': 'Coronation Events',  # Royal events
                'royal_wedding': 'Royal Wedding',  # Royal family weddings
                'birthday': 'Birthday',  # Personal birthdays
                'anniversary': 'Anniversary',  # Wedding anniversaries
                'retirement': 'Retirement',  # Career milestone
                'housewarming': 'Housewarming',  # New home celebration
                'baby_shower': 'Baby Shower',  # Expecting celebration
                'christening': 'Christening',  # Baby baptism
                'communion': 'First Communion',  # Religious milestone
                'bar_mitzvah': 'Bar/Bat Mitzvah',  # Jewish celebration
                'weekend': 'Weekend',  # Weekend activities
                'pub_night': 'Pub Night',  # British pub culture
                'sunday_roast': 'Sunday Roast',  # Traditional Sunday meal
                'afternoon_tea': 'Afternoon Tea',  # British tea tradition
                'garden_party': 'Garden Party',  # Summer entertaining
                'bbq_season': 'BBQ Season',  # British summer BBQs
                'staycation': 'Staycation',  # UK holidays
                'half_term': 'Half Term Holiday',  # School break
                'summer_holiday': 'Summer Holidays'  # School summer break
            },
            
            'au': {  # Australia
                'australia_day': 'Australia Day',  # January 26 - Most important national celebration
                'anzac_day': 'ANZAC Day',  # April 25 - Remembrance day
                'queens_birthday': "Queen's Birthday",  # Second Monday in June (varies by state)
                'melbourne_cup': 'Melbourne Cup Day',  # First Tuesday in November
                'christmas': 'Christmas',  # December 25
                'boxing_day': 'Boxing Day',  # December 26 - Major shopping day
                'new_year': "New Year's Day",  # January 1
                'good_friday': 'Good Friday',  # Good Friday
                'easter_monday': 'Easter Monday',  # Easter Monday
                'labour_day': 'Labour Day',  # Varies by state (March/May/October)
                'mothers_day': "Mother's Day",  # Second Sunday of May
                'fathers_day': "Father's Day",  # First Sunday of September
                'valentines_day': "Valentine's Day",  # February 14
                'black_friday': 'Black Friday',  # Black Friday sales
                'cyber_monday': 'Cyber Monday',  # Cyber Monday online sales
                'click_frenzy': 'Click Frenzy',  # Major Australian online shopping event
                'end_of_financial_year': 'End of Financial Year',  # June 30 - EOFY sales
                'back_to_school': 'Back to School',  # February school term starts
                'footy_season': 'Footy Season',  # AFL/NRL season
                'spring_racing_carnival': 'Spring Racing Carnival',  # Melbourne racing season
                'grand_final_day': 'Grand Final Day',  # AFL Grand Final (September/October)
                'state_of_origin': 'State of Origin',  # Rugby League series
                'cricket_season': 'Cricket Season',  # Summer cricket season
                'big_bash_league': 'Big Bash League',  # Cricket T20 competition
                'tennis_open': 'Australian Open',  # Tennis Grand Slam (January)
                'formula_1_gp': 'Formula 1 Australian Grand Prix',  # F1 race (March/April)
                'easter_show': 'Royal Easter Show',  # Agricultural shows
                'schoolies_week': 'Schoolies Week',  # Post-graduation celebrations
                'wedding_season': 'Wedding Season',  # Spring/Summer weddings
                'graduation_season': 'Graduation Season',  # University graduations
                'housewarming': 'Housewarming',  # New home celebrations
                'baby_shower': 'Baby Shower',  # Baby celebrations
                'birthday': 'Birthday',  # Birthday celebrations
                'anniversary': 'Anniversary',  # Wedding anniversaries
                'retirement': 'Retirement',  # Retirement celebrations
                'promotion': 'Job Promotion',  # Career advancement
                'weekend': 'Weekend',  # Weekend gatherings
                'public_holiday': 'Public Holiday',  # Long weekends
                'school_holiday': 'School Holidays',  # Term break periods
                'summer_season': 'Summer Season',  # December-February
                'winter_season': 'Winter Season',  # June-August
                'bushfire_season': 'Bushfire Season',  # Fire danger period
                'cyclone_season': 'Cyclone Season',  # Tropical cyclone season
                'drought_season': 'Drought Season',  # Dry periods
                'flood_season': 'Flood Season',  # Wet season
                'tax_time': 'Tax Time',  # July-October tax returns
                'bonus_season': 'Bonus Season',  # End of year bonuses
                'harvest_season': 'Harvest Season',  # Agricultural harvest
                'camping_season': 'Camping Season',  # Outdoor recreation
                'fishing_season': 'Fishing Season',  # Recreational fishing
                'surfing_season': 'Surfing Season',  # Peak surf conditions
                'road_trip_season': 'Road Trip Season',  # Travel season
                'festival_season': 'Festival Season',  # Music and arts festivals
                'outback_travel': 'Outback Travel',  # Inland exploration
                'reef_diving_season': 'Reef Diving Season',  # Great Barrier Reef
                'wine_harvest': 'Wine Harvest',  # Vintage season
                'farmers_market': 'Farmers Market Season'  # Local produce markets
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
            'eg': {
                'ramadan': ['رمضان مبارك', 'شهر رمضان', 'رمضان كريم', 'إفطار رمضان', 'سحور رمضان', 'المائدة المصرية'],
                'eid_al_fitr': ['هدية عيد الفطر', 'عيد الفطر المبارك', 'هدايا العيد', 'عيدية', 'فرحة العيد', 'كحك العيد'],
                'eid_al_adha': ['هدية عيد الأضحى', 'عيد الأضحى المبارك', 'أضحى مبارك', 'عيد الحج', 'عيد القربان', 'الأضحية'],
                'sham_el_nessim': ['شم النسيم', 'عيد الربيع', 'فسيخ ورنجة', 'نزهة شم النسيم', 'التراث المصري'],
                'coptic_christmas': ['عيد الميلاد المجيد', 'الكريسماس القبطي', 'هدية عيد الميلاد', 'احتفال قبطي'],
                'mother_day': ['هدية عيد الأم', 'هدية أمي', 'عيد الأم', 'أمي الحبيبة', 'المرأة المصرية'],
                'wedding_season': ['هدية زفاف', 'عرس مصري', 'هدايا العرس', 'زفة مصرية', 'ليلة الحناء'],
                'graduation': ['هدية تخرج', 'تهنئة التخرج', 'نجاح وتفوق', 'فرحة التخرج', 'دفعة جديدة'],
                'revolution_day': ['ثورة 25 يناير', 'اليوم الوطني', 'الثورة المصرية', 'فخر مصري'],
                'sinai_liberation': ['تحرير سيناء', 'النصر المصري', 'الجيش المصري', 'أرض مصر'],
                'coptic_easter': ['عيد القيامة', 'عيد الفصح', 'احتفال مسيحي', 'فرحة القيامة'],
                'housewarming': ['احتفال المنزل الجديد', 'بيت جديد', 'هدية البيت', 'تهنئة المنزل'],
                'engagement': ['خطوبة مصرية', 'هدية خطوبة', 'ليلة الخطوبة', 'فرحة الخطوبة'],
                'baby_shower': ['حفلة استقبال المولود', 'هدية المولود', 'البيبي الجديد', 'فرحة الولادة'],
                'birthday': ['عيد ميلاد', 'هدية عيد ميلاد', 'حفلة عيد ميلاد', 'فرحة الميلاد'],
                'anniversary': ['ذكرى سنوية', 'عيد زواج', 'ذكرى الزواج', 'احتفال سنوي'],
                'new_year': ['رأس السنة', 'سنة جديدة سعيدة', 'هدية رأس السنة', 'احتفال السنة الجديدة'],
                'valentine_day': ['عيد الحب', 'هدية عيد الحب', 'فالنتاين', 'حب ورومانسية'],
                'father_day': ['عيد الأب', 'هدية أبي', 'بابا العزيز', 'تقدير الأب'],
                'teachers_day': ['يوم المعلم', 'هدية المعلم', 'تقدير المعلم', 'شكر للمعلم'],
                'womens_day': ['يوم المرأة', 'تكريم المرأة', 'المرأة المصرية', 'فخر المرأة'],
                'children_day': ['يوم الطفل', 'هدية الأطفال', 'فرحة الطفولة', 'حب الأطفال'],
                'back_to_school': ['العودة للمدارس', 'بداية العام الدراسي', 'هدية المدرسة', 'تحضير المدرسة'],
                'pharaonic_heritage': ['التراث الفرعوني', 'الحضارة المصرية', 'أهرامات مصر', 'عظمة مصر'],
                'nile_flood': ['فيضان النيل', 'بركة النيل', 'خير النيل', 'نهر الحياة'],
                'cairo_festival': ['مهرجان القاهرة', 'فعاليات القاهرة', 'ثقافة مصرية', 'تراث القاهرة'],
                'alexandria_heritage': ['تراث الإسكندرية', 'عروس البحر المتوسط', 'إسكندرية التاريخية'],
                'coptic_culture': ['الثقافة القبطية', 'التراث القبطي', 'المسيحية في مصر'],
                'family_gathering': ['تجمع العائلة', 'لم الشمل', 'فرحة العائلة', 'حب الأهل'],
                'ramadan_iftar': ['إفطار رمضان', 'مائدة الإفطار', 'روحانية رمضان', 'إفطار جماعي'],
                'black_friday': ['الجمعة السوداء', 'تخفيضات كبيرة', 'عروض مميزة', 'تسوق ذكي'],
                'weekend': ['نهاية الأسبوع', 'استراحة الأسبوع', 'وقت العائلة', 'راحة واسترخاء'],
                'vacation': ['إجازة صيفية', 'عطلة سعيدة', 'سفر وترفيه', 'راحة واستجمام']
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
            },
            'pl': {
                'boze_narodzenie': ['prezent świąteczny', 'boże narodzenie prezent', 'wigilia prezent', 'choinka prezent', 'mikołaj prezent'],
                'wielkanoc': ['prezent wielkanocny', 'wielkanoc prezent', 'śmigus dyngus', 'święcone prezent', 'zajączek wielkanocny'],
                'dzien_matki': ['prezent dzień matki', 'prezent dla mamy', 'mama prezent', 'dzień matki prezent', 'podziękowanie mama'],
                'dzien_ojca': ['prezent dzień ojca', 'prezent dla taty', 'tata prezent', 'dzień ojca prezent', 'podziękowanie tata'],
                'dzien_dziecka': ['prezent dzień dziecka', 'prezent dla dzieci', 'dziecko prezent', 'radość dziecka', 'zabawa dla dzieci'],
                'walentynki': ['prezent walentynkowy', 'walentynki prezent', 'prezent miłosny', 'romantyczny prezent', 'dla ukochanej'],
                'imieniny': ['prezent imieninowy', 'imieniny prezent', 'z okazji imienin', 'imieniny życzenia', 'święto imion'],
                'slub': ['prezent ślubny', 'ślub prezent', 'prezent weselny', 'para młoda prezent', 'wesele prezent'],
                'urodziny': ['prezent urodzinowy', 'urodziny prezent', 'z okazji urodzin', 'tort urodzinowy', 'świętowanie urodzin'],
                'pierwsza_komunia': ['prezent komunijny', 'pierwsza komunia prezent', 'komunia święta', 'pamiątka komunia', 'dziecko komunia'],
                'studniowka': ['prezent studniówka', 'studniówka prezent', 'bal maturalny', 'elegancki prezent', 'młodzież prezent'],
                'matura': ['prezent maturalny', 'matura prezent', 'egzamin prezent', 'sukces matura', 'absolwent prezent'],
                'swieto_niepodleglosci': ['prezent patriotyczny', 'polska niepodległość', 'biało czerwony', 'polska tradycja', 'dumny polak'],
                'andrzejki': ['prezent andrzejki', 'andrzejki prezent', 'wróżby andrzejki', 'tradycja polska', 'zabawa andrzejki'],
                'mikolajki': ['prezent mikołajki', 'mikołajki prezent', 'święty mikołaj', 'buty pod choinkę', 'dzieci mikołaj'],
                'powrot_do_szkoly': ['przybory szkolne', 'szkoła prezent', 'plecak szkolny', 'ucznia prezent', 'rok szkolny'],
                'sylwester': ['prezent sylwestrowy', 'sylwester prezent', 'nowy rok prezent', 'zabawa sylwestrowa', 'noworoczny prezent'],
                'black_friday': ['black friday polska', 'promocja black friday', 'wyprzedaż black friday', 'okazja zakupy', 'taniej zakupy'],
                'weekend': ['prezent weekend', 'relaks weekend', 'odpoczynek prezent', 'wolny czas', 'rodzina czas'],
                'wakacje': ['prezent wakacyjny', 'wakacje prezent', 'urlop prezent', 'lato prezent', 'podróż prezent'],
                'parapetówka': ['prezent parapetówka', 'nowe mieszkanie', 'dom prezent', 'housewarming prezent', 'nowy dom prezent'],
                'baby_shower': ['prezent baby shower', 'dziecko w drodze', 'przyszła mama', 'noworodek prezent', 'brzuszek prezent']
            },
            'be': {
                'noel': ['cadeau noël', 'cadeau de noël', 'idée cadeau noël', 'père noël', 'réveillon de noël', 'sapin de noël', "fêtes de fin d'année"],
                'saint_valentin': ['cadeau saint valentin', 'cadeau amour', 'cadeau romantique', 'cadeau couple', 'idée cadeau saint valentin', 'amoureux cadeau'],
                'paques': ['cadeau pâques', 'cadeau de pâques', 'lapin de pâques', 'œufs de pâques', 'chocolats pâques', 'fêtes de pâques'],
                'fete_des_meres': ['cadeau fête des mères', 'cadeau maman', 'idée cadeau maman', 'cadeau mère', 'bonne fête maman', 'maman adorée'],
                'fete_des_peres': ['cadeau fête des pères', 'cadeau papa', 'idée cadeau papa', 'cadeau père', 'bonne fête papa', 'papa adoré'],
                'fete_nationale': ['cadeau fête nationale belge', 'belgique fête', 'fierté belge', 'tradition belge', '21 juillet belgique'],
                'saint_nicolas': ['cadeau saint nicolas', 'saint nicolas belgique', 'tradition saint nicolas', 'enfants saint nicolas', 'père noël belge'],
                'communion': ['cadeau première communion', 'communion solennelle', 'cadeau communion', 'tradition catholique', 'communion belge'],
                'mariage': ['cadeau mariage', 'cadeau de mariage', 'liste mariage', 'noces', 'félicitations mariage', 'couple belge'],
                'anniversaire': ['cadeau anniversaire', "cadeau d'anniversaire", 'fête anniversaire', 'joyeux anniversaire', 'surprise anniversaire'],
                'diplome': ['cadeau diplôme', 'remise diplôme', 'félicitations diplôme', 'cadeau graduation', 'succès scolaire', 'réussite études'],
                'pendaison_cremaillere': ['cadeau pendaison crémaillère', 'nouveau logement', 'nouvelle maison', 'emménagement', 'bienvenue maison'],
                'carnaval': ['cadeau carnaval', 'carnaval binche', 'tradition carnaval', 'fête carnaval', 'carnaval belge', 'déguisement carnaval'],
                'ducasse': ['cadeau ducasse', 'tradition ducasse', 'fête locale belge', 'folklore belge', 'culture belge'],
                'diables_rouges': ['cadeau diables rouges', 'équipe belgique', 'football belge', 'supporter belgique', 'fierté belge football'],
                'soldes_hiver': ['cadeau soldes hiver', 'bonnes affaires hiver', 'promotions hiver', 'réductions hiver'],
                'soldes_ete': ['cadeau soldes été', 'bonnes affaires été', 'promotions été', 'réductions été'],
                'black_friday': ['black friday belgique', 'promotions black friday', 'bonnes affaires black friday', 'shopping black friday'],
                'week_end': ['cadeau week-end', 'détente week-end', 'famille week-end', 'repos week-end', 'plaisir week-end'],
                'vacances_ete': ['cadeau vacances été', 'vacances famille', 'plaisir vacances', 'détente été', 'congés été'],
                'rentree_scolaire': ['cadeau rentrée scolaire', 'nouvelle année scolaire', 'école cadeau', 'enfant école', 'rentrée septembre']
            },
            'sg': {
                'chinese_new_year': ['cny gift', 'chinese new year gift', 'ang bao gift', 'reunion dinner gift', 'auspicious gift', 'prosperity gift', 'red packet gift'],
                'chinese_valentine': ['chinese valentine gift', 'qixi gift', 'romantic gift', 'couple gift', 'love gift'],
                'valentines_day': ['valentine gift', 'romantic gift', 'couple gift', 'love gift', 'singapore valentine'],
                'mothers_day': ['mothers day gift', 'mom gift', 'mother gift', 'mama gift', 'singapore mom'],
                'fathers_day': ['fathers day gift', 'dad gift', 'father gift', 'papa gift', 'singapore dad'],
                'national_day': ['national day gift', 'singapore national day', 'ndp gift', 'patriotic gift', 'singapore pride'],
                'deepavali': ['deepavali gift', 'diwali gift', 'festival of lights', 'hindu festival', 'indian celebration'],
                'hari_raya_puasa': ['hari raya gift', 'eid gift', 'muslim festival', 'ramadan gift', 'singapore eid'],
                'hari_raya_haji': ['hari raya haji gift', 'eid adha gift', 'pilgrimage festival', 'sacrifice festival'],
                'christmas': ['christmas gift', 'xmas gift', 'holiday gift', 'singapore christmas', 'festive gift'],
                'mid_autumn_festival': ['mid autumn gift', 'mooncake festival', 'lantern festival', 'chinese festival'],
                'dragon_boat_festival': ['dragon boat gift', 'dumpling festival', 'traditional festival'],
                'singles_day': ['singles day gift', '11.11 gift', 'self gift', 'treat yourself'],
                'great_singapore_sale': ['gss gift', 'singapore sale', 'shopping festival', 'discount gift'],
                'f1_singapore_gp': ['f1 gift', 'racing gift', 'singapore gp', 'motorsport gift'],
                'singapore_food_festival': ['food festival gift', 'culinary gift', 'foodie gift', 'singapore cuisine'],
                'wedding_season': ['wedding gift', 'bridal gift', 'couple gift', 'marriage gift', 'singapore wedding'],
                'graduation_season': ['graduation gift', 'achievement gift', 'success gift', 'student gift'],
                'housewarming': ['housewarming gift', 'new home gift', 'house blessing', 'moving gift'],
                'baby_shower': ['baby shower gift', 'new baby gift', 'pregnancy gift', 'expecting gift'],
                'birthday': ['birthday gift', 'bday gift', 'celebration gift', 'party gift'],
                'anniversary': ['anniversary gift', 'relationship gift', 'milestone gift', 'couple anniversary'],
                'black_friday': ['black friday singapore', 'black friday deals', 'cyber deals', 'online shopping'],
                'year_end_bonus': ['bonus gift', '13th month bonus', 'year end treat', 'reward gift'],
                'cny_bonus': ['cny bonus gift', 'chinese new year bonus', 'festive bonus', 'prosperity bonus'],
                'back_to_school': ['back to school gift', 'school gift', 'student gift', 'education gift'],
                'staycation': ['staycation gift', 'local travel', 'singapore holiday', 'weekend getaway'],
                'durian_season': ['durian season gift', 'fruit lover gift', 'singapore durian', 'tropical fruit']
            },
            'uk': {
                'christmas': ['christmas gift', 'xmas present', 'festive gift', 'christmas stocking', 'secret santa', 'holiday gift', 'christmas must-have'],
                'boxing_day': ['boxing day deals', 'boxing day bargain', 'post-christmas sale', 'boxing day special', 'december sale'],
                'bonfire_night': ['bonfire night gift', 'guy fawkes gift', 'fireworks night', '5th november gift', 'sparkler night present'],
                'mothers_day': ['mothers day gift', 'mothering sunday present', 'mum gift', 'mother present', 'special mum gift'],
                'fathers_day': ['fathers day gift', 'dad gift', 'father present', 'daddy gift', 'special dad present'],
                'easter': ['easter gift', 'easter present', 'easter basket', 'easter sunday gift', 'spring gift'],
                'valentines_day': ['valentine gift', 'romantic gift', 'love present', 'valentine special', 'sweetheart gift'],
                'halloween': ['halloween gift', 'spooky present', 'trick or treat', 'halloween party', 'october 31st gift'],
                'black_friday': ['black friday deal', 'black friday uk', 'november sale', 'black friday bargain', 'mega deals'],
                'january_sales': ['january sale', 'new year sale', 'winter sale', 'january bargain', 'post-christmas clearance'],
                'back_to_school': ['back to school', 'school supplies', 'september start', 'school term', 'student essentials'],
                'wedding_season': ['wedding gift', 'bridal present', 'wedding registry', 'wedding favour', 'marriage gift'],
                'wimbledon': ['wimbledon gift', 'tennis present', 'championship gift', 'strawberries and cream', 'tennis fan gift'],
                'royal_ascot': ['ascot gift', 'racing present', 'royal ascot style', 'race day gift', 'ladies day present'],
                'premier_league': ['football gift', 'premier league present', 'football fan gift', 'match day essential', 'footie gift'],
                'six_nations': ['rugby gift', 'six nations present', 'rugby fan gift', 'match day gift', 'rugby essential'],
                'afternoon_tea': ['afternoon tea gift', 'tea time present', 'british tea gift', 'tea lover present', 'teatime essential'],
                'sunday_roast': ['sunday roast essential', 'sunday dinner gift', 'roast dinner present', 'sunday lunch gift'],
                'pub_night': ['pub night essential', 'pub gift', 'friday night gift', 'pub quiz present', 'local pub gift'],
                'garden_party': ['garden party gift', 'summer party present', 'outdoor entertaining', 'garden essential', 'party host gift'],
                'birthday': ['birthday gift', 'birthday present', 'special day gift', 'birthday surprise', 'celebration gift'],
                'anniversary': ['anniversary gift', 'anniversary present', 'special milestone', 'romantic anniversary', 'celebration present'],
                'graduation': ['graduation gift', 'university present', 'graduation celebration', 'achievement gift', 'degree celebration'],
                'baby_shower': ['baby shower gift', 'expecting present', 'new baby gift', 'baby celebration', 'mum-to-be gift'],
                'retirement': ['retirement gift', 'retirement present', 'farewell gift', 'career milestone', 'retirement celebration']
            },
            'au': {
                'australia_day': ['australia day gift', 'aussie day gift', 'australia day present', 'patriotic gift', 'national day gift', 'fair dinkum gift', 'true blue gift'],
                'anzac_day': ['anzac day gift', 'remembrance gift', 'lest we forget', 'military gift', 'veteran gift', 'commemoration gift', 'respect gift'],
                'queens_birthday': ['queens birthday gift', 'royal celebration', 'long weekend gift', 'monarchy gift', 'british heritage'],
                'melbourne_cup': ['melbourne cup gift', 'horse racing gift', 'cup day gift', 'racing carnival', 'spring racing'],
                'christmas': ['christmas gift', 'xmas gift', 'holiday gift', 'aussie christmas', 'summer christmas', 'festive gift'],
                'boxing_day': ['boxing day gift', 'boxing day sales', 'post christmas gift', 'aussie boxing day', 'summer sale'],
                'anzac_day': ['anzac day gift', 'remembrance day', 'military tribute', 'veteran gift', 'dawn service'],
                'mothers_day': ['mothers day gift', 'mum gift', 'aussie mum', 'mother gift', 'mama gift'],
                'fathers_day': ['fathers day gift', 'dad gift', 'aussie dad', 'father gift', 'papa gift'],
                'valentines_day': ['valentine gift', 'romantic gift', 'love gift', 'couple gift', 'aussie romance'],
                'black_friday': ['black friday australia', 'black friday deals', 'cyber deals', 'aussie black friday'],
                'click_frenzy': ['click frenzy gift', 'aussie online sale', 'click frenzy deals', 'australian cyber sale'],
                'end_of_financial_year': ['eofy gift', 'end of financial year', 'tax time gift', 'june sale', 'financial year end'],
                'back_to_school': ['back to school gift', 'school gift', 'student gift', 'aussie school', 'term gift'],
                'footy_season': ['footy gift', 'afl gift', 'nrl gift', 'football gift', 'aussie sport', 'team gift'],
                'grand_final_day': ['grand final gift', 'afl grand final', 'footy final', 'championship gift'],
                'state_of_origin': ['state of origin gift', 'origin gift', 'rugby league', 'nsw qld gift'],
                'cricket_season': ['cricket gift', 'aussie cricket', 'summer cricket', 'test match gift'],
                'big_bash_league': ['big bash gift', 'bbl gift', 't20 cricket', 'cricket league'],
                'tennis_open': ['australian open gift', 'tennis gift', 'grand slam gift', 'melbourne tennis'],
                'formula_1_gp': ['f1 gift', 'australian gp', 'formula one gift', 'racing gift', 'melbourne gp'],
                'wedding_season': ['wedding gift', 'aussie wedding', 'marriage gift', 'couple gift', 'bridal gift'],
                'graduation_season': ['graduation gift', 'uni gift', 'achievement gift', 'success gift', 'aussie graduate'],
                'housewarming': ['housewarming gift', 'new home gift', 'house blessing', 'aussie home', 'moving gift'],
                'baby_shower': ['baby shower gift', 'new baby gift', 'aussie baby', 'pregnancy gift'],
                'birthday': ['birthday gift', 'bday gift', 'aussie birthday', 'celebration gift', 'party gift'],
                'anniversary': ['anniversary gift', 'relationship gift', 'aussie couple', 'milestone gift'],
                'retirement': ['retirement gift', 'farewell gift', 'career end', 'aussie retirement'],
                'summer_season': ['summer gift', 'aussie summer', 'beach gift', 'hot weather', 'outdoor gift'],
                'winter_season': ['winter gift', 'aussie winter', 'cold weather', 'cozy gift', 'indoor gift'],
                'camping_season': ['camping gift', 'outdoor gift', 'bush camping', 'aussie adventure', 'wilderness gift'],
                'fishing_season': ['fishing gift', 'angling gift', 'aussie fishing', 'catch gift', 'rod gift'],
                'surfing_season': ['surfing gift', 'surf gift', 'beach gift', 'wave rider', 'aussie surf'],
                'road_trip_season': ['road trip gift', 'travel gift', 'aussie adventure', 'journey gift', 'outback trip'],
                'outback_travel': ['outback gift', 'bush gift', 'rural gift', 'red centre', 'aussie outback'],
                'reef_diving_season': ['diving gift', 'reef gift', 'underwater gift', 'great barrier reef', 'scuba gift'],
                'wine_harvest': ['wine gift', 'vintage gift', 'aussie wine', 'vineyard gift', 'harvest gift'],
                'tax_time': ['tax time gift', 'refund gift', 'accountant gift', 'financial gift', 'ato gift']
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