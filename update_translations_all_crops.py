# -*- coding: utf-8 -*-
"""
Update static/js/translations.js with all 90 Indian Crops (61 General + 29 Fruit)
across all 10 Indian Regional Languages (en, hi, pa, bn, mr, gu, te, ta, kn, ml).
Also adds UI translations for 'general_crops', 'fruit_crops', and guide details.
"""

import json
import re

CROP_DICT_90 = {
    # ==============================
    # 🌾 61 GENERAL CROPS
    # ==============================
    "wheat": {
        "en": "Wheat", "hi": "गेहूँ", "pa": "ਕਣਕ", "bn": "গম", "mr": "गहू",
        "gu": "ઘઉં", "te": "గోధుమలు", "ta": "கோதுமை", "kn": "ಗೋಧಿ", "ml": "ഗോതമ്പ്"
    },
    "rice": {
        "en": "Rice / Paddy", "hi": "धान / चावल", "pa": "ਝੋਨਾ / ਚੌਲ", "bn": "ধান / চাল", "mr": "भात / तांदूळ",
        "gu": "ડાંગર / ચોખા", "te": "వరి / బియ్యం", "ta": "நெல் / அரிசி", "kn": "ಭತ್ತ / ಅಕ್ಕಿ", "ml": "നെല്ല് / അരി"
    },
    "maize": {
        "en": "Maize / Corn", "hi": "मक्का", "pa": "ਮੱਕੀ", "bn": "ভুট্টা", "mr": "मका",
        "gu": "મકાઈ", "te": "మొక్కజొన్న", "ta": "மக்காச்சோளம்", "kn": "ಮೆಕ್ಕೆಜೋಳ", "ml": "മക്കച്ചോളം"
    },
    "bajra": {
        "en": "Pearl Millet (Bajra)", "hi": "बाजरा", "pa": "ਬਾਜਰਾ", "bn": "বাজরা", "mr": "बाजरी",
        "gu": "બાજરી", "te": "సజ్జలు", "ta": "கம்பு", "kn": "ಸಜ್ಜೆ", "ml": "കമ്പം"
    },
    "jowar": {
        "en": "Sorghum (Jowar)", "hi": "ज्वार", "pa": "ਜਵਾਰ", "bn": "জোয়ার", "mr": "ज्वारी",
        "gu": "જુવાર", "te": "జొన్నలు", "ta": "சோளம்", "kn": "ಜೋಳ", "ml": "ചോളം"
    },
    "ragi": {
        "en": "Finger Millet (Ragi)", "hi": "रागी / मडुआ", "pa": "ਰਾਗੀ", "bn": "মারুয়া / রাগি", "mr": "नाचणी / रागी",
        "gu": "નાગલી / રાગી", "te": "రాగులు", "ta": "கேழ்வரகு / ராகி", "kn": "ರಾಗಿ", "ml": "കൂവരക് / റാഗി"
    },
    "barley": {
        "en": "Barley (Jau)", "hi": "जौ", "pa": "ਜੌਂ", "bn": "যব", "mr": "सत्तू / जव",
        "gu": "જવ", "te": "బార్లీ", "ta": "பார்லி", "kn": "ಬಾರ್ಲಿ", "ml": "ബാർലി"
    },
    "foxtail_millet": {
        "en": "Foxtail Millet (Kangni)", "hi": "कंगनी / काकुन", "pa": "ਕੰਗਣੀ", "bn": "কাওন", "mr": "राळा",
        "gu": "કાંગ", "te": "కొర్రలు", "ta": "தினை", "kn": "ನವಣೆ", "ml": "തിന"
    },
    "kodo_millet": {
        "en": "Kodo Millet (Kodra)", "hi": "कोदो / कोदरा", "pa": "ਕੋਦਰਾ", "bn": "কোদা", "mr": "कोदरा",
        "gu": "કોદરા", "te": "అరికెలు", "ta": "வரகு", "kn": "ಹಾರಕ", "ml": "വരക്"
    },
    "little_millet": {
        "en": "Little Millet (Kutki)", "hi": "कुटकी", "pa": "ਕੁਟਕੀ", "bn": "সামা", "mr": "वरी / भगर",
        "gu": "ગજરો / મોરૈયો", "te": "సామలు", "ta": "சாமை", "kn": "ಸಾಮೆ", "ml": "ചാമ"
    },
    "barnyard_millet": {
        "en": "Barnyard Millet (Sanwa)", "hi": "सांवा / झंगोरा", "pa": "ਸਵਾਂਕ", "bn": "শ্যামা চাল", "mr": "वरई",
        "gu": "મોરૈયો / સામો", "te": "ఊదలు", "ta": "குதிரைவாலி", "kn": "ಊದಲು", "ml": "കുതിരവാലി"
    },
    "proso_millet": {
        "en": "Proso Millet (Cheena)", "hi": "चीना / बारी", "pa": "ਚੀਨਾ", "bn": "চীনা", "mr": "वरी",
        "gu": "ચેણો", "te": "వరిగెలు", "ta": "பனிவரகு", "kn": "ಬರಗು", "ml": "പനിവരക്"
    },
    "chickpea": {
        "en": "Chickpea (Chana)", "hi": "चना", "pa": "ਛੋਲੇ / ਚਣਾ", "bn": "ছোলা", "mr": "हरभरा / चणा",
        "gu": "ચણા", "te": "శనగలు", "ta": "கொண்டைக்கடலை", "kn": "ಕಡಲೆ", "ml": "കടല"
    },
    "pigeonpeas": {
        "en": "Pigeonpeas (Arhar / Tur)", "hi": "अरहर / तुअर", "pa": "ਅਰਹਰ / ਤੂਰ", "bn": "অড়হর", "mr": "तूर",
        "gu": "તુવેર", "te": "కందులు", "ta": "துவரம்பருப்பு", "kn": "ತೊಗರಿ", "ml": "തുവരപ്പരിപ്പ്"
    },
    "mungbean": {
        "en": "Mung Bean (Moong)", "hi": "मूंग", "pa": "ਮੂੰਗ", "bn": "মুগ", "mr": "मूग",
        "gu": "મગ", "te": "పెసలు", "ta": "பாசிப்பயறு", "kn": "ಹೆಸರುಕಾಳು", "ml": "ചെറുപയർ"
    },
    "blackgram": {
        "en": "Black Gram (Urad)", "hi": "उड़द", "pa": "ਮਾਂਹ / ਉੜਦ", "bn": "মাষকলাই", "mr": "उडीद",
        "gu": "અડદ", "te": "మినుములు", "ta": "உளுந்து", "kn": "ಉದ್ದಿನಕಾಳು", "ml": "உழுந்து"
    },
    "lentil": {
        "en": "Lentil (Masoor)", "hi": "मसूर", "pa": "ਮਸਰ", "bn": "মসুর", "mr": "मसूर",
        "gu": "મસૂર", "te": "మసూర్ పప్పు", "ta": "மசூர் பருப்பு", "kn": "ಮಸೂರ ಬೇಳೆ", "ml": "മസൂർ പരിപ്പ്"
    },
    "kidneybeans": {
        "en": "Kidney Beans (Rajma)", "hi": "राजमा", "pa": "ਰਾਜਮਾਂਹ", "bn": "রাজমা", "mr": "राजमा",
        "gu": "રાજમા", "te": "రాజ్మా", "ta": "ராஜ்மா", "kn": "ರಾಜ್ಮಾ", "ml": "രാജ്മ"
    },
    "mothbeans": {
        "en": "Moth Bean (Matki)", "hi": "मोठ", "pa": "ਮੋਠ", "bn": "মটকি", "mr": "मटकी",
        "gu": "મઠ", "te": "బొబ్బర్లు / మోత్", "ta": "தட்டப்பயறு", "kn": "ಮಡಿಕೆಕಾಳು", "ml": "പയർ"
    },
    "cowpea": {
        "en": "Cowpea (Lobia)", "hi": "लोबिया / चौली", "pa": "ਰਵਾਂਹ / ਲੋਬੀਆ", "bn": "বরবটি", "mr": "चवळी",
        "gu": "ચોળા", "te": "అలసందలు", "ta": "காராமணி", "kn": "ಅಲಸಂದೆ", "ml": "വൻപയർ"
    },
    "green_peas": {
        "en": "Green Peas (Matar)", "hi": "हरी मटर", "pa": "ਹਰਾ ਮਟਰ", "bn": "মটরশুঁটি", "mr": "हिरवा वाटाणा",
        "gu": "લીલા વટાણા", "te": "బఠానీలు", "ta": "பச்சை பட்டாணி", "kn": "ಹಸಿರು ಬಟಾಣಿ", "ml": "പച്ചപ്പട്ടാണി"
    },
    "horsegram": {
        "en": "Horse Gram (Kulthi)", "hi": "कुलथी", "pa": "ਕੁਲਥੀ", "bn": "কুলথী কলাই", "mr": "कुळीथ / हुलगा",
        "gu": "કુળથી", "te": "ఉలవలు", "ta": "கொள்ளு", "kn": "ಹುರುಳಿ", "ml": "മുതിര"
    },
    "sugarcane": {
        "en": "Sugarcane", "hi": "गन्ना", "pa": "ਗੰਨਾ", "bn": "আখ", "mr": "ऊस",
        "gu": "શેરડી", "te": "చెరకు", "ta": "கரும்பு", "kn": "ಕಬ್ಬು", "ml": "കരിമ്പ്"
    },
    "cotton": {
        "en": "Cotton (Kapas)", "hi": "कपास", "pa": "ਨਰਮਾ / ਕਪਾਹ", "bn": "তুলা", "mr": "कापूस",
        "gu": "કપાસ", "te": "పత్తి", "ta": "பருத்தி", "kn": "ಹತ್ತಿ", "ml": "പരുത്തി"
    },
    "jute": {
        "en": "Jute (Pat)", "hi": "पटसन / जूट", "pa": "ਪਟਸਨ", "bn": "পাট", "mr": "ताग",
        "gu": "શણ", "te": "జనపనార", "ta": "சணல்", "kn": "ಸೆಣಬು", "ml": "ചണം"
    },
    "tea": {
        "en": "Tea", "hi": "चाय", "pa": "ਚਾਹ", "bn": "চা", "mr": "चहा",
        "gu": "ચા", "te": "తేయాకు", "ta": "தேயிலை", "kn": "ಚಹಾ", "ml": "തേയില"
    },
    "coffee": {
        "en": "Coffee", "hi": "कॉफ़ी", "pa": "ਕੌਫੀ", "bn": "কফি", "mr": "कॉफी",
        "gu": "કોફી", "te": "కాఫీ", "ta": "காபி", "kn": "ಕಾಫಿ", "ml": "കാപ്പി"
    },
    "rubber": {
        "en": "Rubber", "hi": "रबर", "pa": "ਰਬੜ", "bn": "রবার", "mr": "रबर",
        "gu": "રબર", "te": "రబ్బరు", "ta": "ரப்பர்", "kn": "ರಬ್ಬರ್", "ml": "റബ്ബർ"
    },
    "tobacco": {
        "en": "Tobacco", "hi": "तंबाकू", "pa": "ਤੰਬਾਕੂ", "bn": "তামাক", "mr": "तंबाखू",
        "gu": "તમાકુ", "te": "పొగాకు", "ta": "புகையிலை", "kn": "ತಂಬಾಕು", "ml": "പുകയില"
    },
    "mustard": {
        "en": "Mustard (Sarson)", "hi": "सरसों / राई", "pa": "ਸਰ੍ਹੋਂ", "bn": "সরিষা", "mr": "मोहरी",
        "gu": "રાઈ / સરસવ", "te": "ఆవాలు", "ta": "கடுகு", "kn": "ಸಾಸಿವೆ", "ml": "കടുക്"
    },
    "soybean": {
        "en": "Soybean", "hi": "सोयाबीन", "pa": "ਸੋਇਆਬੀਨ", "bn": "সয়াবিন", "mr": "सोयाबीन",
        "gu": "સોયાબીન", "te": "సోయాబీన్", "ta": "சோயாபீன்", "kn": "ಸೋಯಾಬೀನ್", "ml": "സോയാബീൻ"
    },
    "groundnut": {
        "en": "Groundnut / Peanut", "hi": "मूंगफली", "pa": "ਮੂੰਗਫਲੀ", "bn": "চীনাবাদাম", "mr": "भुईमूग",
        "gu": "મગફળી", "te": "వేరుశనగ", "ta": "வேர்க்கடலை", "kn": "ಕಡಲೆಕಾಯಿ", "ml": "നിലക്കടല"
    },
    "sunflower": {
        "en": "Sunflower", "hi": "सूरजमुखी", "pa": "ਸੂਰਜਮੁਖੀ", "bn": "সূর্যমুখী", "mr": "सूर्यफूल",
        "gu": "સૂર્યમુખી", "te": "పొద్దుతిరుగుడు", "ta": "சூரியகாந்தி", "kn": "ಸೂರ್ಯಕಾಂತಿ", "ml": "സൂര്യകാന്തി"
    },
    "sesame": {
        "en": "Sesame (Til)", "hi": "तिल", "pa": "ਤਿਲ", "bn": "তিল", "mr": "तीळ",
        "gu": "તલ", "te": "నువ్వులు", "ta": "எள்", "kn": "ಎಳ್ಳು", "ml": "എള്ള്"
    },
    "castor": {
        "en": "Castor (Arandi)", "hi": "अरण्डी", "pa": "ਅਰਿੰਡ", "bn": "রেড়ী", "mr": "एरंडी",
        "gu": "દિવેલા / એરંડા", "te": "ఆముదము", "ta": "ஆமணக்கு", "kn": "ಹರಳು", "ml": "ആവണക്ക്"
    },
    "linseed": {
        "en": "Linseed (Alsi)", "hi": "अलसी", "pa": "ਅਲਸੀ", "bn": "তিসি", "mr": "जवस",
        "gu": "અળસી", "te": "అవిసె గింజలు", "ta": "ஆளி விதை", "kn": "ಅಗಸೆ", "ml": "ചണവിത്ത്"
    },
    "safflower": {
        "en": "Safflower (Kusum)", "hi": "कुसुम / करड़ी", "pa": "ਕੁਸੁਮ", "bn": "কুসুমফুল", "mr": "करडई",
        "gu": "કુસુમ / કરડી", "te": "కుసుమలు", "ta": "குசும்ப பூ", "kn": "ಕುಸುಬೆ", "ml": "കുസുമം"
    },
    "turmeric": {
        "en": "Turmeric (Haldi)", "hi": "हल्दी", "pa": "ਹਲਦੀ", "bn": "হলুদ", "mr": "हळद",
        "gu": "હળદર", "te": "పసుపు", "ta": "மஞ்சள்", "kn": "ಅರಿಶಿನ", "ml": "മഞ്ഞൾ"
    },
    "chilli": {
        "en": "Chilli / Red Pepper", "hi": "मिर्च", "pa": "ਮਿਰਚ", "bn": "লঙ্কা / মরিচ", "mr": "मिरची",
        "gu": "મરચાં", "te": "మిరపకాయ", "ta": "மிளகாய்", "kn": "ಮೆಣಸಿನಕಾಯಿ", "ml": "മുളക്"
    },
    "ginger": {
        "en": "Ginger (Adrak)", "hi": "अदरक", "pa": "ਅਦਰਕ", "bn": "আদা", "mr": "आले",
        "gu": "આદું", "te": "అల్లం", "ta": "இஞ்சி", "kn": "ಶುಂಠಿ", "ml": "ഇഞ്ചി"
    },
    "garlic": {
        "en": "Garlic (Lahsun)", "hi": "लहसुन", "pa": "ਲਸਣ", "bn": "রসুন", "mr": "लसूण",
        "gu": "લસણ", "te": "వెల్లుల్లి", "ta": "பூண்டு", "kn": "ಬೆಳ್ಳುಳ್ಳಿ", "ml": "വെളുത്തുള്ളി"
    },
    "cardamom": {
        "en": "Cardamom (Elaichi)", "hi": "इलायची", "pa": "ਇਲਾਇਚੀ", "bn": "এলাচ", "mr": "वेलची",
        "gu": "ઈલાયચી", "te": "ఏలకులు", "ta": "ஏலக்காய்", "kn": "ಏಲಕ್ಕಿ", "ml": "ഏലയ്ക്ക"
    },
    "coriander": {
        "en": "Coriander (Dhaniya)", "hi": "धनिया", "pa": "ਧਨੀਆ", "bn": "ধনে", "mr": "धने / कोथिंबीर",
        "gu": "ધાણા", "te": "ధనియాలు", "ta": "கொத்தமல்லி", "kn": "ಕೊತ್ತಂಬರಿ", "ml": "മല്ലി"
    },
    "cumin": {
        "en": "Cumin (Jeera)", "hi": "जीरा", "pa": "ਜੀਰਾ", "bn": "জিরে", "mr": "जिरे",
        "gu": "જીરું", "te": "జీలకర్ర", "ta": "சீரகம்", "kn": "ಜೀರಿಗೆ", "ml": "ജീരകം"
    },
    "fennel": {
        "en": "Fennel (Saunf)", "hi": "सौंफ", "pa": "ਸੌਂਫ", "bn": "মৌরি", "mr": "बडीशेप",
        "gu": "વરિયાળી", "te": "సోంపు", "ta": "சோம்பு", "kn": "ಸೋಂಪು", "ml": "പെരുംജീരകം"
    },
    "fenugreek": {
        "en": "Fenugreek (Methi)", "hi": "मेथी", "pa": "ਮੇਥੀ", "bn": "মেথি", "mr": "मेथी",
        "gu": "મેથી", "te": "మెంతులు", "ta": "வெந்தயம்", "kn": "ಮೆಂತ್ಯ", "ml": "ഉലുവ"
    },
    "black_pepper": {
        "en": "Black Pepper (Kali Mirch)", "hi": "काली मिर्च", "pa": "ਕਾਲੀ ਮਿਰਚ", "bn": "গোলমরিচ", "mr": "काळी मिरी",
        "gu": "કાળા મરી", "te": "మిరియాలు", "ta": "மிளகு", "kn": "ಕಾಳುಮೆಣಸು", "ml": "കുരുമുളക്"
    },
    "potato": {
        "en": "Potato (Aalu)", "hi": "आलू", "pa": "ਆਲੂ", "bn": "আলু", "mr": "बटाटा",
        "gu": "બટાટા", "te": "బంగాళాదుంప", "ta": "உருளைக்கிழங்கு", "kn": "ಆಲೂಗಡ್ಡೆ", "ml": "ഉരുളക്കിഴങ്ങ്"
    },
    "tomato": {
        "en": "Tomato (Tamatar)", "hi": "टमाटर", "pa": "ਟਮਾਟਰ", "bn": "টমেটো", "mr": "टोमॅटो",
        "gu": "ટામેટાં", "te": "టమాటా", "ta": "தக்காளி", "kn": "ಟೊಮೆಟೊ", "ml": "തക്കാളി"
    },
    "onion": {
        "en": "Onion (Pyaz)", "hi": "प्याज़", "pa": "ਪਿਆਜ਼", "bn": "পেঁয়াজ", "mr": "कांदा",
        "gu": "ડુંગળી", "te": "ఉల్లిపాయ", "ta": "வெங்காயம்", "kn": "ಈರುಳ್ಳಿ", "ml": "സവാള"
    },
    "cauliflower": {
        "en": "Cauliflower", "hi": "फूलगोभी", "pa": "ਫੁੱਲ ਗੋਭੀ", "bn": "ফুলকপি", "mr": "फ्लॉवर",
        "gu": "ફુલાવર", "te": "క్యాలీఫ్లవర్", "ta": "காலிஃபிளவர்", "kn": "ಹೂಕೋಸು", "ml": "കോളിഫ്ലവർ"
    },
    "cabbage": {
        "en": "Cabbage", "hi": "पत्तागोभी", "pa": "ਬੰਦ ਗੋਭੀ", "bn": "বাঁধাকপি", "mr": "कोबी",
        "gu": "કોબીજ", "te": "క్యాಬೇజీ", "ta": "முட்டைக்கோஸ்", "kn": "ಎಲೆಕೋಸು", "ml": "മുട്ടക്കോസ്"
    },
    "brinjal": {
        "en": "Brinjal (Baingan)", "hi": "बैंगन", "pa": "ਬੈਂਗਣ", "bn": "বেগুন", "mr": "वांगे",
        "gu": "રીંગણ", "te": "వంకాయ", "ta": "கத்தரிக்காய்", "kn": "ಬದನೆಕಾಯಿ", "ml": "വഴുതനങ്ങ"
    },
    "okra": {
        "en": "Okra / Bhindi", "hi": "भिंडी", "pa": "ਭਿੰਡੀ", "bn": "ঢ্যাঁড়শ", "mr": "भेंडी",
        "gu": "ભીંડા", "te": "బెండకాయ", "ta": "வெண்டைக்காய்", "kn": "ಬೆಂಡೆಕಾಯಿ", "ml": "വെണ്ടയ്ക്ക"
    },
    "carrot": {
        "en": "Carrot (Gajar)", "hi": "गाजर", "pa": "ਗਾਜਰ", "bn": "গাজর", "mr": "गाजर",
        "gu": "ગાજર", "te": "క్యారెట్", "ta": "கேரட்", "kn": "ಕ್ಯಾರೆಟ್", "ml": "കാരറ്റ്"
    },
    "radish": {
        "en": "Radish (Mooli)", "hi": "मूली", "pa": "ਮੂਲੀ", "bn": "মুলো", "mr": "मुळा",
        "gu": "મૂળો", "te": "ముల్లంగి", "ta": "முள்ளங்கி", "kn": "ಮೂಲಂಗಿ", "ml": "മുള്ളങ്കി"
    },
    "spinach": {
        "en": "Spinach (Palak)", "hi": "पालक", "pa": "ਪਾਲਕ", "bn": "পালং শাক", "mr": "पालक",
        "gu": "પાલક", "te": "పాలకూర", "ta": "பசலைக்கீரை", "kn": "ಪಾಲಕ್", "ml": "ചീര"
    },
    "bottle_gourd": {
        "en": "Bottle Gourd (Lauki)", "hi": "लौकी / घिया", "pa": "ਘੀਆ / ਲੌਕੀ", "bn": "লাউ", "mr": "दुधी भोपळा",
        "gu": "દૂધી", "te": "సొరకాయ", "ta": "சுரைக்காய்", "kn": "ಸೋರೆಕಾಯಿ", "ml": "ചുരയ്ക്ക"
    },
    "bitter_gourd": {
        "en": "Bitter Gourd (Karela)", "hi": "करेला", "pa": "ਕਰੇਲਾ", "bn": "উচ্ছে / করলা", "mr": "कारले",
        "gu": "કારેલાં", "te": "కాకరకాయ", "ta": "பாகற்காய்", "kn": "ಹಾಗಲಕಾಯಿ", "ml": "പാവയ്ക്ക"
    },
    "cucumber": {
        "en": "Cucumber (Kheera)", "hi": "खीरा / ककड़ी", "pa": "ਖੀਰਾ", "bn": "শসা", "mr": "काकडी",
        "gu": "કાકડી", "te": "దోసకాయ", "ta": "வெள்ளரிக்காய்", "kn": "ಸೌತೆಕಾಯಿ", "ml": "വെള്ളരിക്ക"
    },
    "capsicum": {
        "en": "Capsicum / Bell Pepper", "hi": "शिमला मिर्च", "pa": "ਸ਼ਿਮਲਾ ਮਿਰਚ", "bn": "ক্যাপসিকাম", "mr": "ढोबळी मिरची",
        "gu": "કેપ્સિકમ / ભોપલી મરચાં", "te": "క్యాప్సికమ్", "ta": "குடைமிளகாய்", "kn": "ದಪ್ಪಮೆಣಸಿನಕಾಯಿ", "ml": "ക്യാപ്സിക്കം"
    },

    # ==============================
    # 🍎 29 FRUIT CROPS
    # ==============================
    "mango": {
        "en": "Mango", "hi": "आम", "pa": "ਅੰਬ", "bn": "আম", "mr": "आंबा",
        "gu": "કેરી", "te": "మామిడికాయ", "ta": "மாம்பழம்", "kn": "ಮಾವಿನಹಣ್ಣು", "ml": "മാങ്ങ"
    },
    "banana": {
        "en": "Banana", "hi": "केला", "pa": "ਕੇਲਾ", "bn": "কলা", "mr": "केळी",
        "gu": "કેળાં", "te": "అరటిపండు", "ta": "வாழைப்பழம்", "kn": "ಬಾಳೆಹಣ್ಣು", "ml": "വാഴപ്പഴം"
    },
    "apple": {
        "en": "Apple", "hi": "सेब", "pa": "ਸੇਬ", "bn": "আপেল", "mr": "सफरचंद",
        "gu": "સફરજન", "te": "యాపిల్", "ta": "ஆப்பிள்", "kn": "ಸೇಬು", "ml": "ആപ്പിൾ"
    },
    "orange": {
        "en": "Orange / Kinnow", "hi": "संतरा / किन्नू", "pa": "ਸੰਤਰਾ / ਕਿੰਨੂ", "bn": "কমলালেবু", "mr": "संत्रे",
        "gu": "સંતરા", "te": "నారింజ", "ta": "ஆரஞ்சு", "kn": "ಕಿತ್ತಳೆ", "ml": "ഓറഞ്ച്"
    },
    "papaya": {
        "en": "Papaya", "hi": "पपीता", "pa": "ਪਪੀਤਾ", "bn": "পেঁপে", "mr": "पपई",
        "gu": "પપૈયું", "te": "బొప్పాయి", "ta": "பப்பாளி", "kn": "ಪರಂಗಿಹಣ್ಣು", "ml": "പപ്പായ"
    },
    "pomegranate": {
        "en": "Pomegranate (Anar)", "hi": "अनार", "pa": "ਅਨਾਰ", "bn": "ডালিম / বেদানা", "mr": "डाळिंब",
        "gu": "દાડમ", "te": "దానిమ్మ", "ta": "மாதுளை", "kn": "ದಾಳಿಂಬೆ", "ml": "മാതളനാരങ്ങ"
    },
    "grapes": {
        "en": "Grapes", "hi": "अंगूर", "pa": "ਅੰਗੂਰ", "bn": "আঙুর", "mr": "द्राक्षे",
        "gu": "દ્રાક્ષ", "te": "ద్రాక్ష", "ta": "திராட்சை", "kn": "ದ್ರಾಕ್ಷಿ", "ml": "മുന്തിരി"
    },
    "guava": {
        "en": "Guava (Amrood)", "hi": "अमरूद", "pa": "ਅਮਰੂਦ", "bn": "পেয়ারা", "mr": "पेरू",
        "gu": "જામફળ", "te": "జామపండు", "ta": "கொய்யா", "kn": "ಸೀಬೆಹಣ್ಣು", "ml": "പേരയ്ക്ക"
    },
    "pineapple": {
        "en": "Pineapple (Ananas)", "hi": "अनानास", "pa": "ਅਨਾਨਾਸ", "bn": "আনারস", "mr": "अननस",
        "gu": "અનાનસ", "te": "అనాసపండు", "ta": "அன்னாசி", "kn": "ಅನಾನಸ್", "ml": "കൈതച്ചക്ക"
    },
    "lemon": {
        "en": "Lemon / Lime (Nimbu)", "hi": "नींबू", "pa": "ਨਿੰਬੂ", "bn": "লেবু", "mr": "लिंबू",
        "gu": "લીંબુ", "te": "నిమ్మకాయ", "ta": "எலுமிச்சை", "kn": "ನಿಂಬೆಹಣ್ಣು", "ml": "നാരങ്ങ"
    },
    "watermelon": {
        "en": "Watermelon (Tarbooj)", "hi": "तरबूज", "pa": "ਤਰਬੂਜ਼", "bn": "তরমুজ", "mr": "कलिंगड",
        "gu": "તરબૂચ", "te": "పుచ్చకాయ", "ta": "தர்பூசணி", "kn": "ಕಲ್ಲಂಗಡಿ", "ml": "തണ്ണിമത്തൻ"
    },
    "muskmelon": {
        "en": "Muskmelon (Kharbooja)", "hi": "खरबूजा", "pa": "ਖ਼ਰਬੂਜ਼ਾ", "bn": "ফুটি / খরমুজ", "mr": "खरबूज",
        "gu": "ટેટી / શક્કરટેટી", "te": "కర్బూజ", "ta": "முலாம் பழம்", "kn": "ಕರ್ಬೂಜ", "ml": "മധുര തണ്ണിമത്തൻ"
    },
    "coconut": {
        "en": "Coconut (Nariyal)", "hi": "नारियल", "pa": "ਨਾਰੀਅਲ", "bn": "নারকেল", "mr": "नारळ",
        "gu": "નાળિયેર", "te": "కొబ్బరికాయ", "ta": "தேங்காய்", "kn": "ತೆಂಗಿನಕಾಯಿ", "ml": "തേങ്ങ"
    },
    "litchi": {
        "en": "Litchi / Lychee", "hi": "लीची", "pa": "ਲੀਚੀ", "bn": "লিচু", "mr": "लिची",
        "gu": "લીચી", "te": "లిచీ", "ta": "லிச்சி", "kn": "ಲಿಚಿ", "ml": "ലിച്ചി"
    },
    "sapota": {
        "en": "Sapota (Chiku)", "hi": "चीकू", "pa": "ਚੀਕੂ", "bn": "সফেদা", "mr": "चिकू",
        "gu": "ચીકુ", "te": "సపోటా", "ta": "சப்போட்டா", "kn": "ಚಿಕ್ಕು", "ml": "സപ്പോട്ട"
    },
    "custard_apple": {
        "en": "Custard Apple (Sharifa)", "hi": "शरीफा / सीताफल", "pa": "ਸ਼ਰੀਫ਼ਾ", "bn": "আতা ফল", "mr": "सीताफळ",
        "gu": "સીતાફળ", "te": "సీతాఫలం", "ta": "சீத்தாப்பழம்", "kn": "ಸೀತಾಫಲ", "ml": "ആത്തച്ചക്ക"
    },
    "strawberry": {
        "en": "Strawberry", "hi": "स्ट्रॉबेरी", "pa": "ਸਟ੍ਰਾਬੇਰੀ", "bn": "স্ট্রবেরি", "mr": "स्ट्रॉबेरी",
        "gu": "સ્ટ્રોબેરી", "te": "స్ట్రాబెర్రీ", "ta": "ஸ்ட்ராபெரி", "kn": "ಸ್ಟ್ರಾಬೆರಿ", "ml": "സ്ട്രോബെറി"
    },
    "jamun": {
        "en": "Black Plum (Jamun)", "hi": "जामुन", "pa": "ਜਾਮਣ", "bn": "জাম", "mr": "जांभूळ",
        "gu": "જાંબુ", "te": "నేరేడు పండు", "ta": "நாவல் பழம்", "kn": "ನೇರಳೆ ಹಣ್ಣು", "ml": "ഞാവൽ പഴം"
    },
    "amla": {
        "en": "Indian Gooseberry (Amla)", "hi": "आंवला", "pa": "ਔਂਵਲਾ", "bn": "আমলকী", "mr": "आवळा",
        "gu": "આંબળા", "te": "ఉసిరికాయ", "ta": "நெல்லிக்காய்", "kn": "ನೆಲ್ಲಿಕಾಯಿ", "ml": "നെല്ലിക്ക"
    },
    "jackfruit": {
        "en": "Jackfruit (Kathal)", "hi": "कटहल", "pa": "ਕਠਹਲ", "bn": "কাঁঠাল", "mr": "फणस",
        "gu": "ફણસ", "te": "పనసపండు", "ta": "பலாப்பழம்", "kn": "ಹಲಸಿನ ಹಣ್ಣು", "ml": "ചക്ക"
    },
    "dragon_fruit": {
        "en": "Dragon Fruit (Kamalam)", "hi": "ड्रैगन फ्रूट / कमलम", "pa": "ਡ੍ਰੈਗਨ ਫਲ", "bn": "ড্রাগন ফল", "mr": "ड्रॅगन फ्रूट",
        "gu": "કમલમ / ડ્રેગન ફ્રૂટ", "te": "డ్రాగన్ ఫ్రూట్", "ta": "டிராகன் பழம்", "kn": "ಡ್ರ್ಯಾಗನ್ ಹಣ್ಣು", "ml": "ഡ്രാഗൺ ഫ്രൂട്ട്"
    },
    "ber": {
        "en": "Indian Jujube (Ber)", "hi": "बेर", "pa": "ਬੇਰ", "bn": "কুল / বরই", "mr": "बोर",
        "gu": "બોર", "te": "రేగుపండు", "ta": "இலந்தை பழம்", "kn": "ಬೋರೆ ಹಣ್ಣು", "ml": "ഇലന്തപ്പഴം"
    },
    "fig": {
        "en": "Fig (Anjeer)", "hi": "अंजीर", "pa": "ਅੰਜੀਰ", "bn": "ডুমুর / আঞ্জির", "mr": "अंजीर",
        "gu": "અંજીર", "te": "అంజీర", "ta": "அத்திப்பழம்", "kn": "ಅಂಜೂರ", "ml": "അത്തിപ്പഴം"
    },
    "peach": {
        "en": "Peach (Aadu)", "hi": "आड़ू", "pa": "ਆੜੂ", "bn": "পীচ ফল", "mr": "पीच",
        "gu": "પીચ / આડુ", "te": "పీచ్", "ta": "பீச் பழம்", "kn": "ಪೀಚ್", "ml": "പീച്ച്"
    },
    "plum": {
        "en": "Plum (Alobukhara)", "hi": "आलू बुखारा", "pa": "ਆਲੂਬੁਖਾਰਾ", "bn": "আলুবোখারা", "mr": "आलूबुखारा",
        "gu": "આલુ બુખારા", "te": "ప్లమ్", "ta": "பிளம் பழம்", "kn": "ಪ್ಲಮ್", "ml": "പ്ലം"
    },
    "apricot": {
        "en": "Apricot (Khurmani)", "hi": "खुबानी", "pa": "ਖੁਰਮਾਨੀ", "bn": "খুবানি", "mr": "जर्दाळू",
        "gu": "જરદાળુ", "te": "జల్దరు పండు", "ta": "சர்க்கரை பாதாமி", "kn": "ಜರ್ದಾಳು", "ml": "ആപ്രിക്കോട്ട്"
    },
    "pear": {
        "en": "Pear (Nashpati)", "hi": "नाशपाती", "pa": "ਨਾਸ਼ਪਾਤੀ", "bn": "নাশপাতি", "mr": "नाशपाती",
        "gu": "નાસપતિ", "te": "బేరిపండు", "ta": "பேரிக்காய்", "kn": "ಪೇರಳೆ ಹಣ್ಣು", "ml": "സബർജിൽ"
    },
    "walnut": {
        "en": "Walnut (Akhrot)", "hi": "अखरोट", "pa": "ਅਖਰੋਟ", "bn": "আখরোট", "mr": "अक्रोड",
        "gu": "અખરોટ", "te": "అక్రోట్", "ta": "அக்ரூட்", "kn": "ಅಕ್ರೋಟ", "ml": "വാൽനട്ട്"
    },
    "almond": {
        "en": "Almond (Badam)", "hi": "बादाम", "pa": "ਬਦਾਮ", "bn": "বাদাম", "mr": "बदाम",
        "gu": "બદામ", "te": "బాదం", "ta": "பாதாம்", "kn": "ಬಾದಾಮಿ", "ml": "ബദാം"
    }
}

ADDITIONAL_ALIASES = {
    "chiku": "sapota",
    "sitaphal": "custard_apple",
    "sharifa": "custard_apple",
    "amrood": "guava",
    "anar": "pomegranate",
    "tarbooj": "watermelon",
    "kharbooja": "muskmelon",
    "nimbu": "lemon",
    "lauki": "bottle_gourd",
    "karela": "bitter_gourd",
    "kheera": "cucumber",
    "shimla_mirch": "capsicum",
    "baingan": "brinjal",
    "bhindi": "okra",
    "gajar": "carrot",
    "mooli": "radish",
    "palak": "spinach",
    "anjeer": "fig",
    "khurmani": "apricot",
    "nashpati": "pear",
    "akhrot": "walnut",
    "badam": "almond",
    "aam": "mango",
    "kela": "banana",
    "seb": "apple",
    "santra": "orange",
    "kinnow": "orange",
    "papita": "papaya",
    "angoor": "grapes",
    "kathal": "jackfruit",
    "nariyal": "coconut",
    "alsi": "linseed",
    "til": "sesame",
    "kusum": "safflower",
    "arandi": "castor",
    "moongphali": "groundnut",
    "chana": "chickpea",
    "arhar": "pigeonpeas",
    "tur": "pigeonpeas",
    "moong": "mungbean",
    "urad": "blackgram",
    "masoor": "lentil",
    "rajma": "kidneybeans",
    "matki": "mothbeans",
    "moth": "mothbeans",
    "lobia": "cowpea",
    "matar": "green_peas",
    "kulthi": "horsegram",
    "jau": "barley",
    "kangni": "foxtail_millet",
    "kodra": "kodo_millet",
    "kutki": "little_millet",
    "sanwa": "barnyard_millet",
    "cheena": "proso_millet",
    "sarson": "mustard",
    "rai": "mustard"
}

def update_translations_js():
    with open("static/js/translations.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Format CROP_DICT_90 as Javascript object string
    lines = ["const CROP_TRANSLATIONS = {"]
    for crop_id, t_dict in CROP_DICT_90.items():
        lines.append(f'  "{crop_id}": {{')
        items = []
        for l_code, l_val in t_dict.items():
            items.append(f'    "{l_code}": "{l_val}"')
        lines.append(",\n".join(items))
        lines.append("  },")
    
    # Also add generic categories
    lines.append('  "vegetables": {')
    lines.append('    "en": "Vegetables", "hi": "सब्जियां", "pa": "ਸਬਜ਼ੀਆਂ", "bn": "শাকসবজি", "mr": "भाज्या", "gu": "શાકભાજી", "te": "కూరగాయలు", "ta": "காய்கறிகள்", "kn": "ತರಕಾರಿಗಳು", "ml": "പച്ചക്കറികൾ"')
    lines.append('  },')
    lines.append('  "fruits": {')
    lines.append('    "en": "Fruits", "hi": "फल", "pa": "ਫਲ", "bn": "ফলমূল", "mr": "फळे", "gu": "ફળો", "te": "పండ్లు", "ta": "பழங்கள்", "kn": "ಹಣ್ಣುಗಳು", "ml": "പഴങ്ങൾ"')
    lines.append('  },')
    lines.append('  "pulses": {')
    lines.append('    "en": "Pulses", "hi": "दालें", "pa": "ਦਾਲਾਂ", "bn": "ডাল", "mr": "डाळी", "gu": "કઠોળ / દાળ", "te": "పప్పుధాన్యాలు", "ta": "பருப்பு வகைகள்", "kn": "ಬೇಳೆಕಾಳುಗಳು", "ml": "പയർവർഗ്ഗങ്ങൾ"')
    lines.append('  },')
    lines.append('  "general": {')
    lines.append('    "en": "General Farming", "hi": "सामान्य खेती", "pa": "ਆਮ ਖੇਤੀ", "bn": "সাধারণ চাষাবাদ", "mr": "सामान्य शेती", "gu": "સામાન્ય ખેતી", "te": "సాధారణ వ్యవసాయం", "ta": "பொது விவசாயம்", "kn": "ಸಾಮಾನ್ಯ ಕೃಷಿ", "ml": "പൊതു കൃഷി"')
    lines.append('  }')
    lines.append("};")
    new_crop_translations_str = "\n".join(lines)

    # Replace CROP_TRANSLATIONS in content
    # Find start and end of CROP_TRANSLATIONS
    crop_start = content.find("const CROP_TRANSLATIONS = {")
    crop_end = content.find("const CROP_ALIASES = {")
    if crop_start != -1 and crop_end != -1:
        content = content[:crop_start] + new_crop_translations_str + "\n\n" + content[crop_end:]
        print("Updated CROP_TRANSLATIONS successfully!")
    else:
        print("Could not find boundaries for CROP_TRANSLATIONS!")

    # Now update CROP_ALIASES
    alias_start = content.find("const CROP_ALIASES = {")
    alias_end = content.find("const CATEGORY_TRANSLATIONS = {")
    if alias_start != -1 and alias_end != -1:
        alias_lines = ["const CROP_ALIASES = {"]
        for k, v in ADDITIONAL_ALIASES.items():
            alias_lines.append(f'  "{k}": "{v}",')
        alias_lines.append("};")
        content = content[:alias_start] + "\n".join(alias_lines) + "\n\n" + content[alias_end:]
        print("Updated CROP_ALIASES successfully!")

    # Write back
    with open("static/js/translations.js", "w", encoding="utf-8") as f:
        f.write(content)

    print("static/js/translations.js written successfully!")

if __name__ == "__main__":
    update_translations_js()
