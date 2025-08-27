const chatBox = document.getElementById("chatBox");
const chatBody = document.getElementById("chatBody");
const optionsContainer = document.getElementById("optionsContainer");
let history = [];
function toggleChat() {
  const logoWidget = document.querySelector(".help-widget");
  logoWidget.classList.add("logo-slide-down");
  chatBox.classList.add("visible");
  chatBody.innerHTML = "";
  optionsContainer.innerHTML = "";
  startConversation();
}

function closeChat() {
  const logoWidget = document.querySelector(".help-widget");
  logoWidget.classList.remove("logo-slide-down");
  chatBox.classList.remove("visible");
  chatBody.innerHTML = "";
  optionsContainer.innerHTML = "";
}

function appendAssistantMessage(text) {
  const wrapper = document.createElement("div");
  wrapper.className = "message-wrapper assistant-wrapper";

  const avatarContainer = document.createElement("div");
  avatarContainer.className = "avatar-wrapper";

  const avatar = document.createElement("img");
  avatar.src = "image/logo-small (1).png";
  avatar.alt = "Assistant";
  avatar.className = "assistant-pic";

  avatarContainer.appendChild(avatar);

  const bubble = document.createElement("div");
  bubble.className = "message assistant";
  bubble.textContent = text;

  wrapper.appendChild(avatarContainer);
  wrapper.appendChild(bubble);
  chatBody.appendChild(wrapper);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function appendUserMessage(text) {
  const wrapper = document.createElement("div");
  wrapper.className = "message-wrapper user-wrapper";

  const avatarContainer = document.createElement("div");
  avatarContainer.className = "avatar-wrapper";

  const avatar = document.createElement("img");
  avatar.src = "image/profile2 (1).png";
  avatar.alt = "You";
  avatar.className = "user-pic";

  avatarContainer.appendChild(avatar);

  const bubble = document.createElement("div");
  bubble.className = "message user";
  bubble.textContent = text;

  wrapper.appendChild(avatarContainer);
  wrapper.appendChild(bubble);
  chatBody.appendChild(wrapper);
  chatBody.scrollTop = chatBody.scrollHeight;
}

function showTypingIndicator() {
  const wrapper = document.createElement("div");
  wrapper.className = "message-wrapper assistant-wrapper";

  const avatarContainer = document.createElement("div");
  avatarContainer.className = "avatar-wrapper";

  const avatar = document.createElement("img");
  avatar.src = "image/logo-small (1).png";
  avatar.alt = "Assistant";
  avatar.className = "assistant-pic";
  avatarContainer.appendChild(avatar);

  const bubble = document.createElement("div");
  bubble.className = "message assistant typing-indicator";
  bubble.innerHTML = `<span></span><span></span><span></span>`;

  wrapper.appendChild(avatarContainer);
  wrapper.appendChild(bubble);
  chatBody.appendChild(wrapper);
  chatBody.scrollTop = chatBody.scrollHeight;

  return wrapper;
}

function sendAssistantMessagesSequentially(messages, delay = 700, callback) {
  if (!messages.length) {
    if (callback) callback();
    return;
  }

  const typing = showTypingIndicator();
  setTimeout(() => {
    typing.remove();
    appendAssistantMessage(messages[0]);
    sendAssistantMessagesSequentially(messages.slice(1), delay, callback);
  }, delay);
}

function startConversation() {
  sendAssistantMessagesSequentially([
    "Welcome to Voyago",
    "How can I help you?"
  ], 700, showMainOptions);
}

function showMainOptions() {
  const options = [
    "Booking & Flights",
    "Hotels",
    "Packages",
    "Destinations",
    "Payment & Checkout",
    "Offers & Discounts",
    "Loyalty & Frequent Traveler Benefits"
  ];
  
  renderOptions(options, handleMainOptionClick);
}

function renderOptions(options, callback) {
  optionsContainer.innerHTML = "";
  options.forEach(option => {
    const opt = document.createElement("div");
    opt.className = "option-bubble";
    opt.textContent = option;
    opt.onclick = () => callback(option);
    optionsContainer.appendChild(opt);
  });
}

function handleMainOptionClick(option) {
  appendUserMessage(option);

  setTimeout(() => {
    const typing = showTypingIndicator();

    setTimeout(() => {
      typing.remove();

      if (option === "Booking & Flights") {
        appendAssistantMessage("Great! Here are some questions:");
        renderOptions([
          "How can I book a flight?",
          "Which airlines do you work with?",
          "How can I customize my flight search to match my preferences?",
          "Back"
        ], handleBookingOptions);

              } else if (option === "Hotels") {
                appendAssistantMessage("Let me help you with hotels:");
                renderOptions([
                  "How can I book a hotel?",
                  "Do I need to pay in advance for hotels?",
                  "Can I cancel my hotel booking?",
                  "Back"
                ], handleHotelOptions);

              } else if (option === "Packages") {
                appendAssistantMessage("Here’s what you can know about packages:");
                renderOptions([
                  "What is a travel package?",
                  "How do I customize a package?",
                  "Are travel packages refundable?",
                  "Back"
                ], handlePackageOptions);

              } else if (option === "Destinations") {
                appendAssistantMessage("Here’s what I can show you:");
                renderOptions([
                  "What can I find on the Destinations page?",
                  "Can I discover local dishes and where to eat?",
                  "Do you show things to do in each city?",
                  "Back"
                ], handleDestinationOptions);
              }else if (option === "Hotels") {
  appendAssistantMessage("Here’s what I can help you with:");
  renderOptions([
    "How can I book a hotel?",
    "Do I need to pay in advance for hotels?",
    "Can I cancel my hotel booking?",
    "Back"
  ], handleHotelsOptions);
} else if (option === "Packages") {
  appendAssistantMessage("Here are your questions:");
  renderOptions([
    "What is a travel package?",
    "How do I customize a package?",
    "Are travel packages refundable?",
    "Back"
  ], handlePackagesOptions);
} else if (option === "Destinations") {
  appendAssistantMessage("Discover our destination guides:");
  renderOptions([
    "What can I find on the Destinations page?",
    "Can I discover local dishes and where to eat?",
    "Do you show things to do in each city?",
    "Back"
  ], handleDestinationsOptions);
} else if (option === "Payment & Checkout") {
  appendAssistantMessage("Payment-related questions:");
  renderOptions([
    "What payment methods can I use to book?",
    "Can I pay in my local currency?",
    "Is my payment information secure?",
    "Back"
  ], handlePaymentOptions);
} else if (option === "Offers & Discounts") {
  appendAssistantMessage("Here’s what’s available:");
  renderOptions([
    "Are there any current promotions or discount codes?",
    "How do I apply a discount code?",
    "Back"
  ], handleOffersOptions);
} else if (option === "Loyalty & Frequent Traveler Benefits") {
  appendAssistantMessage("Here’s how you benefit:");
  renderOptions([
    "Do you have a loyalty or rewards program?",
    "How do I know if I’m eligible for loyalty benefits?",
    "Back"
  ], handleLoyaltyOptions);
}


    }, 1000);
  }, 500);
}


function handlePaymentOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  const responses = {
    "What payment methods can I use to book?": [
      "You can pay securely using Visa, MasterCard, PayPal, or Dhahabiya.",
      "We use encrypted payment gateways to ensure your information is protected."
    ],
    "Can I pay in my local currency?": [
      "Yes, we support multiple currencies depending on your location.",
      "Prices will be shown in your local currency automatically where possible."
    ],
    "Is my payment information secure?": [
      "Absolutely. All payments are processed through secure, encrypted gateways that meet international security standards."
    ]
  };

  sendAssistantMessagesSequentially(responses[option], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
}

function handleOffersOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  const responses = {
    "Are there any current promotions or discount codes?": [
      "We regularly offer seasonal promotions and exclusive deals.",
      "Be sure to check our homepage or subscribe to our newsletter to stay updated!"
    ],
    "How do I apply a discount code?": [
      "You can enter your promo code at checkout.",
      "The discount will be applied instantly if the code is valid and still active."
    ]
  };

  sendAssistantMessagesSequentially(responses[option], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
}

function handleLoyaltyOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  const responses = {
    "Do you have a loyalty or rewards program?": [
      "Yes! Customers who book frequently with us are eligible for special discounts, early access to deals, and occasional surprise perks."
    ],
    "How do I know if I’m eligible for loyalty benefits?": [
      "We track your booking history, and once you hit certain milestones, you’ll receive an email or notification in your account dashboard with your rewards or discounts."
    ]
  };

  sendAssistantMessagesSequentially(responses[option], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
}
function handleHotelOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  setTimeout(() => {
    const typing = showTypingIndicator();

    setTimeout(() => {
      typing.remove();

      if (option === "How can I book a hotel?") {
        sendAssistantMessagesSequentially([
          "Use our search bar to enter your destination and travel dates.",
          "You’ll see a list of available hotels that you can filter by rating, price, and amenities.",
          "Click any hotel to view full details and book instantly."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));

      } else if (option === "Do I need to pay in advance for hotels?") {
        sendAssistantMessagesSequentially([
          "Some hotels require prepayment, while others allow you to pay at check-in.",
          "Look for the payment policy on each hotel’s booking page."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));

      } else if (option === "Can I cancel my hotel booking?") {
        sendAssistantMessagesSequentially([
          "Yes, depending on the hotel's cancellation policy.",
          "Many listings offer free cancellation up to a certain date.",
          "Always check the policy before booking."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      }

    }, 1000);
  }, 500);
}
function handlePackageOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  setTimeout(() => {
    const typing = showTypingIndicator();

    setTimeout(() => {
      typing.remove();

      if (option === "What is a travel package?") {
        sendAssistantMessagesSequentially([
          "A travel package combines flights, hotels, and sometimes activities into a single convenient booking—often at a discounted price."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));

      } else if (option === "How do I customize a package?") {
        sendAssistantMessagesSequentially([
          "You can select your preferred flights and hotels during the booking process.",
          "Some packages even let you add extras like airport transfers or local tours."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));

      } else if (option === "Are travel packages refundable?") {
        sendAssistantMessagesSequentially([
          "It depends on the provider.",
          "Check the cancellation policy before confirming your package.",
          "Many packages offer partial or full refunds if canceled in time."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      }

    }, 1000);
  }, 500);
}
function handleDestinationOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  setTimeout(() => {
    const typing = showTypingIndicator();

    setTimeout(() => {
      typing.remove();

      if (option === "What can I find on the Destinations page?") {
        sendAssistantMessagesSequentially([
          "You can explore top cities worldwide, complete with must-see attractions, local dishes, hidden gems, and restaurant recommendations."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      } else if (option === "Can I discover local dishes and where to eat?") {
        sendAssistantMessagesSequentially([
          "Absolutely! Each city guide highlights popular dishes and recommends the best spots to try them—whether it’s street food or fine dining."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      } else if (option === "Do you show things to do in each city?") {
        sendAssistantMessagesSequentially([
          "Yes, from historical landmarks and museums to nightlife and adventure activities—we cover everything to help you plan the perfect trip."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      }

    }, 1000);
  }, 500);
}


function handleBookingOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  // Delay before typing appears
  setTimeout(() => {
    const typing = showTypingIndicator();
    
    setTimeout(() => {
      typing.remove();
      if (option === "How can I book a flight?") {
        appendAssistantMessage("You can book a flight directly through our website.");
        appendAssistantMessage("Just select your destination, travel dates, and passenger info.");
        appendAssistantMessage("We’ll show you all available options instantly.");
      } else if (option === "Which airlines do you work with?") {
        appendAssistantMessage("We partner with major global airlines as well as low-cost carriers to provide a wide range of flight options.");
      }
      renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions);
    }, 1000); // Time the assistant "types"

  }, 500); // Delay before typing starts
}

function handleChangeOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  setTimeout(() => {
    const typing = showTypingIndicator();

    setTimeout(() => {
      typing.remove();

      if (option === "Can I change my flight date after booking?") {
        sendAssistantMessagesSequentially([
          "Yes, flight dates can be changed depending on the fare rules of your ticket.",
          "Change fees may apply."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      } else if (option === "What if my flight is delayed or canceled?") {
        sendAssistantMessagesSequentially([
          "If your flight is affected, we’ll notify you by email or SMS.",
          "You may be eligible for a refund or alternative options."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      }

    }, 1000);
  }, 500);
}


function handleBaggageOptions(option) {
  if (option === "Back") return showMainOptions();
  appendUserMessage(option);

  setTimeout(() => {
    const typing = showTypingIndicator();

    setTimeout(() => {
      typing.remove();

      if (option === "What’s the baggage allowance for my flight?") {
        sendAssistantMessagesSequentially([
          "Your baggage allowance depends on the airline and fare type.",
          "It is clearly displayed before payment."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      } else if (option === "Are meals included in the flight?") {
        sendAssistantMessagesSequentially([
          "Meal service depends on the airline and class of service.",
          "You’ll see the meal info during the booking process."
        ], 700, () => renderOptions(["Thanks", "Back to Main Menu"], handleFinalOptions));
      }

    }, 1000);
  }, 500);
}


function handleFinalOptions(option) {
  appendUserMessage(option);
  optionsContainer.innerHTML = "";

  setTimeout(() => {
    const typing = showTypingIndicator();

    setTimeout(() => {
      typing.remove();

      if (option === "Thanks") {
        sendAssistantMessagesSequentially([
          "You're welcome! Let me know if you need anything else."
        ], 700, showBackOnly);
      } else if (option === "Back to Main Menu") {
        showMainOptions();
      }

    }, 1000);
  }, 500);
}


function showBackOnly() {
  optionsContainer.innerHTML = "";
  const back = document.createElement("div");
  back.className = "option-bubble";
  back.textContent = "Back";
  back.onclick = () => showMainOptions();
  optionsContainer.appendChild(back);
}

  