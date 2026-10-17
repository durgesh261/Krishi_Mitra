"""
5-Crop All-India Regional Benchmark: Healthy vs. Diseased Comparison
Region-wise Popular Crops (ICAR Zones):
1. North India: Wheat (Punjab / Haryana)
2. South & East India: Rice / Paddy (Andhra Pradesh / West Bengal)
3. Central & West India: Cotton (Maharashtra / Gujarat)
4. West India: Groundnut (Gujarat / Saurashtra)
5. Central & South India: Maize (Karnataka / Madhya Pradesh)

Runs full Multimodal Inference + Grad-CAM Heatmap Generation + Single-Leaf Diagnostics
Produces side-by-side comparative analytics for all 10 samples.
"""

import os
import sys
import json
import base64
import shutil
import numpy as np
from PIL import Image

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from multimodal_remote_sensing import (
    predict_multimodal_disease_and_yield,
    CROP_YIELD_BASELINES
)
from chat2 import analyze_crop_disease

# Output directories
BENCHMARK_DIR = os.path.join("experiment_data", "5_crop_benchmark")
RESULTS_DIR = os.path.join(BENCHMARK_DIR, "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

ART_DIR = r"C:\Users\durge\.gemini\antigravity-ide\brain\ca070edd-896e-4030-bf74-fa219df28898"

# 1. Map source images to canonical benchmark paths
source_mapping = {
    # Crop 1: Wheat
    "wheat_healthy": os.path.join(ART_DIR, "wheat_healthy_leaf_1792250465237.jpg"),
    "wheat_diseased": os.path.join("experiment_data", "wheat_stripe_rust_real.jpg"),

    # Crop 2: Rice
    "rice_healthy": os.path.join(ART_DIR, "rice_healthy_leaf_1792250488945.jpg"),
    "rice_diseased": os.path.join(ART_DIR, "rice_blast_leaf_1792250526109.jpg"),

    # Crop 3: Cotton
    "cotton_healthy": os.path.join(ART_DIR, "cotton_healthy_leaf_1792250555068.jpg"),
    "cotton_diseased": os.path.join(ART_DIR, "cotton_blight_leaf_1792250597220.jpg"),

    # Crop 4: Groundnut
    "groundnut_healthy": os.path.join(ART_DIR, "groundnut_healthy_leaf_1792250628752.jpg"),
    "groundnut_diseased": os.path.join("experiment_data", "groundnut_leaf_spot_real.jpg"),

    # Crop 5: Maize
    "maize_healthy": os.path.join(ART_DIR, "maize_healthy_leaf_1792250661163.jpg"),
    "maize_diseased": os.path.join(ART_DIR, "maize_blight_leaf_1792250694169.jpg"),
}

# Verify and copy into benchmark folder
for key, src_path in source_mapping.items():
    assert os.path.exists(src_path), f"Missing source image: {src_path}"
    dest_path = os.path.join(BENCHMARK_DIR, f"{key}.jpg")
    shutil.copy(src_path, dest_path)
    # Also copy to artifacts directory for markdown embedding
    shutil.copy(src_path, os.path.join(ART_DIR, f"{key}.jpg"))
    print(f"[OK] Staged {key}.jpg ({os.path.getsize(dest_path)} bytes)")

# Telemetry profiles per crop (Healthy vs Diseased micro-climate context)
crop_telemetry = {
    "wheat": {
        "crop_key": "wheat",
        "display_name": "Wheat (गेहूँ)",
        "region": "North India (Punjab / Haryana / UP)",
        "healthy_env": {"temp": 20.0, "rh": 58.0, "rainfall_7d": 10.0, "soil_moisture": 55.0, "vpd": 1.2},
        "diseased_env": {"temp": 17.5, "rh": 86.0, "rainfall_7d": 35.0, "soil_moisture": 72.0, "vpd": 0.65}
    },
    "rice": {
        "crop_key": "rice",
        "display_name": "Rice / Paddy (धान)",
        "region": "South & East India (West Bengal / Andhra Pradesh / Cauvery)",
        "healthy_env": {"temp": 28.0, "rh": 72.0, "rainfall_7d": 40.0, "soil_moisture": 80.0, "vpd": 1.1},
        "diseased_env": {"temp": 26.5, "rh": 92.0, "rainfall_7d": 75.0, "soil_moisture": 90.0, "vpd": 0.35}
    },
    "cotton": {
        "crop_key": "cotton",
        "display_name": "Cotton (कपास)",
        "region": "Central & West India (Maharashtra / Gujarat / Telangana)",
        "healthy_env": {"temp": 30.0, "rh": 62.0, "rainfall_7d": 20.0, "soil_moisture": 50.0, "vpd": 1.6},
        "diseased_env": {"temp": 32.0, "rh": 84.0, "rainfall_7d": 55.0, "soil_moisture": 78.0, "vpd": 0.8}
    },
    "groundnut": {
        "crop_key": "groundnut",
        "display_name": "Groundnut / Peanut (मूंगफली)",
        "region": "West India (Gujarat / Saurashtra / Rajasthan)",
        "healthy_env": {"temp": 28.5, "rh": 65.0, "rainfall_7d": 15.0, "soil_moisture": 45.0, "vpd": 1.4},
        "diseased_env": {"temp": 27.5, "rh": 93.0, "rainfall_7d": 45.0, "soil_moisture": 75.0, "vpd": 0.3}
    },
    "maize": {
        "crop_key": "maize",
        "display_name": "Maize / Corn (मक्का)",
        "region": "Central & South India (Karnataka / MP / Bihar)",
        "healthy_env": {"temp": 26.0, "rh": 64.0, "rainfall_7d": 25.0, "soil_moisture": 58.0, "vpd": 1.3},
        "diseased_env": {"temp": 24.5, "rh": 88.0, "rainfall_7d": 60.0, "soil_moisture": 80.0, "vpd": 0.5}
    }
}

benchmark_results = {}

print("\n" + "=" * 90)
print("EXECUTING MULTIMODAL INFERENCE ON 5 HEALTHY VS 5 DISEASED PAIRS")
print("=" * 90)

for crop_id, meta in crop_telemetry.items():
    print(f"\n>>> PROCESSING CROP: {meta['display_name']} [{meta['region']}]")
    crop_res = {"meta": meta, "healthy": {}, "diseased": {}}

    # --- 1. HEALTHY SAMPLE ---
    h_img_path = os.path.join(BENCHMARK_DIR, f"{crop_id}_healthy.jpg")
    with open(h_img_path, "rb") as f:
        h_bytes = f.read()

    h_env = meta["healthy_env"]
    res_h = predict_multimodal_disease_and_yield(
        image_bytes=h_bytes,
        crop_name=meta["crop_key"],
        temperature=h_env["temp"],
        humidity=h_env["rh"],
        rainfall_7d=h_env["rainfall_7d"],
        soil_moisture=h_env["soil_moisture"],
        vpd=h_env["vpd"],
        canopy_source="Sentinel-2 MSI (10m Resolution)"
    )

    # Save Grad-CAM heatmap
    if res_h.get("gradcam_image") and "," in res_h["gradcam_image"]:
        b64_data = res_h["gradcam_image"].split(",", 1)[1]
        gradcam_bytes = base64.b64decode(b64_data)
        h_grad_path = os.path.join(RESULTS_DIR, f"{crop_id}_healthy_gradcam.jpg")
        with open(h_grad_path, "wb") as f:
            f.write(gradcam_bytes)
        shutil.copy(h_grad_path, os.path.join(ART_DIR, f"{crop_id}_healthy_gradcam.jpg"))

    # Single leaf vision analysis
    h_b64 = base64.b64encode(h_bytes).decode("utf-8")
    single_diag_h = analyze_crop_disease(h_b64, mime_type="image/jpeg")

    crop_res["healthy"] = {
        "diagnosis": res_h["diagnosis"]["name"],
        "severity": res_h["diagnosis"]["severity"],
        "confidence": res_h["diagnosis"]["confidence"],
        "ndvi": res_h["spectral_indices"]["ndvi"],
        "ndwi": res_h["spectral_indices"]["ndwi"],
        "canopy_status": res_h["spectral_indices"]["canopy_health"],
        "yield_forecast": res_h["yield_forecast"]["estimated_yield_q_ha"],
        "baseline_yield": res_h["yield_forecast"]["district_baseline_q_ha"],
        "delta_pct": res_h["yield_forecast"]["delta_pct"],
        "chemical_rx": res_h["diagnosis"]["recommended_chemical"],
        "organic_rx": res_h["diagnosis"]["recommended_organic"],
        "single_leaf_summary": single_diag_h[:280]
    }

    # --- 2. DISEASED SAMPLE ---
    d_img_path = os.path.join(BENCHMARK_DIR, f"{crop_id}_diseased.jpg")
    with open(d_img_path, "rb") as f:
        d_bytes = f.read()

    d_env = meta["diseased_env"]
    res_d = predict_multimodal_disease_and_yield(
        image_bytes=d_bytes,
        crop_name=meta["crop_key"],
        temperature=d_env["temp"],
        humidity=d_env["rh"],
        rainfall_7d=d_env["rainfall_7d"],
        soil_moisture=d_env["soil_moisture"],
        vpd=d_env["vpd"],
        canopy_source="Sentinel-2 MSI (10m Resolution)"
    )

    # Save Grad-CAM heatmap
    if res_d.get("gradcam_image") and "," in res_d["gradcam_image"]:
        b64_data = res_d["gradcam_image"].split(",", 1)[1]
        gradcam_bytes = base64.b64decode(b64_data)
        d_grad_path = os.path.join(RESULTS_DIR, f"{crop_id}_diseased_gradcam.jpg")
        with open(d_grad_path, "wb") as f:
            f.write(gradcam_bytes)
        shutil.copy(d_grad_path, os.path.join(ART_DIR, f"{crop_id}_diseased_gradcam.jpg"))

    # Single leaf vision analysis
    d_b64 = base64.b64encode(d_bytes).decode("utf-8")
    single_diag_d = analyze_crop_disease(d_b64, mime_type="image/jpeg")

    crop_res["diseased"] = {
        "diagnosis": res_d["diagnosis"]["name"],
        "severity": res_d["diagnosis"]["severity"],
        "confidence": res_d["diagnosis"]["confidence"],
        "ndvi": res_d["spectral_indices"]["ndvi"],
        "ndwi": res_d["spectral_indices"]["ndwi"],
        "canopy_status": res_d["spectral_indices"]["canopy_health"],
        "yield_forecast": res_d["yield_forecast"]["estimated_yield_q_ha"],
        "baseline_yield": res_d["yield_forecast"]["district_baseline_q_ha"],
        "delta_pct": res_d["yield_forecast"]["delta_pct"],
        "chemical_rx": res_d["diagnosis"]["recommended_chemical"],
        "organic_rx": res_d["diagnosis"]["recommended_organic"],
        "single_leaf_summary": single_diag_d[:280]
    }

    benchmark_results[crop_id] = crop_res

    print(f"  [Healthy]  -> Diagnosis: {crop_res['healthy']['diagnosis']} | NDVI: {crop_res['healthy']['ndvi']} | Yield: {crop_res['healthy']['yield_forecast']} q/ha ({crop_res['healthy']['delta_pct']}%)")
    print(f"  [Diseased] -> Diagnosis: {crop_res['diseased']['diagnosis']} ({crop_res['diseased']['confidence']}%) | NDVI: {crop_res['diseased']['ndvi']} | Yield: {crop_res['diseased']['yield_forecast']} q/ha ({crop_res['diseased']['delta_pct']}%)")

# Save complete benchmark results
out_json = os.path.join(RESULTS_DIR, "benchmark_5_crops_results.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(benchmark_results, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 90)
print(f"[SUCCESS] 5-Crop Benchmark Completed. Report saved to: {out_json}")
print("=" * 90)
