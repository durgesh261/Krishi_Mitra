"""
Crop Recommendation System
"""
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
    """Load the trained model and encoder"""
    global model, label_encoder
    if model is None:
        if os.path.exists(MODEL_PATH) and os.path.exists(ENCODER_PATH):
            model = joblib.load(MODEL_PATH)
            label_encoder = joblib.load(ENCODER_PATH)
            print("✓ Crop recommendation model loaded")
        else:
            raise FileNotFoundError("Model files not found. Please train the model first.")
    return model, label_encoder

def predict_crops(N, P, K, temperature, humidity, ph, rainfall):
    """
    Predict top 3 crops with probabilities and confidence
    
    Returns:
        dict with top_crops, probabilities, confidence, and reasoning
    """
    model, le = load_model()
    
    # Prepare input
    features = np.array([[N, P, K, temperature, humidity, ph, rainfall]])
    
    # Get predictions
    probabilities = model.predict_proba(features)[0]
    
    # Get top 3 crops
    top_3_idx = np.argsort(probabilities)[-3:][::-1]
    
    results = []
    for idx in top_3_idx:
        crop = le.inverse_transform([idx])[0]
        prob = probabilities[idx]
        results.append({
            'crop': crop.title(),
            'probability': round(prob * 100, 2)
        })
    
    # Calculate confidence level
    top_prob = results[0]['probability']
    if top_prob >= 80:
        confidence = 'High'
    elif top_prob >= 60:
        confidence = 'Medium'
    else:
        confidence = 'Low'
    
    # Get feature importance for reasoning
    feature_names = ['N', 'P', 'K', 'Temperature', 'Humidity', 'pH', 'Rainfall']
    feature_values = [N, P, K, temperature, humidity, ph, rainfall]
    feature_importance = model.feature_importances_
    
    # Get top 3 influential features
    top_features_idx = np.argsort(feature_importance)[-3:][::-1]
    reasoning = []
    for idx in top_features_idx:
        reasoning.append({
            'feature': feature_names[idx],
            'value': feature_values[idx],
            'importance': round(feature_importance[idx] * 100, 2)
        })
    
    return {
        'top_crops': results,
        'confidence': confidence,
        'reasoning': reasoning
    }

def get_district_averages(state, district):
    """
    Get average soil and weather values for a district
    Fallback: state average -> national average
    """
    # For now, return sample averages
    # In production, this would query the district dataset
    
    # Default national averages
    defaults = {
        'N': 80,
        'P': 50,
        'K': 50,
        'temperature': 25,
        'humidity': 70,
        'ph': 6.5,
        'rainfall': 100
    }
    
    return defaults

# Load crop guides
def get_crop_guide(crop_name):
    """Get cultivation guide for a crop"""
    try:
        guides_df = pd.read_csv('train/dataset/crop_guides.csv')
        guide = guides_df[guides_df['crop'].str.lower() == crop_name.lower()]
        
        if not guide.empty:
            return guide.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error loading crop guide: {e}")
        return None

# Load crop finance data
def get_crop_finance(crop_name):
    """Get financial data for a crop"""
    try:
        finance_df = pd.read_csv('train/dataset/india_crop_production.csv')
        crop_data = finance_df[finance_df['Crop'].str.lower() == crop_name.lower()]
        
        if not crop_data.empty:
            return crop_data.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"Error loading crop finance: {e}")
        return None

# Load government schemes
def get_government_schemes():
    """Get all government schemes"""
    try:
        schemes_df = pd.read_csv('train/dataset/govt_schemes.csv')
        return schemes_df.to_dict('records')
    except Exception as e:
        print(f"Error loading schemes: {e}")
        return []

# Load soil labs
def get_soil_labs(state=None, district=None):
    """Get soil testing labs"""
    try:
        labs_df = pd.read_csv('train/dataset/soil_labs.csv')
        
        if state:
            labs_df = labs_df[labs_df['state'].str.lower() == state.lower()]
        if district:
            labs_df = labs_df[labs_df['district'].str.lower() == district.lower()]
        
        return labs_df.to_dict('records')
    except Exception as e:
        print(f"Error loading soil labs: {e}")
        return []
