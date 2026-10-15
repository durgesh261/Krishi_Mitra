import io
import os
import sys
import json
import base64
from PIL import Image
from multimodal_remote_sensing import predict_multimodal_disease_and_yield

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

os.makedirs('experiment_data/results', exist_ok=True)

# Experiment 1: Wheat Stripe Rust
print("=" * 70)
print("EXPERIMENT 1: REAL WHEAT LEAF WITH STRIPE RUST (Puccinia striiformis)")
print("=" * 70)

with open('experiment_data/wheat_stripe_rust_real.jpg', 'rb') as f:
    wheat_bytes = f.read()

# Environmental telemetry matching Punjab/Haryana late winter (optimal incubation for stripe rust)
wheat_telemetry = {
    "crop_name": "wheat",
    "temperature": 19.5,      # Favorable rust incubation (15-22°C)
    "humidity": 84.0,         # High relative humidity triggering spore germination
    "rainfall_7d": 38.0,      # Wetting event
    "soil_moisture": 70.0,
    "vpd": 0.8,
    "canopy_source": "Sentinel-2 MSI (10m Resolution)"
}

res_wheat = predict_multimodal_disease_and_yield(
    image_bytes=wheat_bytes,
    **wheat_telemetry
)

# Save Grad-CAM heatmap for Wheat
if res_wheat.get('gradcam_image'):
    b64_data = res_wheat['gradcam_image'].split(',', 1)[1]
    with open('experiment_data/results/wheat_gradcam_overlay.jpg', 'wb') as f:
        f.write(base64.b64decode(b64_data))
    print("Saved Wheat Grad-CAM Attention Heatmap to experiment_data/results/wheat_gradcam_overlay.jpg")

print(f"Crop: {res_wheat['crop']} ({res_wheat['crop_category']}/{res_wheat['crop_sub_category']})")
print(f"NDVI: {res_wheat['spectral_indices']['ndvi']} | NDWI: {res_wheat['spectral_indices']['ndwi']} | Status: {res_wheat['spectral_indices']['canopy_health']}")
print(f"Diagnosed Class: {res_wheat['diagnosis']['name']} (Confidence: {res_wheat['diagnosis']['confidence']}%)")
print(f"Severity: {res_wheat['diagnosis']['severity']}")
print(f"Chemical Spray: {res_wheat['diagnosis']['recommended_chemical']}")
print(f"Organic Control: {res_wheat['diagnosis']['recommended_organic']}")
print(f"ICAR Specific Advisory: {res_wheat['diagnosis']['crop_specific_advisory']}")
print(f"Yield Forecast: {res_wheat['yield_forecast']['estimated_yield_q_ha']} q/ha vs Baseline {res_wheat['yield_forecast']['district_baseline_q_ha']} q/ha ({res_wheat['yield_forecast']['delta_pct']}%)")


# Experiment 2: Groundnut Leaf Spot / Tikka Blight
print("\n" + "=" * 70)
print("EXPERIMENT 2: REAL GROUNDNUT LEAF WITH TIKKA SPOT (Cercospora arachidicola)")
print("=" * 70)

with open('experiment_data/groundnut_leaf_spot_real.jpg', 'rb') as f:
    gn_bytes = f.read()

# Environmental telemetry matching Gujarat/Andhra Pradesh Kharif groundnut belt
gn_telemetry = {
    "crop_name": "groundnut",
    "temperature": 28.0,      # Warm humid tropical weather (25-32°C)
    "humidity": 82.0,         # High relative humidity (>80% needed for Cercospora spore germination)
    "rainfall_7d": 32.0,      # Intermittent rain / leaf wetting
    "soil_moisture": 64.0,
    "vpd": 1.1,
    "canopy_source": "DJI Agras Drone Multispectral (GSD 2.5cm)"
}

res_gn = predict_multimodal_disease_and_yield(
    image_bytes=gn_bytes,
    **gn_telemetry
)

# Save Grad-CAM heatmap for Groundnut
if res_gn.get('gradcam_image'):
    b64_data = res_gn['gradcam_image'].split(',', 1)[1]
    with open('experiment_data/results/groundnut_gradcam_overlay.jpg', 'wb') as f:
        f.write(base64.b64decode(b64_data))
    print("Saved Groundnut Grad-CAM Attention Heatmap to experiment_data/results/groundnut_gradcam_overlay.jpg")

print(f"Crop: {res_gn['crop']} ({res_gn['crop_category']}/{res_gn['crop_sub_category']})")
print(f"NDVI: {res_gn['spectral_indices']['ndvi']} | NDWI: {res_gn['spectral_indices']['ndwi']} | Status: {res_gn['spectral_indices']['canopy_health']}")
print(f"Diagnosed Class: {res_gn['diagnosis']['name']} (Confidence: {res_gn['diagnosis']['confidence']}%)")
print(f"Severity: {res_gn['diagnosis']['severity']}")
print(f"Chemical Spray: {res_gn['diagnosis']['recommended_chemical']}")
print(f"Organic Control: {res_gn['diagnosis']['recommended_organic']}")
print(f"ICAR Specific Advisory: {res_gn['diagnosis']['crop_specific_advisory']}")
print(f"Yield Forecast: {res_gn['yield_forecast']['estimated_yield_q_ha']} q/ha vs Baseline {res_gn['yield_forecast']['district_baseline_q_ha']} q/ha ({res_gn['yield_forecast']['delta_pct']}%)")

# Save detailed JSON summary for report
experiment_summary = {
    "wheat_experiment": res_wheat,
    "groundnut_experiment": res_gn
}
# Omit large base64 strings in json
for k in ["wheat_experiment", "groundnut_experiment"]:
    experiment_summary[k]["gradcam_image"] = "[BASE64_SAVED_AS_JPEG]"

with open('experiment_data/results/experiment_summary.json', 'w', encoding='utf-8') as f:
    json.dump(experiment_summary, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 70)
print("EXPERIMENT COMPLETED SUCCESSFULLY! Full results saved in experiment_data/results/")
print("=" * 70)
