// === FEEDBACKS ===
let feedbacks = document.querySelectorAll(".feedback-card");
let feedbackIndex = 0;

function showFeedback(i) {
    feedbacks.forEach((card, idx) => {
        card.style.display = (idx === i || idx === i + 1) ? "block" : "none";
    });
}

function prevFeedback() {
    feedbackIndex = (feedbackIndex - 1 + feedbacks.length) % feedbacks.length;
    showFeedback(feedbackIndex);
}

function nextFeedback() {
    feedbackIndex = (feedbackIndex + 1) % feedbacks.length;
    showFeedback(feedbackIndex);
}

// Afficher les 2 premiers feedbacks au chargement
showFeedback(0);

function toggleContent(e) {
    e.preventDefault();
    const content = document.getElementById("more-content");
    const button = e.target;

    if (content.style.display === "none") {
      content.style.display = "block";
      button.textContent = "Show Less";
    } else {
      content.style.display = "none";
      button.textContent = "Read More";
    }
  }

  function toggleFAQ(e) {
    e.preventDefault();
    const moreFAQ = document.getElementById("more-faq");
    const link = e.target;

    if (moreFAQ.style.display === "none") {
      moreFAQ.style.display = "block";
      link.textContent = "Show less";
    } else {
      moreFAQ.style.display = "none";
      link.textContent = "See more questions";
      link.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  }


  function showFilter(filterId) {
    // Cacher tous les formulaires
    document.querySelectorAll('.filter-container').forEach(form => {
      form.style.display = 'none';
    });
  
    // Afficher le bon formulaire
    document.getElementById('filter-' + filterId).style.display = 'flex';
  
    // Mettre à jour les classes actives sur les boutons
    document.querySelectorAll('.filter-buttons button').forEach(button => {
      button.classList.remove('active');
    });
    document.getElementById('btn-' + filterId).classList.add('active');
  }
  
  // Activer par défaut un bouton au chargement
  window.addEventListener('DOMContentLoaded', () => {
    showFilter('flight'); // Change à 'hotel' ou 'package' si tu veux un autre par défaut
  });



 