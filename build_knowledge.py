import os
import json
import csv
import PyPDF2

def build_corpus():
    chunks = []

    # 1. Government Schemes CSV
    schemes_path = 'train/dataset/govt_schemes.csv'
    if os.path.exists(schemes_path):
        with open(schemes_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                s_name = row.get('scheme_name', '').strip()
                f_name = row.get('full_name', '').strip()
                desc = row.get('description', '').strip()
                elig = row.get('eligibility', '').strip()
                ben = row.get('benefits', '').strip()
                cat = row.get('category', '').strip()
                web = row.get('website', '').strip()
                
                text = (
                    f"GOVERNMENT SCHEME: {s_name} ({f_name})\n"
                    f"Category: {cat}\n"
                    f"Key Objective: {desc}\n"
                    f"Farmer Eligibility: {elig}\n"
                    f"Direct Financial Benefits: {ben}\n"
                    f"Official Application Portal: {web}"
                )
                chunks.append({'source': 'govt_schemes.csv', 'title': s_name, 'text': text})

    # 2. Crop Guides CSV
    guides_path = 'train/dataset/crop_guides.csv'
    if os.path.exists(guides_path):
        with open(guides_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                crop = row.get('crop', '').strip().upper()
                text = (
                    f"CROP AGRONOMY GUIDE: {crop}\n"
                    f"Crop: {crop}\n"
                    f"Irrigation & Watering Schedule: {row.get('watering_schedule', '')}\n"
                    f"Fertilizer & NPK Management: {row.get('fertilizer_plan', '')}\n"
                    f"Crop Maturity & Growth Duration: {row.get('duration_days', '')} days\n"
                    f"Optimal Temperature: {row.get('ideal_temp_min', '')}°C to {row.get('ideal_temp_max', '')}°C\n"
                    f"Optimal Relative Humidity: {row.get('ideal_humidity_min', '')}% to {row.get('ideal_humidity_max', '')}%\n"
                    f"Soil & Nutrient Advice: Ensure balanced NPK application, soil pH between 6.0-7.5, and zinc/iron supplementation."
                )
                chunks.append({'source': 'crop_guides.csv', 'title': f"{crop} Cultivation Guide", 'text': text})

    # 3. Comprehensive Crop Disease & Pest Control Knowledge Base
    crop_diseases = [
        {
            'title': 'Wheat Yellow & Brown Rust (Puccinia spp.)',
            'text': (
                "Wheat Yellow Rust (Stripe Rust) and Brown Rust (Leaf Rust):\n"
                "Symptoms: Yellow-orange or brown pustules arranged in parallel stripes on leaves, causing premature drying.\n"
                "Chemical Treatment: Spray Propiconazole 25% EC (Tilt) @ 1 ml/L or Tebuconazole 25.9% EC @ 1 ml/L upon first appearance of yellow pustules. Repeat after 15 days if necessary.\n"
                "Organic & Cultural Control: Grow rust-resistant varieties (HD 2967, HD 3086, DBW 187, DBW 222). Avoid late sowing and excessive nitrogen fertilization."
            )
        },
        {
            'title': 'Paddy Rice Blast (Magnaporthe oryzae) and Brown Spot',
            'text': (
                "Paddy Rice Blast and Brown Leaf Spot:\n"
                "Symptoms: Spindle-shaped/diamond lesions with grey centers and brown margins on leaves and panicles; neck blast causes panicle breakage and chaffy grains.\n"
                "Chemical Treatment: Spray Tricyclazole 75% WP @ 0.6 g/L or Isoprothiolane 40% EC @ 1.5 ml/L at tillering and boot leaf stages. For brown spot, spray Mancozeb 75% WP @ 2.5 g/L.\n"
                "Organic Control: Seed treatment with Trichoderma harzianum @ 5g/kg seed. Apply Pseudomonas fluorescens @ 2.5 kg/ha in soil with FYM."
            )
        },
        {
            'title': 'Paddy Khaira Disease (Zinc Deficiency)',
            'text': (
                "Khaira Disease in Paddy (Rice):\n"
                "Cause: Severe micronutrient Zinc (Zn) deficiency occurring commonly in waterlogged, alkaline calcareous soils.\n"
                "Symptoms: Yellowing between veins in young leaves 2-3 weeks after transplanting; rusty bronze or reddish-brown spots merge and leaves wither.\n"
                "Correction & Treatment: Foliar spray of Zinc Sulphate (ZnSO4 21%) @ 5 kg + 2.5 kg slaked lime in 1000 liters of water per hectare (or 5g ZnSO4 + 2.5g lime per liter). Apply basal Zinc Sulphate @ 25 kg/ha during field preparation."
            )
        },
        {
            'title': 'Potato and Tomato Late Blight (Phytophthora infestans)',
            'text': (
                "Potato and Tomato Late Blight:\n"
                "Symptoms: Water-soaked, dark brown to black irregular lesions on leaf margins with white mildew underneath during high humidity; rapid vine rot and tuber blighting.\n"
                "Chemical Treatment: Preventive spray of Mancozeb 75% WP @ 2.5 g/L or Copper Oxychloride 50% WP @ 3 g/L. Upon outbreak, spray systemic Cymoxanil + Mancozeb (Curzate) @ 2.5 g/L or Metalaxyl + Mancozeb (Ridomil Gold) @ 2.5 g/L.\n"
                "Organic & Cultural: Destroy infected haulms before harvest; provide good furrow drainage and avoid overhead sprinkler watering."
            )
        },
        {
            'title': 'Cotton Pink Bollworm and Sucking Pests (Whitefly, Aphids)',
            'text': (
                "Cotton Pink Bollworm (Pectinophora gossypiella) and Sucking Pests (Whitefly, Thrips, Jassids):\n"
                "Symptoms: Rosetted flowers, drilled squares and bolls, damaged lint and premature boll dropping. Sucking pests cause leaf curling and honeydew mold.\n"
                "Pink Bollworm Management: Install Pheromone Traps (Gossyplure) @ 8-10 traps/acre. Spray Emamectin Benzoate 5% SG @ 0.5 g/L or Chlorantraniliprole 18.5% SC (Coragen) @ 0.3 ml/L.\n"
                "Sucking Pests & Whiteflies: Install Yellow Sticky Traps @ 15-20/acre. Spray Neem Oil 1500 ppm @ 5 ml/L or Diafenthiuron 50% WP @ 1.2 g/L or Flonicamid 50% WG @ 0.3 g/L."
            )
        },
        {
            'title': 'Mustard Aphid (Lipaphis erysimi) and White Rust',
            'text': (
                "Mustard / Rapeseed Aphids and White Rust (Albugo candida):\n"
                "Symptoms: Tiny greenish aphids suck sap from inflorescence, pods, and tender shoots, stunting pod formation. White rust causes chalky blisters on leaf undersides and stag-head floral malformation.\n"
                "Aphid Management: Early sowing before October 15 escapes aphid attack. Spray Dimethoate 30% EC @ 1.5 ml/L or Thiamethoxam 25% WG @ 0.25 g/L when aphid colony exceeds 25 insects per 10 cm terminal branch.\n"
                "White Rust Treatment: Spray Mancozeb 75% WP @ 2 g/L or Ridomil Gold @ 2 g/L."
            )
        },
        {
            'title': 'Maize Fall Armyworm (Spodoptera frugiperda)',
            'text': (
                "Maize Fall Armyworm (FAW):\n"
                "Symptoms: Pin holes, ragged shot-hole feeding on leaves, heavy sawdust-like frass inside leaf whorl, destroyed central growing shoot.\n"
                "Management: Handpicking egg masses in small plots; application of neem cake in soil. Spray Chlorantraniliprole 18.5% SC @ 0.4 ml/L or Spinetoram 11.7% SC @ 0.5 ml/L directed into leaf whorls. Apply biological Metarhizium anisopliae or Beauveria bassiana @ 5 g/L."
            )
        },
        {
            'title': 'Chilli and Vegetable Leaf Curl Virus (Gemini Virus)',
            'text': (
                "Chilli Leaf Curl Virus and Tomato Leaf Curl:\n"
                "Vector: Transmitted by Whiteflies (Bemisia tabaci) and Thrips.\n"
                "Symptoms: Upward curling and crinkling of leaves, reduced leaf size, stunted bushy plants with no fruit setting.\n"
                "Treatment: Viruses cannot be cured by fungicides; control the insect vector promptly! Install yellow and blue sticky traps (15/acre). Spray Fipronil 5% SC @ 2 ml/L or Imidacloprid 17.8% SL @ 0.5 ml/L or Neem Oil @ 5 ml/L. Uproot and burn severely infected plants."
            )
        },
        {
            'title': 'Gram / Chickpea Fusarium Wilt and Pod Borer',
            'text': (
                "Gram (Chickpea) Fusarium Wilt and Helicoverpa Pod Borer:\n"
                "Wilt Symptoms: Sudden drooping of leaves, vascular browning inside stem root xylem.\n"
                "Wilt Management: Deep summer ploughing; seed treatment with Trichoderma viride @ 5g/kg seed or Carbendazim @ 2g/kg. Crop rotation with wheat or mustard.\n"
                "Pod Borer: Install Pheromone Traps (Helilure) @ 5/acre. Spray NPV (Nuclear Polyhedrosis Virus) @ 250 LE/ha or Emamectin Benzoate 5% SG @ 0.5 g/L during pod formation."
            )
        }
    ]
    for d in crop_diseases:
        chunks.append({'source': 'crop_diseases_expert', 'title': d['title'], 'text': d['text']})

    # 4. Soil Fertility, Fertilizers & Organic Farming
    soil_topics = [
        {
            'title': 'Balanced NPK Fertilizer Management and Dosage',
            'text': (
                "Balanced NPK Fertilizer Application:\n"
                "General Ideal Ratio: 4:2:1 (N:P2O5:K2O) for cereal crops (Wheat, Paddy, Maize); 1:2:1 for pulse legumes (Gram, Moong, Arhar) since legumes fix atmospheric nitrogen.\n"
                "Nitrogen (Urea 46% N): Apply 50% basal at sowing, 25% at active tillering, and 25% at panicle/flowering initiation. Avoid excess urea which causes lodging and disease vulnerability.\n"
                "Phosphorus (DAP 18:46:0 or SSP 16% P2O5): 100% applied as basal dose placed near root zone during final ploughing for root elongation.\n"
                "Potassium (Muriate of Potash MOP 60% K2O): Crucial for grain weight, starch formation, drought resistance, and pest protection."
            )
        },
        {
            'title': 'Organic Manures, Vermicompost, and FYM',
            'text': (
                "Farm Yard Manure (FYM) and Vermicompost:\n"
                "FYM Dosage: Apply 8-10 tons/hectare of well-decomposed FYM 3-4 weeks before sowing and incorporate thoroughly.\n"
                "Vermicompost: Rich organic manure produced by earthworms (Eisenia fetida). Dose: 2.5-3 tons/ha for field crops; 5 kg per fruit tree. Increases soil water retention by 25% and improves beneficial microbial count.\n"
                "Green Manuring: Sowing Sunnhemp (Crotalaria juncea) or Dhaincha (Sesbania aculeata) and ploughing into the soil at 45 days adds 60-80 kg organic nitrogen per hectare."
            )
        },
        {
            'title': 'Jeevamrit & Natural Farming Organic Formulations',
            'text': (
                "Jeevamrit Organic Biostimulant Preparation (Subhash Palekar Natural Farming):\n"
                "Ingredients (for 1 acre): 200 Liters water, 10 kg fresh desi cow dung, 5-10 Liters desi cow urine, 2 kg jaggery (gur), 2 kg pulse flour (besan), handful of virgin fertile field soil.\n"
                "Preparation: Mix in a drum kept in shade. Stir clockwise twice daily. Ferment for 4-7 days.\n"
                "Application: Filter through cloth and apply through irrigation water or spray as 10% foliar biostimulant. Multiplies native soil beneficial microbes."
            )
        },
        {
            'title': 'Soil Health Card Scheme & Soil Testing Guide',
            'text': (
                "Soil Health Card (SHC) & Soil Testing Procedure:\n"
                "Soil Sampling: Collect V-shaped soil samples up to 15 cm depth from 8-10 spots across the field in zigzag pattern. Mix, dry in shade, and test via District Soil Testing Laboratory or Krishi Vigyan Kendra.\n"
                "12 Parameters Tested: Macro nutrients (N, P, K), Secondary nutrients (Sulphur), Micronutrients (Zinc, Iron, Copper, Manganese, Boron), and Physical parameters (pH, Electrical Conductivity EC, Organic Carbon OC).\n"
                "Benefits: Saves 20-30% on unnecessary fertilizer costs and prevents soil degradation."
            )
        }
    ]
    for s in soil_topics:
        chunks.append({'source': 'soil_fertility_expert', 'title': s['title'], 'text': s['text']})

    # 5. Precision Water Management & Irrigation
    irrigation_topics = [
        {
            'title': 'Drip and Micro-Sprinkler Irrigation Techniques',
            'text': (
                "Precision Irrigation Systems:\n"
                "Drip Irrigation: Delivers water directly to crop root zone with 90-95% efficiency, reducing water consumption by 40-60% compared to flood irrigation. Best suited for sugarcane, cotton, fruit orchards, and vegetables. Reduces weed emergence.\n"
                "Sprinkler Irrigation: Suitable for undulating terrains and sandy soils; ideal for wheat, mustard, pulses, and groundnut with 75-80% efficiency.\n"
                "Government Subsidy: Available up to 55-70% for small & marginal farmers under Pradhan Mantri Krishi Sinchayee Yojana (PMKSY - Per Drop More Crop)."
            )
        },
        {
            'title': 'Alternate Wetting and Drying (AWD) in Paddy',
            'text': (
                "Alternate Wetting and Drying (AWD) Water Saving in Paddy Rice:\n"
                "Technique: Instead of keeping continuous ponded water, allow field water to subside until water table drops 15 cm below soil surface (monitored with perforated PVC field pipe), then re-irrigate.\n"
                "Benefits: Saves 25-35% irrigation water, enhances root aeration, reduces methane greenhouse gas emissions by 40%, and prevents lodging without any yield reduction."
            )
        }
    ]
    for ir in irrigation_topics:
        chunks.append({'source': 'irrigation_expert', 'title': ir['title'], 'text': ir['text']})

    # 6. Mandi Bhav, Minimum Support Price (MSP) & Market Strategy
    mandi_topics = [
        {
            'title': 'Minimum Support Price (MSP) and APMC Mandi Marketing',
            'text': (
                "MSP (Minimum Support Price) and Grain Marketing:\n"
                "Definition: Guaranteed price fixed by Government of India based on recommendations of CACP (Commission for Agricultural Costs and Prices) ensuring at least 50% profit over Cost of Cultivation (A2+FL).\n"
                "Key Crops under MSP: Paddy, Wheat, Cotton, Maize, Gram, Mustard, Soybean, Sugarcane (FRP), Groundnut, Tur/Arhar, Moong, Urad, Bajra, Jowar.\n"
                "Post-Harvest Tips for Higher Mandi Price: Dry grains to optimum moisture (under 12-14% for cereals and oilseeds); clean and grade grains to eliminate dust and chaff; avoid selling under distress; use e-NAM (National Agriculture Market) for online inter-mandi bidding."
            )
        }
    ]
    for m in mandi_topics:
        chunks.append({'source': 'mandi_economics', 'title': m['title'], 'text': m['text']})

    # 7. Farming Schemes PDF extraction if available
    schemes_pdf = 'Data/Farming Schemes.pdf'
    if os.path.exists(schemes_pdf):
        try:
            reader = PyPDF2.PdfReader(schemes_pdf)
            for i in range(min(45, len(reader.pages))):
                page_text = reader.pages[i].extract_text()
                if page_text and len(page_text.strip()) > 80:
                    for piece in [page_text[j:j+600] for j in range(0, len(page_text), 500)]:
                        if len(piece.strip()) > 80:
                            chunks.append({'source': 'Farming Schemes.pdf', 'title': f'Farming Schemes Pg {i+1}', 'text': piece.strip()})
        except Exception as e:
            print(f"Notice reading schemes PDF: {e}")

    # 8. Farmerbook PDF extraction if available
    farmerbook_pdf = 'Data/farmerbook.pdf'
    if os.path.exists(farmerbook_pdf):
        try:
            reader = PyPDF2.PdfReader(farmerbook_pdf)
            for i in range(min(40, len(reader.pages))):
                page_text = reader.pages[i].extract_text()
                if page_text and len(page_text.strip()) > 80:
                    for piece in [page_text[j:j+600] for j in range(0, len(page_text), 500)]:
                        if len(piece.strip()) > 80:
                            chunks.append({'source': 'farmerbook.pdf', 'title': f'Farmerbook Pg {i+1}', 'text': piece.strip()})
        except Exception as e:
            print(f"Notice reading farmerbook PDF: {e}")

    os.makedirs('Data', exist_ok=True)
    out_file = 'Data/knowledge_corpus.json'
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Built enriched agricultural knowledge corpus with {len(chunks)} chunks -> {out_file}")

if __name__ == '__main__':
    build_corpus()
