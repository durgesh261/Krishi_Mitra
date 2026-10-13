# 🌱 Krishi Mitra (कृषि मित्र)
### AI-Powered Smart Farming Assistant & Kisan Seva Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Framework-Flask%203.0-lightgrey?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn%20%7C%20Random%20Forest-orange?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Groq AI](https://img.shields.io/badge/LLM-Groq%20Cloud%20(LLaMA%203.3%2070B)-purple?logo=meta&logoColor=white)](https://groq.com/)
[![Languages](https://img.shields.io/badge/Localization-10%20Indian%20Languages-success)](#-10-indian-regional-languages)
[![Responsive](https://img.shields.io/badge/Design-Mobile--First%20Responsive-brightgreen?logo=google-chrome&logoColor=white)](#-mobile-phone-optimized-ui)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Live Demo & Portal:** [https://durgesh261.github.io/Krishi_Mitra/](https://durgesh261.github.io/Krishi_Mitra/)  
> **Source Repository:** [https://github.com/durgesh261/Krishi_Mitra](https://github.com/durgesh261/Krishi_Mitra)

---

## 🌾 Overview

**Krishi Mitra (कृषि मित्र)** is a production-grade, AI-driven agricultural decision support platform engineered specifically for Indian farmers, agricultural extension workers, and rural entrepreneurs. 

Combining **Machine Learning crop models**, **Domain-Enforced RAG (Retrieval-Augmented Generation)** with **LLaMA 3.3 70B**, **Real-Time APMC Mandi Bhav & MSP benchmarks**, **Live Agro-Weather Analytics**, and **10 Indian Regional Languages**, Krishi Mitra bridges the information gap between modern agricultural science and farmers in the field.

---

## ✨ Key Features & Modules

### 1. 🛰️ Multi-Spectral Remote Sensing & Yield Prediction (`/remote-sensing`)
- **Multimodal Gated Cross-Attention**: Fuses high-resolution satellite/drone multi-spectral imagery with micro-climate telemetry vectors (ambient temperature, relative humidity, cumulative precipitation, soil moisture, VPD).
- **Grad-CAM Visual Interpretability**: Generates real-time visual attention heatmaps overlaying raw canopy imagery, delineating active pathogen sporulation margins from healthy background foliage.
- **Multi-Spectral Indices**: Real-time extraction of NDVI (Photosynthetic Vigor), NDWI (Canopy Water Stress), GNDVI (Chlorophyll Absorption), and SAVI (Soil-Adjusted Index).
- **Empirical Ablation Benchmark**: Outperforms single-modality vision baselines by **+14.2% Macro F1-score** (81.3% → 95.5%) while reducing yield prediction RMSE by **51.4%** (6.42 → 3.12 q/ha).
- **Academic Whitepaper & SOP Dossier**: Complete PyTorch models, dataset loaders, training scripts, and CV/SOP pitch writeup available in [`research/CV_SOP_PORTFOLIO.md`](research/CV_SOP_PORTFOLIO.md).

### 2. 🤖 AI Kisan Agronomist (RAG & Groq LLaMA 3.3 70B)
- **415+ Curated Knowledge Chunks**: In-memory agricultural knowledge base sourced from government scheme guidelines, ICAR agronomy handbooks, and crop protection manuals.
- **Agricultural Domain Guardrails**: Automatically detects and rejects non-farming questions (coding, politics, entertainment) with a polite guidance message, keeping conversations 100% focused on agriculture.
- **Instant Response**: Dual fallback mechanism ensures zero-latency expert answers even if external cloud APIs experience rate limits.

### 2. 🌾 Smart Crop Recommendation Engine
- **35+ Major Indian Crops**: Recommends optimal crops including Cereals (Rice, Wheat, Maize, Barley), Pulses (Gram, Arhar, Moong, Urad), Cash Crops (Cotton, Sugarcane, Jute), Oilseeds (Mustard, Soybean, Groundnut), and Spices/Millets.
- **Multi-Factor Input**: Analyzes soil nutrients ($N, P, K$), soil $pH$, temperature, relative humidity, and annual rainfall.
- **Confidence Scoring**: Delivers top recommendation along with secondary crop alternatives and probability metrics.

### 3. 🌐 10 Indian Regional Languages
Complete native language support covering India's major agricultural belts:
| Language | Script | Primary Regions |
| :--- | :--- | :--- |
| **English** | Latin | Pan-India / Universal |
| **हिन्दी (Hindi)** | Devanagari | Uttar Pradesh, MP, Bihar, Rajasthan, Haryana |
| **ਪੰਜਾਬੀ (Punjabi)** | Gurmukhi | Punjab, Haryana |
| **বাংলা (Bengali)** | Bengali | West Bengal, Assam, Tripura |
| **मराठी (Marathi)** | Devanagari | Maharashtra |
| **ગુજરાતી (Gujarati)** | Gujarati | Gujarat |
| **తెలుగు (Telugu)** | Telugu | Andhra Pradesh, Telangana |
| **தமிழ் (Tamil)** | Tamil | Tamil Nadu, Puducherry |
| **ಕನ್ನಡ (Kannada)** | Kannada | Karnataka |
| **മലയാളം (Malayalam)** | Malayalam | Kerala |

Farmers can set their default language on signup or seamlessly switch anytime via the navbar or dedicated `/select-language` page.

### 4. 📊 Real-Time Mandi Bhav & MSP Tracking (`/mandi-prices`)
- **State & Commodity Search**: Filter real-time mandi prices across 28 states and Union Territories.
- **MSP Price Benchmarks**: Displays Minimum Support Price (MSP) guaranteed rates alongside current market prices so farmers know when their produce is being underpriced.
- **Market Dynamics**: Live modal price, minimum/maximum price ranges, and arrival volumes.

### 5. 📰 Daily Agri News Portal (`/news`)
- **Curated Farming Newsfeed**: Filterable by Subsidies, Mandi & MSP, Weather & Monsoon, Agri Tech, and Policy Reforms.
- **Rotating Farming Advertisements**: Dynamic agricultural advisories showcasing verified solar pump subsidies, micro-irrigation discounts, and organic seeds.

### 6. 🏛️ Krishi Seva Hub & PM Schemes (`/krishi-seva`)
- **Direct Government Schemes**: Complete guidelines, eligibility criteria, subsidy percentages, and official application portals for PM-KISAN, PMFBY, PM-KUSUM, Soil Health Card, e-NAM, and Agriculture Infrastructure Fund.
- **Certified Soil Testing Laboratories**: Interactive database of accredited soil testing labs across all states with phone numbers, emails, and address locations.

### 7. 🌿 Crop Disease Diagnosis (`/disease`)
- Computer vision foliage analysis and symptom checklists.
- Provides immediate chemical spray recommendations (with active ingredients and dosage per liter), organic bio-fungicide treatments (Trichoderma, Pseudomonas), and cultural prevention techniques.

### 8. 🌦️ Live Agro-Weather Advisory (`/weather`)
- Real-time temperature, humidity, wind velocity, and rainfall forecasts via OpenWeatherMap.
- Automated agronomist advice advising farmers whether to spray pesticides, irrigate, or prepare for harvest based on upcoming precipitation.

### 9. 📱 Mobile Phone-Optimized UI
- **Zero Horizontal Overflow**: Built on responsive CSS Flexbox and CSS Grid with strict view constraints (`360px` to `430px` screens).
- **Slide-Out Mobile Drawer**: Custom mobile drawer with header, dedicated close button (`✕`), blurred backdrop overlay, and body scroll locking.
- **Touch-First Buttons**: 44px+ minimum touch target sizes and 16px form inputs to prevent unwanted iOS Safari zooming.

---

## 🏗️ System Architecture

```
                               ┌──────────────────────────────────────────┐
                               │           Farmer Client Device           │
                               │  (Mobile Web / Tablet / Desktop Browser) │
                               └────────────────────┬─────────────────────┘
                                                    │
                                                    ▼
                               ┌──────────────────────────────────────────┐
                               │           Flask Web Application          │
                               │               (app.py)                   │
                               └───────┬────────────┬─────────────┬───────┘
                                       │            │             │
              ┌────────────────────────┘            │             └─────────────────────────┐
              ▼                                     ▼                                       ▼
┌───────────────────────────┐         ┌───────────────────────────┐           ┌───────────────────────────┐
│     Machine Learning      │         │   RAG & Agronomist AI     │           │   Location & Weather      │
│  Random Forest Classifier │         │  • Groq LLaMA 3.3 70B     │           │  • OpenWeatherMap API     │
│  (35+ Indian Crops)       │         │  • In-Memory Corpus (415) │           │  • OpenCage Geocoding     │
│  train/models/*.pkl       │         │  • Agricultural Guardrail │           │  • Mandi & News Feeds     │
└───────────────────────────┘         └───────────────────────────┘           └───────────────────────────┘
              │                                     │                                       │
              └────────────────────────┬────────────┴───────────────────────────────────────┘
                                       ▼
                         ┌───────────────────────────┐
                         │   SQLite User Database    │
                         │   • User Auth & Passwords │
                         │   • Language Preferences  │
                         │   • Activity Audit Logs   │
                         └───────────────────────────┘
```

---

## 📂 Repository Directory Structure

```
Krishi_Mitra/
├── app.py                      # Core Flask application & REST API routes
├── auth.py                     # Authentication blueprints, sessions & bcrypt
├── database.py                 # SQLite schema migration & DB helper functions
├── crop_recommendation.py      # ML crop prediction loader & pipeline
├── chat1.py                    # Lightweight in-memory RAG & agricultural guardrails
├── chat2.py                    # Groq Cloud LLaMA 3.3 70B integration & CV diagnostics
├── mandi_service.py            # Mandi Bhav & MSP real-time data engine
├── news_service.py             # Daily Agri News feed & agricultural ads engine
├── multimodal_remote_sensing.py# Remote sensing, NDVI/NDWI, Grad-CAM & climate fusion engine
├── location_service.py         # OpenCage GPS reverse-geocoding service
├── test_app_endpoints.py       # Comprehensive 15-suite automated test runner
├── requirements.txt            # Python dependencies
├── run.bat                     # Quick-start Windows launch script
├── .env.example                # Sample environment configuration template
├── research/                   # PyTorch Research Pipeline & Benchmark Experiments
│   ├── models/multimodal_net.py# MultimodalCropNet PyTorch class & Grad-CAM hooks
│   ├── dataset/dataloader.py   # Multimodal dataset loader & benchmark generator
│   ├── train.py                # Multi-task training script (CE + MSE loss)
│   ├── ablation_study.py       # Empirical ablation experiment runner (+14.2% F1)
│   └── CV_SOP_PORTFOLIO.md     # Research paper, CV bullet points & SOP formulation
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
│   ├── remote_sensing.html     # Multi-Spectral remote sensing & Grad-CAM dashboard
│   ├── mandi_prices.html       # Mandi Bhav & MSP explorer
│   ├── news.html               # Daily Agri News portal
│   ├── krishi_seva.html        # Schemes directory & soil testing laboratories
│   ├── crop_recommendation.html# Crop prediction wizard
│   ├── weather.html            # Live agro-meteorological advisory
│   ├── disease.html            # Foliage disease diagnosis tool
│   ├── calculator.html         # Farming profit calculator
│   └── select_language.html    # 10 Indian Regional Languages switcher
└── static/
    ├── css/style.css           # Modern green agricultural design system
    ├── js/                     # Modular frontend logic (index, chat, remote_sensing, etc.)
    └── *.png                   # High-contrast icons, logos, and UI graphics
```

---

## 🚀 Quickstart & Setup Guide

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
Update your keys in `.env`:
```ini
GROQ_API_KEY=your_groq_api_key_here
WEATHER_API_KEY=your_openweather_api_key_here
SECRET_KEY=your_secret_random_key_here
OPENCAGE_API_KEY=your_opencage_api_key_here
```
*(Note: Krishi Mitra is designed with intelligent local fallbacks; all core features and local AI agronomist functions will continue working even if third-party API keys are unset).*

### 5. Run the Application
```bash
# Windows quick-launch
run.bat

# Or run directly with Python
python app.py
```
Open your browser at **`http://127.0.0.1:5000`**.

---

## 🧪 Automated Testing

Krishi Mitra includes an end-to-end test suite validating all routes, prediction models, language switchers, and RAG guardrails:

```bash
python test_app_endpoints.py
```

**Verification Results:**
- ✅ Random Forest Crop Prediction Pipeline (Top-1 & Confidence)
- ✅ 10 Regional Language Switching & Persistence (`/api/set-language`)
- ✅ RAG Agricultural Knowledge Retrieval & Non-Farming Query Rejection
- ✅ Mandi Bhav & MSP API State/Commodity Filtering
- ✅ Krishi Seva Schemes & Soil Testing Laboratories Directory
- ✅ Daily Agri News & Partner Advertisements API
- ✅ User Authentication & Password Hashing
- **Result: 14/14 Suites Passing (100% OK)**

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/predict-crop` | `POST` | Predict recommended crop based on N, P, K, pH, temp, humidity, rainfall |
| `/api/mandi-prices` | `GET` | Retrieve real-time Mandi Bhav and MSP filtered by state and commodity |
| `/api/news` | `GET` | Fetch daily farming news stories with category filters |
| `/api/farming-ads` | `GET` | Get verified agricultural partner advisories & subsidies |
| `/api/schemes` | `GET` | Search and filter government agricultural welfare schemes |
| `/api/soil-labs` | `GET` | Query certified soil testing laboratories by state and district |
| `/api/set-language` | `POST` | Change active session language to one of 10 Indian regional languages |
| `/api/weather-advisory` | `POST` | Get agro-meteorological advisory from latitude & longitude |

---

## 🤝 Contributing

Contributions to empower Indian farmers are warmly welcomed!
1. Fork the Project (`https://github.com/durgesh261/Krishi_Mitra`)
2. Create your Feature Branch (`git checkout -b feature/NewFarmingFeature`)
3. Commit your Changes (`git commit -m 'Add NewFarmingFeature'`)
4. Push to the Branch (`git push origin feature/NewFarmingFeature`)
5. Open a Pull Request

---

## 📄 License & Attribution

Distributed under the **MIT License**. See `LICENSE` for more information.  
Crafted with ❤️ for the farming community of India.
