"""
Crop Recommendation System
Implements Ensemble ML, Explainable AI (XAI) feature importance,
and Shannon Entropy Uncertainty Quantification based on the Krishi Mitra research paper.
"""
import math
import joblib
import numpy as np
import pandas as pd
import os

# Load model and encoder
MODEL_PATH = 'train/models/crop_recommendation_model.pkl'
ENCODER_PATH = 'train/models/crop_label_encoder.pkl'
DISTRICT_DATA_PATH = 'train/dataset/india_crop_production.csv'

model = None
label_encoder = None

def load_model():
    """Load the trained model and encoder safely"""
    global model, label_encoder
    if model is None:
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
            model = joblib.load(MODEL_PATH)
            label_encoder = joblib.load(ENCODER_PATH)
            print("[OK] Crop recommendation model loaded successfully.")
        else:
            raise FileNotFoundError("Model files not found. Please train the model first.")
    return model, label_encoder

def calculate_shannon_entropy(probabilities):
    """
    Shannon Entropy Uncertainty Quantification:
    H = - sum(p_i * log2(p_i)) for all p_i > 0
    Higher entropy indicates model uncertainty/confusion between classes.
    """
    entropy = 0.0
    for p in probabilities:
        if p > 1e-6:
            entropy -= p * math.log2(p)
    return round(entropy, 3)

def predict_crops(N, P, K, temperature, humidity, ph, rainfall):
    """
    Predict top 3 crops with probabilities, Shannon entropy uncertainty, and XAI feature reasoning.
    
    Returns:
        dict with top_crops, probabilities, confidence, entropy, and reasoning
    """
    clf, le = load_model()
    
    feature_names = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    feature_values = [float(N), float(P), float(K), float(temperature), float(humidity), float(ph), float(rainfall)]
    
    # Prepare input as DataFrame with feature names to prevent scikit-learn warnings
    features_df = pd.DataFrame([feature_values], columns=feature_names)
    
    # Get predictions
    probabilities = clf.predict_proba(features_df)[0]
    
    # Calculate Shannon Entropy
    entropy_score = calculate_shannon_entropy(probabilities)
    
    # Get top 3 crops
    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    
    results = []
    for idx in top_3_idx:
        crop = le.inverse_transform([idx])[0]
        prob = probabilities[idx]
        results.append({
            'crop': str(crop).title(),
            'probability': round(float(prob) * 100, 2)
        })
    
    # Determine confidence based on top probability and Shannon Entropy (Research Paper Eq 1)
    top_prob = results[0]['probability']
    if top_prob >= 75.0 and entropy_score < 1.2:
        confidence = 'High'
    elif top_prob >= 50.0 and entropy_score < 2.0:
        confidence = 'Medium'
    else:
        confidence = 'Low (Uncertainty detected)'
    
    # Get feature importance for reasoning (XAI)
    feature_importance = clf.feature_importances_
    top_features_idx = np.argsort(feature_importance)[-3:][::-1]
    
    reasoning = []
    for idx in top_features_idx:
        reasoning.append({
            'feature': feature_names[idx],
            'value': feature_values[idx],
            'importance': round(float(feature_importance[idx]) * 100, 2)
        })
    
    return {
        'top_crops': results,
        'confidence': confidence,
        'entropy': entropy_score,
        'reasoning': reasoning
    }

# Rich state-district averages lookup
STATE_DISTRICT_AVERAGES = {
    'Punjab': {
        'Ludhiana': {'N': 110, 'P': 45, 'K': 48, 'temperature': 24.5, 'humidity': 68.0, 'ph': 7.2, 'rainfall': 75.0},
        'Amritsar': {'N': 105, 'P': 42, 'K': 45, 'temperature': 23.8, 'humidity': 70.0, 'ph': 7.3, 'rainfall': 80.0},
        'Patiala': {'N': 115, 'P': 48, 'K': 50, 'temperature': 25.0, 'humidity': 65.0, 'ph': 7.1, 'rainfall': 70.0},
        'Jalandhar': {'N': 112, 'P': 46, 'K': 47, 'temperature': 24.2, 'humidity': 69.0, 'ph': 7.2, 'rainfall': 78.0},
        '_default': {'N': 110, 'P': 45, 'K': 48, 'temperature': 24.0, 'humidity': 68.0, 'ph': 7.2, 'rainfall': 75.0}
    },
    'Haryana': {
        'Karnal': {'N': 100, 'P': 50, 'K': 52, 'temperature': 25.2, 'humidity': 64.0, 'ph': 7.4, 'rainfall': 65.0},
        'Hisar': {'N': 85, 'P': 40, 'K': 45, 'temperature': 26.5, 'humidity': 55.0, 'ph': 7.8, 'rainfall': 45.0},
        '_default': {'N': 95, 'P': 46, 'K': 48, 'temperature': 25.5, 'humidity': 60.0, 'ph': 7.5, 'rainfall': 55.0}
    },
    'Uttar Pradesh': {
        'Lucknow': {'N': 90, 'P': 48, 'K': 45, 'temperature': 26.0, 'humidity': 72.0, 'ph': 6.8, 'rainfall': 95.0},
        'Varanasi': {'N': 88, 'P': 52, 'K': 44, 'temperature': 26.5, 'humidity': 74.0, 'ph': 6.9, 'rainfall': 105.0},
        'Agra': {'N': 80, 'P': 42, 'K': 46, 'temperature': 27.0, 'humidity': 58.0, 'ph': 7.3, 'rainfall': 60.0},
        '_default': {'N': 88, 'P': 48, 'K': 45, 'temperature': 26.2, 'humidity': 70.0, 'ph': 7.0, 'rainfall': 90.0}
    },
    'Maharashtra': {
        'Pune': {'N': 75, 'P': 42, 'K': 55, 'temperature': 24.8, 'humidity': 65.0, 'ph': 6.8, 'rainfall': 85.0},
        'Nagpur': {'N': 82, 'P': 46, 'K': 50, 'temperature': 27.5, 'humidity': 60.0, 'ph': 7.2, 'rainfall': 110.0},
        'Nashik': {'N': 70, 'P': 45, 'K': 60, 'temperature': 23.5, 'humidity': 68.0, 'ph': 6.6, 'rainfall': 90.0},
        '_default': {'N': 76, 'P': 44, 'K': 54, 'temperature': 25.5, 'humidity': 64.0, 'ph': 6.9, 'rainfall': 95.0}
    },
    'Gujarat': {
        'Ahmedabad': {'N': 80, 'P': 44, 'K': 46, 'temperature': 27.8, 'humidity': 58.0, 'ph': 7.4, 'rainfall': 70.0},
        'Rajkot': {'N': 72, 'P': 38, 'K': 44, 'temperature': 27.2, 'humidity': 60.0, 'ph': 7.6, 'rainfall': 60.0},
        'Surat': {'N': 85, 'P': 48, 'K': 52, 'temperature': 28.0, 'humidity': 72.0, 'ph': 7.1, 'rainfall': 120.0},
        '_default': {'N': 78, 'P': 43, 'K': 47, 'temperature': 27.5, 'humidity': 62.0, 'ph': 7.4, 'rainfall': 80.0}
    },
    'Rajasthan': {
        'Jaipur': {'N': 65, 'P': 35, 'K': 40, 'temperature': 26.8, 'humidity': 50.0, 'ph': 7.8, 'rainfall': 55.0},
        'Jodhpur': {'N': 55, 'P': 28, 'K': 35, 'temperature': 28.5, 'humidity': 42.0, 'ph': 8.1, 'rainfall': 32.0},
        '_default': {'N': 60, 'P': 32, 'K': 38, 'temperature': 27.5, 'humidity': 46.0, 'ph': 7.9, 'rainfall': 45.0}
    },
    'Karnataka': {
        'Bengaluru': {'N': 70, 'P': 45, 'K': 52, 'temperature': 23.5, 'humidity': 68.0, 'ph': 6.4, 'rainfall': 90.0},
        'Mysuru': {'N': 72, 'P': 42, 'K': 50, 'temperature': 24.2, 'humidity': 70.0, 'ph': 6.5, 'rainfall': 85.0},
        '_default': {'N': 71, 'P': 43, 'K': 51, 'temperature': 24.0, 'humidity': 69.0, 'ph': 6.5, 'rainfall': 88.0}
    },
    'Tamil Nadu': {
        'Coimbatore': {'N': 75, 'P': 40, 'K': 50, 'temperature': 26.0, 'humidity': 66.0, 'ph': 6.8, 'rainfall': 75.0},
        '_default': {'N': 75, 'P': 42, 'K': 48, 'temperature': 27.0, 'humidity': 70.0, 'ph': 6.9, 'rainfall': 90.0}
    },
    'West Bengal': {
        'Kolkata': {'N': 95, 'P': 55, 'K': 48, 'temperature': 27.0, 'humidity': 78.0, 'ph': 6.5, 'rainfall': 160.0},
        'Burdwan': {'N': 98, 'P': 52, 'K': 50, 'temperature': 26.8, 'humidity': 76.0, 'ph': 6.6, 'rainfall': 150.0},
        'Hooghly': {'N': 92, 'P': 50, 'K': 48, 'temperature': 27.2, 'humidity': 77.0, 'ph': 6.7, 'rainfall': 145.0},
        '_default': {'N': 92, 'P': 52, 'K': 46, 'temperature': 26.5, 'humidity': 76.0, 'ph': 6.6, 'rainfall': 150.0}
    },
    'Madhya Pradesh': {
        'Indore': {'N': 82, 'P': 48, 'K': 52, 'temperature': 25.5, 'humidity': 58.0, 'ph': 7.3, 'rainfall': 85.0},
        'Ujjain': {'N': 80, 'P': 46, 'K': 50, 'temperature': 25.8, 'humidity': 56.0, 'ph': 7.4, 'rainfall': 80.0},
        'Bhopal': {'N': 85, 'P': 50, 'K': 54, 'temperature': 26.0, 'humidity': 62.0, 'ph': 7.2, 'rainfall': 95.0},
        'Jabalpur': {'N': 88, 'P': 52, 'K': 52, 'temperature': 25.0, 'humidity': 65.0, 'ph': 7.1, 'rainfall': 110.0},
        '_default': {'N': 84, 'P': 49, 'K': 52, 'temperature': 25.6, 'humidity': 60.0, 'ph': 7.2, 'rainfall': 92.0}
    },
    'Bihar': {
        'Patna': {'N': 92, 'P': 54, 'K': 46, 'temperature': 26.2, 'humidity': 72.0, 'ph': 7.0, 'rainfall': 105.0},
        'Purnia': {'N': 96, 'P': 56, 'K': 48, 'temperature': 25.8, 'humidity': 76.0, 'ph': 6.8, 'rainfall': 130.0},
        'Muzaffarpur': {'N': 90, 'P': 52, 'K': 44, 'temperature': 26.0, 'humidity': 74.0, 'ph': 7.1, 'rainfall': 115.0},
        '_default': {'N': 93, 'P': 54, 'K': 46, 'temperature': 26.0, 'humidity': 74.0, 'ph': 7.0, 'rainfall': 116.0}
    },
    'Andhra Pradesh': {
        'Guntur': {'N': 85, 'P': 46, 'K': 55, 'temperature': 28.5, 'humidity': 68.0, 'ph': 7.2, 'rainfall': 88.0},
        'Kurnool': {'N': 75, 'P': 40, 'K': 50, 'temperature': 29.0, 'humidity': 58.0, 'ph': 7.6, 'rainfall': 65.0},
        'Visakhapatnam': {'N': 82, 'P': 44, 'K': 52, 'temperature': 27.5, 'humidity': 78.0, 'ph': 6.8, 'rainfall': 110.0},
        '_default': {'N': 81, 'P': 43, 'K': 52, 'temperature': 28.3, 'humidity': 68.0, 'ph': 7.2, 'rainfall': 88.0}
    },
    'Telangana': {
        'Nizamabad': {'N': 84, 'P': 48, 'K': 54, 'temperature': 28.0, 'humidity': 64.0, 'ph': 7.1, 'rainfall': 92.0},
        'Warangal': {'N': 86, 'P': 46, 'K': 52, 'temperature': 28.2, 'humidity': 62.0, 'ph': 7.3, 'rainfall': 95.0},
        'Hyderabad': {'N': 80, 'P': 44, 'K': 50, 'temperature': 27.5, 'humidity': 60.0, 'ph': 7.2, 'rainfall': 82.0},
        '_default': {'N': 83, 'P': 46, 'K': 52, 'temperature': 27.9, 'humidity': 62.0, 'ph': 7.2, 'rainfall': 90.0}
    },
    'Kerala': {
        'Wayanad': {'N': 70, 'P': 40, 'K': 75, 'temperature': 22.0, 'humidity': 86.0, 'ph': 5.6, 'rainfall': 220.0},
        'Palakkad': {'N': 78, 'P': 45, 'K': 68, 'temperature': 27.5, 'humidity': 78.0, 'ph': 6.2, 'rainfall': 180.0},
        '_default': {'N': 74, 'P': 42, 'K': 72, 'temperature': 25.0, 'humidity': 82.0, 'ph': 5.9, 'rainfall': 200.0}
    },
    'Assam': {
        'Guwahati': {'N': 90, 'P': 42, 'K': 65, 'temperature': 24.5, 'humidity': 84.0, 'ph': 5.4, 'rainfall': 190.0},
        'Jorhat': {'N': 94, 'P': 40, 'K': 68, 'temperature': 23.8, 'humidity': 86.0, 'ph': 5.2, 'rainfall': 210.0},
        '_default': {'N': 92, 'P': 41, 'K': 66, 'temperature': 24.0, 'humidity': 85.0, 'ph': 5.3, 'rainfall': 200.0}
    },
    'Odisha': {
        'Bhubaneswar': {'N': 85, 'P': 48, 'K': 50, 'temperature': 27.5, 'humidity': 76.0, 'ph': 6.5, 'rainfall': 140.0},
        'Sambalpur': {'N': 82, 'P': 45, 'K': 48, 'temperature': 27.0, 'humidity': 72.0, 'ph': 6.6, 'rainfall': 130.0},
        '_default': {'N': 84, 'P': 46, 'K': 49, 'temperature': 27.2, 'humidity': 74.0, 'ph': 6.5, 'rainfall': 135.0}
    },
    'Himachal Pradesh': {
        'Shimla': {'N': 65, 'P': 40, 'K': 55, 'temperature': 15.0, 'humidity': 68.0, 'ph': 6.2, 'rainfall': 120.0},
        'Kangra': {'N': 72, 'P': 42, 'K': 50, 'temperature': 20.0, 'humidity': 65.0, 'ph': 6.5, 'rainfall': 140.0},
        '_default': {'N': 68, 'P': 41, 'K': 52, 'temperature': 17.5, 'humidity': 66.0, 'ph': 6.3, 'rainfall': 130.0}
    },
    'Jammu and Kashmir': {
        'Srinagar': {'N': 60, 'P': 38, 'K': 52, 'temperature': 13.5, 'humidity': 65.0, 'ph': 6.4, 'rainfall': 85.0},
        'Jammu': {'N': 82, 'P': 44, 'K': 46, 'temperature': 24.0, 'humidity': 62.0, 'ph': 7.2, 'rainfall': 95.0},
        '_default': {'N': 71, 'P': 41, 'K': 49, 'temperature': 18.5, 'humidity': 64.0, 'ph': 6.8, 'rainfall': 90.0}
    }
}

def get_district_averages(state, district):
    """
    Get average soil and weather values for a district
    Fallback hierarchy: District -> State average -> National average
    """
    national_default = {
        'N': 80,
        'P': 50,
        'K': 50,
        'temperature': 25.0,
        'humidity': 68.0,
        'ph': 6.8,
        'rainfall': 95.0
    }
    
    if not state:
        return national_default
        
    state_data = None
    for s_key in STATE_DISTRICT_AVERAGES:
        if s_key.lower() == str(state).strip().lower():
            state_data = STATE_DISTRICT_AVERAGES[s_key]
            break
            
    if not state_data:
        return national_default
        
    if district:
        for d_key in state_data:
            if d_key.lower() == str(district).strip().lower():
                return state_data[d_key]
                
    return state_data.get('_default', national_default)

def get_crop_guide(crop_name):
    """Get cultivation guide for a crop with alias and name support"""
    try:
        guides_df = pd.read_csv('train/dataset/crop_guides.csv')
        c_clean = str(crop_name).strip().lower()
        # Direct match by crop key
        guide = guides_df[guides_df['crop'].str.lower() == c_clean]
        if not guide.empty:
            return guide.iloc[0].to_dict()
        
        # Match by crop_name column containing key
        name_match = guides_df[guides_df['crop_name'].str.lower().str.contains(c_clean, regex=False, na=False)]
        if not name_match.empty:
            return name_match.iloc[0].to_dict()

        # Check aliases
        crop_alias = {
            'chana': 'chickpea', 'arhar': 'pigeonpeas', 'tur': 'pigeonpeas', 'moong': 'mungbean',
            'urad': 'blackgram', 'masoor': 'lentil', 'rajma': 'kidneybeans', 'matki': 'mothbeans',
            'lobia': 'cowpea', 'matar': 'green_peas', 'kulthi': 'horsegram', 'gehu': 'wheat',
            'dhan': 'rice', 'paddy': 'rice', 'makka': 'maize', 'sarson': 'mustard', 'kapas': 'cotton',
            'ganna': 'sugarcane', 'aalu': 'potato', 'pyaz': 'onion', 'tamatar': 'tomato',
            'adrak': 'ginger', 'haldi': 'turmeric', 'mirch': 'chilli', 'lahsun': 'garlic',
            'chiku': 'sapota', 'sitaphal': 'custard_apple', 'amrood': 'guava', 'anar': 'pomegranate',
            'tarbooj': 'watermelon', 'kharbooja': 'muskmelon', 'nimbu': 'lemon', 'lauki': 'bottle_gourd',
            'karela': 'bitter_gourd', 'kheera': 'cucumber', 'shimla_mirch': 'capsicum', 'aam': 'mango',
            'kela': 'banana', 'seb': 'apple', 'santra': 'orange', 'papita': 'papaya', 'angoor': 'grapes',
            'nariyal': 'coconut', 'badam': 'almond', 'akhrot': 'walnut', 'nashpati': 'pear'
        }
        if c_clean in crop_alias:
            target = crop_alias[c_clean]
            guide = guides_df[guides_df['crop'].str.lower() == target]
            if not guide.empty:
                return guide.iloc[0].to_dict()

        return None
    except Exception as e:
        print(f"Error loading crop guide: {e}")
        return None

def get_crop_finance(crop_name):
    """Get financial data for a crop"""
    try:
        finance_df = pd.read_csv('train/dataset/india_crop_production.csv')
        crop_data = finance_df[finance_df['Crop'].str.lower() == str(crop_name).strip().lower()]
        if not crop_data.empty:
            return crop_data.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error loading crop finance: {e}")
        return None

def get_government_schemes():
    """Get all government schemes"""
    try:
        schemes_df = pd.read_csv('train/dataset/govt_schemes.csv')
        return schemes_df.to_dict('records')
    except Exception as e:
        print(f"Error loading schemes: {e}")
        return []

def get_soil_labs(state=None, district=None):
    """Get soil testing labs"""
    try:
        labs_df = pd.read_csv('train/dataset/soil_labs.csv')
        if state and str(state).strip().lower() != 'all' and str(state).strip() != '':
            labs_df = labs_df[labs_df['state'].str.lower() == str(state).strip().lower()]
        if district and str(district).strip().lower() != 'all' and str(district).strip() != '':
            labs_df = labs_df[labs_df['district'].str.lower() == str(district).strip().lower()]
        return labs_df.to_dict('records')
    except Exception as e:
        print(f"Error loading soil labs: {e}")
        return []
