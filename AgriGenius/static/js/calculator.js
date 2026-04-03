$(function () {
  // Unit conversion rates to hectares
  const conversionRates = {
    acres: 0.404686,
    hectares: 1,
    bigha: 0.25, // UP Bigha
    bigha_punjab: 0.2023, // Punjab Bigha
    bigha_rajasthan: 0.25, // Rajasthan Bigha
    kanal: 0.0505857,
    gunta: 0.010117,
    sq_meters: 0.0001,
  };

  const unitNames = {
    acres: "Acres",
    hectares: "Hectares",
    bigha: "Bigha (UP)",
    bigha_punjab: "Bigha (Punjab)",
    bigha_rajasthan: "Bigha (Rajasthan)",
    kanal: "Kanal",
    gunta: "Gunta",
    sq_meters: "Square Meters",
  };

  $("#calculateBtn").on("click", function () {
    var cropType = $("#cropType").val().trim();
    var area = parseFloat($("#areaInput").val());
    var areaUnit = $("#areaUnit").val();
    var soilType = $("#soilType").val();
    var growthStage = $("#growthStage").val();

    if (!cropType || !area || isNaN(area)) {
      $("#calcError").text("Please fill in crop type and area.").show();
      return;
    }

    // Convert to hectares
    var areaInHectares = area * conversionRates[areaUnit];

    // Show conversion info
    var conversionText = `${area} ${unitNames[areaUnit]} = ${areaInHectares.toFixed(3)} Hectares`;
    if (areaUnit !== "hectares") {
      conversionText += ` (${(areaInHectares * 2.47105).toFixed(3)} Acres)`;
    }

    $("#calcError").hide();
    $("#calcResult").hide();
    $("#loadingCalc").show();
    $("#calculateBtn").prop("disabled", true);

    $.ajax({
      type: "POST",
      url: "/api/calculate-profit",
      contentType: "application/json",
      data: JSON.stringify({
        crop_type: cropType,
        area: area,
        area_unit: areaUnit,
        area_hectares: areaInHectares,
        soil_type: soilType,
        growth_stage: growthStage,
      }),
      success: function (response) {
        $("#loadingCalc").hide();
        $("#calculateBtn").prop("disabled", false);

        if (response.error) {
          $("#calcError").text(response.error).show();
          return;
        }

        // Display conversion
        $("#conversionInfo").html(`
          <div class="conversion-box">
            <i class="fas fa-info-circle"></i>
            <span>${conversionText}</span>
          </div>
        `);

        // Display profit analysis
        if (response.profit_analysis) {
          const profit = response.profit_analysis;
          $("#totalCost").text(`₹${profit.total_cost.toLocaleString()}`);
          $("#expectedYield").text(`${profit.expected_yield} quintals`);
          $("#totalRevenue").text(`₹${profit.total_revenue.toLocaleString()}`);
          $("#netProfit").text(`₹${profit.net_profit.toLocaleString()}`);

          // Color code profit
          if (profit.net_profit > 0) {
            $("#netProfit").css("color", "#4caf50");
          } else {
            $("#netProfit").css("color", "#f44336");
          }

          // Breakdown
          $("#profitBreakdown").html(`
            <div class="breakdown-section">
              <h4>Cost Breakdown</h4>
              <p><strong>Cost per Hectare:</strong> ₹${profit.cost_per_hectare.toLocaleString()}</p>
              <p><strong>Total Area:</strong> ${areaInHectares.toFixed(3)} hectares</p>
              <p><strong>Total Cost:</strong> ₹${profit.total_cost.toLocaleString()}</p>
            </div>
            <div class="breakdown-section">
              <h4>Revenue Breakdown</h4>
              <p><strong>Yield per Hectare:</strong> ${profit.yield_per_hectare} quintals</p>
              <p><strong>Price per Quintal:</strong> ₹${profit.price_per_quintal.toLocaleString()}</p>
              <p><strong>Expected Yield:</strong> ${profit.expected_yield} quintals</p>
              <p><strong>Total Revenue:</strong> ₹${profit.total_revenue.toLocaleString()}</p>
            </div>
            <div class="breakdown-section highlight">
              <h4>Profit Margin</h4>
              <p><strong>Net Profit:</strong> ₹${profit.net_profit.toLocaleString()}</p>
              <p><strong>Profit Margin:</strong> ${profit.profit_margin}%</p>
              <p><strong>ROI:</strong> ${profit.roi}%</p>
            </div>
          `);
        }

        // Display resource requirements
        $("#calcContent").html(formatMarkdown(response.resources));
        $("#calcResult").show();
      },
      error: function () {
        $("#loadingCalc").hide();
        $("#calculateBtn").prop("disabled", false);
        $("#calcError").text("Error calculating. Please try again.").show();
      },
    });
  });

  function formatMarkdown(text) {
    if (!text) return "";
    return text
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/^### (.*$)/gm, "<h4>$1</h4>")
      .replace(/^## (.*$)/gm, "<h3>$1</h3>")
      .replace(/^# (.*$)/gm, "<h2>$1</h2>")
      .replace(/^\- (.*$)/gm, "• $1")
      .replace(/^\d+\. (.*$)/gm, "<li>$1</li>")
      .replace(/\n/g, "<br>");
  }
});
