document.addEventListener("DOMContentLoaded", function () {
  

  // Feedback carousel
  let feedbacks = document.querySelectorAll(".feedback-card");
  let index = 0;

  function showFeedback(i) {
      feedbacks.forEach((card, idx) => {
          card.style.display = (idx === i || idx === i + 1) ? "block" : "none";
      });
  }

  function prevFeedback() {
      index = (index - 1 + feedbacks.length) % feedbacks.length;
      showFeedback(index);
  }

  function nextFeedback() {
      index = (index + 1) % feedbacks.length;
      showFeedback(index);
  }

  showFeedback(0);

  // Booking Modal
  const modal = document.getElementById('bookingModal');
  const bookNowButtons = document.querySelectorAll('.bookNowBtn');
  const closeBtn = document.getElementById('modalCloseBtn');

  document.querySelectorAll('.bookNowBtn').forEach(button => {
    button.addEventListener('click', function () {
      const hotelType = this.getAttribute('data-hotel-type');
      const hotelDescription = this.getAttribute('data-hotel-description');
      const roomType = this.getAttribute('data-room-type');
      const roomDescription = this.getAttribute('data-room-description');
      const roomPrice = this.getAttribute('data-room-price');
  
      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
  
      // Reset modal sections
      document.getElementById('bookingSummarySection').style.display = 'block';
      document.getElementById('infoSection').style.display = 'none';
  
      // Fill modal fields
      document.getElementById("hotelType").textContent = hotelType;
      document.getElementById("hotelDescription").textContent = hotelDescription;
      document.getElementById("roomType").textContent = roomType;
      document.getElementById("roomDescription").textContent = roomDescription;
      document.getElementById("pricePerNight").value = roomPrice;

  
  
    
  
      // Trigger calculation and add event listeners
      calculateTotal();
      document.getElementById("room_count").addEventListener("change", calculateTotal);
      document.getElementById("nights").addEventListener("input", calculateTotal);
  
      // Show modal
      document.getElementById("bookingSummarySection").style.display = "block";
    });
  });
  
  
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
 
    
  function calculateTotal() {
    const rooms = parseInt(document.getElementById("room_count").value) || 1;
    const nights = parseInt(document.getElementById("nights").value) || 1;
    const pricePerNight = parseFloat(document.getElementById("pricePerNight").value) || 0;
  
    let total = rooms * nights * pricePerNight;
  
    const coupon = document.getElementById("summaryCoupon").value.trim();
    if (coupon === "SAVE10") {
      total *= 0.9;
    }
  
    document.getElementById("totalPrice").textContent = total.toFixed(2) + "\u00A0DZD";

    document.getElementById("finalAmount").value = total.toFixed(2);
  };
  
  
  
    window.applyCoupon = function () {
      const coupon = document.getElementById("summaryCoupon").value.trim();
      if (coupon === "SAVE10") {
        let totalElement = document.getElementById("totalPrice");
        let currentTotal = parseFloat(totalElement.textContent);
        let discountedTotal = currentTotal * 0.9;
        totalElement.textContent = discountedTotal.toFixed(2);
        alert("Coupon applied! 10% off.");
      } else {
        alert("Invalid coupon.");
      }
    };
    
    window.showInfoSection = function () {
      document.getElementById('infoSection').style.display = 'flex';
      document.getElementById('bookingSummarySection').style.display = 'none';
    };

    setTimeout(() => {
      const alert = document.querySelector('[style*="background-color: #d4edda"]');
      if (alert) {
          alert.style.transition = 'opacity 0.5s ease';
          alert.style.opacity = '0';
          setTimeout(() => alert.remove(), 500);
      }
  }, 4000);

  document.getElementById("nights").addEventListener("input", function() {
    updateCheckOutDate();
  });

  document.getElementById("check_in_date").addEventListener("change", function() {
    updateCheckOutDate();
  });

  function updateCheckOutDate() {
    const checkInDate = document.getElementById("check_in_date").value;
    const nights = document.getElementById("nights").value;
    
    if (checkInDate && nights) {
      const checkIn = new Date(checkInDate);
      checkIn.setDate(checkIn.getDate() + parseInt(nights));
      
      const checkOutDate = checkIn.toISOString().split('T')[0]; // Format as yyyy-mm-dd
      document.getElementById("check_out_date").value = checkOutDate;
    }
  };
});

