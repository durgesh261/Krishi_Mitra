import re

file_path = 'static/js/translations.js'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

NEW_KEYS = {
    'en': {
        'nav_signin': 'Sign In',
        'nav_mandi': 'Mandi Prices & MSP',
        'nav_mandi_direct': 'Mandi Bhav',
        'tab_login': 'Login',
        'tab_signup': 'Create Account',
        'login_welcome': 'Welcome Back',
        'login_sub': 'Login to access Krishi Mitra',
        'signup_welcome': 'Create Account',
        'signup_sub': 'Join Krishi Mitra today'
    },
    'hi': {
        'nav_signin': 'साइन इन',
        'nav_mandi': 'मंडी भाव और MSP',
        'nav_mandi_direct': 'मंडी भाव',
        'tab_login': 'लॉगिन',
        'tab_signup': 'खाता बनाएं',
        'login_welcome': 'पुनः स्वागत है',
        'login_sub': 'कृषि मित्र में लॉगिन करें',
        'signup_welcome': 'नया खाता बनाएं',
        'signup_sub': 'आज ही कृषि मित्र से जुड़ें'
    },
    'pa': {
        'nav_signin': 'ਸਾਈਨ ਇਨ',
        'nav_mandi': 'ਮੰਡੀ ਭਾਅ ਅਤੇ MSP',
        'nav_mandi_direct': 'ਮੰਡੀ ਭਾਅ',
        'tab_login': 'ਲਾਗਇਨ',
        'tab_signup': 'ਖਾਤਾ ਬਣਾਓ',
        'login_welcome': 'ਜੀ ਆਇਆਂ ਨੂੰ',
        'login_sub': 'ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਵਿੱਚ ਲਾਗਇਨ ਕਰੋ',
        'signup_welcome': 'ਨਵਾਂ ਖਾਤਾ ਬਣਾਓ',
        'signup_sub': 'ਅੱਜ ਹੀ ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਨਾਲ ਜੁੜੋ'
    },
    'bn': {
        'nav_signin': 'সাইন ইন',
        'nav_mandi': 'মান্ডি দর ও MSP',
        'nav_mandi_direct': 'মান্ডি দর',
        'tab_login': 'লগইন',
        'tab_signup': 'অ্যাকাউন্ট তৈরি করুন',
        'login_welcome': 'স্বাগতম',
        'login_sub': 'কৃষি মিত্রে লগইন করুন',
        'signup_welcome': 'নতুন অ্যাকাউন্ট তৈরি করুন',
        'signup_sub': 'আজই কৃষি মিত্রের সাথে যুক্ত হন'
    },
    'mr': {
        'nav_signin': 'साइन इन',
        'nav_mandi': 'बाजारभाव व हमीभाव (MSP)',
        'nav_mandi_direct': 'बाजारभाव',
        'tab_login': 'लॉगिन',
        'tab_signup': 'खाते तयार करा',
        'login_welcome': 'पुन्हा स्वागत आहे',
        'login_sub': 'कृषी मित्रमध्ये लॉगिन करा',
        'signup_welcome': 'नवीन खाते तयार करा',
        'signup_sub': 'आजच कृषी मित्रशी जोडा'
    },
    'gu': {
        'nav_signin': 'સાઇન ઇન',
        'nav_mandi': 'માર્કેટ યાર્ડ ભાવ & MSP',
        'nav_mandi_direct': 'માર્કેટ ભાવ',
        'tab_login': 'લૉગિન',
        'tab_signup': 'ખાતું બનાવો',
        'login_welcome': 'સ્વાગત છે',
        'login_sub': 'કૃષિ મિત્રમાં લૉગિન કરો',
        'signup_welcome': 'નવું ખાતું બનાવો',
        'signup_sub': 'આજે જ કૃષિ મિત્ર સાથે જોડાઓ'
    },
    'te': {
        'nav_signin': 'సైన్ ఇన్',
        'nav_mandi': 'మార్కెట్ ధరలు & MSP',
        'nav_mandi_direct': 'మార్కెట్ ధరలు',
        'tab_login': 'లాగిన్',
        'tab_signup': 'ఖాతాను సృష్టించండి',
        'login_welcome': 'తిరిగి స్వాగతం',
        'login_sub': 'కృషి మిత్రలోకి లాగిన్ అవ్వండి',
        'signup_welcome': 'కొత్త ఖాతాను సృష్టించండి',
        'signup_sub': 'ఈరోజే కృషి మిత్రతో చేరండి'
    },
    'ta': {
        'nav_signin': 'உள்நுழைக',
        'nav_mandi': 'மண்டி விலை & MSP',
        'nav_mandi_direct': 'மண்டி விலை',
        'tab_login': 'உள்நுழை',
        'tab_signup': 'கணக்கை உருவாக்கு',
        'login_welcome': 'மீண்டும் வருக',
        'login_sub': 'கிருஷி மித்ராவில் உள்நுழையவும்',
        'signup_welcome': 'புதிய கணக்கை உருவாக்கவும்',
        'signup_sub': 'இன்றே கிருஷி மித்ராவுடன் இணையுங்கள்'
    },
    'kn': {
        'nav_signin': 'ಸೈನ್ ಇನ್',
        'nav_mandi': 'ಮಂಡಿ ಬೆಲೆಗಳು & MSP',
        'nav_mandi_direct': 'ಮಂಡಿ ಬೆಲೆ',
        'tab_login': 'ಲಾಗಿನ್',
        'tab_signup': 'ಖಾತೆ ರಚಿಸಿ',
        'login_welcome': 'ಮತ್ತೆ ಸ್ವಾಗತ',
        'login_sub': 'ಕೃಷಿ ಮಿತ್ರಗೆ ಲಾಗಿನ್ ಮಾಡಿ',
        'signup_welcome': 'ಹೊಸ ಖಾತೆ ರಚಿಸಿ',
        'signup_sub': 'ಇಂದೇ ಕೃಷಿ ಮಿತ್ರ ಜೊತೆ ಸೇರಿಕೊಳ್ಳಿ'
    },
    'ml': {
        'nav_signin': 'സൈൻ ഇൻ',
        'nav_mandi': 'വിപണി വിലകളും MSP യും',
        'nav_mandi_direct': 'വിപണി വില',
        'tab_login': 'ലോഗിൻ',
        'tab_signup': 'അക്കൗണ്ട് സൃഷ്ടിക്കുക',
        'login_welcome': 'സ്വാഗതം',
        'login_sub': 'കൃഷി മിത്രയിലേക്ക് ലോഗിൻ ചെയ്യുക',
        'signup_welcome': 'പുതിയ അക്കൗണ്ട് സൃഷ്ടിക്കുക',
        'signup_sub': 'ഇന്ന് തന്നെ കൃഷി മിത്രയോടൊപ്പം ചേരൂ'
    }
}

for lang, keys in NEW_KEYS.items():
    # Find the language block
    pattern = rf'({lang}:\s*\{{\s*\n)'
    extra_lines = ""
    for k, v in keys.items():
        escaped_v = v.replace('"', '\\"')
        extra_lines += f'    {k}: "{escaped_v}",\n'
    content = re.sub(pattern, rf'\1{extra_lines}', content, count=1)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("[OK] Successfully injected all 10 language translations!")
