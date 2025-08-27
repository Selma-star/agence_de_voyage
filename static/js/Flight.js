
  // Flight Booking Modal Logic
document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById('bookingModal');
  const bookNowButtons = document.querySelectorAll('.bookNowBtn');
  const closeBtn = document.getElementById('modalCloseBtn');
  document.getElementById("seat_count").addEventListener("input", calculateTotal);
  document.getElementById("class_type").addEventListener("change", calculateTotal);

  // Attach event to each 'Book Now' button
  bookNowButtons.forEach(button => {
    button.addEventListener('click', function () {
      const company = this.getAttribute('data-airline');
      const departureCity = this.getAttribute('data-departure-city');
      const departureTime = this.getAttribute('data-departure-time');
      const arrivalCity = this.getAttribute('data-arrival-city');
      const arrivalTime = this.getAttribute('data-arrival-time');
      const price = parseFloat(this.getAttribute('data-price'));

      // Fill flight summary details
      document.getElementById("companyName").textContent = company;
      document.getElementById("departureCity").textContent = departureCity;
      document.getElementById("departureTime").textContent = departureTime;
      document.getElementById("arrivalCity").textContent = arrivalCity;
      document.getElementById("arrivalTime").textContent = arrivalTime;

      // Set base price as value for calculation
      const finalAmountInput = document.getElementById("finalAmount");
      finalAmountInput.value = price.toFixed(2);
      finalAmountInput.setAttribute("data-base-price", price.toFixed(2));
      document.getElementById("totalPrice").textContent = price.toFixed(2) + "\u00A0DZD";

        // Reset form sections
        document.getElementById('bookingSummarySection').style.display = 'block';
        document.getElementById('infoSection').style.display = 'none';
    
        // Set default values
        document.getElementById("seat_count").value = 1;
        document.getElementById("class_type").value = "Economy";
    
        // Show modal
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    
        // Add listener for seat count and class type
        document.getElementById("seat_count").addEventListener("input", calculateTotal);
        document.getElementById("class_type").addEventListener("change", calculateTotal);
    });
  });

  // Modal Close
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    });
  }

  window.onclick = function (event) {
    if (event.target === modal) {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }
  };

  // Coupon Application

  window.applyCoupon = function () {
    const coupon = document.getElementById("summaryCoupon").value.trim();
    fetch(`/validate-coupon/?code=${coupon}`)
      .then(response => response.json())
      .then(data => {
        if (data.valid) {
          alert(`Coupon appliqué ! ${data.discount}% de réduction.`);
          couponApplied = true;
          couponDiscount = data.discount; // ← stocke la valeur dynamique
          calculateTotal();
        } else {
          alert(data.message);
          couponApplied = false;
          couponDiscount = 0;
          calculateTotal();
        }
      });
  };
  
  

  let couponApplied = false;
  let couponDiscount = 0;

  // Calculate Total Price
  function calculateTotal() {
    const baseInput = document.getElementById("finalAmount");
    const basePrice = parseFloat(baseInput.getAttribute("data-base-price")) || 0;
  
    const seatCount = parseInt(document.getElementById("seat_count").value) || 1;
    const classType = document.getElementById("class_type").value;
   
  
    let classMultiplier = 1;
    if (classType === "Business") {
      classMultiplier = 1.5;
    } else if (classType === "First Class") {
      classMultiplier = 2;
    }
    let total = basePrice * classMultiplier * seatCount;

    const coupon = document.getElementById("summaryCoupon").value.trim();

    if (couponApplied) {
      total *= (1 - couponDiscount / 100);
    }
  
    document.getElementById("totalPrice").textContent = total.toFixed(2) + "\u00A0DZD";
    baseInput.value = total.toFixed(2); // Final amount to submit
  }
  
  

  // Dropdown Option for Class Type
  window.selectOption = function (value) {
    document.getElementById("class_type").value = value;
    calculateTotal();
  };

  // Move to Info Section
  window.showInfoSection = function () {
    document.getElementById('infoSection').style.display = 'flex';
    document.getElementById('bookingSummarySection').style.display = 'none';
  };

  // Success message fade-out (if exists)
  setTimeout(() => {
    const alert = document.querySelector('[style*="background-color: #d4edda"]');
    if (alert) {
      alert.style.transition = 'opacity 0.5s ease';
      alert.style.opacity = '0';
      setTimeout(() => alert.remove(), 500);
    }
  }, 4000);
});
