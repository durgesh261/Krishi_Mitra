/**
 * Krishi Mitra: Indian Regional Languages Translation Engine (i18n)
 * Covers the 10 most prominent languages across every geographic region of India:
 * North: Hindi, Punjabi
 * West: Gujarati, Marathi
 * East: Bengali
 * South: Telugu, Tamil, Kannada, Malayalam
 * Universal: English
 */

const INDIAN_LANGUAGES = {
  en: {
    nav_signin: "Sign In",
    nav_mandi: "Mandi Prices & MSP",
    nav_mandi_direct: "Mandi Bhav",
    tab_login: "Login",
    tab_signup: "Create Account",
    login_welcome: "Welcome Back",
    login_sub: "Login to access Krishi Mitra",
    signup_welcome: "Create Account",
    signup_sub: "Join Krishi Mitra today",
    code: "en",
    name: "English",
    nativeName: "English",
    region: "Pan-India / Universal",
    badge: "Universal"
  },
  hi: {
    nav_signin: "साइन इन",
    nav_mandi: "मंडी भाव और MSP",
    nav_mandi_direct: "मंडी भाव",
    tab_login: "लॉगिन",
    tab_signup: "खाता बनाएं",
    login_welcome: "पुनः स्वागत है",
    login_sub: "कृषि मित्र में लॉगिन करें",
    signup_welcome: "नया खाता बनाएं",
    signup_sub: "आज ही कृषि मित्र से जुड़ें",
    code: "hi",
    name: "Hindi",
    nativeName: "हिन्दी",
    region: "उत्तर एवं मध्य भारत (UP, MP, बिहार, राजस्थान, दिल्ली, हरियाणा)",
    badge: "North & Central"
  },
  pa: {
    nav_signin: "ਸਾਈਨ ਇਨ",
    nav_mandi: "ਮੰਡੀ ਭਾਅ ਅਤੇ MSP",
    nav_mandi_direct: "ਮੰਡੀ ਭਾਅ",
    tab_login: "ਲਾਗਇਨ",
    tab_signup: "ਖਾਤਾ ਬਣਾਓ",
    login_welcome: "ਜੀ ਆਇਆਂ ਨੂੰ",
    login_sub: "ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਵਿੱਚ ਲਾਗਇਨ ਕਰੋ",
    signup_welcome: "ਨਵਾਂ ਖਾਤਾ ਬਣਾਓ",
    signup_sub: "ਅੱਜ ਹੀ ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਨਾਲ ਜੁੜੋ",
    code: "pa",
    name: "Punjabi",
    nativeName: "ਪੰਜਾਬੀ",
    region: "ਉੱਤਰੀ ਭਾਰਤ (ਪੰਜਾਬ, ਹਰਿਆਣਾ, ਚੰਡੀਗੜ੍ਹ)",
    badge: "Punjab"
  },
  bn: {
    nav_signin: "সাইন ইন",
    nav_mandi: "মান্ডি দর ও MSP",
    nav_mandi_direct: "মান্ডি দর",
    tab_login: "লগইন",
    tab_signup: "অ্যাকাউন্ট তৈরি করুন",
    login_welcome: "স্বাগতম",
    login_sub: "কৃষি মিত্রে লগইন করুন",
    signup_welcome: "নতুন অ্যাকাউন্ট তৈরি করুন",
    signup_sub: "আজই কৃষি মিত্রের সাথে যুক্ত হন",
    code: "bn",
    name: "Bengali",
    nativeName: "বাংলা",
    region: "পূর্ব ভারত (পশ্চিমবঙ্গ, ত্রিপুরা, আসাম)",
    badge: "East India"
  },
  mr: {
    nav_signin: "साइन इन",
    nav_mandi: "बाजारभाव व हमीभाव (MSP)",
    nav_mandi_direct: "बाजारभाव",
    tab_login: "लॉगिन",
    tab_signup: "खाते तयार करा",
    login_welcome: "पुन्हा स्वागत आहे",
    login_sub: "कृषी मित्रमध्ये लॉगिन करा",
    signup_welcome: "नवीन खाते तयार करा",
    signup_sub: "आजच कृषी मित्रशी जोडा",
    code: "mr",
    name: "Marathi",
    nativeName: "मराठी",
    region: "पश्चिम भारत (महाराष्ट्र, गोवा)",
    badge: "Maharashtra"
  },
  gu: {
    nav_signin: "સાઇન ઇન",
    nav_mandi: "માર્કેટ યાર્ડ ભાવ & MSP",
    nav_mandi_direct: "માર્કેટ ભાવ",
    tab_login: "લૉગિન",
    tab_signup: "ખાતું બનાવો",
    login_welcome: "સ્વાગત છે",
    login_sub: "કૃષિ મિત્રમાં લૉગિન કરો",
    signup_welcome: "નવું ખાતું બનાવો",
    signup_sub: "આજે જ કૃષિ મિત્ર સાથે જોડાઓ",
    code: "gu",
    name: "Gujarati",
    nativeName: "ગુજરાતી",
    region: "પશ્ચિમ ભારત (ગુજરાત)",
    badge: "Gujarat"
  },
  te: {
    nav_signin: "సైన్ ఇన్",
    nav_mandi: "మార్కెట్ ధరలు & MSP",
    nav_mandi_direct: "మార్కెట్ ధరలు",
    tab_login: "లాగిన్",
    tab_signup: "ఖాతాను సృష్టించండి",
    login_welcome: "తిరిగి స్వాగతం",
    login_sub: "కృషి మిత్రలోకి లాగిన్ అవ్వండి",
    signup_welcome: "కొత్త ఖాతాను సృష్టించండి",
    signup_sub: "ఈరోజే కృషి మిత్రతో చేరండి",
    code: "te",
    name: "Telugu",
    nativeName: "తెలుగు",
    region: "దక్షిణ భారతదేశం (ఆంధ్రప్రదేశ్, తెలంగాణ)",
    badge: "Andhra & Telangana"
  },
  ta: {
    nav_signin: "உள்நுழைக",
    nav_mandi: "மண்டி விலை & MSP",
    nav_mandi_direct: "மண்டி விலை",
    tab_login: "உள்நுழை",
    tab_signup: "கணக்கை உருவாக்கு",
    login_welcome: "மீண்டும் வருக",
    login_sub: "கிருஷி மித்ராவில் உள்நுழையவும்",
    signup_welcome: "புதிய கணக்கை உருவாக்கவும்",
    signup_sub: "இன்றே கிருஷி மித்ராவுடன் இணையுங்கள்",
    code: "ta",
    name: "Tamil",
    nativeName: "தமிழ்",
    region: "தென்னிந்தியா (தமிழ்நாடு, புதுச்சேரி)",
    badge: "Tamil Nadu"
  },
  kn: {
    nav_signin: "ಸೈನ್ ಇನ್",
    nav_mandi: "ಮಂಡಿ ಬೆಲೆಗಳು & MSP",
    nav_mandi_direct: "ಮಂಡಿ ಬೆಲೆ",
    tab_login: "ಲಾಗಿನ್",
    tab_signup: "ಖಾತೆ ರಚಿಸಿ",
    login_welcome: "ಮತ್ತೆ ಸ್ವಾಗತ",
    login_sub: "ಕೃಷಿ ಮಿತ್ರಗೆ ಲಾಗಿನ್ ಮಾಡಿ",
    signup_welcome: "ಹೊಸ ಖಾತೆ ರಚಿಸಿ",
    signup_sub: "ಇಂದೇ ಕೃಷಿ ಮಿತ್ರ ಜೊತೆ ಸೇರಿಕೊಳ್ಳಿ",
    code: "kn",
    name: "Kannada",
    nativeName: "ಕನ್ನಡ",
    region: "ದಕ್ಷಿಣ ಭಾರತ (ಕರ್ನಾಟಕ)",
    badge: "Karnataka"
  },
  ml: {
    nav_signin: "സൈൻ ഇൻ",
    nav_mandi: "വിപണി വിലകളും MSP യും",
    nav_mandi_direct: "വിപണി വില",
    tab_login: "ലോഗിൻ",
    tab_signup: "അക്കൗണ്ട് സൃഷ്ടിക്കുക",
    login_welcome: "സ്വാഗതം",
    login_sub: "കൃഷി മിത്രയിലേക്ക് ലോഗിൻ ചെയ്യുക",
    signup_welcome: "പുതിയ അക്കൗണ്ട് സൃഷ്ടിക്കുക",
    signup_sub: "ഇന്ന് തന്നെ കൃഷി മിത്രയോടൊപ്പം ചേരൂ",
    code: "ml",
    name: "Malayalam",
    nativeName: "മലയാളം",
    region: "ദക്ഷിണേന്ത്യ (കേരളം, ലക്ഷദ്വീപ്)",
    badge: "Kerala"
  }
};

const KRISHI_TRANSLATIONS = {
  en: {
    nav_home: "Home",
    nav_features: "Features",
    nav_crop_rec: "Crop Recommendation",
    nav_crop_guide: "Crop Guide",
    nav_weather: "Weather",
    nav_disease: "Disease Detection",
    nav_calc: "Profit Calculator",
    nav_sustainability: "Sustainability",
    nav_krishi_seva: "Krishi Seva",
    nav_chat: "AI Chat",
    nav_about: "About",
    nav_contact: "Contact",
    nav_account: "Account",
    nav_profile: "My Profile",
    nav_admin: "Admin Panel",
    nav_settings: "Settings",
    nav_login: "Login",
    nav_signup: "Sign Up",
    nav_logout: "Logout",
    nav_language: "Language",

    hero_title: "Welcome to Krishi Mitra",
    hero_subtitle: "Your Trusted Smart Farming Assistant",
    hero_desc: "Your trusted digital farming companion for higher crop yield, instant disease diagnosis, real-time mandi prices, daily agricultural news, and verified government subsidies.",
    cta_chat: "Start Chatting",

    features_heading: "Our Features",
    feat_chat_title: "AI Chat Assistant",
    feat_chat_desc: "Ask any agriculture-related question. Supports text and image inputs for comprehensive farming advice.",
    feat_chat_btn: "Try Chat",
    feat_weather_title: "Weather-Based Decisions",
    feat_weather_desc: "Get real-time weather data and AI-powered farming recommendations based on current conditions.",
    feat_weather_btn: "Check Weather",
    feat_disease_title: "Crop Disease Detection",
    feat_disease_desc: "Upload crop images for instant disease identification, diagnosis, and treatment recommendations.",
    feat_disease_btn: "Detect Disease",
    feat_calc_title: "Resource & Profit Calculator",
    feat_calc_desc: "Calculate water, fertilizer, and cost requirements based on crop type and farm size.",
    feat_calc_btn: "Calculate",
    feat_sust_title: "Sustainability Tips",
    feat_sust_desc: "Learn eco-friendly farming practices for environmental sustainability and long-term soil health.",
    feat_sust_btn: "Learn More",
    feat_rag_title: "RAG Knowledge Base",
    feat_rag_desc: "Powered by retrieval-augmented generation with agricultural documents and government schemes.",
    feat_rag_btn: "Explore",

    crop_rec_title: "Crop Recommendation System",
    crop_rec_subtitle: "Get AI-powered crop suggestions based on soil and weather conditions",
    mode_autofill: "Auto-Fill (State/District)",
    mode_manual: "Manual Input",
    select_state: "Select State",
    select_district: "Select District",
    btn_my_location: "Use My Location",
    btn_autofill: "Auto-Fill Values",
    btn_predict: "Predict Suitable Crops",

    disease_title: "Crop Disease Detection",
    disease_subtitle: "Upload a photo of your crop for instant disease diagnosis and treatment recommendations",
    btn_analyze_disease: "Analyze for Diseases",

    weather_title: "Weather Advisory",
    weather_subtitle: "Real-time weather data and crop-specific farming decisions",
    btn_check_weather: "Get Weather & Advice",

    calc_title: "Profit & Resource Calculator",
    calc_subtitle: "Calculate cultivation expenses, expected yield, revenue, and net profit",
    btn_calculate_profit: "Calculate Profit",

    sust_title: "Sustainable Farming Tips",
    sust_subtitle: "Learn eco-friendly practices for environmental sustainability",

    krishi_title: "Krishi Seva Hub",
    krishi_subtitle: "Government Schemes & Soil Testing Laboratories",

    settings_lang_title: "Default Language Setting",
    settings_lang_desc: "Choose your preferred regional language. It will be saved as your default across all features.",
    btn_save_lang: "Save as Default Language",
    lang_modal_title: "Choose Your Language",
    lang_modal_subtitle: "Select your preferred regional language to personalize your experience:",

    nav_news: "Daily Agri News & Alerts",
    nav_news_direct: "Agri News",
    ad_flair: "Farmer Marketplace & Subsidies",
    ad_carousel_title: "Featured Agricultural Deals & Verified Offers",
    home_news_live: "Updated Today • Live RSS",
    home_news_heading: "Daily Krishi Samachar & Weather Alerts",
    view_all_news: "View All Agri News →",
    news_live_badge: "Live Agricultural Feed • Updated Daily",
    news_main_title: "Daily Krishi Samachar & Advisories",
    news_subtitle: "Stay updated with real-time Indian farming news, MSP announcements, IMD monsoon forecasts, government subsidy deadlines, and pest advisories.",
    news_breaking_label: "Latest Headline",
    news_search_ph: "Search news by topic (e.g., MSP, Subsidy, Monsoon, Fertilizer, Drone)..."
  },

  hi: {
    nav_home: "होम",
    nav_features: "सुविधाएं",
    nav_crop_rec: "फसल अनुशंसा",
    nav_crop_guide: "फसल मार्गदर्शिका",
    nav_weather: "मौसम परामर्श",
    nav_disease: "रोग पहचान",
    nav_calc: "लाभ कैलकुलेटर",
    nav_sustainability: "संधारणीय खेती",
    nav_krishi_seva: "कृषि सेवा",
    nav_chat: "एआई चैट",
    nav_about: "हमारे बारे में",
    nav_contact: "संपर्क",
    nav_account: "खाता",
    nav_profile: "मेरी प्रोफ़ाइल",
    nav_admin: "एडमिन पैनल",
    nav_settings: "सेटिंग्स",
    nav_login: "लॉगिन",
    nav_signup: "साइन अप",
    nav_logout: "लॉगआउट",
    nav_language: "भाषा",

    hero_title: "कृषि मित्र में आपका स्वागत है",
    hero_subtitle: "आपका भरोसेमंद स्मार्ट कृषि सहायक",
    hero_desc: "बेहतर पैदावार, फसल रोग निदान, ताजा मंडी भाव, दैनिक कृषि समाचार और सरकारी योजनाओं के लिए आपका भरोसेमंद डिजिटल कृषि साथी।",
    cta_chat: "चैट शुरू करें",

    features_heading: "हमारी मुख्य सुविधाएं",
    feat_chat_title: "एआई चैट सहायक",
    feat_chat_desc: "कृषि संबंधी कोई भी प्रश्न पूछें। संपूर्ण सलाह के लिए टेक्स्ट और फ़ोटो दोनों का समर्थन।",
    feat_chat_btn: "चैट करें",
    feat_weather_title: "मौसम आधारित निर्णय",
    feat_weather_desc: "वर्तमान मौसम के अनुसार वास्तविक समय में खेती और सिंचाई संबंधी सिफारिशें पाएं।",
    feat_weather_btn: "मौसम देखें",
    feat_disease_title: "फसल रोग पहचान",
    feat_disease_desc: "तुरंत रोग पहचान, निदान और उपचार की सलाह के लिए फसल की पत्ती की तस्वीर अपलोड करें।",
    feat_disease_btn: "रोग जांचें",
    feat_calc_title: "लागत एवं लाभ कैलकुलेटर",
    feat_calc_desc: "फसल के प्रकार और खेत के आकार के आधार पर पानी, खाद और मुनाफ़े का सटीक अनुमान लगाएं।",
    feat_calc_btn: "गणना करें",
    feat_sust_title: "संधारणीय खेती टिप्स",
    feat_sust_desc: "दीर्घकालिक मिट्टी स्वास्थ्य और पर्यावरण संरक्षण के लिए जैविक एवं प्राकृतिक विधियां सीखें।",
    feat_sust_btn: "और जानें",
    feat_rag_title: "ज्ञान एवं सरकारी योजनाएं",
    feat_rag_desc: "सरकारी योजनाओं (PM-KISAN, PMFBY, KCC) और कृषि शोध से सत्यापित प्रमाणिक जानकारी।",
    feat_rag_btn: "खोजें",

    crop_rec_title: "फसल अनुशंसा प्रणाली",
    crop_rec_subtitle: "मिट्टी और मौसम की स्थिति के आधार पर सर्वाधिक उपयुक्त फसलों की सिफारिश",
    mode_autofill: "स्वतः भरें (राज्य/ज़िला)",
    mode_manual: "स्वयं भरें",
    select_state: "राज्य चुनें",
    select_district: "ज़िला चुनें",
    btn_my_location: "मेरा स्थान उपयोग करें",
    btn_autofill: "मान स्वतः भरें",
    btn_predict: "उपयुक्त फसलें जानें",

    disease_title: "फसल रोग पहचान",
    disease_subtitle: "तुरंत रोग निदान और उपचार की सलाह के लिए अपनी फसल की फ़ोटो अपलोड करें",
    btn_analyze_disease: "रोग की जांच करें",

    weather_title: "मौसम परामर्श",
    weather_subtitle: "वास्तविक समय मौसम और फसल-विशिष्ट कृषि सलाह",
    btn_check_weather: "मौसम और सलाह प्राप्त करें",

    calc_title: "मुनाफ़ा एवं संसाधन कैलकुलेटर",
    calc_subtitle: "खेती की लागत, अनुमानित पैदावार, बाज़ार भाव और शुद्ध लाभ की गणना करें",
    btn_calculate_profit: "लाभ की गणना करें",

    sust_title: "संधारणीय खेती के उपाय",
    sust_subtitle: "पर्यावरण के अनुकूल और टिकाऊ खेती के लिए जैविक तरीके सीखें",

    krishi_title: "कृषि सेवा केंद्र",
    krishi_subtitle: "सरकारी योजनाएं और मृदा परीक्षण प्रयोगशालाएं",

    settings_lang_title: "डिफ़ॉल्ट भाषा सेटिंग",
    settings_lang_desc: "अपनी पसंदीदा क्षेत्रीय भाषा चुनें। यह सभी सुविधाओं के लिए स्थायी रूप से सहेजी जाएगी।",
    btn_save_lang: "डिफ़ॉल्ट भाषा के रूप में सहेजें",
    lang_modal_title: "अपनी भाषा चुनें",
    lang_modal_subtitle: "कृषि मित्र को अपनी पसंदीदा क्षेत्रीय भाषा में चलाने के लिए चुनें:",

    nav_news: "दैनिक कृषि समाचार एवं अलर्ट",
    nav_news_direct: "कृषि समाचार",
    ad_flair: "किसान बाज़ार एवं सरकारी सब्सिडी",
    ad_carousel_title: "कृषि विशेष ऑफ़र एवं सत्यापित सब्सिडी योजनाएं",
    home_news_live: "आज का ताज़ा अपडेट • लाइव RSS",
    home_news_heading: "दैनिक कृषि समाचार एवं मौसम चेतावनी",
    view_all_news: "सभी कृषि समाचार देखें →",
    news_live_badge: "लाइव कृषि फ़ीड • प्रतिदिन अपडेट",
    news_main_title: "दैनिक कृषि समाचार एवं परामर्श",
    news_subtitle: "भारतीय कृषि, न्यूनतम समर्थन मूल्य (MSP), मौसम पूर्वानुमान, खाद-बीज और सरकारी सब्सिडी की ताज़ा जानकारी प्राप्त करें।",
    news_breaking_label: "ताज़ा मुख्य समाचार",
    news_search_ph: "विषय अनुसार खोजें (जैसे: MSP, सब्सिडी, बारिश, खाद, ड्रोन)..."
  },

  pa: {
    nav_home: "ਮੁੱਖ ਪੰਨਾ",
    nav_features: "ਸਹੂਲਤਾਂ",
    nav_crop_rec: "ਫ਼ਸਲ ਸਿਫ਼ਾਰਸ਼",
    nav_crop_guide: "ਫ਼ਸਲ ਗਾਈਡ",
    nav_weather: "ਮੌਸਮ ਸਲਾਹ",
    nav_disease: "ਬਿਮਾਰੀ ਜਾਂਚ",
    nav_calc: "ਮੁਨਾਫ਼ਾ ਕੈਲਕੁਲੇਟਰ",
    nav_sustainability: "ਟਿਕਾਊ ਖੇਤੀ",
    nav_krishi_seva: "ਕ੍ਰਿਸ਼ੀ ਸੇਵਾ",
    nav_chat: "ਏਆਈ ਚੈਟ",
    nav_about: "ਸਾਡੇ ਬਾਰੇ",
    nav_contact: "ਸੰਪਰਕ",
    nav_account: "ਖਾਤਾ",
    nav_profile: "ਮੇਰੀ ਪ੍ਰੋਫਾਈਲ",
    nav_admin: "ਐਡਮਿਨ ਪੈਨਲ",
    nav_settings: "ਸੈਟਿੰਗਾਂ",
    nav_login: "ਲੌਗਇਨ",
    nav_signup: "ਸਾਈਨ ਅੱਪ",
    nav_logout: "ਲੌਗਆਉਟ",
    nav_language: "ਭਾਸ਼ਾ",

    hero_title: "ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਵਿੱਚ ਤੁਹਾਡਾ ਸਵਾਗਤ ਹੈ",
    hero_subtitle: "ਤੁਹਾਡਾ ਏਆਈ-ਅਧਾਰਤ ਸਮਾਰਟ ਖੇਤੀ ਸਹਾਇਕ",
    hero_desc: "ਸਟੀਕ ਖੇਤੀ, ਖਾਦ-ਪਾਣੀ ਦੀ ਬਚਤ ਅਤੇ ਟਿਕਾਊ ਖੇਤੀ ਲਈ ਆਧੁਨਿਕ ਏਆਈ ਤਕਨੀਕ।",
    cta_chat: "ਚੈਟ ਸ਼ੁਰੂ ਕਰੋ",

    features_heading: "ਸਾਡੀਆਂ ਸਹੂਲਤਾਂ",
    feat_chat_title: "ਏਆਈ ਚੈਟ ਸਹਾਇਕ",
    feat_chat_desc: "ਖੇਤੀ ਨਾਲ ਸਬੰਧਤ ਕੋਈ ਵੀ ਸਵਾਲ ਪੁੱਛੋ। ਫ਼ੋਟੋ ਅਤੇ ਲਿਖਤੀ ਸਵਾਲ ਦੋਵਾਂ ਦੀ ਸੁਵਿਧਾ।",
    feat_chat_btn: "ਚੈਟ ਕਰੋ",
    feat_weather_title: "ਮੌਸਮ ਅਧਾਰਤ ਸਲਾਹ",
    feat_weather_desc: "ਮੌਜੂਦਾ ਮੌਸਮ ਅਨੁਸਾਰ ਸਿੰਚਾਈ ਅਤੇ ਫ਼ਸਲ ਸੰਭਾਲ ਦੇ ਤਾਜ਼ਾ ਸੁਝਾਅ।",
    feat_weather_btn: "ਮੌਸਮ ਵੇਖੋ",
    feat_disease_title: "ਫ਼ਸਲ ਦੀ ਬਿਮਾਰੀ ਜਾਂਚ",
    feat_disease_desc: "ਪੱਤੇ ਦੀ ਫ਼ੋਟੋ ਅਪਲੋਡ ਕਰਕੇ ਬਿਮਾਰੀ ਦਾ ਪਤਾ ਅਤੇ ਇਲਾਜ ਦੇ ਤਰੀਕੇ ਜਾਣੋ।",
    feat_disease_btn: "ਜਾਂਚ ਕਰੋ",
    feat_calc_title: "ਖਰਚ ਅਤੇ ਮੁਨਾਫ਼ਾ ਕੈਲਕੁਲੇਟਰ",
    feat_calc_desc: "ਜ਼ਮੀਨ ਅਤੇ ਫ਼ਸਲ ਅਨੁਸਾਰ ਬੀਜ, ਖਾਦ, ਪਾਣੀ ਅਤੇ ਸ਼ੁੱਧ ਮੁਨਾਫ਼ੇ ਦਾ ਹਿਸਾਬ ਲਗਾਓ।",
    feat_calc_btn: "ਹਿਸਾਬ ਕਰੋ",
    feat_sust_title: "ਟਿਕਾਊ ਖੇਤੀ ਦੇ ਸੁਝਾਅ",
    feat_sust_desc: "ਜ਼ਮੀਨ ਦੀ ਉਪਜਾਊ ਸ਼ਕਤੀ ਵਧਾਉਣ ਲਈ ਦੇਸੀ ਅਤੇ ਜੈਵਿਕ ਖੇਤੀ ਤਰੀਕੇ।",
    feat_sust_btn: "ਹੋਰ ਜਾਣੋ",
    feat_rag_title: "ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਤੇ ਜਾਣਕਾਰੀ",
    feat_rag_desc: "ਪੀਐਮ-ਕਿਸਾਨ, ਫ਼ਸਲ ਬੀਮਾ ਅਤੇ ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ ਬਾਰੇ ਪੂਰੀ ਜਾਣਕਾਰੀ।",
    feat_rag_btn: "ਵੇਖੋ",

    crop_rec_title: "ਫ਼ਸਲ ਸਿਫ਼ਾਰਸ਼ ਪ੍ਰਣਾਲੀ",
    crop_rec_subtitle: "ਮਿੱਟੀ ਅਤੇ ਮੌਸਮ ਅਨੁਸਾਰ ਸਭ ਤੋਂ ਵਧੀਆ ਫ਼ਸਲ ਚੁਣੋ",
    mode_autofill: "ਆਪਣੇ ਆਪ ਭਰੋ (ਸੂਬਾ/ਜ਼ਿਲ੍ਹਾ)",
    mode_manual: "ਖੁਦ ਦਰਜ ਕਰੋ",
    select_state: "ਸੂਬਾ ਚੁਣੋ",
    select_district: "ਜ਼ਿਲ੍ਹਾ ਚੁਣੋ",
    btn_my_location: "ਮੇਰੀ ਲੋਕੇਸ਼ਨ ਵਰਤੋ",
    btn_autofill: "ਮੁੱਲ ਆਪਣੇ ਆਪ ਭਰੋ",
    btn_predict: "ਢੁਕਵੀਆਂ ਫ਼ਸਲਾਂ ਲੱਭੋ",

    disease_title: "ਫ਼ਸਲ ਰੋਗ ਜਾਂਚ",
    disease_subtitle: "ਰੋਗ ਜਾਂਚ ਅਤੇ ਇਲਾਜ ਲਈ ਆਪਣੀ ਫ਼ਸਲ ਦੀ ਤਸਵੀਰ ਅਪਲੋਡ ਕਰੋ",
    btn_analyze_disease: "ਬਿਮਾਰੀ ਦੀ ਜਾਂਚ ਕਰੋ",

    weather_title: "ਮੌਸਮ ਸਲਾਹਕਾਰ",
    weather_subtitle: "ਮੌਸਮ ਅਨੁਸਾਰ ਖੇਤੀ ਅਤੇ ਸਿੰਚਾਈ ਦੀਆਂ ਸਿਫ਼ਾਰਸ਼ਾਂ",
    btn_check_weather: "ਮੌਸਮ ਅਤੇ ਸਲਾਹ ਲਵੋ",

    calc_title: "ਮੁਨਾਫ਼ਾ ਤੇ ਸਰੋਤ ਕੈਲਕੁਲੇਟਰ",
    calc_subtitle: "ਖ਼ਰਚਾ, ਸੰਭਾਵਿਤ ਝਾੜ, ਬਾਜ਼ਾਰ ਭਾਅ ਅਤੇ ਕੁੱਲ ਮੁਨਾਫ਼ਾ ਜਾਣੋ",
    btn_calculate_profit: "ਮੁਨਾਫ਼ੇ ਦਾ ਹਿਸਾਬ ਲਾਓ",

    sust_title: "ਟਿਕਾਊ ਖੇਤੀਬਾੜੀ ਸੁਝਾਅ",
    sust_subtitle: "ਜੈਵਿਕ ਅਤੇ ਕੁਦਰਤੀ ਤਰੀਕਿਆਂ ਨਾਲ ਵਾਤਾਵਰਣ ਦੀ ਸੰਭਾਲ",

    krishi_title: "ਕ੍ਰਿਸ਼ੀ ਸੇਵਾ ਹੱਬ",
    krishi_subtitle: "ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਅਤੇ ਮਿੱਟੀ ਪਰਖ ਲੈਬਾਰਟਰੀਆਂ",

    settings_lang_title: "ਮੂਲ ਭਾਸ਼ਾ ਸੈਟਿੰਗ",
    settings_lang_desc: "ਆਪਣੀ ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ ਚੁਣੋ। ਇਹ ਹਮੇਸ਼ਾ ਲਈ ਤੁਹਾਡੀ ਡਿਫਾਲਟ ਭਾਸ਼ਾ ਬਣ ਜਾਵੇਗੀ।",
    btn_save_lang: "ਮੂਲ ਭਾਸ਼ਾ ਵਜੋਂ ਸੁਰੱਖਿਅਤ ਕਰੋ",
    lang_modal_title: "ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ",
    lang_modal_subtitle: "ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਨੂੰ ਆਪਣੀ ਪਸੰਦੀਦਾ ਖੇਤਰੀ ਭਾਸ਼ਾ ਵਿੱਚ ਵਰਤਣ ਲਈ ਚੁਣੋ:",

    nav_news: "ਰੋਜ਼ਾਨਾ ਖੇਤੀ ਖ਼ਬਰਾਂ ਤੇ ਅਲਰਟ",
    nav_news_direct: "ਖੇਤੀ ਖ਼ਬਰਾਂ",
    ad_flair: "ਕਿਸਾਨ ਬਾਜ਼ਾਰ ਅਤੇ ਸਬਸਿਡੀਆਂ",
    ad_carousel_title: "ਖੇਤੀਬਾੜੀ ਖਾਸ ਆਫ਼ਰਾਂ ਅਤੇ ਸਰਕਾਰੀ ਸਕੀਮਾਂ",
    home_news_live: "ਅੱਜ ਦਾ ਤਾਜ਼ਾ ਅਪਡੇਟ • ਲਾਈਵ RSS",
    home_news_heading: "ਰੋਜ਼ਾਨਾ ਖੇਤੀ ਖ਼ਬਰਾਂ ਅਤੇ ਮੌਸਮ ਚੇਤਾਵਨੀਆਂ",
    view_all_news: "ਸਾਰੀਆਂ ਖੇਤੀ ਖ਼ਬਰਾਂ ਵੇਖੋ →",
    news_live_badge: "ਲਾਈਵ ਖੇਤੀ ਫੀਡ • ਰੋਜ਼ਾਨਾ ਅਪਡੇਟ",
    news_main_title: "ਰੋਜ਼ਾਨਾ ਕ੍ਰਿਸ਼ੀ ਸਮਾਚਾਰ ਅਤੇ ਸਲਾਹ",
    news_subtitle: "ਤਾਜ਼ਾ ਭਾਰਤੀ ਖੇਤੀਬਾੜੀ ਖ਼ਬਰਾਂ, MSP, ਮੌਸਮ ਪੂਰਵ-ਅਨੁਮਾਨ ਅਤੇ ਖਾਦ-ਬੀਜ ਸਬਸਿਡੀਆਂ ਦੀ ਪੂਰੀ ਜਾਣਕਾਰੀ।",
    news_breaking_label: "ਮੁੱਖ ਸੁਰਖੀ",
    news_search_ph: "ਖ਼ਬਰਾਂ ਖੋਜੋ (ਜਿਵੇਂ: MSP, ਸਬਸਿਡੀ, ਮੀਂਹ, ਖਾਦ, ਟਰੈਕਟਰ)..."
  },

  bn: {
    nav_home: "হোম",
    nav_features: "বৈশিষ্ট্য",
    nav_crop_rec: "ফসল সুপারিশ",
    nav_crop_guide: "ফসল গাইড",
    nav_weather: "আবহাওয়া",
    nav_disease: "রোগ নির্ণয়",
    nav_calc: "লাভ ক্যালকুলেটর",
    nav_sustainability: "টেকসই কৃষি",
    nav_krishi_seva: "কৃষি সেবা",
    nav_chat: "এআই চ্যাট",
    nav_about: "আমাদের সম্পর্কে",
    nav_contact: "যোগাযোগ",
    nav_account: "অ্যাকাউন্ট",
    nav_profile: "আমার প্রোফাইল",
    nav_admin: "অ্যাডমিন প্যানেল",
    nav_settings: "সেটিংস",
    nav_login: "লগইন",
    nav_signup: "সাইন আপ",
    nav_logout: "লগআউট",
    nav_language: "ভাষা",

    hero_title: "কৃষি মিত্রে স্বাগতম",
    hero_subtitle: "আপনার এআই-চালিত স্মার্ট কৃষি সহকারী",
    hero_desc: "নির্ভুল চাষাবাদ, সম্পদ সাশ্রয় এবং টেকসই কৃষির জন্য উন্নত এআই প্রযুক্তি।",
    cta_chat: "চ্যাট শুরু করুন",

    features_heading: "আমাদের সুবিধাসমূহ",
    feat_chat_title: "এআই চ্যাট সহকারী",
    feat_chat_desc: "কৃষি সংক্রান্ত যে কোনো প্রশ্ন জিজ্ঞাসা করুন। ছবি ও টেক্সট উভয়ের সুবিধা।",
    feat_chat_btn: "চ্যাট করুন",
    feat_weather_title: "আবহাওয়া ভিত্তিক সিদ্ধান্ত",
    feat_weather_desc: "বর্তমান আবহাওয়া অনুযায়ী সেচ এবং ফসল পরিচর্যার সুপরামর্শ পান।",
    feat_weather_btn: "আবহাওয়া দেখুন",
    feat_disease_title: "ফসল রোগ সনাক্তকরণ",
    feat_disease_desc: "পাতার ছবি আপলোড করে দ্রুত রোগ নির্ণয় এবং প্রতিকার জানুন।",
    feat_disease_btn: "রোগ পরীক্ষা করুন",
    feat_calc_title: "লাভ ও সম্পদ ক্যালকুলেটর",
    feat_calc_desc: "জমির পরিমাণ অনুযায়ী সার, জল এবং আর্থিক লাভের সঠিক হিসাব।",
    feat_calc_btn: "হিসাব করুন",
    feat_sust_title: "টেকসই চাষের পরামর্শ",
    feat_sust_desc: "মাটির উর্বরতা বৃদ্ধি এবং পরিবেশবান্ধব জৈব চাষের পদ্ধতি জানুন।",
    feat_sust_btn: "আরও জানুন",
    feat_rag_title: "সরকারি প্রকল্প ও জ্ঞান",
    feat_rag_desc: "পিএম-কিসান, ফসল বিমা এবং সরকারি অনুদান সম্পর্কিত নির্ভুল তথ্য।",
    feat_rag_btn: "খুঁজুন",

    crop_rec_title: "ফসল সুপারিশ ব্যবস্থা",
    crop_rec_subtitle: "মাটি ও জলবায়ুর ভিত্তিতে সেরা ফসলের পরামর্শ",
    mode_autofill: "স্বয়ংক্রিয় পূরণ (রাজ্য/জেলা)",
    mode_manual: "হাতে লিখুন",
    select_state: "রাজ্য বাছুন",
    select_district: "জেলা বাছুন",
    btn_my_location: "আমার অবস্থান নিন",
    btn_autofill: "স্বয়ংক্রিয় মান দিন",
    btn_predict: "উপযুক্ত ফসল খুঁজুন",

    disease_title: "ফসল রোগ সনাক্তকরণ",
    disease_subtitle: "রোগ নির্ণয়ের জন্য ফসলের ছবি আপলোড করুন",
    btn_analyze_disease: "রোগ পরীক্ষা করুন",

    weather_title: "আবহাওয়া পরামর্শ",
    weather_subtitle: "রিয়েল-টাইম আবহাওয়া ও ফসল সুরক্ষা পরামর্শ",
    btn_check_weather: "আবহাওয়া ও পরামর্শ পান",

    calc_title: "মুনাফা ও সম্পদ ক্যালকুলেটর",
    calc_subtitle: "চাষের খরচ, ফলন এবং মোট লাভের হিসাব করুন",
    btn_calculate_profit: "মুনাফা হিসাব করুন",

    sust_title: "টেকসই কৃষির নির্দেশিকা",
    sust_subtitle: "জৈব সার ও পরিবেশবান্ধব চাষাবাদের কৌশল",

    krishi_title: "কৃষি সেবা কেন্দ্র",
    krishi_subtitle: "সরকারি প্রকল্প ও মৃত্তিকা পরীক্ষা গবেষণাগার",

    settings_lang_title: "ডিফল্ট ভাষা সেটিংস",
    settings_lang_desc: "আপনার পছন্দের ভাষা নির্বাচন করুন। এটি আপনার ডিফল্ট ভাষা হিসেবে সংরক্ষিত হবে।",
    btn_save_lang: "ডিফল্ট হিসেবে সংরক্ষণ করুন",
    lang_modal_title: "আপনার ভাষা নির্বাচন করুন",
    lang_modal_subtitle: "কৃষি মিত্রকে আপনার পছন্দের ভাষায় ব্যবহার করতে বেছে নিন:",

    nav_news: "দৈনিক কৃষি সংবাদ ও সতর্কতা",
    nav_news_direct: "কৃষি সংবাদ",
    ad_flair: "কৃষক বাজার ও সরকারি ভর্তুকি",
    ad_carousel_title: "কৃষি বিশেষ অফার ও যাচাইকৃত প্রকল্পসমূহ",
    home_news_live: "আজকের তাজা আপডেট • লাইভ RSS",
    home_news_heading: "দৈনিক কৃষি সমাচার ও আবহাওয়া সতর্কতা",
    view_all_news: "সকল কৃষি সংবাদ দেখুন →",
    news_live_badge: "লাইভ কৃষি ফিড • প্রতিদিন আপডেট",
    news_main_title: "দৈনিক কৃষি সমাচার ও পরামর্শ",
    news_subtitle: "ভারতীয় কৃষি, সহায়ক মূল্য (MSP), আবহাওয়া পূর্বাভাস এবং সরকারি ভর্তুকির তাজা খবরাখবর।",
    news_breaking_label: "তাজা শিরোনাম",
    news_search_ph: "বিষয় অনুযায়ী খুঁজুন (যেমন: MSP, ভর্তুকি, বৃষ্টি, সার, ড্রোন)..."
  },

  mr: {
    nav_home: "मुख्यपृष्ठ",
    nav_features: "वैशिष्ट्ये",
    nav_crop_rec: "पीक शिफारस",
    nav_crop_guide: "पीक मार्गदर्शक",
    nav_weather: "हवामान सल्ला",
    nav_disease: "रोग निदान",
    nav_calc: "नफा कॅल्क्युलेटर",
    nav_sustainability: "शाश्वत शेती",
    nav_krishi_seva: "कृषी सेवा",
    nav_chat: "एआय चॅट",
    nav_about: "आमच्याबद्दल",
    nav_contact: "संपर्क",
    nav_account: "खाते",
    nav_profile: "माझी प्रोफाइल",
    nav_admin: "ॲडमिन पॅनेल",
    nav_settings: "सेटिंग्ज",
    nav_login: "लॉगिन",
    nav_signup: "साइन अप",
    nav_logout: "लॉगआउट",
    nav_language: "भाषा",

    hero_title: "कृषी मित्र मध्ये आपले स्वागत आहे",
    hero_subtitle: "तुमचा एआय-आधारित स्मार्ट कृषी सहाय्यक",
    hero_desc: "अचूक शेती, खत-पाण्याची बचत आणि शाश्वत उत्पादकतेसाठी आधुनिक एआय तंत्रज्ञान.",
    cta_chat: "चॅट सुरू करा",

    features_heading: "आमची मुख्य वैशिष्ट्ये",
    feat_chat_title: "एआय चॅट सहाय्यक",
    feat_chat_desc: "शेतीविषयक कोणताही प्रश्न विचारा. फोटो आणि मजकूर दोन्हीद्वारे सल्ला.",
    feat_chat_btn: "चॅट करा",
    feat_weather_title: "हवामान सल्ला",
    feat_weather_desc: "वर्तमान हवामानानुसार सिंचन आणि कीड नियंत्रणाचे ताजे सल्ले मिळवा.",
    feat_weather_btn: "हवामान पहा",
    feat_disease_title: "पीक रोग निदान",
    feat_disease_desc: "पानाचा फोटो अपलोड करून रोगाची तात्काळ तपासणी आणि उपाय जाणून घ्या.",
    feat_disease_btn: "रोग तपासा",
    feat_calc_title: "नफा व खर्च कॅल्क्युलेटर",
    feat_calc_desc: "जमीन आणि पिकानुसार बियाणे, खत, पाणी आणि निव्वळ नफ्याचे गणित.",
    feat_calc_btn: "हिशोब करा",
    feat_sust_title: "शाश्वत शेती सल्ले",
    feat_sust_desc: "सेंद्रिय खते, गांडूळ खत आणि पर्यावरणास पूरक शेतीचे मार्ग.",
    feat_sust_btn: "अधिक जाणून घ्या",
    feat_rag_title: "सरकारी योजना माहिती",
    feat_rag_desc: "पीएम-किसान, पीक विमा आणि इतर शासकीय योजनांची सविस्तर माहिती.",
    feat_rag_btn: "माहिती पहा",

    crop_rec_title: "पीक शिफारस प्रणाली",
    crop_rec_subtitle: "माती आणि हवामानानुसार सर्वाधिक फायदेशीर पिकांची शिफारस",
    mode_autofill: "स्वयं भरा (राज्य/जिल्हा)",
    mode_manual: "स्वतः भरा",
    select_state: "राज्य निवडा",
    select_district: "जिल्हा निवडा",
    btn_my_location: "माझे स्थान वापरा",
    btn_autofill: "मूल्ये आपोआप भरा",
    btn_predict: "योग्य पिके शोधा",

    disease_title: "पीक रोग निदान",
    disease_subtitle: "रोगाचे निदान आणि औषधोपचारासाठी पिकाचा फोटो अपलोड करा",
    btn_analyze_disease: "रोगाचे विश्लेषण करा",

    weather_title: "हवामान सल्लागार",
    weather_subtitle: "रिअल-टाइम हवामान आणि पीक संरक्षण सल्ला",
    btn_check_weather: "हवामान व सल्ला मिळवा",

    calc_title: "नफा व संसाधन कॅल्क्युलेटर",
    calc_subtitle: "लागवड खर्च, अपेक्षित उत्पादन आणि निव्वळ नफ्याचे अचूक अंदाज",
    btn_calculate_profit: "नफा मोजा",

    sust_title: "शाश्वत शेती मार्गदर्शन",
    sust_subtitle: "जमीन सुपीकता आणि नैसर्गिक शेतीसाठी उपयुक्त टिप्स",

    krishi_title: "कृषी सेवा केंद्र",
    krishi_subtitle: "शासकीय योजना आणि माती परीक्षण प्रयोगशाळा",

    settings_lang_title: "डीफॉल्ट भाषा सेटिंग",
    settings_lang_desc: "तुमची प्रादेशिक भाषा निवडा. ही तुमची कायमस्वरूपी भाषा म्हणून सेव्ह केली जाईल.",
    btn_save_lang: "डीफॉल्ट भाषा म्हणून सेव्ह करा",
    lang_modal_title: "तुमची भाषा निवडा",
    lang_modal_subtitle: "कृषी मित्र वापरण्यासाठी तुमची पसंतीची भाषा निवडा:",

    nav_news: "दैनिक कृषी बातम्या व सूचना",
    nav_news_direct: "कृषी बातम्या",
    ad_flair: "शेतकरी बाजार व सरकारी अनुदाने",
    ad_carousel_title: "कृषी विशेष ऑफर्स व पडताळणी केलेल्या योजना",
    home_news_live: "आजचे ताजे अपडेट • लाईव्ह RSS",
    home_news_heading: "दैनिक कृषी समाचार व हवामान इशारे",
    view_all_news: "सर्व कृषी बातम्या पहा →",
    news_live_badge: "लाईव्ह कृषी फीड • दररोज अपडेट",
    news_main_title: "दैनिक कृषी समाचार व सल्लागार",
    news_subtitle: "भारतीय शेती, हमीभाव (MSP), हवामान अंदाज आणि शासकीय अनुदान योजनांची अद्ययावत माहिती मिळवा.",
    news_breaking_label: "ताजी ठळक बातमी",
    news_search_ph: "विषयानुसार शोधा (उदा. हमीभाव, अनुदान, पाऊस, खते, सौर पंप)..."
  },

  gu: {
    nav_home: "હોમ",
    nav_features: "વિશેષતાઓ",
    nav_crop_rec: "પાક ભલામણ",
    nav_crop_guide: "પાક માર્ગદર્શિકા",
    nav_weather: "હવામાન સલાહ",
    nav_disease: "રોગ ઓળખ",
    nav_calc: "નફા કેલ્ક્યુલેટર",
    nav_sustainability: "ટકાઉ ખેતી",
    nav_krishi_seva: "કૃષિ સેવા",
    nav_chat: "AI ચેટ",
    nav_about: "અમારા વિશે",
    nav_contact: "સંપર્ક",
    nav_account: "ખાતું",
    nav_profile: "મારી પ્રોફાઇલ",
    nav_admin: "એડમિન પેનલ",
    nav_settings: "સેટિંગ્સ",
    nav_login: "લૉગિન",
    nav_signup: "સાઇન અપ",
    nav_logout: "લૉગઆઉટ",
    nav_language: "ભાષા",

    hero_title: "કૃષિ મિત્રમાં આપનું સ્વાગત છે",
    hero_subtitle: "તમારો AI-આધારિત સ્માર્ટ ખેતી સહાયક",
    hero_desc: "ચોક્કસ ખેતી, ખાતર-પાણીની બચત અને ટકાઉ કૃષિ માટે અત્યાધુનિક AI ટેકનોલોજી.",
    cta_chat: "ચેટ શરૂ કરો",

    features_heading: "અમારી મુખ્ય વિશેષતાઓ",
    feat_chat_title: "AI ચેટ સહાયક",
    feat_chat_desc: "ખેતી સંબંધિત કોઈપણ પ્રશ્ન પૂછો. ફોટો અને લખાણ બંને દ્વારા માર્ગદર્શન.",
    feat_chat_btn: "ચેટ કરો",
    feat_weather_title: "હવામાન આધારિત નિર્ણયો",
    feat_weather_desc: "વર્તમાન હવામાન અનુસાર પિયત અને પાક સંરક્ષણની સલાહ મેળવો.",
    feat_weather_btn: "હવામાન જુઓ",
    feat_disease_title: "પાક રોગ નિદાન",
    feat_disease_desc: "પાંદડાનો ફોટો અપલોડ કરી તરત જ રોગની ઓળખ અને દવાઓની માહિતી મેળવો.",
    feat_disease_btn: "રોગ તપાસો",
    feat_calc_title: "ખર્ચ અને નફા કેલ્ક્યુલેટર",
    feat_calc_desc: "જમીન અને પાક અનુસાર ખાતર, બિયારણ અને ચોખ્ખા નફાની ગણતરી કરો.",
    feat_calc_btn: "ગણતરી કરો",
    feat_sust_title: "ટકાઉ ખેતીની પદ્ધતિઓ",
    feat_sust_desc: "જમીનની ફળદ્રુપતા જાળવવા માટે પ્રાકૃતિક અને જૈવિક ખેતીના ઉપાયો.",
    feat_sust_btn: "વધુ જાણો",
    feat_rag_title: "સરકારી યોજનાઓ અને માહિતી",
    feat_rag_desc: "પીએમ-કિસાન, પાક વીમો અને અન્ય સહાયકારી સરકારી યોજનાઓની વિગતો.",
    feat_rag_btn: "તપાસો",

    crop_rec_title: "પાક ભલામણ પદ્ધતિ",
    crop_rec_subtitle: "જમીન અને હવામાન અનુસાર સૌથી યોગ્ય પાકની ભલામણ",
    mode_autofill: "ઓટો-ફિલ (રાજ્ય/જિલ્લો)",
    mode_manual: "હાથેથી લખો",
    select_state: "રાજ્ય પસંદ કરો",
    select_district: "જિલ્લો પસંદ કરો",
    btn_my_location: "મારું લોકેશન વાપરો",
    btn_autofill: "આપોઆપ મૂલ્યો ભરો",
    btn_predict: "યોગ્ય પાક શોધો",

    disease_title: "પાક રોગ નિદાન",
    disease_subtitle: "રોગની તપાસ માટે પાંદડાનો ફોટો અપલોડ કરો",
    btn_analyze_disease: "રોગ તપાસો",

    weather_title: "હવામાન સલાહકાર",
    weather_subtitle: "રિયલ-ટાઇમ હવામાન અને પાક સંરક્ષણ માહિતી",
    btn_check_weather: "હવામાન અને સલાહ મેળવો",

    calc_title: "નફો અને સંસાધન કેલ્ક્યુલેટર",
    calc_subtitle: "ખેતી ખર્ચ, અંદાજિત ઉત્પાદન અને ચોખ્ખા નફાની ગણતરી",
    btn_calculate_profit: "નફાની ગણતરી કરો",

    sust_title: "પ્રાકૃતિક ખેતી ટિપ્સ",
    sust_subtitle: "જીવામૃત, ઓર્ગેનિક ખાતરો અને પર્યાવરણને અનુકૂળ ખેતી",

    krishi_title: "કૃષિ સેવા કેન્દ્ર",
    krishi_subtitle: "સરકારી યોજનાઓ અને સોઇલ ટેસ્ટિંગ લેબોરેટરીઝ",

    settings_lang_title: "ડિફોલ્ટ ભાષા સેટિંગ",
    settings_lang_desc: "તમારી મનપસંદ પ્રાદેશિક ભાષા પસંદ કરો. તે આપોઆપ ડિફોલ્ટ ભાષા તરીકે સચવાશે.",
    btn_save_lang: "ડિફોલ્ટ ભાષા તરીકે સાચવો",
    lang_modal_title: "તમારી ભાષા પસંદ કરો",
    lang_modal_subtitle: "કૃષિ મિત્ર વાપરવા માટે તમારી માતૃભાષા પસંદ કરો:",

    nav_news: "દૈનિક કૃષિ સમાચાર અને ચેતવણીઓ",
    nav_news_direct: "કૃષિ સમાચાર",
    ad_flair: "ખેડૂત બજાર અને સરકારી સબસિડી",
    ad_carousel_title: "કૃષિ ખાસ ઑફર્સ અને ચકાસાયેલી યોજનાઓ",
    home_news_live: "આજનું નવું અપડેટ • લાઈવ RSS",
    home_news_heading: "દૈનિક કૃષિ સમાચાર અને હવામાન આગાહી",
    view_all_news: "બધા કૃષિ સમાચાર જુઓ →",
    news_live_badge: "લાઈવ કૃષિ ફીડ • રોજ અપડેટ",
    news_main_title: "દૈનિક કૃષિ સમાચાર અને માર્ગદર્શન",
    news_subtitle: "ભારતીય ખેતી, ટેકાના ભાવ (MSP), હવામાન આગાહી અને સરકારી સબસિડીના તાજા સમાચારો.",
    news_breaking_label: "મુખ્ય સમાચાર",
    news_search_ph: "વિષય અનુસાર શોધો (દા.ત. ટેકાના ભાવ, સબસિડી, વરસાદ, ખાતર)..."
  },

  te: {
    nav_home: "హోమ్",
    nav_features: "ఫీచర్లు",
    nav_crop_rec: "పంట సిఫార్సు",
    nav_crop_guide: "పంట గైడ్",
    nav_weather: "వాతావరణం",
    nav_disease: "తెగుళ్ల గుర్తింపు",
    nav_calc: "లాభం కాలిక్యులేటర్",
    nav_sustainability: "స్థిరమైన వ్యవసాయం",
    nav_krishi_seva: "కృషి సేవ",
    nav_chat: "AI చాట్",
    nav_about: "మా గురించి",
    nav_contact: "సంప్రదించండి",
    nav_account: "ఖాతా",
    nav_profile: "నా ప్రొఫైల్",
    nav_admin: "అడ్మిన్ ప్యానెల్",
    nav_settings: "సెట్టింగులు",
    nav_login: "లాగిన్",
    nav_signup: "సైన్ అప్",
    nav_logout: "లాగ్అవుట్",
    nav_language: "భాష",

    hero_title: "కృషి మిత్రకు స్వాగతం",
    hero_subtitle: "మీ AI ఆధారిత స్మార్ట్ వ్యవసాయ సహాయకుడు",
    hero_desc: "ఖచ్చితమైన వ్యవసాయం, వనరుల పొదుపు మరియు లాభదాయకమైన దిగుబడి కోసం ఆధునిక AI సాంకేతికత.",
    cta_chat: "చాట్ ప్రారంభించండి",

    features_heading: "మా ముఖ్య ఫీచర్లు",
    feat_chat_title: "AI చాట్ అసిస్టెంట్",
    feat_chat_desc: "వ్యవసాయంపై ఏ ప్రశ్ననైనా అడగండి. ఫోటో మరియు టెక్స్ట్ రెండింటి ద్వారా సలహాలు.",
    feat_chat_btn: "చాట్ చేయండి",
    feat_weather_title: "వాతావరణ ఆధారిత నిర్ణయాలు",
    feat_weather_desc: "ప్రస్తుత వాతావరణానికి అనుగుణంగా సాగు మరియు నీటిపారుదల సలహాలు.",
    feat_weather_btn: "వాతావరణం చూడండి",
    feat_disease_title: "పంట తెగుళ్ల గుర్తింపు",
    feat_disease_desc: "తెగుళ్ల నివారణ మరియు మందుల వివరాల కోసం పంట ఆకు ఫోటో అప్‌లోడ్ చేయండి.",
    feat_disease_btn: "తెగుళ్లను పరీక్షించండి",
    feat_calc_title: "లాభం & వనరుల కాలిక్యులేటర్",
    feat_calc_desc: "భూమి విస్తీర్ణం బట్టి విత్తనాలు, ఎరువులు, నీరు మరియు నికర లాభం లెక్కించండి.",
    feat_calc_btn: "లెక్కించండి",
    feat_sust_title: "స్థిరమైన సాగు పద్ధతులు",
    feat_sust_desc: "నేల సారాన్ని పెంచడానికి సేంద్రీయ ఎరువులు మరియు సహజ సాగు విధానాలు.",
    feat_sust_btn: "మరింత తెలుసుకోండి",
    feat_rag_title: "ప్రభుత్వ పథకాలు & సమాచారం",
    feat_rag_desc: "పీఎం-కిసాన్, పంటల బీమా మరియు ఇతర రైతు పథకాల వివరాలు.",
    feat_rag_btn: "చూడండి",

    crop_rec_title: "పంట సిఫార్సు విధానం",
    crop_rec_subtitle: "నేల స్వభావం మరియు వాతావరణం ఆధారంగా ఉత్తమ పంట ఎంపిక",
    mode_autofill: "ఆటో-ఫిల్ (రాష్ట్రం/జిల్లా)",
    mode_manual: "నేరుగా నమోదు చేయండి",
    select_state: "రాష్ట్రాన్ని ఎంచుకోండి",
    select_district: "జిల్లాను ఎంచుకోండి",
    btn_my_location: "నా లొకేషన్ ఉపయోగించండి",
    btn_autofill: "ఆటో ఫిల్ విలువలు",
    btn_predict: "సరిపోయే పంటలను కనుగొనండి",

    disease_title: "పంట తెగుళ్ల నిర్ధారణ",
    disease_subtitle: "తెగుళ్ల నివారణ చిట్కాల కోసం పంట ఫోటో అప్‌లోడ్ చేయండి",
    btn_analyze_disease: "తెగులు విశ్లేషించండి",

    weather_title: "వాతావరణ సలహా",
    weather_subtitle: "నిజ సమయ వాతావరణం మరియు పంట రక్షణ సలహాలు",
    btn_check_weather: "వాతావరణం & సలహా పొందండి",

    calc_title: "లాభం మరియు వనరుల కాలిక్యులేటర్",
    calc_subtitle: "సాగు ఖర్చులు, దిగుబడి, మార్కెట్ ధర మరియు నికర లాభం",
    btn_calculate_profit: "లాభాన్ని లెక్కించండి",

    sust_title: "సేంద్రీయ వ్యవసాయ చిట్కాలు",
    sust_subtitle: "భూమి ఆరోగ్యం మరియు పర్యావరణ పరిరక్షణకు సహజ పద్ధతులు",

    krishi_title: "కృషి సేవా కేంద్రం",
    krishi_subtitle: "ప్రభుత్వ పథకాలు మరియు భూసార పరీక్ష ప్రయోగశాలలు",

    settings_lang_title: "డిఫాల్ట్ భాష అమరిక",
    settings_lang_desc: "మీకు నచ్చిన ప్రాంతీయ భాషను ఎంచుకోండి. ఇది మీ శాశ్వత డిఫాల్ట్ భాషగా సేవ్ అవుతుంది.",
    btn_save_lang: "డిఫాల్ట్ భాషగా సేవ్ చేయండి",
    lang_modal_title: "మీ భాషను ఎంచుకోండి",
    lang_modal_subtitle: "కృషి మిత్రను మీ ప్రాంతీయ భాషలో ఉపయోగించడానికి ఎంచుకోండి:",

    nav_news: "రోజువారీ వ్యవసాయ వార్తలు & హెచ్చరికలు",
    nav_news_direct: "వ్యవసాయ వార్తలు",
    ad_flair: "రైతు బజార్ & ప్రభుత్వ సబ్సిడీలు",
    ad_carousel_title: "వ్యవసాయ ప్రత్యేక ఆఫర్లు & ధృవీకరించబడిన పథకాలు",
    home_news_live: "నేటి తాజా అప్‌డేట్ • లైవ్ RSS",
    home_news_heading: "రోజువారీ వ్యవసాయ వార్తలు & వాతావరణ సమాచారం",
    view_all_news: "అన్ని వ్యవసాయ వార్తలు చూడండి →",
    news_live_badge: "లైవ్ వ్యవసాయ ఫీడ్ • ప్రతిరోజూ అప్‌డేట్",
    news_main_title: "రోజువారీ కృషి సమాచార్ & సలహాలు",
    news_subtitle: "భారతీయ వ్యవసాయం, కనీస మద్దతు ధర (MSP), వాతావరణ సూచనలు మరియు ప్రభుత్వ సబ్సిడీల వివరాలు తెలుసుకోండి.",
    news_breaking_label: "తాజా ముఖ్యాంశాలు",
    news_search_ph: "టాపిక్ ద్వారా వెతకండి (ఉదా: మద్దతు ధర, సబ్సిడీ, వర్షం, ఎరువులు)..."
  },

  ta: {
    nav_home: "முகப்பு",
    nav_features: "அம்சங்கள்",
    nav_crop_rec: "பயிர் பரிந்துரை",
    nav_crop_guide: "பயிர் வழிகாட்டி",
    nav_weather: "வானிலை",
    nav_disease: "நோய் கண்டறிதல்",
    nav_calc: "லாப கால்குலேட்டர்",
    nav_sustainability: "நிலையான வேளாண்மை",
    nav_krishi_seva: "கிருஷி சேவை",
    nav_chat: "AI அரட்டை",
    nav_about: "எங்களைப் பற்றி",
    nav_contact: "தொடர்பு",
    nav_account: "கணக்கு",
    nav_profile: "சுயவிவரம்",
    nav_admin: "நிர்வாகக் குழு",
    nav_settings: "அமைப்புகள்",
    nav_login: "உள்நுழைக",
    nav_signup: "பதிவு செய்க",
    nav_logout: "வெளியேறு",
    nav_language: "மொழி",

    hero_title: "கிருஷி மித்ராவிற்கு நல்வரவு",
    hero_subtitle: "உங்கள் AI ஸ்மார்ட் விவசாய உதவியாளர்",
    hero_desc: "துல்லியமான விவசாயம், உர நீர் சேமிப்பு மற்றும் நிலையான வருமானத்திற்கான மேம்பட்ட AI தொழில்நுட்பம்.",
    cta_chat: "அரட்டையைத் தொடங்கு",

    features_heading: "முக்கிய அம்சங்கள்",
    feat_chat_title: "AI அரட்டை உதவியாளர்",
    feat_chat_desc: "விவசாயம் சார்ந்த எந்த கேள்வியையும் கேளுங்கள். படம் மற்றும் உரை இரண்டிற்கும் பதில்.",
    feat_chat_btn: "அரட்டை அடிக்க",
    feat_weather_title: "வானிலை சார் முடிவுகள்",
    feat_weather_desc: "தற்போதைய வானிலைக்கு ஏற்ப பாசனம் மற்றும் பயிர் பாதுகாப்பு ஆலோசனைகள்.",
    feat_weather_btn: "வானிலை பார்க்க",
    feat_disease_title: "பயிர் நோய் கண்டறிதல்",
    feat_disease_desc: "இலை புகைப்படத்தைப் பதிவேற்றி நோயைக் கண்டறிந்து தீர்வு பெறுங்கள்.",
    feat_disease_btn: "நோய் பரிசோதிக்க",
    feat_calc_title: "லாப கால்குலேட்டர்",
    feat_calc_desc: "நிலப்பரப்பிற்கு ஏற்ப உரம், விதை மற்றும் நிகர லாபத்தைக் கணக்கிடுங்கள்.",
    feat_calc_btn: "கணக்கிடு",
    feat_sust_title: "இயற்கை விவசாய ஆலோசனைகள்",
    feat_sust_desc: "மண் வளம் பெருக்கும் இயற்கை உரங்கள் மற்றும் பூச்சி மேலாண்மை.",
    feat_sust_btn: "மேலும் அறிய",
    feat_rag_title: "அரசுத் திட்டங்கள்",
    feat_rag_desc: "பிஎம்-கிசான், பயிர் காப்பீடு மற்றும் மானிய விவரங்கள்.",
    feat_rag_btn: "பார்க்க",

    crop_rec_title: "பயிர் பரிந்துரை அமைப்பு",
    crop_rec_subtitle: "மண் மற்றும் வானிலைக்கு உகந்த சிறந்த பயிர் தேர்வு",
    mode_autofill: "தானியங்கி தேர்வு (மாநிலம்/மாவட்டம்)",
    mode_manual: "கையேடு உள்ளீடு",
    select_state: "மாநிலத்தைத் தேர்ந்தெடுக்கவும்",
    select_district: "மாவட்டத்தைத் தேர்ந்தெடுக்கவும்",
    btn_my_location: "என் இருப்பிடத்தைப் பயன்படுத்து",
    btn_autofill: "தானாக நிரப்பவும்",
    btn_predict: "பொருத்தமான பயிர்களைக் கண்டறியவும்",

    disease_title: "பயிர் நோய் கண்டறிதல்",
    disease_subtitle: "நோய் கண்டறிதலுக்கு பயிர் புகைப்படத்தை பதிவேற்றவும்",
    btn_analyze_disease: "நோயை ஆராய்க",

    weather_title: "வானிலை ஆலோசனை",
    weather_subtitle: "நேரலை வானிலை மற்றும் பயிர் பாதுகாப்பு வழிமுறைகள்",
    btn_check_weather: "வானிலை மற்றும் ஆலோசனை பெறுக",

    calc_title: "லாப கால்குலேட்டர்",
    calc_subtitle: "சாகுபடி செலவு, விளைச்சல் மற்றும் நிகர லாப கணக்கீடு",
    btn_calculate_profit: "லாபத்தைக் கணக்கிடுக",

    sust_title: "நிலையான விவசாய குறிப்புகள்",
    sust_subtitle: "இயற்கை உரங்கள் மற்றும் மண் வள பாதுகாப்பு முறைகள்",

    krishi_title: "கிருஷி சேவை மையம்",
    krishi_subtitle: "அரசு திட்டங்கள் மற்றும் மண் பரிசோதனை ஆய்வகங்கள்",

    settings_lang_title: "இயல்புநிலை மொழி அமைப்பு",
    settings_lang_desc: "உங்கள் விருப்பமான பிராந்திய மொழியைத் தேர்ந்தெடுக்கவும். அது எப்போதும் சேமிக்கப்படும்.",
    btn_save_lang: "இயல்புநிலை மொழியாகச் சேமிக்கவும்",
    lang_modal_title: "உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்",
    lang_modal_subtitle: "கிருஷி மித்ராவை உங்கள் சொந்த மொழியில் பயன்படுத்த தேர்வு செய்யவும்:",

    nav_news: "தினசரி விவசாய செய்திகள் & எச்சரிக்கைகள்",
    nav_news_direct: "விவசாய செய்திகள்",
    ad_flair: "உழவர் சந்தை & அரசு மானியங்கள்",
    ad_carousel_title: "விவசாய சிறப்பு சலுகைகள் & சரிபார்க்கப்பட்ட திட்டங்கள்",
    home_news_live: "இன்றைய புதிய தகவல் • நேரலை RSS",
    home_news_heading: "தினசரி விவசாய செய்திகள் & வானிலை எச்சரிக்கைகள்",
    view_all_news: "அனைத்து விவசாய செய்திகளையும் காண்க →",
    news_live_badge: "நேரலை விவசாய தகவல் • தினமும் புதுப்பிக்கப்படுகிறது",
    news_main_title: "தினசரி கிருஷி சமாச்சார் & ஆலோசனைகள்",
    news_subtitle: "இந்திய விவசாயம், குறைந்தபட்ச ஆதரவு விலை (MSP), வானிலை முன்னறிவிப்பு மற்றும் அரசு மானியங்கள் குறித்த நேரடித் தகவல்கள்.",
    news_breaking_label: "முக்கிய தலைப்புச் செய்தி",
    news_search_ph: "தேடல் (எ.கா: MSP, மானியம், மழை, உரம், டிராக்டர்)..."
  },

  kn: {
    nav_home: "ಮುಖಪುಟ",
    nav_features: "ವೈಶಿಷ್ಟ್ಯಗಳು",
    nav_crop_rec: "ಬೆಳೆ ಶಿಫಾರಸು",
    nav_crop_guide: "ಬೆಳೆ ಮಾರ್ಗದರ್ಶಿ",
    nav_weather: "ಹವಾಮಾನ",
    nav_disease: "ರೋಗ ಪತ್ತೆ",
    nav_calc: "ಲಾಭ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
    nav_sustainability: "ಸುಸ್ಥಿರ ಕೃಷಿ",
    nav_krishi_seva: "ಕೃಷಿ ಸೇವೆ",
    nav_chat: "AI ಚಾಟ್",
    nav_about: "ನಮ್ಮ ಬಗ್ಗೆ",
    nav_contact: "ಸಂಪರ್ಕ",
    nav_account: "ಖಾತೆ",
    nav_profile: "ನನ್ನ ಪ್ರೊಫೈಲ್",
    nav_admin: "ನಿರ್ವಾಹಕ ಫಲಕ",
    nav_settings: "ಸೆಟ್ಟಿಂಗ್‌ಗಳು",
    nav_login: "ಲಾಗಿನ್",
    nav_signup: "ಸೈನ್ ಅಪ್",
    nav_logout: "ಲಾಗ್‌ಔಟ್",
    nav_language: "ಭಾಷೆ",

    hero_title: "ಕೃಷಿ ಮಿತ್ರಗೆ ಸುಸ್ವಾಗತ",
    hero_subtitle: "ನಿಮ್ಮ AI-ಚಾಲಿತ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ ಸಹಾಯಕ",
    hero_desc: "ನಿಖರ ಕೃಷಿ, ಸಂಪನ್ಮೂಲ ಉಳಿತಾಯ ಮತ್ತು ಸುಸ್ಥಿರ ಬೆಳವಣಿಗೆಗಾಗಿ ಆಧುನಿಕ AI ತಂತ್ರಜ್ಞಾನ.",
    cta_chat: "ಚಾಟ್ ಪ್ರಾರಂಭಿಸಿ",

    features_heading: "ನಮ್ಮ ಪ್ರಮುಖ ವೈಶಿಷ್ಟ್ಯಗಳು",
    feat_chat_title: "AI ಚಾಟ್ ಸಹಾಯಕ",
    feat_chat_desc: "ಕೃಷಿಗೆ ಸಂಬಂಧಿಸಿದ ಯಾವುದೇ ಪ್ರಶ್ನೆ ಕೇಳಿ. ಫೋಟೋ ಮತ್ತು ಪಠ್ಯ ಎರಡರಲ್ಲೂ ಸಲಹೆ.",
    feat_chat_btn: "ಚಾಟ್ ಮಾಡಿ",
    feat_weather_title: "ಹವಾಮಾನ ಆಧಾರಿತ ನಿರ್ಧಾರಗಳು",
    feat_weather_desc: "ಪ್ರಸ್ತುತ ಹವಾಮಾನಕ್ಕೆ ಅನುಗುಣವಾಗಿ ನೀರಾವರಿ ಮತ್ತು ಬೆಳೆ ರಕ್ಷಣೆಯ ಸಲಹೆಗಳು.",
    feat_weather_btn: "ಹವಾಮಾನ ನೋಡಿ",
    feat_disease_title: "ಬೆಳೆ ರೋಗ ಪತ್ತೆ",
    feat_disease_desc: "ಎಲೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ ರೋಗ ಪತ್ತೆ ಮತ್ತು ಪರಿಹಾರ ಪಡೆಯಿರಿ.",
    feat_disease_btn: "ರೋಗ ಪರೀಕ್ಷಿಸಿ",
    feat_calc_title: "ಲಾಭ ಮತ್ತು ಸಂಪನ್ಮೂಲ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
    feat_calc_desc: "ಭೂಮಿಯ ವಿಸ್ತೀರ್ಣಕ್ಕೆ ತಕ್ಕಂತೆ ಗೊಬ್ಬರ, ನೀರು ಮತ್ತು ನಿವ್ವಳ ಲಾಭದ ಲೆಕ್ಕಾಚಾರ.",
    feat_calc_btn: "ಲೆಕ್ಕ ಹಾಕಿ",
    feat_sust_title: "ಸುಸ್ಥಿರ ಕೃಷಿ ಸಲಹೆಗಳು",
    feat_sust_desc: "ಮಣ್ಣಿನ ಫಲವತ್ತತೆ ಹೆಚ್ಚಿಸಲು ಸಾವಯವ ಕೃಷಿ ಮತ್ತು ನೈಸರ್ಗಿಕ ವಿಧಾನಗಳು.",
    feat_sust_btn: "ಇನ್ನಷ್ಟು ತಿಳಿಯಿರಿ",
    feat_rag_title: "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು",
    feat_rag_desc: "ಪಿಎಂ-ಕಿಸಾನ್, ಬೆಳೆ ವಿಮೆ ಮತ್ತು ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ ವಿವರಗಳು.",
    feat_rag_btn: "ನೋಡಿ",

    crop_rec_title: "ಬೆಳೆ ಶಿಫಾರಸು ವ್ಯವಸ್ಥೆ",
    crop_rec_subtitle: "ಮಣ್ಣು ಮತ್ತು ಹವಾಮಾನಕ್ಕೆ ಸೂಕ್ತವಾದ ಅತ್ಯುತ್ತಮ ಬೆಳೆ ಸಲಹೆ",
    mode_autofill: "ಸ್ವಯಂ ಭರ್ತಿ (ರಾಜ್ಯ/ಜಿಲ್ಲೆ)",
    mode_manual: "ಹಸ್ತಚಾಲಿತ ನಮೂದು",
    select_state: "ರಾಜ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    select_district: "ಜಿಲ್ಲೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    btn_my_location: "ನನ್ನ ಸ್ಥಳ ಬಳಸಿ",
    btn_autofill: "ಸ್ವಯಂ ಭರ್ತಿ ಮೌಲ್ಯಗಳು",
    btn_predict: "ಸೂಕ್ತ ಬೆಳೆಗಳನ್ನು ಹುಡುಕಿ",

    disease_title: "ಬೆಳೆ ರೋಗ ಪತ್ತೆ",
    disease_subtitle: "ರೋಗ ಪತ್ತೆಗಾಗಿ ನಿಮ್ಮ ಬೆಳೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
    btn_analyze_disease: "ರೋಗ ವಿಶ್ಲೇಷಿಸಿ",

    weather_title: "ಹವಾಮಾನ ಸಲಹೆಗಾರ",
    weather_subtitle: "ನೈಜ ಸಮಯದ ಹವಾಮಾನ ಮತ್ತು ಬೆಳೆ ಸಂರಕ್ಷಣಾ ಸಲಹೆಗಳು",
    btn_check_weather: "ಹವಾಮಾನ ಮತ್ತು ಸಲಹೆ ಪಡೆಯಿರಿ",

    calc_title: "ಲಾಭ ಮತ್ತು ಸಂಪನ್ಮೂಲ ಕ್ಯಾಲ್ಕುಲೇಟರ್",
    calc_subtitle: "ಕೃಷಿ ವೆಚ್ಚ, ನಿರೀಕ್ಷಿತ ಇಳುವರಿ ಮತ್ತು ನಿವ್ವಳ ಲಾಭದ ಲೆಕ್ಕ",
    btn_calculate_profit: "ಲಾಭ ಲೆಕ್ಕ ಹಾಕಿ",

    sust_title: "ಸಾವಯವ ಕೃಷಿ ಸಲಹೆಗಳು",
    sust_subtitle: "ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಮತ್ತು ನೈಸರ್ಗಿಕ ಕೃಷಿ ಪದ್ಧತಿಗಳು",

    krishi_title: "ಕೃಷಿ ಸೇವಾ ಕೇಂದ್ರ",
    krishi_subtitle: "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಮತ್ತು ಮಣ್ಣು ಪರೀಕ್ಷಾ ಪ್ರಯೋಗಾಲಯಗಳು",

    settings_lang_title: "ಡೀಫಾಲ್ಟ್ ಭಾಷಾ ಸೆಟ್ಟಿಂಗ್",
    settings_lang_desc: "ನಿಮ್ಮ ಪ್ರಾದೇಶಿಕ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ. ಇದನ್ನು ನಿಮ್ಮ ಡೀಫಾಲ್ಟ್ ಭಾಷೆಯಾಗಿ ಉಳಿಸಲಾಗುತ್ತದೆ.",
    btn_save_lang: "ಡೀಫಾಲ್ಟ್ ಭಾಷೆಯಾಗಿ ಉಳಿಸಿ",
    lang_modal_title: "ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ",
    lang_modal_subtitle: "ಕೃಷಿ ಮಿತ್ರವನ್ನು ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಬಳಸಲು ಆಯ್ಕೆಮಾಡಿ:",

    nav_news: "ದೈನಂದಿನ ಕೃಷಿ ಸುದ್ದಿಗಳು & ಮುನ್ಸೂಚನೆಗಳು",
    nav_news_direct: "ಕೃಷಿ ಸುದ್ದಿ",
    ad_flair: "ರೈತ ಮಾರುಕಟ್ಟೆ ಮತ್ತು ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿಗಳು",
    ad_carousel_title: "ಕೃಷಿ ವಿಶೇಷ ಆಫರ್‌ಗಳು ಮತ್ತು ಪರಿಶೀಲಿಸಿದ ಯೋಜನೆಗಳು",
    home_news_live: "ಇಂದಿನ ತಾಜಾ ಅಪ್‌ಡೇಟ್ • ಲೈವ್ RSS",
    home_news_heading: "ದೈನಂದಿನ ಕೃಷಿ ಸಮಾಚಾರ & ಹವಾಮಾನ ಎಚ್ಚರಿಕೆಗಳು",
    view_all_news: "ಎಲ್ಲಾ ಕೃಷಿ ಸುದ್ದಿಗಳನ್ನು ವೀಕ್ಷಿಸಿ →",
    news_live_badge: "ಲೈವ್ ಕೃಷಿ ಫೀಡ್ • ಪ್ರತಿದಿನ ನವೀಕರಿಸಲಾಗುತ್ತದೆ",
    news_main_title: "ದೈನಂದಿನ ಕೃಷಿ ಸಮಾಚಾರ & ಸಲಹೆಗಳು",
    news_subtitle: "ಭಾರತೀಯ ಕೃಷಿ, ಬೆಂಬಲ ಬೆಲೆ (MSP), ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ ಮತ್ತು ಸರ್ಕಾರಿ ಸಬ್ಸಿಡಿಗಳ ಕುರಿತು ನೈಜ-ಸಮಯದ ವಿವರಗಳು.",
    news_breaking_label: "ತಾಜಾ ಮುಖ್ಯಾಂಶ",
    news_search_ph: "ವಿಷಯ ಹುಡುಕಿ (ಉದಾ: MSP, ಸಬ್ಸಿಡಿ, ಮಳೆ, ಗೊಬ್ಬರ, ಟ್ರ್ಯಾಕ್ಟರ್)..."
  },

  ml: {
    nav_home: "ഹോം",
    nav_features: "സവിശേഷതകൾ",
    nav_crop_rec: "വിള ശുപാർശ",
    nav_crop_guide: "വിള ഗൈഡ്",
    nav_weather: "കാലാവസ്ഥ",
    nav_disease: "രോഗ നിർണയം",
    nav_calc: "ലാഭ കാൽക്കുലേറ്റർ",
    nav_sustainability: "സുസ്ഥിര കൃഷി",
    nav_krishi_seva: "കൃഷി സേവ",
    nav_chat: "AI ചാറ്റ്",
    nav_about: "ഞങ്ങളെ കുറിച്ച്",
    nav_contact: "ബന്ധപ്പെടുക",
    nav_account: "അക്കൗണ്ട്",
    nav_profile: "പ്രൊഫൈൽ",
    nav_admin: "അഡ്മിൻ പാനൽ",
    nav_settings: "ക്രമീകരണങ്ങൾ",
    nav_login: "ലോഗിൻ",
    nav_signup: "സൈൻ അപ്പ്",
    nav_logout: "ലോഗൗട്ട്",
    nav_language: "ഭാഷ",

    hero_title: "കൃഷി മിത്രയിലേക്ക് സ്വാഗതം",
    hero_subtitle: "നിങ്ങളുടെ AI സ്മാർട്ട് കൃഷി സഹായി",
    hero_desc: "കൃത്യതയാർന്ന കൃഷിരീതികൾക്കും മികച്ച വിളവിനും നൂതന AI സാങ്കേതികവിദ്യ.",
    cta_chat: "ചാറ്റ് തുടങ്ങൂ",

    features_heading: "പ്രധാന സവിശേഷതകൾ",
    feat_chat_title: "AI ചാറ്റ് അസിസ്റ്റന്റ്",
    feat_chat_desc: "കൃഷിയുമായി ബന്ധപ്പെട്ട ഏത് സംശയങ്ങൾക്കും ചിത്രങ്ങളിലൂടെയും എഴുത്തിലൂടെയും മറുപടി.",
    feat_chat_btn: "ചാറ്റ് ചെയ്യുക",
    feat_weather_title: "കാലാവസ്ഥാധിഷ്ഠിത കൃഷി",
    feat_weather_desc: "നിലവിലെ കാലാവസ്ഥയ്ക്ക് അനുയോജ്യമായ നനയ്ക്കലും പരിചരണ നിർദ്ദേശങ്ങളും.",
    feat_weather_btn: "കാലാവസ്ഥ കാണുക",
    feat_disease_title: "വിള രോഗനിർണയം",
    feat_disease_desc: "ഇലകളുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്ത് രോഗവും പ്രതിവിധികളും തത്സമയം അറിയാം.",
    feat_disease_btn: "രോഗം പരിശോധിക്കുക",
    feat_calc_title: "ലാഭ കാൽക്കുലേറ്റർ",
    feat_calc_desc: "കൃഷിസ്ഥലത്തിന് ആവശ്യമായ വളവും വെള്ളവും ചെലവും പ്രതീക്ഷിക്കുന്ന ലാഭവും കണക്കാക്കൂ.",
    feat_calc_btn: "കണക്കുകൂട്ടുക",
    feat_sust_title: "സുസ്ഥിര ജൈവകൃഷി",
    feat_sust_desc: "മണ്ണിന്റെ ഫലഭൂയിഷ്ഠത നിലനിർത്താൻ പ്രകൃതിദത്ത കൃഷിരീതികൾ.",
    feat_sust_btn: "കൂടുതലറിയാൻ",
    feat_rag_title: "സർക്കാർ പദ്ധതികൾ",
    feat_rag_desc: "പിഎം-കിസാൻ, വിള ഇൻഷുറൻസ് എന്നിവയെക്കുറിച്ചുള്ള ആധികാരിക വിവരങ്ങൾ.",
    feat_rag_btn: "കാണുക",

    crop_rec_title: "വിള ശുപാർശ സംവിധാനം",
    crop_rec_subtitle: "മണ്ണിന്റെ ഗുണനിലവാരവും കാലാവസ്ഥയും അനുസരിച്ച് അനുയോജ്യമായ വിള കണ്ടെത്താം",
    mode_autofill: "ഓട്ടോ-ഫിൽ (സംസ്ഥാനം/ജില്ല)",
    mode_manual: "സ്വയം നൽകുക",
    select_state: "സംസ്ഥാനം തിരഞ്ഞെടുക്കുക",
    select_district: "ജില്ല തിരഞ്ഞെടുക്കുക",
    btn_my_location: "എന്റെ ലൊക്കേഷൻ ഉപയോഗിക്കുക",
    btn_autofill: "ഓട്ടോ-ഫിൽ മൂല്യങ്ങൾ",
    btn_predict: "യോജിച്ച വിളകൾ കണ്ടെത്തുക",

    disease_title: "വിള രോഗനിർണയം",
    disease_subtitle: "രോഗനിർണയത്തിനായി ചെടിയുടെ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക",
    btn_analyze_disease: "രോഗം പരിശോധിക്കുക",

    weather_title: "കാലാവസ്ഥാ ഉപദേശം",
    weather_subtitle: "തത്സമയ കാലാവസ്ഥയും വിള സംരക്ഷണ നിർദ്ദേശങ്ങളും",
    btn_check_weather: "കാലാവസ്ഥ പരിശോധിക്കുക",

    calc_title: "ലാഭ കാൽക്കുലേറ്റർ",
    calc_subtitle: "ഉൽപ്പാദനച്ചെലവും പ്രതീക്ഷിക്കുന്ന വരുമാനവും ലാഭവും",
    btn_calculate_profit: "ലാഭം കണക്കാക്കുക",

    sust_title: "സുസ്ഥിര കൃഷി രീതികൾ",
    sust_subtitle: "ജൈവകൃഷിയും പരിസ്ഥിതി സംരക്ഷണവും",

    krishi_title: "കൃഷി സേവാ കേന്ദ്രം",
    krishi_subtitle: "സർക്കാർ പദ്ധതികളും മണ്ണ് പരിശോധനാ ലാബുകളും",

    settings_lang_title: "സ്ഥിര ഭാഷാ ക്രമീകരണം",
    settings_lang_desc: "നിങ്ങളുടെ പ്രിയപ്പെട്ട ഭാഷ തിരഞ്ഞെടുക്കുക. ഇത് നിങ്ങളുടെ ഡിഫോൾട്ട് ഭാഷയായി സൂക്ഷിക്കും.",
    btn_save_lang: "സ്ഥിര ഭാഷയായി സംരക്ഷിക്കുക",
    lang_modal_title: "ഭാഷ തിരഞ്ഞെടുക്കുക",
    lang_modal_subtitle: "കൃഷി മിത്ര നിങ്ങളുടെ സ്വന്തം ഭാഷയിൽ ഉപയോഗിക്കാൻ തിരഞ്ഞെടുക്കൂ:",

    nav_news: "പ്രതിദിന കൃഷി വാർത്തകളും ജാഗ്രതാനിർദ്ദേശങ്ങളും",
    nav_news_direct: "കൃഷി വാർത്തകൾ",
    ad_flair: "കർഷക വിപണിയും സർക്കാർ സബ്‌സിഡികളും",
    ad_carousel_title: "കാർഷിക പ്രത്യേക ഓഫറുകളും അംഗീകൃത പദ്ധതികളും",
    home_news_live: "ഇന്നത്തെ പുതിയ അപ്‌ഡേറ്റ് • ലൈവ് RSS",
    home_news_heading: "പ്രതിദിന കൃഷി സമാചാരവും കാലാവസ്ഥാ മുന്നറിയിപ്പുകളും",
    view_all_news: "എല്ലാ കാർഷിക വാർത്തകളും കാണുക →",
    news_live_badge: "തത്സമയ കാർഷിക ഫീഡ് • ദിവസവും അപ്‌ഡേറ്റ് ചെയ്യുന്നത്",
    news_main_title: "പ്രതിദിന കൃഷി സമാചാരവും നിർദ്ദേശങ്ങളും",
    news_subtitle: "ഇന്ത്യൻ കാർഷിക മേഖല, താങ്ങുവില (MSP), കാലാവസ്ഥാ പ്രവചനം, സർക്കാർ സബ്‌സിഡികൾ എന്നിവയുടെ ഏറ്റവും പുതിയ വിവരങ്ങൾ.",
    news_breaking_label: "പ്രധാന വാർത്ത",
    news_search_ph: "വിഷയം തിരയുക (ഉദാ: താങ്ങുവില, സബ്‌സിഡി, മഴ, വളം, ഡ്രോൺ)..."
  }
};

/**
 * Get current language code from cookie / localStorage / default
 */
function getCurrentLanguage() {
  const stored = localStorage.getItem("krishi_language");
  if (stored && KRISHI_TRANSLATIONS[stored]) return stored;

  const cookieMatch = document.cookie.match(/krishi_lang=([a-z]{2})/);
  if (cookieMatch && KRISHI_TRANSLATIONS[cookieMatch[1]]) return cookieMatch[1];

  return "en";
}

/**
 * Apply selected language translations to the entire DOM
 */
function applyLanguage(langCode) {
  if (!KRISHI_TRANSLATIONS[langCode]) {
    langCode = "en";
  }

  const dict = KRISHI_TRANSLATIONS[langCode];
  const langMeta = INDIAN_LANGUAGES[langCode];

  // Save in storage & cookie
  localStorage.setItem("krishi_language", langCode);
  document.cookie = `krishi_lang=${langCode}; path=/; max-age=2592000; SameSite=Lax`;
  document.documentElement.lang = langCode;

  // Update navbar label
  const labelEl = document.getElementById("currentLangLabel");
  if (labelEl && langMeta) {
    labelEl.textContent = `${langMeta.nativeName}`;
  }

  // Update elements with data-i18n
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    if (dict[key]) {
      if (el.tagName === "INPUT" || el.tagName === "TEXTAREA") {
        el.placeholder = dict[key];
      } else {
        // Preserve icon if present
        const icon = el.querySelector("i");
        if (icon) {
          const iconHTML = icon.outerHTML;
          el.innerHTML = iconHTML + " " + dict[key];
        } else {
          el.textContent = dict[key];
        }
      }
    }
  });

  // Update elements with data-i18n-placeholder
  document.querySelectorAll("[data-i18n-placeholder]").forEach((el) => {
    const key = el.getAttribute("data-i18n-placeholder");
    if (dict[key]) {
      el.placeholder = dict[key];
    }
  });

  // Sync any active language select boxes
  document.querySelectorAll(".krishi-lang-select").forEach((sel) => {
    sel.value = langCode;
  });

  // Update active state in dropdown
  document.querySelectorAll(".lang-opt").forEach((opt) => {
    if (opt.getAttribute("data-lang") === langCode) {
      opt.classList.add("active");
    } else {
      opt.classList.remove("active");
    }
  });

  // Notify backend if logged in
  try {
    fetch("/api/set-language", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ language: langCode })
    }).catch(() => {});
  } catch (e) {}

  // Dispatch custom event for page scripts (chat, weather, etc.)
  window.dispatchEvent(new CustomEvent("krishiLanguageChanged", { detail: { language: langCode } }));
}

// Auto-run on DOM ready
document.addEventListener("DOMContentLoaded", function () {
  const activeLang = getCurrentLanguage();
  applyLanguage(activeLang);

  // Attach navbar language dropdown handlers
  document.querySelectorAll(".lang-opt").forEach((opt) => {
    opt.addEventListener("click", function (e) {
      e.preventDefault();
      const code = this.getAttribute("data-lang");
      if (code) {
        applyLanguage(code);
        // Close dropdown
        const dropdown = this.closest(".dropdown");
        if (dropdown) dropdown.classList.remove("active");
      }
    });
  });
});
