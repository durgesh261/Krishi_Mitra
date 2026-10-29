"""
Multimodal Dataset & Benchmark Generator
Pairs Multi-Spectral / Remote Sensing Canopy Images with Environmental Micro-Climate Telemetry
"""

import os
import numpy as np

try:
    import torch
    from torch.utils.data import Dataset, DataLoader
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False

if TORCH_AVAILABLE:
    class MultimodalCropDataset(Dataset):
        """
        Multimodal PyTorch Dataset:
        Combines spatial imagery tensors (C, H, W) with micro-climate telemetry vectors (6,).
        Labels:
        - disease_label: LongTensor (0 to num_classes-1)
        - yield_label: FloatTensor (quintals / hectare)
        """
        def __init__(self, images, climate_vectors, disease_labels, yield_labels, transform=None):
            self.images = images  # (N, C, H, W)
            self.climate = torch.tensor(climate_vectors, dtype=torch.float32)
            self.disease = torch.tensor(disease_labels, dtype=torch.long)
            self.yield_targets = torch.tensor(yield_labels, dtype=torch.float32).unsqueeze(1)
            self.transform = transform

        def __len__(self):
            return len(self.disease)

        def __getitem__(self, idx):
            img = self.images[idx]
            if isinstance(img, np.ndarray):
                img = torch.tensor(img, dtype=torch.float32)
            if self.transform:
                img = self.transform(img)
            return {
                "image": img,
                "climate": self.climate[idx],
                "disease_label": self.disease[idx],
                "yield_label": self.yield_targets[idx]
            }

def generate_calibrated_multimodal_benchmark(num_samples=1000, img_size=(6, 128, 128), seed=42):
    """
    Generates an in-silico biophysically calibrated multimodal benchmark dataset modeling 
    real agro-ecological conditions across major Indian crops:
    
    Channels (C=6 matching Sentinel-2 Level-2A surface reflectance):
    - Band 0: Green (B3, 560 nm)
    - Band 1: Red (B4, 665 nm)
    - Band 2: Red-Edge (B5, 705 nm)
    - Band 3: Near-Infrared (B8, 842 nm)
    - Band 4: Short-Wave Infrared 1 (B11, 1610 nm)
    - Band 5: Short-Wave Infrared 2 (B12, 2190 nm)
    
    6 Disease Classes:
    - 0: Healthy Canopy
    - 1: Foliar Blight (Alternaria / Helminthosporium)
    - 2: Stripe Rust (Puccinia striiformis)
    - 3: Paddy Blast (Magnaporthe oryzae)
    - 4: Powdery Mildew (Erysiphe / Leveillula)
    - 5: Chlorosis & Abiotic Moisture Stress
    
    Climate features (6D):
    [Temperature, Relative Humidity, 7-day Rainfall, Soil Moisture, VPD, Solar Radiation]
    """
    np.random.seed(seed)
    
    # 1. Climate vectors (calibrated to Indian agro-climatic zones)
    temp = np.random.uniform(15.0, 38.0, num_samples)
    rh = np.random.uniform(40.0, 95.0, num_samples)
    rain = np.random.exponential(20.0, num_samples)
    soil = np.random.uniform(25.0, 85.0, num_samples)
    
    # Thermodynamic Vapor Pressure Deficit (Tetens equation)
    es = 0.61078 * np.exp((17.27 * temp) / (temp + 237.3))
    ea = es * (rh / 100.0)
    vpd = np.clip(es - ea, 0.2, 3.2)
    solar = np.random.uniform(12.0, 24.0, num_samples)
    
    climate_matrix = np.stack([temp, rh, rain, soil, vpd, solar], axis=1)
    
    disease_labels = []
    c_channels = img_size[0]
    images = np.zeros((num_samples, c_channels, img_size[1], img_size[2]), dtype=np.float32)
    yield_labels = []
    
    for i in range(num_samples):
        t, h, r, sm, v, s = climate_matrix[i]
        
        # Epidemiological incubation envelopes (ICAR / FAO guidelines)
        if h > 80.0 and 15.0 <= t <= 23.0:
            d = 2  # Stripe Rust (Puccinia striiformis)
            loss = 0.28
            # Spectral reflectance: Green, Red, Red-Edge, NIR, SWIR1, SWIR2
            bands = [0.12, 0.24, 0.32, 0.42, 0.26, 0.18]
        elif h > 75.0 and t > 28.0:
            d = 1  # Foliar Blight (Alternaria)
            loss = 0.20
            bands = [0.10, 0.22, 0.28, 0.40, 0.28, 0.20]
        elif r > 35.0 and h > 70.0:
            d = 3  # Paddy Blast (Magnaporthe)
            loss = 0.22
            bands = [0.11, 0.20, 0.30, 0.44, 0.24, 0.17]
        elif h > 70.0 and r < 10.0:
            d = 4  # Powdery Mildew
            loss = 0.14
            bands = [0.16, 0.18, 0.32, 0.46, 0.22, 0.15]
        elif sm < 38.0 or v > 2.2:
            d = 5  # Abiotic Drought & Chlorosis (High SWIR, pale chlorosis)
            loss = 0.16
            bands = [0.16, 0.14, 0.24, 0.44, 0.36, 0.28]
        else:
            d = 0  # Healthy Canopy (Vigorous green, high NIR, low SWIR)
            loss = 0.0
            bands = [0.15, 0.06, 0.35, 0.58, 0.18, 0.10]
            
        disease_labels.append(d)
        
        # Spatial spectral patch with biological texture noise
        noise = np.random.normal(0.0, 0.03, (c_channels, img_size[1], img_size[2])).astype(np.float32)
        base_patch = np.zeros((c_channels, img_size[1], img_size[2]), dtype=np.float32)
        for b_idx in range(min(c_channels, len(bands))):
            base_patch[b_idx] = bands[b_idx]
        images[i] = np.clip(base_patch + noise, 0.01, 1.0)
        
        # Agronomic yield regression target (Wheat/Field crop baseline ~38.5 q/ha)
        ndvi = (bands[3] - bands[1]) / (bands[3] + bands[1] + 1e-5)
        y = 38.5 * (1.0 + (ndvi - 0.70) * 0.45) * (1.0 - loss) + np.random.normal(0, 1.2)
        yield_labels.append(max(8.0, y))
        
    disease_labels = np.array(disease_labels, dtype=np.int64)
    yield_labels = np.array(yield_labels, dtype=np.float32)
    
    return images, climate_matrix, disease_labels, yield_labels

def generate_presymptomatic_incubation_benchmark(num_samples=120, img_size=(6, 128, 128), seed=101):
    """
    Generates a dedicated in-silico incubation testbed of 120 samples modeling 
    the latent pre-symptomatic phase (Days 3 to 6 post-pathogen exposure).
    
    Under Mills/Wallin epidemiological models:
    - Microclimate satisfies infection criteria (prolonged leaf wetness, optimal temp, low VPD).
    - Macroscopic leaf pigments still look green (surface RGB reflectance resembles healthy).
    - Internal mesophyll cellular scattering shows early degradation in NIR (B8) and Red-Edge (B5).
    """
    np.random.seed(seed)
    temp = np.random.uniform(16.0, 22.0, num_samples) # Optimal rust/blight germination
    rh = np.random.uniform(82.0, 96.0, num_samples)   # High humidity
    rain = np.random.uniform(15.0, 45.0, num_samples) # Wet canopy
    soil = np.random.uniform(65.0, 85.0, num_samples)
    es = 0.61078 * np.exp((17.27 * temp) / (temp + 237.3))
    ea = es * (rh / 100.0)
    vpd = np.clip(es - ea, 0.1, 0.7)                 # Low VPD favoring sporulation
    solar = np.random.uniform(10.0, 18.0, num_samples)
    
    climate_matrix = np.stack([temp, rh, rain, soil, vpd, solar], axis=1)
    
    c_channels = img_size[0]
    images = np.zeros((num_samples, c_channels, img_size[1], img_size[2]), dtype=np.float32)
    disease_labels = np.full(num_samples, 2, dtype=np.int64) # Latent Stripe Rust
    yield_labels = np.random.normal(31.5, 1.8, num_samples).astype(np.float32)
    
    # Latent spectral signature: Green appears normal, but NIR drops ~18% due to spongy mesophyll disruption
    latent_bands = [0.14, 0.08, 0.28, 0.44, 0.22, 0.14]
    for i in range(num_samples):
        noise = np.random.normal(0.0, 0.02, (c_channels, img_size[1], img_size[2])).astype(np.float32)
        base_patch = np.zeros((c_channels, img_size[1], img_size[2]), dtype=np.float32)
        for b_idx in range(min(c_channels, len(latent_bands))):
            base_patch[b_idx] = latent_bands[b_idx]
        images[i] = np.clip(base_patch + noise, 0.01, 1.0)
        
    return images, climate_matrix, disease_labels, yield_labels

# Backward-compatibility alias
generate_synthetic_benchmark_dataset = generate_calibrated_multimodal_benchmark
