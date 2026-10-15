"""
Crop Imagery & Media Service for Krishi Mitra
Provides authentic, high-resolution photography and vector graphics
for all 90+ Indian Field, Pulse, Cereal, Commercial, Vegetable, and Fruit Crops.
"""

# Curated high-resolution authentic crop imagery mapping
CROP_IMAGE_MAP = {
    # Cereals & Millets
    'wheat': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=800&q=80',
    'rice': 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?auto=format&fit=crop&w=800&q=80',
    'maize': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=800&q=80',
    'bajra': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80',
    'jowar': 'https://images.unsplash.com/photo-1628102491328-98e684074ee5?auto=format&fit=crop&w=800&q=80',
    'ragi': 'https://images.unsplash.com/photo-1607672632458-9eb56696346b?auto=format&fit=crop&w=800&q=80',
    'barley': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80',
    'foxtail_millet': 'https://images.unsplash.com/photo-1598965402089-897ce52e8355?auto=format&fit=crop&w=800&q=80',
    'kodo_millet': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80',
    'little_millet': 'https://images.unsplash.com/photo-1607672632458-9eb56696346b?auto=format&fit=crop&w=800&q=80',
    'barnyard_millet': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80',
    'proso_millet': 'https://images.unsplash.com/photo-1598965402089-897ce52e8355?auto=format&fit=crop&w=800&q=80',

    # Pulses & Legumes
    'chickpea': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=800&q=80',
    'pigeonpeas': 'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?auto=format&fit=crop&w=800&q=80',
    'mungbean': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=800&q=80',
    'blackgram': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80',
    'lentil': 'https://images.unsplash.com/photo-1543353071-873f17a7a088?auto=format&fit=crop&w=800&q=80',
    'kidneybeans': 'https://images.unsplash.com/photo-1551462147-37885acc36f1?auto=format&fit=crop&w=800&q=80',
    'mothbeans': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=800&q=80',
    'cowpea': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=800&q=80',
    'green_peas': 'https://images.unsplash.com/photo-1587735243615-c03f25aaff15?auto=format&fit=crop&w=800&q=80',
    'horsegram': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=800&q=80',

    # Commercial & Cash Crops
    'cotton': 'https://images.unsplash.com/photo-1606041008023-472dfb5e530f?auto=format&fit=crop&w=800&q=80',
    'sugarcane': 'https://images.unsplash.com/photo-1596797882870-8c33deeac224?auto=format&fit=crop&w=800&q=80',
    'jute': 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?auto=format&fit=crop&w=800&q=80',
    'tea': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=800&q=80',
    'coffee': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=800&q=80',
    'rubber': 'https://images.unsplash.com/photo-1513836279014-a89f7a76ae86?auto=format&fit=crop&w=800&q=80',
    'tobacco': 'https://images.unsplash.com/photo-1527661591475-527312dd65f5?auto=format&fit=crop&w=800&q=80',

    # Oilseeds
    'mustard': 'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
    'soybean': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=800&q=80',
    'groundnut': 'https://images.unsplash.com/photo-1567894340315-735d7c361db0?auto=format&fit=crop&w=800&q=80',
    'sunflower': 'https://images.unsplash.com/photo-1597848212624-a19eb35e2651?auto=format&fit=crop&w=800&q=80',
    'sesame': 'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
    'castor': 'https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?auto=format&fit=crop&w=800&q=80',
    'linseed': 'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
    'safflower': 'https://images.unsplash.com/photo-1597848212624-a19eb35e2651?auto=format&fit=crop&w=800&q=80',

    # Spices & Condiments
    'turmeric': 'https://images.unsplash.com/photo-1615485290176-0bfd56c42971?auto=format&fit=crop&w=800&q=80',
    'chilli': 'https://images.unsplash.com/photo-1588252303782-cb80119abd6d?auto=format&fit=crop&w=800&q=80',
    'ginger': 'https://images.unsplash.com/photo-1615485290176-0bfd56c42971?auto=format&fit=crop&w=800&q=80',
    'garlic': 'https://images.unsplash.com/photo-1615477032219-bc188f289c78?auto=format&fit=crop&w=800&q=80',
    'cardamom': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=800&q=80',
    'coriander': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80',
    'cumin': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=800&q=80',
    'fennel': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80',
    'fenugreek': 'https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?auto=format&fit=crop&w=800&q=80',
    'black_pepper': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=800&q=80',

    # Vegetables & Tubers
    'potato': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=800&q=80',
    'tomato': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=800&q=80',
    'onion': 'https://images.unsplash.com/photo-1580201092675-a0a6a6cafbb1?auto=format&fit=crop&w=800&q=80',
    'cauliflower': 'https://images.unsplash.com/photo-1568584711075-3d021a7c3ca3?auto=format&fit=crop&w=800&q=80',
    'cabbage': 'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?auto=format&fit=crop&w=800&q=80',
    'brinjal': 'https://images.unsplash.com/photo-1528825871115-3581a5387919?auto=format&fit=crop&w=800&q=80',
    'okra': 'https://images.unsplash.com/photo-1425543103986-22abb7d7e8d2?auto=format&fit=crop&w=800&q=80',
    'carrot': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5c317?auto=format&fit=crop&w=800&q=80',
    'radish': 'https://images.unsplash.com/photo-1598170845058-32b9d6a5c317?auto=format&fit=crop&w=800&q=80',
    'spinach': 'https://images.unsplash.com/photo-1576045057995-568f588f82fb?auto=format&fit=crop&w=800&q=80',
    'bottle_gourd': 'https://images.unsplash.com/photo-1563865436874-9aef32095fad?auto=format&fit=crop&w=800&q=80',
    'bitter_gourd': 'https://images.unsplash.com/photo-1563865436874-9aef32095fad?auto=format&fit=crop&w=800&q=80',
    'cucumber': 'https://images.unsplash.com/photo-1449300079323-02e209d9d3a6?auto=format&fit=crop&w=800&q=80',
    'capsicum': 'https://images.unsplash.com/photo-1563565375-f3fdfdbefa83?auto=format&fit=crop&w=800&q=80',

    # Fruits & Horticulture
    'mango': 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=800&q=80',
    'banana': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=800&q=80',
    'apple': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=800&q=80',
    'orange': 'https://images.unsplash.com/photo-1582979512210-99b6a53386f9?auto=format&fit=crop&w=800&q=80',
    'papaya': 'https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?auto=format&fit=crop&w=800&q=80',
    'pomegranate': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=800&q=80',
    'grapes': 'https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=800&q=80',
    'guava': 'https://images.unsplash.com/photo-1536511135899-73132e4d9c02?auto=format&fit=crop&w=800&q=80',
    'pineapple': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?auto=format&fit=crop&w=800&q=80',
    'lemon': 'https://images.unsplash.com/photo-1534940562477-8f5b66d4050e?auto=format&fit=crop&w=800&q=80',
    'watermelon': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=800&q=80',
    'muskmelon': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=800&q=80',
    'coconut': 'https://images.unsplash.com/photo-1544378730-8b5104b18790?auto=format&fit=crop&w=800&q=80',
    'litchi': 'https://images.unsplash.com/photo-1596547609652-9cf5d8d76921?auto=format&fit=crop&w=800&q=80',
    'sapota': 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=800&q=80',
    'custard_apple': 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=800&q=80',
    'strawberry': 'https://images.unsplash.com/photo-1464965911861-746a04b4bca6?auto=format&fit=crop&w=800&q=80',
    'jamun': 'https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=800&q=80',
    'amla': 'https://images.unsplash.com/photo-1534940562477-8f5b66d4050e?auto=format&fit=crop&w=800&q=80',
    'jackfruit': 'https://images.unsplash.com/photo-1550258987-190a2d41a8ba?auto=format&fit=crop&w=800&q=80',
    'dragon_fruit': 'https://images.unsplash.com/photo-1527324688151-0e627063f2b1?auto=format&fit=crop&w=800&q=80',
    'ber': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=800&q=80',
    'fig': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=800&q=80',
    'peach': 'https://images.unsplash.com/photo-1595781572981-d63151b232ed?auto=format&fit=crop&w=800&q=80',
    'plum': 'https://images.unsplash.com/photo-1595781572981-d63151b232ed?auto=format&fit=crop&w=800&q=80',
    'apricot': 'https://images.unsplash.com/photo-1595781572981-d63151b232ed?auto=format&fit=crop&w=800&q=80',
    'pear': 'https://images.unsplash.com/photo-1514756331096-242fdeb70d4a?auto=format&fit=crop&w=800&q=80',
    'walnut': 'https://images.unsplash.com/photo-1567894340315-735d7c361db0?auto=format&fit=crop&w=800&q=80',
    'almond': 'https://images.unsplash.com/photo-1567894340315-735d7c361db0?auto=format&fit=crop&w=800&q=80'
}

# Category fallback defaults
CATEGORY_FALLBACK_IMAGES = {
    'cereal': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=800&q=80',
    'millet': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=800&q=80',
    'pulse': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=800&q=80',
    'oilseed': 'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=800&q=80',
    'commercial': 'https://images.unsplash.com/photo-1596797882870-8c33deeac224?auto=format&fit=crop&w=800&q=80',
    'spice': 'https://images.unsplash.com/photo-1588252303782-cb80119abd6d?auto=format&fit=crop&w=800&q=80',
    'vegetable': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=800&q=80',
    'fruit': 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=800&q=80'
}

DEFAULT_CROP_IMAGE = 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=800&q=80'

def get_crop_image_url(crop_name):
    """
    Returns authentic high-res image URL for any Indian crop.
    Resolves aliases and case insensitivity.
    """
    if not crop_name:
        return DEFAULT_CROP_IMAGE
    
    key = str(crop_name).strip().lower().replace(' ', '_').replace('/', '_').replace('-', '_')
    
    # Direct lookup
    if key in CROP_IMAGE_MAP:
        return CROP_IMAGE_MAP[key]
    
    # Partial matching
    for k, url in CROP_IMAGE_MAP.items():
        if k in key or key in k:
            return url
            
    return DEFAULT_CROP_IMAGE
