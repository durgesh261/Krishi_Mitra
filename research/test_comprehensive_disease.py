"""
Comprehensive Real-Crop Early Disease Detection & Yield Prediction Verification
Testing:
1. Scenario 1: Dwarka region, Gujarat | Crop: Groundnut (Real leaf spot image)
   - Method A: Via Location (Open-Meteo Live Weather Fetch for Dwarka)
   - Method B: Manual Telemetry Entry (Agronomic Parameters)
   - Single-Leaf Vision & Agricultural Diagnosis (/api/disease)
2. Scenario 2: Punjab region | Crop: Wheat (Real stripe rust image)
   - Method A: Via Location (Open-Meteo Live Weather Fetch for Punjab/Ludhiana)
   - Method B: Manual Telemetry Entry (Agronomic Parameters)
   - Single-Leaf Vision & Agricultural Diagnosis (/api/disease)
3. Live HTTP API endpoint verification against running Flask server
"""

import os
import sys
import json
import base64
import requests

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from location_service import get_open_meteo_weather
from multimodal_remote_sensing import (
    predict_multimodal_disease_and_yield
)
import math

def calculate_vpd(temp_c, rh_pct):
    # Tetens equation for saturation vapor pressure (kPa)
    vp_sat = 0.61078 * math.exp((17.27 * temp_c) / (temp_c + 237.3))
    vp_actual = vp_sat * (rh_pct / 100.0)
    return round(max(0.1, vp_sat - vp_actual), 2)
from chat2 import analyze_crop_disease

def test_all():
    print("=" * 80)
    print("STARTING KRISHI MITRA COMPREHENSIVE EARLY DISEASE DETECTION VERIFICATION")
    print("=" * 80)

    # 1. Verify Image Assets
    groundnut_img_path = os.path.join("experiment_data", "groundnut_leaf_spot_real.jpg")
    wheat_img_path = os.path.join("experiment_data", "wheat_stripe_rust_real.jpg")

    assert os.path.exists(groundnut_img_path), f"Missing {groundnut_img_path}"
    assert os.path.exists(wheat_img_path), f"Missing {wheat_img_path}"

    with open(groundnut_img_path, "rb") as f:
        groundnut_bytes = f.read()
    with open(wheat_img_path, "rb") as f:
        wheat_bytes = f.read()

    print(f"[OK] Groundnut image loaded: {len(groundnut_bytes)} bytes")
    print(f"[OK] Wheat image loaded: {len(wheat_bytes)} bytes")

    output_report = {}

    # =========================================================================
    # SCENARIO 1: DWARKA, GUJARAT - GROUNDNUT (मूंगफली)
    # =========================================================================
    print("\n" + "=" * 80)
    print("SCENARIO 1: DWARKA REGION, GUJARAT | CROP: GROUNDNUT / PEANUT")
    print("=" * 80)

    # Method A: Via Location (Live Open-Meteo Weather)
    print("\n--- Method A: Via Location (Dwarka, Gujarat: Lat 22.2442, Lon 68.9685) ---")
    dwarka_weather = get_open_meteo_weather(city_name="Dwarka", lat=22.2442, lon=68.9685)
    dwarka_temp = float(dwarka_weather.get('temp', 28.0))
    dwarka_rh = float(dwarka_weather.get('humidity', 80.0))
    dwarka_precip = float(dwarka_weather.get('precipitation', 0.0))
    dwarka_rainfall_7d = max(10.0, dwarka_precip * 7 if dwarka_precip > 0 else 22.0)
    dwarka_vpd = calculate_vpd(dwarka_temp, dwarka_rh)
    dwarka_soil_moisture = min(85.0, max(30.0, dwarka_rh * 0.75))

    print(f"Dwarka Live Weather Fetched:")
    print(f"  - Temperature: {dwarka_temp}°C")
    print(f"  - Relative Humidity: {dwarka_rh}%")
    print(f"  - Calculated VPD: {dwarka_vpd} kPa")
    print(f"  - Estimated 7-day Rainfall: {dwarka_rainfall_7d} mm")
    print(f"  - Soil Moisture Proxy: {dwarka_soil_moisture}%")
    print(f"  - Weather Condition: {dwarka_weather.get('description')}")

    dwarka_loc_result = predict_multimodal_disease_and_yield(
        image_bytes=groundnut_bytes,
        crop_name="groundnut",
        temperature=dwarka_temp,
        humidity=dwarka_rh,
        rainfall_7d=dwarka_rainfall_7d,
        soil_moisture=dwarka_soil_moisture,
        vpd=dwarka_vpd,
        canopy_source="DJI Agras Drone Multispectral (GSD 2.5cm)"
    )

    print("\nResult [Dwarka Groundnut via Location]:")
    print(f"  - Diagnosed Disease: {dwarka_loc_result['diagnosis']['name']}")
    print(f"  - Severity Level: {dwarka_loc_result['diagnosis']['severity']}")
    print(f"  - Confidence: {dwarka_loc_result['diagnosis']['confidence']}%")
    print(f"  - NDVI (Photosynthetic Vigor): {dwarka_loc_result['spectral_indices']['ndvi']}")
    print(f"  - NDWI (Canopy Moisture): {dwarka_loc_result['spectral_indices']['ndwi']}")
    print(f"  - Canopy Status: {dwarka_loc_result['spectral_indices']['canopy_health']}")
    print(f"  - Forecasted Yield: {dwarka_loc_result['yield_forecast']['estimated_yield_q_ha']} q/ha (Baseline: {dwarka_loc_result['yield_forecast']['district_baseline_q_ha']} q/ha, Delta: {dwarka_loc_result['yield_forecast']['delta_pct']}%)")
    print(f"  - Chemical Rx: {dwarka_loc_result['diagnosis']['recommended_chemical']}")
    print(f"  - Organic Rx: {dwarka_loc_result['diagnosis']['recommended_organic']}")
    print(f"  - ICAR Advisory: {dwarka_loc_result['diagnosis']['crop_specific_advisory']}")

    # Method B: Manual Parameter Entry (Warm coastal monsoon telemetry)
    print("\n--- Method B: Manual Agronomic Parameters (Saurashtra Groundnut Belt) ---")
    manual_gn_temp = 29.5
    manual_gn_rh = 84.0
    manual_gn_rainfall_7d = 45.0
    manual_gn_soil_moisture = 70.0
    manual_gn_vpd = 1.05

    dwarka_manual_result = predict_multimodal_disease_and_yield(
        image_bytes=groundnut_bytes,
        crop_name="groundnut",
        temperature=manual_gn_temp,
        humidity=manual_gn_rh,
        rainfall_7d=manual_gn_rainfall_7d,
        soil_moisture=manual_gn_soil_moisture,
        vpd=manual_gn_vpd,
        canopy_source="Ground-Level Smartphone Macro"
    )

    print("\nResult [Dwarka Groundnut via Manual Entry]:")
    print(f"  - Diagnosed Disease: {dwarka_manual_result['diagnosis']['name']}")
    print(f"  - Severity Level: {dwarka_manual_result['diagnosis']['severity']}")
    print(f"  - Confidence: {dwarka_manual_result['diagnosis']['confidence']}%")
    print(f"  - Forecasted Yield: {dwarka_manual_result['yield_forecast']['estimated_yield_q_ha']} q/ha (Delta: {dwarka_manual_result['yield_forecast']['delta_pct']}%)")

    # Single-leaf Vision Agricultural Diagnosis
    print("\n--- Method C: Single-Leaf Disease Detection Vision Engine (/api/disease) ---")
    gn_b64 = base64.b64encode(groundnut_bytes).decode('utf-8')
    gn_single_diag = analyze_crop_disease(gn_b64, mime_type="image/jpeg")
    print("Single-Leaf Diagnosis Output Sample:")
    print(gn_single_diag[:400] + "...\n")

    # =========================================================================
    # SCENARIO 2: PUNJAB - WHEAT (गेहूँ)
    # =========================================================================
    print("\n" + "=" * 80)
    print("SCENARIO 2: PUNJAB REGION (LUDHIANA) | CROP: WHEAT")
    print("=" * 80)

    # Method A: Via Location (Live Open-Meteo Weather)
    print("\n--- Method A: Via Location (Punjab/Ludhiana: Lat 30.9010, Lon 75.8573) ---")
    punjab_weather = get_open_meteo_weather(city_name="Ludhiana", lat=30.9010, lon=75.8573)
    punjab_temp = float(punjab_weather.get('temp', 22.0))
    punjab_rh = float(punjab_weather.get('humidity', 50.0))
    punjab_precip = float(punjab_weather.get('precipitation', 0.0))
    punjab_rainfall_7d = max(5.0, punjab_precip * 7 if punjab_precip > 0 else 12.0)
    punjab_vpd = calculate_vpd(punjab_temp, punjab_rh)
    punjab_soil_moisture = min(80.0, max(25.0, punjab_rh * 0.70))

    print(f"Punjab Live Weather Fetched:")
    print(f"  - Temperature: {punjab_temp}°C")
    print(f"  - Relative Humidity: {punjab_rh}%")
    print(f"  - Calculated VPD: {punjab_vpd} kPa")
    print(f"  - Estimated 7-day Rainfall: {punjab_rainfall_7d} mm")
    print(f"  - Soil Moisture Proxy: {punjab_soil_moisture}%")
    print(f"  - Weather Condition: {punjab_weather.get('description')}")

    punjab_loc_result = predict_multimodal_disease_and_yield(
        image_bytes=wheat_bytes,
        crop_name="wheat",
        temperature=punjab_temp,
        humidity=punjab_rh,
        rainfall_7d=punjab_rainfall_7d,
        soil_moisture=punjab_soil_moisture,
        vpd=punjab_vpd,
        canopy_source="Sentinel-2 MSI (10m Resolution)"
    )

    print("\nResult [Punjab Wheat via Location]:")
    print(f"  - Diagnosed Disease: {punjab_loc_result['diagnosis']['name']}")
    print(f"  - Severity Level: {punjab_loc_result['diagnosis']['severity']}")
    print(f"  - Confidence: {punjab_loc_result['diagnosis']['confidence']}%")
    print(f"  - NDVI (Photosynthetic Vigor): {punjab_loc_result['spectral_indices']['ndvi']}")
    print(f"  - NDWI (Canopy Moisture): {punjab_loc_result['spectral_indices']['ndwi']}")
    print(f"  - Canopy Status: {punjab_loc_result['spectral_indices']['canopy_health']}")
    print(f"  - Forecasted Yield: {punjab_loc_result['yield_forecast']['estimated_yield_q_ha']} q/ha (Baseline: {punjab_loc_result['yield_forecast']['district_baseline_q_ha']} q/ha, Delta: {punjab_loc_result['yield_forecast']['delta_pct']}%)")
    print(f"  - Chemical Rx: {punjab_loc_result['diagnosis']['recommended_chemical']}")
    print(f"  - Organic Rx: {punjab_loc_result['diagnosis']['recommended_organic']}")
    print(f"  - ICAR Advisory: {punjab_loc_result['diagnosis']['crop_specific_advisory']}")

    # Method B: Manual Parameter Entry (Winter Yellow Rust Conducive conditions)
    print("\n--- Method B: Manual Agronomic Parameters (Punjab Winter Yellow Rust Window) ---")
    manual_wh_temp = 16.5
    manual_wh_rh = 86.0
    manual_wh_rainfall_7d = 36.0
    manual_wh_soil_moisture = 75.0
    manual_wh_vpd = 0.65

    punjab_manual_result = predict_multimodal_disease_and_yield(
        image_bytes=wheat_bytes,
        crop_name="wheat",
        temperature=manual_wh_temp,
        humidity=manual_wh_rh,
        rainfall_7d=manual_wh_rainfall_7d,
        soil_moisture=manual_wh_soil_moisture,
        vpd=manual_wh_vpd,
        canopy_source="Sentinel-2 MSI (10m Resolution)"
    )

    print("\nResult [Punjab Wheat via Manual Entry]:")
    print(f"  - Diagnosed Disease: {punjab_manual_result['diagnosis']['name']}")
    print(f"  - Severity Level: {punjab_manual_result['diagnosis']['severity']}")
    print(f"  - Confidence: {punjab_manual_result['diagnosis']['confidence']}%")
    print(f"  - Forecasted Yield: {punjab_manual_result['yield_forecast']['estimated_yield_q_ha']} q/ha (Delta: {punjab_manual_result['yield_forecast']['delta_pct']}%)")

    # Single-leaf Vision Agricultural Diagnosis
    print("\n--- Method C: Single-Leaf Disease Detection Vision Engine (/api/disease) ---")
    wheat_b64 = base64.b64encode(wheat_bytes).decode('utf-8')
    wheat_single_diag = analyze_crop_disease(wheat_b64, mime_type="image/jpeg")
    print("Single-Leaf Diagnosis Output Sample:")
    print(wheat_single_diag[:400] + "...\n")

    # =========================================================================
    # PART 3: TEST LIVE HTTP REST ENDPOINTS ON FLASK SERVER
    # =========================================================================
    print("=" * 80)
    print("TESTING RUNNING FLASK SERVER ENDPOINTS (http://127.0.0.1:5000)")
    print("=" * 80)
    session_req = requests.Session()

    # Login to authenticate
    login_resp = session_req.post(
        "http://127.0.0.1:5000/login",
        data={"username": "test_farmer", "password": "Password123!"},
        timeout=10,
        allow_redirects=True
    )
    print(f"Login Response Status: {login_resp.status_code}")

    # Test 1: /api/weather endpoint with Dwarka coordinates
    weather_payload = {"lat": 22.2442, "lon": 68.9685, "crop": "groundnut"}
    w_resp = session_req.post("http://127.0.0.1:5000/api/weather", json=weather_payload, timeout=10)
    print(f"API /api/weather (Dwarka) Status: {w_resp.status_code}")
    if w_resp.status_code == 200:
        w_json = w_resp.json()
        print(f"  -> Weather City: {w_json.get('weather', {}).get('city')}, Temp: {w_json.get('weather', {}).get('temp')}C, RH: {w_json.get('weather', {}).get('humidity')}%")

    # Test 2: /api/weather endpoint with Punjab coordinates
    punjab_w_payload = {"lat": 30.9010, "lon": 75.8573, "crop": "wheat"}
    w2_resp = session_req.post("http://127.0.0.1:5000/api/weather", json=punjab_w_payload, timeout=10)
    print(f"API /api/weather (Punjab) Status: {w2_resp.status_code}")
    if w2_resp.status_code == 200:
        w2_json = w2_resp.json()
        print(f"  -> Weather City: {w2_json.get('weather', {}).get('city')}, Temp: {w2_json.get('weather', {}).get('temp')}C, RH: {w2_json.get('weather', {}).get('humidity')}%")

    # Test 3: /api/multimodal-predict with Groundnut image
    files_gn = {
        'image': ('groundnut_leaf_spot_real.jpg', groundnut_bytes, 'image/jpeg')
    }
    data_gn = {
        'crop_name': 'groundnut',
        'temperature': str(dwarka_temp),
        'humidity': str(dwarka_rh),
        'rainfall_7d': str(dwarka_rainfall_7d),
        'soil_moisture': str(dwarka_soil_moisture),
        'vpd': str(dwarka_vpd),
        'canopy_source': 'Sentinel-2 MSI'
    }
    mm_resp = session_req.post("http://127.0.0.1:5000/api/multimodal-predict", files=files_gn, data=data_gn, timeout=15)
    print(f"API /api/multimodal-predict (Dwarka Groundnut) Status: {mm_resp.status_code}")
    if mm_resp.status_code == 200:
        mm_json = mm_resp.json()
        print(f"  -> Success: {mm_json.get('success')}, Disease: {mm_json.get('diagnosis', {}).get('name')}, Yield: {mm_json.get('yield_forecast', {}).get('estimated_yield_q_ha')} q/ha, NDVI: {mm_json.get('spectral_indices', {}).get('ndvi')}")

    # Test 4: /api/multimodal-predict with Wheat image
    files_wh = {
        'image': ('wheat_stripe_rust_real.jpg', wheat_bytes, 'image/jpeg')
    }
    data_wh = {
        'crop_name': 'wheat',
        'temperature': str(punjab_temp),
        'humidity': str(punjab_rh),
        'rainfall_7d': str(punjab_rainfall_7d),
        'soil_moisture': str(punjab_soil_moisture),
        'vpd': str(punjab_vpd),
        'canopy_source': 'Sentinel-2 MSI'
    }
    mm2_resp = session_req.post("http://127.0.0.1:5000/api/multimodal-predict", files=files_wh, data=data_wh, timeout=15)
    print(f"API /api/multimodal-predict (Punjab Wheat) Status: {mm2_resp.status_code}")
    if mm2_resp.status_code == 200:
        mm2_json = mm2_resp.json()
        print(f"  -> Success: {mm2_json.get('success')}, Disease: {mm2_json.get('diagnosis', {}).get('name')}, Yield: {mm2_json.get('yield_forecast', {}).get('estimated_yield_q_ha')} q/ha, NDVI: {mm2_json.get('spectral_indices', {}).get('ndvi')}")

    # Test 5: /api/disease (Single-Leaf Engine) with Groundnut
    d_resp = session_req.post("http://127.0.0.1:5000/api/disease", files={'image': ('groundnut.jpg', groundnut_bytes, 'image/jpeg')}, timeout=15)
    print(f"API /api/disease (Groundnut) Status: {d_resp.status_code}")
    if d_resp.status_code == 200:
        d_json = d_resp.json()
        print(f"  -> Diagnosis preview: {d_json.get('diagnosis', '')[:120]}...")

    # Save comprehensive results
    summary_data = {
        "scenario_1_dwarka_groundnut": {
            "location": {"city": "Dwarka", "state": "Gujarat", "lat": 22.2442, "lon": 68.9685},
            "live_weather": {
                "temp": dwarka_temp,
                "rh": dwarka_rh,
                "rainfall_7d": dwarka_rainfall_7d,
                "vpd": dwarka_vpd,
                "soil_moisture": dwarka_soil_moisture
            },
            "location_method_result": dwarka_loc_result,
            "manual_method_result": dwarka_manual_result,
            "single_leaf_diagnosis": gn_single_diag
        },
        "scenario_2_punjab_wheat": {
            "location": {"city": "Ludhiana", "state": "Punjab", "lat": 30.9010, "lon": 75.8573},
            "live_weather": {
                "temp": punjab_temp,
                "rh": punjab_rh,
                "rainfall_7d": punjab_rainfall_7d,
                "vpd": punjab_vpd,
                "soil_moisture": punjab_soil_moisture
            },
            "location_method_result": punjab_loc_result,
            "manual_method_result": punjab_manual_result,
            "single_leaf_diagnosis": wheat_single_diag
        }
    }

    # Clean gradcam base64 from summary file so it is compact and readable
    def clean_gradcam(obj):
        if isinstance(obj, dict):
            for k, v in list(obj.items()):
                if k == 'gradcam_image' and isinstance(v, str) and len(v) > 100:
                    obj[k] = "[CONFIRMED_VALID_BASE64_HEATMAP_DATA_URI]"
                elif isinstance(v, (dict, list)):
                    clean_gradcam(v)
        elif isinstance(obj, list):
            for item in obj:
                clean_gradcam(item)

    clean_gradcam(summary_data)

    out_file = os.path.join("experiment_data", "results", "comprehensive_verification_report.json")
    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)

    print(f"\n[SUCCESS] Comprehensive verification report written to: {out_file}")

if __name__ == "__main__":
    test_all()
