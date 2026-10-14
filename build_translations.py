# -*- coding: utf-8 -*-
"""
Generator for Krishi Mitra translations.js
Generates comprehensive multi-lingual translations for 10 Indian regional languages:
English (en), Hindi (hi), Punjabi (pa), Bengali (bn), Marathi (mr),
Gujarati (gu), Telugu (te), Tamil (ta), Kannada (kn), Malayalam (ml).
Covers all 42 crops, Mandi Bhav keys, navigation, and interactive helpers.
"""

import json

# 1. Indian Languages Metadata
INDIAN_LANGUAGES = {
    "en": {
        "code": "en",
        "name": "English",
        "nativeName": "English",
        "region": "Pan-India / Universal",
        "badge": "Universal"
    },
    "hi": {
        "code": "hi",
        "name": "Hindi",
        "nativeName": "हिन्दी",
        "region": "उत्तर एवं मध्य भारत (UP, MP, बिहार, राजस्थान, दिल्ली, हरियाणा)",
        "badge": "North & Central"
    },
    "pa": {
        "code": "pa",
        "name": "Punjabi",
        "nativeName": "ਪੰਜਾਬੀ",
        "region": "ਉੱਤਰੀ ਭਾਰਤ (ਪੰਜਾਬ, ਹਰਿਆਣਾ, ਚੰਡੀਗੜ੍ਹ)",
        "badge": "Punjab"
    },
    "bn": {
        "code": "bn",
        "name": "Bengali",
        "nativeName": "বাংলা",
        "region": "পূর্ব ভারত (পশ্চিমবঙ্গ, ত্রিপুরা, আসাম)",
        "badge": "East India"
    },
    "mr": {
        "code": "mr",
        "name": "Marathi",
        "nativeName": "मराठी",
        "region": "पश्चिम भारत (महाराष्ट्र, गोवा)",
        "badge": "Maharashtra"
    },
    "gu": {
        "code": "gu",
        "name": "Gujarati",
        "nativeName": "ગુજરાતી",
        "region": "પશ્ચિમ ભારત (ગુજરાત)",
        "badge": "Gujarat"
    },
    "te": {
        "code": "te",
        "name": "Telugu",
        "nativeName": "తెలుగు",
        "region": "దక్షిణ భారతదేశం (ఆంధ్రప్రదేశ్, తెలంగాణ)",
        "badge": "Andhra & Telangana"
    },
    "ta": {
        "code": "ta",
        "name": "Tamil",
        "nativeName": "தமிழ்",
        "region": "தென்னிந்தியா (தமிழ்நாடு, புதுச்சேரி)",
        "badge": "Tamil Nadu"
    },
    "kn": {
        "code": "kn",
        "name": "Kannada",
        "nativeName": "ಕನ್ನಡ",
        "region": "ದಕ್ಷಿಣ ಭಾರತ (ಕರ್ನಾಟಕ)",
        "badge": "Karnataka"
    },
    "ml": {
        "code": "ml",
        "name": "Malayalam",
        "nativeName": "മലയാളം",
        "region": "ദക്ഷിണേന്ത്യ (കേരളം, ലക്ഷദ്വീപ്)",
        "badge": "Kerala"
    }
}

# 2. Master Crop Translations Dictionary (42+ Indian Crops across all 10 languages)
CROP_TRANSLATIONS = {
    "wheat": {
        "en": "Wheat", "hi": "गेहूँ", "pa": "ਕਣਕ", "bn": "গম", "mr": "गहू",
        "gu": "ઘઉં", "te": "గోధుమలు", "ta": "கோதுமை", "kn": "ಗೋಧಿ", "ml": "ഗോതമ്പ്"
    },
    "rice": {
        "en": "Rice / Paddy", "hi": "धान / चावल", "pa": "ਝੋਨਾ / ਚੌਲ", "bn": "ধান / চাল", "mr": "भात / तांदूळ",
        "gu": "ડાંગર / ચોખા", "te": "వరి / బియ్యం", "ta": "நெல் / அரிசி", "kn": "ಭತ್ತ / ಅಕ್ಕಿ", "ml": "നെല്ല് / അരി"
    },
    "paddy": {
        "en": "Paddy", "hi": "धान", "pa": "ਝੋਨਾ", "bn": "ধান", "mr": "भात",
        "gu": "ડાંગર", "te": "వరి", "ta": "நெல்", "kn": "ಭತ್ತ", "ml": "നെല്ല്"
    },
    "paddy_basmati": {
        "en": "Paddy (Basmati)", "hi": "धान (बासमती)", "pa": "ਝੋਨਾ (ਬਾਸਮਤੀ)", "bn": "ধান (বাসমতী)", "mr": "भात (बासमती)",
        "gu": "ડાંગર (બાસમતી)", "te": "వరి (బాస్మతి)", "ta": "நெல் (பாஸ்மதி)", "kn": "ಭತ್ತ (ಬಾಸ್ಮತಿ)", "ml": "നെല്ല് (ബസ്മതി)"
    },
    "paddy_common": {
        "en": "Paddy (Common)", "hi": "धान (सामान्य)", "pa": "ਝੋਨਾ (ਆਮ)", "bn": "ধান (সাধারণ)", "mr": "भात (सर्वसाधारण)",
        "gu": "ડાંગર (સામાન્ય)", "te": "వరి (సాధారణ)", "ta": "நெல் (சாதாரண)", "kn": "ಭತ್ತ (ಸಾಮಾನ್ಯ)", "ml": "നെല്ല് (സാധാരണ)"
    },
    "cotton": {
        "en": "Cotton", "hi": "कपास", "pa": "ਕਪਾਹ", "bn": "তুলা", "mr": "कापूस",
        "gu": "કપાસ", "te": "ప్రత్తి", "ta": "பருத்தி", "kn": "ಹತ್ತಿ", "ml": "പരുത്തി"
    },
    "mustard": {
        "en": "Mustard", "hi": "सरसों", "pa": "ਸਰ੍ਹੋਂ / ਰਾਈ", "bn": "সরিষা", "mr": "मोहरी",
        "gu": "રાય / સરસવ", "te": "ఆవాలు", "ta": "கடுகு", "kn": "ಸಾಸಿವೆ", "ml": "കടുക്"
    },
    "soybean": {
        "en": "Soybean", "hi": "सोयाबीन", "pa": "ਸੋਇਆਬੀਨ", "bn": "সয়াবিন", "mr": "सोयाबीन",
        "gu": "સોયાબીન", "te": "సోయాబీన్", "ta": "சோயாபீன்", "kn": "ಸೋಯಾಬೀನ್", "ml": "സോയാബീൻ"
    },
    "chickpea": {
        "en": "Gram (Chana)", "hi": "चना", "pa": "ਛੋਲੇ (ਚਣਾ)", "bn": "ছোলা", "mr": "हरभरा (चणा)",
        "gu": "ચણા", "te": "శనగలు", "ta": "கொண்டைக்கடலை", "kn": "ಕಡಲೆ", "ml": "കടല"
    },
    "gram": {
        "en": "Gram", "hi": "चना", "pa": "ਚਣਾ", "bn": "ছোলা", "mr": "चणा",
        "gu": "ચણા", "te": "శనగలు", "ta": "கொண்டைக்கடலை", "kn": "ಕಡಲೆ", "ml": "കടല"
    },
    "pigeonpeas": {
        "en": "Pigeonpeas (Arhar/Tur)", "hi": "अरहर / तुअर", "pa": "ਅਰਹਰ (ਤੂਰ)", "bn": "অড়হর ডাল", "mr": "तूर",
        "gu": "તુવેર", "te": "కందులు", "ta": "துவரம்பருப்பு", "kn": "ತೊಗರಿ", "ml": "തുവരപ്പരിപ്പ്"
    },
    "sugarcane": {
        "en": "Sugarcane", "hi": "गन्ना", "pa": "ਕਮਾਦ (ਗੰਨਾ)", "bn": "আখ", "mr": "ऊस",
        "gu": "શેરડી", "te": "చెరకు", "ta": "கரும்பு", "kn": "ಕಬ್ಬು", "ml": "കരിമ്പ്"
    },
    "maize": {
        "en": "Maize", "hi": "मक्का", "pa": "ਮੱਕੀ", "bn": "ভুট্টা", "mr": "मका",
        "gu": "મકાઈ", "te": "మొక్కజొన్న", "ta": "மக்காச்சோளம்", "kn": "ಮೆಕ್ಕೆಜೋಳ", "ml": "ചോളം"
    },
    "groundnut": {
        "en": "Groundnut", "hi": "मूंगफली", "pa": "ਮੂੰਗਫਲੀ", "bn": "চীনাবাদাম", "mr": "भुईमूग",
        "gu": "મગફળી", "te": "వేరుశనగ", "ta": "வேர்க்கடலை", "kn": "ಕಡಲೆಕಾಯಿ", "ml": "നിലക്കടല"
    },
    "potato": {
        "en": "Potato", "hi": "आलू", "pa": "ਆਲੂ", "bn": "আলু", "mr": "बटाटा",
        "gu": "બટાકા", "te": "బంగాళాదుంప", "ta": "உருளைக்கிழங்கு", "kn": "ಆಲೂಗಡ್ಡೆ", "ml": "ഉരുളക്കിഴങ്ങ്"
    },
    "onion": {
        "en": "Onion", "hi": "प्याज", "pa": "ਪਿਆਜ਼", "bn": "পেঁয়াজ", "mr": "कांदा",
        "gu": "ડુંગળી", "te": "ఉల్లిపాయ", "ta": "வெங்காயம்", "kn": "ಈರುಳ್ಳಿ", "ml": "സവാള / ഉള്ളി"
    },
    "tomato": {
        "en": "Tomato", "hi": "टमाटर", "pa": "ਟਮਾਟਰ", "bn": "টমেটো", "mr": "टोमॅटो",
        "gu": "ટામેટા", "te": "టమోటా", "ta": "தக்காளி", "kn": "ಟೊಮೆಟೊ", "ml": "തക്കാളി"
    },
    "garlic": {
        "en": "Garlic", "hi": "लहसुन", "pa": "ਲਸਣ", "bn": "রসুন", "mr": "लसूण",
        "gu": "લસણ", "te": "వెల్లుల్లి", "ta": "பூண்டு", "kn": "ಬೆಳ್ಳುಳ್ಳಿ", "ml": "വെളുത്തുള്ളി"
    },
    "ginger": {
        "en": "Ginger", "hi": "अदरक", "pa": "ਅਦਰਕ", "bn": "আদা", "mr": "आले",
        "gu": "આદુ", "te": "అల్లం", "ta": "இஞ்சி", "kn": "ಶುಂಠಿ", "ml": "ഇഞ്ചി"
    },
    "turmeric": {
        "en": "Turmeric", "hi": "हल्दी", "pa": "ਹਲਦੀ", "bn": "হলুদ", "mr": "हळद",
        "gu": "હળદર", "te": "పసుపు", "ta": "மஞ்சள்", "kn": "ಅರಿಶಿನ", "ml": "മഞ്ഞൾ"
    },
    "chilli": {
        "en": "Chilli", "hi": "मिर्च", "pa": "ਮਿਰਚ", "bn": "লঙ্কা", "mr": "मिरची",
        "gu": "મરચાં", "te": "మిరపకాయ", "ta": "மிளகாய்", "kn": "ಮೆಣಸಿನಕಾಯಿ", "ml": "മുളക്"
    },
    "bajra": {
        "en": "Bajra", "hi": "बाजरा", "pa": "ਬਾਜਰਾ", "bn": "বাজরা", "mr": "बाजरी",
        "gu": "બાજરી", "te": "సజ్జలు", "ta": "கம்பு", "kn": "ಸಜ್ಜೆ", "ml": "കമ്പം"
    },
    "jowar": {
        "en": "Jowar", "hi": "ज्वार", "pa": "ਜਵਾਰ", "bn": "জোয়ার", "mr": "ज्वारी",
        "gu": "જુવાર", "te": "జొన్నలు", "ta": "சோளம்", "kn": "ಜೋಳ", "ml": "ചോളം"
    },
    "ragi": {
        "en": "Ragi", "hi": "रागी (मडुआ)", "pa": "ਰਾਗੀ", "bn": "রাগি", "mr": "नाचणी / रागी",
        "gu": "રાગી / નાગલી", "te": "రాగులు", "ta": "கேழ்வரகு", "kn": "ರಾಗಿ", "ml": "റാഗി / കൂവരക്"
    },
    "barley": {
        "en": "Barley", "hi": "जौ", "pa": "ਜੌਂ", "bn": "যব", "mr": "जवस / सातू",
        "gu": "જવ", "te": "బార్లీ", "ta": "பார்லி", "kn": "ಬಾರ್ಲಿ", "ml": "ബാർലി"
    },
    "mungbean": {
        "en": "Moong (Green Gram)", "hi": "मूंग", "pa": "ਮੂੰਗੀ", "bn": "মুগ ডাল", "mr": "मूग",
        "gu": "મગ", "te": "పెసలు", "ta": "பாசிப்பயறு", "kn": "ಹೆಸರುಕಾಳು", "ml": "ചെറുപയർ"
    },
    "blackgram": {
        "en": "Urad (Black Gram)", "hi": "उड़द", "pa": "ਮਾਂਹ (ਉੜਦ)", "bn": "মাষকলাই", "mr": "उडीद",
        "gu": "અડદ", "te": "మినుములు", "ta": "உளுந்து", "kn": "ಉದ್ದಿನಕಾಳು", "ml": "ഉഴുന്ന്"
    },
    "lentil": {
        "en": "Lentil (Masoor)", "hi": "मसूर", "pa": "ਮਸਰ", "bn": "মসুর ডাল", "mr": "मसूर",
        "gu": "મસૂર", "te": "మైసూర్ పప్పు", "ta": "மைசூர் பருப்பு", "kn": "ಮಸೂರ ಬೇಳೆ", "ml": "മസൂർ പരിപ്പ്"
    },
    "kidneybeans": {
        "en": "Kidney Beans (Rajma)", "hi": "राजमा", "pa": "ਰਾਜਮਾਂਹ", "bn": "রাজমা", "mr": "राजमा",
        "gu": "રાજમા", "te": "రాజ్మా", "ta": "ராஜ்மா", "kn": "ರಾಜ್ಮಾ", "ml": "രാജ്മ"
    },
    "mothbeans": {
        "en": "Moth Beans", "hi": "मोठ", "pa": "ਮੋਠ", "bn": "মথ কলাই", "mr": "मठ",
        "gu": "મઠ", "te": "బొబ్బర్లు", "ta": "தட்டப்பயறு", "kn": "ಮಡಿಕೆ ಕಾಳು", "ml": "വൻപയർ"
    },
    "sunflower": {
        "en": "Sunflower", "hi": "सूरजमुखी", "pa": "ਸੂਰਜਮੁਖੀ", "bn": "সূর্যমুখী", "mr": "सूर्यफूल",
        "gu": "સૂર્યમુખી", "te": "పొద్దుతిరుగుడు", "ta": "சூரியகாந்தி", "kn": "ಸೂರ್ಯಕಾಂತಿ", "ml": "സൂര്യകാന്തി"
    },
    "tea": {
        "en": "Tea", "hi": "चाय", "pa": "ਚਾਹ", "bn": "চা", "mr": "चहा",
        "gu": "ચા", "te": "టీ", "ta": "தேயிலை", "kn": "ಟೀ / ಚಹಾ", "ml": "ചായ"
    },
    "coffee": {
        "en": "Coffee", "hi": "कॉफी", "pa": "ਕੌਫੀ", "bn": "কফি", "mr": "कॉफी",
        "gu": "કોફી", "te": "కాఫీ", "ta": "காபி", "kn": "ಕಾಫಿ", "ml": "കാപ്പി"
    },
    "jute": {
        "en": "Jute", "hi": "जूट / पटसन", "pa": "ਪਟਸਨ", "bn": "পাট", "mr": "ताग",
        "gu": "શણ", "te": "జనపనార", "ta": "சணல்", "kn": "ಸೆಣಬು", "ml": "ചണം"
    },
    "rubber": {
        "en": "Rubber", "hi": "रबर", "pa": "ਰਬੜ", "bn": "রবার", "mr": "रबर",
        "gu": "રબર", "te": "రబ్బరు", "ta": "ரப்பர்", "kn": "ರಬ್ಬರ್", "ml": "റബ്ബർ"
    },
    "cardamom": {
        "en": "Cardamom", "hi": "इलायची", "pa": "ਇਲਾਇਚੀ", "bn": "এলাচ", "mr": "वेलची",
        "gu": "ઈલાયચી", "te": "ఏలకులు", "ta": "ஏலக்காய்", "kn": "ಏಲಕ್ಕಿ", "ml": "ഏലയ്ക്ക"
    },
    "coconut": {
        "en": "Coconut", "hi": "नारियल", "pa": "ਨਾਰੀਅਲ", "bn": "নারকেল", "mr": "नारळ",
        "gu": "નાળિયેર", "te": "కొబ్బరికాయ", "ta": "தேங்காய்", "kn": "ತೆಂಗಿನಕಾಯಿ", "ml": "തേങ്ങ"
    },
    "mango": {
        "en": "Mango", "hi": "आम", "pa": "ਅੰਬ", "bn": "আম", "mr": "आंबा",
        "gu": "કેરી", "te": "మామిడికాయ", "ta": "மாம்பழம்", "kn": "ಮಾವಿನಹಣ್ಣು", "ml": "മാങ്ങ"
    },
    "banana": {
        "en": "Banana", "hi": "केला", "pa": "ਕੇਲਾ", "bn": "কলা", "mr": "केळी",
        "gu": "કેળાં", "te": "అరటిపండు", "ta": "வாழைப்பழம்", "kn": "ಬಾಳೆಹಣ್ಣು", "ml": "വാഴപ്പഴം"
    },
    "grapes": {
        "en": "Grapes", "hi": "अंगूर", "pa": "ਅੰਗੂਰ", "bn": "আঙুর", "mr": "द्राक्षे",
        "gu": "દ્રાક્ષ", "te": "ద్రాక్ష", "ta": "திராட்சை", "kn": "ದ್ರಾಕ್ಷಿ", "ml": "മുന്തിരി"
    },
    "apple": {
        "en": "Apple", "hi": "सेब", "pa": "ਸੇਬ", "bn": "আপেল", "mr": "सफरचंद",
        "gu": "સફરજન", "te": "యాపిల్", "ta": "ஆப்பிள்", "kn": "ಸೇಬು", "ml": "ആപ്പിൾ"
    },
    "orange": {
        "en": "Orange", "hi": "संतरा", "pa": "ਸੰਤਰਾ", "bn": "কমলালেবু", "mr": "संत्रे",
        "gu": "સંતરા", "te": "నారింజ", "ta": "ஆரஞ்சு", "kn": "ಕಿತ್ತಳೆ", "ml": "ഓറഞ്ച്"
    },
    "papaya": {
        "en": "Papaya", "hi": "पपीता", "pa": "ਪਪੀਤਾ", "bn": "পেঁপে", "mr": "पपई",
        "gu": "પપૈયું", "te": "బొప్పాయి", "ta": "பப்பாளி", "kn": "ಪರಂಗಿಹಣ್ಣು", "ml": "പപ്പായ"
    },
    "pomegranate": {
        "en": "Pomegranate", "hi": "अनार", "pa": "ਅਨਾਰ", "bn": "ডালিম / বেদানা", "mr": "डाळिंब",
        "gu": "દાડમ", "te": "దానిమ్మ", "ta": "மாதுளை", "kn": "ದಾಳಿಂಬೆ", "ml": "മാതളനാരങ്ങ"
    },
    "watermelon": {
        "en": "Watermelon", "hi": "तरबूज", "pa": "ਤਰਬੂਜ਼", "bn": "তরমুজ", "mr": "कलिंगड",
        "gu": "તરબૂચ", "te": "పుచ్చకాయ", "ta": "தர்பூசணி", "kn": "ಕಲ್ಲಂಗಡಿ", "ml": "തണ്ണിമത്തൻ"
    },
    "muskmelon": {
        "en": "Muskmelon", "hi": "खरबूजा", "pa": "ਖ਼ਰਬੂਜ਼ਾ", "bn": "ফুটি / খরমুজ", "mr": "खरबूज",
        "gu": "ટેટી / શક્કરટેટી", "te": "కర్బూజ", "ta": "முலாம் பழம்", "kn": "ಕರ್ಬೂಜ", "ml": "തണ്ണിമത്തൻ (മധുര)"
    },
    "vegetables": {
        "en": "Vegetables", "hi": "सब्जियां", "pa": "ਸਬਜ਼ੀਆਂ", "bn": "শাকসবজি", "mr": "भाज्या",
        "gu": "શાકભાજી", "te": "కూరగాయలు", "ta": "காய்கறிகள்", "kn": "ತರಕಾರಿಗಳು", "ml": "പച്ചക്കറികൾ"
    },
    "fruits": {
        "en": "Fruits", "hi": "फल", "pa": "ਫਲ", "bn": "ফলমূল", "mr": "फळे",
        "gu": "ફળો", "te": "పండ్లు", "ta": "பழங்கள்", "kn": "ಹಣ್ಣುಗಳು", "ml": "പഴങ്ങൾ"
    },
    "pulses": {
        "en": "Pulses", "hi": "दालें", "pa": "ਦਾਲਾਂ", "bn": "ডাল", "mr": "डाळी",
        "gu": "કઠોળ / દાળ", "te": "పప్పుధాన్యాలు", "ta": "பருப்பு வகைகள்", "kn": "ಬೇಳೆಕಾಳುಗಳು", "ml": "പയർവർഗ്ഗങ്ങൾ"
    },
    "general": {
        "en": "General Farming", "hi": "सामान्य खेती", "pa": "ਆਮ ਖੇਤੀ", "bn": "সাধারণ চাষাবাদ", "mr": "सामान्य शेती",
        "gu": "સામાન્ય ખેતી", "te": "సాధారణ వ్యవసాయం", "ta": "பொது விவசாயம்", "kn": "ಸಾಮಾನ್ಯ ಕೃಷಿ", "ml": "പൊതു കൃഷി"
    }
}

# 3. Commodity Category Translations
CATEGORY_TRANSLATIONS = {
    "cereal": {
        "en": "Cereal", "hi": "अनाज", "pa": "ਅਨਾਜ", "bn": "খাদ্যশস্য", "mr": "धान्य",
        "gu": "અનાજ", "te": "ధాన్యాలు", "ta": "தானியம்", "kn": "ಧಾನ್ಯ", "ml": "ധാന്യം"
    },
    "commercial": {
        "en": "Commercial", "hi": "व्यावसायिक", "pa": "ਵਪਾਰਕ", "bn": "বাণিজ্যিক", "mr": "व्यापारी",
        "gu": "વાણિજ્યિક", "te": "వాణిజ్య", "ta": "வணிகப் பயிர்", "kn": "ವಾಣಿಜ್ಯ", "ml": "വാണിജ്യ വിള"
    },
    "vegetable": {
        "en": "Vegetable", "hi": "सब्जी", "pa": "ਸਬਜ਼ੀ", "bn": "সবজি", "mr": "भाजीपाला",
        "gu": "શાકભાજી", "te": "కూరగాయ", "ta": "காய்கறி", "kn": "ತರಕಾರಿ", "ml": "പച്ചക്കറി"
    },
    "oilseed": {
        "en": "Oilseed", "hi": "तिलहन", "pa": "ਤੇਲ ਬੀਜ", "bn": "তৈলবীজ", "mr": "तेलबिया",
        "gu": "તેલીબિયાં", "te": "నూనెగింజలు", "ta": "எண்ணெய் வித்துக்கள்", "kn": "ಎಣ್ಣೆಕಾಳು", "ml": "എണ്ണക്കുരു"
    },
    "pulse": {
        "en": "Pulse", "hi": "दलहन", "pa": "ਦਾਲਾਂ", "bn": "ডাল", "mr": "कडधान्य",
        "gu": "કઠોળ", "te": "పప్పు", "ta": "பருப்பு", "kn": "ಬೇಳೆಕಾಳು", "ml": "പയർ"
    },
    "spice": {
        "en": "Spice", "hi": "मसाला", "pa": "ਮਸਾਲਾ", "bn": "মশলা", "mr": "मसाला",
        "gu": "મસાલા", "te": "మసాలా", "ta": "மசாலா", "kn": "ಮಸಾಲೆ", "ml": "സുഗന്ധവ്യഞ്ജനം"
    },
    "fruit": {
        "en": "Fruit", "hi": "फल", "pa": "ਫਲ", "bn": "ফল", "mr": "फळ",
        "gu": "ફળ", "te": "పండు", "ta": "பழம்", "kn": "ಹಣ್ಣು", "ml": "പഴം"
    }
}

# 4. Market Trend Translations
TREND_TRANSLATIONS = {
    "rising": {
        "en": "Rising", "hi": "तेजी / बढ़त", "pa": "ਚੜ੍ਹਤ", "bn": "ঊর্ধ্বমুখী", "mr": "तेजी",
        "gu": "વધારો", "te": "పెరుగుదల", "ta": "ஏற்றம்", "kn": "ಏರಿಕೆ", "ml": "വർദ്ധനവ്"
    },
    "steady": {
        "en": "Steady", "hi": "स्थिर", "pa": "ਸਥਿਰ", "bn": "স্থিতিশীল", "mr": "स्थिर",
        "gu": "સ્થિર", "te": "స్థిరమైన", "ta": "நிலையான", "kn": "ಸ್ಥಿರ", "ml": "സ്ഥിരതയുള്ളത്"
    },
    "soft": {
        "en": "Soft", "hi": "नरम / मंदी", "pa": "ਮੰਦਾ", "bn": "নিম্নমুখী", "mr": "मंदी",
        "gu": "નરમ", "te": "తగ్గుదల", "ta": "இறக்கம்", "kn": "ಇಳಿಕೆ", "ml": "കുറവ്"
    }
}

# 5. Mandi & Common UI Strings per Language
MANDI_UI_STRINGS = {
    "en": {
        "nav_signin": "Sign In",
        "nav_mandi": "Mandi Prices & MSP",
        "nav_mandi_direct": "Mandi Bhav",
        "mandi_live_tag": "Live Market Intelligence",
        "mandi_title": "🌾 Real-Time Mandi Bhav & MSP Tracker",
        "mandi_subtitle": "Daily APMC wholesale mandi rates, Government Minimum Support Price (MSP 2024-25/2026), and commodity market trends across India.",
        "mandi_stat_crops": "Key Crops",
        "mandi_stat_states": "States Covered",
        "mandi_stat_mandis": "APMC Mandis",
        "mandi_stat_above_msp": "Trading Above MSP",
        "mandi_search_ph": "Search by crop, market (e.g., Wheat, Indore, Lasalgaon)...",
        "mandi_filter_state": "State:",
        "mandi_all_states": "All States / All Markets",
        "mandi_filter_comm": "Commodity:",
        "mandi_all_comm": "All Commodities / All Crops",
        "mandi_filter_msp": "MSP Status:",
        "mandi_all_rates": "All Rates",
        "mandi_opt_above": "Above MSP (Profitable)",
        "mandi_opt_below": "Below MSP",
        "mandi_advisory_text": "Farmer Advisory: Mandi prices are updated daily from APMC eNAM benchmarks. If market rates fall below Govt MSP, farmers can sell at designated government procurement centers (FCI/NAFED).",
        "mandi_modal_rate": "Modal Mandi Rate",
        "mandi_per_quintal": "per Quintal",
        "mandi_govt_msp": "Govt MSP 2024-25",
        "mandi_above_msp": "Above MSP",
        "mandi_below_msp": "Below MSP",
        "mandi_range": "Range:",
        "mandi_arrivals": "Arrivals:",
        "mandi_trend": "Trend:",
        "trend_rising": "Rising",
        "trend_steady": "Steady",
        "trend_soft": "Soft",
        "cat_cereal": "Cereal",
        "cat_commercial": "Commercial",
        "cat_vegetable": "Vegetable",
        "cat_oilseed": "Oilseed",
        "cat_pulse": "Pulse",
        "cat_spice": "Spice",
        "cat_fruit": "Fruit"
    },
    "hi": {
        "nav_signin": "साइन इन",
        "nav_mandi": "मंडी भाव और MSP",
        "nav_mandi_direct": "मंडी भाव",
        "mandi_live_tag": "ताज़ा मंडी भाव एवं बाज़ार विश्लेषण",
        "mandi_title": "🌾 लाइव मंडी भाव एवं न्यूनतम समर्थन मूल्य (MSP)",
        "mandi_subtitle": "देश भर की मंडियों के दैनिक थोक भाव, केंद्र सरकार का न्यूनतम समर्थन मूल्य (MSP 2024-25/2026) एवं फसल बाज़ार रुझान।",
        "mandi_stat_crops": "प्रमुख फसलें",
        "mandi_stat_states": "शामिल राज्य",
        "mandi_stat_mandis": "APMC मंडियां",
        "mandi_stat_above_msp": "एमएसपी से ऊपर व्यापार",
        "mandi_search_ph": "फसल या मंडी खोजें (जैसे: गेहूं, इंदौर, लासलगांव)...",
        "mandi_filter_state": "राज्य:",
        "mandi_all_states": "सभी राज्य / सभी मंडियां",
        "mandi_filter_comm": "फसल / जींस:",
        "mandi_all_comm": "सभी फसलें",
        "mandi_filter_msp": "MSP स्थिति:",
        "mandi_all_rates": "सभी दरें",
        "mandi_opt_above": "MSP से अधिक (लाभकारी)",
        "mandi_opt_below": "MSP से कम",
        "mandi_advisory_text": "किसान सलाह: मंडी भाव दैनिक APMC eNAM बेंचमार्क से अपडेट किए जाते हैं। यदि बाज़ार भाव सरकारी MSP से नीचे गिरता है, तो किसान निकटतम सरकारी खरीद केंद्रों (FCI/NAFED) पर बेच सकते हैं।",
        "mandi_modal_rate": "मॉडल मंडी भाव",
        "mandi_per_quintal": "प्रति क्विंटल",
        "mandi_govt_msp": "सरकारी MSP 2024-25",
        "mandi_above_msp": "MSP से अधिक",
        "mandi_below_msp": "MSP से कम",
        "mandi_range": "भाव सीमा:",
        "mandi_arrivals": "दैनिक आवक:",
        "mandi_trend": "रुझान:",
        "trend_rising": "तेजी / बढ़त",
        "trend_steady": "स्थिर",
        "trend_soft": "नरम / मंदी",
        "cat_cereal": "अनाज",
        "cat_commercial": "व्यावसायिक",
        "cat_vegetable": "सब्जी",
        "cat_oilseed": "तिलहन",
        "cat_pulse": "दलहन",
        "cat_spice": "मसाला",
        "cat_fruit": "फल"
    },
    "pa": {
        "nav_signin": "ਸਾਈਨ ਇਨ",
        "nav_mandi": "ਮੰਡੀ ਭਾਅ ਅਤੇ MSP",
        "nav_mandi_direct": "ਮੰਡੀ ਭਾਅ",
        "mandi_live_tag": "ਤਾਜ਼ਾ ਮੰਡੀ ਭਾਅ ਅਤੇ ਬਾਜ਼ਾਰ ਅਪਡੇਟ",
        "mandi_title": "🌾 ਲਾਈਵ ਮੰਡੀ ਭਾਅ ਅਤੇ ਸਰਕਾਰੀ ਸਮਰਥਨ ਮੁੱਲ (MSP)",
        "mandi_subtitle": "ਭਾਰਤ ਭਰ ਦੀਆਂ ਏਪੀਐਮਸੀ ਮੰਡੀਆਂ ਦੇ ਰੋਜ਼ਾਨਾ ਭਾਅ, ਸਰਕਾਰੀ ਐਮਐਸਪੀ (2024-25/2026) ਅਤੇ ਫ਼ਸਲਾਂ ਦੇ ਬਾਜ਼ਾਰ ਰੁਝਾਨ।",
        "mandi_stat_crops": "ਮੁੱਖ ਫ਼ਸਲਾਂ",
        "mandi_stat_states": "ਕਵਰ ਕੀਤੇ ਸੂਬੇ",
        "mandi_stat_mandis": "ਏਪੀਐਮਸੀ ਮੰਡੀਆਂ",
        "mandi_stat_above_msp": "ਐਮਐਸਪੀ ਤੋਂ ਉੱਪਰ ਵਿਕਰੀ",
        "mandi_search_ph": "ਫ਼ਸਲ ਜਾਂ ਮੰਡੀ ਖੋਜੋ (ਜਿਵੇਂ: ਕਣਕ, ਖੰਨਾ, ਅੰਮ੍ਰਿਤਸਰ)...",
        "mandi_filter_state": "ਸੂਬਾ:",
        "mandi_all_states": "ਸਾਰੇ ਸੂਬੇ / ਸਾਰੀਆਂ ਮੰਡੀਆਂ",
        "mandi_filter_comm": "ਫ਼ਸਲ / ਜਿਣਸ:",
        "mandi_all_comm": "ਸਾਰੀਆਂ ਫ਼ਸਲਾਂ",
        "mandi_filter_msp": "MSP ਸਥਿਤੀ:",
        "mandi_all_rates": "ਸਾਰੇ ਰੇਟ",
        "mandi_opt_above": "ਐਮਐਸਪੀ ਤੋਂ ਵੱਧ (ਲਾਭਦਾਇਕ)",
        "mandi_opt_below": "ਐਮਐਸਪੀ ਤੋਂ ਘੱਟ",
        "mandi_advisory_text": "ਕਿਸਾਨ ਸਲਾਹ: ਮੰਡੀ ਦੇ ਭਾਅ ਰੋਜ਼ਾਨਾ APMC eNAM ਤੋਂ ਅਪਡੇਟ ਹੁੰਦੇ ਹਨ। ਜੇਕਰ ਬਾਜ਼ਾਰ ਭਾਅ ਸਰਕਾਰੀ ਐਮਐਸਪੀ ਤੋਂ ਘੱਟ ਹੋਵੇ ਤਾਂ ਕਿਸਾਨ ਸਰਕਾਰੀ ਖਰੀਦ ਕੇਂਦਰਾਂ (FCI/NAFED) 'ਤੇ ਵੇਚ ਸਕਦੇ ਹਨ।",
        "mandi_modal_rate": "ਔਸਤ ਮੰਡੀ ਭਾਅ",
        "mandi_per_quintal": "ਪ੍ਰਤੀ ਕੁਇੰਟਲ",
        "mandi_govt_msp": "ਸਰਕਾਰੀ ਐਮਐਸਪੀ",
        "mandi_above_msp": "ਐਮਐਸਪੀ ਤੋਂ ਵੱਧ",
        "mandi_below_msp": "ਐਮਐਸਪੀ ਤੋਂ ਘੱਟ",
        "mandi_range": "ਰੇਂਜ:",
        "mandi_arrivals": "ਆਮਦ:",
        "mandi_trend": "ਰੁਝਾਨ:",
        "trend_rising": "ਚੜ੍ਹਤ",
        "trend_steady": "ਸਥਿਰ",
        "trend_soft": "ਮੰਦਾ",
        "cat_cereal": "ਅਨਾਜ",
        "cat_commercial": "ਵਪਾਰਕ",
        "cat_vegetable": "ਸਬਜ਼ੀ",
        "cat_oilseed": "ਤੇਲ ਬੀਜ",
        "cat_pulse": "ਦਾਲਾਂ",
        "cat_spice": "ਮਸਾਲਾ",
        "cat_fruit": "ਫਲ"
    },
    "bn": {
        "nav_signin": "সাইন ইন",
        "nav_mandi": "মান্ডি দর ও MSP",
        "nav_mandi_direct": "মান্ডি দর",
        "mandi_live_tag": "লাইভ বাজার দর ও তথ্য",
        "mandi_title": "🌾 লাইভ মান্ডি দর ও সরকারি সহায়ক মূল্য (MSP)",
        "mandi_subtitle": "ভারত জুড়ে এপিএমসি মান্ডির দৈনিক পাইকারি দর, সরকারি এমএসপি (2024-25/2026) এবং ফসলের বাজার প্রবণতা।",
        "mandi_stat_crops": "প্রধান ফসল",
        "mandi_stat_states": "অন্তর্ভুক্ত রাজ্য",
        "mandi_stat_mandis": "এপিএমসি মান্ডি",
        "mandi_stat_above_msp": "এমএসপির উপরে বিক্রি",
        "mandi_search_ph": "ফসল বা মান্ডি অনুসন্ধান করুন (যেমন: গম, বর্ধমান, হুগলি)...",
        "mandi_filter_state": "রাজ্য:",
        "mandi_all_states": "সমস্ত রাজ্য / সমস্ত মান্ডি",
        "mandi_filter_comm": "ফসল:",
        "mandi_all_comm": "সমস্ত ফসল",
        "mandi_filter_msp": "MSP স্থিতি:",
        "mandi_all_rates": "সব দর",
        "mandi_opt_above": "এমএসপির বেশি (লাভজনক)",
        "mandi_opt_below": "এমএসপির কম",
        "mandi_advisory_text": "কৃষক পরামর্শ: মান্ডির দর প্রতিদিন APMC eNAM থেকে আপডেট করা হয়। যদি বাজার দর সরকারি MSP-এর নিচে নেমে যায়, তবে কৃষকরা নিকটস্থ সরকারি ক্রয় কেন্দ্রে (FCI/NAFED) বিক্রি করতে পারেন।",
        "mandi_modal_rate": "গড় পাইকারি দর",
        "mandi_per_quintal": "প্রতি কুইন্টাল",
        "mandi_govt_msp": "সরকারি এমএসপি",
        "mandi_above_msp": "এমএসপির বেশি",
        "mandi_below_msp": "এমএসপির কম",
        "mandi_range": "দর সীমা:",
        "mandi_arrivals": "আমদানি:",
        "mandi_trend": "প্রবণতা:",
        "trend_rising": "ঊর্ধ্বমুখী",
        "trend_steady": "স্থিতিশীল",
        "trend_soft": "নিম্নমুখী",
        "cat_cereal": "খাদ্যশস্য",
        "cat_commercial": "বাণিজ্যিক",
        "cat_vegetable": "সবজি",
        "cat_oilseed": "তৈলবীজ",
        "cat_pulse": "ডাল",
        "cat_spice": "মশলা",
        "cat_fruit": "ফল"
    },
    "mr": {
        "nav_signin": "साइन इन",
        "nav_mandi": "बाजारभाव व MSP",
        "nav_mandi_direct": "बाजारभाव",
        "mandi_live_tag": "थेट बाजारभाव व हमीभाव",
        "mandi_title": "🌾 थेट कृषी उत्पन्न बाजारभाव व हमीभाव (MSP)",
        "mandi_subtitle": "देशभरातील प्रमुख कृषी उत्पन्न बाजार समित्यांचे (APMC) दर, शासकीय हमीभाव (2024-25) व बाजार कल।",
        "mandi_stat_crops": "प्रमुख पिके",
        "mandi_stat_states": "समाविष्ट राज्ये",
        "mandi_stat_mandis": "बाजार समित्या",
        "mandi_stat_above_msp": "हमीभावापेक्षा जास्त दर",
        "mandi_search_ph": "पीक किंवा बाजार समिती शोधा (उदा. गहू, नाशिक, लासलगाव)...",
        "mandi_filter_state": "राज्य:",
        "mandi_all_states": "सर्व राज्ये / सर्व मंड्या",
        "mandi_filter_comm": "शेतमाल / पीक:",
        "mandi_all_comm": "सर्व पिके",
        "mandi_filter_msp": "हमीभाव स्थिती:",
        "mandi_all_rates": "सर्व दर",
        "mandi_opt_above": "हमीभावापेक्षा जास्त (नफाकारक)",
        "mandi_opt_below": "हमीभावापेक्षा कमी",
        "mandi_advisory_text": "शेतकरी सल्ला: बाजारभाव दररोज APMC eNAM वरून अपडेट केले जातात. जर बाजारभाव हमीभावापेक्षा खाली घसरल्यास शेतकरी शासकीय खरेदी केंद्रांवर (FCI/NAFED) शेतमाल विकू शकतात.",
        "mandi_modal_rate": "सरासरी बाजारभाव",
        "mandi_per_quintal": "प्रति क्विंटल",
        "mandi_govt_msp": "शासकीय हमीभाव",
        "mandi_above_msp": "हमीभावापेक्षा जास्त",
        "mandi_below_msp": "हमीभावापेक्षा कमी",
        "mandi_range": "किंमत पट्टा:",
        "mandi_arrivals": "आवक:",
        "mandi_trend": "बाजार कल:",
        "trend_rising": "तेजी",
        "trend_steady": "स्थिर",
        "trend_soft": "मंदी",
        "cat_cereal": "धान्य",
        "cat_commercial": "व्यापारी",
        "cat_vegetable": "भाजीपाला",
        "cat_oilseed": "तेलबिया",
        "cat_pulse": "कडधान्य",
        "cat_spice": "मसाला",
        "cat_fruit": "फळ"
    },
    "gu": {
        "nav_signin": "સાઇન ઇન",
        "nav_mandi": "માર્કેટ ભાવ અને MSP",
        "nav_mandi_direct": "માર્કેટ ભાવ",
        "mandi_live_tag": "લાઈવ માર્કેટ યાર્ડ ભાવ",
        "mandi_title": "🌾 લાઈવ માર્કેટ યાર્ડ ભાવ અને ટેકાના ભાવ (MSP)",
        "mandi_subtitle": "સમગ્ર ભારતના APMC માર્કેટ યાર્ડના દૈનિક જથ્થાબંધ ભાવ, સરકારી ટેકાના ભાવ (MSP) અને બજાર વલણો.",
        "mandi_stat_crops": "મુખ્ય પાક",
        "mandi_stat_states": "સમાવિષ્ટ રાજ્યો",
        "mandi_stat_mandis": "માર્કેટ યાર્ડ",
        "mandi_stat_above_msp": "ટેકાના ભાવથી ઉપર",
        "mandi_search_ph": "પાક અથવા માર્કેટ યાર્ડ શોધો (જેમ કે: ઘઉં, રાજકોટ, ઊંઝા)...",
        "mandi_filter_state": "રાજ્ય:",
        "mandi_all_states": "બધા રાજ્યો / તમામ યાર્ડ",
        "mandi_filter_comm": "પાક / જિન્સ:",
        "mandi_all_comm": "બધા પાક",
        "mandi_filter_msp": "MSP સ્થિતિ:",
        "mandi_all_rates": "બધા ભાવ",
        "mandi_opt_above": "ટેકાના ભાવથી વધુ (નફાકારક)",
        "mandi_opt_below": "ટેકાના ભાવથી ઓછું",
        "mandi_advisory_text": "ખેડૂત સલાહ: માર્કેટ યાર્ડના ભાવ દરરોજ APMC eNAM પરથી અપડેટ થાય છે. જો બજાર ભાવ સરકારી ટેકાના ભાવથી નીચે જાય, તો ખેડૂતો સરકારી ખરીદ કેન્દ્રો (FCI/NAFED) પર વેચી શકે છે.",
        "mandi_modal_rate": "સરેરાશ માર્કેટ ભાવ",
        "mandi_per_quintal": "પ્રતિ ક્વિન્ટલ",
        "mandi_govt_msp": "સરકારી ટેકાના ભાવ",
        "mandi_above_msp": "ટેકાના ભાવથી વધુ",
        "mandi_below_msp": "ટેકાના ભાવથી ઓછું",
        "mandi_range": "ભાવ શ્રેણી:",
        "mandi_arrivals": "આવક:",
        "mandi_trend": "વલણ:",
        "trend_rising": "વધારો",
        "trend_steady": "સ્થિર",
        "trend_soft": "નરમ",
        "cat_cereal": "અનાજ",
        "cat_commercial": "વાણિજ્યિક",
        "cat_vegetable": "શાકભાજી",
        "cat_oilseed": "તેલીબિયાં",
        "cat_pulse": "કઠોળ",
        "cat_spice": "મસાલા",
        "cat_fruit": "ફળ"
    },
    "te": {
        "nav_signin": "సైన్ ఇన్",
        "nav_mandi": "మార్కెట్ ధరలు & MSP",
        "nav_mandi_direct": "మార్కెట్ ధరలు",
        "mandi_live_tag": "ప్రత్యక్ష మార్కెట్ ధరలు & సమాచారం",
        "mandi_title": "🌾 ప్రత్యక్ష మార్కెట్ ధరలు & కనీస మద్దతు ధర (MSP)",
        "mandi_subtitle": "భారతదేశం అంతటా APMC మార్కెట్ ధరలు, ప్రభుత్వ కనీస మద్దతు ధర (MSP) మరియు మార్కెట్ ట్రెండ్స్.",
        "mandi_stat_crops": "ప్రధాన పంటలు",
        "mandi_stat_states": "కవర్ చేయబడిన రాష్ట్రాలు",
        "mandi_stat_mandis": "APMC మార్కెట్లు",
        "mandi_stat_above_msp": "MSP కంటే ఎక్కువ ధర",
        "mandi_search_ph": "పంట లేదా మార్కెట్ వెతకండి (ఉదా: గోధుమలు, గుంటూరు, నిజామాబాద్)...",
        "mandi_filter_state": "రాష్ట్రం:",
        "mandi_all_states": "అన్ని రాష్ట్రాలు / అన్ని మార్కెట్లు",
        "mandi_filter_comm": "పంట / వస్తువు:",
        "mandi_all_comm": "అన్ని పంటలు",
        "mandi_filter_msp": "MSP స్థితి:",
        "mandi_all_rates": "అన్ని ధరలు",
        "mandi_opt_above": "MSP కంటే ఎక్కువ (లాభదాయకం)",
        "mandi_opt_below": "MSP కంటే తక్కువ",
        "mandi_advisory_text": "రైతు సలహా: మార్కెట్ ధరలు రోజూ APMC eNAM నుండి నవీకరించబడతాయి. మార్కెట్ ధరలు ప్రభుత్వం నిర్ణయించిన MSP కంటే తక్కువగా ఉంటే, రైతులు ప్రభుత్వ కొనుగోలు కేంద్రాలలో (FCI/NAFED) విక్రయించవచ్చు.",
        "mandi_modal_rate": "సగటు మార్కెట్ ధర",
        "mandi_per_quintal": "క్వింటాల్‌కు",
        "mandi_govt_msp": "ప్రభుత్వ MSP",
        "mandi_above_msp": "MSP కంటే ఎక్కువ",
        "mandi_below_msp": "MSP కంటే తక్కువ",
        "mandi_range": "శ్రేణి:",
        "mandi_arrivals": "రాక:",
        "mandi_trend": "ట్రెండ్:",
        "trend_rising": "పెరుగుదల",
        "trend_steady": "స్థిరమైన",
        "trend_soft": "తగ్గుదల",
        "cat_cereal": "ధాన్యాలు",
        "cat_commercial": "వాణిజ్య",
        "cat_vegetable": "కూరగాయ",
        "cat_oilseed": "నూనెగింజలు",
        "cat_pulse": "పప్పు",
        "cat_spice": "మసాలా",
        "cat_fruit": "పండు"
    },
    "ta": {
        "nav_signin": "உள்நுழைக",
        "nav_mandi": "மண்டி விலை & MSP",
        "nav_mandi_direct": "மண்டி விலை",
        "mandi_live_tag": "நேரடி சந்தை விலை நிலவரம்",
        "mandi_title": "🌾 நேரடி மண்டி விலை & குறைந்தபட்ச ஆதரவு விலை (MSP)",
        "mandi_subtitle": "இந்தியா முழுவதும் உள்ள APMC சந்தை மொத்த விலைகள், அரசு ஆதரவு விலை (MSP) மற்றும் சந்தை போக்குகள்.",
        "mandi_stat_crops": "முக்கிய பயிர்கள்",
        "mandi_stat_states": "உள்ளடக்கிய மாநிலங்கள்",
        "mandi_stat_mandis": "சந்தைகள்",
        "mandi_stat_above_msp": "MSP விட அதிக விலை",
        "mandi_search_ph": "பயிர் அல்லது சந்தையைத் தேடுங்கள் (எ.கா: கோதுமை, ஈரோடு, தஞ்சாவூர்)...",
        "mandi_filter_state": "மாநிலம்:",
        "mandi_all_states": "அனைத்து மாநிலங்கள் / சந்தைகள்",
        "mandi_filter_comm": "பயிர்:",
        "mandi_all_comm": "அனைத்து பயிர்கள்",
        "mandi_filter_msp": "MSP நிலை:",
        "mandi_all_rates": "அனைத்து விலைகள்",
        "mandi_opt_above": "MSP விட அதிகம் (லாபகரமானது)",
        "mandi_opt_below": "MSP விட குறைவு",
        "mandi_advisory_text": "விவசாயி ஆலோசனை: மண்டி விலைகள் தினமும் APMC eNAM மூலம் புதுப்பிக்கப்படுகின்றன. சந்தை விலை அரசு MSP-ஐ விடக் குறைந்தால், விவசாயிகள் அரசு கொள்முதல் மையங்களில் (FCI/NAFED) விற்கலாம்.",
        "mandi_modal_rate": "சராசரி மண்டி விலை",
        "mandi_per_quintal": "குவிண்டாலுக்கு",
        "mandi_govt_msp": "அரசு MSP",
        "mandi_above_msp": "MSP விட அதிகம்",
        "mandi_below_msp": "MSP விட குறைவு",
        "mandi_range": "விலை வரம்பு:",
        "mandi_arrivals": "வரத்து:",
        "mandi_trend": "போக்கு:",
        "trend_rising": "ஏற்றம்",
        "trend_steady": "நிலையான",
        "trend_soft": "இறக்கம்",
        "cat_cereal": "தானியம்",
        "cat_commercial": "வணிகப் பயிர்",
        "cat_vegetable": "காய்கறி",
        "cat_oilseed": "எண்ணெய் வித்துக்கள்",
        "cat_pulse": "பருப்பு",
        "cat_spice": "மசாலா",
        "cat_fruit": "பழம்"
    },
    "kn": {
        "nav_signin": "ಸೈನ್ ಇನ್",
        "nav_mandi": "ಮಂಡಿ ಬೆಲೆಗಳು & MSP",
        "nav_mandi_direct": "ಮಂಡಿ ಬೆಲೆ",
        "mandi_live_tag": "ಲೈವ್ ಮಂಡಿ ಬೆಲೆಗಳ ಮಾಹಿತಿ",
        "mandi_title": "🌾 ನೈಜ ಸಮಯದ ಮಂಡಿ ಬೆಲೆಗಳು & ಬೆಂಬಲ ಬೆಲೆ (MSP)",
        "mandi_subtitle": "ದೇಶಾದ್ಯಂತ APMC ಮಂಡಿಗಳ ದೈನಂದಿನ ಸಗಟು ದರಗಳು, ಸರ್ಕಾರಿ ಬೆಂಬಲ ಬೆಲೆ (MSP) ಮತ್ತು ಮಾರುಕಟ್ಟೆ ಪ್ರವೃತ್ತಿಗಳು.",
        "mandi_stat_crops": "ಪ್ರಮುಖ ಬೆಳೆಗಳು",
        "mandi_stat_states": "ಒಳಗೊಂಡ ರಾಜ್ಯಗಳು",
        "mandi_stat_mandis": "ಮಂಡಿಗಳು",
        "mandi_stat_above_msp": "MSP ಗಿಂತ ಹೆಚ್ಚಿನ ದರ",
        "mandi_search_ph": "ಬೆಳೆ ಅಥವಾ ಮಂಡಿ ಹುಡುಕಿ (ಉದಾ: ಗೋಧಿ, ಕೋಲಾರ, ದಾವಣಗೆರೆ)...",
        "mandi_filter_state": "ರಾಜ್ಯ:",
        "mandi_all_states": "ಎಲ್ಲಾ ರಾಜ್ಯಗಳು / ಎಲ್ಲಾ ಮಂಡಿಗಳು",
        "mandi_filter_comm": "ಬೆಳೆ:",
        "mandi_all_comm": "ಎಲ್ಲಾ ಬೆಳೆಗಳು",
        "mandi_filter_msp": "MSP ಸ್ಥಿತಿ:",
        "mandi_all_rates": "ಎಲ್ಲಾ ದರಗಳು",
        "mandi_opt_above": "MSP ಗಿಂತ ಹೆಚ್ಚು (ಲಾಭದಾಯಕ)",
        "mandi_opt_below": "MSP ಗಿಂತ ಕಡಿಮೆ",
        "mandi_advisory_text": "ರೈತರ ಸಲಹೆ: ಮಂಡಿ ಬೆಲೆಗಳನ್ನು ಪ್ರತಿದಿನ APMC eNAM ನಿಂದ ನವೀಕರಿಸಲಾಗುತ್ತದೆ. ಮಾರುಕಟ್ಟೆ ದರಗಳು ಸರ್ಕಾರದ MSP ಗಿಂತ ಕಡಿಮೆಯಾದರೆ, ರೈತರು ಸರ್ಕಾರಿ ಖರೀದಿ ಕೇಂದ್ರಗಳಲ್ಲಿ (FCI/NAFED) ಮಾರಾಟ ಮಾಡಬಹುದು.",
        "mandi_modal_rate": "ಸರಾಸರಿ ಮಂಡಿ ಬೆಲೆ",
        "mandi_per_quintal": "ಪ್ರತಿ ಕ್ವಿಂಟಾಲ್‌ಗೆ",
        "mandi_govt_msp": "ಸರ್ಕಾರಿ ಬೆಂಬಲ ಬೆಲೆ",
        "mandi_above_msp": "MSP ಗಿಂತ ಹೆಚ್ಚು",
        "mandi_below_msp": "MSP ಗಿಂತ ಕಡಿಮೆ",
        "mandi_range": "ಬೆಲೆ ಶ್ರೇಣಿ:",
        "mandi_arrivals": "ಆವಕ:",
        "mandi_trend": "ಪ್ರವೃತ್ತಿ:",
        "trend_rising": "ಏರಿಕೆ",
        "trend_steady": "ಸ್ಥಿರ",
        "trend_soft": "ಇಳಿಕೆ",
        "cat_cereal": "ಧಾನ್ಯ",
        "cat_commercial": "ವಾಣಿಜ್ಯ",
        "cat_vegetable": "ತರಕಾರಿ",
        "cat_oilseed": "ಎಣ್ಣೆಕಾಳು",
        "cat_pulse": "ಬೇಳೆಕಾಳು",
        "cat_spice": "ಮಸಾಲೆ",
        "cat_fruit": "ಹಣ್ಣು"
    },
    "ml": {
        "nav_signin": "സൈൻ ഇൻ",
        "nav_mandi": "വിപണി വിലകളും MSP യും",
        "nav_mandi_direct": "വിപണി വില",
        "mandi_live_tag": "തത്സമയ വിപണി വിലകൾ",
        "mandi_title": "🌾 തത്സമയ വിപണി വിലകളും താങ്ങുവിലയും (MSP)",
        "mandi_subtitle": "ഇന്ത്യയിലുടനീളമുള്ള APMC മാർക്കറ്റ് നിരക്കുകൾ, സർക്കാർ താങ്ങുവില (MSP), വിപണി പ്രവണതകൾ.",
        "mandi_stat_crops": "പ്രധാന വിളകൾ",
        "mandi_stat_states": "ഉൾപ്പെടുത്തിയ സംസ്ഥാനങ്ങൾ",
        "mandi_stat_mandis": "വിപണികൾ",
        "mandi_stat_above_msp": "MSP യേക്കാൾ ഉയർന്ന നിരക്ക്",
        "mandi_search_ph": "വിള അല്ലെങ്കിൽ വിപണി തിരയുക (ഉദാ: ഗോതമ്പ്, വയനാട്, ഇടുക്കി)...",
        "mandi_filter_state": "സംസ്ഥാനം:",
        "mandi_all_states": "എല്ലാ സംസ്ഥാനങ്ങളും / വിപണികളും",
        "mandi_filter_comm": "വിള:",
        "mandi_all_comm": "എല്ലാ വിളകളും",
        "mandi_filter_msp": "MSP നില:",
        "mandi_all_rates": "എല്ലാ നിരക്കുകളും",
        "mandi_opt_above": "MSP യേക്കാൾ കൂടുതൽ (ലാഭകരം)",
        "mandi_opt_below": "MSP യേക്കാൾ കുറവ്",
        "mandi_advisory_text": "കർഷക നിർദ്ദേശം: വിപണി വിലകൾ ദിവസവും APMC eNAM-ൽ നിന്ന് പുതുക്കുന്നു. വിപണി വില സർക്കാർ MSP-യേക്കാൾ കുറവാണെങ്കിൽ കർഷകർക്ക് സർക്കാർ സംഭരണ കേന്ദ്രങ്ങളിൽ (FCI/NAFED) വിൽക്കാം.",
        "mandi_modal_rate": "ശരാശരി വിപണി നിരക്ക്",
        "mandi_per_quintal": "ക്വിന്റലിന്",
        "mandi_govt_msp": "സർക്കാർ താങ്ങുവില",
        "mandi_above_msp": "MSP യേക്കാൾ കൂടുതൽ",
        "mandi_below_msp": "MSP യേക്കാൾ കുറവ്",
        "mandi_range": "വില പരിധി:",
        "mandi_arrivals": "വരവ്:",
        "mandi_trend": "പ്രവണത:",
        "trend_rising": "വർദ്ധനവ്",
        "trend_steady": "സ്ഥിരതയുള്ളത്",
        "trend_soft": "കുറവ്",
        "cat_cereal": "ധാന്യം",
        "cat_commercial": "വാണിജ്യ വിള",
        "cat_vegetable": "പച്ചക്കറി",
        "cat_oilseed": "എണ്ണക്കുരു",
        "cat_pulse": "പയർ",
        "cat_spice": "സുഗന്ധവ്യഞ്ജനം",
        "cat_fruit": "പഴം"
    }
}

# 6. Aliases Map
CROP_ALIASES = {
    "chana": "chickpea",
    "chana_desi": "chickpea",
    "bengal_gram": "chickpea",
    "arhar": "pigeonpeas",
    "tur": "pigeonpeas",
    "red_gram": "pigeonpeas",
    "tuver": "pigeonpeas",
    "moong": "mungbean",
    "green_gram": "mungbean",
    "urad": "blackgram",
    "black_gram": "blackgram",
    "masoor": "lentil",
    "rajma": "kidneybeans",
    "moth": "mothbeans",
    "gehu": "wheat",
    "dhan": "paddy",
    "chawal": "rice",
    "makka": "maize",
    "sarson": "mustard",
    "rai": "mustard",
    "til": "sunflower",
    "kapas": "cotton",
    "ganna": "sugarcane",
    "aalu": "potato",
    "pyaz": "onion",
    "tamatar": "tomato",
    "adrak": "ginger",
    "haldi": "turmeric",
    "mirch": "chilli",
    "lahsun": "garlic",
    "paddy (basmati)": "paddy_basmati",
    "paddy (common)": "paddy_common",
    "gram (chana)": "chickpea",
    "pigeonpeas (arhar/tur)": "pigeonpeas"
}

def generate_translations_js():
    import re
    # Read existing translations.js
    with open("static/js/translations.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Find the KRISHI_TRANSLATIONS dictionary block
    kt_start = content.find('const KRISHI_TRANSLATIONS = {')
    kt_end = content.find('};\n\n/**', kt_start)
    kt_block = content[kt_start:kt_end]

    lang_codes = ["en", "hi", "pa", "bn", "mr", "gu", "te", "ta", "kn", "ml"]
    
    extracted_translations = {}
    
    for i, code in enumerate(lang_codes):
        pattern = r'\b' + code + r':\s*\{([^}]+)\}'
        match = re.search(pattern, kt_block)
        dict_items = {}
        if match:
            block = match.group(1)
            # Find all `key: "value"`
            kv_pattern = r'([a-zA-Z0-9_]+)\s*:\s*["\']([^"\']+)["\']'
            for k, v in re.findall(kv_pattern, block):
                dict_items[k] = v
        
        # Merge with MANDI_UI_STRINGS
        if code in MANDI_UI_STRINGS:
            for mk, mv in MANDI_UI_STRINGS[code].items():
                dict_items[mk] = mv
        
        extracted_translations[code] = dict_items

    print("Extracted and merged translation keys for all languages:")
    for code, items in extracted_translations.items():
        print(f"  {code}: {len(items)} keys")

    # Now construct the full translations.js content
    js_parts = []
    js_parts.append("""/**
 * Krishi Mitra: Indian Regional Languages Translation Engine (i18n)
 * Covers the 10 most prominent languages across every geographic region of India:
 * North: Hindi (hi), Punjabi (pa)
 * West: Gujarati (gu), Marathi (mr)
 * East: Bengali (bn)
 * South: Telugu (te), Tamil (ta), Kannada (kn), Malayalam (ml)
 * Universal: English (en)
 * 
 * Features:
 * - Real-time full-page UI translation
 * - Master 42+ Indian Crop Multi-lingual Dictionary
 * - APMC Mandi Bhav & Govt MSP Localization
 * - Dynamic form selectors, cards, badges, and AI components
 */

const INDIAN_LANGUAGES = """ + json.dumps(INDIAN_LANGUAGES, ensure_ascii=False, indent=2) + """;

const CROP_TRANSLATIONS = """ + json.dumps(CROP_TRANSLATIONS, ensure_ascii=False, indent=2) + """;

const CROP_ALIASES = """ + json.dumps(CROP_ALIASES, ensure_ascii=False, indent=2) + """;

const CATEGORY_TRANSLATIONS = """ + json.dumps(CATEGORY_TRANSLATIONS, ensure_ascii=False, indent=2) + """;

const TREND_TRANSLATIONS = """ + json.dumps(TREND_TRANSLATIONS, ensure_ascii=False, indent=2) + """;

const KRISHI_TRANSLATIONS = """ + json.dumps(extracted_translations, ensure_ascii=False, indent=2) + """;

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
 * Helper to get translated crop name across 10 regional Indian languages
 * Supports exact match, normalized lowercase, and aliases
 */
function getCropTranslation(cropName, langCode) {
  if (!cropName) return "";
  langCode = langCode || getCurrentLanguage() || "en";
  const str = String(cropName).trim();
  const rawLower = str.toLowerCase();

  if (langCode === "en") {
    const aliasKey = CROP_ALIASES[rawLower];
    if (aliasKey && CROP_TRANSLATIONS[aliasKey]) {
      return CROP_TRANSLATIONS[aliasKey].en;
    }
    if (CROP_TRANSLATIONS[rawLower]) {
      return CROP_TRANSLATIONS[rawLower].en;
    }
    return str;
  }

  // 1. Check exact key
  if (CROP_TRANSLATIONS[rawLower] && CROP_TRANSLATIONS[rawLower][langCode]) {
    return CROP_TRANSLATIONS[rawLower][langCode];
  }

  // 2. Check alias map
  const aliasKey = CROP_ALIASES[rawLower];
  if (aliasKey && CROP_TRANSLATIONS[aliasKey] && CROP_TRANSLATIONS[aliasKey][langCode]) {
    return CROP_TRANSLATIONS[aliasKey][langCode];
  }

  // 3. Clean string by removing punctuation
  const cleanKey = rawLower.replace(/[\\(\\)\\[\\]\\{\\}\\/\\\\,]/g, " ").replace(/\\s+/g, "_").trim();
  if (CROP_TRANSLATIONS[cleanKey] && CROP_TRANSLATIONS[cleanKey][langCode]) {
    return CROP_TRANSLATIONS[cleanKey][langCode];
  }

  // 4. Check if standard keywords appear in compound string
  if (rawLower.includes("basmati") && CROP_TRANSLATIONS["paddy_basmati"]) {
    return CROP_TRANSLATIONS["paddy_basmati"][langCode];
  }
  if (rawLower.includes("paddy") && rawLower.includes("common") && CROP_TRANSLATIONS["paddy_common"]) {
    return CROP_TRANSLATIONS["paddy_common"][langCode];
  }
  if ((rawLower.includes("chana") || rawLower.includes("chickpea") || rawLower === "gram") && CROP_TRANSLATIONS["chickpea"]) {
    return CROP_TRANSLATIONS["chickpea"][langCode];
  }
  if ((rawLower.includes("arhar") || rawLower.includes("tur") || rawLower.includes("pigeonpea")) && CROP_TRANSLATIONS["pigeonpeas"]) {
    return CROP_TRANSLATIONS["pigeonpeas"][langCode];
  }

  // 5. Keyword search in crop dictionary
  for (const [key, trans] of Object.entries(CROP_TRANSLATIONS)) {
    if (rawLower === key || rawLower.startsWith(key) || key.startsWith(rawLower)) {
      return trans[langCode] || trans.en;
    }
  }

  // Fallback: return original string
  return str;
}

/**
 * Helper to get translated category (Cereal, Commercial, Vegetable, Oilseed, Pulse, Spice, Fruit)
 */
function getCategoryTranslation(catName, langCode) {
  if (!catName) return "";
  langCode = langCode || getCurrentLanguage() || "en";
  const key = String(catName).toLowerCase().trim();
  if (CATEGORY_TRANSLATIONS[key] && CATEGORY_TRANSLATIONS[key][langCode]) {
    return CATEGORY_TRANSLATIONS[key][langCode];
  }
  return catName;
}

/**
 * Helper to get translated trend (Rising, Steady, Soft)
 */
function getTrendTranslation(trendName, langCode) {
  if (!trendName) return "";
  langCode = langCode || getCurrentLanguage() || "en";
  const key = String(trendName).toLowerCase().trim();
  if (TREND_TRANSLATIONS[key] && TREND_TRANSLATIONS[key][langCode]) {
    return TREND_TRANSLATIONS[key][langCode];
  }
  return trendName;
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

  // Update crop names across the page
  document.querySelectorAll("[data-crop], .crop-title, .crop-name").forEach((el) => {
    const orig = el.getAttribute("data-crop") || el.getAttribute("data-crop-original") || el.textContent.trim();
    if (!el.getAttribute("data-crop-original")) {
      el.setAttribute("data-crop-original", orig);
    }
    const translated = getCropTranslation(orig, langCode);
    if (translated) {
      el.textContent = translated;
    }
  });

  // Update crop select dropdowns (e.g. Mandi Commodity filter, Crop Guide, Weather, Remote Sensing)
  document.querySelectorAll("select#commodityFilter, select#cropSelect, select#cropName").forEach((sel) => {
    Array.from(sel.options).forEach((opt) => {
      if (opt.value === "" || opt.value === "all") return;
      if (!opt.getAttribute("data-orig-text")) {
        opt.setAttribute("data-orig-text", opt.textContent.trim());
      }
      const rawText = opt.getAttribute("data-crop") || opt.value || opt.getAttribute("data-orig-text");
      const trans = getCropTranslation(rawText, langCode);
      if (langCode === "en") {
        opt.textContent = opt.getAttribute("data-orig-text");
      } else {
        const cleanBase = opt.getAttribute("data-orig-text").split("(")[0].trim();
        opt.textContent = `${trans} (${cleanBase})`;
      }
    });
  });

  // Update category tags
  document.querySelectorAll("[data-cat], .commodity-tag").forEach((el) => {
    const orig = el.getAttribute("data-cat") || el.getAttribute("data-cat-original") || el.textContent.trim();
    if (!el.getAttribute("data-cat-original")) {
      el.setAttribute("data-cat-original", orig);
    }
    const trans = getCategoryTranslation(orig, langCode);
    if (trans) {
      el.textContent = trans;
    }
  });

  // Update trend badges
  document.querySelectorAll("[data-trend], .trend-badge").forEach((el) => {
    const orig = el.getAttribute("data-trend") || el.getAttribute("data-trend-original");
    if (!orig) return;
    if (!el.getAttribute("data-trend-original")) {
      el.setAttribute("data-trend-original", orig);
    }
    const trans = getTrendTranslation(orig, langCode);
    const dot = orig.toLowerCase() === "rising" ? "🟢" : orig.toLowerCase() === "steady" ? "🟡" : "🔴";
    el.textContent = `${dot} ${trans}`;
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

  // Dispatch custom event for page scripts (chat, weather, crop rec, etc.)
  window.dispatchEvent(new CustomEvent("krishiLanguageChanged", { detail: { language: langCode } }));
}

// Global exposure for all application components
window.getCropTranslation = getCropTranslation;
window.formatCrop = getCropTranslation;
window.getCategoryTranslation = getCategoryTranslation;
window.getTrendTranslation = getTrendTranslation;
window.CROP_TRANSLATIONS = CROP_TRANSLATIONS;
window.CROP_ALIASES = CROP_ALIASES;
window.CATEGORY_TRANSLATIONS = CATEGORY_TRANSLATIONS;
window.TREND_TRANSLATIONS = TREND_TRANSLATIONS;
window.KRISHI_TRANSLATIONS = KRISHI_TRANSLATIONS;
window.INDIAN_LANGUAGES = INDIAN_LANGUAGES;
window.applyLanguage = applyLanguage;
window.getCurrentLanguage = getCurrentLanguage;

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
""")

    output_js = "".join(js_parts)
    with open("static/js/translations.js", "w", encoding="utf-8") as f:
        f.write(output_js)
    print("Successfully generated static/js/translations.js!")

if __name__ == "__main__":
    generate_translations_js()
