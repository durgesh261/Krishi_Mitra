import sqlite3
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

DATABASE = 'Krishi Mitra.db'

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            full_name TEXT,
            phone TEXT,
            state TEXT,
            district TEXT,
            latitude REAL,
            longitude REAL,
            is_admin INTEGER DEFAULT 0,
            preferred_language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP
        )
    ''')
    
    # Migrate existing users table if preferred_language is missing
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN preferred_language TEXT DEFAULT 'en'")
    except Exception:
        pass
    
    # Contact submissions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contact_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT,
            message TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # User activity log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            activity_type TEXT NOT NULL,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Analytics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            feature TEXT NOT NULL,
            query_data TEXT,
            result_data TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Prediction history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prediction_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            prediction_type TEXT NOT NULL,
            input_data TEXT,
            output_data TEXT,
            confidence REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Farmer Community News / Field Reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmer_community_news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            summary TEXT NOT NULL,
            category TEXT DEFAULT 'Crop Care & Alerts',
            author_name TEXT NOT NULL,
            village_district TEXT,
            state TEXT,
            contact TEXT,
            tag TEXT DEFAULT 'Farmer Report',
            source TEXT DEFAULT 'Community Advisory',
            source_url TEXT DEFAULT '',
            upvotes INTEGER DEFAULT 0,
            status TEXT DEFAULT 'approved',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Seed authentic starter farmer field reports if table is empty
    cursor.execute("SELECT COUNT(*) as count FROM farmer_community_news")
    if cursor.fetchone()['count'] == 0:
        seed_farmer_news = [
            (
                "Ludhiana Mandi Update: Early Paddy 1509 Arrivals Fetch Premium ₹3,450/Qtl",
                "Good moisture quality paddy is receiving immediate bids from private millers. Farmers advised to bring grain with moisture below 17% for instant spot payment at Khanna & Ludhiana APMC.",
                "Market & Mandi",
                "Sardar Jaswinder Singh",
                "Khanna, Ludhiana",
                "Punjab",
                "Farmer Advisory",
                "",
                14
            ),
            (
                "Warning: Mild Whitefly Infestation Observed on Late Cotton in Sirsa District",
                "Spotted whitefly nymphs on underside of leaves in 3 blocks. Agricultural extension officer recommends neem-based spray (1500 ppm @ 5ml/liter) before applying chemical insecticides.",
                "Crop Care & Alerts",
                "Chaudhary Virender Sihag",
                "Sirsa",
                "Haryana",
                "Kisan Mitra Reporter",
                "",
                9
            ),
            (
                "IFFCO Nano DAP Stock Delivered at Village Co-operative Society (PACS)",
                "Fresh consignment of 500 bottles of Nano DAP arrived today. Available to all registered farmers with Aadhaar card at government MRP ₹225 per bottle.",
                "Technology & Inputs",
                "Rameshwar Meena",
                "Ramganj Mandi, Kota",
                "Rajasthan",
                "PACS Committee Member",
                "",
                21
            ),
            (
                "Pre-Rabi Soil Moisture Ideal: Recommending Early Mustard Sowing in Ujjain",
                "Due to late September showers, deep black soil moisture is exceptionally high. Sowing Pioneer 45S46 or Giriraj variety this week will avoid aphid attacks in January.",
                "Weather & Monsoon",
                "Patel Shivraj Patidar",
                "Tarana, Ujjain",
                "Madhya Pradesh",
                "Progressive Farmer",
                "",
                18
            )
        ]
        cursor.executemany('''
            INSERT INTO farmer_community_news 
            (title, summary, category, author_name, village_district, state, source, source_url, upvotes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_farmer_news)

    # Farmer Deals & Verified Marketplace Offers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farmer_deals_offers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subtitle TEXT,
            description TEXT NOT NULL,
            badge TEXT DEFAULT 'Verified Farmer Offer',
            deal_tag TEXT DEFAULT 'Special Farmer Offer',
            category TEXT DEFAULT 'Machinery & Rentals',
            partner TEXT NOT NULL,
            location TEXT,
            state TEXT,
            helpline TEXT,
            cta_text TEXT DEFAULT 'Inquire / Connect',
            cta_link TEXT DEFAULT '#',
            benefits TEXT,
            theme_color TEXT DEFAULT '#2e7d32',
            bg_gradient TEXT DEFAULT 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%)',
            icon TEXT DEFAULT 'fas fa-tractor',
            image_url TEXT,
            upvotes INTEGER DEFAULT 0,
            is_farmer_deal INTEGER DEFAULT 1,
            status TEXT DEFAULT 'approved',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Seed initial community deals if table empty
    cursor.execute("SELECT COUNT(*) as count FROM farmer_deals_offers")
    if cursor.fetchone()['count'] == 0:
        seed_deals = [
            (
                "55 HP Tractor with Laser Land Leveler & Happy Seeder for Hire",
                "Cut diesel and save 30% sowing time with GPS-guided land leveling",
                "Complete custom hiring package available for Rabi sowing across Sangrur & Patiala. Includes experienced operator and diesel support.",
                "Custom Hiring Center • Punjab",
                "Seasonal Hire Available",
                "Farm Machinery & Rentals",
                "Sardar Harjit Singh Dhillon",
                "Sangrur & Sunam",
                "Punjab",
                "98765-22441",
                "Book Tractor Rental",
                "tel:9876522441",
                "₹800/Hour All-Inclusive||GPS-Precision ±1cm Leveling||Doorstep Delivery to Farm",
                "#1565c0",
                "linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%)",
                "fas fa-tractor",
                "",
                18
            ),
            (
                "NSC Certified High-Yield Wheat (PBW-826 & HD-3086) Seed Stock",
                "ICAR Recommended varieties with 98% germination guarantee",
                "Direct from registered cooperative seed growers. Pre-treated with bio-fungicide (Trichoderma) to resist yellow rust and smut.",
                "National Seeds Cooperative",
                "Certified Seed Subsidy",
                "Certified Seeds",
                "Kisan Beej Sahyog Kendra",
                "Khanna Mandi, Ludhiana",
                "Punjab",
                "1800-180-1551",
                "Order Certified Seeds",
                "tel:18001801551",
                "₹42/kg Government Subsidized||Treated against Rust||Doorstep PACS Delivery",
                "#2e7d32",
                "linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%)",
                "fas fa-seedling",
                "",
                24
            ),
            (
                "Agricultural Drone Spraying Service for Nano Urea & Insecticides",
                "Spray 1 Acre in 7 Minutes with 95% Uniform Canopy Coverage",
                "DGCA-certified drone pilot service covering wheat, mustard, sugarcane, and cotton. Saves 50% water and eliminates health risks of manual backpack spraying.",
                "Kisan Drone Seva",
                "DGCA Certified Pilot",
                "Drone & Technology",
                "Krishi Drone Sahyog Network",
                "Karnal & Kurukshetra",
                "Haryana",
                "98120-77889",
                "Book Drone Spraying",
                "tel:9812077889",
                "Just ₹350 per Acre||Zero Crop Trampling Damage||Battery & Water Self-Supplied",
                "#6a1b9a",
                "linear-gradient(135deg, #f3e5f5 0%, #e1bee7 50%, #ce93d8 100%)",
                "fas fa-helicopter",
                "",
                31
            ),
            (
                "100% Earthworm Enriched Organic Vermicompost Bulk Supply",
                "Lab-tested organic manure with high nitrogen, humic acid and micro-nutrients",
                "Prepared using desi cow dung and Eisenia fetida earthworms. Improves soil water retention, restores beneficial microflora, and cuts chemical DAP need by 40%.",
                "Organic Farmers Group",
                "Bulk Tractor-Trolley Discount",
                "Bio-Fertilizers & Nutrients",
                "Meena Organic Agro Farm",
                "Ramganj Mandi, Kota",
                "Rajasthan",
                "94140-33211",
                "Inquire Bulk Compost",
                "tel:9414033211",
                "₹6/kg in 50kg Bags||Free Testing Certificate||Bulk Delivery across Rajasthan & MP",
                "#b71c1c",
                "linear-gradient(135deg, #ffebee 0%, #ffcdd2 50%, #ef9a9a 100%)",
                "fas fa-leaf",
                "",
                15
            )
        ]
        cursor.executemany('''
            INSERT INTO farmer_deals_offers
            (title, subtitle, description, badge, deal_tag, category, partner, location, state, helpline, cta_text, cta_link, benefits, theme_color, bg_gradient, icon, image_url, upvotes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_deals)

    # ---------------------------------------------------------
    # Farmer Community Hub (Kisan Chaupal): Area-wise & Regional
    # ---------------------------------------------------------
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS community_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author_name TEXT NOT NULL,
            author_phone TEXT,
            user_id INTEGER,
            region TEXT NOT NULL,
            state TEXT NOT NULL,
            district TEXT,
            village TEXT,
            category TEXT NOT NULL,
            item_name TEXT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            language TEXT DEFAULT 'hi',
            language_name TEXT DEFAULT 'Hindi',
            rating REAL DEFAULT 5.0,
            image_url TEXT,
            upvotes INTEGER DEFAULT 0,
            views INTEGER DEFAULT 1,
            is_verified_farmer INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS community_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            author_name TEXT NOT NULL,
            location TEXT,
            state TEXT,
            comment TEXT NOT NULL,
            rating REAL DEFAULT 5.0,
            language TEXT DEFAULT 'hi',
            helpful_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(post_id) REFERENCES community_posts(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute("SELECT COUNT(*) as count FROM community_posts")
    if cursor.fetchone()['count'] == 0:
        seed_posts = [
            (
                "Sardar Gurpreet Singh Dhillon", "98765-11223", None, "North", "Punjab", "Ludhiana", "Jagraon",
                "Farming Machinery & Instruments", "Shaktiman 7-Feet Regular Light Rotavator",
                "Rotavator vs Super Seeder review for Paddy residue management (ਰੋਟਾਵੇਟਰ ਬਨਾਮ ਸੁਪਰ ਸੀਡਰ ਤਜ਼ਰਬਾ)",
                "ਮੈਂ ਪਿਛਲੇ 2 ਸੀਜ਼ਨਾਂ ਤੋਂ ਸ਼ਕਤੀਮਾਨ ਰੋਟਾਵੇਟਰ 50HP ਟਰੈਕਟਰ ਨਾਲ ਵਰਤ ਰਿਹਾ ਹਾਂ। ਝੋਨੇ ਦੀ ਪਰਾਲੀ ਨੂੰ ਮਿੱਟੀ ਵਿੱਚ ਮਿਲਾਉਣ ਲਈ ਬਹੁਤ ਵਧੀਆ ਹੈ। ਡੀਜ਼ਲ 4.5 ਲੀਟਰ ਪ੍ਰਤੀ ਏਕੜ ਲੈਂਦਾ ਹੈ ਅਤੇ ਬਲੇਡਾਂ ਦੀ ਗੁਣਵੱਤਾ ਮਜ਼ਬੂਤ ਹੈ। ਸੁਪਰ ਸੀਡਰ ਨਾਲੋਂ ਘੱਟ ਲੋਡ ਲੈਂਦਾ ਹੈ।",
                "pa", "Punjabi (ਪੰਜਾਬੀ)", 4.8,
                "https://images.unsplash.com/photo-1589923188900-85dae523342b?auto=format&fit=crop&w=800&q=80",
                27, 342
            ),
            (
                "Dnyaneshwar Shinde", "98220-44556", None, "West", "Maharashtra", "Nashik", "Niphad",
                "Pesticides & Agrochemicals", "Trichoderma Viride + Pseudomonas Bio-Mix",
                "Best bio-fungicide for Grape downy mildew & thrips control (द्राक्षावरील डाऊनीसाठी ट्रायकोडर्मा अनुभव)",
                "नाशिक मधील द्राक्ष उत्पादक शेतकरी मित्रांसाठी: डाऊनी मिल्ड्यू आणि करपा रोगावर ट्रायकोडर्मा आणि स्यूडोमोनास चा जैविक स्प्रे अत्यंत प्रभावी ठरला आहे. रासायनिक बुरशीनाशकांपेक्षा 40% खर्च वाचतो आणि निर्यात दर्जाची द्राक्षे तयार होतात.",
                "mr", "Marathi (मराठी)", 4.9,
                "https://images.unsplash.com/photo-1506377247377-2a5b3b417ebb?auto=format&fit=crop&w=800&q=80",
                38, 512
            ),
            (
                "Subhash Mondal", "94340-77889", None, "East", "West Bengal", "Purba Bardhaman", "Memari",
                "Crops & Harvest", "Swarna Sub-1 (Flood-Tolerant Paddy)",
                "Aman Paddy Bumper Harvest: Swarna Sub-1 variety experience (স্বর্ণ সাব-১ ধানের বাম্পার ফলন পর্যালোচনা)",
                "বর্ধমান অঞ্চলের কৃষক ভাইদের জন্য: স্বর্ণ সাব-১ ধানের ফলন প্রতি বিঘায় ২২ মণ হয়েছে। আগস্টের বন্যায় জমিতে ১০ দিন জল জমে থাকার পরেও ধানের শিকড় পচেনি। নাইট্রোজেন সার কম লাগে এবং চাল অত্যন্ত সরু ও সুস্বাদু হয়।",
                "bn", "Bengali (বাংলা)", 4.7,
                "https://images.unsplash.com/photo-1536657464919-892534f60d6e?auto=format&fit=crop&w=800&q=80",
                21, 289
            ),
            (
                "Koteswara Rao", "98480-12345", None, "South", "Andhra Pradesh", "Guntur", "Tenali",
                "Pesticides & Agrochemicals", "Diafenthiuron 50% WP (Pegasus) + Cold Pressed Neem Oil",
                "Black Thrips management in Guntur Chilli crop (గుంటూరు మిర్చిలో నల్ల తామర పురుగు నివారణ పద్ధతులు)",
                "గుంటూరు మరియు ప్రకాశం జిల్లాల మిర్చి రైతులకు ముఖ్య సలహా: నల్ల తామర పురుగులకు పెగాసస్ 250 గ్రాములు మరియు 10000 PPM వేప నూనె కలిపి పిచಿಕారీ చేస్తే 4 రోజుల్లో అద్భుతమైన ఫలితం కనిపించింది. పూత రాలడం ఆగిపోయి కొత్త చిగురు వేగంగా వచ్చింది.",
                "te", "Telugu (తెలుగు)", 4.8,
                "https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&w=800&q=80",
                35, 460
            ),
            (
                "Radheshyam Patidar", "94250-99881", None, "Central", "Madhya Pradesh", "Ujjain", "Badnagar",
                "Seeds & Fertilizers", "JS-2034 ICAR Certified Soybean Seed",
                "सोयाबीन JS-2034 किस्म का अनुभव: कम बारिश में भी 11 क्विंटल प्रति एकड़ पैदावार",
                "मालवा के किसान भाइयों को राम-राम! पिछले खरीफ में मैंने 5 एकड़ में JS-2034 बोया था। पीला मोजेक और गर्डल बीटल का कोई असर नहीं हुआ। 88 दिनों में फसल पक कर तैयार हो गई। तेल की मात्रा 21% निकली जिससे मंडी में ₹200 प्रति क्विंटल का अधिक भाव मिला।",
                "hi", "Hindi (हिन्दी)", 4.9,
                "https://images.unsplash.com/photo-1574323347407-f5e1ad659c40?auto=format&fit=crop&w=800&q=80",
                42, 580
            ),
            (
                "Chaudhary Virendra Singh", "98370-55667", None, "North", "Uttar Pradesh", "Muzaffarnagar", "Khatauli",
                "Farming Machinery & Instruments", "Automatic Sugarcane Cutter Planter with Fertilizer Drill",
                "गन्ना ट्रेंच प्लांटर मशीन: 4 फीट दूरी पर बुवाई से लेबर खर्च में 65% की बचत",
                "पश्चिम यूपी के गन्ना उत्पादक भाई ध्यान दें: 4 फीट ट्रेंच विधि से पेड़ी गन्ने में बंपर कल्ले निकलते हैं। 50HP ट्रैक्टर से चलने वाली इस प्लांटर मशीन से 1 दिन में 8 एकड़ गन्ने की बुवाई, खाद डालना और पाटा लगाना एक साथ हो गया। 15 मजदूरों का काम 2 लोग कर लेते हैं।",
                "hi", "Hindi (हिन्दी)", 4.9,
                "https://images.unsplash.com/photo-1589923188900-85dae523342b?auto=format&fit=crop&w=800&q=80",
                29, 410
            ),
            (
                "Mansukhbhai Patel", "98250-33445", None, "West", "Gujarat", "Rajkot", "Gondal",
                "Crops & Harvest", "Bt Cotton Bollgard-II with Integrated Pest Traps",
                "Bt Cotton Pink Bollworm prevention strategy (કપાસમાં ગુલાબી ઈયળ નિયંત્રણ માટે ફેરોમોન ટ્રેપ)",
                "સૌરાષ્ટ્રના કપાસ ખેડૂત મિત્રો માટે: એક વીઘામાં 8 ફેરોમોન ટ્રેપ લગાવ્યા અને લીમડાના તેલનો નિયમિત છંટકાવ કર્યો. ગુલાબી ઈયળનો ઉપદ੍ਰવ 90% અટક્યો અને વીઘે 32 મણ ઉત્તમ ગુણવત્તાવાળો સફેદ કપાસ ઉતર્યો. જીનિંગ મિલ વાળાએ ઊંચો ભાવ આપ્યો.",
                "gu", "Gujarati (ગુજરાતી)", 4.8,
                "https://images.unsplash.com/photo-1605000797499-95a51c5269ae?auto=format&fit=crop&w=800&q=80",
                31, 395
            ),
            (
                "Basavaraju Gowda", "94480-66778", None, "South", "Karnataka", "Mandya", "Maddur",
                "Farming Machinery & Instruments", "5HP Solar Drip Irrigation Automation System",
                "Solar Powered GSM Drip Irrigation Review (ಸೌರಶಕ್ತಿ ಚಾಲಿತ ಹನಿ ನೀರಾವರಿ ಆಟೋಮೇಷನ್ ಅನುಭವ)",
                "ಮಂಡ್ಯ ಮತ್ತು ಮೈಸೂರು ಕಬ್ಬು ಹಾಗೂ ತರಕಾರಿ ಬೆಳೆಗಾರರಿಗೆ: ಮೊಬೈಲ್ ಮೂಲಕ ನೀರಾವರಿ ನಿಯಂತ್ರಿಸುವ ಜಿಎಸ್ಎಂ ಕಂಟ್ರੋಲರ್ ಅಳವಡಿಸಿದ್ದೇನೆ. ಮನೆಯಲ್ಲೇ ಕುಳಿತು ಮೋಟಾರ್ ಆನ್/ಆಫ್ ಮಾಡಬಹುದು. ರಾತ್ರಿ ಹೊಲಕ್ಕೆ ಹೋಗುವ ಹಾವು ಕಡಿತದ ಅಪಾಯ ತಪ್ಪಿದೆ ಮತ್ತು 100% ವಿದ್ಯುತ್ ಬಿಲ್ ಮುಕ್ತ.",
                "kn", "Kannada (ಕನ್ನಡ)", 5.0,
                "https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?auto=format&fit=crop&w=800&q=80",
                33, 440
            )
        ]
        cursor.executemany('''
            INSERT INTO community_posts
            (author_name, author_phone, user_id, region, state, district, village, category, item_name, title, content, language, language_name, rating, image_url, upvotes, views)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_posts)

        # Seed realistic farmer reviews for these posts
        seed_reviews = [
            (1, "Baldev Singh", "Moga", "Punjab", "ਬਿਲਕੁਲ ਸਹੀ ਵੀਰ ਜੀ, ਅਸੀਂ ਵੀ 3 ਸਾਲਾਂ ਤੋਂ ਸ਼ਕਤੀਮਾਨ ਰੋਟਾਵੇਟਰ ਵਰਤ ਰਹੇ ਹਾਂ, ਸੁਪਰ ਸੀਡਰ ਨਾਲੋਂ ਡੀਜ਼ਲ ਕਾਫੀ ਬਚਦਾ ਹੈ।", 5.0, "pa", 8),
            (1, "Rameshwar Yadav", "Karnal", "Haryana", "हरियाणा की भारी चिकनी मिट्टी में यह 50HP सोनालिका पर बहुत बढ़िया काम करता है। ब्लेड 3 सीजन चल जाते हैं।", 4.5, "hi", 5),
            (2, "Pravin Patil", "Sangli", "Maharashtra", "आम्ही तासगाव पट्ट्यात बेदाणा द्राक्षासाठी हाच जैविक प्रयोग केला, मणी गळती थांबली आणि उत्तम साखर भरली.", 5.0, "mr", 12),
            (2, "Sachin Kadam", "Solapur", "Maharashtra", "स्प्रे करताना गूळ आणि ताक मिसळल्यास जिवाणूंची वाढ जलद होते आणि डाऊनी 100% थांबतो.", 5.0, "mr", 9),
            (3, "Animesh Das", "Nadia", "West Bengal", "বন্যা প্রবণ এলাকায় স্বর্ণ সাব-১ সত্যি আশীর্বাদ। রোগবালাই অনেক কম এবং ধানের ওজন ভালো হয়।", 5.0, "bn", 6),
            (4, "Venkat Reddy", "Khammam", "Telangana", "రైతు సోదరులకు మంచి సలహా. మేము కూడా పెగాసస్ తో వేప నూనె కలిపి పిచಿಕారీ చేశాము, పూత బాగా నిలిచింది.", 5.0, "te", 11),
            (5, "Mukesh Sharma", "Dewas", "Madhya Pradesh", "पाटीदार जी, बीज उपचार किस दवा से किया था? क्या आपने राइजोबियम कल्चर का उपयोग किया था?", 4.5, "hi", 7),
            (5, "Radheshyam Patidar", "Ujjain", "Madhya Pradesh", "शर्मा जी, वीटावैक्स पावर और राइजोबियम दोनों से उपचारित किया था। इससे जड़ें 15 दिन में मजबूत हो गईं।", 5.0, "hi", 14),
            (6, "Amit Malik", "Shamli", "Uttar Pradesh", "चौधरी साहब, क्या इसमें कीटनाशक स्प्रेयर का अटैचमेंट भी साथ में आता है? दीमक से बचाव के लिए कैसा है?", 5.0, "hi", 4),
            (7, "Kishorbhai Savaliya", "Amreli", "Gujarat", "ફેરોમોન ટ્રેપ કપાસ વાવ્યાના કેટલા દિવસે લગાવ્યા હતા ભાઈ? અમારે પણ આ વખતે ગુલાબી ઈયળ મુક્ત પાક લેવો છે.", 5.0, "gu", 8),
            (8, "Channappa", "Ramanagara", "Karnataka", "ಸರ್, ಸೋಲಾರ್ ಪಂಪ್ ಸಬ್ಸಿಡಿ ಕುಸುಮ್ ಯೋಜನೆಯಲ್ಲಿ ಸಿಕ್ಕಿತಾ? ದಯವಿಟ್ಟು ಅರ್ಜಿ ಹಾಕುವ ವಿಧಾನ ತಿಳಿಸಿ.", 5.0, "kn", 7)
        ]
        cursor.executemany('''
            INSERT INTO community_reviews
            (post_id, author_name, location, state, comment, rating, language, helpful_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_reviews)

    # Create default admin user if not exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_hash = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, is_admin)
            VALUES (?, ?, ?, ?, ?)
        ''', ('admin', 'admin@Krishi Mitra.com', admin_hash, 'Administrator', 1))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# User management functions
def create_user(username, email, password, full_name=None, phone=None):
    """Create a new user"""
    conn = get_db()
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute('''
            INSERT INTO users (username, email, password_hash, full_name, phone)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password_hash, full_name, phone))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return {'success': True, 'user_id': user_id}
    except sqlite3.IntegrityError as e:
        conn.close()
        return {'success': False, 'error': 'Username or email already exists'}

def verify_user(username, password):
    """Verify user credentials"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None

def update_user_location(user_id, latitude, longitude, state=None, district=None):
    """Update user location"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users 
        SET latitude = ?, longitude = ?, state = ?, district = ?
        WHERE id = ?
    ''', (latitude, longitude, state, district, user_id))
    conn.commit()
    conn.close()

def update_user_language(user_id, language):
    """Update user's preferred language"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET preferred_language = ? WHERE id = ?
    ''', (str(language).lower(), user_id))
    conn.commit()
    conn.close()

def get_user_language(user_id):
    """Get user's preferred language"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT preferred_language FROM users WHERE id = ?', (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row['preferred_language']:
        return row['preferred_language']
    return 'en'


def update_last_login(user_id):
    """Update last login timestamp"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
    ''', (user_id,))
    conn.commit()
    conn.close()

def get_user_by_id(user_id):
    """Get user by ID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def get_all_users():
    """Get all users (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, full_name, phone, state, district, created_at, last_login FROM users WHERE is_admin = 0')
    users = cursor.fetchall()
    conn.close()
    return [dict(user) for user in users]

def delete_user(user_id):
    """Delete user (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM users WHERE id = ? AND is_admin = 0', (user_id,))
    conn.commit()
    conn.close()

# Contact form functions
def create_contact_submission(name, email, subject, message):
    """Create contact form submission"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO contact_submissions (name, email, subject, message)
        VALUES (?, ?, ?, ?)
    ''', (name, email, subject, message))
    conn.commit()
    conn.close()
    return {'success': True}

def get_all_contacts():
    """Get all contact submissions (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM contact_submissions ORDER BY created_at DESC')
    contacts = cursor.fetchall()
    conn.close()
    return [dict(contact) for contact in contacts]

def update_contact_status(contact_id, status):
    """Update contact submission status"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE contact_submissions SET status = ? WHERE id = ?', (status, contact_id))
    conn.commit()
    conn.close()

# Activity logging
def log_activity(user_id, activity_type, details=None):
    """Log user activity"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO activity_log (user_id, activity_type, details)
        VALUES (?, ?, ?)
    ''', (user_id, activity_type, details))
    conn.commit()
    conn.close()

def log_analytics(user_id, feature, query_data=None, result_data=None):
    """Log analytics data"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analytics (user_id, feature, query_data, result_data)
        VALUES (?, ?, ?, ?)
    ''', (user_id, feature, query_data, result_data))
    conn.commit()
    conn.close()

def log_prediction(user_id, prediction_type, input_data, output_data, confidence=None):
    """Log prediction history"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO prediction_history (user_id, prediction_type, input_data, output_data, confidence)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, prediction_type, input_data, output_data, confidence))
    conn.commit()
    conn.close()

def get_user_predictions(user_id, limit=10):
    """Get user's prediction history"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM prediction_history 
        WHERE user_id = ? 
        ORDER BY created_at DESC 
        LIMIT ?
    ''', (user_id, limit))
    predictions = cursor.fetchall()
    conn.close()
    return [dict(pred) for pred in predictions]

# Analytics functions
def get_analytics_summary():
    """Get analytics summary (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Total users
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE is_admin = 0')
    total_users = cursor.fetchone()['count']
    
    # Total queries
    cursor.execute('SELECT COUNT(*) as count FROM analytics')
    total_queries = cursor.fetchone()['count']
    
    # Total contacts
    cursor.execute('SELECT COUNT(*) as count FROM contact_submissions')
    total_contacts = cursor.fetchone()['count']
    
    # Feature usage
    cursor.execute('''
        SELECT feature, COUNT(*) as count 
        FROM analytics 
        GROUP BY feature 
        ORDER BY count DESC
    ''')
    feature_usage = [dict(row) for row in cursor.fetchall()]
    
    # Recent activities
    cursor.execute('''
        SELECT a.*, u.username 
        FROM activity_log a
        LEFT JOIN users u ON a.user_id = u.id
        ORDER BY a.created_at DESC
        LIMIT 10
    ''')
    recent_activities = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    
    return {
        'total_users': total_users,
        'total_queries': total_queries,
        'total_contacts': total_contacts,
        'feature_usage': feature_usage,
        'recent_activities': recent_activities
    }

# Farmer Community News & Field Advisories Functions
def create_farmer_news(title, summary, category, author_name, village_district=None, state=None, contact=None, source_url=None):
    """Save a community farmer news or field advisory"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO farmer_community_news (title, summary, category, author_name, village_district, state, contact, source_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title.strip(), summary.strip(), category.strip(), author_name.strip(), 
          (village_district or '').strip(), (state or '').strip(), 
          (contact or '').strip(), (source_url or '').strip()))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_all_farmer_news(limit=50, category=None):
    """Retrieve community farmer news items"""
    conn = get_db()
    cursor = conn.cursor()
    if category and category.lower() != 'all':
        cursor.execute('''
            SELECT * FROM farmer_community_news 
            WHERE status = 'approved' AND (category = ? OR category LIKE ?)
            ORDER BY created_at DESC LIMIT ?
        ''', (category, f"%{category}%", limit))
    else:
        cursor.execute('''
            SELECT * FROM farmer_community_news 
            WHERE status = 'approved'
            ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def upvote_farmer_news(news_id):
    """Increment upvote count for helpful farmer news"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE farmer_community_news 
        SET upvotes = upvotes + 1 
        WHERE id = ?
    ''', (news_id,))
    conn.commit()
    cursor.execute('SELECT upvotes FROM farmer_community_news WHERE id = ?', (news_id,))
    row = cursor.fetchone()
    conn.close()
    return row['upvotes'] if row else 0

# Farmer Deals & Marketplace Offers Functions
def create_farmer_deal(title, description, partner=None, category='Machinery & Rentals',
                       subtitle='', badge=None, deal_tag=None,
                       location='', state='', helpline=None, cta_text=None,
                       cta_link=None, benefits='', theme_color=None, icon=None,
                       image_url='', price_terms=None, seller_name=None, contact_number=None):
    """Save a community-submitted agricultural deal or equipment offer"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Resolve aliases
    partner_name = partner or seller_name or 'Local Farmer'
    contact_phone = helpline or contact_number or ''
    tag = deal_tag or (f"₹ {price_terms}" if price_terms else 'Verified Offer')
    deal_badge = badge or f"Farmer Deal • {category}"
    cta = cta_text or ("Call Seller" if contact_phone else "Inquire / Connect")
    link = cta_link or (f"tel:{contact_phone}" if contact_phone else "#")
    sub = subtitle or (f"Offered by {partner_name} ({location}, {state})" if location else f"Offered by {partner_name}")

    # Build benefits if price_terms given
    b_list = [b.strip() for b in benefits.split('||') if b.strip()] if benefits else []
    if price_terms and not any('Rate' in b for b in b_list):
        b_list.insert(0, f"Rate / Terms: {price_terms}")
    if location and not any('Location' in b for b in b_list):
        b_list.append(f"Location: {location}, {state}".strip(', '))
    if not any('Verified' in b or 'Farmer' in b for b in b_list):
        b_list.append("Direct Farmer-to-Farmer Deal")
    benefits_str = "||".join(b_list)

    # Determine theme color & icon based on category
    cat_lower = category.lower()
    if not theme_color:
        if 'seed' in cat_lower:
            theme_color = '#2e7d32'
            deal_icon = 'fas fa-seedling'
        elif 'machinery' in cat_lower or 'tractor' in cat_lower:
            theme_color = '#1565c0'
            deal_icon = 'fas fa-tractor'
        elif 'drone' in cat_lower or 'tech' in cat_lower:
            theme_color = '#6a1b9a'
            deal_icon = 'fas fa-drone'
        elif 'fertilizer' in cat_lower or 'organic' in cat_lower or 'compost' in cat_lower:
            theme_color = '#b71c1c'
            deal_icon = 'fas fa-leaf'
        elif 'solar' in cat_lower or 'irrigation' in cat_lower:
            theme_color = '#e65100'
            deal_icon = 'fas fa-solar-panel'
        else:
            theme_color = '#2e7d32'
            deal_icon = 'fas fa-handshake'
    else:
        deal_icon = icon or 'fas fa-tag'

    if icon:
        deal_icon = icon

    color_map = {
        '#1565c0': 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 50%, #90caf9 100%)',
        '#2e7d32': 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%)',
        '#6a1b9a': 'linear-gradient(135deg, #f3e5f5 0%, #e1bee7 50%, #ce93d8 100%)',
        '#b71c1c': 'linear-gradient(135deg, #ffebee 0%, #ffcdd2 50%, #ef9a9a 100%)',
        '#e65100': 'linear-gradient(135deg, #fff3e0 0%, #ffe0b2 50%, #ffcc80 100%)'
    }
    bg_gradient = color_map.get(theme_color, 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 50%, #a5d6a7 100%)')

    cursor.execute('''
        INSERT INTO farmer_deals_offers 
        (title, subtitle, description, badge, deal_tag, category, partner, location, state, 
         helpline, cta_text, cta_link, benefits, theme_color, bg_gradient, icon, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title.strip(), sub.strip(), description.strip(), deal_badge.strip(), tag.strip(),
          category.strip(), partner_name.strip(), location.strip(), state.strip(),
          contact_phone.strip(), cta.strip(), link.strip(), benefits_str.strip(),
          theme_color.strip(), bg_gradient, deal_icon.strip(), (image_url or '').strip()))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id

def get_all_farmer_deals(limit=50):
    """Retrieve community-submitted and partner agricultural deals"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM farmer_deals_offers 
        WHERE status = 'approved'
        ORDER BY created_at DESC LIMIT ?
    ''', (limit,))
    rows = cursor.fetchall()
    conn.close()
    results = []
    for row in rows:
        d = dict(row)
        d['seller_name'] = d.get('partner')
        d['contact_number'] = d.get('helpline')
        if isinstance(d.get('benefits'), str):
            d['benefits_list'] = [b.strip() for b in d['benefits'].split('||') if b.strip()]
        else:
            d['benefits_list'] = []
        d['price_terms'] = d.get('deal_tag', '').replace('₹', '').strip()
        results.append(d)
    return results

def upvote_farmer_deal(deal_id):
    """Increment upvote/interest count for agricultural deal"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE farmer_deals_offers 
        SET upvotes = upvotes + 1 
        WHERE id = ?
    ''', (deal_id,))
    conn.commit()
    cursor.execute('SELECT upvotes FROM farmer_deals_offers WHERE id = ?', (deal_id,))
    row = cursor.fetchone()
    conn.close()
    return row['upvotes'] if row else 0

# =====================================================================
# Farmer Community Hub (Kisan Chaupal) Database Operations
# =====================================================================

REGION_STATE_MAPPING = {
    'North': ['Punjab', 'Haryana', 'Uttar Pradesh', 'Himachal Pradesh', 'Jammu & Kashmir', 'Uttarakhand', 'Delhi', 'Chandigarh'],
    'South': ['Andhra Pradesh', 'Telangana', 'Karnataka', 'Tamil Nadu', 'Kerala'],
    'West': ['Maharashtra', 'Gujarat', 'Rajasthan', 'Goa'],
    'East': ['West Bengal', 'Bihar', 'Odisha', 'Jharkhand', 'Assam'],
    'Central': ['Madhya Pradesh', 'Chhattisgarh']
}

LANGUAGE_NAMES = {
    'hi': 'Hindi (हिन्दी)',
    'pa': 'Punjabi (ਪੰਜਾਬੀ)',
    'mr': 'Marathi (मराठी)',
    'gu': 'Gujarati (ગુજરાતી)',
    'bn': 'Bengali (বাংলা)',
    'te': 'Telugu (తెలుగు)',
    'ta': 'Tamil (தமிழ்)',
    'kn': 'Kannada (ಕನ್ನಡ)',
    'en': 'English'
}

def create_community_post(author_name, author_phone, region, state, district, village,
                          category, item_name, title, content, language='hi',
                          rating=5.0, image_url='', user_id=None):
    """Create a new community discussion or review post"""
    conn = get_db()
    cursor = conn.cursor()
    lang_name = LANGUAGE_NAMES.get(language, 'Hindi (हिन्दी)')
    
    # Auto-assign region if missing based on state
    if not region or region == 'All-India':
        for reg, states in REGION_STATE_MAPPING.items():
            if state in states:
                region = reg
                break
        if not region:
            region = 'North'

    cursor.execute('''
        INSERT INTO community_posts
        (author_name, author_phone, user_id, region, state, district, village,
         category, item_name, title, content, language, language_name, rating, image_url)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (author_name.strip(), (author_phone or '').strip(), user_id, region.strip(),
          state.strip(), (district or '').strip(), (village or '').strip(),
          category.strip(), (item_name or '').strip(), title.strip(), content.strip(),
          language.strip(), lang_name, float(rating or 5.0), (image_url or '').strip()))
    conn.commit()
    post_id = cursor.lastrowid
    conn.close()
    return post_id

def get_community_posts(region=None, state=None, district=None, category=None,
                        search=None, sort='latest', limit=50):
    """Retrieve community posts with location-wise, regional, and category filters"""
    conn = get_db()
    cursor = conn.cursor()
    
    query = '''
        SELECT p.*, COUNT(r.id) as review_count
        FROM community_posts p
        LEFT JOIN community_reviews r ON p.id = r.post_id
        WHERE 1=1
    '''
    params = []

    if region and region not in ('all', 'All', 'All-India'):
        query += ' AND p.region = ?'
        params.append(region)
    
    if state and state not in ('all', 'All', 'All States'):
        query += ' AND p.state = ?'
        params.append(state)

    if district and district not in ('all', 'All', 'All Districts'):
        query += ' AND LOWER(p.district) = LOWER(?)'
        params.append(district)

    if category and category not in ('all', 'All', 'All Categories'):
        query += ' AND p.category = ?'
        params.append(category)

    if search:
        search_pattern = f'%{search.strip().lower()}%'
        query += ' AND (LOWER(p.title) LIKE ? OR LOWER(p.content) LIKE ? OR LOWER(p.item_name) LIKE ? OR LOWER(p.author_name) LIKE ?)'
        params.extend([search_pattern, search_pattern, search_pattern, search_pattern])

    query += ' GROUP BY p.id'

    if sort == 'top_rated':
        query += ' ORDER BY p.rating DESC, p.upvotes DESC'
    elif sort == 'most_upvoted':
        query += ' ORDER BY p.upvotes DESC, p.created_at DESC'
    elif sort == 'most_discussed':
        query += ' ORDER BY review_count DESC, p.created_at DESC'
    else: # default latest
        query += ' ORDER BY p.created_at DESC'

    query += ' LIMIT ?'
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    posts = []
    for row in rows:
        posts.append(dict(row))
    return posts

def get_community_post(post_id, increment_view=True):
    """Get single post with all its reviews"""
    conn = get_db()
    cursor = conn.cursor()

    if increment_view:
        cursor.execute('UPDATE community_posts SET views = views + 1 WHERE id = ?', (post_id,))
        conn.commit()

    cursor.execute('SELECT * FROM community_posts WHERE id = ?', (post_id,))
    post_row = cursor.fetchone()
    if not post_row:
        conn.close()
        return None

    post = dict(post_row)

    # Fetch reviews
    cursor.execute('''
        SELECT * FROM community_reviews 
        WHERE post_id = ? 
        ORDER BY created_at ASC
    ''', (post_id,))
    reviews = [dict(r) for r in cursor.fetchall()]
    post['reviews'] = reviews
    post['review_count'] = len(reviews)
    conn.close()
    return post

def add_community_review(post_id, author_name, location, state, comment, rating=5.0, language='hi'):
    """Add a review or comment to a community post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO community_reviews
        (post_id, author_name, location, state, comment, rating, language)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (post_id, author_name.strip(), (location or '').strip(),
          (state or '').strip(), comment.strip(), float(rating or 5.0), language))
    conn.commit()
    new_id = cursor.lastrowid
    
    # Recalculate average post rating if ratings are provided
    cursor.execute('''
        SELECT AVG(rating) as avg_rating FROM community_reviews
        WHERE post_id = ? AND rating > 0
    ''', (post_id,))
    avg_row = cursor.fetchone()
    if avg_row and avg_row['avg_rating']:
        cursor.execute('UPDATE community_posts SET rating = ROUND(?, 1) WHERE id = ?',
                       (avg_row['avg_rating'], post_id))
        conn.commit()

    conn.close()
    return new_id

def upvote_community_post(post_id):
    """Increment helpful / upvote count for a community post"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE community_posts SET upvotes = upvotes + 1 WHERE id = ?', (post_id,))
    conn.commit()
    cursor.execute('SELECT upvotes FROM community_posts WHERE id = ?', (post_id,))
    row = cursor.fetchone()
    conn.close()
    return row['upvotes'] if row else 0

def get_community_regions_summary():
    """Return regions, states and category counts for UI dropdowns"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT region, COUNT(*) as count FROM community_posts GROUP BY region')
    region_counts = {row['region']: row['count'] for row in cursor.fetchall()}
    cursor.execute('SELECT category, COUNT(*) as count FROM community_posts GROUP BY category')
    cat_counts = {row['category']: row['count'] for row in cursor.fetchall()}
    conn.close()
    return {
        'regions': REGION_STATE_MAPPING,
        'region_counts': region_counts,
        'category_counts': cat_counts,
        'languages': LANGUAGE_NAMES
    }

if __name__ == '__main__':
    init_db()

