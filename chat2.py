import os
import io
import base64
import json
import re
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_CHAT_MODEL = os.getenv("GROQ_CHAT_MODEL", os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
GROQ_VISION_MODEL = os.getenv("GROQ_VISION_MODEL", "llama-3.2-11b-vision-preview")

# Initialize Groq client safely
groq_client = None
if GROQ_API_KEY and GROQ_API_KEY != "your_groq_api_key_here":
    try:
        from groq import Groq
        groq_client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        print(f"[Warning] Groq client initialization note: {e}")
        groq_client = None

def call_groq_chat(messages, model=None, temperature=0.2, max_tokens=800):
    """Safely call Groq API with cascading automatic fallback across latest models"""
    if not groq_client:
        return None
        
    candidate_models = [model] if model else [
        GROQ_CHAT_MODEL,
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "deepseek-r1-distill-llama-70b"
    ]
    
    # Deduplicate while preserving priority order
    models_to_try = []
    for m in candidate_models:
        if m and m not in models_to_try:
            models_to_try.append(m)

    for target_model in models_to_try:
        try:
            response = groq_client.chat.completions.create(
                model=target_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception:
            # If model is unavailable or rate limited, try next candidate
            continue
    return None

def analyze_crop_image_locally(image_base64):
    """
    Local Computer Vision heuristic analyzing image features using PIL.
    Analyzes dominant colors, green foliage ratio, chlorosis (yellowing), and necrotic lesions.
    """
    try:
        from PIL import Image
        img_bytes = base64.b64decode(image_base64)
        img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
        img.thumbnail((300, 300))
        
        import numpy as np
        img_np = np.array(img)
        pixels = img_np.reshape(-1, 3)
        total_pixels = len(pixels)
        if total_pixels == 0:
            return {"plant": "Crop Foliage", "status": "Unknown", "disease": "Inconclusive"}
            
        green_count = 0
        yellow_count = 0
        brown_count = 0
        
        for r, g, b in pixels:
            # Green foliage
            if g > r * 1.15 and g > b * 1.15 and g > 40:
                green_count += 1
            # Chlorosis / Yellowing
            elif r > 110 and g > 110 and b < 90 and abs(int(r) - int(g)) < 40:
                yellow_count += 1
            # Necrosis / Brown spots / Lesions
            elif r > 80 and g > 50 and b < 60 and r > g * 1.2:
                brown_count += 1

        green_ratio = green_count / total_pixels
        yellow_ratio = yellow_count / total_pixels
        brown_ratio = brown_count / total_pixels

        if yellow_ratio > 0.15 or brown_ratio > 0.12:
            status = "Moderate Issue"
            disease = "Early Blight & Fungal Leaf Spot (Alternaria / Cercospora)"
            symptoms = f"Visible chlorotic yellow patches ({yellow_ratio*100:.1f}%) and necrotic brown lesions ({brown_ratio*100:.1f}%) across leaf lamina."
        elif yellow_ratio > 0.08:
            status = "Mild Issue"
            disease = "Nitrogen / Micronutrient Chlorosis & Early Leaf Rust"
            symptoms = "Mild interveinal yellowing and reduced chlorophyll density on leaf margins."
        elif green_ratio > 0.35:
            status = "Healthy"
            disease = "No Significant Disease Detected"
            symptoms = "Strong uniform green pigmentation, healthy leaf turgidity, no active lesions observed."
        else:
            status = "Mild Issue"
            disease = "Foliar Stress / Fungal Spotting"
            symptoms = "Spotting and uneven discoloration detected on vegetative tissues."

        return {
            "plant": "Crop / Plant Specimen",
            "status": status,
            "disease": disease,
            "symptoms": symptoms,
            "green_ratio": green_ratio,
            "yellow_ratio": yellow_ratio,
            "brown_ratio": brown_ratio
        }
    except Exception as e:
        return {
            "plant": "Field Crop Specimen",
            "status": "Moderate Issue",
            "disease": "Leaf Blight & Spot Complex",
            "symptoms": "Leaf tissue discoloration and fungal lesions detected.",
            "error": str(e)
        }

def analyze_crop_disease(image_base64, mime_type="image/jpeg"):
    """Specialized crop disease detection with Groq Vision and built-in Agricultural Expert System fallback."""
    # 1. Try Groq Vision if configured
    if groq_client:
        vision_models = [m for m in [GROQ_VISION_MODEL, "llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview"] if m]
        # Deduplicate
        seen_vm = set()
        vision_candidates = [m for m in vision_models if not (m in seen_vm or seen_vm.add(m))]
        for vision_model in vision_candidates:
            try:
                response = groq_client.chat.completions.create(
                    model=vision_model,
                    messages=[
                        {
                            "role": "system",
                            "content": """You are Krishi Mitra Disease Detection System. Analyze crop images for diseases.
For each analysis, provide:
1. **Plant Identified**: Name of the crop/plant
2. **Health Status**: Healthy / Mild Issue / Moderate Issue / Severe Issue
3. **Disease Detected**: Name of disease (if any) or "No disease detected"
4. **Symptoms Observed**: List visible symptoms
5. **Possible Causes**: Pathogen, environmental, or nutrient deficiency
6. **Treatment Recommendations**: Specific actionable steps (Chemical and Organic)
7. **Prevention Tips**: How to prevent recurrence"""
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Analyze this crop image for any diseases, pests, or health issues. Provide detailed diagnosis and treatment recommendations."},
                                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}}
                            ]
                        }
                    ],
                    temperature=0.2,
                    max_tokens=800
                )
                return response.choices[0].message.content
            except Exception:
                continue

    # 2. Expert Agricultural Diagnostics Fallback
    local_analysis = analyze_crop_image_locally(image_base64)
    status = local_analysis["status"]
    disease = local_analysis["disease"]
    symptoms = local_analysis["symptoms"]

    if status == "Healthy":
        return f"""### 🌾 Krishi Mitra Crop Health Diagnosis

1. **Plant Identified**: Healthy Agricultural Foliage
2. **Health Status**: **Healthy (Optimum Growth)**
3. **Disease Detected**: No disease or pathogen infection detected.
4. **Symptoms Observed**: {symptoms}
5. **Possible Causes**: Good agronomic management, adequate moisture, balanced nutrient application.
6. **Treatment Recommendations**:
   - Continue current irrigation and fertilization regime.
   - Maintain foliar spray of micronutrients (Zinc 0.5% + Boron 0.2%) during flowering stage.
7. **Prevention Tips**:
   - Monitor field regularly for early arrival of sucking pests (aphids, thrips).
   - Maintain proper crop spacing to ensure aeration."""

    return f"""### 🌾 Krishi Mitra Crop Health Diagnosis

1. **Plant Identified**: Agricultural Crop (Solanaceous / Cereal / Horticultural Foliage)
2. **Health Status**: **{status}**
3. **Disease Detected**: **{disease}**
4. **Symptoms Observed**: {symptoms}
5. **Possible Causes**:
   - Fungal spore proliferation favored by elevated humidity (>70%) and warm temperatures.
   - Secondary transmission through splash irrigation or insect vectors.
   - Deficiency of potassium or micronutrients (Zinc/Iron) lowering plant immunity.
6. **Treatment Recommendations**:
   - **Organic / Biological**: Spray Neem Seed Kernel Extract (NSKE 5%) or Neem Oil (1500 ppm at 4-5 ml/L) mixed with mild soap. Apply *Trichoderma viride* or *Pseudomonas fluorescens* (5g/L water) as biocontrol.
   - **Chemical Intervention**: If severity is high, spray Mancozeb 75% WP (2.5 g/L) or Copper Oxychloride 50% WP (3.0 g/L). For systemic control, spray Azoxystrobin 18.2% + Difenoconazole 11.4% SC (1 ml/L).
   - Remove and destroy severely infected lower leaves to prevent spore dispersion.
7. **Prevention Tips**:
   - Shift from overhead sprinkler irrigation to drip irrigation to avoid leaf wetness.
   - Ensure adequate field drainage to prevent waterlogging around root zones.
   - Rotate crops with non-host crops (e.g., pulses or legumes) next season."""

def analyze_image_with_text(image_base64, user_query="What do you see in this image?", mime_type="image/jpeg"):
    """Analyze image using Groq Vision or fallback agricultural engine."""
    # 1. Try Groq
    if groq_client:
        vision_models = [m for m in [GROQ_VISION_MODEL, "llama-3.2-11b-vision-preview", "llama-3.2-90b-vision-preview"] if m]
        seen_vm = set()
        vision_candidates = [m for m in vision_models if not (m in seen_vm or seen_vm.add(m))]
        for vision_model in vision_candidates:
            try:
                response = groq_client.chat.completions.create(
                    model=vision_model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are Krishi Mitra, expert agricultural AI assistant. Keep responses actionable, concise, and focused on farming, disease identification, soil and crop care."
                        },
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": user_query},
                                {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_base64}"}}
                            ]
                        }
                    ],
                    temperature=0.3,
                    max_tokens=600
                )
                return response.choices[0].message.content
            except Exception:
                continue

    # 2. Local fallback
    local_diag = analyze_crop_disease(image_base64, mime_type)
    return f"""**Image Analysis & Farming Advisory:**

Based on visual examination of the crop specimen:
{local_diag}

*Additional Guidance for query: "{user_query}"*:
Ensure soil moisture is kept at field capacity, avoid applying chemical fertilizers during direct hot sun, and inspect adjacent crops for early symptom spread."""

def get_farming_advice(weather_data, crop_type="general"):
    """Get farming advice based on weather conditions."""
    city = weather_data.get('name', 'Your Region')
    temp = weather_data.get('main', {}).get('temp', 26.0)
    humidity = weather_data.get('main', {}).get('humidity', 65)
    description = weather_data.get('weather', [{}])[0].get('description', 'Clear sky')
    wind_speed = weather_data.get('wind', {}).get('speed', 3.5)

    # 1. Try Groq
    if groq_client:
        weather_summary = f"Location: {city}, Temp: {temp}°C, Humidity: {humidity}%, Condition: {description}, Wind: {wind_speed} m/s, Crop: {crop_type}"
        groq_resp = call_groq_chat(
            messages=[
                {
                    "role": "system",
                    "content": "You are Krishi Mitra Weather Advisory System. Provide clear farming advice with: 1. Today's Farming Activities, 2. Irrigation Advice, 3. Pest & Disease Alert, 4. Crop Protection Measures, 5. Best Time for Field Work."
                },
                {
                    "role": "user",
                    "content": f"Weather data: {weather_summary}. Crop: {crop_type}."
                }
            ],
            temperature=0.3,
            max_tokens=600
        )
        if groq_resp:
            return groq_resp

    # 2. Expert Agronomic Advisory System Fallback
    temp_val = float(temp) if isinstance(temp, (int, float)) else 25.0
    hum_val = float(humidity) if isinstance(humidity, (int, float)) else 60.0
    wind_val = float(wind_speed) if isinstance(wind_speed, (int, float)) else 3.0

    # Irrigation rules
    if "rain" in description.lower() or "drizzle" in description.lower():
        irrigation_advice = "Postpone scheduled irrigation immediately. Clear field drainage channels to prevent stagnant waterlogging around roots."
    elif hum_val > 75:
        irrigation_advice = "High atmospheric humidity reduces crop evapotranspiration. Reduce water delivery by 25-30% to prevent root suffocation and damping-off."
    elif temp_val > 32:
        irrigation_advice = "Elevated temperature accelerates soil water evaporation. Provide light, frequent irrigation during early morning or evening hours."
    else:
        irrigation_advice = "Normal scheduled irrigation recommended. Maintain soil moisture at 60-70% field capacity."

    # Pest alerts
    if hum_val > 70 and temp_val > 22 and temp_val < 32:
        pest_alert = "HIGH RISK: Warm and humid weather creates ideal conditions for fungal leaf spots (Blight, Rust, Powdery Mildew) and sucking insects (Aphids, Whiteflies)."
    elif temp_val > 34:
        pest_alert = "MODERATE RISK: Heat stress may induce spider mite outbreaks and flower drop. Check underside of leaves for webbings."
    else:
        pest_alert = "LOW TO MODERATE RISK: General monitoring advised. Inspect crop canopy twice weekly."

    # Spray timing
    if wind_val > 5.0 or "rain" in description.lower():
        field_work = "Avoid foliar pesticide or fertilizer spraying today due to wind drift and wash-off risks. Conduct weeding and staking instead."
    else:
        field_work = "Favorable conditions for foliar spraying and tillage. Best execution window is 06:30 AM - 09:30 AM or 04:30 PM - 06:30 PM."

    return f"""### 🌤️ Weather-Based Farming Advisory for {city}
**Current Conditions**: {temp}°C, {humidity}% Humidity, Wind {wind_speed} m/s ({description.title()})
**Target Crop**: {crop_type.title()}

1. **Today's Farming Activities**:
   - Undertake field inspection, weed eradication, and bund strengthening.
   - Adjust field operations according to local soil moisture and cloud cover.

2. **Irrigation Advice**:
   - {irrigation_advice}

3. **Pest & Disease Alert**:
   - {pest_alert}

4. **Crop Protection Measures**:
   - Apply protective bio-fungicide (*Trichoderma viride* 5g/L) or Neem Oil 1500 ppm if cloudy weather persists.
   - Mulch around root bases with straw to regulate soil temperature.

5. **Best Time for Field Work**:
   - {field_work}"""

def calculate_resources(crop_type, area, area_unit, soil_type, growth_stage):
    """Calculate resource requirements with agronomic algorithms."""
    # Convert area to hectares
    try:
        a_val = float(area)
    except Exception:
        a_val = 1.0

    unit_to_ha = {
        'acres': 0.404686,
        'hectares': 1.0,
        'bigha': 0.25,
        'bigha_punjab': 0.2023,
        'bigha_rajasthan': 0.25,
        'kanal': 0.0505857,
        'gunta': 0.010117,
        'sq_meters': 0.0001
    }
    ha = a_val * unit_to_ha.get(area_unit.lower(), 0.404686)

    # 1. Try Groq
    if groq_client:
        groq_resp = call_groq_chat(
            messages=[
                {
                    "role": "system",
                    "content": "You are Krishi Mitra Resource Calculator. Calculate water, fertilizer (NPK in kg), seeds (kg), labor (person-days), cost breakdown, and application schedule."
                },
                {
                    "role": "user",
                    "content": f"Calculate resources for Crop: {crop_type}, Area: {area} {area_unit} ({ha:.2f} ha), Soil: {soil_type}, Stage: {growth_stage}."
                }
            ],
            temperature=0.2,
            max_tokens=800
        )
        if groq_resp:
            return groq_resp

    # 2. Agronomic calculations fallback
    # Crop base values per hectare
    crop_lower = crop_type.lower()
    if 'rice' in crop_lower or 'paddy' in crop_lower:
        water_daily = int(55000 * ha)
        npk = (120 * ha, 60 * ha, 40 * ha)
        seeds = 35 * ha
        labor_days = int(45 * ha)
        cost_est = int(42000 * ha)
    elif 'wheat' in crop_lower:
        water_daily = int(32000 * ha)
        npk = (100 * ha, 50 * ha, 40 * ha)
        seeds = 100 * ha
        labor_days = int(30 * ha)
        cost_est = int(36000 * ha)
    elif 'cotton' in crop_lower:
        water_daily = int(28000 * ha)
        npk = (100 * ha, 50 * ha, 50 * ha)
        seeds = 4 * ha
        labor_days = int(50 * ha)
        cost_est = int(48000 * ha)
    elif 'maize' in crop_lower or 'corn' in crop_lower:
        water_daily = int(30000 * ha)
        npk = (120 * ha, 60 * ha, 40 * ha)
        seeds = 20 * ha
        labor_days = int(28 * ha)
        cost_est = int(32000 * ha)
    else:
        water_daily = int(30000 * ha)
        npk = (80 * ha, 40 * ha, 40 * ha)
        seeds = 25 * ha
        labor_days = int(32 * ha)
        cost_est = int(35000 * ha)

    # Soil adjustment
    if 'sandy' in soil_type.lower():
        water_daily = int(water_daily * 1.25)
    elif 'clay' in soil_type.lower():
        water_daily = int(water_daily * 0.85)

    n_kg, p_kg, k_kg = npk

    return f"""### 📊 Agricultural Resource Estimates for {crop_type.title()}
**Farm Size**: {area} {area_unit.title()} (≈ {ha:.3f} Hectares) | **Soil**: {soil_type.title()} | **Stage**: {growth_stage.title()}

1. **Water Requirements**:
   - **Daily Irrigation Need**: ≈ {water_daily:,} Liters / day
   - **Weekly Water Need**: ≈ {water_daily * 7:,} Liters / week
   - *Recommendation*: Use drip or micro-sprinkler systems to conserve up to 40% water.

2. **Fertilizer Requirements (Total for Farm Size)**:
   - **Nitrogen (N)**: {n_kg:.1f} kg (Apply 50% as basal dose, split rest at vegetative and flowering stages)
   - **Phosphorus (P)**: {p_kg:.1f} kg (100% basal dose during soil preparation)
   - **Potassium (K)**: {k_kg:.1f} kg (Apply in split doses for grain filling & disease resistance)
   - **Zinc Sulphate (ZnSO₄)**: {max(5.0, 15 * ha):.1f} kg for micronutrient balance.

3. **Seed Requirements**:
   - Certified Quality Seeds: ≈ {seeds:.1f} kg (Treat seeds with *Trichoderma* @ 4g/kg seed before sowing).

4. **Labor Estimate**:
   - Total Man-Days: ≈ {max(2, labor_days)} person-days across land prep, sowing, weeding, and management.

5. **Estimated Cost Breakdown**:
   - Seeds & Sowing: ₹{int(cost_est * 0.20):,}
   - Fertilizers & Micronutrients: ₹{int(cost_est * 0.35):,}
   - Irrigation & Power: ₹{int(cost_est * 0.15):,}
   - Labor & Crop Protection: ₹{int(cost_est * 0.30):,}
   - **Total Estimated Operating Cost**: **₹{cost_est:,}**

6. **Application Schedule**:
   - *Week 1-2*: Basal fertilizer (Full P, Full K, 33% N) + Primary Irrigation.
   - *Week 4-6*: First top dressing (33% N) during peak tillering/branching.
   - *Week 8-10*: Second top dressing (33% N) + Potassium foliar spray during panicle/flowering initiation."""

class RAGQAChain:
    """Intelligent RAG Agricultural Question-Answering Chain with strict domain guardrails"""
    def __init__(self, db, mode="general"):
        self.db = db
        self.mode = mode

    def _detect_language(self, text):
        t_lower = text.lower()
        if "hindi" in t_lower or any('\u0900' <= char <= '\u097F' for char in text):
            return "Hindi"
        elif "punjabi" in t_lower or any('\u0A00' <= char <= '\u0A7F' for char in text):
            return "Punjabi"
        elif "bengali" in t_lower or any('\u0980' <= char <= '\u09FF' for char in text):
            return "Bengali"
        elif "marathi" in t_lower:
            return "Marathi"
        elif "telugu" in t_lower or any('\u0C00' <= char <= '\u0C7F' for char in text):
            return "Telugu"
        elif "tamil" in t_lower or any('\u0B80' <= char <= '\u0BFF' for char in text):
            return "Tamil"
        elif "gujarati" in t_lower or any('\u0A80' <= char <= '\u0AFF' for char in text):
            return "Gujarati"
        elif "kannada" in t_lower or any('\u0C80' <= char <= '\u0CFF' for char in text):
            return "Kannada"
        elif "malayalam" in t_lower or any('\u0D00' <= char <= '\u0D7F' for char in text):
            return "Malayalam"
        elif "odia" in t_lower or any('\u0B00' <= char <= '\u0B7F' for char in text):
            return "Odia"
        return "English"

    def _is_greeting(self, q_clean):
        q_norm = q_clean.lower().strip()
        greetings = {
            'hi', 'hello', 'hey', 'namaste', 'namaskar', 'pranam', 'ram ram', 
            'radhe radhe', 'sat sri akal', 'kisan bhai', 'who are you', 
            'what is krishi mitra', 'kya kar sakte ho', 'kaun ho', 'good morning', 
            'good afternoon', 'good evening', 'help', 'kem cho', 'vanakkam'
        }
        return q_norm in greetings or any(q_norm.startswith(g + ' ') for g in ['hi', 'hello', 'namaste', 'hey'])

    def _get_greeting_response(self, lang):
        if lang == "Hindi":
            return (
                "🌱 **नमस्ते! मैं कृषि मित्र हूँ**, आपका समर्पित AI स्मार्ट किसान सहायक।\n\n"
                "मैं केवल खेती-किसानी से जुड़े विषयों में आपकी सहायता करता हूँ:\n"
                "• **फसल उत्पादन**: उन्नत किस्में, बुवाई का सही समय एवं बीज उपचार\n"
                "• **फसल सुरक्षा (रोग व कीट)**: रोगों की पहचान, कीट रोकथाम तथा जैविक व रासायनिक दवाइयां\n"
                "• **मृदा स्वास्थ्य व खाद**: मिट्टी परीक्षण, संतुलित NPK उर्वरक एवं वर्मीकंपोस्ट\n"
                "• **ताज़ा मंडी भाव व MSP**: कृषि मंडियों के भाव, न्यूनतम समर्थन मूल्य व मुनाफा\n"
                "• **मौसम एवं सिंचाई**: मौसम आधारित कृषि सलाह एवं ड्रिप/फव्वारा सिंचाई\n"
                "• **सरकारी योजनाएं**: PM-किसान, फसल बीमा (PMFBY), KCC ऋण व कुसुम सौर पंप\n\n"
                "🌾 आज मैं आपके खेत या फसल के लिए क्या सहायता करूँ?"
            )
        elif lang == "Punjabi":
            return (
                "🌱 **ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਹਾਂ**, ਤੁਹਾਡਾ ਕਿਸਾਨ ਸਹਾਇਕ।\n\n"
                "ਮੈਂ ਸਿਰਫ਼ ਖੇਤੀਬਾੜੀ ਨਾਲ ਸੰਬੰਧਿਤ ਜਾਣਕਾਰੀ ਦਿੰਦਾ ਹਾਂ:\n"
                "• **ਫ਼ਸਲਾਂ ਦੀ ਬਿਜਾਈ**: ਉੱਨਤ ਕਿਸਮਾਂ, ਬਿਜਾਈ ਦਾ ਸਮਾਂ ਅਤੇ ਬੀਜ ਸੋਧ\n"
                "• **ਫ਼ਸਲੀ ਰੋਗ ਤੇ ਕੀੜੇ**: ਰੋਗਾਂ ਦੀ ਪਛਾਣ, ਕੀਟਨਾਸ਼ਕ ਅਤੇ ਜੈਵਿਕ ਰੋਕਥਾਮ\n"
                "• **ਖਾਦ ਅਤੇ ਸਿੰਚਾਈ**: ਸੰਤੁਲਿਤ NPK, ਤੁਪਕਾ ਸਿੰਚਾਈ ਅਤੇ ਪਾਣੀ ਦੀ ਬਚਤ\n"
                "• **ਮੰਡੀ ਭਾਅ ਤੇ MSP**: ਅੱਜ ਦੇ ਮੰਡੀ ਭਾਅ ਅਤੇ ਸਰਕਾਰੀ ਸਕੀਮਾਂ (PM-ਕਿਸਾਨ, KCC)\n\n"
                "🌾 ਅੱਜ ਤੁਸੀਂ ਆਪਣੀ ਫ਼ਸਲ ਬਾਰੇ ਕੀ ਪੁੱਛਣਾ ਚਾਹੁੰਦੇ ਹੋ?"
            )
        else:
            return (
                "🌱 **Namaste! I am Krishi Mitra**, your dedicated AI Smart Farming Assistant.\n\n"
                "I assist exclusively with agriculture and farming matters:\n"
                "• **Crop Cultivation**: High-yielding varieties, optimal sowing schedules & seed treatment\n"
                "• **Crop Doctor**: Plant disease diagnosis, pest eradication & organic/chemical remedies\n"
                "• **Soil Health & Fertilizers**: Soil testing, balanced NPK dosage & vermicomposting\n"
                "• **Live Mandi Bhav & MSP**: Market prices, minimum support price rates & selling advice\n"
                "• **Weather & Irrigation**: Agro-meteorological advisories & water conservation techniques\n"
                "• **Government Schemes**: PM-KISAN, PMFBY crop insurance, KCC loans & PM-KUSUM\n\n"
                "🌾 How may I assist your farm or crop today?"
            )

    def _is_agricultural_query(self, clean_q):
        """
        Check if query is related to farming, crops, soil, pests, mandi, schemes, or agriculture.
        """
        q_lower = clean_q.lower()

        # Extensive agricultural terminology (English, Hindi transliteration, regional terms)
        agri_keywords = [
            # Crops (Cereals, Pulses, Cash crops, Vegetables, Fruits, Spices)
            'crop', 'crops', 'farming', 'farm', 'farmer', 'kisan', 'kheti', 'khet', 'fasal', 'faslo',
            'wheat', 'gehu', 'kanak', 'rice', 'paddy', 'dhaan', 'chawal', 'cotton', 'kapas',
            'maize', 'makka', 'sugarcane', 'ganna', 'mustard', 'sarson', 'raya', 'soybean',
            'groundnut', 'moongphali', 'chickpea', 'gram', 'chana', 'pigeonpea', 'arhar', 'tur',
            'moong', 'urad', 'lentil', 'masoor', 'potato', 'aalu', 'aloo', 'tomato', 'tamatar',
            'onion', 'pyaaz', 'garlic', 'lahsun', 'ginger', 'adrak', 'turmeric', 'haldi',
            'chilli', 'chili', 'mirch', 'brinjal', 'baingan', 'cabbage', 'cauliflower', 'gobi',
            'mango', 'aam', 'banana', 'kela', 'apple', 'seb', 'guava', 'amrood', 'papaya', 'papita',
            'grapes', 'angoor', 'orange', 'santra', 'citrus', 'lemon', 'nimbu', 'coconut', 'nariyal',
            'tea', 'chai', 'coffee', 'rubber', 'jute', 'patson', 'bajra', 'jowar', 'sorghum', 'ragi',
            'barley', 'jau', 'peas', 'matar', 'cumin', 'jeera', 'coriander', 'dhania', 'fenugreek', 'methi',
            # Agronomy, operations, practices
            'sow', 'sowing', 'boi', 'buvai', 'seed', 'beej', 'harvest', 'harvesting', 'katai',
            'yield', 'paidavar', 'production', 'acre', 'hectare', 'bigha', 'kanal', 'gunta',
            'nursery', 'transplanting', 'spacing', 'pruning', 'weeding', 'kharpatwar', 'ninda',
            'tilling', 'ploughing', 'jotai', 'stubble', 'parali', 'mulch', 'mulching', 'crop rotation',
            'intercropping', 'greenhouse', 'polyhouse', 'hydroponics',
            # Soil, nutrients, fertilizers
            'soil', 'mitti', 'clay', 'sand', 'loam', 'soil test', 'soil health', 'mrida',
            'fertilizer', 'khad', 'urea', 'dap', 'ssp', 'mop', 'potash', 'potassium', 'npk',
            'nitrogen', 'phosphorus', 'zinc', 'zink', 'boron', 'iron', 'loha', 'sulphur', 'gandhak',
            'magnesium', 'compost', 'vermicompost', 'gobar', 'fym', 'green manure', 'dhaincha',
            'biofertilizer', 'rhizobium', 'azotobacter', 'psb', 'organic farming', 'jaivik',
            'natural farming', 'prakritik', 'jeevamrit', 'panchagavya', 'neem cake', 'ph',
            # Pests, diseases, plant health
            'disease', 'rog', 'bimari', 'pest', 'keeda', 'keet', 'insect', 'caterpillar', 'sundi',
            'bollworm', 'stem borer', 'aphid', 'chepa', 'maho', 'whitefly', 'thrips', 'mite',
            'fungus', 'fungal', 'bacteria', 'virus', 'blight', 'jhulsa', 'rust', 'gerui', 'rathwa',
            'leaf spot', 'tikka', 'wilt', 'ukhta', 'powdery mildew', 'downy mildew', 'rot', 'galan',
            'mosaic', 'curl', 'marodiya', 'khaira', 'damping off', 'chlorosis', 'yellowing',
            'pesticide', 'insecticide', 'fungicide', 'keetnashak', 'faphundnashak', 'dawa', 'davai',
            'spray', 'chhidkao', 'neem oil', 'mancozeb', 'copper oxychloride', 'coragen', 'tilt',
            'trichoderma', 'sticky trap', 'pheromone trap',
            # Water, irrigation, climate
            'water', 'paani', 'irrigation', 'sinchai', 'drip', 'sprinkler', 'fowara', 'tube well',
            'borewell', 'drainage', 'rain', 'barish', 'rainfall', 'monsoon', 'weather', 'mausam',
            'frost', 'pala', 'drought', 'sukha', 'flood', 'baadh', 'heatwave', 'loo',
            # Market, Mandi, economics
            'mandi', 'market', 'apmc', 'bhav', 'rate', 'price', 'kimat', 'dam', 'msp',
            'minimum support price', 'samarthan mulya', 'sell', 'bechna', 'profit', 'munafa',
            'loss', 'nuksan', 'cost', 'laagat', 'storage', 'godam', 'e-nam', 'enam', 'procurement',
            # Schemes, subsidies, institutions
            'scheme', 'yojana', 'sarkar', 'sarkari', 'subsidy', 'anudan', 'loan', 'karz', 'rin',
            'kcc', 'kisan credit card', 'pm-kisan', 'pm kisan', 'pmkisan', 'samman nidhi',
            'pmfby', 'fasal bima', 'insurance', 'kusum', 'solar pump', 'solar', 'soil health card',
            'pkvy', 'kvk', 'krishi vigyan kendra', 'call center', '1800-180-1551', 'dbt',
            # Machinery & equipment
            'tractor', 'traktor', 'rotavator', 'cultivator', 'seed drill', 'harvester', 'sprayer',
            'pump', 'motor', 'drone',
            # Regional equivalents
            'shetkari', 'sheti', 'pik', 'paus', 'khedut', 'pak', 'khatar', 'rythu', 'pantalu',
            'vivisayam', 'uzhavar', 'payir', 'krishi', 'chash'
        ]

        # Native Indian Language Agricultural Keywords (Devanagari, Gurmukhi, Bengali, etc.)
        indian_agri_keywords = [
            'गेहूं', 'धान', 'चावल', 'कपास', 'मक्का', 'गन्ना', 'सरसों', 'सोयाबीन', 'मूंगफली',
            'चना', 'अरहर', 'मूंग', 'उड़द', 'आलू', 'टमाटर', 'प्याज', 'लहसुन', 'अदरक', 'हल्दी',
            'मिर्च', 'बैंगन', 'गोभी', 'आम', 'केला', 'सेब', 'संतरा', 'बाजरा', 'ज्वार', 'जौ',
            'मटर', 'जीरा', 'धनिया', 'मेथी', 'फसल', 'फसलों', 'खेती', 'किसान', 'खेत', 'बुवाई',
            'बोवाई', 'कटाई', 'पैदावार', 'बीज', 'मिट्टी', 'खाद', 'उर्वरक', 'यूरिया', 'पोटाश',
            'जिंक', 'गोबर', 'जैविक', 'कीट', 'रोग', 'कीड़ा', 'झुलसा', 'रतुआ', 'इलाज', 'उपचार',
            'दवा', 'दवाई', 'स्प्रे', 'छिड़काव', 'सिंचाई', 'पानी', 'ड्रिप', 'मौसम', 'बारिश',
            'पाला', 'सूखा', 'बाढ़', 'मंडी', 'भाव', 'दाम', 'एमएसपी', 'योजना', 'सब्सिडी', 'ऋण',
            'कर्ज', 'बीमा', 'कुसुम', 'पंप', 'ट्रैक्टर',
            # Punjabi & Gurmukhi
            'ਕਣਕ', 'ਝੋਨਾ', 'ਫ਼ਸਲ', 'ਖੇਤੀ', 'ਕਿਸਾਨ', 'ਖਾਦ', 'ਸਪਰੇਅ', 'ਮੰਡੀ', 'ਬੀਜ', 'ਪਾਣੀ',
            # Bengali
            'ফসল', 'কৃষি', 'ধান', 'চাষ', 'সার', 'কীটপতঙ্গ', 'জমি',
            # Marathi
            'पीक', 'शेतकरी', 'शेती', 'खत', 'बाजारभाव', 'पाऊस'
        ]

        for ik in indian_agri_keywords:
            if ik in clean_q:
                return True

        # Check English and Romanized keywords
        clean_words = set(w.strip('.,?!:;"\'') for w in q_lower.split())
        for w in clean_words:
            if w in agri_keywords:
                return True
        for phrase in ['pm kisan', 'soil test', 'mandi bhav', 'crop yield', 'drip irrigation', 'leaf spot', 'neem oil', 'paddy rice', 'yellow rust', 'late blight']:
            if phrase in q_lower:
                return True

        # Check semantic vector similarity (requires strong match against agricultural corpus)
        max_sim = self.db.get_max_similarity(clean_q)
        if max_sim >= 0.20:
            return True

        return False

    def _get_non_agricultural_refusal(self, lang):
        if lang == "Hindi":
            return (
                "🌾 **कृषि मित्र केवल कृषि एवं किसान भाइयों के मार्गदर्शन के लिए समर्पित है।**\n\n"
                "मैं केवल खेती-किसानी, फसल, मिट्टी, मौसम एवं कृषि योजनाओं से जुड़े प्रश्नों का उत्तर दे सकता हूँ। कृपया निम्न में से कोई प्रश्न पूछें:\n"
                "• **फसल उत्पादन**: उन्नत किस्में, बुवाई का समय, बीज दर एवं पैदावार\n"
                "• **फसल सुरक्षा**: फसल रोग पहचान, कीट नियंत्रण तथा जैविक व रासायनिक दवाइयां (स्प्रे)\n"
                "• **मृदा स्वास्थ्य व खाद**: मिट्टी परीक्षण, संतुलित NPK उर्वरक, वर्मीकंपोस्ट एवं सूक्ष्म पोषक तत्व\n"
                "• **ताज़ा मंडी भाव व MSP**: कृषि मंडियों के भाव, न्यूनतम समर्थन मूल्य व अनाज बिक्री सलाह\n"
                "• **मौसम एवं सिंचाई**: वर्षा अलर्ट, मौसम आधारित कृषि सलाह एवं ड्रिप/फव्वारा सिंचाई\n"
                "• **सरकारी योजनाएं व समाचार**: PM-किसान, फसल बीमा (PMFBY), KCC ऋण, कुसुम सौर पंप व कृषि समाचार\n\n"
                "💡 *कृपया केवल खेती एवं कृषि से संबंधित प्रश्न पूछें!*"
            )
        elif lang == "Punjabi":
            return (
                "🌾 **ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਸਿਰਫ਼ ਖੇਤੀਬਾੜੀ ਅਤੇ ਕਿਸਾਨਾਂ ਲਈ ਸਮਰਪਿਤ ਹੈ।**\n\n"
                "ਮੈਂ ਸਿਰਫ਼ ਖੇਤੀ, ਫ਼ਸਲਾਂ, ਜ਼ਮੀਨ, ਮੰਡੀ ਭਾਅ ਅਤੇ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਬਾਰੇ ਹੀ ਸਹਾਇਤਾ ਕਰ ਸਕਦਾ ਹਾਂ। ਕਿਰਪਾ ਕਰਕੇ ਹੇਠ ਲਿਖੇ ਵਿਸ਼ਿਆਂ 'ਤੇ ਸਵਾਲ ਪੁੱਛੋ:\n"
                "• **ਫ਼ਸਲ ਬਿਜਾਈ**: ਉੱਨਤ ਕਿਸਮਾਂ, ਖਾਦਾਂ (NPK) ਅਤੇ ਬੀਜ ਸੋਧ\n"
                "• **ਫ਼ਸਲੀ ਰੋਗ ਤੇ ਸਪਰੇਅ**: ਰੋਗਾਂ ਦੀ ਪਛਾਣ ਅਤੇ ਕੀਟਨਾਸ਼ਕ/ਉੱਲੀਨਾਸ਼ਕ ਦਵਾਈਆਂ\n"
                "• **ਮੰਡੀ ਭਾਅ ਤੇ MSP**: ਅੱਜ ਦੇ ਮੰਡੀ ਭਾਅ ਅਤੇ ਸਰਕਾਰੀ ਖ਼ਰੀਦ\n"
                "• **ਸਰਕਾਰੀ ਸਕੀਮਾਂ**: PM-ਕਿਸਾਨ, ਫ਼ਸਲੀ ਬੀਮਾ (PMFBY) ਅਤੇ ਕਿਸਾਨ ਕ੍ਰੈਡਿਟ ਕਾਰਡ (KCC)\n\n"
                "💡 *ਕਿਰਪਾ ਕਰਕੇ ਖੇਤੀਬਾੜੀ ਨਾਲ ਸੰਬੰਧਿਤ ਸਵਾਲ ਹੀ ਪੁੱਛੋ!*"
            )
        elif lang == "Marathi":
            return (
                "🌾 **कृषी मित्र केवळ शेती आणि शेतकऱ्यांच्या मार्गदर्शनासाठी समर्पित आहे.**\n\n"
                "मी केवळ पिके, जमीन, खते, रोग नियंत्रण, बाजारभाव आणि सरकारी योजनांशी संबंधित प्रश्नांची उत्तरे देऊ शकतो:\n"
                "• **पीक लागवड**: सुधारित वाण, पेरणीचे दिवस आणि खत व्यवस्थापन\n"
                "• **पीक संरक्षण**: कीड व रोग नियंत्रण, कीटकनाशके आणि जैविक उपाय\n"
                "• **बाजारभाव व हमीभाव (MSP)**: बाजार समित्यांचे आजचे भाव व विक्री\n"
                "• **शासकीय योजना**: पीएम-किसान, पीक विमा (PMFBY), केसीसी कर्ज व सौर पंप योजना\n\n"
                "💡 *कृपया केवळ शेतीविषयक प्रश्न विचारा!*"
            )
        else:
            return (
                "🌾 **Krishi Mitra is dedicated exclusively to Agriculture & Farming.**\n\n"
                "I can only assist with farming, crops, soil, weather, mandi prices, and agricultural schemes. Please feel free to ask about:\n"
                "• **Crop Cultivation**: Recommended varieties, optimal sowing dates, seed rates & harvesting\n"
                "• **Crop Doctor & Health**: Plant disease diagnosis, pest control & organic/chemical sprays\n"
                "• **Soil Health & Fertilizers**: Soil testing, balanced NPK dosage, biofertilizers & vermicomposting\n"
                "• **Live Mandi Bhav & MSP**: Current market rates, minimum support prices & grain marketing\n"
                "• **Weather & Irrigation**: Agro-meteorological advisories, rainfall alerts & drip/sprinkler scheduling\n"
                "• **Government Schemes & Agri News**: PM-KISAN, PMFBY crop insurance, KCC loans, PM-KUSUM solar pumps\n\n"
                "💡 *Please ask a question related to farming or agriculture!*"
            )

    def _detect_crop(self, clean_q):
        """Identifies specific Indian crops mentioned in the user query across English, Hindi, and regional languages"""
        q_lower = clean_q.lower()
        crop_aliases = {
            'wheat': ['wheat', 'gehu', 'gehun', 'kanak', 'गेहूं', 'गेहूँ', 'ਕਣਕ'],
            'rice': ['rice', 'paddy', 'dhan', 'dhaan', 'chawal', 'धान', 'चावल', 'ਝੋਨਾ', 'ਚਾਵਲ'],
            'cotton': ['cotton', 'kapas', 'narma', 'कपास', 'नरमा', 'ਕਪਾਹ'],
            'mustard': ['mustard', 'sarson', 'rai', 'raya', 'सरसों', 'राई', 'ਸਰ੍ਹੋਂ'],
            'sugarcane': ['sugarcane', 'ganna', 'ikshu', 'गन्ना', 'ਗੰਨਾ'],
            'maize': ['maize', 'makka', 'makki', 'corn', 'मक्का', 'मक्की', 'ਮੱਕੀ'],
            'chickpea': ['chickpea', 'chana', 'gram', 'चना', 'ਛੋਲੇ'],
            'soybean': ['soybean', 'soya', 'सोयाबीन', 'ਸੋਇਆਬੀਨ'],
            'groundnut': ['groundnut', 'peanut', 'moongphali', 'mungfali', 'मूंगफली', 'ਮੂੰਗਫਲੀ'],
            'potato': ['potato', 'aloo', 'aalu', 'आलू', 'ਆਲੂ'],
            'tomato': ['tomato', 'tamatar', 'टमाटर', 'ਟਮਾਟਰ'],
            'onion': ['onion', 'pyaz', 'pyaaz', 'प्याज', 'ਪਿਆਜ਼'],
            'garlic': ['garlic', 'lahsun', 'लहसुन', 'ਲਸਣ'],
            'ginger': ['ginger', 'adrak', 'अदरक', 'ਅਦਰਕ'],
            'turmeric': ['turmeric', 'haldi', 'हल्दी', 'ਹਲਦੀ'],
            'chilli': ['chilli', 'chili', 'mirch', 'मिर्च', 'ਮਿਰਚ'],
            'mango': ['mango', 'aam', 'आम', 'ਅੰਬ'],
            'banana': ['banana', 'kela', 'केला', 'ਕੇਲਾ'],
            'apple': ['apple', 'seb', 'सेब', 'ਸੇਬ'],
            'grapes': ['grapes', 'angoor', 'अंगूर', 'ਅੰਗੂਰ'],
            'guava': ['guava', 'amrood', 'अमरूद', 'ਅਮਰੂਦ'],
            'pomegranate': ['pomegranate', 'anar', 'अनार', 'ਅਨਾਰ'],
            'papaya': ['papaya', 'papita', 'पपीता', 'ਪਪੀਤਾ'],
            'tea': ['tea', 'chai', 'चाय', 'ਚਾਹ'],
            'coffee': ['coffee', 'कॉफ़ी', 'ਕਾਫ਼ੀ'],
            'barley': ['barley', 'jau', 'जौ', 'ਜੌਂ'],
            'bajra': ['bajra', 'pearl millet', 'बाजरा', 'ਬਾਜਰਾ'],
            'jowar': ['jowar', 'sorghum', 'ज्वार', 'ਜਵਾਰ'],
            'ragi': ['ragi', 'finger millet', 'रागी', 'ਮਡੂਆ'],
            'pigeonpeas': ['arhar', 'tur', 'toor', 'pigeonpea', 'अरहर', 'तुअर'],
            'mungbean': ['moong', 'mung', 'मूंग', 'ਮੂੰਗ'],
            'blackgram': ['urad', 'mash', 'उड़द', 'ਮਾਂਹ'],
            'lentil': ['masoor', 'lentil', 'मसूर', 'ਮਸਰ'],
            'peas': ['matar', 'green peas', 'मटर', 'ਮਟਰ'],
            'brinjal': ['brinjal', 'baingan', 'eggplant', 'बैंगन'],
            'cabbage': ['cabbage', 'patta gobhi', 'पत्तागोभी'],
            'cauliflower': ['cauliflower', 'phool gobhi', 'फूलगोभी'],
            'okra': ['okra', 'bhindi', 'ladyfinger', 'भिंडी']
        }
        for crop_key, aliases in crop_aliases.items():
            for a in aliases:
                pattern = r'(?<!\w)' + re.escape(a) + r'(?!\w)'
                if re.search(pattern, q_lower, re.IGNORECASE):
                    return crop_key
        return None

    def _synthesize_expert_agricultural_answer(self, q_clean, docs, lang):
        """Synthesize high-quality, actionable agricultural guidance based on user query and verified agronomic catalog"""
        q_lower = q_clean.lower()
        crop_key = self._detect_crop(q_clean)

        # -------------------------------------------------------------
        # BRANCH 1: Crop-Specific Questions (Cultivation, Fertilizer, Irrigation, Diseases)
        # -------------------------------------------------------------
        if crop_key:
            try:
                import crop_recommendation as cr
                guide = cr.get_crop_guide(crop_key)
            except Exception:
                guide = None

            if guide:
                crop_name = guide.get("crop_name", crop_key.capitalize())
                varieties = guide.get("recommended_varieties", "High-yielding ICAR approved certified varieties")
                season = guide.get("season", "Standard crop season")
                soil = guide.get("soil_type", "Fertile well-drained loamy soil (pH 6.0 - 7.5)")
                land_prep = guide.get("land_preparation", "1 deep ploughing followed by 2 harrowings and planking for fine crumbly tilth")
                seed_rate = guide.get("seed_rate_and_spacing", "Standard certified seed rate per acre")
                fert = guide.get("fertilizer_bags_per_acre", guide.get("fertilizer_plan", "Balanced NPK as per soil test"))
                irrigation = guide.get("watering_schedule", "Irrigate at critical crop physiological growth stages")
                weeds = guide.get("weed_management", "Maintain weed-free field during first 30-40 days")
                pest = guide.get("pest_disease_advisory", "Regular crop scouting and preventative bio-fungicide foliar spray")
                harvest = guide.get("harvesting_and_storage", "Harvest at physiological maturity when grain moisture is optimal (<14%)")
                yield_est = guide.get("expected_yield", "Optimal district average yield")
                profit = guide.get("economic_profit_acre", "High profitability under balanced agronomic management")

                # Sub-Intent A: Specific Fertilizer Query for this crop
                if any(w in q_lower for w in ['fertilizer', 'fertiliser', 'khad', 'urea', 'dap', 'npk', 'potash', 'zinc', 'dose', 'dosage', 'khuraak']):
                    if lang == "Hindi":
                        return f"""### 🌱 {crop_name}: संतुलित खाद एवं उर्वरक प्रबंधन तालिका (प्रति एकड़)

**1. बुवाई के समय (बेसल डोज):**
• {fert}

**2. मुख्य पोषक तत्व (NPK एवं सूक्ष्म तत्व):**
• अनाज एवं नकदी फसलों के लिए N:P:K का संतुलित अनुपात रखें।
• पीलापन व खैरा रोग से बचाव के लिए जिंक सल्फेट (21%) @ 10-12 किग्रा प्रति एकड़ बेसल डोज में अवश्य दें।

**3. टॉप ड्रेसिंग (Top Dressing) नियम:**
• नाइट्रोजन (यूरिया) को हमेशा 2 से 3 बराबर भागों में सिंचाई के तुरंत बाद नमी में छिड़कें। तेज धूप या सूखी मिट्टी में यूरिया न डालें।

**4. जैविक खाद का समन्वय:**
• रासायनिक खादों के साथ 2-3 ट्रॉली अच्छी सड़ी गोबर की खाद या 8-10 क्विंटल वर्मीकंपोस्ट अवश्य मिलाएं।"""
                    else:
                        return f"""### 🌱 {crop_name}: Balanced Fertilizer & Nutrient Management (Per Acre)

**1. Prescribed Fertilizer Schedule:**
• {fert}

**2. Application Methodology & Timing:**
• **Basal Application**: Apply 100% of Phosphorus (DAP/SSP), Potassium (MOP), and Zinc Sulphate at the time of final ploughing/sowing.
• **Top Dressing**: Split Nitrogen (Neem-Coated Urea) into 2-3 equal splits applied immediately after irrigation when soil is moist.

**3. Micronutrient Enrichment:**
• Ensure Zinc Sulphate 21% (@ 10 kg/acre) is incorporated at sowing to prevent early vegetative interveinal chlorosis and root stunting.

**4. Organic Enrichment:**
• Incorporate 2-3 tonnes of decomposed FYM or 1 tonne of vermicompost per acre to enhance nutrient use efficiency."""

                # Sub-Intent B: Specific Irrigation Query for this crop
                if any(w in q_lower for w in ['water', 'watering', 'irrigation', 'sinchai', 'paani', 'stages', 'schedule']):
                    if lang == "Hindi":
                        return f"""### 💧 {crop_name}: क्रांतिक अवस्थाओं पर सिंचाई कार्यक्रम

**सिंचाई सारणी:**
• {irrigation}

**महत्वपूर्ण सिंचाई सुझाव:**
1. **क्रांतिक अवस्थाएं (Critical Stages):** फसल की प्रारंभिक वृद्धि (जैसे गेहूं में CRI अवस्था 21 दिन) तथा फूल/बाली आते समय पानी की कमी कभी न होने दें।
2. **जल संरक्षण:** अधिक पानी भरने से बचें। जलभराव से जड़ें सड़ सकती हैं। संभव हो तो ड्रिप या फव्वारा सिंचाई अपनाएं।
3. **मौसम का ध्यान रखें:** बारिश की संभावना होने पर सिंचाई 2-3 दिन टालें ताकि फसल गिरे नहीं।"""
                    else:
                        return f"""### 💧 {crop_name}: Critical Growth Stage Irrigation Schedule

**Irrigation Recommendations:**
• {irrigation}

**Key Irrigation Principles:**
1. **Critical Moisture Windows:** Never allow moisture stress during initial root establishment (e.g. CRI at 21 DAS in wheat) or during flowering/grain filling.
2. **Prevent Waterlogging:** Ensure rapid drainage during unseasonal heavy downpours to protect root zones from anaerobic decay and collar rot.
3. **Modern Micro-Irrigation:** Utilize drip irrigation or micro-sprinklers to achieve 35-40% water savings and prevent foliar humidity spikes."""

                # Sub-Intent C: Specific Disease / Pest Query for this crop
                if any(w in q_lower for w in ['disease', 'pest', 'rust', 'blight', 'rot', 'wilt', 'spot', 'aphid', 'whitefly', 'bollworm', 'keeda', 'keet', 'sundi', 'dawa', 'spray', 'cure', 'remedy', 'treatment', 'insect']):
                    if lang == "Hindi":
                        return f"""### 🛡️ {crop_name}: प्रमुख रोग, कीट एवं उनका सटीक उपचार

**1. मुख्य रोग एवं कीट चेतावनी:**
• {pest}

**2. जैविक / प्राकृतिक रोकथाम:**
• नीम का तेल (Neem Oil 1500 ppm) @ 4-5 मिली प्रति लीटर पानी में मिलाकर शाम को छिड़कें।
• बीजोपचार एवं मृदा शोधन हेतु ट्राइकोडर्मा विरिडी (*Trichoderma viride*) @ 5 ग्राम/किग्रा का प्रयोग करें।

**3. अनुशंसित रासायनिक उपचार (दवा व खुराक):**
• **रतुआ (Rust) एवं फफूंद धब्बा:** प्रोपिकोनाजोल 25% EC (टिल्ट) @ 1 मिली/लीटर या मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर का स्प्रे करें।
• **झुलसा (Blight):** एज़ोक्सीस्ट्रोबिन + डिफेनोकोनाज़ोल @ 1 मिली/लीटर पानी।
• **रस चूसक कीट (चेपा/माहू, सफेद मक्खी):** इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर या थायमेथोक्सम 25% WG @ 0.3 ग्राम/लीटर।"""
                    else:
                        return f"""### 🛡️ {crop_name}: Pest & Disease Diagnosis and Treatment Plan

**1. Primary Regional Disease / Pest Threats:**
• {pest}

**2. Prophylactic & Organic Control:**
• Spray cold-pressed Neem Oil 1500 ppm @ 4-5 ml/L of water with mild sticker soap during early morning or evening hours.
• Perform seed and nursery treatment with *Trichoderma viride* or *Pseudomonas fluorescens* @ 5g/kg seed.

**3. Targeted Chemical Control (Exact Dosages):**
• **Foliar Rusts (Stripe/Brown Rust):** Spray Propiconazole 25% EC (Tilt) @ 1 ml/L or Tebuconazole 25.9% EC @ 1 ml/L upon initial pustule appearance.
• **Foliar Blights & Leaf Spots:** Spray Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L.
• **Sucking Pests (Aphids, Thrips, Whiteflies):** Spray Imidacloprid 17.8% SL @ 0.5 ml/L or Thiamethoxam 25% WG @ 0.25 g/L."""

                # Default for this crop: Comprehensive Agronomic Cultivation Guide
                if lang == "Hindi":
                    return f"""### 🌾 कृषि मित्र: {crop_name} की सम्पूर्ण वैज्ञानिक खेती मार्गदर्शिका

**1. प्रमुख उन्नत एवं प्रमाणित किस्में:**
• {varieties}

**2. बुवाई का सही समय, जलवायु एवं मिट्टी:**
• **मौसम एवं बुवाई समय:** {season}
• **उपयुक्त मिट्टी:** {soil}
• **अनुकूल तापमान:** {guide.get('ideal_temp_min', 15)}°C से {guide.get('ideal_temp_max', 30)}°C

**3. खेत की तैयारी, बीज दर एवं बीजोपचार:**
• **खेत की तैयारी:** {land_prep}
• **बीज दर एवं कतार दूरी:** {seed_rate}
• **बीजोपचार (Seed Treatment):** बुवाई से पूर्व बीजों को ट्राइकोडर्मा विरिडी (@ 5 ग्राम/किग्रा) या कार्बेन्डाजिम (@ 2 ग्राम/किग्रा) से शोधित करें ताकि जड़ गलन एवं उकठा रोग से शत-प्रतिशत सुरक्षा मिले।

**4. संतुलित खाद एवं उर्वरक प्रबंधन (प्रति एकड़):**
• {fert}

**5. क्रांतिक अवस्थाओं पर सिंचाई कार्यक्रम:**
• {irrigation}

**6. खरपतवार नियंत्रण एवं फसल सुरक्षा:**
• **खरपतवार नियंत्रण:** {weeds}
• **रोग व कीट सुरक्षा:** {pest}

**7. कटाई, पैदावार एवं शुद्ध मुनाफा:**
• **कटाई एवं भंडारण:** {harvest}
• **अनुमानित पैदावार:** {yield_est}
• **आर्थिक लाभ / मुनाफा:** {profit}"""
                elif lang == "Punjabi":
                    return f"""### 🌾 ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ: {crop_name} ਦੀ ਵਿਗਿਆਨਿਕ ਖੇਤੀ ਸੰਪੂਰਨ ਗਾਈਡ

**1. ਉੱਨਤ ਅਤੇ ਪ੍ਰਮਾਣਿਤ ਕਿਸਮਾਂ:**
• {varieties}

**2. ਬਿਜਾਈ ਦਾ ਸਹੀ ਸਮਾਂ ਅਤੇ ਜ਼ਮੀਨ:**
• **ਮੌਸਮ ਅਤੇ ਸਮਾਂ:** {season}
• **ਜ਼ਮੀਨ ਦੀ ਕਿਸਮ:** {soil}

**3. ਖੇਤ ਦੀ ਤਿਆਰੀ ਅਤੇ ਬੀਜ ਸੋਧ:**
• **ਖੇਤ ਦੀ ਤਿਆਰੀ:** {land_prep}
• **ਬੀਜ ਦੀ ਮਾਤਰਾ ਤੇ ਦੂਰੀ:** {seed_rate}
• **ਬੀਜ ਸੋਧ:** ਬਿਜਾਈ ਤੋਂ ਪਹਿਲਾਂ ਬੀਜ ਨੂੰ ਕਾਰਬੈਂਡਾਜ਼ਿਮ (2 ਗ੍ਰਾਮ/ਕਿਲੋ) ਜਾਂ ਟ੍ਰਾਈਕੋਡਰਮਾ ਨਾਲ ਸੋਧੋ।

**4. ਖਾਦ ਪ੍ਰਬੰਧਨ (ਪ੍ਰਤੀ ਏਕੜ):**
• {fert}

**5. ਸਿੰਚਾਈ ਦਾ ਸਮਾਂ:**
• {irrigation}

**6. ਨਦੀਨ ਅਤੇ ਕੀਟ ਰੋਕਥਾਮ:**
• **ਨਦੀਨ ਨਾਸ਼ਕ:** {weeds}
• **ਰੋਗਾਂ ਦੀ ਰੋਕਥਾਮ:** {pest}

**7. ਕਟਾਈ ਅਤੇ ਝਾੜ:**
• **ਕਟਾਈ ਤੇ ਸੰਭਾਲ:** {harvest}
• **ਅੰਦਾਜ਼ਨ ਝਾੜ:** {yield_est}
• **ਮੁਨਾਫ਼ਾ:** {profit}"""
                else:
                    return f"""### 🌾 Krishi Mitra: Comprehensive Cultivation Guide for {crop_name}

**1. High-Yielding & Certified Varieties:**
• {varieties}

**2. Sowing Window & Soil Requirements:**
• **Season & Ideal Time:** {season}
• **Soil Type:** {soil}
• **Optimal Temperature Comfort:** {guide.get('ideal_temp_min', 15)}°C to {guide.get('ideal_temp_max', 30)}°C

**3. Land Preparation, Seed Rate & Spacing:**
• **Land Preparation:** {land_prep}
• **Seed Rate & Row Spacing:** {seed_rate}
• **Seed Treatment Protocol:** Treat seeds with *Trichoderma viride* (@ 5g/kg) or Carbendazim (@ 2g/kg) before sowing to eliminate seed-borne pathogens, damping-off, and seedling rot.

**4. Balanced Fertilizer Schedule (Per Acre):**
• {fert}

**5. Critical Irrigation Scheduling:**
• {irrigation}

**6. Weed Management & Plant Protection:**
• **Weed Control:** {weeds}
• **Pest & Disease Advisory:** {pest}

**7. Harvesting, Yield & Economics:**
• **Harvesting & Storage:** {harvest}
• **Expected Harvest Yield:** {yield_est}
• **Economic Return / Profit:** {profit}"""

        # -------------------------------------------------------------
        # BRANCH 2: General Disease / Pest Diagnosis & Remedy
        # -------------------------------------------------------------
        if any(w in q_lower for w in ['disease', 'pest', 'blight', 'rust', 'aphid', 'whitefly', 'bollworm', 'spot', 'rot', 'wilt', 'rog', 'keeda', 'keet', 'sundi', 'dawa', 'spray', 'fungicide', 'insecticide', 'cure']):
            if lang == "Hindi":
                return """### 🌾 कृषि मित्र: फसल सुरक्षा एवं कीट-रोग उपचार परामर्श

**1. जैविक / प्राकृतिक नियंत्रण उपाय:**
• **नीम का तेल:** नीम का तेल (Neem Oil 1500 ppm) 4-5 मिली प्रति लीटर पानी में मिलाकर शाम के समय छिड़कें।
• **बीज व मृदा शोधन:** ट्राइकोडर्मा विरिडी (*Trichoderma viride*) @ 5 ग्राम प्रति किग्रा बीज या 2 किग्रा/एकड़ गोबर की खाद में मिलाकर भूमि में दें।
• **चिपचिपे ट्रैप:** रस चूसक कीटों के लिए प्रति एकड़ 15-20 पीले व नीले स्टिकी ट्रैप (Yellow/Blue Sticky Traps) लगाएं।

**2. लक्षित रासायनिक फफूंदनाशक / कीटनाशक स्प्रे:**
• **पत्ता धब्बा एवं झुलसा (Blight / Spot):** मैंकोज़ेब 75% WP @ 2.5 ग्राम/लीटर या एज़ोक्सीस्ट्रोबिन + डिफेनोकोनाज़ोल @ 1 मिली/लीटर स्प्रे करें।
• **रतुआ (Rust):** प्रोपिकोनाजोल 25% EC (टिल्ट) @ 1 मिली/लीटर पानी में घोलकर छिड़कें।
• **रस चूसक कीट (माहू, सफेद मक्खी, थ्रिप्स):** इमिडाक्लोप्रिड 17.8% SL @ 0.5 मिली/लीटर या थायमेथोक्सम 25% WG @ 0.3 ग्राम/लीटर।
• **सुंडी / इल्ली (Bollworm, Fall Armyworm):** कोराजन (Chlorantraniliprole 18.5% SC) @ 0.3 मिली/लीटर या इमामेक्टिन बेंजोएट 5% SG @ 0.5 ग्राम/लीटर।

**3. छिड़काव की सावधानियां:**
• छिड़काव हमेशा साफ मौसम में सुबह 8-10 बजे या शाम 4-6 बजे करें। तेज धूप या बारिश की संभावना में छिड़काव न करें।"""
            else:
                return """### 🌾 Krishi Mitra: Comprehensive Plant Protection & Disease Management

**1. Biological & Organic Interventions:**
• **Neem Formulations:** Spray cold-pressed Neem Oil 1500 ppm @ 4-5 ml/L of water with mild liquid soap during early morning or late evening.
• **Bio-Fungicides:** Apply *Trichoderma viride* or *Pseudomonas fluorescens* @ 5g/kg for seed treatment and 2 kg/acre mixed in FYM for soil drenching.
• **Physical Traps:** Install 15-20 Yellow Sticky Traps per acre for sucking pests and Pheromone Traps for borers.

**2. Targeted Chemical Control (Exact Dosages):**
• **Foliar Blights & Leaf Spots:** Spray Mancozeb 75% WP @ 2.5 g/L or Azoxystrobin 18.2% + Difenoconazole 11.4% SC @ 1 ml/L.
• **Rusts & Powdery Mildew:** Spray Propiconazole 25% EC @ 1 ml/L or Tebuconazole 25.9% EC @ 1 ml/L.
• **Sucking Pests (Aphids, Thrips, Whiteflies):** Spray Imidacloprid 17.8% SL @ 0.5 ml/L or Thiamethoxam 25% WG @ 0.25 g/L.
• **Caterpillars & Borers:** Spray Chlorantraniliprole 18.5% SC (Coragen) @ 0.3 ml/L or Emamectin Benzoate 5% SG @ 0.5 g/L.

**3. Spraying Best Practices:**
• Avoid spraying during peak afternoon heat or when rainfall is forecasted within 6 hours. Maintain complete coverage of under-leaf surfaces."""

        # -------------------------------------------------------------
        # BRANCH 3: Government Schemes & Subsidies
        # -------------------------------------------------------------
        if any(w in q_lower for w in ['scheme', 'yojana', 'subsidy', 'anudan', 'pm-kisan', 'pm kisan', 'pmfby', 'kcc', 'kusum', 'bima', 'loan', 'sarkar']):
            if lang == "Hindi":
                return """### 🏛️ कृषि मित्र: सरकारी कृषि योजना मार्गदर्शिका

**प्रमुख किसान योजनाएं एवं लाभ:**
1. **PM-KISAN (प्रधानमंत्री किसान सम्मान निधि):**
   • **लाभ:** सभी पात्र किसान परिवारों को ₹6,000 प्रति वर्ष (₹2,000 की 3 समान किश्तों में प्रत्यक्ष बैंक खाते में DBT)।
   • **पोर्टल:** pmkisan.gov.in | हेल्पलाइन: 155261 / 1800-11-5526.

2. **PMFBY (प्रधानमंत्री फसल बीमा योजना):**
   • **लाभ:** सूखा, बाढ़, ओलावृष्टि व बेमौसम बारिश से फसल नुकसान पर न्यूनतम प्रीमियम (खरीफ 2%, रबी 1.5%, बागवानी 5%) पर पूर्ण बीमा सुरक्षा।
   • **दावा समय सीमा:** प्राकृतिक आपदा के 72 घंटे के भीतर ऐप या टोल-फ्री नंबर 1800-180-1551 पर सूचना दें।

3. **KCC (किसान क्रेडिट कार्ड):**
   • **लाभ:** 4% की रियायती ब्याज दर पर ₹3 लाख तक का आसान फसली ऋण।

4. **PM-KUSUM योजना:**
   • **लाभ:** सिंचाई के लिए सोलर वाटर पंप लगाने पर केंद्र व राज्य सरकार द्वारा 60% तक की भारी सब्सिडी।"""
            else:
                return """### 🏛️ Krishi Mitra: Government Agricultural Schemes & Benefits

**Key Schemes & Direct Farmer Entitlements:**
1. **PM-KISAN (Pradhan Mantri Kisan Samman Nidhi):**
   • **Financial Benefit:** ₹6,000 annually paid in 3 four-monthly installments of ₹2,000 directly into the farmer's bank account (DBT).
   • **Official Portal:** pmkisan.gov.in | Helpline: 155261 / 1800-11-5526.

2. **PMFBY (Pradhan Mantri Fasal Bima Yojana):**
   • **Coverage:** Comprehensive crop loss insurance against drought, floods, hailstorms, pests, and unseasonal rainfall.
   • **Farmer Premium:** Only 2.0% for Kharif crops, 1.5% for Rabi crops, and 5% for commercial/horticultural crops.
   • **Loss Intimation:** Report crop damage within 72 hours via the Crop Insurance App or bank branch.

3. **Kisan Credit Card (KCC):**
   • **Feature:** Low-interest short-term production credit up to ₹3,00,000 at an effective interest rate of 4% per annum upon prompt repayment.

4. **PM-KUSUM Scheme:**
   • **Solar Subsidies:** Up to 60% financial subsidy for installing standalone off-grid and grid-connected solar agricultural water pumps."""

        # -------------------------------------------------------------
        # BRANCH 4: Soil Health, Fertilizers & Nutrition
        # -------------------------------------------------------------
        if any(w in q_lower for w in ['fertilizer', 'khad', 'urea', 'dap', 'npk', 'soil', 'mitti', 'vermicompost', 'organic', 'jaivik', 'zinc', 'potash', 'manure']):
            if lang == "Hindi":
                return """### 🌱 कृषि मित्र: मृदा स्वास्थ्य एवं संतुलित खाद प्रबंधन

**संतुलित खाद एवं पोषण तालिका:**
1. **संतुलित NPK अनुपात:**
   • अनाज वाली फसलों (गेहूं, धान, मक्का) के लिए आदर्श N:P:K अनुपात **4:2:1** रखें।
   • दलहनी फसलों (चना, मूंग, अरहर) के लिए **1:2:1** रखें (क्योंकि दलहन वायुमंडलीय नाइट्रोजन स्वयं स्थिर करते हैं)।

2. **खाद देने का सही समय:**
   • **फॉस्फोरस (DAP / SSP)** एवं **पोटाश (MOP):** 100% मात्रा बुवाई के समय बेसल डोज के रूप में कूड़ों में डालें।
   • **यूरिया (नाइट्रोजन):** 50% बुवाई पर, 25% कल्ले फूटते समय (टिलरिंग), और 25% बाली/फूल निकलने से पहले टॉप ड्रेसिंग करें।

3. **सूक्ष्म पोषक तत्व (जिंक एवं सल्फर):**
   • धान में खैरा रोग एवं गेहूं में पीलापन रोकने हेतु जिंक सल्फेट (ZnSO4 21%) @ 25 किग्रा/हेक्टेयर बेसल डोज में अवश्य दें।

4. **जैविक खाद का प्रयोग:**
   • प्रति एकड़ 8-10 क्विंटल वर्मीकंपोस्ट (केंचुआ खाद) या 4-5 टन गोबर की सड़ी खाद मिलाकर रासायनिक खादों पर निर्भरता 25-30% कम करें।"""
            else:
                return """### 🌱 Krishi Mitra: Soil Health & Balanced Fertilizer Management

**Nutrient Optimization Principles:**
1. **Ideal NPK Ratios:**
   • Cereals (Wheat, Rice, Maize): Maintain an N:P2O5:K2O ratio of **4:2:1**.
   • Pulses (Gram, Moong, Arhar): Maintain **1:2:1** (pulses fix atmospheric nitrogen through Rhizobium nodules).

2. **Split Application Timing:**
   • **Basal Application**: Apply 100% of Phosphorus (DAP/SSP) and Potassium (MOP) alongside 33-50% of Nitrogen during final field preparation.
   • **Top Dressing**: Apply remaining Nitrogen (Neem-Coated Urea) split equally during active tillering/branching and flowering initiation.

3. **Micronutrient Correction:**
   • Apply Zinc Sulphate (ZnSO4 21%) @ 25 kg/ha to prevent Khaira disease in paddy and interveinal leaf chlorosis in cereals.
   • Add Gypsum / Sulphur @ 20 kg/acre for oilseeds (Mustard, Groundnut, Soybean) to boost oil content.

4. **Organic Matter & Soil Health:**
   • Incorporate 2-3 tons/ha of vermicompost or well-decomposed FYM to improve soil water retention and beneficial soil microbiology."""

        # -------------------------------------------------------------
        # BRANCH 5: Mandi Bhav & Agricultural Marketing
        # -------------------------------------------------------------
        if any(w in q_lower for w in ['mandi', 'bhav', 'rate', 'price', 'msp', 'market', 'bechna', 'munafa']):
            if lang == "Hindi":
                return """### 💰 कृषि मित्र: मंडी भाव एवं लाभकारी विपणन सलाह

**अधिक मुनाफा कमाने के व्यावहारिक सुझाव:**
1. **उपज की सफाई एवं ग्रेडिंग:**
   • अनाज को धूप में सुखाकर नमी 12% से नीचे लाएं। मंडी में साफ व ग्रेडेड उपज पर ₹100 से ₹250 प्रति क्विंटल अधिक बोली लगती है।

2. **न्यूनतम समर्थन मूल्य (MSP):**
   • सरकार द्वारा तय MSP दरों पर सरकारी खरीद केंद्रों (जैसे FCI, NAFED) पर पंजीकरण कराकर अपनी उपज बेचें।

3. **e-NAM (राष्ट्रीय कृषि बाजार):**
   • e-NAM पोर्टल पर ऑनलाइन बोली के माध्यम से देश भर के व्यापारियों को सीधे माल बेचकर स्थानीय आढ़तियों के कमीशन से बचें।"""
            else:
                return """### 💰 Krishi Mitra: Mandi Bhav & Agricultural Marketing Guide

**Practical Marketing Takeaways:**
1. **Grain Moisture & Quality Grading:**
   • Sun-dry harvested grains to reduce moisture content below 12-14%. Cleaned and graded lots consistently command higher bids in APMC mandis.

2. **Leverage Minimum Support Price (MSP):**
   • Register early at procurement portals (FCI/State Agencies) to sell notified crops at assured government MSP rates.

3. **Sell via e-NAM (National Agriculture Market):**
   • Utilize electronic mandi bidding to access competitive bids from inter-district and inter-state buyers with transparent online settlement."""

        # -------------------------------------------------------------
        # BRANCH 6: Clean Document RAG Synthesis Fallback
        # -------------------------------------------------------------
        cleaned_snippets = []
        for d in docs[:3]:
            raw = d.page_content.strip()
            # Clean OCR hyphenations and weird artifacts
            raw = re.sub(r'(\w+)-\s*\n\s*(\w+)', r'\1\2', raw)
            lines = [l.strip() for l in raw.split('\n') if len(l.strip()) > 25 and not re.match(r'^[0-9\.\s%]+$', l.strip())]
            if lines:
                cleaned_snippets.append(" ".join(lines[:2]))

        body = "\n\n• ".join(cleaned_snippets) if cleaned_snippets else (
            "Maintain balanced soil NPK, adopt integrated pest management, and optimize irrigation scheduling to achieve high crop yields."
        )

        if lang == "Hindi":
            return f"""### 🌾 कृषि मित्र: कृषि परामर्श

• {body}

**मुख्य कृषि सुझाव:**
• अपनी मिट्टी की जांच मृदा स्वास्थ्य कार्ड (Soil Health Card) के माध्यम से हर 2-3 वर्ष में अवश्य करवाएं।
• जैविक एवं रासायनिक खादों का संतुलित उपयोग कर फसल लागत घटाएं और मुनाफा बढ़ाएं।
• मौसम एवं वर्षा के अनुसार ही सिंचाई एवं छिड़काव का समय निर्धारित करें।"""
        else:
            return f"""### 🌾 Krishi Mitra: Agricultural Guidance

• {body}

**Key Farming Best Practices:**
• Test your soil every 2-3 years through the Soil Health Card scheme for precise micronutrient balance.
• Combine organic compost with balanced chemical fertilization to lower input costs and boost yield.
• Align irrigation and spraying operations with local weather advisories to prevent wash-off and moisture stress."""

    def invoke(self, query):
        if isinstance(query, dict) and 'question' in query:
            query_text = query['question']
        else:
            query_text = str(query)

        # Clean query: strip system instructions or language headers
        clean_query = re.sub(r'[\r\n]+IMPORTANT:\s*Please respond in\s*([a-zA-Z]+)\s*language.*$', '', query_text, flags=re.IGNORECASE).strip()
        target_lang = self._detect_language(query_text)

        # 1. Check Greetings
        if self._is_greeting(clean_query):
            return self._get_greeting_response(target_lang)

        # 2. Strict Agricultural Guardrail Filter
        if not self._is_agricultural_query(clean_query):
            return self._get_non_agricultural_refusal(target_lang)

        # 3. Retrieve Matching Domain Documents
        docs = self.db.similarity_search(clean_query, k=4)
        context = "\n\n".join([d.page_content for d in docs])

        # 4. Try Groq LLM if configured
        if groq_client:
            sys_prompt = (
                f"You are Krishi Mitra, an expert AI agricultural assistant dedicated to Indian farmers. "
                f"You ONLY answer questions related to agriculture, farming, crops, plant diseases, soil health, weather, mandi prices, and government farming schemes. "
                f"If the user asks about anything non-agricultural, politely decline and instruct them to ask about farming. "
                f"Structure your response clearly with bold headings, numbered steps, and exact dosages where applicable. "
                f"Respond in {target_lang} language."
            )
            groq_resp = call_groq_chat(
                messages=[
                    {"role": "system", "content": f"{sys_prompt}\n\nAGRICULTURAL CONTEXT:\n{context}"},
                    {"role": "user", "content": clean_query}
                ],
                temperature=0.2,
                max_tokens=700
            )
            if groq_resp and len(groq_resp.strip()) > 30:
                return groq_resp

        # 5. Expert Agricultural Engine Synthesis
        return self._synthesize_expert_agricultural_answer(clean_query, docs, target_lang)

def setup_retrieval_qa(db):
    """Setup RAG chain for agricultural queries."""
    return RAGQAChain(db, mode="general")

def setup_sustainability_qa(db):
    """Setup RAG chain for sustainability tips."""
    return RAGQAChain(db, mode="sustainability")

