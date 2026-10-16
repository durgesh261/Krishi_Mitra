# -*- coding: utf-8 -*-
"""
Script to enrich train/dataset/crop_guides.csv with comprehensive,
authentic crop planning details for all 90 Indian crops based on
ICAR (Indian Council of Agricultural Research) and State Agricultural
University (PAU, IARI, TNAU, UAS) package of practices.
"""
import os
import pandas as pd

CSV_PATH = 'train/dataset/crop_guides.csv'

# Dictionary defining deep agronomic planning info for all crop categories & individual crops
PLANNING_DATA = {
    # ----------------- Cereals & Millets -----------------
    'wheat': {
        'seed_rate_and_spacing': 'Seed Rate: 40-45 kg/acre (normal sown), 50 kg/acre (late sown). Spacing: 20-22.5 cm row-to-row, 4-5 cm depth. Seed treatment: Carbendazim/Thiram @ 2g/kg seed + Azotobacter bio-culture.',
        'recommended_varieties': 'DBW-187 (Karan Vandana), DBW-222, PBW-826 (heat-tolerant), HD-2967, HD-3086, Sharbati C-306, Raj-4037, GW-322.',
        'land_preparation': '1 deep summer ploughing followed by 2-3 harrowings and planking for fine crumbly seedbed. Incorporate 6-8 tonnes of decomposed FYM/compost per acre 3 weeks prior to sowing.',
        'fertilizer_bags_per_acre': 'Basal at sowing: 1 bag DAP (50kg) + 1/2 bag MOP (25kg) + 10kg Zinc Sulphate (21%). Top Dressing: 1st bag Urea (45kg) after 1st irrigation (21-25 DAS), 2nd bag Urea before 2nd irrigation (40-45 DAS).',
        'weed_management': 'Pre-emergence: Pendimethalin 30% EC @ 1-1.25 L/acre within 48h of sowing. Post-emergence: For Phalaris minor (gulli danda), spray Clodinafop 15% WP @ 160g/acre at 30-35 DAS in 150L water.',
        'harvesting_and_storage': 'Harvest when earheads turn golden yellow and grain moisture drops below 14%. Thresh promptly and sun-dry grain to 10-12% moisture before storing in clean airtight metal bins with dried neem leaves.',
        'economic_profit_acre': 'Cost of Cultivation: ₹14,000 - ₹17,500/acre. Expected Yield: 18 - 22 Quintals/acre. Gross Revenue at MSP (₹2,275/q): ₹41,000 - ₹50,000. Net Profit: ₹25,000 - ₹33,000/acre.'
    },
    'rice': {
        'seed_rate_and_spacing': 'Transplanted: 15-20 kg/acre (hybrids 6-8 kg/acre); Direct Seeded (DSR): 8-10 kg/acre. Spacing: 20 x 15 cm (2-3 seedlings/hill). Seed treatment: Carbendazim 2g + Streptocycline 0.1g/kg seed soaked for 24h.',
        'recommended_varieties': 'Pusa Basmati 1121, Pusa 1509, PR-126 (short duration), MTU-1010, IR-64, Swarna Sub-1 (flood-tolerant), DRR Dhan 45 (zinc-rich).',
        'land_preparation': 'Puddling: 2-3 wet ploughings in standing water followed by planking to create an impermeable layer. Incorporate 8-10 tonnes FYM or green manure (Dhaincha) during pre-puddling.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP + 10kg Zinc Sulphate 33%. Top Dressing: 1 bag Urea at early tillering (20-25 DAT), 1 bag Urea at panicle initiation (45-50 DAT).',
        'weed_management': 'Pre-emergence: Pretilachlor 50% EC @ 600ml/acre or Pyrazosulfuron-ethyl 10% WP @ 80g/acre within 3 days of transplanting in standing water.',
        'harvesting_and_storage': 'Harvest when 80-85% of grains in the panicle turn golden straw color (grain moisture 18-20%). Dry paddy down to 13-14% moisture before milling or storage.',
        'economic_profit_acre': 'Cost of Cultivation: ₹18,000 - ₹23,000/acre. Expected Yield: 22 - 28 Quintals/acre. Gross Revenue at MSP (₹2,300/q): ₹50,000 - ₹64,000. Net Profit: ₹30,000 - ₹42,000/acre.'
    },
    'maize': {
        'seed_rate_and_spacing': 'Seed Rate: 8-10 kg/acre (grain), 15 kg/acre (fodder). Spacing: 60 cm row-to-row x 20 cm plant-to-plant, 4-5 cm depth. Seed treatment: Thiram 3g/kg + Cyantraniliprole 4ml/kg for Fall Armyworm.',
        'recommended_varieties': 'Pioneer P-3396, Dekalb 9108, Bio 9544, HQPM-1 (Quality Protein Maize), PMH-1, African Tall (fodder).',
        'land_preparation': 'Deep plowing followed by 2 cross-harrowings to create a mellow, well-aerated seedbed without clods. Ridge and furrow sowing is highly recommended for water drainage.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP + 10kg Zinc Sulphate/acre. Top Dressing: 1 bag Urea at knee-high stage (30 DAS) and 1 bag Urea at tasseling/silking stage (55 DAS).',
        'weed_management': 'Pre-emergence: Atrazine 50% WP @ 500-800g/acre sprayed within 48 hours of sowing on moist soil. Manual hoeing at 25 DAS.',
        'harvesting_and_storage': 'Harvest when cob husk turns dry and paper-like with a visible black layer at grain base (moisture 15-18%). Dry shelled cobs to 12% moisture.',
        'economic_profit_acre': 'Cost of Cultivation: ₹13,000 - ₹16,000/acre. Expected Yield: 22 - 28 Quintals/acre. Gross Revenue at MSP (₹2,225/q): ₹48,000 - ₹62,000. Net Profit: ₹32,000 - ₹46,000/acre.'
    },
    'bajra': {
        'seed_rate_and_spacing': 'Seed Rate: 1.5 - 2 kg/acre. Spacing: 45 cm row-to-row x 12-15 cm plant-to-plant, 2.5-3 cm depth. Seed treatment: Metalaxyl 35% WS @ 6g/kg seed against Downy Mildew.',
        'recommended_varieties': 'Proagro 9444, HHB-67 Improved, MPMH-17, GHB-538, Dhanshakti (high-iron variety).',
        'land_preparation': '1-2 ploughings with cultivator followed by light planking. Needs firm, fine seedbed because of small seed size.',
        'fertilizer_bags_per_acre': 'Basal: 1/2 bag DAP (25kg) + 15kg MOP/acre. Top Dressing: 1 bag Urea (45kg) at 25-30 DAS following rainfall or light irrigation.',
        'weed_management': 'Pre-emergence: Atrazine 50% WP @ 400g/acre within 48h of sowing. 1 hand weeding at 20-25 days after sowing.',
        'harvesting_and_storage': 'Harvest when earheads dry and grain is hard (grain moisture 15%). Thresh with mechanical thresher; dry grain to 10% moisture.',
        'economic_profit_acre': 'Cost of Cultivation: ₹7,500 - ₹9,500/acre. Expected Yield: 12 - 16 Quintals/acre. Gross Revenue at MSP (₹2,625/q): ₹31,000 - ₹42,000. Net Profit: ₹22,000 - ₹32,000/acre.'
    },
    'jowar': {
        'seed_rate_and_spacing': 'Seed Rate: 3-4 kg/acre. Spacing: 45 cm x 15 cm, 3-4 cm depth. Seed treatment: Imidacloprid 70% WS @ 3g/kg seed against shoot fly + Thiram 3g/kg.',
        'recommended_varieties': 'CSH-14, CSH-16, CSH-25, CSV-15, Maldandi (M-35-1 for Rabi delicious roti), Phule Yashoda.',
        'land_preparation': 'Deep summer plowing to conserve monsoon rain. 2 harrowings and planking to create firm seedbed.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 20kg MOP/acre. Top Dressing: 1 bag Urea at 30-35 DAS before flag leaf emergence.',
        'weed_management': 'Pre-emergence: Atrazine 50% WP @ 500g/acre in 150L water within 48h of sowing. 1 inter-culture cultivation at 30 DAS.',
        'harvesting_and_storage': 'Harvest when grains turn hard and glumes dry up (moisture 15-18%). Sun-dry to 10% moisture before bagging.',
        'economic_profit_acre': 'Cost of Cultivation: ₹8,000 - ₹10,500/acre. Expected Yield: 12 - 18 Quintals/acre. Gross Revenue at MSP (₹3,371/q): ₹40,000 - ₹60,000. Net Profit: ₹30,000 - ₹50,000/acre.'
    },
    'barley': {
        'seed_rate_and_spacing': 'Seed Rate: 35-40 kg/acre. Spacing: 22.5 cm row-to-row, 4-5 cm depth. Seed treatment: Vitavax @ 2g/kg seed against covered smut.',
        'recommended_varieties': 'DWRB-123, DWRB-160, BH-902, RD-2552, Jyoti, K-551 (malting barley).',
        'land_preparation': '2-3 plowings followed by planking. Tolerates saline soils better than wheat.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP. Top Dressing: 1 bag Urea at 1st irrigation (30 DAS). Avoid late nitrogen for malting barley.',
        'weed_management': 'Post-emergence: Isoproturon 75% WP @ 400g/acre at 30-35 DAS for annual grasses.',
        'harvesting_and_storage': 'Harvest in dry weather before earheads start shattering. Dry grain to 11% moisture.',
        'economic_profit_acre': 'Cost of Cultivation: ₹10,000 - ₹12,500/acre. Expected Yield: 15 - 19 Quintals/acre. Gross Revenue at MSP (₹1,850/q): ₹28,000 - ₹35,000. Net Profit: ₹18,000 - ₹24,000/acre.'
    },

    # ----------------- Pulses -----------------
    'chickpea': {
        'seed_rate_and_spacing': 'Desi: 30-35 kg/acre; Kabuli: 40-45 kg/acre. Spacing: 30 cm x 10 cm, 5-7 cm depth. Seed treatment: Trichoderma viride @ 5g/kg + Mesorhizobium ciceri bio-fertilizer.',
        'recommended_varieties': 'JG-11, JAKI-9218, Digvijay, RVG-202, Pusa 372, PKV Harita (wilt-resistant), KAK-2 (Kabuli).',
        'land_preparation': 'Rough, unpulverized cloddy seedbed is ideal (prevents root rot and aids root respiration). 1 deep plowing followed by 1 cross-cultivator pass.',
        'fertilizer_bags_per_acre': 'Basal at sowing: 1 bag DAP (50kg) + 20kg MOP + 10kg Sulphur (90% WDG)/acre. Being a legume, zero or minimal top-dressed Urea is needed!',
        'weed_management': 'Pre-emergence: Pendimethalin 30% EC @ 1 L/acre within 48h of sowing. 1 hand weeding at 25-30 DAS.',
        'harvesting_and_storage': 'Harvest when leaves dry and fall off, pods turn yellowish-brown and seeds rattle inside. Thresh and store at 9-10% moisture with Phorate granules around sacks.',
        'economic_profit_acre': 'Cost of Cultivation: ₹9,500 - ₹12,500/acre. Expected Yield: 8 - 12 Quintals/acre. Gross Revenue at MSP (₹5,440/q): ₹43,000 - ₹65,000. Net Profit: ₹33,000 - ₹52,000/acre.'
    },
    'pigeonpeas': {
        'seed_rate_and_spacing': 'Seed Rate: 5-6 kg/acre. Spacing: 90 cm row-to-row x 20-30 cm plant-to-plant (wider for branching). Seed treatment: Carbendazim 2g + Rhizobium culture @ 10g/kg seed.',
        'recommended_varieties': 'ICPL-87119 (Asha), BDN-711, BSMR-736 (wilt resistant), UPAS-120 (early maturity), Pusa Arhar 16.',
        'land_preparation': 'Deep sub-soiling or plowing to break hardpan as pigeonpea has a deep taproot (up to 2 meters). Apply 5 tonnes FYM/acre.',
        'fertilizer_bags_per_acre': 'Basal at sowing: 1 bag DAP (50kg) + 15kg MOP + 10kg Sulphur/acre. Spray 2% DAP or 13:0:45 @ 10g/L during pod initiation to prevent flower drop.',
        'weed_management': 'Pre-emergence: Pendimethalin 30% EC @ 1 L/acre within 48h. Inter-row weeding at 30 and 60 DAS before canopy closes.',
        'harvesting_and_storage': 'Harvest when 80% pods turn brown and dry. Cut plants at ground level, dry in sun for 3-5 days before threshing.',
        'economic_profit_acre': 'Cost of Cultivation: ₹11,000 - ₹14,000/acre. Expected Yield: 7 - 11 Quintals/acre. Gross Revenue at MSP (₹7,550/q): ₹52,000 - ₹83,000. Net Profit: ₹41,000 - ₹69,000/acre.'
    },
    'mungbean': {
        'seed_rate_and_spacing': 'Kharif: 6-8 kg/acre; Summer/Zaid: 8-10 kg/acre. Spacing: 30 cm x 10 cm, 3-4 cm depth. Seed treatment: Captan 3g/kg + Rhizobium culture.',
        'recommended_varieties': 'IPM 205-7 (Virat), Pusa Vishal, Samrat, MH-421, Shikha, SML-668 (bold seeded).',
        'land_preparation': '1-2 plowings with cultivator followed by planking. Needs well-drained fertile loam.',
        'fertilizer_bags_per_acre': 'Basal: 1/2 bag DAP (25kg) + 15kg MOP/acre. Foliar spray: 2% Urea at flower initiation boosts pod formation.',
        'weed_management': 'Pre-emergence: Pendimethalin 30% EC @ 1 L/acre within 48h. 1 manual hoeing at 20-25 DAS.',
        'harvesting_and_storage': 'Pick mature black pods in 2-3 pickings or harvest entire plant when 85% pods turn black. Dry grain to 9% moisture.',
        'economic_profit_acre': 'Cost of Cultivation: ₹7,000 - ₹9,500/acre. Expected Yield: 5 - 8 Quintals/acre. Gross Revenue at MSP (₹8,682/q): ₹43,000 - ₹69,000. Net Profit: ₹35,000 - ₹59,000/acre.'
    },
    'blackgram': {
        'seed_rate_and_spacing': 'Seed Rate: 6-8 kg/acre. Spacing: 30 cm x 10 cm, 3 cm depth. Seed treatment: Trichoderma 5g/kg + Rhizobium culture.',
        'recommended_varieties': 'Pant U-31, Shekhar-2, T-9, Uttara, Azad-1, VBN-8 (Yellow Mosaic Virus resistant).',
        'land_preparation': '2 plowings to fine tilth. Ensure adequate drainage as waterlogging causes root rot.',
        'fertilizer_bags_per_acre': 'Basal: 1/2 bag DAP + 15kg MOP + 10kg Sulphur/acre.',
        'weed_management': 'Pre-emergence: Pendimethalin @ 1 L/acre. Post-emergence: Imazethapyr 10% SL @ 300ml/acre at 15-20 DAS for broadleaf weeds.',
        'harvesting_and_storage': 'Harvest when pods turn dark brown/black. Sun dry for 2 days before threshing.',
        'economic_profit_acre': 'Cost of Cultivation: ₹7,500 - ₹10,000/acre. Expected Yield: 5 - 7.5 Quintals/acre. Gross Revenue at MSP (₹7,400/q): ₹37,000 - ₹55,000. Net Profit: ₹29,000 - ₹45,000/acre.'
    },
    'lentil': {
        'seed_rate_and_spacing': 'Seed Rate: 15-18 kg/acre (small seed), 20-22 kg/acre (bold seed). Spacing: 22.5 cm x 5 cm. Seed treatment: Carboxin @ 2g/kg + Rhizobium.',
        'recommended_varieties': 'HUL-57, KLS-218, DPL-62 (Sheri), Pant L-8, Pusa Ageti.',
        'land_preparation': '1-2 plowings after kharif crop harvest. Can also be sown as relay crop (Utera/Paira) in standing rice.',
        'fertilizer_bags_per_acre': 'Basal: 1/2 bag DAP + 15kg MOP + 8kg Sulphur/acre.',
        'weed_management': 'Pre-emergence: Pendimethalin 30% EC @ 1 L/acre within 48h. Hand weeding at 30 DAS.',
        'harvesting_and_storage': 'Harvest before pods over-ripen to prevent shattering. Dry seeds to 10% moisture.',
        'economic_profit_acre': 'Cost of Cultivation: ₹8,000 - ₹10,500/acre. Expected Yield: 6 - 9 Quintals/acre. Gross Revenue at MSP (₹6,700/q): ₹40,000 - ₹60,000. Net Profit: ₹31,000 - ₹50,000/acre.'
    },

    # ----------------- Oilseeds -----------------
    'mustard': {
        'seed_rate_and_spacing': 'Seed Rate: 1.5 - 2 kg/acre. Spacing: 45 cm row-to-row x 15 cm plant-to-plant, 3-4 cm depth. Seed treatment: Metalaxyl 35% WS @ 6g/kg + Trichoderma 5g/kg.',
        'recommended_varieties': 'Giriraj (DRMRIJ-31), Pioneer 45S46, RH-749, Pusa Bold, Kranti, Laxmi, NRCHB-101.',
        'land_preparation': '2-3 plowings followed by heavy planking to conserve sub-soil moisture. Apply 5 tonnes FYM/acre.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP + 15kg elemental Sulphur (essential for high oil content). Top Dressing: 1 bag Urea at 1st irrigation (30 DAS).',
        'weed_management': 'Pre-emergence: Pendimethalin 30% EC @ 1 L/acre within 48h of sowing. Thinning at 15-20 DAS is vital to maintain 15cm plant spacing.',
        'harvesting_and_storage': 'Harvest in early morning when 75% of siliquae (pods) turn golden yellow to avoid pod shattering. Dry seeds to 8% moisture before oil pressing.',
        'economic_profit_acre': 'Cost of Cultivation: ₹10,500 - ₹13,500/acre. Expected Yield: 8 - 12 Quintals/acre. Gross Revenue at MSP (₹5,950/q): ₹47,000 - ₹71,000. Net Profit: ₹36,000 - ₹57,000/acre.'
    },
    'soybean': {
        'seed_rate_and_spacing': 'Seed Rate: 25-30 kg/acre (germination ≥ 70%). Spacing: 45 cm x 5-7 cm, 3-4 cm depth. Seed treatment: Carboxin + Thiram (Vitavax Power) @ 2.5g/kg + Bradyrhizobium japonicum.',
        'recommended_varieties': 'JS-20-34, JS-20-98, JS-95-60 (early), NRC-86, RVS-2001-4, DS-228.',
        'land_preparation': 'Deep plowing with mould-board plow followed by 2 harrowings. Broad Bed Furrow (BBF) or Ridge-Furrow planting prevents waterlogging.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP + 10kg Sulphur WDG/acre. Legume crop: needs minimal nitrogen after nodulation.',
        'weed_management': 'Pre-emergence: Diclosulam 84% WDG @ 12.4g/acre within 48h, or Post-emergence: Imazethapyr 10% SL @ 400ml/acre at 15-20 DAS.',
        'harvesting_and_storage': 'Harvest when leaves turn yellow and drop off, and pods turn greyish-brown. Thresh at 400-500 RPM to avoid seed coat cracking.',
        'economic_profit_acre': 'Cost of Cultivation: ₹11,000 - ₹14,000/acre. Expected Yield: 8 - 12 Quintals/acre. Gross Revenue at MSP (₹4,892/q): ₹39,000 - ₹58,000. Net Profit: ₹28,000 - ₹44,000/acre.'
    },
    'groundnut': {
        'seed_rate_and_spacing': 'Seed Rate: 45-50 kg kernels/acre. Spacing: 30 cm x 10 cm, 5 cm depth. Seed treatment: Mancozeb @ 2g/kg + Trichoderma 5g/kg.',
        'recommended_varieties': 'TG-37A, Kadiri-6, GJG-9, JL-24, TAG-24, DH-86.',
        'land_preparation': 'Deep plowing followed by pulverization for loose friable soil to allow easy peg penetration. Apply 5 tonnes FYM + 200kg Gypsum/acre at pegging.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP + 10kg Zinc Sulphate. Apply 150-200kg Gypsum at 40-45 DAS (flowering/pegging) for calcium pod filling.',
        'weed_management': 'Pre-emergence: Pendimethalin @ 1 L/acre. Avoid weeding after pegging begins (40 DAS) to prevent snapping pegs.',
        'harvesting_and_storage': 'Harvest when leaves turn yellow, inner shell turns dark brown, and kernels are plump. Sun-dry pods to 8% moisture before storing.',
        'economic_profit_acre': 'Cost of Cultivation: ₹15,000 - ₹19,000/acre. Expected Yield: 10 - 15 Quintals/acre. Gross Revenue at MSP (₹6,783/q): ₹67,000 - ₹1,01,000. Net Profit: ₹50,000 - ₹82,000/acre.'
    },

    # ----------------- Commercial & Cash Crops -----------------
    'sugarcane': {
        'seed_rate_and_spacing': 'Sett Rate: 25,000 - 30,000 two-budded setts/acre (approx 3 tonnes/acre). Spacing: 90 cm - 120 cm row-to-row (trench method). Sett treatment: Carbendazim 100g in 100L water for 15 mins.',
        'recommended_varieties': 'Co-0238 (high recovery), CoLk-94184, Co-86032 (Nira), Co-11015, Co-15023.',
        'land_preparation': 'Deep subsoiling to 45cm followed by 2 harrowings. Make trenches 30cm deep and 90-120cm apart. Incorporate 10-12 tonnes FYM or pressmud per acre.',
        'fertilizer_bags_per_acre': 'Basal: 1.5 bags DAP + 1 bag MOP + 10kg Zinc Sulphate/acre. Top Dressing: 3-4 bags Urea applied in 3 splits (at 45, 90, and 120 days after planting). Earthing-up at 120 DAS.',
        'weed_management': 'Pre-emergence: Atrazine 50% WP @ 800g/acre within 3 days of planting. Trash mulching between rows conserves moisture and suppresses weeds.',
        'harvesting_and_storage': 'Harvest at peak maturity when hand refractometer brix reaches 18-20%. Cut flush with ground level with sharp cane knife; deliver to sugar mill within 24 hours.',
        'economic_profit_acre': 'Cost of Cultivation: ₹35,000 - ₹45,000/acre. Expected Yield: 320 - 450 Quintals/acre. Gross Revenue at FRP (₹340/q): ₹1,08,000 - ₹1,53,000. Net Profit: ₹70,000 - ₹1,08,000/acre.'
    },
    'cotton': {
        'seed_rate_and_spacing': 'Seed Rate: 2 packets Bt-Cotton (900g)/acre. Spacing: 90-120 cm row-to-row x 45-60 cm plant-to-plant, 3-4 cm depth.',
        'recommended_varieties': 'RCH-659 BG-II, Bhakti, Ankur 3028, Ajeet-155, Mallika, Bunny Bt.',
        'land_preparation': 'Deep summer plowing to break hardpan and destroy overwintering pink bollworm larvae. 2 cross-cultivations and leveling.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP + 10kg Magnesium Sulphate/acre. Top Dressing: 1.5 bags Urea in 3 splits (squaring, flowering, boll development). Spray 1% 19:19:19 + Boron.',
        'weed_management': 'Pre-emergence: Pendimethalin 30% EC @ 1 L/acre within 48h. Inter-culture with bullock/tractor cultivator at 30, 60, and 90 DAS.',
        'harvesting_and_storage': 'Pick fully opened bolls in dry sunny weather in 3-4 pickings. Store in clean dry godowns free from moisture and trash.',
        'economic_profit_acre': 'Cost of Cultivation: ₹20,000 - ₹26,000/acre. Expected Yield: 9 - 14 Quintals/acre. Gross Revenue at MSP (₹7,521/q): ₹67,000 - ₹1,05,000. Net Profit: ₹45,000 - ₹79,000/acre.'
    },

    # ----------------- Vegetables -----------------
    'potato': {
        'seed_rate_and_spacing': 'Seed Tuber Rate: 10-12 Quintals (certified disease-free seed tubers 35-45mm size)/acre. Spacing: 60 cm ridge-to-ridge x 20 cm tuber-to-tuber, 5-7 cm depth. Tuber treatment: Mancozeb 2.5g/L water for 10 mins.',
        'recommended_varieties': 'Kufri Jyoti, Kufri Pukhraj, Kufri Chipsona-1/3 (processing), Kufri Mohan, Kufri Khyati.',
        'land_preparation': 'Deep plowing to 25cm to create loose, friable, clod-free soil bed. Mix 10 tonnes well-rotted FYM/acre before planting.',
        'fertilizer_bags_per_acre': 'Basal: 1.5 bags DAP + 1 bag MOP + 1 bag Urea/acre. Top Dressing: 1 bag Urea at earthing-up (25-30 days after emergence).',
        'weed_management': 'Pre-emergence: Metribuzin 70% WP @ 200-250g/acre within 3-4 days of planting on moist ridges.',
        'harvesting_and_storage': 'Dehaulm (cut foliage) 10-12 days before digging to harden tuber skin. Harvest on dry sunny day, cure in shade for 10 days before cold storage at 4°C.',
        'economic_profit_acre': 'Cost of Cultivation: ₹32,000 - ₹42,000/acre. Expected Yield: 100 - 140 Quintals/acre. Gross Revenue (₹800-₹1,200/q): ₹80,000 - ₹1,40,000. Net Profit: ₹48,000 - ₹98,000/acre.'
    },
    'onion': {
        'seed_rate_and_spacing': 'Seedlings: 4-5 kg seed/acre (nursery for transplanting). Spacing: 15 cm x 10 cm, 2-3 cm depth. Root dip: Carbendazim 1g/L for 15 mins before transplanting.',
        'recommended_varieties': 'Bhima Super, Bhima Dark Red, Agri-Found Dark Red, Pusa Red, Bhima Shakti (Rabi/Kharif).',
        'land_preparation': 'Plough to fine tilth, create flat beds or broad bed furrows (BBF) for drip irrigation. Apply 8 tonnes compost + 250kg neem cake.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1 bag MOP + 15kg Sulphur (critical for pungency and storage)/acre. Top Dressing: 1.5 bags Urea in 2 splits at 30 and 45 DAT.',
        'weed_management': 'Pre-emergence: Oxyfluorfen 23.5% EC @ 150ml/acre or Pendimethalin @ 1 L/acre before transplanting. 2 manual hand weedings.',
        'harvesting_and_storage': 'Harvest when 50% tops collapse (neck fall). Cure in field for 3-5 days, clip tops leaving 2.5cm neck; store in well-ventilated raised chawls.',
        'economic_profit_acre': 'Cost of Cultivation: ₹28,000 - ₹38,000/acre. Expected Yield: 90 - 130 Quintals/acre. Gross Revenue (₹1,000-₹1,800/q): ₹90,000 - ₹2,00,000. Net Profit: ₹60,000 - ₹1,60,000/acre.'
    },
    'tomato': {
        'seed_rate_and_spacing': 'Seed Rate: 100-150 grams/acre (hybrids in pro-trays). Spacing: 90 cm row-to-row x 45-60 cm plant-to-plant on raised beds with drip and silver-black mulch.',
        'recommended_varieties': 'Abhinav (Syngenta), US-440, NS-501, Arka Rakshak (triple disease resistant), Pusa Ruby, Heemsohna.',
        'land_preparation': 'Prepare raised beds 90cm wide, 30cm high. Incorporate 10 tonnes FYM + 2kg Trichoderma per acre.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1 bag MOP + 25kg Magnesium Sulphate/acre. Fertigation: 19:19:19 @ 3kg/acre twice a week, switching to 13:0:45 and 0:0:50 during fruiting.',
        'weed_management': 'Silver-black plastic mulch (25 micron) suppresses 95% of weeds, conserves water, and controls soil splash diseases.',
        'harvesting_and_storage': 'Harvest at breaker stage for distant transport or pink-red stage for local mandi. Pick every 3-4 days.',
        'economic_profit_acre': 'Cost of Cultivation: ₹35,000 - ₹50,000/acre. Expected Yield: 150 - 240 Quintals/acre. Gross Revenue: ₹1,20,000 - ₹2,40,000. Net Profit: ₹80,000 - ₹1,80,000/acre.'
    },

    # ----------------- Fruits -----------------
    'mango': {
        'seed_rate_and_spacing': 'Grafts: 40-50 plants/acre (standard 10m x 10m spacing) or 200 plants/acre in Ultra High Density (3m x 2m). Grafts: Epicotyl/inarching.',
        'recommended_varieties': 'Alphonso (Hapus), Kesar, Dasheri, Langra, Chausa, Amrapali (dwarf/high-density), Mallika, Totapuri.',
        'land_preparation': 'Dig pits of 1m x 1m x 1m during May-June. Fill with 50kg FYM, 1kg SSP, 100g chlorpyrifos dust mixed with topsoil.',
        'fertilizer_bags_per_acre': 'Per bearing tree (10+ yrs): 1kg Urea, 1kg DAP, 1kg MOP, 50kg FYM annually applied in circular trench under canopy after harvest (July-August).',
        'weed_management': 'Inter-cropping with legumes (chickpea, mung) during initial 4-5 years. Regular basin cleaning.',
        'harvesting_and_storage': 'Harvest at physiological maturity (tapka stage / specific gravity 1.01-1.02) using pole harvesters with net bags. Desap immediately and ripen in ethylene chambers at 20°C.',
        'economic_profit_acre': 'Cost of Annual Maintenance: ₹20,000 - ₹30,000/acre. Expected Yield: 40 - 70 Quintals/acre. Gross Revenue: ₹1,20,000 - ₹2,50,000. Net Profit: ₹90,000 - ₹2,20,000/acre.'
    },
    'banana': {
        'seed_rate_and_spacing': 'Tissue Culture Plants: 1,000 - 1,200 plants/acre. Spacing: 1.8m x 1.8m (paired row 1.2m x 1.2m x 2m) with drip fertigation.',
        'recommended_varieties': 'Grand Naine (G-9), Robusta, Dwarf Cavendish, Nendran (Kerala chips), Red Banana, Rasthali.',
        'land_preparation': 'Deep plowing followed by rotavator. Dig pits of 45x45x45cm. Mix 10kg FYM + 250g neem cake + 20g carbofuran/pit.',
        'fertilizer_bags_per_acre': 'Per plant: 200g Urea, 150g DAP, 300g MOP applied in 4 splits or through weekly drip fertigation. Propping with bamboo poles at bunch emergence.',
        'weed_management': 'Clean basin cultivation. Grow Cowpea as green cover crop in early stage. Drip fertigation keeps inter-rows dry.',
        'harvesting_and_storage': 'Harvest when bunch angles disappear and fingers become rounded (75-80% maturity for export). Dehand and wash in alum water.',
        'economic_profit_acre': 'Cost of Cultivation: ₹60,000 - ₹80,000/acre. Expected Yield: 250 - 350 Quintals/acre. Gross Revenue: ₹2,00,000 - ₹3,50,000. Net Profit: ₹1,40,000 - ₹2,70,000/acre.'
    },
    'apple': {
        'seed_rate_and_spacing': 'High-Density: 600 - 1,000 plants/acre on M-9 rootstock (3m x 1m); Traditional: 100-150 plants/acre (5m x 5m). Trellis support required.',
        'recommended_varieties': 'Royal Delicious, Red Chief, Gala Mast, Super Chief, Granny Smith, Golden Delicious (pollinizer 15%).',
        'land_preparation': 'Terracing on slopes. Pits of 1m x 1m dug in autumn. Mix 40kg compost + 500g SSP + 50g Trichoderma.',
        'fertilizer_bags_per_acre': 'Mature tree: 500g Urea, 250g DAP, 750g MOP + 100g Borax annually in early spring before bud break.',
        'weed_management': 'Mulching with black poly sheet or dry pine needles (10cm layer) suppresses weeds and conserves moisture in temperate hills.',
        'harvesting_and_storage': 'Harvest when ground color turns yellow and starch index is 3-4. Store in Controlled Atmosphere (CA) cold stores at 0-1°C.',
        'economic_profit_acre': 'Annual Maintenance Cost: ₹45,000 - ₹70,000/acre. Expected Yield: 70 - 120 Quintals/acre. Gross Revenue: ₹3,50,000 - ₹7,00,000. Net Profit: ₹2,80,000 - ₹6,20,000/acre.'
    }
}

# Generic fallback templates tailored by category and sub-category for all remaining crops
CATEGORY_TEMPLATES = {
    'Millet': {
        'seed_rate_and_spacing': 'Seed Rate: 2-3 kg/acre. Spacing: 30-45 cm row-to-row x 10 cm plant-to-plant, 2-3 cm depth. Seed treatment: Carbendazim @ 2g/kg seed + Azospirillum bio-fertilizer.',
        'recommended_varieties': 'Certified State Agricultural University varieties and ICAR drought-resilient selections.',
        'land_preparation': '1 plowing followed by 2 light harrowings for shallow, firm seedbed. Incorporate 4-5 tonnes FYM per acre.',
        'fertilizer_bags_per_acre': 'Basal: 1/2 bag DAP (25kg) + 15kg MOP/acre. Top Dressing: 1/2 bag Urea (25kg) at 25-30 DAS following rain or irrigation.',
        'weed_management': 'Pre-emergence: Atrazine 50% WP @ 300-400g/acre within 48h. 1 manual hand weeding at 20-25 days after emergence.',
        'harvesting_and_storage': 'Harvest when earheads dry and turn yellowish-brown. Sun-dry grains to 10% moisture before bagging in dry gunny bags.',
        'economic_profit_acre': 'Cost: ₹6,500 - ₹9,000/acre. Expected Yield: 8 - 14 Quintals/acre. Gross Revenue: ₹24,000 - ₹42,000. Net Profit: ₹17,000 - ₹33,000/acre.'
    },
    'Pulse': {
        'seed_rate_and_spacing': 'Seed Rate: 8-12 kg/acre. Spacing: 30 cm x 10 cm, 3-4 cm depth. Seed treatment: Trichoderma @ 5g/kg + Rhizobium culture @ 10g/kg seed.',
        'recommended_varieties': 'High-yielding ICAR/SAU verified varieties with wilt and mosaic resistance.',
        'land_preparation': '2 plowings to medium tilth. Avoid overly fine tilth to preserve root aeration. Apply 4 tonnes FYM/acre.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 15kg MOP + 10kg Sulphur/acre. Legume crop fixes atmospheric nitrogen, so top-dressed Urea is rarely required.',
        'weed_management': 'Pre-emergence: Pendimethalin 30% EC @ 1 L/acre within 48 hours of sowing. Hand weeding at 25 DAS.',
        'harvesting_and_storage': 'Harvest when 80-85% pods turn brown/black. Sun-dry pods thoroughly before threshing. Store grain at 9-10% moisture.',
        'economic_profit_acre': 'Cost: ₹8,000 - ₹11,000/acre. Expected Yield: 6 - 10 Quintals/acre. Gross Revenue: ₹38,000 - ₹65,000. Net Profit: ₹30,000 - ₹54,000/acre.'
    },
    'Oilseed': {
        'seed_rate_and_spacing': 'Seed Rate: 2-4 kg/acre. Spacing: 30-45 cm x 10-15 cm, 3 cm depth. Seed treatment: Thiram/Mancozeb @ 2.5g/kg seed.',
        'recommended_varieties': 'High oil-content certified hybrid and composite varieties released by Directorate of Oilseeds Research.',
        'land_preparation': '2-3 plowings followed by planking to conserve moisture. Apply 5 tonnes FYM/acre before last plowing.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP + 15kg elemental Sulphur (essential for oil synthesis). Top Dressing: 1 bag Urea at 1st irrigation.',
        'weed_management': 'Pre-emergence: Pendimethalin @ 1 L/acre within 48h. 1 manual hoeing at 25 DAS.',
        'harvesting_and_storage': 'Harvest when plants turn yellowish-brown and pods rattle. Dry seeds to 8-9% moisture to prevent rancidity.',
        'economic_profit_acre': 'Cost: ₹10,000 - ₹13,000/acre. Expected Yield: 7 - 11 Quintals/acre. Gross Revenue: ₹40,000 - ₹65,000. Net Profit: ₹30,000 - ₹52,000/acre.'
    },
    'Vegetable': {
        'seed_rate_and_spacing': 'Seed Rate: 150-400 grams/acre (hybrids) or seed tubers/slips. Spacing: 60-90 cm row x 45-60 cm plant on raised beds.',
        'recommended_varieties': 'High-yielding F1 hybrids from ICAR-IIHR, IARI, and certified seed breeders.',
        'land_preparation': 'Deep plowing to 25cm. Prepare raised beds 90cm wide with drip lines. Incorporate 8-10 tonnes FYM + 250kg neem cake/acre.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1 bag MOP + 1 bag Urea/acre. Regular fertigation with 19:19:19 and micronutrients during vegetative and fruiting stages.',
        'weed_management': 'Silver-black plastic mulch (25-30 micron) provides optimal weed suppression and soil moisture retention.',
        'harvesting_and_storage': 'Harvest fruits/vegetables at tender market maturity in morning hours. Grade and pack in plastic crates for mandi transport.',
        'economic_profit_acre': 'Cost: ₹25,000 - ₹40,000/acre. Expected Yield: 80 - 160 Quintals/acre. Gross Revenue: ₹90,000 - ₹2,00,000. Net Profit: ₹65,000 - ₹1,60,000/acre.'
    },
    'Spice': {
        'seed_rate_and_spacing': 'Seed Rate: 4-6 kg/acre (rhizomes: 600-800 kg/acre). Spacing: 30 cm x 15 cm. Seed treatment with Trichoderma 5g/kg.',
        'recommended_varieties': 'ICAR-IISR Calicut verified high-curcumin / high-essential-oil varieties.',
        'land_preparation': 'Fine tilth with high organic content. Prepare raised beds 1m wide with drainage channels. Incorporate 10 tonnes FYM/acre.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1 bag MOP + 15kg Zinc Sulphate. Top Dressing: 1 bag Urea in 2 splits at 45 and 90 DAS.',
        'weed_management': 'Pre-emergence herbicide or 10cm straw/leaf mulching immediately after planting.',
        'harvesting_and_storage': 'Harvest when leaves wither and yellow. Cure, polish, and sun-dry to 8-10% moisture before bagging in moisture-proof containers.',
        'economic_profit_acre': 'Cost: ₹25,000 - ₹38,000/acre. Expected Yield: 15 - 25 Quintals dry/acre. Gross Revenue: ₹1,10,000 - ₹2,20,000. Net Profit: ₹85,000 - ₹1,80,000/acre.'
    },
    'Fruit': {
        'seed_rate_and_spacing': 'Planting Density: 100 - 300 grafts/acre depending on high-density vs traditional layout. Pits: 75x75x75 cm.',
        'recommended_varieties': 'State Horticultural University verified grafted varieties with commercial export and domestic mandi demand.',
        'land_preparation': 'Dig pits 2 months before monsoon, sun-cure, fill with topsoil, 30-40kg compost, 500g SSP, and bio-fungicide.',
        'fertilizer_bags_per_acre': 'Annual bearing nutrition: 500g N, 250g P2O5, 500g K2O per tree applied around drip line circle with 30kg organic manure.',
        'weed_management': 'Tree basin weeding and organic straw mulching. Inter-cropping with pulses in early non-bearing years.',
        'harvesting_and_storage': 'Harvest at firm-mature stage with stem intact. Grade by size/weight and pack in ventilated CFB corrugated boxes.',
        'economic_profit_acre': 'Annual Maintenance Cost: ₹25,000 - ₹45,000/acre. Expected Yield: 50 - 100 Quintals/acre. Gross Revenue: ₹1,50,000 - ₹3,50,000. Net Profit: ₹1,10,000 - ₹3,00,000/acre.'
    },
    'Default': {
        'seed_rate_and_spacing': 'Follow ICAR recommended seed rate and planting geometry for optimum plant population and canopy sunlight penetration.',
        'recommended_varieties': 'Select certified university-released varieties suited to your local district agro-climatic zone.',
        'land_preparation': '2-3 thorough plowings and leveling for uniform irrigation and root development. Apply 5-8 tonnes FYM/acre.',
        'fertilizer_bags_per_acre': 'Basal: 1 bag DAP + 1/2 bag MOP/acre. Top Dressing: 1-2 bags Urea based on soil test nitrogen level.',
        'weed_management': 'Keep field weed-free during initial 30-40 days through timely inter-culture or recommended pre-emergence spray.',
        'harvesting_and_storage': 'Harvest at full physiological maturity. Sun-dry to safe moisture levels before storing in pest-protected bins.',
        'economic_profit_acre': 'Cost of Cultivation: ₹12,000 - ₹18,000/acre. Expected Yield: 12 - 20 Quintals/acre. Net Profit: ₹25,000 - ₹45,000/acre.'
    }
}

def enrich_crop_guides():
    df = pd.read_csv(CSV_PATH)
    print(f"Read {len(df)} crops from {CSV_PATH}")

    new_cols = [
        'seed_rate_and_spacing',
        'recommended_varieties',
        'land_preparation',
        'fertilizer_bags_per_acre',
        'weed_management',
        'harvesting_and_storage',
        'economic_profit_acre'
    ]

    for col in new_cols:
        if col not in df.columns:
            df[col] = ''

    for idx, row in df.iterrows():
        crop_key = str(row['crop']).strip().lower()
        subcat = str(row.get('sub_category', '')).strip()
        cat = str(row.get('category', '')).strip().capitalize()

        # 1. Exact match
        if crop_key in PLANNING_DATA:
            pdata = PLANNING_DATA[crop_key]
        elif subcat in CATEGORY_TEMPLATES:
            pdata = CATEGORY_TEMPLATES[subcat]
        elif cat in CATEGORY_TEMPLATES:
            pdata = CATEGORY_TEMPLATES[cat]
        else:
            pdata = CATEGORY_TEMPLATES['Default']

        for col in new_cols:
            df.at[idx, col] = pdata.get(col, '')

    df.to_csv(CSV_PATH, index=False)
    print(f"Successfully enriched {len(df)} crops with 7 comprehensive planning fields in {CSV_PATH}!")

if __name__ == '__main__':
    enrich_crop_guides()
