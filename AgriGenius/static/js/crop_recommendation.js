$(function () {
  // Mode switching
  $(".mode-btn").click(function () {
    $(".mode-btn").removeClass("active");
    $(this).addClass("active");

    const mode = $(this).data("mode");
    if (mode === "auto") {
      $("#auto-mode").show();
      $("#manual-mode").hide();
    } else {
      $("#auto-mode").hide();
      $("#manual-mode").show();
    }
  });

  // Get user location
  $("#getLocationBtn").click(function () {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by your browser");
      return;
    }

    $(this)
      .prop("disabled", true)
      .html('<i class="fas fa-spinner fa-spin"></i> Getting location...');

    navigator.geolocation.getCurrentPosition(
      function (position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;

        $.ajax({
          url: "/api/get-location",
          method: "POST",
          contentType: "application/json",
          data: JSON.stringify({ latitude: lat, longitude: lon }),
          success: function (data) {
            if (data.success && data.state) {
              $("#state").val(data.state).trigger("change");

              // Wait for districts to load, then select
              setTimeout(function () {
                if (data.district) {
                  $("#district").val(data.district);
                }
              }, 100);

              alert(
                `Location detected: ${data.city || data.district}, ${data.state}`,
              );
            } else {
              alert("Could not determine location details");
            }
            $("#getLocationBtn")
              .prop("disabled", false)
              .html('<i class="fas fa-map-marker-alt"></i> Use My Location');
          },
          error: function () {
            alert("Error getting location details");
            $("#getLocationBtn")
              .prop("disabled", false)
              .html('<i class="fas fa-map-marker-alt"></i> Use My Location');
          },
        });
      },
      function (error) {
        alert("Error: " + error.message);
        $("#getLocationBtn")
          .prop("disabled", false)
          .html('<i class="fas fa-map-marker-alt"></i> Use My Location');
      },
    );
  });

  // District data
  const districts = {
    Punjab: ["Amritsar", "Ludhiana", "Patiala", "Jalandhar", "Bathinda"],
    Haryana: ["Karnal", "Panipat", "Ambala", "Hisar", "Rohtak"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut"],
    Maharashtra: ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    Karnataka: ["Bangalore", "Mysore", "Hubli", "Belgaum", "Mangalore"],
    "Tamil Nadu": [
      "Chennai",
      "Coimbatore",
      "Madurai",
      "Salem",
      "Tiruchirappalli",
    ],
    "West Bengal": ["Kolkata", "Darjeeling", "Howrah", "Siliguri", "Durgapur"],
    Gujarat: ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
    Rajasthan: ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain"],
  };

  // Update districts when state changes
  $("#state").change(function () {
    const state = $(this).val();
    const districtSelect = $("#district");
    districtSelect.html('<option value="">Choose District</option>');

    if (state && districts[state]) {
      districts[state].forEach((district) => {
        districtSelect.append(
          `<option value="${district}">${district}</option>`,
        );
      });
    }
  });

  // Auto-fill button
  $("#autoFillBtn").click(function () {
    const state = $("#state").val();
    const district = $("#district").val();

    if (!state || !district) {
      alert("Please select both state and district");
      return;
    }

    $.ajax({
      url: "/api/get-district-averages",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify({ state, district }),
      success: function (data) {
        $("#N").val(data.N);
        $("#P").val(data.P);
        $("#K").val(data.K);
        $("#temperature").val(data.temperature);
        $("#humidity").val(data.humidity);
        $("#ph").val(data.ph);
        $("#rainfall").val(data.rainfall);

        // Switch to manual mode to show filled values
        $('.mode-btn[data-mode="manual"]').click();
        alert("Values auto-filled! You can adjust them if needed.");
      },
      error: function () {
        alert("Error fetching district data");
      },
    });
  });

  // Predict button
  $("#predictBtn").click(function () {
    const data = {
      N: parseFloat($("#N").val()),
      P: parseFloat($("#P").val()),
      K: parseFloat($("#K").val()),
      temperature: parseFloat($("#temperature").val()),
      humidity: parseFloat($("#humidity").val()),
      ph: parseFloat($("#ph").val()),
      rainfall: parseFloat($("#rainfall").val()),
    };

    // Validate
    for (let key in data) {
      if (isNaN(data[key])) {
        alert(`Please enter valid ${key} value`);
        return;
      }
    }

    $("#loading").show();
    $("#results").hide();
    $("#error").hide();

    $.ajax({
      url: "/api/predict-crop",
      method: "POST",
      contentType: "application/json",
      data: JSON.stringify(data),
      success: function (response) {
        $("#loading").hide();
        displayResults(response);
      },
      error: function (xhr) {
        $("#loading").hide();
        $("#error")
          .text(xhr.responseJSON?.error || "Error predicting crops")
          .show();
      },
    });
  });

  function displayResults(data) {
    // Display top crops
    let cropsHTML = "";
    data.top_crops.forEach((crop, index) => {
      const medal = index === 0 ? "🥇" : index === 1 ? "🥈" : "🥉";
      cropsHTML += `
        <div class="crop-item">
          <span class="crop-rank">${medal}</span>
          <span class="crop-name">${crop.crop}</span>
          <div class="crop-probability">
            <div class="prob-bar" style="width: ${crop.probability}%"></div>
            <span class="prob-text">${crop.probability}%</span>
          </div>
        </div>
      `;
    });
    $("#cropsList").html(cropsHTML);

    // Display confidence
    const confidenceClass = data.confidence.toLowerCase();
    $("#confidenceBadge").html(`
      <span class="confidence-${confidenceClass}">
        <i class="fas fa-check-circle"></i> ${data.confidence} Confidence
      </span>
    `);

    // Display reasoning
    let reasoningHTML = "";
    data.reasoning.forEach((factor) => {
      reasoningHTML += `
        <div class="factor-item">
          <strong>${factor.feature}:</strong> ${factor.value}
          <span class="importance">(${factor.importance}% influence)</span>
        </div>
      `;
    });
    $("#reasoning").html(reasoningHTML);

    $("#results").show();
  }
});
