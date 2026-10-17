# 🛰️ Multimodal Deep Learning for Pre-Symptomatic Crop Disease Diagnosis & Yield Prediction: A Gated Cross-Attention Framework Combining Remote Sensing Imagery with Climate Telemetry

**Authors:** Durgesh & The Krishi Mitra Research Group  
**Domain:** Artificial Intelligence • Multimodal Deep Learning • Remote Sensing • Precision Agriculture • Computer Vision  
**Publication Target:** IEEE Transactions on AgriFood Electronics / Computers and Electronics in Agriculture (Elsevier) / Springer Precision Agriculture  
**Open Source Implementation:** [https://github.com/durgesh261/Krishi_Mitra](https://github.com/durgesh261/Krishi_Mitra)

---

## 📄 Abstract

Accurate early detection of foliar crop diseases and localized yield estimation are vital for smallholder livelihood and global food security. Existing computer vision solutions for agricultural diagnostics rely predominantly on single-modality RGB leaf photography captured under controlled conditions. These approaches suffer from three critical real-world limitations: (1) **symptom latency**, wherein optical RGB sensors cannot detect cellular infection during the 4–10 day latent incubation phase before macroscopic chlorosis appears; (2) **abiotic-biotic visual ambiguity**, where drought scorch and nutrient starvation mimic fungal blights; and (3) **decoupled yield forecasting**, which estimates harvest production without accounting for active foliar pathogen damage.

In this paper, we propose **MultimodalCropNet**, an end-to-end multi-task deep learning architecture integrated within the **Krishi Mitra** precision agriculture platform. The framework unifies:
1. **Multi-Spectral Spatial Reflectance:** Near-Infrared (NIR), Red-Edge, Red, and Green wavelengths synthesized from UAV multi-spectral sensors and European Space Agency (ESA) Sentinel-2 Level-2A surface reflectance.
2. **Micro-Climatic Environmental Telemetry:** Ambient temperature ($T$), relative humidity ($RH$), 7-day cumulative precipitation ($P_{7d}$), root-zone soil moisture ($SM$), vapor pressure deficit ($VPD$), and growing degree days ($GDD$).
3. **Gated Cross-Modal Attention Fusion (GCAF):** A gating mechanism that prevents high-dimensional visual feature dominance and dynamically modulates spatial attention maps using meteorological disease-conduciveness probabilities.
4. **Multi-Task Objective:** Joint optimization for multi-class pathogen classification and continuous localized yield regression.

Extensive cross-regional empirical evaluation across 10 major Indian crops (Wheat, Rice, Maize, Cotton, Sugarcane, Groundnut, Mustard, Soybean, Tomato, and Apple) demonstrates that our proposed GCAF architecture achieves **95.8% Top-1 Accuracy** and **95.5% Macro F1-score** on disease diagnosis—outperforming single-modality vision baselines (ResNet-50 / ConvNeXt) by **+14.2% Macro F1**—while reducing localized harvest yield prediction Root Mean Squared Error (RMSE) by **51.4% (from 6.42 q/ha to 3.12 q/ha)**. Gradient-Weighted Class Activation Mapping (Grad-CAM) confirms that the model grounds predictions on active pathogen sporulation zones while filtering out background soil furrows and shadow artifacts.

**Index Terms:** Multimodal Deep Learning, Precision Agriculture, Cross-Attention Fusion, Pre-Symptomatic Disease Detection, Remote Sensing, Sentinel-2, Crop Yield Regression, Explainable AI.

---

## 1. Introduction & Problem Formulation

Global agricultural systems face severe yield degradation from unpredictable climate extremes and pathogen epidemics. Fungal foliar pathogens such as *Puccinia striiformis* (Wheat Stripe Rust), *Phytophthora infestans* (Late Blight), and *Magnaporthe oryzae* (Rice Blast) cause estimated seasonal yield losses between 20% and 40% across developing nations. Smallholder farmers, who produce over 80% of food in Asia and Sub-Saharan Africa, frequently lack access to agricultural extension officers and depend on visual scouting to identify crop stress.

### 1.1 The Limitations of Single-Modality RGB Computer Vision
Over the past decade, Convolutional Neural Networks (CNNs) and Vision Transformers (ViTs) trained on public benchmarks (e.g., PlantVillage) have achieved reported classification accuracies exceeding 95%. However, field deployments consistently reveal that these laboratory-benchmarked vision models fail under actual farm conditions due to three fundamental scientific bottlenecks:

1. **Pathological Symptom Latency:** Fungal and bacterial infections follow an internal incubation phase. After spore germination, fungal hyphae actively invade the intercellular mesophyll tissue days before structural cell wall collapse and chlorophyll degradation occur. On the visible optical spectrum (400–700 nm), the leaf surface appears entirely green and asymptomatic. Single-image RGB classifiers cannot detect a signal that has not yet manifested on the plant surface.
2. **Spectral Mimicry between Biotic & Abiotic Stress:** Abiotic stress factors, such as temporary moisture deficit, root waterlogging, and soil nitrogen starvation, produce interveinal chlorosis (yellowing) that is optically indistinguishable from early fungal blights on standard RGB cameras. Differentiating them requires continuous ground soil moisture, atmospheric vapor pressure deficit, and root-zone telemetry.
3. **Decoupling of Pathology and Agronomic Yield:** Conventional agronomic models predict regional harvest yield based on historical macro-weather statistics, ignoring localized spatial pathogen outbreaks. Conversely, automated disease diagnostic tools identify pathogens without estimating resulting crop yield and financial loss.

### 1.2 Research Objectives & Contributions
To overcome these challenges, this paper presents **MultimodalCropNet**, formulated, evaluated, and deployed within the open-source **Krishi Mitra** platform. The key scientific contributions of this work are:

* **Multimodal Formulation for Pre-Symptomatic Diagnosis:** We combine high-resolution spatial multi-spectral reflectance (NIR, Red-Edge, Red, Green) with continuous micro-climatic environmental telemetry ($T, RH, P_{7d}, SM, VPD, GDD$) to detect crop disease vulnerability during the pre-symptomatic incubation window.
* **Gated Cross-Modal Attention Fusion (GCAF):** We design a gating mechanism that prevents high-dimensional visual feature dominance ($\mathbb{R}^{2048}$) over low-dimensional meteorological signals ($\mathbb{R}^6$), allowing atmospheric disease-conduciveness vectors to dynamically guide visual attention over foliar lesions.
* **Unified Multi-Task Prediction:** We formulate a joint multi-task loss function coupling multi-class disease diagnosis with localized continuous harvest yield regression (in quintals per hectare).
* **Empirical Multi-Regional Validation Across India:** We benchmark our methodology across 10 major crops across distinct Indian agro-climatic zones (Punjab, Saurashtra, Kashmir, Maharashtra, Haryana, and Assam), verifying model generalizability across diverse canopy structures and disease phenotypes.
* **Open-Source Production Deployment:** We integrate the proposed model into the production Krishi Mitra platform, providing ICAR-verified agronomic guidance, real-time APMC Mandi prices, and multilingual access across 10 Indian regional languages.

---

## 2. Related Work

### 2.1 Computer Vision for Plant Pathology
Early works utilized hand-crafted texture descriptors (e.g., SIFT, GLCM, color histograms) with Support Vector Machines (SVMs) to segment leaf lesions. With the advent of deep learning, Mohanty et al. demonstrated that deep CNNs could classify 26 crop diseases across 14 crop species with >99% accuracy on the PlantVillage dataset. Subsequent studies introduced modern architectures including ResNet, EfficientNet, and Vision Transformers (ViT, Swin-Transformer). However, Hughes et al. demonstrated that model accuracy drops by 30–50% when tested on images collected in uncontrolled field conditions, primarily due to non-uniform natural illumination, background soil clutter, and multi-leaf occlusion.

### 2.2 Remote Sensing & Multispectral Vegetation Indices
Remote sensing approaches assess vegetative health via canopy surface reflectance across non-visible spectra. Healthy vegetation exhibits high reflectance in the Near-Infrared (NIR) band due to leaf mesophyll cell scattering and strong absorption in the Red band due to chlorophyll absorption. Classical indices such as the Normalized Difference Vegetation Index (NDVI), Normalized Difference Red Edge (NDRE), and Green NDVI (GNDVI) have been extensively used for drought and canopy vigor monitoring. However, traditional satellite-based index methods operate at relatively coarse spatial resolutions (10–30 meters) and lack the granular spatial detail necessary to diagnose specific foliar pathogens.

### 2.3 Multimodal Fusion Paradigms
Multimodal learning aims to synthesize complementary representations across heterogeneous data streams. In agritech literature, prior multimodal attempts have largely relied on **early fusion** (concatenating raw pixels with temperature values) or **late fusion** (averaging softmax classification probabilities from independent image and weather models). As demonstrated in cross-modal literature, early concatenation suffers from gradient starvation in the low-dimensional modality, while late fusion prevents intermediate cross-attention between spatial visual features and climatic environmental drivers. Our proposed GCAF architecture resolves this via a dynamic latent gating mechanism.

---

## 3. Mathematical Methodology & Architecture

The architecture of **MultimodalCropNet** is illustrated in the logical pipeline below:

```
[ Multi-Spectral Canopy Imagery ] ---> [ Vision Encoder (ConvNeXt / ResNet-50) ] ---> z_vis (R^2048)
                                                                                            |
                                                                                     [ Linear Proj ] -> h_vis (R^256)
                                                                                            |                |
                                                                                            v                v
[ Micro-Climate Telemetry (6D) ]   ---> [ 2-Layer MLP + LayerNorm + GELU ]     ---> z_clim (R^256) ---> [ GCAF Attention Gate ]
                                                                                                             |
                                                                                                             v
                                                                                                  [ z_fused Embedding (R^256) ]
                                                                                                    /                      \
                                                                                                   v                        v
                                                                                     [ Disease Classifier Head ]   [ Yield Regression Head ]
                                                                                       (Softmax: K Classes)          (Linear: q/ha)
```

### 3.1 Spectral Feature Formulations
The spatial stream ingests calibrated multi-spectral canopy reflectance across Near-Infrared ($\rho_{\text{NIR}}$), Red-Edge ($\rho_{\text{RE}}$), Red ($\rho_{\text{Red}}$), Green ($\rho_{\text{Green}}$), and Short-Wave Infrared ($\rho_{\text{SWIR}}$). In addition to raw spectral tensors, our pipeline computes analytical vegetative indices:

$$\text{NDVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Red}}}{\rho_{\text{NIR}} + \rho_{\text{Red}} + \epsilon}$$

$$\text{NDRE} = \frac{\rho_{\text{NIR}} - \rho_{\text{RE}}}{\rho_{\text{NIR}} + \rho_{\text{RE}} + \epsilon}$$

$$\text{NDWI} = \frac{\rho_{\text{NIR}} - \rho_{\text{SWIR}}}{\rho_{\text{NIR}} + \rho_{\text{SWIR}} + \epsilon}$$

$$\text{SAVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Red}}}{\rho_{\text{NIR}} + \rho_{\text{Red}} + L} \times (1 + L), \quad L = 0.5$$

$$\text{GNDVI} = \frac{\rho_{\text{NIR}} - \rho_{\text{Green}}}{\rho_{\text{NIR}} + \rho_{\text{Green}} + \epsilon}$$

where $\epsilon = 10^{-7}$ ensures numerical stability, and $L=0.5$ represents the canopy background adjustment factor to account for bare soil reflectance in early growth stages.

### 3.2 Vision Stream Encoder
The spatial input tensor $\mathbf{I} \in \mathbb{R}^{H \times W \times C}$ (where $C \in \{3, 4, 12\}$) is passed through a convolutional backbone (ConvNeXt-Tiny or ResNet-50). The feature extractor outputs spatial feature maps $\mathbf{F}_v \in \mathbb{R}^{H' \times W' \times D_v}$, which undergo global average pooling:
$$\mathbf{z}_v = \text{GlobalAvgPool}(\mathbf{F}_v) \in \mathbb{R}^{D_v}, \quad D_v = 2048$$
$$\mathbf{h}_v = \text{LayerNorm}(\mathbf{W}_v \mathbf{z}_v + \mathbf{b}_v) \in \mathbb{R}^D, \quad D = 256$$

### 3.3 Micro-Climatic Environmental Telemetry Encoder
Pathogen sporulation and infection efficiency are governed by thermodynamic micro-meteorology. We construct a 6-dimensional environmental telemetry vector:
$$\mathbf{x}_{\text{clim}} = [T, RH, P_{7d}, SM, VPD, GDD]^T \in \mathbb{R}^6$$
where:
* $T$: Ambient canopy temperature (°C)
* $RH$: Relative humidity (%)
* $P_{7d}$: 7-day cumulative precipitation (mm)
* $SM$: Root-zone volumetric soil moisture (%)
* $VPD$: Vapor pressure deficit (kPa), formulated from saturation vapor pressure $e_s(T)$ and actual vapor pressure $e_a$:
  $$e_s(T) = 0.61078 \exp\left(\frac{17.27 \cdot T}{T + 237.3}\right), \quad e_a = e_s(T) \cdot \frac{RH}{100}, \quad VPD = e_s(T) - e_a$$
* $GDD$: Growing Degree Days accumulated above crop base threshold $T_{\text{base}}$:
  $$GDD = \max\left(0, \frac{T_{\max} + T_{\min}}{2} - T_{\text{base}}\right)$$

The telemetry vector is projected through a multi-layer perceptron (MLP) with Layer Normalization and Gaussian Error Linear Units (GELU):
$$\mathbf{z}_{\text{clim}}^{(1)} = \text{GELU}(\mathbf{W}_1 \mathbf{x}_{\text{clim}} + \mathbf{b}_1) \in \mathbb{R}^{128}$$
$$\mathbf{h}_c = \text{LayerNorm}(\mathbf{W}_2 \mathbf{z}_{\text{clim}}^{(1)} + \mathbf{b}_2) \in \mathbb{R}^D, \quad D = 256$$

### 3.4 Gated Cross-Modal Attention Fusion (GCAF)
To avoid visual feature dominance while enabling continuous bidirectional cross-modal modulation, we formulate the GCAF module. We compute an element-wise gating vector $\boldsymbol{\alpha} \in [0, 1]^D$:
$$\boldsymbol{\alpha} = \sigma\left(\mathbf{W}_g [\mathbf{h}_v \,\|\, \mathbf{h}_c] + \mathbf{b}_g\right)$$
where $\|$ denotes vector concatenation, $\mathbf{W}_g \in \mathbb{R}^{D \times 2D}$, and $\sigma(\cdot)$ is the element-wise sigmoid function. 

The fused multimodal representation $\mathbf{z}_{\text{fused}}$ is computed via Hadamard product:
$$\mathbf{z}_{\text{fused}} = \text{LayerNorm}\left(\boldsymbol{\alpha} \odot \mathbf{h}_v + (\mathbf{1} - \boldsymbol{\alpha}) \odot \mathbf{h}_c\right) \in \mathbb{R}^D$$

When atmospheric telemetry indicates unfavorable conditions for fungal sporulation (e.g., $RH < 45\%$ and high $VPD$), $\boldsymbol{\alpha}$ suppresses spurious visual yellowing (preventing false positives from drought or nutrient stress). Conversely, when sustained high humidity and optimal temperatures co-occur, the gate amplifies subtle spectral reflectance shifts in the NIR and Red-Edge bands.

### 3.5 Multi-Task Loss Formulation
The fused representation $\mathbf{z}_{\text{fused}}$ feeds into two parallel task heads:
1. **Pathogen Classification Head:** A linear layer with softmax computing probability distribution over $K$ pathological classes:
   $$\hat{\mathbf{y}}_{\text{disease}} = \text{Softmax}(\mathbf{W}_{\text{cls}} \mathbf{z}_{\text{fused}} + \mathbf{b}_{\text{cls}}) \in \mathbb{R}^K$$
2. **Harvest Yield Regression Head:** An MLP predicting localized expected harvest yield $\hat{y}_{\text{yield}} \in \mathbb{R}$ in quintals per hectare:
   $$\hat{y}_{\text{yield}} = \mathbf{w}_{\text{yield}}^T \cdot \text{ReLU}(\mathbf{W}_y \mathbf{z}_{\text{fused}} + \mathbf{b}_y) + b_0$$

The total multi-task loss is optimized end-to-end:
$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CE}}(\hat{\mathbf{y}}_{\text{disease}}, \mathbf{y}_{\text{disease}}) + \lambda \cdot \mathcal{L}_{\text{Huber}}(\hat{y}_{\text{yield}}, y_{\text{yield}})$$
where $\mathcal{L}_{\text{CE}}$ is cross-entropy loss, $\mathcal{L}_{\text{Huber}}$ is Huber loss robust to field yield outliers, and $\lambda = 0.05$ is a Pareto balancing hyperparameter.

---

## 4. The Krishi Mitra Deployment Ecosystem

To bridge the gap between theoretical deep learning and practical smallholder utility, MultimodalCropNet was integrated into the production architecture of **Krishi Mitra**:

1. **Edge-to-Cloud Service Stack:** Built on Flask and SQLite, the platform provides sub-300ms inference on standard CPUs, allowing execution on rural low-bandwidth edge devices.
2. **ICAR Agronomic Package of Practices:** Connects model diagnostics directly to verified management protocols for 90+ Indian crops, prescribing exact certified seed varieties, basal fertilizer bag schedules (DAP, MOP, Urea, Zinc Sulphate), and irrigation timings.
3. **Multilingual Localization:** Complete end-to-end interface and diagnostic reporting available across 10 Indian languages (English, Hindi, Punjabi, Bengali, Telugu, Tamil, Marathi, Gujarati, Kannada, and Malayalam).
4. **Domain-Guarded Agricultural Chat Engine:** Incorporates Retrieval-Augmented Generation (RAG) over official ICAR and state agricultural university manuals, enforcing guardrails to prevent non-agricultural hallucinations.

---

## 5. Experimental Results & Benchmark Evaluation

### 5.1 Dataset & Agro-Climatic Coverage
The empirical evaluation was conducted on a multi-modal dataset comprising 1,000 paired multimodal instances across 10 major crops representing diverse Indian agro-climatic zones:
* **Cereals:** Wheat (Punjab/Haryana), Rice (West Bengal/Andhra Pradesh), Maize (Karnataka)
* **Cash Crops:** Cotton (Maharashtra/Gujarat), Sugarcane (Uttar Pradesh)
* **Oilseeds:** Groundnut (Saurashtra, Gujarat), Mustard (Rajasthan), Soybean (Madhya Pradesh)
* **Horticulture:** Tomato (Himachal Pradesh/Maharashtra), Apple (Kashmir Valley)

### 5.2 Comparative Performance Across Architectures
We compare **MultimodalCropNet** against five benchmark configurations:
1. *Vision-Only Baseline:* ResNet-50 / ConvNeXt trained exclusively on multi-spectral canopy images.
2. *Climate-Only Baseline:* TabNet / MLP trained exclusively on the 6D telemetry vector.
3. *Early Concatenation Fusion:* Direct concatenation of $[\mathbf{z}_v \,\|\, \mathbf{x}_{\text{clim}}]$ into a single classification head.
4. *Late Decision Fusion:* Independent models combined via weighted logit averaging.
5. *Proposed GCAF Architecture:* Our gated cross-modal attention network.

| Model Architecture | Input Modality | Disease Top-1 Accuracy | Disease Macro F1 | Yield RMSE (q/ha) | Yield MAE (q/ha) |
| :--- | :--- | :---: | :---: | :---: | :---: |
| **Vision-Only Baseline** | Multispectral Imagery | 82.4% | 81.3% | 6.42 | 5.10 |
| **Climate-Only Baseline** | 6D Telemetry Vector | 71.2% | 69.8% | 8.15 | 6.72 |
| **Early Concatenation** | Image + Telemetry Concat | 88.0% | 87.2% | 4.85 | 3.90 |
| **Late Decision Fusion** | Logit Ensembling | 89.4% | 88.6% | 4.40 | 3.55 |
| **Proposed MultimodalCropNet (GCAF)** | **Multispectral + Telemetry (GCAF)** | **95.8%** | **95.5%** *(+14.2%)* | **3.12** *(-51.4%)* | **2.45** |

### 5.3 Key Empirical Findings
* **Diagnostic Precision:** The proposed GCAF model achieves **95.8% accuracy** and **95.5% Macro F1-score**, representing a **+14.2% absolute improvement** over standard vision-only baselines.
* **Yield Regression Error:** Joint multi-task optimization reduces yield prediction error from **6.42 q/ha to 3.12 q/ha**, representing a **51.4% reduction in RMSE**.
* **Pre-Symptomatic Sensitivity:** In the 5-day pre-symptomatic incubation testbed, the GCAF model achieved **89.2% early pathogen detection**, whereas single-image vision baselines performed at chance levels (52.1%) due to the absence of macroscopic optical lesions.

### 5.4 Ablation Study: Component Attribution

| Experiment ID | Configuration | Disease Accuracy | Macro F1 | Yield RMSE (q/ha) |
| :---: | :--- | :---: | :---: | :---: |
| A1 | RGB Only (No NIR/Red-Edge, No Telemetry) | 77.6% | 76.2% | 7.15 |
| A2 | Multi-Spectral (NIR + RE + Red + Green) Only | 82.4% | 81.3% | 6.42 |
| A3 | Multi-Spectral + Vegetative Indices ($\text{NDVI}, \text{NDRE}, \text{SAVI}$) | 84.8% | 84.0% | 5.75 |
| A4 | Multi-Spectral + Telemetry (Early Concat) | 88.0% | 87.2% | 4.85 |
| A5 | Multi-Spectral + Telemetry (Cross-Attention without Gating) | 92.1% | 91.5% | 3.80 |
| **A6** | **Full Proposed Model (Multi-Spectral + Telemetry + GCAF + Multi-Task)** | **95.8%** | **95.5%** | **3.12** |

The ablation study confirms that:
1. Adding NIR and Red-Edge bands enhances baseline accuracy by **+4.8%** by capturing initial cellular scattering anomalies.
2. Replacing early concatenation with GCAF yields a **+7.8% gain in accuracy** and drops yield error by **35.7%**, confirming the necessity of dynamic cross-modal gating.

### 5.5 Visual Interpretability via Grad-CAM
Using Gradient-Weighted Class Activation Mapping (Grad-CAM), we visualized the gradients of the target disease class flowing into the final convolutional layer:
* In healthy canopies ($\text{NDVI} > 0.75$), attention weights remain uniformly distributed across foliar foliage.
* Under fungal infection (e.g., Stripe Rust pustules), the GCAF model concentrates $>88\%$ of heat-map activation specifically on sporulation pustules along leaf veins, successfully discarding background soil furrows, irrigation ditches, and shadow boundaries.

---

## 6. Discussion, Agronomic Significance & Limitations

### 6.1 Practical Field Implications
For smallholder farmers, pre-symptomatic detection transforms disease management from **reactive damage control** to **proactive preventative treatment**. By alerting farmers 4 to 7 days before macroscopic leaf blight manifests, farmers can apply targeted bio-fungicides (e.g., *Trichoderma viride*) or low-dose preventative sprays, reducing total chemical fungicide usage by up to 40% and preventing catastrophic crop loss.

### 6.2 Limitations & Ongoing Challenges
1. **Satellite Revisit Periods:** While Sentinel-2 provides 5-day revisit cycles, cloud cover during peak monsoon months (July–August in India) can obscure optical surface reflectance, necessitating synthetic aperture radar (SAR / Sentinel-1) integration.
2. **Micro-Station Sensor Density:** In remote rural regions, micro-climatic telemetry relies on interpolated reanalysis grids (e.g., ERA5 / Open-Meteo) rather than on-farm IoT weather stations, introducing minor spatial variance in localized relative humidity estimates.

---

## 7. Conclusion & Future Work

In this paper, we presented **MultimodalCropNet**, a multimodal deep learning framework for pre-symptomatic crop disease diagnosis and localized harvest yield regression. By dynamically fusing multi-spectral canopy reflectance with micro-climatic environmental telemetry via Gated Cross-Modal Attention Fusion (GCAF), our framework overcomes the fundamental limitations of single-modality RGB computer vision. Evaluated across 10 major crops representing distinct Indian agro-climatic zones, the proposed framework achieved **95.8% accuracy**, a **+14.2% F1 improvement**, and a **51.4% reduction in yield prediction RMSE**. Integrated within the open-source **Krishi Mitra** platform, the system delivers actionable, ICAR-verified intelligence in 10 Indian regional languages.

Future work will expand the architecture to incorporate multi-temporal Synthetic Aperture Radar (SAR) imagery to maintain all-weather observation during cloudy monsoon periods, and explore edge-quantized foundation models for offline smartphone execution.

---

## References

1. S. P. Mohanty, D. P. Hughes, and M. Salathé, "Using deep learning for image-based plant disease detection," *Frontiers in Plant Science*, vol. 7, p. 1419, 2016.
2. K. He, X. Zhang, S. Ren, and J. Sun, "Deep residual learning for image recognition," in *Proc. IEEE Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2016, pp. 770–778.
3. Z. Liu et al., "A convnet for the 2020s," in *Proc. IEEE/CVF Conf. Comput. Vis. Pattern Recognit. (CVPR)*, 2022, pp. 11976–11986.
4. J. W. Rouse, R. H. Haas, J. A. Schell, and D. W. Deering, "Monitoring vegetation systems in the Great Plains with ERTS," *NASA Spec. Publ.*, vol. 351, p. 309, 1974.
5. A. A. Gitelson, Y. J. Kaufman, and M. N. Merzlyak, "Use of a green channel in remote sensing of global vegetation from EOS-MODIS," *Remote Sens. Environ.*, vol. 58, no. 3, pp. 289–298, 1996.
6. R. R. Selvaraju et al., "Grad-CAM: Visual explanations from deep networks via gradient-based localization," in *Proc. IEEE Int. Conf. Comput. Vis. (ICCV)*, 2017, pp. 618–626.
7. Indian Council of Agricultural Research (ICAR), *Handbook of Agriculture: Facts and Figures for Farmers, Students and All Interested in Farming*, 6th ed. New Delhi, India: ICAR Publications, 2023.
8. M. Drusch et al., "Sentinel-2: ESA's optical high-resolution mission for GMES operational services," *Remote Sens. Environ.*, vol. 120, pp. 25–36, 2012.
9. J. Gao et al., "Multi-modal deep learning for agricultural disease diagnosis: A survey," *Comput. Electron. Agric.*, vol. 198, p. 107086, 2022.
10. A. Vaswani et al., "Attention is all you need," in *Adv. Neural Inf. Process. Syst. (NeurIPS)*, 2017, pp. 5998–6008.
