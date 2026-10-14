/**
 * Multimodal Remote Sensing & Crop Disease/Yield Prediction Frontend Logic
 * Connects with /api/multimodal-predict and /api/sample-remote-sensing/<preset>
 */

document.addEventListener('DOMContentLoaded', function () {
  const dropZone = document.getElementById('dropZone');
  const canopyImageInput = document.getElementById('canopyImageInput');
  const imagePreviewContainer = document.getElementById('imagePreviewContainer');
  const canopyPreviewImg = document.getElementById('canopyPreviewImg');
  const clearImageBtn = document.getElementById('clearImageBtn');
  const imageFilenameBadge = document.getElementById('imageFilenameBadge');
  const autoFillWeatherBtn = document.getElementById('autoFillWeatherBtn');
  const multimodalForm = document.getElementById('multimodalForm');
  const runPredictionBtn = document.getElementById('runPredictionBtn');
  const loadingSpinner = document.getElementById('loadingSpinner');
  const resultsContainer = document.getElementById('resultsContainer');
  const presetButtons = document.querySelectorAll('.preset-btn');

  let currentImageFile = null;
  let currentImageBase64 = null;

  // Dynamic Crop Agronomic Hints (All 90 crops supported)
  const cropSelectEl = document.getElementById('cropName');
  const cropAgronomicHint = document.getElementById('cropAgronomicHint');

  const CROP_HINTS = {
    wheat: "🌾 Baseline: 50.0 q/ha • Comfort: 12-25°C • 50-70% RH",
    rice: "🌱 Baseline: 57.5 q/ha • Comfort: 20-35°C • 70-90% RH",
    cotton: "🌿 Baseline: 26.0 q/ha • Comfort: 21-36°C • 55-80% RH",
    mustard: "🌻 Baseline: 18.0 q/ha • Comfort: 14-25°C • 50-70% RH",
    sugarcane: "🎋 Baseline: 950.0 q/ha • Comfort: 20-38°C • 65-88% RH",
    maize: "🌽 Baseline: 42.0 q/ha • Comfort: 18-32°C • 55-75% RH",
    chickpea: "🌱 Baseline: 24.0 q/ha • Comfort: 15-28°C • 45-70% RH",
    soybean: "🌻 Baseline: 26.0 q/ha • Comfort: 20-32°C • 60-80% RH",
    potato: "🥔 Baseline: 300.0 q/ha • Comfort: 14-24°C • 65-85% RH",
    tomato: "🍅 Baseline: 500.0 q/ha • Comfort: 18-30°C • 55-75% RH",
    onion: "🧅 Baseline: 220.0 q/ha • Comfort: 15-28°C • 50-70% RH",
    mango: "🥭 Baseline: 125.0 q/ha • Comfort: 20-38°C • 50-75% RH",
    banana: "🍌 Baseline: 450.0 q/ha • Comfort: 20-35°C • 70-90% RH",
    apple: "🍎 Baseline: 185.0 q/ha • Comfort: 5-24°C • 60-80% RH",
    grapes: "🍇 Baseline: 250.0 q/ha • Comfort: 15-35°C • 50-70% RH",
    pomegranate: "🍎 Baseline: 140.0 q/ha • Comfort: 20-38°C • 40-65% RH",
    guava: "🍈 Baseline: 180.0 q/ha • Comfort: 18-34°C • 50-75% RH",
    papaya: "🍈 Baseline: 550.0 q/ha • Comfort: 22-35°C • 60-85% RH",
    chilli: "🌶️ Baseline: 25.0 q/ha • Comfort: 18-32°C • 50-75% RH"
  };

  if (cropSelectEl && cropAgronomicHint) {
    cropSelectEl.addEventListener('change', function () {
      const selectedCrop = this.value;
      const hint = CROP_HINTS[selectedCrop] || "🌿 Authentic ICAR agronomic envelope & yield calibration active";
      cropAgronomicHint.textContent = hint;
    });
  }

  // 1. Dropzone Click & Drag Events
  if (dropZone) {
    dropZone.addEventListener('click', () => canopyImageInput.click());

    ['dragenter', 'dragover'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.style.background = '#e8f5e9';
        dropZone.style.borderColor = '#2e7d32';
      });
    });

    ['dragleave', 'drop'].forEach(eventName => {
      dropZone.addEventListener(eventName, (e) => {
        e.preventDefault();
        dropZone.style.background = '#f9fbf9';
        dropZone.style.borderColor = '#81c784';
      });
    });

    dropZone.addEventListener('drop', (e) => {
      if (e.dataTransfer.files && e.dataTransfer.files[0]) {
        handleFileSelect(e.dataTransfer.files[0]);
      }
    });
  }

  if (canopyImageInput) {
    canopyImageInput.addEventListener('change', (e) => {
      if (e.target.files && e.target.files[0]) {
        handleFileSelect(e.target.files[0]);
      }
    });
  }

  function handleFileSelect(file) {
    currentImageFile = file;
    imageFilenameBadge.textContent = `${file.name} (${Math.round(file.size / 1024)} KB)`;

    const reader = new FileReader();
    reader.onload = function (e) {
      currentImageBase64 = e.target.result;
      canopyPreviewImg.src = e.target.result;
      imagePreviewContainer.style.display = 'block';
      dropZone.style.display = 'none';
    };
    reader.readAsDataURL(file);
  }

  if (clearImageBtn) {
    clearImageBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      currentImageFile = null;
      currentImageBase64 = null;
      canopyImageInput.value = '';
      imagePreviewContainer.style.display = 'none';
      dropZone.style.display = 'block';
    });
  }

  // 2. Preset Scenarios Loading
  presetButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const presetId = btn.getAttribute('data-preset');
      btn.style.opacity = '0.6';

      try {
        const resp = await fetch(`/api/sample-remote-sensing/${presetId}`);
        const data = await resp.json();

        if (data.success) {
          const sc = data.scenario;
          if (cropSelectEl) {
            cropSelectEl.value = sc.crop;
            cropSelectEl.dispatchEvent(new Event('change'));
          }
          document.getElementById('temperatureInput').value = sc.temperature;
          document.getElementById('humidityInput').value = sc.humidity;
          document.getElementById('rainfallInput').value = sc.rainfall_7d;
          document.getElementById('soilMoistureInput').value = sc.soil_moisture;
          document.getElementById('vpdInput').value = sc.vpd;
          document.getElementById('canopySource').value = sc.canopy_source;

          // Set synthetic image
          currentImageBase64 = data.image_data_url;
          currentImageFile = null;
          canopyPreviewImg.src = data.image_data_url;
          imageFilenameBadge.textContent = `${sc.title} (Preloaded Multispectral Array)`;
          imagePreviewContainer.style.display = 'block';
          dropZone.style.display = 'none';

          // Visual highlight active preset
          presetButtons.forEach(b => b.style.boxShadow = 'none');
          btn.style.boxShadow = '0 0 0 2.5px #2e7d32';

          // Trigger prediction automatically for instant user wow factor
          runPrediction();
        }
      } catch (err) {
        console.error('Preset loading error:', err);
      } finally {
        btn.style.opacity = '1';
      }
    });
  });

  // 3. Auto-Fill GPS Weather
  if (autoFillWeatherBtn) {
    autoFillWeatherBtn.addEventListener('click', () => {
      autoFillWeatherBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Geocoding...';

      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          async (pos) => {
            try {
              const resp = await fetch('/api/weather', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  lat: pos.coords.latitude,
                  lon: pos.coords.longitude,
                  crop: document.getElementById('cropName').value
                })
              });
              const data = await resp.json();
              if (data.weather) {
                document.getElementById('temperatureInput').value = data.weather.temp;
                document.getElementById('humidityInput').value = data.weather.humidity;
                if (data.weather.precipitation !== undefined) {
                  document.getElementById('rainfallInput').value = Math.max(5, data.weather.precipitation * 7);
                }
              }
            } catch (e) {
              console.warn('Weather fetch warning:', e);
            } finally {
              autoFillWeatherBtn.innerHTML = '<i class="fas fa-check"></i> Weather Synced!';
              setTimeout(() => {
                autoFillWeatherBtn.innerHTML = '<i class="fas fa-location-arrow"></i> Auto-Fill GPS Weather';
              }, 3000);
            }
          },
          () => {
            autoFillWeatherBtn.innerHTML = '<i class="fas fa-exclamation-triangle"></i> GPS Access Denied';
            setTimeout(() => {
              autoFillWeatherBtn.innerHTML = '<i class="fas fa-location-arrow"></i> Auto-Fill GPS Weather';
            }, 3000);
          }
        );
      }
    });
  }

  // 4. Submit & Execute Multimodal Prediction
  if (multimodalForm) {
    multimodalForm.addEventListener('submit', (e) => {
      e.preventDefault();
      runPrediction();
    });
  }

  async function runPrediction() {
    runPredictionBtn.disabled = true;
    loadingSpinner.style.display = 'block';

    const formData = new FormData();
    if (currentImageFile) {
      formData.append('image', currentImageFile);
    } else if (currentImageBase64) {
      formData.append('image_base64', currentImageBase64);
    }

    formData.append('crop_name', document.getElementById('cropName').value);
    formData.append('temperature', document.getElementById('temperatureInput').value);
    formData.append('humidity', document.getElementById('humidityInput').value);
    formData.append('rainfall_7d', document.getElementById('rainfallInput').value);
    formData.append('soil_moisture', document.getElementById('soilMoistureInput').value);
    formData.append('vpd', document.getElementById('vpdInput').value);
    formData.append('canopy_source', document.getElementById('canopySource').value);

    try {
      const resp = await fetch('/api/multimodal-predict', {
        method: 'POST',
        body: formData
      });
      const data = await resp.json();

      if (data.success) {
        renderResults(data);
      } else {
        alert(data.error || 'Failed to process multimodal analysis.');
      }
    } catch (err) {
      console.error('Inference error:', err);
      alert('Error connecting with the multimodal server.');
    } finally {
      runPredictionBtn.disabled = false;
      loadingSpinner.style.display = 'none';
    }
  }

  function renderResults(res) {
    resultsContainer.style.display = 'block';

    // 1. Spectral Indices
    const s = res.spectral_indices;
    document.getElementById('valNdvi').textContent = s.ndvi.toFixed(3);
    document.getElementById('badgeNdvi').textContent = s.canopy_health;
    document.getElementById('badgeNdvi').style.color = s.health_color;

    document.getElementById('valNdwi').textContent = s.ndwi.toFixed(3);
    document.getElementById('valGndvi').textContent = s.gndvi.toFixed(3);
    document.getElementById('valSavi').textContent = s.savi.toFixed(3);
    document.getElementById('valCoverage').textContent = `${s.vegetation_coverage_pct}%`;

    // Populate Printable Report Header Metadata
    const cropSelect = document.getElementById('cropName');
    const selectedCropText = cropSelect && cropSelect.selectedIndex >= 0 ? cropSelect.options[cropSelect.selectedIndex].text : 'Crop';
    const sourceSelect = document.getElementById('canopySource');
    const selectedSourceText = sourceSelect && sourceSelect.selectedIndex >= 0 ? sourceSelect.options[sourceSelect.selectedIndex].text : 'Multispectral Sensor';
    const tempVal = document.getElementById('temperatureInput') ? document.getElementById('temperatureInput').value : '--';
    const rhVal = document.getElementById('humidityInput') ? document.getElementById('humidityInput').value : '--';
    const rainVal = document.getElementById('rainfallInput') ? document.getElementById('rainfallInput').value : '--';
    const smVal = document.getElementById('soilMoistureInput') ? document.getElementById('soilMoistureInput').value : '--';
    const vpdVal = document.getElementById('vpdInput') ? document.getElementById('vpdInput').value : '--';

    if (document.getElementById('printCropName')) document.getElementById('printCropName').textContent = selectedCropText;
    if (document.getElementById('printCanopySource')) document.getElementById('printCanopySource').textContent = selectedSourceText;
    if (document.getElementById('printWeatherSummary')) document.getElementById('printWeatherSummary').textContent = `${tempVal}°C / ${rhVal}% RH (${rainVal}mm Rain)`;
    if (document.getElementById('printSoilSummary')) document.getElementById('printSoilSummary').textContent = `${smVal}% Moisture / ${vpdVal} kPa VPD`;
    if (document.getElementById('printReportId')) {
      const rndId = Math.floor(1000 + Math.random() * 9000);
      document.getElementById('printReportId').textContent = `KM-MS-${new Date().toISOString().slice(0,10).replace(/-/g,'')}-${rndId}`;
    }
    if (document.getElementById('printTimestamp')) {
      document.getElementById('printTimestamp').textContent = new Date().toLocaleString('en-IN', {
        dateStyle: 'medium',
        timeStyle: 'short'
      });
    }

    // 2. Images: Raw & Grad-CAM
    document.getElementById('rawResultImg').src = currentImageBase64 || canopyPreviewImg.src;
    document.getElementById('gradcamResultImg').src = res.gradcam_image;

    // 3. Disease Diagnosis
    const diag = res.diagnosis;
    document.getElementById('diseaseName').textContent = diag.name;
    document.getElementById('confidenceScore').textContent = `${diag.confidence}%`;
    const sevBadge = document.getElementById('severityBadge');
    sevBadge.textContent = diag.severity;
    sevBadge.style.background = `${diag.color}22`;
    sevBadge.style.color = diag.color;
    sevBadge.style.border = `1px solid ${diag.color}`;

    document.getElementById('chemicalAction').textContent = diag.recommended_chemical;
    document.getElementById('organicAction').textContent = diag.recommended_organic;

    // Render ICAR Crop-Specific Pathogen Advisory
    const advisoryBox = document.getElementById('cropSpecificAdvisoryContainer');
    const advisoryTitle = document.getElementById('advisoryCropTitle');
    const advisoryText = document.getElementById('cropSpecificAdvisoryText');
    const specificAdvisory = (diag && diag.crop_specific_advisory) || res.crop_advisory;

    if (advisoryBox && specificAdvisory) {
      if (advisoryTitle) advisoryTitle.textContent = res.crop || 'Selected Crop';
      if (advisoryText) advisoryText.textContent = specificAdvisory;
      advisoryBox.style.display = 'block';
    } else if (advisoryBox) {
      advisoryBox.style.display = 'none';
    }

    // Probability breakdown bars
    const probList = document.getElementById('classProbList');
    probList.innerHTML = '';
    diag.probabilities.forEach(p => {
      const barItem = document.createElement('div');
      barItem.innerHTML = `
        <div style="display: flex; justify-content: space-between; font-size: 11px; margin-bottom: 2px;">
          <span>${p.class}</span>
          <strong>${p.prob}%</strong>
        </div>
        <div style="background: #e0e0e0; height: 6px; border-radius: 4px; overflow: hidden;">
          <div style="width: ${p.prob}%; height: 100%; background: ${p.color}; border-radius: 4px; transition: width 0.5s ease;"></div>
        </div>
      `;
      probList.appendChild(barItem);
    });

    // 4. Yield Forecast
    const yf = res.yield_forecast;
    document.getElementById('yieldForecastVal').textContent = yf.estimated_yield_q_ha;
    document.getElementById('districtBaseVal').textContent = `${yf.district_baseline_q_ha} q/ha`;
    const yDelta = document.getElementById('yieldDeltaVal');
    const sign = yf.delta_pct >= 0 ? '+' : '';
    yDelta.textContent = `${sign}${yf.delta_pct}% (${yf.status})`;
    yDelta.style.color = yf.delta_pct >= 0 ? '#2e7d32' : '#c62828';

    // 5. Environmental Attribution
    const attrList = document.getElementById('attributionList');
    attrList.innerHTML = '';
    res.climate_attribution.forEach(a => {
      const item = document.createElement('div');
      item.style.padding = '8px 10px';
      item.style.background = '#f9f9f9';
      item.style.borderRadius = '8px';
      item.style.border = '1px solid #eee';
      item.innerHTML = `
        <div style="display: flex; justify-content: space-between; font-size: 12px; font-weight: 600; margin-bottom: 2px;">
          <span>${a.factor}</span>
          <span style="color: #1b5e20;">${a.weight}% Weight</span>
        </div>
        <div style="font-size: 11px; color: #666;">${a.impact}</div>
      `;
      attrList.appendChild(item);
    });

    // Smooth scroll to results
    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }

  // Load the first preset by default so the page looks active on initial open
  const firstPreset = document.querySelector('.preset-btn');
  if (firstPreset) {
    firstPreset.click();
  }
});
