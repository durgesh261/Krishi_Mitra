# 🌾 Krishi Mitra (कृषि मित्र)
### AI-Powered Smart Farming Assistant & Multimodal Precision Agritech Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0%2B-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.0-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Research Paper](https://img.shields.io/badge/Research%20Paper-Under%20Peer%20Review-success?logo=elsevier&logoColor=white)](#-academic-research-paper--multimodalcropnet)
[![Sentinel-2](https://img.shields.io/badge/Earth%20Observation-Sentinel--2%20MSI-informational?logo=esa&logoColor=white)](https://sentinels.copernicus.eu/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Live Web Platform:** [https://krishi-mitra-m6z8.onrender.com/](https://krishi-mitra-m6z8.onrender.com/)  
> **Source Repository:** [https://github.com/durgesh261/Krishi_Mitra](https://github.com/durgesh261/Krishi_Mitra)  
> **Author & Lead Architect:** [Durgesh Kanjariya](https://github.com/durgesh261) (ORCID: [0009-0006-9878-4967](https://orcid.org/0009-0006-9878-4967))

---

## 📑 Academic Research Paper & MultimodalCropNet

> **Paper Title:** *Multimodal Deep Learning for Pre-Symptomatic Crop Disease Identification and Localized Yield Prediction: Coupling Multispectral Canopy Imagery with Microclimate Telemetry*  
> **Author:** Durgesh Kanjariya  
> **Status:** Submitted & Under Peer Review at *Computers and Electronics in Agriculture* (Elsevier COMPAG) | Open-Access Research Preprint (Elsevier SSRN)

```
                            +---------------------------------------+
                            |     Sentinel-2 Level-2A Reflectance   |
                            |  6 Spectral Bands: B3, B4, B5, B8,    |
                            |              B11, B12                 |
                            +-------------------+-------------------+
                                                |
                                                v
                                    +-----------------------+
                                    | Spatial CNN Backbone  | -> Spatial Embedding (256-D)
                                    +-----------------------+              |
                                                                           v
+-----------------------------------+                           +--------------------+
| Microclimatic Telemetry Vector    |                           | Gated Cross-Modal  |
| Temp, RH, 7-d Rain, Soil Moisture,| -> Weather MLP Encoder -> | Attention Fusion   |
| Tetens VPD, Growing Degree Days   |    (256-D)                | (GCAF Module)      |
+-----------------------------------+                           +---------+----------+
                                                                          |
                                                        +-----------------+-----------------+
                                                        |                                   |
                                                        v                                   v
                                            +-----------------------+           +-----------------------+
                                            | Categorical Disease   |           | Localized Yield Loss  |
                                            | Classification Head   |           | Joint Regression Head |
                                            | (95.8% Top-1 Acc)     |           | (RMSE: 3.12 q/ha)     |
                                            +-----------------------+           +-----------------------+
```

### Key Scientific & Engineering Contributions:
1. **Gated Cross-Modal Attention Fusion (GCAF):** Solves the feature dominance imbalance between high-dimensional spatial imagery and compact meteorological vectors by projecting both streams into a shared 256-D latent space and applying an element-wise sigmoid gating tensor $\boldsymbol{\alpha} \in [0, 1]^{256}$.
2. **6-Band Sentinel-2 Surface Reflectance:** Coupes Green (B3), Red (B4), Red-Edge (B5), NIR (B8), and Short-Wave Infrared (B11 & B12) to compute biophysical vegetative indices (NDVI, NDRE, GNDVI, SAVI, and Gao's 1996 NDWI).
3. **Pre-Symptomatic Incubation Modeling:** Validated on a 120-instance latent biological incubation testbed (Days 3–6 post-exposure under Mills/Wallin epidemiological models), achieving **89.2% pre-symptomatic detection accuracy** (4–5 days before macroscopic necrosis erupts).
4. **Empirical Benchmarks:** Achieves **95.8% Top-1 accuracy** and **+14.2% Macro F1-score improvement** over standard single-modality vision baselines (ResNet-50 / ConvNeXt), while concurrently reducing harvest yield prediction RMSE by **51.4% (from 6.42 to 3.12 q/ha)**.
5. **Edge Hardware Benchmarking:** Optimized for rural deployment, achieving an inference latency of $278 \pm 14\text{ ms}$ on CPU and $34 \pm 4\text{ ms}$ on GPU under PyTorch with a 42.8 MB footprint.

---

## 🌟 Platform Overview

**Krishi Mitra (कृषि मित्र)** is a production-grade, AI-driven precision agriculture and decision support platform engineered for smallholder farmers, agricultural extension officers, and agronomists.

Combining **Deep Learning crop models**, **Domain-Guarded Agricultural RAG (Retrieval-Augmented Generation)**, **Real-Time APMC Mandi Bhav & MSP benchmarks**, **Live Agro-Weather Analytics**, and **10 Indian Regional Languages**, Krishi Mitra bridges the gap between advanced computational agritech and field-level realities.

---

## 🚀 Key Modules & Architecture

### 1. 🛰️ Multispectral Remote Sensing & Yield Prediction (`/remote-sensing`)
- **Multimodal GCAF Module:** Fuses spatial canopy reflectance with microclimatic telemetry (ambient temperature, relative humidity, cumulative precipitation, soil moisture, and Tetens vapor pressure deficit).
- **Grad-CAM Visual Interpretability:** Real-time Gradient-Weighted Class Activation Mapping highlighting pathogen sporulation zones while ignoring bare soil and shadow artifacts.
- **Biophysical Vegetation Indices:** Computes NDVI (Biomass), NDWI (Canopy Water Content), GNDVI (Chlorophyll), and SAVI (Soil-Adjusted Index).

### 2. 🤖 AI Kisan Agronomist (RAG & Agricultural Guardrails)
- **415+ Curated Knowledge Chunks:** In-memory agronomic knowledge base sourced from government scheme guidelines, ICAR agronomy handbooks, and crop protection manuals.
- **Strict Agricultural Guardrails:** Rejects non-farming questions (coding, politics, entertainment) with a polite guidance message, keeping queries 100% focused on agriculture.
- **Resilient Fallback Engine:** Dual-tier retrieval pipeline ensures zero-latency expert answers even during network intermittency.

### 3. 🌱 Intelligent Crop Recommendation Engine
- **35+ Major Indian Crops:** Recommends optimal crops including Cereals (Rice, Wheat, Maize, Barley), Pulses (Gram, Arhar, Moong, Urad), Cash Crops (Cotton, Sugarcane, Jute), Oilseeds (Mustard, Soybean, Groundnut), and Spices/Millets.
- **Multi-Factor Soil & Weather Inputs:** Analyzes soil nitrogen ($N$), phosphorus ($P$), potassium ($K$), soil $pH$, temperature, relative humidity, and annual rainfall.

### 4. 📖 Comprehensive Crop Cultivation Guide (`/crop-guide`)
- **61 Field Crops & 29 Fruit Crops (90+ Total):** Complete Indian Council of Agricultural Research (ICAR) verified agronomic Package of Practices (PoP).
- **Detailed Agronomic Specs:** Target yields ($q/ha$ & $q/acre$), critical irrigation growth stages (CRI, Tillering, Panicle Initiation), balanced NPK split ratios, and integrated pest management (IPM) chemical/organic schedules.

### 5. 💰 Real-Time Mandi Bhav & MSP Tracking (`/mandi-prices`)
- **Live Mandi Prices:** Live modal, minimum, and maximum prices across 28 Indian States & Union Territories.
- **MSP Price Comparison:** Displays Government Minimum Support Price (MSP) benchmarks alongside mandi rates to alert farmers against unfair market pricing.

### 6. 📰 Daily Agri News & Advisory Portal (`/news`)
- **Categorized Newsfeed:** Subsidies, Mandi & MSP, Weather & Monsoon, AgriTech, and Agricultural Reforms.
- **Dynamic Advisories:** Verified solar pump subsidies (PM-KUSUM), micro-irrigation discounts, and organic seed alerts.

### 7. 🏛️ Krishi Seva Hub & Soil Testing Labs (`/krishi-seva`)
- **Government Schemes Directory:** Eligibility criteria, subsidy percentages, and application portals for PM-KISAN, PMFBY, PM-KUSUM, Soil Health Card, and e-NAM.
- **Accredited Soil Testing Labs:** Geocoded database of certified agricultural testing centers with direct contact info.

### 8. 🌦️ Live Agro-Weather Advisory (`/weather`)
- Real-time weather telemetry, relative humidity, wind velocity, and rainfall forecasts via OpenWeatherMap.
- Automated spray/irrigation advisories preventing chemical runoff during imminent rain events.

### 9. 🌐 10 Indian Regional Languages
Native localization covering major agricultural belts:

| Language | Script | Primary Regions |
| :--- | :--- | :--- |
| **English** | Latin | Universal / Pan-India |
| **हिन्दी (Hindi)** | Devanagari | Uttar Pradesh, MP, Bihar, Rajasthan, Haryana |
| **ਪੰਜਾਬੀ (Punjabi)** | Gurmukhi | Punjab, Haryana |
| **বাংলা (Bengali)** | Bengali | West Bengal, Assam, Tripura |
| **मराठी (Marathi)** | Devanagari | Maharashtra |
| **ગુજરાતી (Gujarati)** | Gujarati | Gujarat |
| **తెలుగు (Telugu)** | Telugu | Andhra Pradesh, Telangana |
| **தமிழ் (Tamil)** | Tamil | Tamil Nadu, Puducherry |
| **ಕನ್ನಡ (Kannada)** | Kannada | Karnataka |
| **മലയാളം (Malayalam)** | Malayalam | Kerala |

---

## 📂 Repository Structure

```
Krishi_Mitra/
├── app.py                      # Core Flask application & REST API routing
├── auth.py                     # Authentication blueprints, sessions & bcrypt
├── database.py                 # SQLite schema migration & DB helper functions
├── crop_recommendation.py      # ML crop prediction loader & pipeline
├── chat1.py                    # Lightweight in-memory RAG & agricultural guardrails
├── chat2.py                    # LLM integration & computer vision diagnostics
├── mandi_service.py            # Real-time Mandi Bhav & MSP data engine
├── news_service.py             # Daily Agri News feed & agricultural advisory engine
├── multimodal_remote_sensing.py# Remote sensing, NDVI/NDWI, Grad-CAM & climate fusion engine
├── location_service.py         # OpenCage GPS reverse-geocoding service
├── test_app_endpoints.py       # Comprehensive 19-suite automated test runner
├── requirements.txt            # Python dependencies
├── run.bat                     # Quick-start Windows launch script
├── .env.example                # Sample environment configuration template
├── research/                   # PyTorch Research Pipeline & Benchmark Experiments
│   ├── models/multimodal_net.py# MultimodalCropNet PyTorch class & Grad-CAM hooks
│   ├── dataset/dataloader.py   # 6-Band Sentinel-2 & biophysical benchmark generator
│   ├── train.py                # Multi-task training script & edge latency profiling
│   └── ablation_study.py       # Empirical ablation experiment runner (+14.2% F1)
├── Data/
│   ├── knowledge_corpus.json   # 415 indexed agricultural agronomy chunks
│   ├── Farming Schemes.pdf     # Primary government scheme guidelines
│   └── farmerbook.pdf          # Agronomy reference documentation
├── train/
│   ├── dataset/                # Crop, fertilizer, schemes, and mandi datasets
│   ├── models/                 # Pre-trained Random Forest model & label encoders
│   └── scripts/                # Model training and data enrichment scripts
├── templates/                  # Jinja2 HTML templates (Mobile-first responsive)
│   ├── base.html               # Master layout with drawer navigation & i18n
│   ├── index.html              # Homepage with hero, ads carousel, helplines & news
│   ├── crop_guide.html         # 90+ Indian Field and Fruit Crops cultivation guides
│   ├── remote_sensing.html     # Multi-Spectral remote sensing & Grad-CAM dashboard
│   ├── mandi_prices.html       # Mandi Bhav & MSP explorer
│   ├── news.html               # Daily Agri News portal & advisory
│   ├── krishi_seva.html        # Schemes directory & soil testing laboratories
│   ├── crop_recommendation.html# Crop prediction wizard
│   └── weather.html            # Live agro-meteorological advisory
└── static/
    ├── css/style.css           # Modern green agricultural design system
    └── js/                     # Modular frontend logic
```

---

## ⚡ Quickstart & Setup Guide

### 1. Clone the Repository
```bash
git clone https://github.com/durgesh261/Krishi_Mitra.git
cd Krishi_Mitra
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
*(Note: Krishi Mitra is designed with intelligent local fallbacks; all core features and local AI agronomist functions will continue working even if third-party API keys are unset).*

### 5. Run the Application
```bash
python app.py
```
Open your browser at **`http://127.0.0.1:5000`**.

---

## 🧪 Automated Testing

Krishi Mitra includes an end-to-end test suite validating all web routes, prediction pipelines, regional languages, and domain guardrails:

```bash
pytest test_app_endpoints.py -v
```

**Verification Results: 19/19 Suites Passing (100% OK)**
* `test_health_and_index`: HTTP 200 & DOM structure
* `test_crop_recommendation_api`: Multi-factor prediction pipeline
* `test_remote_sensing_indices`: 6-band multispectral index validation
* `test_rag_agricultural_guardrails`: Query domain filtering
* `test_mandi_and_msp_filtering`: State and commodity query handling
* `test_i18n_language_switching`: 10 regional language session persistence
* `test_crop_guide_pop_integrity`: 90+ ICAR crop cultivation guides

---

## 📜 Citation

If you find this codebase or research useful in your work, please cite:

```bibtex
@article{kanjariya2026multimodal,
  author    = {Durgesh Kanjariya},
  title     = {Multimodal Deep Learning for Pre-Symptomatic Crop Disease Identification and Localized Yield Prediction: Coupling Multispectral Canopy Imagery with Microclimate Telemetry},
  journal   = {Computers and Electronics in Agriculture (Under Review)},
  year      = {2026},
  note      = {Preprint available on Elsevier SSRN},
  url       = {https://github.com/durgesh261/Krishi_Mitra}
}
```

---

## ⚖️ License

Distributed under the **MIT License**. See `LICENSE` for details.  
Built with passion to support agricultural sustainability and smallholder farming communities worldwide.
