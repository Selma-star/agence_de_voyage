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

// Afficher les 2 premiers feedbacks au chargement
showFeedback(0);
  // Ouvrir la modale
  document.querySelector(".view-more-link").addEventListener("click", function(e) {
    e.preventDefault();
    document.getElementById("photoModal").style.display = "block";
  });

  // Fermer la modale
  document.querySelector(".close-modal").addEventListener("click", function() {
    document.getElementById("photoModal").style.display = "none";
  });

  // Fermer en cliquant en dehors
  window.addEventListener("click", function(e) {
    if (e.target === document.getElementById("photoModal")) {
      document.getElementById("photoModal").style.display = "none";
    }
  });

