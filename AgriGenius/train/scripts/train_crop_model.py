"""
Train Crop Recommendation Model
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

print("="*70)
print("Training Crop Recommendation Model")
print("="*70)

# Load dataset
print("\n1. Loading dataset...")
df = pd.read_csv('train/dataset/crop_dataset.csv')
print(f"   Dataset shape: {df.shape}")
print(f"   Crops: {sorted(df['label'].unique())}")

# Prepare features and target
print("\n2. Preparing features...")
X = df[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']]
y = df['label']

# Encode labels
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)
print(f"   Training samples: {len(X_train)}")
print(f"   Testing samples: {len(X_test)}")

# Train model
print("\n3. Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=100,
    max_depth=20,
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)
print("   ✓ Model trained")

# Evaluate
print("\n4. Evaluating model...")
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"   Accuracy: {accuracy*100:.2f}%")

# Get feature importance
feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)
print("\n   Feature Importance:")
for _, row in feature_importance.iterrows():
    print(f"     {row['feature']}: {row['importance']:.4f}")

# Save model and encoder
print("\n5. Saving model...")
os.makedirs('train/models', exist_ok=True)
joblib.dump(model, 'train/models/crop_recommendation_model.pkl')
joblib.dump(le, 'train/models/crop_label_encoder.pkl')
print("   ✓ Model saved to train/models/crop_recommendation_model.pkl")
print("   ✓ Encoder saved to train/models/crop_label_encoder.pkl")

# Test prediction
print("\n6. Testing prediction...")
sample = X_test.iloc[0:1]
pred_proba = model.predict_proba(sample)[0]
top_3_idx = np.argsort(pred_proba)[-3:][::-1]
print(f"   Sample input: {sample.values[0]}")
print(f"   Top 3 predictions:")
for idx in top_3_idx:
    crop = le.inverse_transform([idx])[0]
    prob = pred_proba[idx]
    print(f"     {crop}: {prob*100:.2f}%")

print("\n" + "="*70)
print("Model Training Complete!")
print("="*70)
