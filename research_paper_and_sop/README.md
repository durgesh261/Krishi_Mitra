# 📚 Academic Research Paper, SOP Dossier & Technical Portfolio

This directory contains the **academic research paper**, **Statement of Purpose (SOP) narrative**, **Curriculum Vitae (CV) technical formulation**, and **empirical ablation benchmarks** for the Multi-Spectral Remote Sensing & Crop Disease/Yield Prediction system of Krishi Mitra.

> **Note**: As per research integrity and clean web design standards, all research dossiers and academic whitepapers are housed here in this dedicated repository archive rather than on public end-user farming interface pages.

---

## 📂 Directory Contents

1. [`RESEARCH_WHITEPAPER_MULTIMODAL_AGRICULTURE.md`](RESEARCH_WHITEPAPER_MULTIMODAL_AGRICULTURE.md)
   * **Full IEEE / ACM Format Research Paper**
   * Abstract, Introduction, Problem Formulation, Multi-Spectral Remote Sensing (Sentinel-2 & Drone), Early vs. Late vs. Cross-Modal Gated Attention Fusion.
   * Mathematical Equations: NDVI, NDWI, SAVI, GNDVI, Gated Cross-Attention Matrix, Joint Multi-Task Pareto Loss, Grad-CAM Heatmap Derivations.
   * Empirical Ablation Benchmark Across 1,000 Multi-Spectral Crop Instances.

2. [`STATEMENT_OF_PURPOSE_AND_CV_PORTFOLIO.md`](STATEMENT_OF_PURPOSE_AND_CV_PORTFOLIO.md)
   * **CV Bullet Points**: Quantified resume impact lines (+14.2% F1 score, -51.4% yield RMSE).
   * **Statement of Purpose (SOP) Pitch**: High-impact narrative for M.S. / Ph.D. applications in Computer Vision, Data Science, and Remote Sensing.
   * **Interview Talking Points & Defense Q&A**: Why multimodal fusion outperforms single-modality vision, how cloud cover and spatial resolution constraints are mitigated, and real-world deployment on mobile edge devices.

3. [`../research/`](../research/)
   * PyTorch model architectures (`models/multimodal_net.py`).
   * Synthetic & Sentinel-2 dataset generators (`dataset/multimodal_loader.py`).
   * Training and ablation evaluation scripts (`train.py`, `ablation_study.py`).
