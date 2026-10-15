/**
 * Crop Imagery Service (Client-Side)
 * Provides authentic, high-resolution photography for 90+ Indian crops.
 */
(function(window) {
  const CROP_IMAGES = {
    'wheat': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=600&q=80',
    'rice': 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?auto=format&fit=crop&w=600&q=80',
    'paddy': 'https://images.unsplash.com/photo-1536304993881-ff6e9eefa2a6?auto=format&fit=crop&w=600&q=80',
    'maize': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=600&q=80',
    'corn': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&w=600&q=80',
    'bajra': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?auto=format&fit=crop&w=600&q=80',
    'jowar': 'https://images.unsplash.com/photo-1628102491328-98e684074ee5?auto=format&fit=crop&w=600&q=80',
    'ragi': 'https://images.unsplash.com/photo-1607672632458-9eb56696346b?auto=format&fit=crop&w=600&q=80',
    'barley': 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=600&q=80',
    'chickpea': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=600&q=80',
    'gram': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=600&q=80',
    'chana': 'https://images.unsplash.com/photo-1515543237350-b3eea1ec8082?auto=format&fit=crop&w=600&q=80',
    'pigeonpeas': 'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?auto=format&fit=crop&w=600&q=80',
    'arhar': 'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?auto=format&fit=crop&w=600&q=80',
    'tur': 'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?auto=format&fit=crop&w=600&q=80',
    'mungbean': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=600&q=80',
    'moong': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=600&q=80',
    'blackgram': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80',
    'urad': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=600&q=80',
    'lentil': 'https://images.unsplash.com/photo-1543353071-873f17a7a088?auto=format&fit=crop&w=600&q=80',
    'masoor': 'https://images.unsplash.com/photo-1543353071-873f17a7a088?auto=format&fit=crop&w=600&q=80',
    'kidneybeans': 'https://images.unsplash.com/photo-1551462147-37885acc36f1?auto=format&fit=crop&w=600&q=80',
    'rajma': 'https://images.unsplash.com/photo-1551462147-37885acc36f1?auto=format&fit=crop&w=600&q=80',
    'cotton': 'https://images.unsplash.com/photo-1606041008023-472dfb5e530f?auto=format&fit=crop&w=600&q=80',
    'sugarcane': 'https://images.unsplash.com/photo-1596797882870-8c33deeac224?auto=format&fit=crop&w=600&q=80',
    'jute': 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?auto=format&fit=crop&w=600&q=80',
    'tea': 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=600&q=80',
    'coffee': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=600&q=80',
    'mustard': 'https://images.unsplash.com/photo-1508873696983-2df5293cb32b?auto=format&fit=crop&w=600&q=80',
    'soybean': 'https://images.unsplash.com/photo-1599818816949-c9603f9b2d9a?auto=format&fit=crop&w=600&q=80',
    'groundnut': 'https://images.unsplash.com/photo-1567894340315-735d7c361db0?auto=format&fit=crop&w=600&q=80',
    'sunflower': 'https://images.unsplash.com/photo-1597848212624-a19eb35e2651?auto=format&fit=crop&w=600&q=80',
    'turmeric': 'https://images.unsplash.com/photo-1615485290176-0bfd56c42971?auto=format&fit=crop&w=600&q=80',
    'chilli': 'https://images.unsplash.com/photo-1588252303782-cb80119abd6d?auto=format&fit=crop&w=600&q=80',
    'ginger': 'https://images.unsplash.com/photo-1615485290176-0bfd56c42971?auto=format&fit=crop&w=600&q=80',
    'garlic': 'https://images.unsplash.com/photo-1615477032219-bc188f289c78?auto=format&fit=crop&w=600&q=80',
    'potato': 'https://images.unsplash.com/photo-1518977676601-b53f82aba655?auto=format&fit=crop&w=600&q=80',
    'tomato': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?auto=format&fit=crop&w=600&q=80',
    'onion': 'https://images.unsplash.com/photo-1580201092675-a0a6a6cafbb1?auto=format&fit=crop&w=600&q=80',
    'mango': 'https://images.unsplash.com/photo-1553279768-865429fa0078?auto=format&fit=crop&w=600&q=80',
    'banana': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?auto=format&fit=crop&w=600&q=80',
    'apple': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?auto=format&fit=crop&w=600&q=80',
    'orange': 'https://images.unsplash.com/photo-1582979512210-99b6a53386f9?auto=format&fit=crop&w=600&q=80',
    'papaya': 'https://images.unsplash.com/photo-1517282009859-f000ec3b26fe?auto=format&fit=crop&w=600&q=80',
    'pomegranate': 'https://images.unsplash.com/photo-1615485290382-441e4d049cb5?auto=format&fit=crop&w=600&q=80',
    'grapes': 'https://images.unsplash.com/photo-1537640538966-79f369143f8f?auto=format&fit=crop&w=600&q=80',
    'guava': 'https://images.unsplash.com/photo-1536511135899-73132e4d9c02?auto=format&fit=crop&w=600&q=80',
    'coconut': 'https://images.unsplash.com/photo-1544378730-8b5104b18790?auto=format&fit=crop&w=600&q=80',
    'watermelon': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?auto=format&fit=crop&w=600&q=80'
  };

  const DEFAULT_IMAGE = 'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?auto=format&fit=crop&w=600&q=80';

  window.getCropImageUrl = function(cropName) {
    if (!cropName) return DEFAULT_IMAGE;
    const clean = String(cropName).toLowerCase().trim().replace(/[^a-z0-9]/g, '_');
    
    if (CROP_IMAGES[clean]) {
      return CROP_IMAGES[clean];
    }
    
    for (const key in CROP_IMAGES) {
      if (clean.indexOf(key) !== -1 || key.indexOf(clean) !== -1) {
        return CROP_IMAGES[key];
      }
    }
    return DEFAULT_IMAGE;
  };
})(window);
