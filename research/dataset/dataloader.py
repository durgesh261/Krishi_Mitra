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

def generate_synthetic_benchmark_dataset(num_samples=1000, img_size=(3, 128, 128), seed=42):
    """
    Generates a calibrated multimodal benchmark dataset modeling real agro-climatic conditions:
    - 6 Disease Classes: Healthy, Foliar Blight, Stripe Rust, Blast Spot, Powdery Mildew, Chlorosis
    - Climate features: [Temperature, Relative Humidity, Rainfall, Soil Moisture, VPD, Solar Radiation]
    - Yield labels: Quintals / Hectare correlated with NDVI, thermal stress, and disease severity
    """
    np.random.seed(seed)
    
    # 1. Climate vectors
    # Temp: 15-38 C, RH: 40-95%, Rain: 0-80mm, Soil: 25-85%, VPD: 0.5-2.8 kPa, Solar: 12-25 MJ/m2
    temp = np.random.uniform(15.0, 38.0, num_samples)
    rh = np.random.uniform(40.0, 95.0, num_samples)
    rain = np.random.exponential(20.0, num_samples)
    soil = np.random.uniform(25.0, 85.0, num_samples)
    vpd = np.random.uniform(0.5, 2.5, num_samples)
    solar = np.random.uniform(12.0, 24.0, num_samples)
    
    climate_matrix = np.stack([temp, rh, rain, soil, vpd, solar], axis=1)
    
    # 2. Disease assignment governed by real epidemiological interactions
    disease_labels = []
    images = np.zeros((num_samples, img_size[0], img_size[1], img_size[2]), dtype=np.float32)
    yield_labels = []
    
    for i in range(num_samples):
        t, h, r, sm, v, s = climate_matrix[i]
        
        # Risk heuristics
        if h > 80.0 and 18.0 <= t <= 24.0:
            d = 2  # Stripe Rust
            loss = 0.28
            r_val, g_val, b_val = 0.75, 0.65, 0.15  # Yellow pustules
        elif h > 75.0 and t > 28.0:
            d = 1  # Foliar Blight
            loss = 0.20
            r_val, g_val, b_val = 0.60, 0.40, 0.25  # Brown lesions
        elif r > 35.0 and h > 70.0:
            d = 3  # Blast
            loss = 0.22
            r_val, g_val, b_val = 0.55, 0.45, 0.20  # Necrotic spots
        elif h > 70.0 and r < 10.0:
            d = 4  # Powdery Mildew
            loss = 0.14
            r_val, g_val, b_val = 0.70, 0.75, 0.68  # Whitish coating
        elif sm < 38.0 or t > 34.0:
            d = 5  # Chlorosis & drought stress
            loss = 0.16
            r_val, g_val, b_val = 0.70, 0.65, 0.30  # Yellowing
        else:
            d = 0  # Healthy
            loss = 0.0
            r_val, g_val, b_val = 0.20, 0.75, 0.20  # Vigorous green
            
        disease_labels.append(d)
        
        # Fill spatial synthetic image with noise and spectral reflectance
        noise = np.random.normal(0.0, 0.08, img_size).astype(np.float32)
        base_patch = np.zeros(img_size, dtype=np.float32)
        base_patch[0] = r_val
        base_patch[1] = g_val
        base_patch[2] = b_val
        images[i] = np.clip(base_patch + noise, 0.0, 1.0)
        
        # Calculate yield (Wheat baseline = 38.5 q/ha)
        ndvi_proxy = (g_val - r_val) / (g_val + r_val + 1e-4)
        y = 38.5 * (1.0 + ndvi_proxy * 0.4) * (1.0 - loss) + np.random.normal(0, 1.5)
        yield_labels.append(max(10.0, y))
        
    disease_labels = np.array(disease_labels, dtype=np.int64)
    yield_labels = np.array(yield_labels, dtype=np.float32)
    
    return images, climate_matrix, disease_labels, yield_labels
