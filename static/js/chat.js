$(function () {
  var synth = window.speechSynthesis;
  var msg = new SpeechSynthesisUtterance();
  msg.rate = 1;
  msg.pitch = 1;
  var selectedImage = null;
  var isProcessing = false;

  // Load saved language preference
  var savedLanguage = localStorage.getItem("chatLanguage") || "en";
  $("#chatLanguage").val(savedLanguage);

  // Save language preference when changed
  $("#chatLanguage").change(function () {
    var language = $(this).val();
    localStorage.setItem("chatLanguage", language);

    // Show language change notification
    var languageName = $(this).find("option:selected").text();
    appendMessage("Language changed to " + languageName, false);
  });

  function formatMarkdown(text) {
    if (!text) return "";
    var escaped = $("<div>").text(text).html();
    
    // Headings ###
    escaped = escaped.replace(/^### (.*$)/gim, '<h3 style="margin: 8px 0 4px 0; color: #1b5e20; font-size: 1.05rem; font-weight: 700;">$1</h3>');
    escaped = escaped.replace(/^## (.*$)/gim, '<h2 style="margin: 8px 0 4px 0; color: #1b5e20; font-size: 1.15rem; font-weight: 700;">$1</h2>');
    
    // Bold **text**
    escaped = escaped.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    
    // Italics *text*
    escaped = escaped.replace(/\*([^\*]+)\*/g, '<em>$1</em>');
    
    // Bullet points (•, -, *)
    escaped = escaped.replace(/^[•\-\*] (.*$)/gim, '<div style="margin-left: 6px; padding: 2px 0;">• $1</div>');
    
    // Numbered items 1. 2.
    escaped = escaped.replace(/^(\d+)\. (.*$)/gim, '<div style="margin-left: 6px; padding: 2px 0;"><strong>$1.</strong> $2</div>');
    
    // Paragraph spacers and line breaks
    escaped = escaped.replace(/\n\n/g, '<div style="height: 8px;"></div>');
    escaped = escaped.replace(/\n/g, '<br>');
    
    return escaped;
  }

  function appendMessage(message, isUser, imageUrl = null) {
    var messageClass = isUser ? "user-message" : "bot-message";
    var logoHTML = isUser
      ? ""
      : '<div class="bot-logo"><img src="../static/robo.png" alt="Krishi Mitra"></div>';
    var userImageHTML = isUser
      ? '<div class="user-image"><img src="../static/user.png" alt="User"></div>'
      : "";

    var imageHTML =
      imageUrl && isUser
        ? '<div class="message-image"><img src="' +
          imageUrl +
          '" alt="Uploaded"></div>'
        : "";

    var messageElement = $(
      '<div class="message-container ' +
        (isUser ? "user-container" : "bot-container") +
        '">' +
        logoHTML +
        '<div class="message ' +
        messageClass +
        '">' +
        imageHTML +
        "</div>" +
        userImageHTML +
        "</div>",
    );
    $(".chat-messages").append(messageElement);

    if (isUser) {
      if (message)
        messageElement
          .find(".message")
          .append('<div class="message-text">' + $("<div>").text(message).html() + "</div>");
    } else {
      var textDiv = $('<div class="message-text"></div>');
      messageElement.find(".message").append(textDiv);
      textDiv.html(formatMarkdown(message));
    }
    $(".chat-messages").scrollTop($(".chat-messages")[0].scrollHeight);
  }

  function showTypingIndicator() {
    var typingIndicator = $(
      '<div class="typing-indicator bot-message"><span></span><span></span><span></span></div>',
    );
    $(".chat-messages").append(typingIndicator);
    $(".chat-messages").scrollTop($(".chat-messages")[0].scrollHeight);
  }

  function removeTypingIndicator() {
    $(".typing-indicator").remove();
  }

  function disableInput() {
    $(
      "#messageText, #chatbot-form-btn, #chatbot-form-btn-voice, #chatbot-form-btn-image",
    ).prop("disabled", true);
  }

  function enableInput() {
    $(
      "#messageText, #chatbot-form-btn, #chatbot-form-btn-voice, #chatbot-form-btn-image",
    ).prop("disabled", false);
  }

  $("#chatbot-form-btn-image").click(function (e) {
    e.preventDefault();
    $("#imageInput").click();
  });

  $("#imageInput").change(function (e) {
    var file = e.target.files[0];
    if (file) {
      selectedImage = file;
      var reader = new FileReader();
      reader.onload = function (e) {
        $("#imagePreview").attr("src", e.target.result);
        $("#imagePreviewContainer").show();
      };
      reader.readAsDataURL(file);
    }
  });

  $("#removeImage").click(function (e) {
    e.preventDefault();
    selectedImage = null;
    $("#imageInput").val("");
    $("#imagePreviewContainer").hide();
  });

  $("#chatbot-form-btn").click(function (e) {
    e.preventDefault();
    sendMessage();
  });

  $("#messageText").keypress(function (e) {
    if (e.which == 13) {
      e.preventDefault();
      sendMessage();
    }
  });

  function sendMessage() {
    var message = $("#messageText").val().trim();
    var imageUrl = selectedImage ? $("#imagePreview").attr("src") : null;
    var language = $("#chatLanguage").val() || "en";

    if ((message || selectedImage) && !isProcessing) {
      isProcessing = true;
      disableInput();

      appendMessage(message, true, imageUrl);
      $("#messageText").val("");
      showTypingIndicator();

      var formData = new FormData();
      formData.append("messageText", message);
      formData.append("language", language);
      if (selectedImage) formData.append("image", selectedImage);

      $.ajax({
        type: "POST",
        url: "/api/chat",
        data: formData,
        processData: false,
        contentType: false,
        success: function (response) {
          removeTypingIndicator();
          var answer = response.error
            ? "Error: " + response.error
            : response.answer;
          appendMessage(answer, false);

          if ($("#voiceReadingCheckbox").is(":checked")) {
            msg.text = answer;
            synth.speak(msg);
          }
          isProcessing = false;
          enableInput();
          selectedImage = null;
          $("#imageInput").val("");
          $("#imagePreviewContainer").hide();
        },
        error: function () {
          removeTypingIndicator();
          appendMessage("Sorry, there was an error. Please try again.", false);
          isProcessing = false;
          enableInput();
        },
      });
    }
  }

  var welcomeMessage =
    "🌱 **Welcome to Krishi Mitra!** I am your AI Smart Farming Assistant.\n\nI can help you with:\n• **Crop Advice**: Recommended varieties, sowing times & seed treatment\n• **Disease Doctor**: Diagnosis from symptoms/images & remedies\n• **Soil Health**: Soil testing, balanced NPK fertilizers & compost\n• **Weather & Irrigation**: Agro-meteorological advisories & water saving\n• **Mandi Bhav & Schemes**: Live market rates, PM-KISAN, PMFBY crop insurance & KCC loans\n\nAsk me anything about agriculture or upload a crop image!";

  $("#chatbot-form-btn-clear").click(function (e) {
    e.preventDefault();
    $(".chat-messages").empty();
    appendMessage(welcomeMessage, false);
  });

  $("#chatbot-form-btn-voice").click(function (e) {
    e.preventDefault();
    if ("webkitSpeechRecognition" in window && !isProcessing) {
      var recognition = new webkitSpeechRecognition();
      recognition.lang = "en-US";
      recognition.interimResults = false;
      recognition.start();

      recognition.onresult = function (event) {
        $("#messageText").val(event.results[0][0].transcript);
        sendMessage();
      };
    }
  });

  $("#voiceReadingCheckbox").change(function () {
    if (!$(this).is(":checked")) synth.cancel();
  });

  setTimeout(function () {
    appendMessage(welcomeMessage, false);
  }, 500);
});
