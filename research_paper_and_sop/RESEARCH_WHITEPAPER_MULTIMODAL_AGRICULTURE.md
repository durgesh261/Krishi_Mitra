# 🛰️ Multimodal Deep Learning for Multi-Spectral Crop Disease Diagnosis & Yield Prediction: A Gated Cross-Attention Framework Combining Remote Sensing Imagery with Climate Telemetry

**Authors:** Durgesh & The Krishi Mitra Research Group  
**Domain:** Deep Learning • Computer Vision • Remote Sensing • Precision Agriculture • Multimodal Fusion  
**Repository:** [https://github.com/durgesh261/Krishi_Mitra](https://github.com/durgesh261/Krishi_Mitra)

---

## 📄 Abstract

Accurate early detection of foliar crop diseases and localized yield estimation are pivotal for national food security and precision agronomy. Existing computer vision solutions rely predominantly on RGB leaf photography captured under controlled lighting conditions, rendering them vulnerable to early-stage symptom latency, field occlusion, and visual confusion between biotic pathogens and abiotic moisture stress. 

In this work, we propose **MultimodalCropNet**, an end-to-end multi-task deep learning architecture that fuses **spatial multi-spectral canopy imagery** (synthesized from high-resolution UAV multispectral cameras and ESA Sentinel-2 L2A surface reflectance) with **continuous micro-climatic environmental telemetry** (ambient temperature, relative humidity, cumulative precipitation, root-zone soil moisture, and vapor pressure deficit). Rather than relying on naive early concatenation, we introduce a **Gated Cross-Modal Attention Fusion (GCAF)** mechanism that dynamically weights visual spectral cues against localized disease-conduciveness windows. Furthermore, we incorporate **Gradient-Weighted Class Activation Mapping (Grad-CAM)** to delineate localized pathogen sporulation and compute canopy vegetation indices ($\text{NDVI}$, $\text{NDWI}$, $\text{SAVI}$, $\text{GNDVI}$). 

Extensive empirical evaluations across 1,000 paired multimodal agro-instances demonstrate that our proposed framework achieves **95.8% Top-1 Accuracy** and **95.5% Macro F1-score** on disease classification—outperforming single-modality vision baselines by **+14.2% F1**—while reducing yield forecast Root Mean Squared Error (RMSE) from **6.42 q/ha to 3.12 q/ha** (a **51.4% error reduction**).

---

## 1. Introduction & Research Problem

Single-image classification methods in precision agriculture suffer from three fundamental limitations:
1. **Symptom Latency:** Visual chlorosis or necrosis appears days or weeks *after* fungal mycelium has colonized the plant tissue. During this incubation phase, atmospheric humidity ($>80\%$) and temperature ($18^\circ\text{C}-24^\circ\text{C}$) are far more predictive than visual RGB spectrum.
2. **Abiotic vs. Biotic Visual Ambiguity:** Nitrogen deficiency, leaf drought scorch, and fungal stripe rust often exhibit identical visual yellowing on camera sensors. Distinguishing between them requires ground soil moisture and atmospheric vapor pressure deficit ($\text{VPD}$).
3. **Decoupled Yield Forecasting:** Traditional agronomic models predict yield solely from historical regional rainfall averages, neglecting real-time pathogen damage across the crop canopy.

To solve these challenges, we combine:
* **Spatial Stream:** 4-band / 12-band multispectral canopy signatures (NIR, Red-Edge, Red, Green, SWIR).
* **Telemetry Stream:** Continuous agro-meteorological vector $\mathbf{x}_{\text{clim}} \in \mathbb{R}^6$.
* **Dual Task Heads:** Joint multi-class pathogen risk classification and regression yield estimation.

---

## 2. Mathematical Methodology & Architecture

### 2.1 Multi-Spectral Vegetative & Hydrological Indices
Given surface reflectance in Near-Infrared ($\rho_{\text{NIR}}$), Red ($\rho_{\text{Red}}$), Green ($\rho_{\text{Green}}$), and Short-Wave Infrared ($\rho_{\text{SWIR}}$):

* **Normalized Difference Vegetation Index (NDVI):**
  $$\text{NDVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Red}}}{\rho_{\text{NIR}} + \rho_{\text{Red}} + \epsilon}$$
* **Normalized Difference Water Index (NDWI):**
  $$\text{NDWI} = \frac{\rho_{\text{NIR}} - \rho_{\text{SWIR}}}{\rho_{\text{NIR}} + \rho_{\text{SWIR}} + \epsilon}$$
* **Soil-Adjusted Vegetation Index (SAVI, $L=0.5$):**
  $$\text{SAVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Red}}}{\rho_{\text{NIR}} + \rho_{\text{Red}} + L} \times (1 + L)$$
* **Green NDVI (Chlorophyll Vigor):**
  $$\text{GNDVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Green}}}{\rho_{\text{NIR}} + \rho_{\text{Green}} + \epsilon}$$

### 2.2 Deep Spatial Feature Extraction
The canopy image $\mathbf{I} \in \mathbb{R}^{H \times W \times C}$ is passed through a convolutional/transformer backbone (ConvNeXt-Tiny / ResNet-50) pretrained with self-supervised masked image modeling:
$$\mathbf{F}_v = \text{Backbone}(\mathbf{I}) \in \mathbb{R}^{H' \times W' \times D_v}$$
$$\mathbf{z}_v = \text{GlobalAvgPool}(\mathbf{F}_v) \in \mathbb{R}^{D_v}$$

### 2.3 Environmental Telemetry Encoder
The meteorological telemetry vector $\mathbf{x}_{\text{clim}} = [T, RH, P_{7d}, SM, VPD, GDD]^T \in \mathbb{R}^6$ is projected into latent feature space via a 2-layer MLP with Layer Normalization and GELU non-linearities:
$$\mathbf{z}_{\text{clim}} = \text{LayerNorm}\left(\mathbf{W}_2 \cdot \text{GELU}(\mathbf{W}_1 \mathbf{x}_{\text{clim}} + \mathbf{b}_1) + \mathbf{b}_2\right) \in \mathbb{R}^{D_c}$$

### 2.4 Gated Cross-Modal Attention Fusion (GCAF)
Rather than simple feature concatenation, we construct a dynamic gating mechanism that allows meteorological risk to modulate visual attention:
$$\mathbf{h}_v = \mathbf{W}_v \mathbf{z}_v \in \mathbb{R}^D, \quad \mathbf{h}_c = \mathbf{W}_c \mathbf{z}_{\text{clim}} \in \mathbb{R}^D$$
$$\boldsymbol{\alpha} = \sigma\left(\mathbf{W}_g [\mathbf{h}_v; \mathbf{h}_c] + \mathbf{b}_g\right) \in [0, 1]^D$$
$$\mathbf{z}_{\text{fused}} = \text{LayerNorm}\left(\boldsymbol{\alpha} \odot \mathbf{h}_v + (\mathbf{1} - \boldsymbol{\alpha}) \odot \mathbf{h}_c\right)$$
where $\sigma$ denotes the sigmoid activation function and $\odot$ denotes the Hadamard element-wise product.

### 2.5 Multi-Task Loss Formulation
$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CE}}(\hat{\mathbf{y}}_{\text{disease}}, \mathbf{y}_{\text{disease}}) + \lambda \cdot \mathcal{L}_{\text{MSE}}(\hat{y}_{\text{yield}}, y_{\text{yield}})$$
where $\lambda = 0.05$ scales the regression penalty across dimensions.

---

## 3. Empirical Results & Ablation Study

| Model Configuration | Modalities | Disease Top-1 Acc | Disease Macro F1 | Yield RMSE (q/ha) | Yield MAE (q/ha) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Vision Baseline** (ConvNeXt / ResNet-50) | Image Only | 82.4% | 81.3% | 6.42 | 5.10 |
| **Climate Baseline** (TabNet / MLP) | Telemetry Only | 71.2% | 69.8% | 8.15 | 6.72 |
| **Early Fusion Baseline** | Image + Telemetry Concat | 88.0% | 87.2% | 4.85 | 3.90 |
| **Late Decision Fusion** | Logit Averaging | 89.4% | 88.6% | 4.40 | 3.55 |
| **Proposed Gated Cross-Attention** | **Multimodal GCAF** | **95.8%** | **95.5%** *(+14.2%)* | **3.12** *(-51.4%)* | **2.45** |

### 3.1 Explainability via Grad-CAM
Visual attention maps demonstrate that the GCAF module focuses attention on actual pathogen sporulation pustules on the leaf surface (red activation $\ge 0.85$), while background soil furrows and shadow regions are effectively filtered out.
